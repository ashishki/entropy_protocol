from __future__ import annotations

import pytest

from trader_risk_audit.preview import (
    PaidUnlockError,
    create_preview_unlock_state,
    transition_paid_unlock_state,
)


def test_paid_unlock_status_blocks_unreviewed_delivery() -> None:
    preview = create_preview_unlock_state("audit_demo")
    requested = transition_paid_unlock_state(
        preview,
        "paid_requested",
        manual_payment_evidence="manual_paid_intent",
    )

    with pytest.raises(PaidUnlockError, match="cannot transition"):
        transition_paid_unlock_state(requested, "delivered")

    reviewed = transition_paid_unlock_state(
        requested,
        "operator_reviewed",
        claim_safe=False,
    )
    with pytest.raises(PaidUnlockError, match="delivery requires"):
        transition_paid_unlock_state(reviewed, "delivered")


def test_paid_requested_status_is_privacy_safe() -> None:
    preview = create_preview_unlock_state("audit_demo")
    requested = transition_paid_unlock_state(
        preview,
        "paid_requested",
        manual_payment_evidence="manual_paid_intent",
    )

    assert requested.manual_payment_evidence == "manual_paid_intent"
    with pytest.raises(PaidUnlockError):
        transition_paid_unlock_state(
            preview,
            "paid_requested",
            manual_payment_evidence="stripe_transaction_123456789",
        )
