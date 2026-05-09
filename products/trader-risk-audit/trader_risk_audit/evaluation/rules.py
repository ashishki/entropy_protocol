from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from trader_risk_audit.evaluation.aggregates import build_equity_curve
from trader_risk_audit.evaluation.calendar import assign_session_date
from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
)
from trader_risk_audit.policy.schema import PolicyRule, RiskPolicy
from trader_risk_audit.trades.schema import TradeRecord


@dataclass(frozen=True)
class EvaluationResult:
    violations: tuple[ViolationRecord, ...]
    warnings: tuple[UnsupportedDataWarning, ...]


def evaluate_position_asset_rules(
    trades: tuple[TradeRecord, ...],
    policy: RiskPolicy,
) -> EvaluationResult:
    violations: list[ViolationRecord] = []
    warnings: list[UnsupportedDataWarning] = []
    scoped_trades = tuple(
        trade for trade in trades if trade.account_id in set(policy.account_scope)
    )
    for rule in policy.rules:
        if rule.type == "forbidden_assets":
            violations.extend(_evaluate_forbidden_assets(scoped_trades, rule))
        elif rule.type == "max_position_size":
            violations.extend(_evaluate_max_position_size(scoped_trades, rule))
        elif rule.type == "max_leverage":
            warnings.append(
                UnsupportedDataWarning(
                    rule_id=rule.rule_id,
                    rule_type=rule.type,
                    message_code="unsupported_leverage_data",
                    missing_fields=("leverage",),
                )
            )
    return EvaluationResult(violations=tuple(violations), warnings=tuple(warnings))


def evaluate_loss_rules(
    trades: tuple[TradeRecord, ...],
    policy: RiskPolicy,
) -> EvaluationResult:
    scoped_trades = tuple(
        trade for trade in trades if trade.account_id in set(policy.account_scope)
    )
    violations: list[ViolationRecord] = []
    for rule in policy.rules:
        if rule.type == "max_daily_loss":
            violations.extend(_evaluate_max_daily_loss(scoped_trades, policy, rule))
        elif rule.type == "max_drawdown":
            violations.extend(_evaluate_max_drawdown(scoped_trades, rule))
        elif rule.type == "cooldown_after_loss":
            violations.extend(_evaluate_cooldown_after_loss(scoped_trades, rule))
    return EvaluationResult(violations=tuple(violations), warnings=())


def _evaluate_max_daily_loss(
    trades: tuple[TradeRecord, ...],
    policy: RiskPolicy,
    rule: PolicyRule,
) -> tuple[ViolationRecord, ...]:
    if rule.threshold is None:
        return ()
    breach_by_key: dict[tuple[str, object], Decimal] = {}
    for point in build_equity_curve(trades):
        session_date = assign_session_date(
            point.timestamp,
            timezone=policy.timezone,
            session_start=policy.session.start,
        )
        key = (point.account_id, session_date)
        realized_loss = -point.current_equity
        if key not in breach_by_key and realized_loss > rule.threshold:
            breach_by_key[key] = realized_loss

    return tuple(
        ViolationRecord(
            rule_id=rule.rule_id,
            rule_type=rule.type,
            source_row_ids=(trade.row_id,),
            timestamp=trade.timestamp,
            evaluated_value=breach_by_key[key],
            threshold=rule.threshold,
            severity="breach",
            message_code="max_daily_loss_post_breach_trade",
            symbol=trade.symbol.upper(),
            details={"session_date": key[1].isoformat()},
        )
        for trade in _trades_after_daily_breach(trades, policy, breach_by_key)
        if (key := _daily_key(trade, policy)) in breach_by_key
    )


def _evaluate_max_drawdown(
    trades: tuple[TradeRecord, ...],
    rule: PolicyRule,
) -> tuple[ViolationRecord, ...]:
    if rule.threshold is None:
        return ()
    breach_point_by_account: dict[str, object] = {}
    for point in build_equity_curve(trades):
        if (
            point.account_id not in breach_point_by_account
            and point.drawdown > rule.threshold
        ):
            breach_point_by_account[point.account_id] = point

    violations: list[ViolationRecord] = []
    for trade in trades:
        point = breach_point_by_account.get(trade.account_id)
        if point is None or trade.timestamp <= point.timestamp:
            continue
        violations.append(
            ViolationRecord(
                rule_id=rule.rule_id,
                rule_type=rule.type,
                source_row_ids=(trade.row_id,),
                timestamp=trade.timestamp,
                evaluated_value=point.drawdown,
                threshold=rule.threshold,
                severity="breach",
                message_code="max_drawdown_post_breach_trade",
                symbol=trade.symbol.upper(),
                details={
                    "peak_equity": point.peak_equity,
                    "current_equity": point.current_equity,
                    "drawdown": point.drawdown,
                },
            )
        )
    return tuple(violations)


def _evaluate_cooldown_after_loss(
    trades: tuple[TradeRecord, ...],
    rule: PolicyRule,
) -> tuple[ViolationRecord, ...]:
    loss_threshold = Decimal(str(rule.params.get("loss_threshold", "0")))
    cooldown_minutes = int(rule.params.get("cooldown_minutes", 0))
    windows = tuple(
        (
            point.account_id,
            point.timestamp,
            point.timestamp + timedelta(minutes=cooldown_minutes),
        )
        for point in build_equity_curve(trades)
        if -point.realized_pnl > loss_threshold
    )
    violations: list[ViolationRecord] = []
    for trade in trades:
        for account_id, window_start, window_end in windows:
            if trade.account_id != account_id:
                continue
            if window_start < trade.timestamp <= window_end:
                violations.append(
                    ViolationRecord(
                        rule_id=rule.rule_id,
                        rule_type=rule.type,
                        source_row_ids=(trade.row_id,),
                        timestamp=trade.timestamp,
                        evaluated_value=trade.timestamp.isoformat(),
                        threshold=window_end.isoformat(),
                        severity="breach",
                        message_code="cooldown_trade_inside_window",
                        symbol=trade.symbol.upper(),
                        details={
                            "window_start": window_start.isoformat(),
                            "window_end": window_end.isoformat(),
                        },
                    )
                )
    return tuple(violations)


def _trades_after_daily_breach(
    trades: tuple[TradeRecord, ...],
    policy: RiskPolicy,
    breach_by_key: dict[tuple[str, object], Decimal],
) -> tuple[TradeRecord, ...]:
    breach_time_by_key: dict[tuple[str, object], datetime] = {}
    for point in build_equity_curve(trades):
        key = (
            point.account_id,
            assign_session_date(
                point.timestamp,
                timezone=policy.timezone,
                session_start=policy.session.start,
            ),
        )
        if key in breach_by_key and key not in breach_time_by_key:
            breach_time_by_key[key] = point.timestamp
    return tuple(
        trade
        for trade in trades
        if (key := _daily_key(trade, policy)) in breach_time_by_key
        and trade.timestamp > breach_time_by_key[key]
    )


def _daily_key(trade: TradeRecord, policy: RiskPolicy) -> tuple[str, object]:
    return (
        trade.account_id,
        assign_session_date(
            trade.timestamp,
            timezone=policy.timezone,
            session_start=policy.session.start,
        ),
    )


def _evaluate_forbidden_assets(
    trades: tuple[TradeRecord, ...],
    rule: PolicyRule,
) -> tuple[ViolationRecord, ...]:
    forbidden_symbols = {
        str(symbol).strip().upper() for symbol in rule.params.get("symbols", ())
    }
    return tuple(
        ViolationRecord(
            rule_id=rule.rule_id,
            rule_type=rule.type,
            source_row_ids=(trade.row_id,),
            timestamp=trade.timestamp,
            evaluated_value=trade.symbol.upper(),
            threshold=",".join(sorted(forbidden_symbols)),
            severity="breach",
            message_code="forbidden_asset",
            symbol=trade.symbol.upper(),
        )
        for trade in trades
        if trade.symbol.upper() in forbidden_symbols
    )


def _evaluate_max_position_size(
    trades: tuple[TradeRecord, ...],
    rule: PolicyRule,
) -> tuple[ViolationRecord, ...]:
    if rule.threshold is None:
        return ()
    return tuple(
        ViolationRecord(
            rule_id=rule.rule_id,
            rule_type=rule.type,
            source_row_ids=(trade.row_id,),
            timestamp=trade.timestamp,
            evaluated_value=_position_exposure(trade),
            threshold=rule.threshold,
            severity="breach",
            message_code="max_position_size_exceeded",
            symbol=trade.symbol.upper(),
        )
        for trade in trades
        if _position_exposure(trade) > rule.threshold
    )


def _position_exposure(trade: TradeRecord) -> Decimal:
    return abs(trade.quantity * trade.price)
