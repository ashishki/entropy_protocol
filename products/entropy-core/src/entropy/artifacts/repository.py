"""Artifact metadata repository with database insert and local fallback paths."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from entropy.artifacts.registry import ArtifactRegistryRecord, safe_registry_record_metadata
from entropy.artifacts.validation import ArtifactValidationResult
from entropy.db.models import ArtifactRecordMetadata, ArtifactValidationEvent


class ArtifactMetadataRepositoryViolation(ValueError):
    """Raised when repository usage would violate append-only behavior."""


class ArtifactMetadataRepositoryResult(BaseModel):
    """Stable repository write/fallback result."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    ok: bool
    backend: Literal["database", "local_registry"]
    artifact_id: str


class ArtifactMetadataRepository:
    """Insert-only repository for artifact metadata and append-only events."""

    def __init__(self, session: Session | None = None) -> None:
        self.session = session

    def insert_artifact_metadata(
        self,
        record: ArtifactRegistryRecord,
    ) -> ArtifactMetadataRepositoryResult:
        """Insert artifact metadata or report local fallback when no DB is configured."""
        if self.session is None:
            return ArtifactMetadataRepositoryResult(
                ok=True,
                backend="local_registry",
                artifact_id=record.artifact_id,
            )

        self.session.add(
            ArtifactRecordMetadata(
                artifact_id=record.artifact_id,
                artifact_contract_version=record.artifact_contract_version,
                product=record.product,
                source_run_id=record.source_run_id,
                validation_status=record.validation_status,
                current_governance_state=record.current_governance_state,
                artifact_hash=record.hashes.artifact_hash,
                policy_config_hash=record.hashes.policy_config_hash,
                code_version_ref=record.hashes.code_version_ref,
                metadata_payload=safe_registry_record_metadata(record),
            )
        )
        self.session.commit()
        return ArtifactMetadataRepositoryResult(
            ok=True,
            backend="database",
            artifact_id=record.artifact_id,
        )

    def append_validation_event(
        self,
        *,
        event_id: str,
        artifact_id: str,
        validation_result: ArtifactValidationResult,
    ) -> ArtifactMetadataRepositoryResult:
        """Append a validation event or report local fallback when no DB is configured."""
        if self.session is None:
            return ArtifactMetadataRepositoryResult(
                ok=True,
                backend="local_registry",
                artifact_id=artifact_id,
            )

        self.session.add(
            ArtifactValidationEvent(
                event_id=event_id,
                artifact_id=artifact_id,
                validation_status="valid" if validation_result.ok else "invalid",
                error_count=len(validation_result.errors),
                payload=validation_result.model_dump(mode="json"),
            )
        )
        self.session.commit()
        return ArtifactMetadataRepositoryResult(
            ok=True,
            backend="database",
            artifact_id=artifact_id,
        )

    def reject_append_only_event_mutation(self, operation: str) -> None:
        """Reject any caller trying to mutate append-only event rows."""
        raise ArtifactMetadataRepositoryViolation(
            "Append-only artifact event rows cannot be mutated by repository operation: "
            + operation
        )


__all__ = [
    "ArtifactMetadataRepository",
    "ArtifactMetadataRepositoryResult",
    "ArtifactMetadataRepositoryViolation",
]
