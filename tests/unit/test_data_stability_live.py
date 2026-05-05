from __future__ import annotations

from datetime import UTC, datetime

import pytest

from entropy.data.stability import read_data_stability_rows_jsonl
from entropy.evidence.data_stability_live import append_live_data_stability_snapshot
from entropy.evidence.simbroker_calibration_bootstrap import CalibrationQuoteTarget


def test_append_live_data_stability_snapshot_appends_and_rebuilds_summary(tmp_path) -> None:
    targets = (
        CalibrationQuoteTarget(
            symbol="BTC-USD",
            source_id="coinbase_exchange_public_api",
            source_symbol="BTC-USD",
            url="https://api.exchange.coinbase.com/products/BTC-USD/ticker",
            domain="api.exchange.coinbase.com",
        ),
        CalibrationQuoteTarget(
            symbol="ETH-USD",
            source_id="coinbase_exchange_public_api",
            source_symbol="ETH-USD",
            url="https://api.exchange.coinbase.com/products/ETH-USD/ticker",
            domain="api.exchange.coinbase.com",
        ),
    )

    first = append_live_data_stability_snapshot(
        output_dir=tmp_path,
        targets=targets,
        target_symbols=("BTC-USD", "ETH-USD"),
        fetch_json=_fake_coinbase_fetch,
        checked_at=datetime(2026, 5, 5, 12, 0, tzinfo=UTC),
    )
    second = append_live_data_stability_snapshot(
        output_dir=tmp_path,
        targets=targets,
        target_symbols=("BTC-USD", "ETH-USD"),
        fetch_json=_fake_coinbase_fetch,
        checked_at=datetime(2026, 5, 6, 12, 0, tzinfo=UTC),
    )

    rows = read_data_stability_rows_jsonl(second.rows_path)
    assert first.appended_rows == 2
    assert first.total_rows == 2
    assert first.summary.monitored_day_count == 1
    assert second.appended_rows == 2
    assert second.total_rows == 4
    assert second.summary.monitored_day_count == 2
    assert second.summary.missing_symbol_days == 0
    assert second.summary.unexplained_gap_count == 0
    assert second.summary.packet_status == "INCOMPLETE"
    assert len(rows) == 4
    assert second.snapshot_manifest_path.exists()
    assert second.summary_path.exists()


def test_append_live_data_stability_snapshot_rejects_same_day_collision(tmp_path) -> None:
    target = CalibrationQuoteTarget(
        symbol="BTC-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="BTC-USD",
        url="https://api.exchange.coinbase.com/products/BTC-USD/ticker",
        domain="api.exchange.coinbase.com",
    )
    checked_at = datetime(2026, 5, 5, 12, 0, tzinfo=UTC)

    append_live_data_stability_snapshot(
        output_dir=tmp_path,
        targets=(target,),
        target_symbols=("BTC-USD",),
        fetch_json=_fake_coinbase_fetch,
        checked_at=checked_at,
    )

    with pytest.raises(ValueError, match="monitor rows already exist"):
        append_live_data_stability_snapshot(
            output_dir=tmp_path,
            targets=(target,),
            target_symbols=("BTC-USD",),
            fetch_json=_fake_coinbase_fetch,
            checked_at=checked_at,
        )


def test_append_live_data_stability_snapshot_records_fetch_failures_as_gaps(tmp_path) -> None:
    target = CalibrationQuoteTarget(
        symbol="BTC-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="BTC-USD",
        url="https://api.exchange.coinbase.com/products/BTC-USD/ticker",
        domain="api.exchange.coinbase.com",
    )

    def failing_fetch(_url: str) -> dict[str, object]:
        raise RuntimeError("source unavailable")

    result = append_live_data_stability_snapshot(
        output_dir=tmp_path,
        targets=(target,),
        target_symbols=("BTC-USD",),
        fetch_json=failing_fetch,
        checked_at=datetime(2026, 5, 5, 12, 0, tzinfo=UTC),
    )

    rows = read_data_stability_rows_jsonl(result.rows_path)
    assert result.appended_rows == 1
    assert result.summary.unexplained_gap_count == 1
    assert rows[0].provider_status == "down"
    assert rows[0].gap_reason_code == "unknown_missing_bars"


def _fake_coinbase_fetch(url: str) -> dict[str, object]:
    symbol = "BTC-USD" if "BTC-USD" in url else "ETH-USD"
    if symbol == "BTC-USD":
        return {"bid": "100.00", "ask": "100.05", "time": "2026-05-05T12:00:00Z"}
    return {"bid": "50.00", "ask": "50.05", "time": "2026-05-05T12:00:00Z"}
