"""Unit tests for data-stability monitoring tooling."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from pydantic import ValidationError

from entropy.data.stability import (
    NO_STABILITY_GATE_CLAIM,
    DataStabilityRow,
    build_data_stability_summary,
    read_data_stability_rows_jsonl,
    render_data_stability_summary,
    write_data_stability_rows_jsonl,
)

UTC_TS = datetime(2026, 5, 3, 12, 0, tzinfo=timezone.utc)


def test_data_stability_row_accepts_clean_monitoring_day() -> None:
    row = make_stability_row()

    assert row.gap_candidate is False
    assert row.gap_explained is False
    assert row.evidence_claim == NO_STABILITY_GATE_CLAIM


def test_data_stability_row_validates_gap_candidate_and_explanation() -> None:
    with pytest.raises(ValidationError, match="gap_candidate"):
        make_stability_row(observed_bars=23, gap_candidate=False)

    explained = make_stability_row(
        monitor_id="explained",
        provider_status="down",
        observed_bars=0,
        first_ts=None,
        last_ts=None,
        gap_candidate=True,
        gap_explained=True,
        gap_reason_code="provider_announced_outage",
        disposition_note_hash="note-hash",
    )

    assert explained.gap_explained is True

    with pytest.raises(ValidationError, match="unexplained reason"):
        make_stability_row(
            monitor_id="bad-explained",
            observed_bars=23,
            gap_candidate=True,
            gap_explained=True,
            gap_reason_code="unknown_missing_bars",
            disposition_note_hash="note-hash",
        )
    with pytest.raises(ValidationError, match="disposition_note_hash"):
        make_stability_row(
            monitor_id="missing-note",
            provider_status="down",
            observed_bars=0,
            first_ts=None,
            last_ts=None,
            gap_candidate=True,
            gap_explained=True,
            gap_reason_code="provider_announced_outage",
        )


def test_data_stability_row_validates_timestamps_and_hashes() -> None:
    with pytest.raises(ValidationError, match="timezone-aware UTC"):
        make_stability_row(first_ts=datetime(2026, 5, 3, 0, 0))
    with pytest.raises(ValidationError, match="last_ts"):
        make_stability_row(first_ts=UTC_TS, last_ts=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc))
    with pytest.raises(ValidationError, match="first_ts and last_ts"):
        make_stability_row(observed_bars=0)
    with pytest.raises(ValidationError, match="dataset_hash"):
        make_stability_row(dataset_hash="")


def test_data_stability_summary_counts_days_gaps_and_assets() -> None:
    rows = (
        make_stability_row(monitor_id="btc-1", symbol="BTC-USD", monitor_date=date(2026, 5, 1)),
        make_stability_row(monitor_id="eth-1", symbol="ETH-USD", monitor_date=date(2026, 5, 1)),
        make_stability_row(monitor_id="btc-2", symbol="BTC-USD", monitor_date=date(2026, 5, 2)),
        make_stability_row(
            monitor_id="eth-2",
            symbol="ETH-USD",
            monitor_date=date(2026, 5, 2),
            provider_status="down",
            expected_bars=24,
            observed_bars=0,
            first_ts=None,
            last_ts=None,
            gap_candidate=True,
            gap_explained=True,
            gap_reason_code="provider_announced_outage",
            disposition_note_hash="note-hash",
        ),
    )

    summary = build_data_stability_summary(rows, target_symbols=("BTC-USD", "ETH-USD"), min_days=2)
    rendered = render_data_stability_summary(summary)

    assert summary.monitored_day_count == 2
    assert summary.missing_symbol_days == 0
    assert summary.explained_gap_count == 1
    assert summary.unexplained_gap_count == 0
    assert summary.packet_status == "PACKET_READY_FOR_REVIEW"
    assert summary.asset_summaries[1].symbol == "ETH-USD"
    assert summary.asset_summaries[1].explained_gap_count == 1
    assert "not_phase_gate_approval" in rendered
    assert "does not approve Phase 0" in rendered


def test_data_stability_summary_reports_incomplete_and_failures() -> None:
    clean = make_stability_row(monitor_id="clean")
    unexplained = make_stability_row(
        monitor_id="gap",
        observed_bars=23,
        gap_candidate=True,
        gap_explained=False,
        gap_reason_code="unknown_missing_bars",
    )

    incomplete = build_data_stability_summary((clean,), target_symbols=("BTC-USD",), min_days=2)
    failed = build_data_stability_summary(
        (clean, unexplained), target_symbols=("BTC-USD",), min_days=1
    )

    assert incomplete.packet_status == "INCOMPLETE"
    assert failed.packet_status == "FAIL"
    assert failed.unexplained_gap_count == 1


def test_data_stability_summary_rejects_duplicate_monitor_ids() -> None:
    row = make_stability_row()

    with pytest.raises(ValueError, match="duplicate"):
        build_data_stability_summary((row, row), target_symbols=("BTC-USD",), min_days=1)
    with pytest.raises(ValueError, match="target_symbols"):
        build_data_stability_summary((row,), target_symbols=("BTC-USD", "BTC-USD"), min_days=1)


def test_data_stability_rows_jsonl_round_trip(tmp_path) -> None:
    rows = (
        make_stability_row(monitor_id="row-1"),
        make_stability_row(monitor_id="row-2", symbol="ETH-USD"),
    )
    path = tmp_path / "data_stability_rows.jsonl"

    write_data_stability_rows_jsonl(rows, path)
    loaded = read_data_stability_rows_jsonl(path)

    assert loaded == rows

    with pytest.raises(ValueError, match="duplicate"):
        write_data_stability_rows_jsonl((rows[0], rows[0]), tmp_path / "duplicate.jsonl")


def make_stability_row(**overrides: object) -> DataStabilityRow:
    data = {
        "monitor_id": "monitor-1",
        "monitor_date": date(2026, 5, 3),
        "symbol": "BTC-USD",
        "timeframe": "1h",
        "calendar_profile": "continuous",
        "provider": "manual-fixture",
        "provider_status": "ok",
        "expected_bars": 24,
        "observed_bars": 24,
        "first_ts": datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
        "last_ts": datetime(2026, 5, 3, 23, 0, tzinfo=timezone.utc),
        "timestamp_check": "PASS",
        "gap_check": "PASS",
        "ohlcv_sanity_check": "PASS",
        "dataset_hash": "dataset-hash",
        "raw_source_hash": "raw-source-hash",
        "gap_candidate": False,
        "gap_explained": False,
        "gap_reason_code": None,
        "disposition_note_hash": None,
        "checked_at": UTC_TS,
        "checker": "monitor-job",
    }
    data.update(overrides)
    return DataStabilityRow(**data)
