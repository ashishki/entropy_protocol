from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.auto_validation.customer_policy import (
    CustomerPolicyInput,
    evaluate_customer_policy,
)
from signal_sandbox.auto_validation.decision import AutoValidationDecisionState
from signal_sandbox.auto_validation.results import ValidationStatus

CREATED = datetime(2026, 5, 31, 12, tzinfo=UTC)


def test_policy_gate_requires_refs_provenance_caveats_and_safe_wording() -> None:
    result = evaluate_customer_policy(_policy_input(), created_at_utc=CREATED)

    assert result.status == ValidationStatus.PASSED
    assert result.blocker_reasons == []
    assert result.evidence_ref_ids == [
        "audit:abc",
        "recompute:market-window-1",
        "source-ref",
    ]


def test_policy_gate_blocks_private_source_missing_audit_and_provider_gap() -> None:
    result = evaluate_customer_policy(
        _policy_input(
            decision_state=AutoValidationDecisionState.EXCLUDED_PROVIDER_GAP,
            source_url="https://t.me/+privateInvite",
            validation_audit_ref=None,
        ),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.BLOCKED_CUSTOMER_FACING
    assert "private_source_risk" in result.blocker_reasons
    assert "missing_validation_audit_ref" in result.blocker_reasons
    assert "decision_not_auto_accepted:excluded_provider_gap" in result.blocker_reasons


def test_policy_gate_blocks_post_factum_auto_rejected_status() -> None:
    result = evaluate_customer_policy(
        _policy_input(decision_state=AutoValidationDecisionState.AUTO_REJECTED),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.BLOCKED_CUSTOMER_FACING
    assert "decision_not_auto_accepted:auto_rejected" in result.blocker_reasons


def test_policy_gate_blocks_forbidden_wording() -> None:
    result = evaluate_customer_policy(
        _policy_input(display_text="This author will profit and is the top signal."),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.BLOCKED_CUSTOMER_FACING
    assert any(
        reason.startswith("forbidden_wording:") for reason in result.blocker_reasons
    )


def test_policy_gate_blocks_missing_public_refs_recompute_and_caveats() -> None:
    result = evaluate_customer_policy(
        _policy_input(
            public_source_ref_ids=[],
            recompute_provenance_ref=None,
            visible_caveats=[],
        ),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.BLOCKED_CUSTOMER_FACING
    assert "missing_public_source_refs" in result.blocker_reasons
    assert "missing_recompute_provenance" in result.blocker_reasons
    assert "missing_visible_caveats" in result.blocker_reasons


def test_policy_gate_cannot_be_bypassed_by_model_confidence() -> None:
    result = evaluate_customer_policy(
        _policy_input(
            decision_state=AutoValidationDecisionState.NEEDS_HUMAN,
            model_confidence=Decimal("1"),
        ),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.BLOCKED_CUSTOMER_FACING
    assert "decision_not_auto_accepted:needs_human" in result.blocker_reasons


def _policy_input(
    *,
    decision_state: AutoValidationDecisionState = (
        AutoValidationDecisionState.AUTO_ACCEPTED
    ),
    source_url: str = "https://t.me/s/example/1",
    public_source_ref_ids: list[str] | None = None,
    validation_audit_ref: str | None = "audit:abc",
    recompute_provenance_ref: str | None = "recompute:market-window-1",
    visible_caveats: list[str] | None = None,
    display_text: str = "Historical research only. Not financial advice.",
    model_confidence: Decimal | None = None,
) -> CustomerPolicyInput:
    return CustomerPolicyInput(
        candidate_id="candidate-1",
        decision_state=decision_state,
        source_url=source_url,
        public_source_ref_ids=(
            ["source-ref"] if public_source_ref_ids is None else public_source_ref_ids
        ),
        validation_audit_ref=validation_audit_ref,
        recompute_provenance_ref=recompute_provenance_ref,
        visible_caveats=(
            ["Historical research only; unsupported rows are exclusions."]
            if visible_caveats is None
            else visible_caveats
        ),
        display_text=display_text,
        model_confidence=model_confidence,
    )
