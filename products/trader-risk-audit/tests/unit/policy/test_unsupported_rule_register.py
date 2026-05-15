from __future__ import annotations

from trader_risk_audit.policy.builder import build_policy_from_profile
from trader_risk_audit.policy.unsupported_register import (
    create_unsupported_rule_entry,
    policy_excludes_unsupported_rules,
    render_unsupported_rule_limitations,
)


def test_register_sanitizes_unsupported_rules() -> None:
    entry = create_unsupported_rule_entry(
        user_text="Track revenge trading after news!!!",
        reason_code="unsupported_behavior_rule",
    )

    assert entry.request_id.startswith("unsupported_")
    assert entry.reason_code == "unsupported_behavior_rule"
    assert entry.status == "manual_review_required"
    assert entry.sanitized_summary == "Track revenge trading after news"
    assert "!!!" not in entry.sanitized_summary


def test_unsupported_rules_do_not_enter_policy() -> None:
    entry = create_unsupported_rule_entry(
        user_text="Stop emotional entries after social media.",
        reason_code="free_text_rule",
    )
    policy = build_policy_from_profile(
        profile="soft",
        intake_session={
            "source_timezone": "UTC",
            "session": {
                "start": "08:00",
                "end": "17:00",
            },
        },
        account_scope=("acct_register_001",),
    )
    limitations = render_unsupported_rule_limitations((entry,))

    assert policy_excludes_unsupported_rules(policy, (entry,)) is True
    assert all(rule.rule_id != entry.request_id for rule in policy.rules)
    assert entry.request_id in limitations[0]
    assert "manual review" in limitations[0]
