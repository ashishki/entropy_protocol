from __future__ import annotations

import json

import pytest

from trader_risk_audit.policy.schema import (
    UnsupportedRuleTypeError,
    load_policy,
    serialize_policy,
)


def test_valid_policy_fixture_loads_required_fields() -> None:
    policy = load_policy("tests/fixtures/policies/valid_policy.yaml")

    assert policy.schema_version == "1"
    assert policy.account_scope == ("acct_demo_001",)
    assert policy.timezone == "UTC"
    assert policy.session.start == "09:30"
    assert policy.session.end == "16:00"
    assert policy.rules
    assert policy.rules[0].type == "max_daily_loss"


def test_unsupported_rule_type_reports_rule_id() -> None:
    with pytest.raises(UnsupportedRuleTypeError) as error:
        load_policy("tests/fixtures/policies/unsupported_rule_policy.yaml")

    assert error.value.rule_id == "rule_news_sentiment"
    assert error.value.unsupported_type == "news_sentiment"
    assert "rule_news_sentiment" in str(error.value)
    assert "news_sentiment" in str(error.value)


def test_rule_ids_remain_stable_after_serialization() -> None:
    policy = load_policy("tests/fixtures/policies/valid_policy.yaml")

    serialized = serialize_policy(policy)
    payload = json.loads(serialized)

    assert [rule.rule_id for rule in policy.rules] == [
        "rule_max_daily_loss",
        "rule_forbidden_assets",
    ]
    assert [rule["rule_id"] for rule in payload["rules"]] == [
        "rule_max_daily_loss",
        "rule_forbidden_assets",
    ]
