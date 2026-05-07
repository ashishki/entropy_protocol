from __future__ import annotations

import csv
from pathlib import Path

from trader_risk_audit.evaluation.attribution import attribute_pnl
from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.trades.schema import TradeRecord

EXPECTED_REPORT = Path("tests/fixtures/expected/report_expected.md")


def test_markdown_contains_required_headings() -> None:
    markdown = render_markdown_report(_report_model())

    assert "# Trader Risk Audit Report" in markdown
    assert "## Summary" in markdown
    assert "## Policy" in markdown
    assert "## Violations" in markdown
    assert "## P&L Attribution" in markdown
    assert "## Limitations" in markdown
    assert "## Next Review" in markdown


def test_markdown_violation_table_has_traceability_columns() -> None:
    markdown = render_markdown_report(_report_model())

    assert (
        "| Rule ID | Timestamp | Source Row IDs | Evaluated Value | "
        "Threshold | Severity | P&L Impact |"
    ) in markdown
    assert (
        "| rule_forbidden_assets | 2026-01-15T10:00:00+00:00 | "
        f"{_trades()[1].row_id} | BTCUSD | test | breach | 99 |"
    ) in markdown


def test_markdown_rendering_is_deterministic() -> None:
    model = _report_model()

    first = render_markdown_report(model)
    second = render_markdown_report(model)

    assert first == second
    assert first.encode("utf-8") == second.encode("utf-8")
    assert first == EXPECTED_REPORT.read_text(encoding="utf-8")


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
        details={},
    )
