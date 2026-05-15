"""Unit tests for artifact evidence packets."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    ArtifactHashSet,
    ArtifactRegistryRecord,
    build_artifact_evidence_packet,
    validate_artifact_file,
)

VALID_ARTIFACT = "tests/fixtures/artifacts/valid_artifact.json"
CREATED_AT = datetime(2026, 5, 14, 12, 0, tzinfo=UTC)


def valid_record(**overrides: object) -> ArtifactRegistryRecord:
    validation_result = validate_artifact_file(VALID_ARTIFACT)
    artifact = validation_result.artifact
    assert artifact is not None
    payload: dict[str, object] = {
        "artifact_id": "artifact-001",
        "product": artifact.product,
        "source_run_id": artifact.run_id,
        "validation_status": "valid",
        "validation_result": validation_result,
        "hashes": ArtifactHashSet(
            artifact_hash="sha256:artifact",
            policy_config_hash=artifact.policy_config_hash,
            code_version_ref=artifact.code_version_ref,
            input_hashes=artifact.input_hashes,
        ),
        "generated_artifact_refs": artifact.generated_artifact_refs,
        "no_claim_boundary": artifact.no_claim_boundary,
        "created_at": CREATED_AT,
        "current_governance_state": "registered_internal",
    }
    payload.update(overrides)
    return ArtifactRegistryRecord.model_validate(payload)


def test_evidence_packet_requires_core_sections() -> None:
    packet = build_artifact_evidence_packet(
        valid_record(),
        limitations=("synthetic fixture only",),
        review_refs=("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",),
    )

    assert packet.packet_version == "entropy-artifact-evidence/v1"
    assert packet.artifact_summary.artifact_id == "artifact-001"
    assert packet.validation_result.ok is True
    assert packet.registry_status.validation_status == "valid"
    assert packet.reproducibility_status == "not_checked"
    assert packet.limitations == ("synthetic fixture only",)
    assert "not_production" in packet.claim_boundary
    assert packet.review_refs == ("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",)
    assert packet.approval_state == "not_approved"


def test_evidence_packet_serializes_deterministically() -> None:
    packet = build_artifact_evidence_packet(
        valid_record(),
        limitations=("synthetic fixture only",),
        review_refs=("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",),
    )

    assert packet.to_deterministic_json() == packet.to_deterministic_json()
    assert packet.to_deterministic_json().startswith('{"approval_state":"not_approved"')


def test_evidence_packet_rejects_unsupported_approval_state() -> None:
    with pytest.raises(ValidationError):
        build_artifact_evidence_packet(
            valid_record(),
            limitations=("synthetic fixture only",),
            review_refs=("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",),
            approval_state="approved_external",  # type: ignore[arg-type]
        )

    with pytest.raises(ValidationError, match="not supported by registry history"):
        build_artifact_evidence_packet(
            valid_record(current_governance_state="blocked"),
            limitations=("synthetic fixture only",),
            review_refs=("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",),
            approval_state="internal_only",
        )
