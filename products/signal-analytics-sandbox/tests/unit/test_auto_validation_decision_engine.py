from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.auto_validation.decision import (
    AutoValidationDecisionState,
    decide_auto_validation,
)
from signal_sandbox.auto_validation.results import (
    ValidationAuditLog,
    ValidationResult,
    ValidationStatus,
)

SHA = "a" * 64
BUNDLE_SHA = "b" * 64
CREATED = datetime(2026, 5, 31, 12, tzinfo=UTC)


def test_decision_auto_accepts_only_when_all_validators_and_policy_pass() -> None:
    decision = decide_auto_validation(
        _audit(
            [
                _result("pre_outcome_timing", ValidationStatus.PASSED),
                _result("setup_consistency", ValidationStatus.PASSED),
                _result("provider_eligibility", ValidationStatus.PASSED),
                _result("post_factum", ValidationStatus.PASSED),
            ]
        ),
        policy_result=_result("customer_policy", ValidationStatus.PASSED),
    )

    assert decision.state == AutoValidationDecisionState.AUTO_ACCEPTED
    assert decision.blocker_reasons == []
    assert "audit-1:" in decision.audit_log_ref
    assert any("pre_outcome_timing" in item for item in decision.validator_result_ids)


def test_decision_routes_any_uncertain_validator_to_needs_human() -> None:
    decision = decide_auto_validation(
        _audit(
            [
                _result("pre_outcome_timing", ValidationStatus.PASSED),
                _result("setup_consistency", ValidationStatus.UNCERTAIN_NEEDS_HUMAN),
                _result("provider_eligibility", ValidationStatus.PASSED),
                _result("post_factum", ValidationStatus.PASSED),
            ]
        ),
        policy_result=_result("customer_policy", ValidationStatus.PASSED),
    )

    assert decision.state == AutoValidationDecisionState.NEEDS_HUMAN
    assert "setup_consistency_blocker" in decision.blocker_reasons


def test_decision_excludes_provider_gap_before_acceptance() -> None:
    decision = decide_auto_validation(
        _audit(
            [
                _result("pre_outcome_timing", ValidationStatus.PASSED),
                _result("setup_consistency", ValidationStatus.PASSED),
                _result("provider_eligibility", ValidationStatus.EXCLUDED_PROVIDER_GAP),
                _result("post_factum", ValidationStatus.PASSED),
            ]
        ),
        policy_result=_result("customer_policy", ValidationStatus.PASSED),
    )

    assert decision.state == AutoValidationDecisionState.EXCLUDED_PROVIDER_GAP


def test_decision_blocks_customer_facing_when_policy_gate_blocks() -> None:
    decision = decide_auto_validation(
        _audit(
            [
                _result("pre_outcome_timing", ValidationStatus.PASSED),
                _result("setup_consistency", ValidationStatus.PASSED),
                _result("provider_eligibility", ValidationStatus.PASSED),
                _result("post_factum", ValidationStatus.PASSED),
            ]
        ),
        policy_result=_result(
            "customer_policy",
            ValidationStatus.BLOCKED_CUSTOMER_FACING,
        ),
    )

    assert decision.state == AutoValidationDecisionState.BLOCKED_CUSTOMER_FACING


def test_decision_auto_rejects_failed_post_factum_validator() -> None:
    decision = decide_auto_validation(
        _audit(
            [
                _result("pre_outcome_timing", ValidationStatus.PASSED),
                _result("setup_consistency", ValidationStatus.PASSED),
                _result("provider_eligibility", ValidationStatus.PASSED),
                _result("post_factum", ValidationStatus.FAILED),
            ]
        ),
        policy_result=_result("customer_policy", ValidationStatus.PASSED),
    )

    assert decision.state == AutoValidationDecisionState.AUTO_REJECTED


def test_decision_routes_missing_required_validator_to_needs_human() -> None:
    decision = decide_auto_validation(
        _audit(
            [
                _result("pre_outcome_timing", ValidationStatus.PASSED),
                _result("setup_consistency", ValidationStatus.PASSED),
                _result("provider_eligibility", ValidationStatus.PASSED),
            ]
        ),
        policy_result=_result("customer_policy", ValidationStatus.PASSED),
    )

    assert decision.state == AutoValidationDecisionState.NEEDS_HUMAN
    assert "missing_required_validator:post_factum" in decision.blocker_reasons


def _audit(results: list[ValidationResult]) -> ValidationAuditLog:
    return ValidationAuditLog(
        audit_id="audit-1",
        candidate_id="candidate-1",
        evidence_bundle_sha256=BUNDLE_SHA,
        results=results,
        created_at_utc=CREATED,
    )


def _result(validator_id: str, status: ValidationStatus) -> ValidationResult:
    return ValidationResult(
        validator_id=validator_id,
        validator_version=f"{validator_id}.v1",
        candidate_id="candidate-1",
        status=status,
        confidence=Decimal("1") if status == ValidationStatus.PASSED else Decimal("0"),
        evidence_ref_ids=[f"{validator_id}-ref"],
        blocker_reasons=(
            [] if status == ValidationStatus.PASSED else [f"{validator_id}_blocker"]
        ),
        deterministic_input_sha256=SHA,
        rationale="test result",
        created_at_utc=CREATED,
    )
