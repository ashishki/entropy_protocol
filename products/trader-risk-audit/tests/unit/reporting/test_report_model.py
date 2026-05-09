from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from trader_risk_audit.evaluation.attribution import attribute_pnl
from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.trades.schema import TradeRecord


def test_report_model_contains_required_sections() -> None:
    model = _report_model()

    assert model.section_titles == (
        "Executive Summary",
        "Input Summary",
        "Policy Summary",
        "Violations",
        "Repeated Patterns",
        "Worst Violation Days",
        "P&L Attribution",
        "Limitations",
        "Next Review",
    )
    assert model.executive_summary.rule_count == 3
    assert model.executive_summary.violation_count == 2
    assert model.executive_summary.affected_pnl == "99"
    assert model.executive_summary.selected_policy_profile == "custom/unspecified"
    assert model.input_summary.trade_count == 4
    assert model.policy_summary.rule_count == 3
    assert model.repeated_patterns.items == (
        "rule_forbidden_assets: 1",
        "rule_max_position_size: 1",
    )


def test_report_violation_rows_include_traceability_fields() -> None:
    model = _report_model()

    row = model.violation_table[0]

    assert row.rule_id == "rule_forbidden_assets"
    assert row.timestamp == "2026-01-15T10:00:00+00:00"
    assert row.source_row_ids == (_trades()[1].row_id,)
    assert row.evaluated_value == "BTCUSD"
    assert row.threshold == "test"
    assert row.severity == "breach"
    assert row.pnl_impact == "99"


def test_warnings_render_as_limitations() -> None:
    model = _report_model()

    assert len(model.violation_table) == 2
    assert [item.rule_id for item in model.limitations] == ["rule_max_leverage"]
    assert model.limitations[0].reason_code == "unsupported_leverage_data"
    assert model.limitations[0].affected_source_fields == ("leverage",)


def _report_model():
    trades = _trades()
    violations = _violations(trades)
    warnings = (
        UnsupportedDataWarning(
            rule_id="rule_max_leverage",
            rule_type="max_leverage",
            message_code="unsupported_leverage_data",
            missing_fields=("leverage",),
        ),
    )
    return build_report_model(
        trades=trades,
        policy=load_policy("tests/fixtures/policies/position_asset_policy.yaml"),
        violations=violations,
        warnings=warnings,
        attribution=attribute_pnl(trades, violations),
    )


def _trades() -> tuple[TradeRecord, ...]:
    fixture = Path("tests/fixtures/trades/attribution_overlap.csv")
    with fixture.open(newline="", encoding="utf-8") as trade_file:
        return tuple(
            TradeRecord.from_mapping(row) for row in csv.DictReader(trade_file)
        )


def _violations(trades: tuple[TradeRecord, ...]) -> tuple[ViolationRecord, ...]:
    violating_trade = trades[1]
    return (
        _violation("rule_forbidden_assets", "forbidden_asset", violating_trade),
        _violation("rule_max_position_size", "max_position_size", violating_trade),
    )


def _violation(rule_id: str, rule_type: str, trade: TradeRecord) -> ViolationRecord:
    return ViolationRecord(
        rule_id=rule_id,
        rule_type=rule_type,
        source_row_ids=(trade.row_id,),
        timestamp=trade.timestamp,
        evaluated_value=trade.symbol,
        threshold="test",
        severity="breach",
        message_code=f"{rule_type}_breach",
        symbol=trade.symbol,
        details={"pnl_impact": Decimal("99")},
    )
