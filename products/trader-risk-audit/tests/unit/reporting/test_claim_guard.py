from __future__ import annotations

import csv
from pathlib import Path

from trader_risk_audit.evaluation.attribution import attribute_pnl
from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.reporting.claim_guard import (
    REQUIRED_DISCLAIMER,
    validate_report_claims,
)
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.trades.schema import TradeRecord


def test_missing_disclaimer_fails_validation() -> None:
    result = validate_report_claims("# Report\n\n## Violations\n\nNone")

    assert result.passed is False
    assert result.findings[0].category == "required_disclaimer"
    assert result.findings[0].matched_text == REQUIRED_DISCLAIMER


def test_forbidden_claim_phrases_return_category_and_match() -> None:
    report = (
        f"{REQUIRED_DISCLAIMER}\n\n"
        "This audit guarantees profit and controls live orders."
    )

    result = validate_report_claims(report)

    assert result.passed is False
    assert (result.findings[0].category, result.findings[0].matched_text) == (
        "profit_promise",
        "guarantees profit",
    )
    assert (result.findings[1].category, result.findings[1].matched_text) == (
        "live_order_control",
        "controls live orders",
    )


def test_evidence_backed_violation_language_passes() -> None:
    report = render_markdown_report(_report_model())

    result = validate_report_claims(report)

    assert result.passed is True
    assert result.findings == ()


def test_open_source_evidence_overclaim_phrases_fail_validation() -> None:
    report = (
        f"{REQUIRED_DISCLAIMER}\n\n"
        "This open-source validation proves PMF. "
        "The demo evidence proves customer demand. "
        "The open-source pack is paid-pilot evidence."
    )

    result = validate_report_claims(report)

    assert result.passed is False
    assert [finding.category for finding in result.findings] == [
        "evidence_overclaim",
        "evidence_overclaim",
        "evidence_overclaim",
    ]
    assert [finding.matched_text for finding in result.findings] == [
        "proves PMF",
        "demo evidence proves customer demand",
        "open-source pack is paid-pilot evidence",
    ]


def test_open_source_boundary_language_passes_validation() -> None:
    report = (
        f"{REQUIRED_DISCLAIMER}\n\n"
        "This open-source artifact is not PMF evidence, not customer "
        "validation, and not proof that traders will pay."
    )

    result = validate_report_claims(report)

    assert result.passed is True
    assert result.findings == ()


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
