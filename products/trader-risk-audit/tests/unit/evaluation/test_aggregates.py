from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from trader_risk_audit.evaluation.aggregates import (
    build_daily_aggregates,
    build_equity_curve,
)
from trader_risk_audit.evaluation.calendar import assign_session_date
from trader_risk_audit.trades.schema import TradeRecord


def test_trades_assign_to_configured_session_date() -> None:
    before_session = TradeRecord.from_mapping(
        {
            "timestamp": "2026-01-15T13:00:00Z",
            "symbol": "EURUSD",
            "side": "buy",
            "quantity": "1",
            "price": "1",
            "fees": "0",
            "account_id": "acct_demo_001",
            "source_file": "aggregate_scenarios.csv",
            "source_row_number": "2",
        }
    )

    assert assign_session_date(
        before_session.timestamp,
        timezone="America/New_York",
        session_start="09:30",
    ) == date(2026, 1, 14)


def test_daily_realized_pnl_subtracts_fees() -> None:
    records = _load_aggregate_fixture()

    aggregates = build_daily_aggregates(
        records,
        timezone="UTC",
        session_start="00:00",
    )

    assert len(aggregates) == 1
    aggregate = aggregates[0]
    assert aggregate.account_id == "acct_demo_001"
    assert aggregate.session_date == date(2026, 1, 15)
    assert aggregate.gross_realized_pnl == Decimal("100")
    assert aggregate.fees == Decimal("3")
    assert aggregate.net_realized_pnl == Decimal("97")


def test_equity_curve_records_peak_and_drawdown() -> None:
    records = _load_aggregate_fixture()

    points = build_equity_curve(records)

    assert [
        (point.current_equity, point.peak_equity, point.drawdown) for point in points
    ] == [
        (Decimal("99"), Decimal("99"), Decimal("0")),
        (Decimal("97"), Decimal("99"), Decimal("2")),
    ]
    assert [point.row_id for point in points] == [records[1].row_id, records[3].row_id]


def _load_aggregate_fixture() -> tuple[TradeRecord, ...]:
    fixture = Path("tests/fixtures/trades/aggregate_scenarios.csv")
    with fixture.open(newline="", encoding="utf-8") as trade_file:
        return tuple(
            TradeRecord.from_mapping(row) for row in csv.DictReader(trade_file)
        )
