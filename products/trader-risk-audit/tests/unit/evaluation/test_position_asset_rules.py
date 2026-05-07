from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from trader_risk_audit.evaluation.rules import evaluate_position_asset_rules
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.trades.schema import TradeRecord


def test_forbidden_assets_emit_source_row_violations() -> None:
    trades = _load_trades()
    policy = load_policy("tests/fixtures/policies/position_asset_policy.yaml")

    result = evaluate_position_asset_rules(trades, policy)

    violations = [
        violation
        for violation in result.violations
        if violation.rule_id == "rule_forbidden_assets"
    ]
    assert len(violations) == 1
    violation = violations[0]
    forbidden_trade = trades[1]
    assert violation.rule_id == "rule_forbidden_assets"
    assert violation.symbol == "BTCUSD"
    assert violation.timestamp == forbidden_trade.timestamp
    assert violation.source_row_ids == (forbidden_trade.row_id,)


def test_max_position_size_records_exposure_and_threshold() -> None:
    trades = _load_trades()
    policy = load_policy("tests/fixtures/policies/position_asset_policy.yaml")

    result = evaluate_position_asset_rules(trades, policy)

    violations = [
        violation
        for violation in result.violations
        if violation.rule_id == "rule_max_position_size"
    ]
    assert len(violations) == 1
    violation = violations[0]
    assert violation.evaluated_value == Decimal("15000")
    assert violation.threshold == Decimal("10000")
    assert violation.message_code == "max_position_size_exceeded"


def test_max_leverage_requires_source_leverage_fields() -> None:
    trades = _load_trades()
    policy = load_policy("tests/fixtures/policies/position_asset_policy.yaml")

    result = evaluate_position_asset_rules(trades, policy)

    assert not [
        violation
        for violation in result.violations
        if violation.rule_id == "rule_max_leverage"
    ]
    assert len(result.warnings) == 1
    warning = result.warnings[0]
    assert warning.rule_id == "rule_max_leverage"
    assert warning.message_code == "unsupported_leverage_data"
    assert warning.missing_fields == ("leverage",)


def _load_trades() -> tuple[TradeRecord, ...]:
    fixture = Path("tests/fixtures/trades/position_asset_trades.csv")
    with fixture.open(newline="", encoding="utf-8") as trade_file:
        return tuple(
            TradeRecord.from_mapping(row) for row in csv.DictReader(trade_file)
        )
