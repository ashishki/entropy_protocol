from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from signal_sandbox.auto_validation.results import (
    ValidationAuditLog,
    ValidationResult,
    ValidationStatus,
)

SHA = "c" * 64
BUNDLE_SHA = "d" * 64
CREATED = datetime(2026, 5, 31, 9, tzinfo=UTC)


def test_validation_result_records_validator_evidence_confidence_and_input_hash() -> (
    None
):
    result = _result()

    assert result.validator_id == "pre_outcome_timing"
    assert result.validator_version == "timing.v1"
    assert result.status == ValidationStatus.PASSED
    assert result.confidence == Decimal("0.92")
    assert result.evidence_ref_ids == ["source-ts-ref", "market-window-ref"]
    assert result.deterministic_input_sha256 == SHA
    assert result.schema_version == "auto_validation_result.v1"


def test_validation_result_rejects_blank_validator_version() -> None:
    with pytest.raises(ValidationError):
        _result(validator_version="")


def test_validation_result_rejects_missing_evidence_refs() -> None:
    with pytest.raises(ValidationError):
        _result(evidence_ref_ids=[])


def test_non_passed_validation_result_requires_blocker_reasons() -> None:
    with pytest.raises(ValidationError, match="blocker_reasons"):
        _result(status=ValidationStatus.UNCERTAIN_NEEDS_HUMAN, blocker_reasons=[])


def test_audit_log_combines_results_without_losing_evidence_refs() -> None:
    timing = _result()
    provider = _result(
        validator_id="provider_eligibility",
        validator_version="provider.v1",
        status=ValidationStatus.EXCLUDED_PROVIDER_GAP,
        confidence=Decimal("0.81"),
        evidence_ref_ids=["asset-ref", "provider-map-ref"],
        blocker_reasons=["no approved provider/proxy for exact instrument"],
    )
    audit = ValidationAuditLog(
        audit_id="audit-1",
        candidate_id="candidate-1",
        evidence_bundle_sha256=BUNDLE_SHA,
        results=[timing, provider],
        created_at_utc=CREATED,
    )

    assert audit.evidence_ref_ids() == [
        "asset-ref",
        "market-window-ref",
        "provider-map-ref",
        "source-ts-ref",
    ]
    assert "provider_eligibility" in audit.canonical_json()
    assert len(audit.audit_sha256()) == 64


def test_audit_log_rejects_mismatched_candidate_results() -> None:
    with pytest.raises(ValidationError, match="candidate_id"):
        ValidationAuditLog(
            audit_id="audit-1",
            candidate_id="candidate-1",
            evidence_bundle_sha256=BUNDLE_SHA,
            results=[_result(candidate_id="other-candidate")],
            created_at_utc=CREATED,
        )


def _result(**overrides: object) -> ValidationResult:
    payload = {
        "validator_id": "pre_outcome_timing",
        "validator_version": "timing.v1",
        "candidate_id": "candidate-1",
        "status": ValidationStatus.PASSED,
        "confidence": Decimal("0.92"),
        "evidence_ref_ids": ["source-ts-ref", "market-window-ref"],
        "blocker_reasons": [],
        "deterministic_input_sha256": SHA,
        "rationale": "source timestamp precedes market window",
        "created_at_utc": CREATED,
    }
    payload.update(overrides)
    return ValidationResult.model_validate(payload)
