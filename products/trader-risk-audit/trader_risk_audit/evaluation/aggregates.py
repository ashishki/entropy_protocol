from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from trader_risk_audit.evaluation.calendar import assign_session_date
from trader_risk_audit.trades.schema import TradeRecord


@dataclass(frozen=True)
class DailyAggregate:
    account_id: str
    session_date: date
    gross_realized_pnl: Decimal
    fees: Decimal
    net_realized_pnl: Decimal
    total_exposure: Decimal


@dataclass(frozen=True)
class EquityCurvePoint:
    row_id: str
    timestamp: datetime
    account_id: str
    current_equity: Decimal
    peak_equity: Decimal
    drawdown: Decimal
    realized_pnl: Decimal


@dataclass
class _OpenLot:
    side: str
    quantity: Decimal
    price: Decimal


@dataclass(frozen=True)
class _ClosedTrade:
    trade: TradeRecord
    gross_realized_pnl: Decimal


def build_daily_aggregates(
    trades: tuple[TradeRecord, ...],
    *,
    timezone: str,
    session_start: str,
) -> tuple[DailyAggregate, ...]:
    closed_trades = _match_closed_trades(trades)
    gross_by_day: defaultdict[tuple[str, date], Decimal] = defaultdict(
        lambda: Decimal("0")
    )
    fees_by_day: defaultdict[tuple[str, date], Decimal] = defaultdict(
        lambda: Decimal("0")
    )
    exposure_by_day: defaultdict[tuple[str, date], Decimal] = defaultdict(
        lambda: Decimal("0")
    )

    for trade in trades:
        session_date = assign_session_date(
            trade.timestamp,
            timezone=timezone,
            session_start=session_start,
        )
        key = (trade.account_id, session_date)
        fees_by_day[key] += trade.fees
        exposure_by_day[key] += abs(trade.quantity * trade.price)

    for closed_trade in closed_trades:
        session_date = assign_session_date(
            closed_trade.trade.timestamp,
            timezone=timezone,
            session_start=session_start,
        )
        key = (closed_trade.trade.account_id, session_date)
        gross_by_day[key] += closed_trade.gross_realized_pnl

    all_keys = set(gross_by_day) | set(fees_by_day) | set(exposure_by_day)
    return tuple(
        DailyAggregate(
            account_id=account_id,
            session_date=session_date,
            gross_realized_pnl=gross_by_day[(account_id, session_date)],
            fees=fees_by_day[(account_id, session_date)],
            net_realized_pnl=(
                gross_by_day[(account_id, session_date)]
                - fees_by_day[(account_id, session_date)]
            ),
            total_exposure=exposure_by_day[(account_id, session_date)],
        )
        for account_id, session_date in sorted(all_keys)
    )


def build_equity_curve(trades: tuple[TradeRecord, ...]) -> tuple[EquityCurvePoint, ...]:
    current_equity = Decimal("0")
    peak_equity = Decimal("0")
    points: list[EquityCurvePoint] = []
    for closed_trade in _match_closed_trades(trades):
        net_realized = closed_trade.gross_realized_pnl - closed_trade.trade.fees
        current_equity += net_realized
        peak_equity = max(peak_equity, current_equity)
        points.append(
            EquityCurvePoint(
                row_id=closed_trade.trade.row_id,
                timestamp=closed_trade.trade.timestamp,
                account_id=closed_trade.trade.account_id,
                current_equity=current_equity,
                peak_equity=peak_equity,
                drawdown=peak_equity - current_equity,
                realized_pnl=net_realized,
            )
        )
    return tuple(points)


def _match_closed_trades(trades: tuple[TradeRecord, ...]) -> tuple[_ClosedTrade, ...]:
    lots_by_key: defaultdict[tuple[str, str], list[_OpenLot]] = defaultdict(list)
    closed_trades: list[_ClosedTrade] = []
    for trade in sorted(
        trades, key=lambda item: (item.timestamp, item.source_row_number)
    ):
        key = (trade.account_id, trade.symbol)
        quantity_to_match = trade.quantity
        open_lots = lots_by_key[key]
        gross_realized_pnl = Decimal("0")
        closed_quantity = Decimal("0")

        while quantity_to_match > 0 and open_lots and open_lots[0].side != trade.side:
            lot = open_lots[0]
            matched_quantity = min(quantity_to_match, lot.quantity)
            gross_realized_pnl += _realized_pnl(lot, trade, matched_quantity)
            closed_quantity += matched_quantity
            lot.quantity -= matched_quantity
            quantity_to_match -= matched_quantity
            if lot.quantity == 0:
                open_lots.pop(0)

        if closed_quantity > 0:
            closed_trades.append(
                _ClosedTrade(trade=trade, gross_realized_pnl=gross_realized_pnl)
            )
        if quantity_to_match > 0:
            open_lots.append(
                _OpenLot(
                    side=trade.side,
                    quantity=quantity_to_match,
                    price=trade.price,
                )
            )
    return tuple(closed_trades)


def _realized_pnl(
    lot: _OpenLot,
    closing_trade: TradeRecord,
    quantity: Decimal,
) -> Decimal:
    if lot.side == "buy" and closing_trade.side == "sell":
        return (closing_trade.price - lot.price) * quantity
    if lot.side == "sell" and closing_trade.side == "buy":
        return (lot.price - closing_trade.price) * quantity
    return Decimal("0")
