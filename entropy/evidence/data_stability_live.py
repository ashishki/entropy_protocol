"""Live data-stability append tooling for approved public quote snapshots."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Sequence

from entropy.data.stability import (
    DataStabilityRow,
    DataStabilitySummary,
    build_data_stability_summary,
    read_data_stability_rows_jsonl,
    render_data_stability_summary,
)
from entropy.evidence.data_stability_simulation import DEFAULT_STABILITY_SYMBOLS
from entropy.evidence.simbroker_calibration_bootstrap import (
    DEFAULT_QUOTE_TARGETS,
    CalibrationQuoteSnapshot,
    CalibrationQuoteTarget,
    FetchJson,
    collect_calibration_quote_bootstrap,
    fetch_json_url,
)

DATA_STABILITY_LIVE_APPEND_ID = "DATA-STABILITY-LIVE-APPEND-v1"


@dataclass(frozen=True)
class DataStabilityLiveAppendResult:
    """Result of one append-only live monitor run."""

    append_id: str
    monitor_date: str
    rows_path: Path
    summary_path: Path
    snapshot_manifest_path: Path
    appended_rows: int
    total_rows: int
    summary: DataStabilitySummary
    gate_claim_allowed: bool = False


def append_live_data_stability_snapshot(
    *,
    output_dir: Path | str,
    targets: Sequence[CalibrationQuoteTarget] = DEFAULT_QUOTE_TARGETS,
    target_symbols: Sequence[str] = DEFAULT_STABILITY_SYMBOLS,
    fetch_json: FetchJson = fetch_json_url,
    checked_at: datetime | None = None,
) -> DataStabilityLiveAppendResult:
    """Append one approved-source monitoring snapshot to cumulative evidence."""
    resolved_checked_at = checked_at or datetime.now(UTC)
    if resolved_checked_at.tzinfo is None or resolved_checked_at.utcoffset() is None:
        raise ValueError("checked_at must be timezone-aware")
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    rows_path = root / "DATA_STABILITY_ROWS.jsonl"
    summary_path = root / "DATA_STABILITY_SUMMARY.md"
    monitor_date = resolved_checked_at.date()
    snapshot_result = collect_calibration_quote_bootstrap(
        output_dir=root / "raw" / monitor_date.isoformat(),
        targets=targets,
        fetch_json=fetch_json,
        fetched_at=resolved_checked_at,
    )
    new_rows = tuple(
        _snapshot_to_monitor_row(
            snapshot=snapshot,
            monitor_date=monitor_date,
            checked_at=resolved_checked_at,
            sequence=index,
        )
        for index, snapshot in enumerate(snapshot_result.snapshots, start=1)
    )
    existing_rows = read_data_stability_rows_jsonl(rows_path) if rows_path.exists() else ()
    _validate_no_append_collisions(existing_rows, new_rows)
    _append_rows_jsonl(new_rows, rows_path)
    all_rows = existing_rows + new_rows
    summary = build_data_stability_summary(all_rows, target_symbols=target_symbols, min_days=90)
    summary_path.write_text(render_data_stability_summary(summary), encoding="utf-8")
    return DataStabilityLiveAppendResult(
        append_id=DATA_STABILITY_LIVE_APPEND_ID,
        monitor_date=monitor_date.isoformat(),
        rows_path=rows_path,
        summary_path=summary_path,
        snapshot_manifest_path=snapshot_result.manifest_path,
        appended_rows=len(new_rows),
        total_rows=len(all_rows),
        summary=summary,
    )


def _snapshot_to_monitor_row(
    *,
    snapshot: CalibrationQuoteSnapshot,
    monitor_date: date,
    checked_at: datetime,
    sequence: int,
) -> DataStabilityRow:
    monitor_id = (
        f"live-stability-{monitor_date.isoformat()}-"
        f"{snapshot.source_id}-{snapshot.source_symbol}-{sequence:03d}"
    )
    if snapshot.status == "DONE":
        if snapshot.quote_ts is None or snapshot.raw_sha256 is None:
            raise ValueError("successful snapshot must carry quote_ts and raw_sha256")
        quote_ts = datetime.fromisoformat(snapshot.quote_ts)
        return DataStabilityRow(
            monitor_id=monitor_id,
            monitor_date=monitor_date,
            symbol=snapshot.symbol,
            timeframe="quote_snapshot",
            calendar_profile="continuous",
            provider=snapshot.source_id,
            provider_status="ok",
            expected_bars=1,
            observed_bars=1,
            first_ts=quote_ts,
            last_ts=quote_ts,
            timestamp_check="PASS",
            gap_check="PASS",
            ohlcv_sanity_check="PASS",
            dataset_hash=snapshot.raw_sha256,
            raw_source_hash=snapshot.raw_sha256,
            gap_candidate=False,
            gap_explained=False,
            gap_reason_code=None,
            disposition_note_hash=None,
            checked_at=checked_at,
            checker="codex_live_data_stability_append",
        )
    error_hash = _hash_error_snapshot(snapshot)
    return DataStabilityRow(
        monitor_id=monitor_id,
        monitor_date=monitor_date,
        symbol=snapshot.symbol,
        timeframe="quote_snapshot",
        calendar_profile="continuous",
        provider=snapshot.source_id,
        provider_status="down",
        expected_bars=1,
        observed_bars=0,
        first_ts=None,
        last_ts=None,
        timestamp_check="FAIL",
        gap_check="FAIL",
        ohlcv_sanity_check="FAIL",
        dataset_hash=error_hash,
        raw_source_hash=None,
        gap_candidate=True,
        gap_explained=False,
        gap_reason_code="unknown_missing_bars",
        disposition_note_hash=None,
        checked_at=checked_at,
        checker="codex_live_data_stability_append",
    )


def _validate_no_append_collisions(
    existing_rows: Sequence[DataStabilityRow],
    new_rows: Sequence[DataStabilityRow],
) -> None:
    existing_ids = {row.monitor_id for row in existing_rows}
    collisions = sorted(row.monitor_id for row in new_rows if row.monitor_id in existing_ids)
    if collisions:
        raise ValueError("monitor rows already exist for this append: " + ", ".join(collisions))


def _append_rows_jsonl(rows: Sequence[DataStabilityRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(row.model_dump_json())
            handle.write("\n")


def _hash_error_snapshot(snapshot: CalibrationQuoteSnapshot) -> str:
    payload = "|".join(
        (
            snapshot.symbol,
            snapshot.source_id,
            snapshot.source_symbol,
            snapshot.url,
            snapshot.error or "unknown_error",
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
