"""Fixture-only data-stability simulation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Sequence

from entropy.data.stability import (
    DataStabilityRow,
    DataStabilitySummary,
    build_data_stability_summary,
    render_data_stability_summary,
    write_data_stability_rows_jsonl,
)

DATA_STABILITY_SIMULATION_ID = "DATA-STABILITY-SIM-90D-v1"
DEFAULT_STABILITY_SYMBOLS = ("BTC-USD", "ETH-USD", "LTC-USD", "BCH-USD", "XLM-USD")


@dataclass(frozen=True)
class DataStabilitySimulationResult:
    """Fixture simulation result and artifact paths."""

    simulation_id: str
    rows_path: Path
    summary_path: Path
    row_count: int
    summary: DataStabilitySummary
    gate_claim_allowed: bool = False
    fixture_only: bool = True


def generate_fixture_stability_window(
    *,
    output_dir: Path | str,
    start_date: date,
    day_count: int = 90,
    target_symbols: Sequence[str] = DEFAULT_STABILITY_SYMBOLS,
) -> DataStabilitySimulationResult:
    """Generate a fixture-only continuous data-stability window."""
    if day_count < 1:
        raise ValueError("day_count must be positive")
    if not target_symbols:
        raise ValueError("target_symbols must not be empty")
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    rows: list[DataStabilityRow] = []
    checked_at = datetime.combine(start_date, time(23, 59), tzinfo=UTC)
    for day_offset in range(day_count):
        monitor_date = start_date + timedelta(days=day_offset)
        first_ts = datetime.combine(monitor_date, time(0, 0), tzinfo=UTC)
        for symbol_index, symbol in enumerate(target_symbols, start=1):
            rows.append(
                DataStabilityRow(
                    monitor_id=(f"fixture-stability-{monitor_date.isoformat()}-{symbol_index:02d}"),
                    monitor_date=monitor_date,
                    symbol=symbol,
                    timeframe="quote_snapshot",
                    calendar_profile="continuous",
                    provider="fixture_simulated_provider",
                    provider_status="ok",
                    expected_bars=1,
                    observed_bars=1,
                    first_ts=first_ts,
                    last_ts=first_ts,
                    timestamp_check="PASS",
                    gap_check="PASS",
                    ohlcv_sanity_check="PASS",
                    dataset_hash=f"fixture_dataset_hash_{monitor_date.isoformat()}_{symbol}",
                    raw_source_hash=f"fixture_raw_hash_{monitor_date.isoformat()}_{symbol}",
                    gap_candidate=False,
                    gap_explained=False,
                    gap_reason_code=None,
                    disposition_note_hash=None,
                    checked_at=checked_at + timedelta(days=day_offset),
                    checker="fixture_data_stability_simulation",
                )
            )
    rows_path = root / "DATA_STABILITY_SIMULATION_ROWS.jsonl"
    summary_path = root / "DATA_STABILITY_SIMULATION_SUMMARY.md"
    write_data_stability_rows_jsonl(tuple(rows), rows_path)
    summary = build_data_stability_summary(tuple(rows), target_symbols=target_symbols, min_days=90)
    summary_path.write_text(render_data_stability_summary(summary), encoding="utf-8")
    return DataStabilitySimulationResult(
        simulation_id=DATA_STABILITY_SIMULATION_ID,
        rows_path=rows_path,
        summary_path=summary_path,
        row_count=len(rows),
        summary=summary,
    )
