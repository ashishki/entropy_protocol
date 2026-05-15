from __future__ import annotations

import json

import pytest

from trader_risk_audit.exchange.snapshot import (
    FetchedPage,
    build_raw_exchange_snapshot,
)


def test_snapshot_schema_serializes_without_secrets() -> None:
    snapshot = build_raw_exchange_snapshot(
        exchange="bybit",
        market="linear",
        symbols=("BTCUSDT",),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-02T00:00:00Z",
        fetched_pages=(
            FetchedPage(
                endpoint_label="bybit.v5.execution.list",
                page_number=1,
                record_count=1,
                cursor="page_cursor_1",
            ),
        ),
        source_endpoint_labels=("bybit.v5.execution.list",),
        raw_records=(
            {
                "category": "linear",
                "exec_id": "synthetic_exec_bybit_001",
                "exec_price": "64000.50",
                "exec_qty": "0.010",
                "exec_time": "2026-04-01T12:00:00Z",
                "order_id": "synthetic_order_bybit_001",
                "side": "Buy",
                "source_row_id": "synthetic_bybit_row_001",
                "symbol": "BTCUSDT",
            },
        ),
    )

    rendered = snapshot.to_json()
    parsed = json.loads(rendered)

    assert parsed["exchange"] == "bybit"
    assert parsed["market"] == "linear"
    assert parsed["symbols"] == ["BTCUSDT"]
    assert parsed["source_endpoint_labels"] == ["bybit.v5.execution.list"]
    assert parsed["fetched_pages"][0]["record_count"] == 1
    assert parsed["raw_records"][0]["exec_id"] == "synthetic_exec_bybit_001"
    assert "api_key" not in rendered
    assert "api_secret" not in rendered
    assert "signature" not in rendered
    assert "account_id" not in rendered


def test_snapshot_schema_rejects_secret_fields() -> None:
    with pytest.raises(ValueError, match="forbidden field: api_key"):
        build_raw_exchange_snapshot(
            exchange="binance",
            market="spot",
            symbols=("BTCUSDT",),
            start_time="2026-04-01T00:00:00Z",
            end_time="2026-04-02T00:00:00Z",
            fetched_pages=(
                FetchedPage(
                    endpoint_label="binance.spot.my_trades",
                    page_number=1,
                    record_count=1,
                ),
            ),
            source_endpoint_labels=("binance.spot.my_trades",),
            raw_records=(
                {
                    "api_key": "fixture_api_key_123",
                    "price": "64010.00",
                    "quantity": "0.020",
                    "symbol": "BTCUSDT",
                },
            ),
        )
