from __future__ import annotations

from trader_risk_audit.exchange.normalizer import (
    ExchangeNormalizationError,
    normalize_exchange_records,
)
from trader_risk_audit.trades.importers import serialize_trade_records


def test_exchange_normalizer_emits_stable_row_ids() -> None:
    first = normalize_exchange_records(
        exchange="bybit",
        market="linear",
        records=(
            {
                "category": "linear",
                "exec_id": "synthetic_exec_bybit_001",
                "exec_price": "64000.50",
                "exec_qty": "0.010",
                "exec_time": "2026-04-01T12:00:00Z",
                "order_id": "synthetic_order_bybit_001",
                "side": "Buy",
                "symbol": "BTCUSDT",
            },
        ),
    )
    repeated = normalize_exchange_records(
        exchange="bybit",
        market="linear",
        records=(
            {
                "category": "linear",
                "exec_id": "synthetic_exec_bybit_001",
                "exec_price": "64000.50",
                "exec_qty": "0.010",
                "exec_time": "2026-04-01T12:00:00Z",
                "order_id": "synthetic_order_bybit_001",
                "side": "Buy",
                "symbol": "BTCUSDT",
            },
        ),
    )

    assert first[0].row_id == repeated[0].row_id
    assert first[0].row_id.startswith("exchange_")
    assert first[0].symbol == "BTCUSDT"
    assert first[0].side == "buy"
    assert first[0].source_file == "exchange:bybit:linear"
    assert first[0].account_id == "bybit_read_only_import"


def test_exchange_normalizer_reports_safe_missing_field_errors() -> None:
    raw_marker = "private note: fixture raw row must not leak"
    try:
        normalize_exchange_records(
            exchange="binance",
            market="spot",
            records=(
                {
                    "commission": "0.00002",
                    "private_note": raw_marker,
                    "symbol": "BTCUSDT",
                    "time": "2026-04-01T12:05:00Z",
                    "trade_id": "synthetic_trade_binance_001",
                },
            ),
        )
    except ExchangeNormalizationError as exc:
        rendered = str(exc)
        assert exc.fields == ("side", "quantity", "price")
        assert "record 1 side: required field is missing" in rendered
        assert raw_marker not in rendered
        assert "synthetic_trade_binance_001" not in rendered
    else:
        raise AssertionError("missing fields should fail normalization")


def test_exchange_normalization_is_deterministic() -> None:
    records = (
        {
            "commission": "0.00002",
            "commission_asset": "BTC",
            "is_buyer": True,
            "order_id": "synthetic_order_binance_001",
            "price": "64010.00",
            "quantity": "0.020",
            "symbol": "BTCUSDT",
            "time": "2026-04-01T12:05:00Z",
            "trade_id": "synthetic_trade_binance_001",
        },
        {
            "commission": "1.20",
            "exec_id": "synthetic_exec_bybit_001",
            "exec_price": "64000.50",
            "exec_qty": "0.010",
            "exec_time": "2026-04-01T12:00:00Z",
            "order_id": "synthetic_order_bybit_001",
            "side": "Sell",
            "symbol": "BTCUSDT",
        },
    )

    first = serialize_trade_records(
        normalize_exchange_records(exchange="binance", market="spot", records=records)
    )
    second = serialize_trade_records(
        normalize_exchange_records(exchange="binance", market="spot", records=records)
    )

    assert first == second
