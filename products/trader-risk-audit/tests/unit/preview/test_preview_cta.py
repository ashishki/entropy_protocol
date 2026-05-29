from __future__ import annotations

from trader_risk_audit.preview import build_paid_pilot_cta, render_paid_pilot_cta


def test_preview_cta_requires_eligible_status() -> None:
    eligible = build_paid_pilot_cta(audit_status="complete")
    blocked = build_paid_pilot_cta(audit_status="blocked")

    eligible_text = render_paid_pilot_cta(eligible)
    blocked_text = render_paid_pilot_cta(blocked)

    assert "One manual reviewed audit report" in eligible_text
    assert "48-72 hours" in eligible_text
    assert "$49-$149" in eligible_text
    assert "checkout flow" in eligible_text
    assert blocked_text == ""
