from __future__ import annotations

from trader_risk_audit.policy.rule_catalog import (
    list_rule_catalog,
    rule_availability,
)
from trader_risk_audit.policy.schema import SUPPORTED_RULE_TYPES


def test_rule_catalog_lists_supported_rules() -> None:
    catalog = list_rule_catalog()

    assert {entry.rule_type for entry in catalog} == SUPPORTED_RULE_TYPES
    assert all(entry.required_source_fields for entry in catalog)
    assert all(entry.threshold_unit for entry in catalog)
    assert all(entry.safe_description for entry in catalog)
    assert {entry.rule_type: entry.threshold_unit for entry in catalog} == {
        "max_daily_loss": "USD",
        "max_drawdown": "USD",
        "cooldown_after_loss": "minutes",
        "max_position_size": "USD",
        "forbidden_assets": "symbol",
        "max_leverage": "ratio",
    }


def test_rule_catalog_marks_unavailable_rules() -> None:
    availability = {
        item.rule_type: item
        for item in rule_availability(
            {
                "missing_required_fields": (),
                "fee_available": False,
                "leverage_available": False,
                "pnl_available": False,
                "account_balance_available": False,
            }
        )
    }

    assert availability["forbidden_assets"].available is True
    assert availability["max_position_size"].available is True
    assert availability["max_daily_loss"].available is False
    assert availability["max_daily_loss"].missing_requirements == (
        "pnl_available",
        "fee_available",
    )
    assert availability["max_drawdown"].available is False
    assert availability["max_drawdown"].missing_requirements == (
        "pnl_available",
        "fee_available",
        "account_balance_available",
    )
    assert availability["cooldown_after_loss"].available is False
    assert availability["max_leverage"].available is False
    assert availability["max_leverage"].missing_requirements == ("leverage_available",)


def test_rule_catalog_copy_is_claim_safe() -> None:
    forbidden_fragments = (
        "advice",
        "optimal",
        "guarantee",
        "profit",
        "reduce risk",
        "prevent loss",
        "block orders",
        "control trades",
        "should trade",
    )

    for entry in list_rule_catalog():
        copy = entry.safe_description.casefold()
        assert not any(fragment in copy for fragment in forbidden_fragments)
