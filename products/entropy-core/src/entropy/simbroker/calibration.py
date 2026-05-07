"""Bid/ask calibration interface for future SimBroker provider work."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Literal, Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

from entropy.models.registry import FillLog, FillSide

CALIBRATION_METHOD_ID = "SB-CAL-15PCT-v1"
NO_GATE_CLAIM = "not_phase_gate_approval"
DEFAULT_QUOTE_TOLERANCE = timedelta(minutes=5)


class BidAskQuote(BaseModel):
    """One bid/ask observation from an external or recorded market-data source."""

    symbol: str = Field(min_length=1)
    timestamp: datetime
    bid: float = Field(gt=0.0)
    ask: float = Field(gt=0.0)

    @field_validator("symbol")
    @classmethod
    def symbol_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only symbols."""
        if not value.strip():
            raise ValueError("symbol must not be blank")
        return value

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC quote timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be timezone-aware UTC")
        return value

    @model_validator(mode="after")
    def validate_spread(self) -> "BidAskQuote":
        """Require a non-inverted spread."""
        if self.ask < self.bid:
            raise ValueError("ask must be greater than or equal to bid")
        return self


class BidAskProvider(ABC):
    """Abstract bid/ask lookup boundary for Phase 1+ broker calibration work."""

    @abstractmethod
    def get_bid_ask(self, symbol: str, timestamp: datetime) -> BidAskQuote | None:
        """Return a bid/ask quote for the symbol and timestamp, or None if unavailable."""
        raise NotImplementedError


class NoOpBidAskProvider(BidAskProvider):
    """Phase 0 placeholder provider that never returns broker calibration data."""

    def get_bid_ask(self, symbol: str, timestamp: datetime) -> None:
        """Return no quote without contacting external systems."""
        return None


class CalibrationRow(BaseModel):
    """One manually verified SimBroker calibration row."""

    calibration_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    asset_class: str | None = None
    side: FillSide
    fill_ts: datetime
    quote_ts: datetime
    quote_source: str = Field(min_length=1)
    quote_source_hash: str = Field(min_length=1)
    bid: Decimal = Field(gt=Decimal("0"))
    ask: Decimal = Field(gt=Decimal("0"))
    mid: Decimal = Field(gt=Decimal("0"))
    spread: Decimal = Field(ge=Decimal("0"))
    simbroker_fill_price: Decimal = Field(gt=Decimal("0"))
    bar_open: Decimal | None = None
    bar_high: Decimal | None = None
    bar_low: Decimal | None = None
    bar_close: Decimal | None = None
    quantity: Decimal = Field(gt=Decimal("0"))
    commission: Decimal = Field(ge=Decimal("0"))
    slippage: Decimal = Field(ge=Decimal("0"))
    market_impact: Decimal = Field(ge=Decimal("0"))
    borrow_rate: Decimal = Field(ge=Decimal("0"))
    funding_rate: Decimal = Field(ge=Decimal("0"))
    total_cost: Decimal = Field(ge=Decimal("0"))
    reference_price: Decimal = Field(gt=Decimal("0"))
    absolute_deviation: Decimal = Field(ge=Decimal("0"))
    pct_deviation: Decimal = Field(ge=Decimal("0"))
    pass_15pct: bool
    manual_verifier: str = Field(min_length=1)
    manual_verification_ts: datetime
    exclusion_reason: str | None = None
    method_id: str = CALIBRATION_METHOD_ID
    evidence_claim: str = NO_GATE_CLAIM

    @field_validator(
        "calibration_id",
        "symbol",
        "quote_source",
        "quote_source_hash",
        "manual_verifier",
        "method_id",
        "evidence_claim",
    )
    @classmethod
    def text_fields_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only identifiers."""
        if not value.strip():
            raise ValueError("text fields must not be blank")
        return value

    @field_validator("fill_ts", "quote_ts", "manual_verification_ts")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamps must be timezone-aware UTC")
        return value

    @field_validator("asset_class", "exclusion_reason")
    @classmethod
    def optional_text_must_not_be_blank(cls, value: str | None) -> str | None:
        """Reject whitespace-only optional text when supplied."""
        if value is not None and not value.strip():
            raise ValueError("optional text fields must not be blank")
        return value

    @model_validator(mode="after")
    def validate_calibration_math(self) -> "CalibrationRow":
        """Validate quote math, side reference, and 15% pass flag."""
        if self.ask < self.bid:
            raise ValueError("ask must be greater than or equal to bid")
        if self.mid != (self.bid + self.ask) / Decimal("2"):
            raise ValueError("mid must equal (bid + ask) / 2")
        if self.spread != self.ask - self.bid:
            raise ValueError("spread must equal ask - bid")
        expected_reference = self.ask if self.side == FillSide.BUY else self.bid
        if self.reference_price != expected_reference:
            raise ValueError("reference_price must equal ask for buys and bid for sells")
        expected_deviation = abs(self.simbroker_fill_price - self.reference_price)
        if self.absolute_deviation != expected_deviation:
            raise ValueError("absolute_deviation must match fill/reference distance")
        expected_pct = expected_deviation / self.reference_price
        if self.pct_deviation != expected_pct:
            raise ValueError("pct_deviation must equal absolute_deviation / reference_price")
        expected_pass = self.pct_deviation <= Decimal("0.15")
        if self.pass_15pct is not expected_pass:
            raise ValueError("pass_15pct must reflect pct_deviation <= 0.15")
        return self


class CalibrationAssetSummary(BaseModel):
    """Per-symbol calibration summary for included rows."""

    symbol: str
    included_count: int
    pass_count: int
    max_pct_deviation: Decimal
    median_pct_deviation: Decimal
    p95_pct_deviation: Decimal


class CalibrationSummary(BaseModel):
    """Aggregate SimBroker calibration summary."""

    method_id: str
    evidence_claim: str
    required_min_rows: int
    total_rows: int
    included_rows: int
    excluded_rows: int
    pass_count: int
    failure_count: int
    all_included_passed: bool
    meets_min_rows: bool
    packet_status: Literal["INCOMPLETE", "FAIL", "PACKET_READY_FOR_REVIEW"]
    asset_summaries: tuple[CalibrationAssetSummary, ...]


def build_calibration_summary(
    rows: Sequence[CalibrationRow],
    *,
    min_included_rows: int = 100,
) -> CalibrationSummary:
    """Summarize validated SimBroker calibration rows without approving a gate."""
    if min_included_rows < 1:
        raise ValueError("min_included_rows must be positive")
    _validate_unique_calibration_ids(rows)
    included_rows = tuple(row for row in rows if row.exclusion_reason is None)
    excluded_count = len(rows) - len(included_rows)
    pass_count = sum(1 for row in included_rows if row.pass_15pct)
    failure_count = len(included_rows) - pass_count
    meets_min_rows = len(included_rows) >= min_included_rows
    all_included_passed = failure_count == 0
    if not meets_min_rows:
        packet_status = "INCOMPLETE"
    elif not all_included_passed:
        packet_status = "FAIL"
    else:
        packet_status = "PACKET_READY_FOR_REVIEW"
    return CalibrationSummary(
        method_id=CALIBRATION_METHOD_ID,
        evidence_claim=NO_GATE_CLAIM,
        required_min_rows=min_included_rows,
        total_rows=len(rows),
        included_rows=len(included_rows),
        excluded_rows=excluded_count,
        pass_count=pass_count,
        failure_count=failure_count,
        all_included_passed=all_included_passed,
        meets_min_rows=meets_min_rows,
        packet_status=packet_status,
        asset_summaries=_summarize_assets(included_rows),
    )


def build_calibration_row_from_fill(
    *,
    calibration_id: str,
    fill: FillLog,
    quote: BidAskQuote,
    quote_source: str,
    quote_source_hash: str,
    manual_verifier: str,
    manual_verification_ts: datetime,
    asset_class: str | None = "crypto",
    quote_tolerance: timedelta = DEFAULT_QUOTE_TOLERANCE,
    bar_open: Decimal | None = None,
    bar_high: Decimal | None = None,
    bar_low: Decimal | None = None,
    bar_close: Decimal | None = None,
    exclusion_reason: str | None = None,
) -> CalibrationRow:
    """Build one manually reviewed calibration row from a fill and approved quote."""
    if fill.symbol != quote.symbol:
        raise ValueError("fill and quote symbols must match")
    if quote_tolerance < timedelta(0):
        raise ValueError("quote_tolerance must be nonnegative")
    reference_price = (
        Decimal(str(quote.ask)) if fill.side == FillSide.BUY else Decimal(str(quote.bid))
    )
    absolute_deviation = abs(fill.fill_price - reference_price)
    pct_deviation = absolute_deviation / reference_price
    row_exclusion = exclusion_reason
    if abs(fill.timestamp - quote.timestamp) > quote_tolerance and row_exclusion is None:
        row_exclusion = "quote_timestamp_outside_tolerance"
    bid = Decimal(str(quote.bid))
    ask = Decimal(str(quote.ask))
    return CalibrationRow(
        calibration_id=calibration_id,
        symbol=fill.symbol,
        asset_class=asset_class,
        side=fill.side,
        fill_ts=fill.timestamp,
        quote_ts=quote.timestamp,
        quote_source=quote_source,
        quote_source_hash=quote_source_hash,
        bid=bid,
        ask=ask,
        mid=(bid + ask) / Decimal("2"),
        spread=ask - bid,
        simbroker_fill_price=fill.fill_price,
        bar_open=bar_open,
        bar_high=bar_high,
        bar_low=bar_low,
        bar_close=bar_close,
        quantity=fill.quantity,
        commission=fill.commission,
        slippage=fill.slippage,
        market_impact=fill.market_impact,
        borrow_rate=fill.borrow_rate,
        funding_rate=fill.funding_rate,
        total_cost=fill.total_cost,
        reference_price=reference_price,
        absolute_deviation=absolute_deviation,
        pct_deviation=pct_deviation,
        pass_15pct=pct_deviation <= Decimal("0.15"),
        manual_verifier=manual_verifier,
        manual_verification_ts=manual_verification_ts,
        exclusion_reason=row_exclusion,
    )


def render_calibration_summary(summary: CalibrationSummary) -> str:
    """Render a deterministic Markdown calibration summary."""
    lines = [
        "# SimBroker Calibration Summary",
        "",
        f"Method ID: `{summary.method_id}`",
        f"Evidence claim: `{summary.evidence_claim}`",
        f"Packet status: `{summary.packet_status}`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Required included rows | {summary.required_min_rows} |",
        f"| Total rows | {summary.total_rows} |",
        f"| Included rows | {summary.included_rows} |",
        f"| Excluded rows | {summary.excluded_rows} |",
        f"| Pass count | {summary.pass_count} |",
        f"| Failure count | {summary.failure_count} |",
        "",
        "| Symbol | Included | Pass | Max pct deviation | Median pct deviation | P95 pct deviation |",
        "|--------|----------|------|-------------------|----------------------|-------------------|",
    ]
    for asset in summary.asset_summaries:
        lines.append(
            "| "
            f"{asset.symbol} | "
            f"{asset.included_count} | "
            f"{asset.pass_count} | "
            f"{asset.max_pct_deviation} | "
            f"{asset.median_pct_deviation} | "
            f"{asset.p95_pct_deviation} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this summary does not approve Phase 0, activate providers, "
            "or prove real SimBroker calibration without approved quote evidence "
            "and approved verification review.",
        ]
    )
    return "\n".join(lines)


def write_calibration_rows_jsonl(rows: Sequence[CalibrationRow], path: Path) -> None:
    """Write validated calibration rows as deterministic JSONL."""
    _validate_unique_calibration_ids(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(row.model_dump_json())
            handle.write("\n")


def read_calibration_rows_jsonl(path: Path) -> tuple[CalibrationRow, ...]:
    """Read calibration rows from JSONL."""
    rows: list[CalibrationRow] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(CalibrationRow.model_validate_json(stripped))
            except ValueError as exc:
                raise ValueError(f"invalid calibration row at line {line_number}") from exc
    _validate_unique_calibration_ids(rows)
    return tuple(rows)


def _validate_unique_calibration_ids(rows: Sequence[CalibrationRow]) -> None:
    seen: set[str] = set()
    for row in rows:
        if row.calibration_id in seen:
            raise ValueError("duplicate calibration_id")
        seen.add(row.calibration_id)


def _summarize_assets(rows: Sequence[CalibrationRow]) -> tuple[CalibrationAssetSummary, ...]:
    by_symbol: dict[str, list[CalibrationRow]] = {}
    for row in rows:
        by_symbol.setdefault(row.symbol, []).append(row)
    summaries: list[CalibrationAssetSummary] = []
    for symbol in sorted(by_symbol):
        symbol_rows = by_symbol[symbol]
        deviations = sorted(row.pct_deviation for row in symbol_rows)
        summaries.append(
            CalibrationAssetSummary(
                symbol=symbol,
                included_count=len(symbol_rows),
                pass_count=sum(1 for row in symbol_rows if row.pass_15pct),
                max_pct_deviation=max(deviations),
                median_pct_deviation=_quantile_decimal(deviations, Decimal("0.5")),
                p95_pct_deviation=_quantile_decimal(deviations, Decimal("0.95")),
            )
        )
    return tuple(summaries)


def _quantile_decimal(values: Sequence[Decimal], q: Decimal) -> Decimal:
    if not values:
        raise ValueError("values must not be empty")
    if q < 0 or q > 1:
        raise ValueError("q must be in [0, 1]")
    index = q * Decimal(len(values) - 1)
    lower_index = int(index)
    upper_index = min(lower_index + 1, len(values) - 1)
    weight = index - Decimal(lower_index)
    return values[lower_index] * (Decimal("1") - weight) + values[upper_index] * weight
