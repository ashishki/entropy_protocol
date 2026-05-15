"""Unit tests for artifact metadata repository fallback behavior."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from entropy.artifacts import (
    ArtifactHashSet,
    ArtifactMetadataRepository,
    ArtifactMetadataRepositoryViolation,
    ArtifactRegistryRecord,
    validate_artifact_file,
)

VALID_ARTIFACT = "tests/fixtures/artifacts/valid_artifact.json"


def test_repository_fallback_without_database() -> None:
    record = valid_record()
    repository = ArtifactMetadataRepository()

    metadata_result = repository.insert_artifact_metadata(record)
    event_result = repository.append_validation_event(
        event_id="event-001",
        artifact_id=record.artifact_id,
        validation_result=record.validation_result,
    )

    assert metadata_result.backend == "local_registry"
    assert event_result.backend == "local_registry"
    assert metadata_result.artifact_id == record.artifact_id
    with pytest.raises(ArtifactMetadataRepositoryViolation, match="cannot be mutated"):
        repository.reject_append_only_event_mutation("modify")


def valid_record() -> ArtifactRegistryRecord:
    validation_result = validate_artifact_file(VALID_ARTIFACT)
    artifact = validation_result.artifact
    assert artifact is not None
    return ArtifactRegistryRecord(
        artifact_id="artifact-001",
        product=artifact.product,
        source_run_id=artifact.run_id,
        validation_status="valid",
        validation_result=validation_result,
        hashes=ArtifactHashSet(
            artifact_hash="sha256:artifact",
            policy_config_hash=artifact.policy_config_hash,
            code_version_ref=artifact.code_version_ref,
            input_hashes=artifact.input_hashes,
        ),
        generated_artifact_refs=artifact.generated_artifact_refs,
        no_claim_boundary=artifact.no_claim_boundary,
        created_at=datetime(2026, 5, 14, 12, 0, tzinfo=UTC),
        current_governance_state="registered_internal",
    )
