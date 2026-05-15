"""Unit tests for governed artifact registry models."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    ArtifactHashSet,
    ArtifactRegistryEvent,
    ArtifactRegistryRecord,
    ArtifactRegistryViolation,
    ArtifactValidationResult,
    append_registry_event,
    validate_artifact_file,
)

VALID_ARTIFACT = "tests/fixtures/artifacts/valid_artifact.json"
INVALID_ARTIFACT = "tests/fixtures/artifacts/invalid_artifact.json"
CREATED_AT = datetime(2026, 5, 14, 12, 0, tzinfo=UTC)


def valid_registry_record(**overrides: object) -> ArtifactRegistryRecord:
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
            generated_artifact_hashes=("sha256:report",),
        ),
        "generated_artifact_refs": artifact.generated_artifact_refs,
        "no_claim_boundary": artifact.no_claim_boundary,
        "created_at": CREATED_AT,
        "current_governance_state": "registered_internal",
    }
    payload.update(overrides)
    return ArtifactRegistryRecord.model_validate(payload)


def test_registry_record_requires_governed_fields() -> None:
    record = valid_registry_record()

    assert record.registry_record_version == "entropy-artifact-registry/v1"
    assert record.artifact_contract_version == "entropy-core-artifact/v1"
    assert record.artifact_id == "artifact-001"
    assert record.product == "internal-core-fixture"
    assert record.validation_status == "valid"
    assert record.hashes.artifact_hash == "sha256:artifact"
    assert record.generated_artifact_refs == ("reports/internal-fixture.md",)
    assert record.created_at == CREATED_AT
    assert record.current_governance_state == "registered_internal"

    with pytest.raises(ValidationError):
        ArtifactRegistryRecord.model_validate(record.model_dump(mode="python") | {"extra": "no"})


def test_registry_corrections_are_append_only() -> None:
    record = valid_registry_record()
    correction = valid_registry_record(
        artifact_id="artifact-002",
        correction_of_artifact_id=record.artifact_id,
    )
    event = ArtifactRegistryEvent(
        event_id="event-001",
        artifact_id=record.artifact_id,
        event_type="correction_appended",
        created_at=CREATED_AT,
        actor="core-operator",
        reason="append correction record for reviewed metadata",
        new_governance_state="superseded_by_correction",
        correction_record_id=correction.artifact_id,
    )

    history: tuple[ArtifactRegistryEvent, ...] = ()
    updated_history = append_registry_event(history, event)

    assert history == ()
    assert updated_history == (event,)
    assert record.current_governance_state == "registered_internal"
    assert correction.correction_of_artifact_id == record.artifact_id
    with pytest.raises(ArtifactRegistryViolation, match="Duplicate registry event id"):
        append_registry_event(updated_history, event)
    with pytest.raises(ValidationError, match="Correction events require"):
        ArtifactRegistryEvent(
            event_id="event-002",
            artifact_id=record.artifact_id,
            event_type="correction_appended",
            created_at=CREATED_AT,
            actor="core-operator",
            reason="missing correction id",
            new_governance_state="superseded_by_correction",
        )


def test_registry_rejects_unvalidated_or_unsafe_records() -> None:
    invalid_result = validate_artifact_file(INVALID_ARTIFACT)
    with pytest.raises(ValidationError, match="Registry records require"):
        valid_registry_record(validation_result=invalid_result)

    empty_result = ArtifactValidationResult(ok=False)
    with pytest.raises(ValidationError, match="Registry records require"):
        valid_registry_record(validation_result=empty_result)

    with pytest.raises(ValidationError, match="Registry no-claim boundary must match"):
        valid_registry_record(no_claim_boundary=("production",))
