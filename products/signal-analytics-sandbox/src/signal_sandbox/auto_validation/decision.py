"""Auto-validation final decision engine."""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.auto_validation.results import (
    ValidationAuditLog,
    ValidationResult,
    ValidationStatus,
)

REQUIRED_VALIDATOR_IDS = frozenset(
    {
        "pre_outcome_timing",
        "setup_consistency",
        "provider_eligibility",
        "post_factum",
    }
)
CUSTOMER_POLICY_VALIDATOR_ID = "customer_policy"


class AutoValidationDecisionState(StrEnum):
    AUTO_ACCEPTED = "auto_accepted"
    AUTO_REJECTED = "auto_rejected"
    EXCLUDED_PROVIDER_GAP = "excluded_provider_gap"
    NEEDS_HUMAN = "needs_human"
    BLOCKED_CUSTOMER_FACING = "blocked_customer_facing"


class AutoValidationDecision(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    candidate_id: str = Field(min_length=1)
    state: AutoValidationDecisionState
    validator_result_ids: list[str] = Field(min_length=1)
    audit_log_ref: str = Field(min_length=1)
    evidence_bundle_sha256: str = Field(min_length=64, max_length=64)
    blocker_reasons: list[str] = Field(default_factory=list)
    decision_input_sha256: str = Field(min_length=64, max_length=64)


def decide_auto_validation(
    audit_log: ValidationAuditLog,
    *,
    policy_result: ValidationResult,
    required_validator_ids: set[str] | None = None,
) -> AutoValidationDecision:
    """Combine validator outputs into one conservative final decision."""

    required = required_validator_ids or set(REQUIRED_VALIDATOR_IDS)
    results = [*audit_log.results, policy_result]
    result_ids = [_result_id(result) for result in results]
    blockers = _blocker_reasons(results)
    audit_ref = f"{audit_log.audit_id}:{audit_log.audit_sha256()}"
    state = _decision_state(audit_log.results, policy_result, required)

    if state == AutoValidationDecisionState.NEEDS_HUMAN:
        blockers = [*blockers, *_missing_required_blockers(audit_log.results, required)]

    return AutoValidationDecision(
        candidate_id=audit_log.candidate_id,
        state=state,
        validator_result_ids=sorted(result_ids),
        audit_log_ref=audit_ref,
        evidence_bundle_sha256=audit_log.evidence_bundle_sha256,
        blocker_reasons=sorted(set(blockers)),
        decision_input_sha256=_decision_input_sha256(audit_log, policy_result),
    )


def _decision_state(
    validator_results: list[ValidationResult],
    policy_result: ValidationResult,
    required_validator_ids: set[str],
) -> AutoValidationDecisionState:
    by_id = {result.validator_id: result for result in validator_results}
    missing_required = required_validator_ids.difference(by_id)
    if missing_required:
        return AutoValidationDecisionState.NEEDS_HUMAN

    all_results = [*validator_results, policy_result]
    if any(
        result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
        for result in all_results
    ):
        return AutoValidationDecisionState.NEEDS_HUMAN

    if any(
        result.status == ValidationStatus.EXCLUDED_PROVIDER_GAP
        for result in validator_results
    ):
        return AutoValidationDecisionState.EXCLUDED_PROVIDER_GAP

    if policy_result.status == ValidationStatus.BLOCKED_CUSTOMER_FACING:
        return AutoValidationDecisionState.BLOCKED_CUSTOMER_FACING

    if any(result.status == ValidationStatus.FAILED for result in validator_results):
        return AutoValidationDecisionState.AUTO_REJECTED

    if policy_result.status != ValidationStatus.PASSED:
        return AutoValidationDecisionState.BLOCKED_CUSTOMER_FACING

    if all(result.status == ValidationStatus.PASSED for result in all_results):
        return AutoValidationDecisionState.AUTO_ACCEPTED

    return AutoValidationDecisionState.NEEDS_HUMAN


def _result_id(result: ValidationResult) -> str:
    return f"{result.validator_id}:{result.validator_version}:{result.status.value}"


def _blocker_reasons(results: list[ValidationResult]) -> list[str]:
    return [reason for result in results for reason in result.blocker_reasons]


def _missing_required_blockers(
    validator_results: list[ValidationResult],
    required_validator_ids: set[str],
) -> list[str]:
    present = {result.validator_id for result in validator_results}
    return [
        f"missing_required_validator:{validator_id}"
        for validator_id in sorted(required_validator_ids.difference(present))
    ]


def _decision_input_sha256(
    audit_log: ValidationAuditLog,
    policy_result: ValidationResult,
) -> str:
    payload = {
        "audit_sha256": audit_log.audit_sha256(),
        "policy_result": policy_result.model_dump(
            mode="json", by_alias=False, exclude_none=True
        ),
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
