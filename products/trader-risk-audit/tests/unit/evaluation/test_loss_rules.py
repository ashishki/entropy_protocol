from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from trader_risk_audit.evaluation.rules import evaluate_loss_rules
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.trades.schema import TradeRecord


def test_max_daily_loss_flags_post_breach_trades() -> None:
    trades = _load_trades()
    policy = load_policy("tests/fixtures/policies/loss_rules_policy.yaml")

    result = evaluate_loss_rules(trades, policy)

    violations = [
        violation
        for violation in result.violations
        if violation.rule_id == "rule_max_daily_loss"
    ]
    assert [violation.source_row_ids for violation in violations] == [
        (trades[2].row_id,)
    ]
    assert violations[0].evaluated_value == Decimal("100")
    assert violations[0].threshold == Decimal("50")


def test_max_drawdown_records_equity_values() -> None:
    trades = _load_trades()
    policy = load_policy("tests/fixtures/policies/loss_rules_policy.yaml")

    result = evaluate_loss_rules(trades, policy)

    violation = next(
        violation
        for violation in result.violations
        if violation.rule_id == "rule_max_drawdown"
    )
    assert violation.threshold == Decimal("50")
    assert violation.details == {
        "peak_equity": Decimal("0"),
        "current_equity": Decimal("-100"),
        "drawdown": Decimal("100"),
    }


def test_cooldown_flags_trades_inside_window() -> None:
    trades = _load_trades()
    policy = load_policy("tests/fixtures/policies/loss_rules_policy.yaml")

    result = evaluate_loss_rules(trades, policy)

    violation = next(
        violation
        for violation in result.violations
        if violation.rule_id == "rule_cooldown_after_loss"
    )
    assert violation.source_row_ids == (trades[2].row_id,)
    assert violation.details == {
        "window_start": "2026-01-15T10:00:00+00:00",
        "window_end": "2026-01-15T10:30:00+00:00",
    }


def _load_trades() -> tuple[TradeRecord, ...]:
    fixture = Path("tests/fixtures/trades/loss_rule_scenarios.csv")
    with fixture.open(newline="", encoding="utf-8") as trade_file:
        return tuple(
            TradeRecord.from_mapping(row) for row in csv.DictReader(trade_file)
        )
