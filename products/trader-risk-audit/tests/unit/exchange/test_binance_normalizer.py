from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.exchange.binance import normalize_binance_spot_trades
from trader_risk_audit.trades.importers import serialize_trade_records

FIXTURE_ROOT = Path("tests/fixtures/exchange/binance")


def test_binance_trades_normalize_to_canonical_trades() -> None:
    fixture = json.loads((FIXTURE_ROOT / "my_trades.json").read_text(encoding="utf-8"))
    expected = (FIXTURE_ROOT / "expected_canonical_trades.json").read_text(
        encoding="utf-8"
    )

    result = normalize_binance_spot_trades(fixture["records"])

    assert serialize_trade_records(result.trades) == expected.strip()
    assert result.warnings == ()


def test_binance_normalizer_emits_stable_row_ids() -> None:
    result = normalize_binance_spot_trades(
        (
            {
                "commission": "0.01",
                "commission_asset": "USDT",
                "is_buyer": True,
                "is_maker": False,
                "order_id": "synthetic_order_123",
                "price": "10",
                "quantity": "2",
                "symbol": "BNBUSDT",
                "time": "2026-04-01T12:00:00Z",
                "trade_id": "synthetic_trade_456",
            },
        )
    )

    assert result.trades[0].row_id == (
        "binance_spot_BNBUSDT_synthetic_order_123_synthetic_trade_456_"
        "2026-04-01T12:00:00Z"
    )


def test_binance_unsupported_fields_are_reported_safely() -> None:
    records = (
        {
            "buyer_order_private_note": "synthetic_note_do_not_render",
            "commission": "0.01",
            "commission_asset": "USDT",
            "is_buyer": False,
            "is_maker": True,
            "order_id": "synthetic_order_123",
            "price": "10",
            "quantity": "2",
            "symbol": "BNBUSDT",
            "time": "2026-04-01T12:00:00Z",
            "trade_id": "synthetic_trade_456",
        },
    )

    result = normalize_binance_spot_trades(records)
    rendered_warnings = "\n".join(
        f"{warning.source_ref}:{warning.field}:{warning.message}"
        for warning in result.warnings
    )

    assert result.trades[0].fees.to_eng_string() == "0.01"
    assert result.metadata[0].fee_asset == "USDT"
    assert result.metadata[0].liquidity == "maker"
    assert [warning.field for warning in result.warnings] == [
        "buyer_order_private_note"
    ]
    assert "unsupported Binance spot trade field ignored" in rendered_warnings
    assert "synthetic_note_do_not_render" not in rendered_warnings
