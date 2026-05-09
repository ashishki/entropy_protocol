from __future__ import annotations

import pytest

from trader_risk_audit.policy.review import (
    ReviewDecision,
    apply_review_decisions,
    build_review_packet,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.policy.validation import (
    PolicyReviewRequiredError,
    ensure_policy_ready_for_evaluation,
)


def test_ambiguous_rule_generates_review_packet() -> None:
    policy = load_policy("tests/fixtures/policies/ambiguous_policy.yaml")

    packet = build_review_packet(policy)

    assert len(packet.items) == 1
    item = packet.items[0]
    assert item.rule_id == "rule_ambiguous_daily_loss"
    assert item.source_text == "Stop if the day gets too red."
    assert item.missing_deterministic_fields == ("threshold",)
    assert "threshold" in item.required_operator_decision


def test_unresolved_review_items_block_evaluation() -> None:
    policy = load_policy("tests/fixtures/policies/ambiguous_policy.yaml")
    packet = build_review_packet(policy)

    with pytest.raises(PolicyReviewRequiredError) as error:
        ensure_policy_ready_for_evaluation(policy, packet)

    assert error.value.packet.unresolved_items == packet.items
    assert "rule_ambiguous_daily_loss" in str(error.value)


def test_approved_review_preserves_source_text() -> None:
    policy = load_policy("tests/fixtures/policies/ambiguous_policy.yaml")

    approved = apply_review_decisions(
        policy,
        [
            ReviewDecision(
                rule_id="rule_ambiguous_daily_loss",
                deterministic_fields={"threshold": "750"},
            )
        ],
    )
    packet = build_review_packet(approved)

    assert packet.unresolved_items == ()
    rule = approved.rules[0]
    assert str(rule.threshold) == "750"
    assert rule.params["source_text"] == "Stop if the day gets too red."
    assert ensure_policy_ready_for_evaluation(approved, packet) == approved
