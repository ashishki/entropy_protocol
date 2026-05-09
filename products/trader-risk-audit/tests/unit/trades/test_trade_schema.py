from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

import pytest

from trader_risk_audit.trades.schema import TradeRecord, TradeValidationError


def test_valid_trade_record_generates_stable_row_id() -> None:
    fixture = Path("tests/fixtures/trades/valid_trades.csv")
    with fixture.open(newline="", encoding="utf-8") as trade_file:
        row = next(csv.DictReader(trade_file))

    record = TradeRecord.from_mapping(row)
    repeated = TradeRecord.from_mapping(row)

    assert record.row_id == repeated.row_id
    assert record.row_id.startswith("trade_")
    assert record.timestamp.isoformat() == "2026-01-15T09:30:00+00:00"
    assert record.symbol == "EURUSD"
    assert record.side == "buy"
    assert record.quantity == Decimal("1000")
    assert record.price == Decimal("1.0842")
    assert record.fees == Decimal("1.25")
    assert record.account_id == "acct_demo_001"
    assert record.source_file == "valid_trades.csv"
    assert record.source_row_number == 2


def test_missing_required_fields_report_canonical_names() -> None:
    with pytest.raises(TradeValidationError) as error:
        TradeRecord.from_mapping(
            {
                "fees": "0",
                "account_id": "acct_demo_001",
                "source_file": "missing.csv",
                "source_row_number": "3",
            }
        )

    assert error.value.fields == ("timestamp", "symbol", "side", "quantity", "price")
    message = str(error.value)
    for field in ("timestamp", "symbol", "side", "quantity", "price"):
        assert field in message


def test_side_normalization_rejects_unknown_values() -> None:
    accepted = TradeRecord.from_mapping(
        {
            "timestamp": "2026-01-15T09:30:00Z",
            "symbol": "EURUSD",
            "side": "LONG",
            "quantity": "1000",
            "price": "1.0842",
            "fees": "1.25",
            "account_id": "acct_demo_001",
            "source_file": "valid_trades.csv",
            "source_row_number": "2",
        },
        side_aliases={"buy": {"long"}, "sell": {"short"}},
    )
    assert accepted.side == "buy"

    with pytest.raises(TradeValidationError) as error:
        TradeRecord.from_mapping(
            {
                "timestamp": "2026-01-15T09:30:00Z",
                "symbol": "EURUSD",
                "side": "hold",
                "quantity": "1000",
                "price": "1.0842",
                "fees": "1.25",
                "account_id": "acct_demo_001",
                "source_file": "valid_trades.csv",
                "source_row_number": "2",
            },
            side_aliases={"buy": {"long"}, "sell": {"short"}},
        )

    assert error.value.fields == ("side",)
