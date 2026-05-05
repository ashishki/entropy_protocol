"""Offline data-stability monitoring evidence tooling."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Literal, Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

STABILITY_METHOD_ID = "DATA-STABILITY-90D-v1"
NO_STABILITY_GATE_CLAIM = "not_phase_gate_approval"

CalendarProfile = Literal["weekday", "continuous"]
ProviderStatus = Literal["ok", "partial", "down", "unknown"]
CheckStatus = Literal["PASS", "FAIL"]
GapReasonCode = Literal[
    "market_closed",
    "provider_announced_outage",
    "asset_halt",
    "symbol_mapping_change",
    "late_arrival_corrected",
    "unknown_missing_bars",
    "timestamp_discontinuity",
    "ohlcv_invalid",
]
PacketStatus = Literal["INCOMPLETE", "INVALID", "FAIL", "PACKET_READY_FOR_REVIEW"]

UNEXPLAINED_GAP_REASONS = frozenset(
    {"unknown_missing_bars", "timestamp_discontinuity", "ohlcv_invalid"}
)


class DataStabilityRow(BaseModel):
    """One asset/day/timeframe monitoring row."""

    monitor_id: str = Field(min_length=1)
    monitor_date: date
    symbol: str = Field(min_length=1)
    timeframe: str = Field(min_length=1)
    calendar_profile: CalendarProfile
    provider: str = Field(min_length=1)
    provider_status: ProviderStatus
    expected_bars: int = Field(ge=0)
    observed_bars: int = Field(ge=0)
    first_ts: datetime | None = None
    last_ts: datetime | None = None
    timestamp_check: CheckStatus
    gap_check: CheckStatus
    ohlcv_sanity_check: CheckStatus
    dataset_hash: str = Field(min_length=1)
    raw_source_hash: str | None = None
    gap_candidate: bool
    gap_explained: bool
    gap_reason_code: GapReasonCode | None = None
    disposition_note_hash: str | None = None
    checked_at: datetime
    checker: str = Field(min_length=1)
    method_id: str = STABILITY_METHOD_ID
    evidence_claim: str = NO_STABILITY_GATE_CLAIM

    @field_validator(
        "monitor_id",
        "symbol",
        "timeframe",
        "provider",
        "dataset_hash",
        "checker",
        "method_id",
        "evidence_claim",
    )
    @classmethod
    def text_fields_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only identifiers."""
        if not value.strip():
            raise ValueError("text fields must not be blank")
        return value

    @field_validator("first_ts", "last_ts", "checked_at")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime | None) -> datetime | None:
        """Require timezone-aware UTC timestamps when supplied."""
        if value is None:
            return value
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamps must be timezone-aware UTC")
        return value

    @field_validator("raw_source_hash", "disposition_note_hash")
    @classmethod
    def optional_text_must_not_be_blank(cls, value: str | None) -> str | None:
        """Reject whitespace-only optional text when supplied."""
        if value is not None and not value.strip():
            raise ValueError("optional text fields must not be blank")
        return value

    @model_validator(mode="after")
    def validate_monitoring_state(self) -> "DataStabilityRow":
        """Validate timestamp coverage and gap disposition consistency."""
        if self.observed_bars > 0 and (self.first_ts is None or self.last_ts is None):
            raise ValueError("first_ts and last_ts are required when observed_bars > 0")
        if self.observed_bars == 0 and (self.first_ts is not None or self.last_ts is not None):
            raise ValueError("first_ts and last_ts must be omitted when observed_bars is zero")
        if self.first_ts is not None and self.last_ts is not None and self.last_ts < self.first_ts:
            raise ValueError("last_ts must be greater than or equal to first_ts")
        expected_gap_candidate = (
            self.observed_bars < self.expected_bars
            or self.timestamp_check == "FAIL"
            or self.gap_check == "FAIL"
            or self.ohlcv_sanity_check == "FAIL"
            or self.provider_status in {"partial", "down", "unknown"}
        )
        if self.gap_candidate is not expected_gap_candidate:
            raise ValueError("gap_candidate must reflect row status and check failures")
        if not self.gap_candidate:
            if self.gap_explained or self.gap_reason_code is not None:
                raise ValueError("non-gap rows must not carry gap explanation fields")
            return self
        if self.gap_reason_code is None:
            raise ValueError("gap_reason_code is required for gap candidates")
        if self.gap_explained:
            if self.gap_reason_code in UNEXPLAINED_GAP_REASONS:
                raise ValueError("unexplained reason codes cannot be marked explained")
            if self.disposition_note_hash is None:
                raise ValueError("disposition_note_hash is required for explained gaps")
        elif self.gap_reason_code not in UNEXPLAINED_GAP_REASONS:
            raise ValueError("explained reason codes must be marked gap_explained")
        return self


class DataStabilityAssetSummary(BaseModel):
    """Per-symbol monitoring summary."""

    symbol: str
    row_count: int
    expected_bars: int
    observed_bars: int
    explained_gap_count: int
    unexplained_gap_count: int
    failing_check_count: int


class DataStabilitySummary(BaseModel):
    """Aggregate data-stability packet summary."""

    method_id: str
    evidence_claim: str
    required_min_days: int
    monitored_day_count: int
    window_start: date | None
    window_end: date | None
    target_symbols: tuple[str, ...]
    total_rows: int
    missing_symbol_days: int
    explained_gap_count: int
    unexplained_gap_count: int
    missing_hash_rows: int
    packet_status: PacketStatus
    asset_summaries: tuple[DataStabilityAssetSummary, ...]


def build_data_stability_summary(
    rows: Sequence[DataStabilityRow],
    *,
    target_symbols: Sequence[str],
    min_days: int = 90,
) -> DataStabilitySummary:
    """Summarize data-stability monitor rows without approving the Phase 0 gate."""
    if min_days < 1:
        raise ValueError("min_days must be positive")
    resolved_symbols = tuple(_validate_target_symbols(target_symbols))
    _validate_unique_monitor_ids(rows)
    dates = sorted({row.monitor_date for row in rows})
    window_start = dates[0] if dates else None
    window_end = dates[-1] if dates else None
    monitored_day_count = _continuous_day_count(window_start, window_end)
    missing_symbol_days = _count_missing_symbol_days(rows, resolved_symbols, dates)
    explained_gap_count = sum(1 for row in rows if row.gap_candidate and row.gap_explained)
    unexplained_gap_count = sum(1 for row in rows if _row_has_unexplained_gap(row))
    missing_hash_rows = sum(1 for row in rows if not row.dataset_hash.strip())
    if monitored_day_count < min_days or missing_symbol_days > 0:
        packet_status = "INCOMPLETE"
    elif missing_hash_rows > 0:
        packet_status = "INVALID"
    elif unexplained_gap_count > 0:
        packet_status = "FAIL"
    else:
        packet_status = "PACKET_READY_FOR_REVIEW"
    return DataStabilitySummary(
        method_id=STABILITY_METHOD_ID,
        evidence_claim=NO_STABILITY_GATE_CLAIM,
        required_min_days=min_days,
        monitored_day_count=monitored_day_count,
        window_start=window_start,
        window_end=window_end,
        target_symbols=resolved_symbols,
        total_rows=len(rows),
        missing_symbol_days=missing_symbol_days,
        explained_gap_count=explained_gap_count,
        unexplained_gap_count=unexplained_gap_count,
        missing_hash_rows=missing_hash_rows,
        packet_status=packet_status,
        asset_summaries=_summarize_assets(rows),
    )


def render_data_stability_summary(summary: DataStabilitySummary) -> str:
    """Render a deterministic Markdown data-stability summary."""
    lines = [
        "# Data Stability Summary",
        "",
        f"Method ID: `{summary.method_id}`",
        f"Evidence claim: `{summary.evidence_claim}`",
        f"Packet status: `{summary.packet_status}`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Required monitored days | {summary.required_min_days} |",
        f"| Monitored day count | {summary.monitored_day_count} |",
        f"| Window start | {summary.window_start or ''} |",
        f"| Window end | {summary.window_end or ''} |",
        f"| Target symbols | {', '.join(summary.target_symbols)} |",
        f"| Total rows | {summary.total_rows} |",
        f"| Missing symbol-days | {summary.missing_symbol_days} |",
        f"| Explained gaps | {summary.explained_gap_count} |",
        f"| Unexplained gaps | {summary.unexplained_gap_count} |",
        "",
        "| Symbol | Rows | Expected bars | Observed bars | Explained gaps | Unexplained gaps | Failing checks |",
        "|--------|------|---------------|---------------|----------------|------------------|----------------|",
    ]
    for asset in summary.asset_summaries:
        lines.append(
            "| "
            f"{asset.symbol} | "
            f"{asset.row_count} | "
            f"{asset.expected_bars} | "
            f"{asset.observed_bars} | "
            f"{asset.explained_gap_count} | "
            f"{asset.unexplained_gap_count} | "
            f"{asset.failing_check_count} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this summary does not approve Phase 0, activate providers, "
            "or prove 90-day data stability without an approved continuous "
            "monitoring packet and manual review.",
        ]
    )
    return "\n".join(lines)


def write_data_stability_rows_jsonl(rows: Sequence[DataStabilityRow], path: Path) -> None:
    """Write validated monitoring rows as deterministic JSONL."""
    _validate_unique_monitor_ids(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(row.model_dump_json())
            handle.write("\n")


def read_data_stability_rows_jsonl(path: Path) -> tuple[DataStabilityRow, ...]:
    """Read monitoring rows from JSONL."""
    rows: list[DataStabilityRow] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(DataStabilityRow.model_validate_json(stripped))
            except ValueError as exc:
                raise ValueError(f"invalid data-stability row at line {line_number}") from exc
    _validate_unique_monitor_ids(rows)
    return tuple(rows)


def _validate_target_symbols(target_symbols: Sequence[str]) -> tuple[str, ...]:
    if not target_symbols:
        raise ValueError("target_symbols must not be empty")
    symbols = tuple(symbol.strip() for symbol in target_symbols)
    if any(not symbol for symbol in symbols):
        raise ValueError("target_symbols must not contain blanks")
    if len(set(symbols)) != len(symbols):
        raise ValueError("target_symbols must not contain duplicates")
    return symbols


def _validate_unique_monitor_ids(rows: Sequence[DataStabilityRow]) -> None:
    seen: set[str] = set()
    for row in rows:
        if row.monitor_id in seen:
            raise ValueError("duplicate monitor_id")
        seen.add(row.monitor_id)


def _continuous_day_count(window_start: date | None, window_end: date | None) -> int:
    if window_start is None or window_end is None:
        return 0
    return (window_end - window_start).days + 1


def _count_missing_symbol_days(
    rows: Sequence[DataStabilityRow],
    target_symbols: Sequence[str],
    dates: Sequence[date],
) -> int:
    present = {(row.symbol, row.monitor_date) for row in rows}
    return sum(
        1
        for symbol in target_symbols
        for monitor_date in dates
        if (symbol, monitor_date) not in present
    )


def _row_has_unexplained_gap(row: DataStabilityRow) -> bool:
    return row.gap_candidate and (
        not row.gap_explained or row.gap_reason_code in UNEXPLAINED_GAP_REASONS
    )


def _summarize_assets(rows: Sequence[DataStabilityRow]) -> tuple[DataStabilityAssetSummary, ...]:
    by_symbol: dict[str, list[DataStabilityRow]] = {}
    for row in rows:
        by_symbol.setdefault(row.symbol, []).append(row)
    summaries: list[DataStabilityAssetSummary] = []
    for symbol in sorted(by_symbol):
        symbol_rows = by_symbol[symbol]
        summaries.append(
            DataStabilityAssetSummary(
                symbol=symbol,
                row_count=len(symbol_rows),
                expected_bars=sum(row.expected_bars for row in symbol_rows),
                observed_bars=sum(row.observed_bars for row in symbol_rows),
                explained_gap_count=sum(
                    1 for row in symbol_rows if row.gap_candidate and row.gap_explained
                ),
                unexplained_gap_count=sum(
                    1 for row in symbol_rows if _row_has_unexplained_gap(row)
                ),
                failing_check_count=sum(
                    1
                    for row in symbol_rows
                    for status in (
                        row.timestamp_check,
                        row.gap_check,
                        row.ohlcv_sanity_check,
                    )
                    if status == "FAIL"
                ),
            )
        )
    return tuple(summaries)
