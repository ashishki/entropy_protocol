from __future__ import annotations

from trader_risk_audit.evaluation.attribution import attribute_pnl
from trader_risk_audit.evaluation.rules import (
    evaluate_loss_rules,
    evaluate_position_asset_rules,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.reporting.claim_guard import (
    REQUIRED_DISCLAIMER,
    ensure_report_claims_valid,
)
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.trades.importers import normalize_csv


def test_demo_report_starts_with_compact_summary() -> None:
    markdown = _public_sample_report()

    executive_index = markdown.index("## Executive Summary")
    summary_index = markdown.index("## Summary")

    assert executive_index < summary_index
    assert "- Rules reviewed: 5" in markdown
    assert "- Violations recorded: 9" in markdown
    assert "- Affected P&L: 0" in markdown
    assert "- Selected policy profile: hard" in markdown


def test_demo_report_preserves_source_traceability() -> None:
    markdown = _public_sample_report()

    assert (
        "| Rule ID | Timestamp | Source Row IDs | Evaluated Value | "
        "Threshold | Severity | P&L Impact |"
    ) in markdown
    assert "public_sample_hard_forbidden_assets" in markdown
    assert "trade_fcdefbab78fa75d6" in markdown
    assert "RISKY" in markdown
    assert "| breach |" in markdown


def test_demo_report_preserves_claim_guard_boundary() -> None:
    markdown = _public_sample_report()

    ensure_report_claims_valid(markdown)
    assert REQUIRED_DISCLAIMER in markdown
    forbidden_phrases = (
        "guaranteed profit",
        "will block orders",
        "caused your losses",
        "would have made",
    )
    lowered = markdown.casefold()
    for phrase in forbidden_phrases:
        assert phrase not in lowered


def _public_sample_report() -> str:
    trades = normalize_csv("demo/public_sample_001/trades.csv")
    policy = load_policy("demo/public_sample_001/policy.yaml")
    position_asset = evaluate_position_asset_rules(trades, policy)
    loss = evaluate_loss_rules(trades, policy)
    violations = tuple(
        sorted(
            position_asset.violations + loss.violations,
            key=lambda item: (item.timestamp, item.rule_id, item.source_row_ids),
        )
    )
    warnings = tuple(
        sorted(
            position_asset.warnings + loss.warnings,
            key=lambda item: (item.rule_id, item.message_code),
        )
    )
    return render_markdown_report(
        build_report_model(
            trades=trades,
            policy=policy,
            violations=violations,
            warnings=warnings,
            attribution=attribute_pnl(trades, violations),
        )
    )
