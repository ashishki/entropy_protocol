from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path

import pytest

from trader_risk_audit.evaluation.attribution import attribute_pnl
from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.reporting.claim_guard import ClaimGuardError
from trader_risk_audit.reporting.delivery import render_delivery_packet
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.trades.schema import TradeRecord


def test_delivery_packet_contains_required_fields() -> None:
    model = _report_model()
    report = render_markdown_report(model)

    packet = render_delivery_packet(
        model=model,
        report_text=report,
        report_path="artifacts/report.md",
    )

    assert "Trader Risk Audit Summary" in packet
    assert "Trades reviewed: 4" in packet
    assert "Violations recorded: 2" in packet
    assert "rule_forbidden_assets: 1" in packet
    assert "Violating P&L: 99" in packet
    assert "rule_max_leverage: unsupported_leverage_data" in packet
    assert "This audit is not investment advice" in packet
    assert "Report: artifacts/report.md" in packet


def test_delivery_packet_respects_character_limit() -> None:
    model = _report_model_with_many_patterns()
    report = render_markdown_report(model)

    packet = render_delivery_packet(
        model=model,
        report_text=report,
        report_path="artifacts/report.md",
        character_limit=350,
    )

    assert len(packet) <= 350
    assert "repeated pattern details omitted" in packet
    assert "rule_extra_09" not in packet


def test_delivery_packet_requires_claim_guard_pass() -> None:
    model = _report_model()

    with pytest.raises(ClaimGuardError):
        render_delivery_packet(
            model=model,
            report_text="# Report without disclaimer",
            report_path="artifacts/report.md",
        )


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


def _report_model_with_many_patterns():
    model = _report_model()
    repeated_patterns = replace(
        model.repeated_patterns,
        items=model.repeated_patterns.items
        + tuple(f"rule_extra_{index:02}: 1" for index in range(10)),
    )
    return replace(model, repeated_patterns=repeated_patterns)


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
