from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.exchange.bybit import normalize_bybit_executions
from trader_risk_audit.trades.importers import serialize_trade_records

FIXTURE_ROOT = Path("tests/fixtures/exchange/bybit")


def test_bybit_executions_normalize_to_canonical_trades() -> None:
    fixture = json.loads((FIXTURE_ROOT / "executions.json").read_text(encoding="utf-8"))
    expected = (FIXTURE_ROOT / "expected_canonical_trades.json").read_text(
        encoding="utf-8"
    )

    result = normalize_bybit_executions(fixture["records"], category="linear")

    assert serialize_trade_records(result.trades) == expected.strip()
    assert result.warnings == ()


def test_bybit_normalizer_orders_same_timestamp_executions() -> None:
    expected = normalize_bybit_executions(
        (
            _execution("synthetic_exec_bybit_001", "synthetic_order_bybit_001"),
            _execution("synthetic_exec_bybit_002", "synthetic_order_bybit_002"),
            _execution("synthetic_exec_bybit_003", "synthetic_order_bybit_003"),
        ),
        category="linear",
    )
    records = (
        _execution("synthetic_exec_bybit_003", "synthetic_order_bybit_003"),
        _execution("synthetic_exec_bybit_001", "synthetic_order_bybit_001"),
        _execution("synthetic_exec_bybit_002", "synthetic_order_bybit_002"),
    )

    result = normalize_bybit_executions(records, category="linear")

    assert [trade.row_id for trade in result.trades] == [
        trade.row_id for trade in expected.trades
    ]
    assert [trade.source_row_number for trade in result.trades] == [1, 2, 3]


def test_bybit_unsupported_fields_are_reported_safely() -> None:
    records = (
        {
            **_execution("synthetic_exec_bybit_001", "synthetic_order_bybit_001"),
            "block_trade_id": "synthetic_block_trade_001",
            "closed_size": "0.010",
        },
    )

    result = normalize_bybit_executions(records, category="linear")
    rendered = "\n".join(
        f"{warning.source_ref}:{warning.field}:{warning.message}"
        for warning in result.warnings
    )

    assert [warning.field for warning in result.warnings] == [
        "block_trade_id",
        "closed_size",
    ]
    assert "unsupported Bybit execution field ignored" in rendered
    assert "synthetic_block_trade_001" not in rendered
    assert result.trades[0].symbol == "BTCUSDT"


def _execution(exec_id: str, order_id: str) -> dict[str, object]:
    return {
        "category": "linear",
        "exec_fee": "0.44",
        "exec_id": exec_id,
        "exec_price": "64000.50",
        "exec_qty": "0.010",
        "exec_time": "2026-04-01T12:00:00Z",
        "fee_currency": "USDT",
        "is_maker": False,
        "order_id": order_id,
        "side": "Buy",
        "source_row_id": exec_id.replace("exec", "row"),
        "symbol": "BTCUSDT",
    }
