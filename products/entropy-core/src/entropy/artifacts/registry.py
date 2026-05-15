"""Governed artifact registry record and append-only event models."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.artifacts.contract import (
    ARTIFACT_CONTRACT_VERSION,
    contains_unsafe_claim_label,
    is_blocked_no_claim_boundary,
)
from entropy.artifacts.validation import ArtifactValidationResult
from entropy.artifacts.validation import validate_artifact_file

ARTIFACT_REGISTRY_SCHEMA_VERSION = "entropy-artifact-registry/v1"

ARTIFACT_REGISTRY_STATUSES = ("valid",)
ARTIFACT_REGISTRY_GOVERNANCE_STATES = (
    "registered_internal",
    "blocked",
    "superseded_by_correction",
    "rejected",
)
ARTIFACT_REGISTRY_EVENT_TYPES = (
    "registered",
    "correction_appended",
    "governance_state_changed",
)


class ArtifactRegistryViolation(ValueError):
    """Raised when artifact registry invariants are violated."""


class ArtifactRegistryDuplicate(ArtifactRegistryViolation):
    """Raised when an artifact is already registered."""


class ArtifactRegistryNotFound(ArtifactRegistryViolation):
    """Raised when a registry record cannot be found."""


class ArtifactHashSet(BaseModel):
    """Hash bindings retained by a registry record."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    artifact_hash: str = Field(min_length=1)
    policy_config_hash: str = Field(min_length=1)
    code_version_ref: str = Field(min_length=1)
    input_hashes: tuple[str, ...] = ()
    generated_artifact_hashes: tuple[str, ...] = ()


class ArtifactRegistryRecord(BaseModel):
    """Immutable governed metadata for one validated artifact."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    registry_record_version: Literal["entropy-artifact-registry/v1"] = (
        ARTIFACT_REGISTRY_SCHEMA_VERSION
    )
    artifact_id: str = Field(min_length=1)
    artifact_contract_version: Literal["entropy-core-artifact/v1"] = ARTIFACT_CONTRACT_VERSION
    product: str = Field(min_length=1)
    source_run_id: str = Field(min_length=1)
    validation_status: Literal["valid"]
    validation_result: ArtifactValidationResult
    hashes: ArtifactHashSet
    generated_artifact_refs: tuple[str, ...] = Field(min_length=1)
    no_claim_boundary: tuple[str, ...] = Field(min_length=1)
    created_at: datetime
    current_governance_state: Literal[
        "registered_internal",
        "blocked",
        "superseded_by_correction",
        "rejected",
    ]
    correction_of_artifact_id: str | None = None

    @model_validator(mode="after")
    def validate_registry_record(self) -> "ArtifactRegistryRecord":
        artifact = self.validation_result.artifact
        if not self.validation_result.ok or artifact is None:
            raise ArtifactRegistryViolation("Registry records require a valid artifact result.")
        if artifact.artifact_contract_version != self.artifact_contract_version:
            raise ArtifactRegistryViolation("Registry contract version must match artifact.")
        if artifact.product != self.product:
            raise ArtifactRegistryViolation("Registry product must match artifact.")
        if artifact.run_id != self.source_run_id:
            raise ArtifactRegistryViolation("Registry source run id must match artifact.")
        if artifact.generated_artifact_refs != self.generated_artifact_refs:
            raise ArtifactRegistryViolation("Registry generated refs must match artifact.")
        if artifact.no_claim_boundary != self.no_claim_boundary:
            raise ArtifactRegistryViolation("Registry no-claim boundary must match artifact.")

        unresolved = tuple(
            boundary
            for boundary in self.no_claim_boundary
            if contains_unsafe_claim_label(boundary) and not is_blocked_no_claim_boundary(boundary)
        )
        if unresolved:
            raise ArtifactRegistryViolation(
                "Registry records cannot contain unresolved unsafe claims."
            )
        return self


class ArtifactRegistryEvent(BaseModel):
    """Append-only registry event for registration, correction, and state changes."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    registry_record_version: Literal["entropy-artifact-registry/v1"] = (
        ARTIFACT_REGISTRY_SCHEMA_VERSION
    )
    event_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    event_type: Literal["registered", "correction_appended", "governance_state_changed"]
    created_at: datetime
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    new_governance_state: Literal[
        "registered_internal",
        "blocked",
        "superseded_by_correction",
        "rejected",
    ]
    correction_record_id: str | None = None
    prior_event_id: str | None = None

    @model_validator(mode="after")
    def validate_event_shape(self) -> "ArtifactRegistryEvent":
        if self.event_type == "correction_appended" and self.correction_record_id is None:
            raise ArtifactRegistryViolation("Correction events require a correction record id.")
        if self.event_type != "correction_appended" and self.correction_record_id is not None:
            raise ArtifactRegistryViolation("Only correction events may reference corrections.")
        return self


def append_registry_event(
    history: tuple[ArtifactRegistryEvent, ...],
    event: ArtifactRegistryEvent,
) -> tuple[ArtifactRegistryEvent, ...]:
    """Return a new event history with one appended event."""
    event_ids = {existing.event_id for existing in history}
    if event.event_id in event_ids:
        raise ArtifactRegistryViolation("Duplicate registry event id.")
    return (*history, event)


def register_artifact_file(
    artifact_path: str | Path,
    registry_dir: str | Path,
    *,
    created_at: datetime | None = None,
    actor: str = "local-operator",
) -> tuple[ArtifactRegistryRecord, ArtifactRegistryEvent]:
    """Validate and append one artifact registry record and registration event."""
    path = Path(artifact_path)
    validation_result = validate_artifact_file(path)
    if not validation_result.ok or validation_result.artifact is None:
        raise ArtifactRegistryViolation("Cannot register invalid artifact.")

    artifact_hash = _sha256_file(path)
    artifact_id = "artifact-" + artifact_hash.removeprefix("sha256:")[:16]
    registry_path = Path(registry_dir)
    existing = _read_records(registry_path)
    if artifact_id in existing:
        raise ArtifactRegistryDuplicate("Artifact already registered.")

    artifact = validation_result.artifact
    event_time = created_at or datetime.now().astimezone()
    record = ArtifactRegistryRecord(
        artifact_id=artifact_id,
        product=artifact.product,
        source_run_id=artifact.run_id,
        validation_status="valid",
        validation_result=validation_result,
        hashes=ArtifactHashSet(
            artifact_hash=artifact_hash,
            policy_config_hash=artifact.policy_config_hash,
            code_version_ref=artifact.code_version_ref,
            input_hashes=artifact.input_hashes,
        ),
        generated_artifact_refs=artifact.generated_artifact_refs,
        no_claim_boundary=artifact.no_claim_boundary,
        created_at=event_time,
        current_governance_state="registered_internal",
    )
    event = ArtifactRegistryEvent(
        event_id="event-" + hashlib.sha256(f"{artifact_id}:registered".encode()).hexdigest()[:16],
        artifact_id=artifact_id,
        event_type="registered",
        created_at=event_time,
        actor=actor,
        reason="validated artifact registered",
        new_governance_state="registered_internal",
    )

    _append_jsonl(_records_path(registry_path), record.model_dump(mode="json"))
    _append_jsonl(_events_path(registry_path), event.model_dump(mode="json"))
    return record, event


def show_artifact_record(artifact_id: str, registry_dir: str | Path) -> ArtifactRegistryRecord:
    """Read one artifact registry record by id."""
    records = _read_records(Path(registry_dir))
    try:
        return records[artifact_id]
    except KeyError as exc:
        raise ArtifactRegistryNotFound("Artifact registry record not found.") from exc


def list_artifact_records(registry_dir: str | Path) -> tuple[ArtifactRegistryRecord, ...]:
    """Return registry records in deterministic display order."""
    records = _read_records(Path(registry_dir)).values()
    return tuple(sorted(records, key=lambda record: (record.created_at, record.artifact_id)))


def read_artifact_history(
    artifact_id: str,
    registry_dir: str | Path,
) -> tuple[ArtifactRegistryEvent, ...]:
    """Return append-only registry events for one artifact in deterministic order."""
    show_artifact_record(artifact_id, registry_dir)
    return tuple(event for event in _read_events(Path(registry_dir)) if event.artifact_id == artifact_id)


def safe_registry_record_metadata(record: ArtifactRegistryRecord) -> dict[str, object]:
    """Return safe metadata without raw validation payload fields."""
    return {
        "artifact_id": record.artifact_id,
        "artifact_contract_version": record.artifact_contract_version,
        "product": record.product,
        "source_run_id": record.source_run_id,
        "validation_status": record.validation_status,
        "current_governance_state": record.current_governance_state,
        "created_at": record.created_at.isoformat(),
        "hashes": record.hashes.model_dump(mode="json"),
        "generated_artifact_refs": list(record.generated_artifact_refs),
        "correction_of_artifact_id": record.correction_of_artifact_id,
    }


def _read_records(registry_dir: Path) -> dict[str, ArtifactRegistryRecord]:
    records: dict[str, ArtifactRegistryRecord] = {}
    path = _records_path(registry_dir)
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = ArtifactRegistryRecord.model_validate(json.loads(line))
        records[record.artifact_id] = record
    return records


def _read_events(registry_dir: Path) -> tuple[ArtifactRegistryEvent, ...]:
    path = _events_path(registry_dir)
    if not path.exists():
        return ()
    return tuple(
        ArtifactRegistryEvent.model_validate(json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def _append_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


def _records_path(registry_dir: Path) -> Path:
    return registry_dir / "records.jsonl"


def _events_path(registry_dir: Path) -> Path:
    return registry_dir / "events.jsonl"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


__all__ = [
    "ARTIFACT_REGISTRY_EVENT_TYPES",
    "ARTIFACT_REGISTRY_GOVERNANCE_STATES",
    "ARTIFACT_REGISTRY_SCHEMA_VERSION",
    "ARTIFACT_REGISTRY_STATUSES",
    "ArtifactHashSet",
    "ArtifactRegistryDuplicate",
    "ArtifactRegistryEvent",
    "ArtifactRegistryNotFound",
    "ArtifactRegistryRecord",
    "ArtifactRegistryViolation",
    "append_registry_event",
    "list_artifact_records",
    "read_artifact_history",
    "register_artifact_file",
    "safe_registry_record_metadata",
    "show_artifact_record",
]
