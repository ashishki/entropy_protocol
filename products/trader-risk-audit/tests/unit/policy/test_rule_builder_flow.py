from __future__ import annotations

from trader_risk_audit.policy.rule_builder_flow import explain_unavailable_rules


def test_rule_builder_explains_unavailable_rules() -> None:
    explanations = explain_unavailable_rules(
        {
            "missing_required_fields": (),
            "fee_available": False,
            "leverage_available": False,
            "pnl_available": False,
            "account_balance_available": False,
        }
    )

    joined = "\n".join(explanations)
    assert "max_daily_loss: unavailable because pnl_available, fee_available" in joined
    assert "max_leverage: unavailable because leverage_available" in joined
    assert "manual review" in joined
    assert "trading advice" not in joined.casefold()
    assert "profit" not in joined.casefold()
