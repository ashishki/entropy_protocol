from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from entropy.evidence.simbroker_calibration_bootstrap import (
    CalibrationQuoteTarget,
    collect_calibration_quote_bootstrap,
    render_calibration_quote_bootstrap_summary,
)


def test_collect_calibration_quote_bootstrap_writes_manifest_and_raw_extracts(tmp_path) -> None:
    targets = (
        CalibrationQuoteTarget(
            symbol="BTC-USD",
            source_id="coinbase_exchange_public_api",
            source_symbol="BTC-USD",
            url="https://api.exchange.coinbase.com/products/BTC-USD/ticker",
            domain="api.exchange.coinbase.com",
        ),
        CalibrationQuoteTarget(
            symbol="BTC-USD",
            source_id="kraken_public_api",
            source_symbol="XBTUSD",
            url="https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
            domain="api.kraken.com",
        ),
    )

    def fake_fetch(url: str) -> dict[str, object]:
        if "coinbase" in url:
            return {"bid": "100.00", "ask": "100.05", "time": "2026-05-05T00:00:00Z"}
        return {
            "error": [],
            "result": {"XXBTZUSD": {"b": ["100.01", "1", "1.0"], "a": ["100.06", "1", "1.0"]}},
        }

    result = collect_calibration_quote_bootstrap(
        output_dir=tmp_path,
        targets=targets,
        fetch_json=fake_fetch,
        fetched_at=datetime(2026, 5, 5, 0, 1, tzinfo=UTC),
    )

    assert result.done_count == 2
    assert result.failed_count == 0
    assert result.gate_claim_allowed is False
    assert result.calibration_rows_created is False
    assert result.manual_verification_complete is False
    assert result.manifest_path.exists()
    assert result.summary_path.exists()
    assert all(snapshot.raw_path for snapshot in result.snapshots)
    assert all(snapshot.raw_sha256 for snapshot in result.snapshots)

    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert payload["evidence_claim"] == "not_phase_gate_approval"
    assert payload["done_count"] == 2
    assert payload["manual_verification_complete"] is False

    summary = render_calibration_quote_bootstrap_summary(result)
    assert "Boundary:" in summary
    assert "does not create manually verified calibration rows" in summary


def test_collect_calibration_quote_bootstrap_records_failures(tmp_path) -> None:
    target = CalibrationQuoteTarget(
        symbol="BTC-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="BTC-USD",
        url="https://api.exchange.coinbase.com/products/BTC-USD/ticker",
        domain="api.exchange.coinbase.com",
    )

    def fake_fetch(_url: str) -> dict[str, object]:
        raise RuntimeError("network unavailable")

    result = collect_calibration_quote_bootstrap(
        output_dir=tmp_path,
        targets=(target,),
        fetch_json=fake_fetch,
        fetched_at=datetime(2026, 5, 5, 0, 1, tzinfo=UTC),
    )

    assert result.done_count == 0
    assert result.failed_count == 1
    assert result.snapshots[0].status == "FAILED"
    assert result.snapshots[0].error == "network unavailable"


def test_collect_calibration_quote_bootstrap_validates_approved_sources(tmp_path) -> None:
    target = CalibrationQuoteTarget(
        symbol="BTC-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="BTC-USD",
        url="https://example.com/ticker",
        domain="example.com",
    )

    with pytest.raises(ValueError, match="domain example.com is not approved"):
        collect_calibration_quote_bootstrap(
            output_dir=tmp_path,
            targets=(target,),
            fetch_json=lambda _url: {},
            fetched_at=datetime(2026, 5, 5, 0, 1, tzinfo=UTC),
        )
