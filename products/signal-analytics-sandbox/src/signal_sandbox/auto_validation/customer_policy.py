"""Customer-facing policy gate for auto-validation decisions."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.auto_validation.decision import AutoValidationDecisionState
from signal_sandbox.auto_validation.results import ValidationResult, ValidationStatus
from signal_sandbox.reports.wording import find_forbidden_wording
from signal_sandbox.sources.private_patterns import is_private_source_url

CUSTOMER_POLICY_VALIDATOR_ID = "customer_policy"
CUSTOMER_POLICY_VALIDATOR_VERSION = "customer_policy.v1"


class CustomerPolicyInput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    candidate_id: str = Field(min_length=1)
    decision_state: AutoValidationDecisionState
    source_url: str = Field(min_length=1)
    public_source_ref_ids: list[str] = Field(default_factory=list)
    validation_audit_ref: str | None = Field(default=None, min_length=1)
    recompute_provenance_ref: str | None = Field(default=None, min_length=1)
    visible_caveats: list[str] = Field(default_factory=list)
    display_text: str = ""
    model_confidence: Decimal | None = Field(
        default=None, ge=Decimal("0"), le=Decimal("1")
    )


def evaluate_customer_policy(
    policy_input: CustomerPolicyInput,
    *,
    created_at_utc: datetime | None = None,
) -> ValidationResult:
    """Gate whether an auto-validated row may enter customer-facing metrics."""

    blockers = _policy_blockers(policy_input)
    evidence_refs = _policy_evidence_refs(policy_input)
    if blockers:
        return ValidationResult(
            validator_id=CUSTOMER_POLICY_VALIDATOR_ID,
            validator_version=CUSTOMER_POLICY_VALIDATOR_VERSION,
            candidate_id=policy_input.candidate_id,
            status=ValidationStatus.BLOCKED_CUSTOMER_FACING,
            confidence=Decimal("1"),
            evidence_ref_ids=evidence_refs,
            blocker_reasons=blockers,
            deterministic_input_sha256=_input_sha256(policy_input),
            rationale="customer-facing policy requirements are not satisfied",
            created_at_utc=created_at_utc or datetime.now(UTC),
        )

    return ValidationResult(
        validator_id=CUSTOMER_POLICY_VALIDATOR_ID,
        validator_version=CUSTOMER_POLICY_VALIDATOR_VERSION,
        candidate_id=policy_input.candidate_id,
        status=ValidationStatus.PASSED,
        confidence=Decimal("1"),
        evidence_ref_ids=evidence_refs,
        blocker_reasons=[],
        deterministic_input_sha256=_input_sha256(policy_input),
        rationale="customer-facing policy requirements are satisfied",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _policy_blockers(policy_input: CustomerPolicyInput) -> list[str]:
    blockers: list[str] = []
    if policy_input.decision_state != AutoValidationDecisionState.AUTO_ACCEPTED:
        blockers.append(
            f"decision_not_auto_accepted:{policy_input.decision_state.value}"
        )
    if is_private_source_url(policy_input.source_url):
        blockers.append("private_source_risk")
    if not policy_input.public_source_ref_ids:
        blockers.append("missing_public_source_refs")
    if policy_input.validation_audit_ref is None:
        blockers.append("missing_validation_audit_ref")
    if policy_input.recompute_provenance_ref is None:
        blockers.append("missing_recompute_provenance")
    if not policy_input.visible_caveats:
        blockers.append("missing_visible_caveats")

    forbidden = find_forbidden_wording(
        "\n".join([policy_input.display_text, *policy_input.visible_caveats])
    )
    blockers.extend(
        f"forbidden_wording:{finding.category.value}:{finding.phrase}"
        for finding in forbidden
    )
    return sorted(set(blockers))


def _policy_evidence_refs(policy_input: CustomerPolicyInput) -> list[str]:
    refs = {
        *policy_input.public_source_ref_ids,
        *(
            set()
            if policy_input.validation_audit_ref is None
            else {policy_input.validation_audit_ref}
        ),
        *(
            set()
            if policy_input.recompute_provenance_ref is None
            else {policy_input.recompute_provenance_ref}
        ),
    }
    return sorted(refs) or [f"policy-input:{policy_input.candidate_id}"]


def _input_sha256(policy_input: CustomerPolicyInput) -> str:
    payload = policy_input.model_dump(mode="json", by_alias=False, exclude_none=True)
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
