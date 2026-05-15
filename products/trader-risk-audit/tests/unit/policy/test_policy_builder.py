from __future__ import annotations

from decimal import Decimal

import pytest

from trader_risk_audit.policy.builder import (
    PolicyBuilderError,
    ThresholdOverride,
    build_policy_from_profile,
)
from trader_risk_audit.policy.schema import RiskPolicy


def test_policy_builder_creates_profile_policy() -> None:
    policy = build_policy_from_profile(
        profile="medium",
        intake_session=_intake_session(),
        account_scope=("acct_builder_001",),
    )

    assert isinstance(policy, RiskPolicy)
    assert policy.account_scope == ("acct_builder_001",)
    assert policy.timezone == "UTC"
    assert policy.session.start == "08:00"
    assert policy.session.end == "17:00"
    assert [rule.type for rule in policy.rules] == [
        "max_daily_loss",
        "max_drawdown",
        "cooldown_after_loss",
        "max_position_size",
        "forbidden_assets",
    ]


def test_policy_builder_validates_threshold_overrides() -> None:
    policy = build_policy_from_profile(
        profile="soft",
        intake_session=_intake_session(),
        account_scope=("acct_builder_001",),
        threshold_overrides={
            "max_daily_loss": ThresholdOverride(
                threshold=Decimal("1250"),
                unit="USD",
            )
        },
    )

    daily_loss = next(rule for rule in policy.rules if rule.type == "max_daily_loss")
    assert daily_loss.threshold == Decimal("1250")
    assert daily_loss.unit == "USD"

    with pytest.raises(PolicyBuilderError, match="unsupported threshold override"):
        build_policy_from_profile(
            profile="soft",
            intake_session=_intake_session(),
            account_scope=("acct_builder_001",),
            threshold_overrides={
                "news_sentiment": ThresholdOverride(
                    threshold=Decimal("1"),
                    unit="score",
                )
            },
        )

    with pytest.raises(PolicyBuilderError, match="threshold unit must be USD"):
        build_policy_from_profile(
            profile="soft",
            intake_session=_intake_session(),
            account_scope=("acct_builder_001",),
            threshold_overrides={
                "max_daily_loss": ThresholdOverride(
                    threshold=Decimal("10"),
                    unit="percent",
                )
            },
        )


def _intake_session() -> dict[str, object]:
    return {
        "source_timezone": "UTC",
        "session": {
            "start": "08:00",
            "end": "17:00",
        },
    }
