"""Archive dataset manifest binding for the first research packet."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.research.candidate import (
    CandidateHashPlaceholders,
    FirstResearchCandidatePacket,
)

ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION = "archive-dataset-manifest/v1"


class DatasetManifestError(ValueError):
    """Raised when archive dataset manifest boundaries are violated."""


class ManifestBaseModel(BaseModel):
    """Base model for frozen deterministic manifest schemas."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class ArchiveDatasetBinding(ManifestBaseModel):
    """One archive dataset artifact bound into a manifest."""

    dataset_id: str
    path: str
    dataset_hash: str
    row_count: int = Field(ge=0)
    role: Literal["formation", "evaluation_probe"]

    @model_validator(mode="after")
    def reject_holdout_path(self) -> "ArchiveDatasetBinding":
        if _looks_like_holdout_path(self.path):
            raise DatasetManifestError("Holdout path is forbidden in archive dataset manifest")
        return self


class ArchiveDatasetManifest(ManifestBaseModel):
    """Archive-only dataset manifest with aggregate hash binding."""

    schema_version: Literal["archive-dataset-manifest/v1"] = ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION
    candidate_id: str
    formation_scope: str
    evaluation_scope: str
    dataset_bindings: tuple[ArchiveDatasetBinding, ...] = Field(min_length=1)
    holdout_exclusion: Literal["holdout_locked_not_read"] = "holdout_locked_not_read"
    holdout_paths: tuple[str, ...] = ()
    aggregate_dataset_hash: str
    manifest_hash: str

    @model_validator(mode="after")
    def validate_holdout_exclusion(self) -> "ArchiveDatasetManifest":
        if self.holdout_paths:
            raise DatasetManifestError("Holdout paths must be excluded from archive manifest")
        return self

    def to_markdown(self) -> str:
        """Render the manifest as stable Markdown."""
        lines = [
            "# First Research Archive Dataset Manifest",
            "",
            "Status: ARCHIVE_ONLY_NO_HOLDOUT",
            f"Schema version: {self.schema_version}",
            f"Candidate id: {self.candidate_id}",
            f"Formation scope: {self.formation_scope}",
            f"Evaluation scope: {self.evaluation_scope}",
            f"Holdout exclusion: {self.holdout_exclusion}",
            f"Aggregate dataset hash: {self.aggregate_dataset_hash}",
            f"Manifest hash: {self.manifest_hash}",
            "",
            "## Dataset Bindings",
            "",
            "| Dataset id | Role | Path | Dataset hash | Row count |",
            "|------------|------|------|--------------|-----------|",
        ]
        for binding in self.dataset_bindings:
            lines.append(
                f"| {binding.dataset_id} | {binding.role} | `{binding.path}` | "
                f"`{binding.dataset_hash}` | {binding.row_count} |"
            )
        lines.extend(
            [
                "",
                "## Holdout Boundary",
                "",
                "- Holdout remains locked.",
                "- No holdout path is listed in this manifest.",
                "- No holdout read, unlock, OOS/performance, production, or capital-ready claim is approved.",
                "",
            ]
        )
        return "\n".join(lines)


def build_archive_dataset_manifest(
    *,
    candidate_id: str,
    dataset_bindings: Sequence[ArchiveDatasetBinding],
    formation_scope: str,
    evaluation_scope: str,
    holdout_paths: Sequence[str] = (),
) -> ArchiveDatasetManifest:
    """Build a deterministic archive-only dataset manifest."""
    if holdout_paths:
        raise DatasetManifestError("Holdout paths must be excluded from archive manifest")
    sorted_bindings = tuple(
        sorted(dataset_bindings, key=lambda binding: (binding.path, binding.dataset_id))
    )
    aggregate_dataset_hash = _hash_payload(
        {
            "kind": "aggregate_dataset_hash",
            "schema_version": ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION,
            "dataset_bindings": [binding.model_dump(mode="json") for binding in sorted_bindings],
        }
    )
    manifest_payload = {
        "schema_version": ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "formation_scope": formation_scope,
        "evaluation_scope": evaluation_scope,
        "dataset_bindings": [binding.model_dump(mode="json") for binding in sorted_bindings],
        "holdout_exclusion": "holdout_locked_not_read",
        "holdout_paths": [],
        "aggregate_dataset_hash": aggregate_dataset_hash,
    }
    manifest_hash = _hash_payload(manifest_payload)
    return ArchiveDatasetManifest(
        **manifest_payload,
        manifest_hash=manifest_hash,
    )


def bind_candidate_dataset_manifest(
    packet: FirstResearchCandidatePacket,
    manifest: ArchiveDatasetManifest,
) -> FirstResearchCandidatePacket:
    """Bind a candidate packet to an archive dataset manifest without changing prereg fields."""
    if packet.candidate_id != manifest.candidate_id:
        raise DatasetManifestError("Candidate id does not match dataset manifest")
    hash_placeholders = CandidateHashPlaceholders(
        **{
            **packet.hash_placeholders.model_dump(mode="python"),
            "dataset_hash": manifest.aggregate_dataset_hash,
        }
    )
    return packet.model_copy(update={"hash_placeholders": hash_placeholders})


def deterministic_manifest_json(manifest: ArchiveDatasetManifest) -> str:
    """Serialize a manifest with stable key ordering and compact separators."""
    return json.dumps(manifest.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def _hash_payload(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _looks_like_holdout_path(path: str) -> bool:
    normalized = path.lower().replace("\\", "/")
    return "holdout" in normalized


__all__ = [
    "ARCHIVE_DATASET_MANIFEST_SCHEMA_VERSION",
    "ArchiveDatasetBinding",
    "ArchiveDatasetManifest",
    "DatasetManifestError",
    "bind_candidate_dataset_manifest",
    "build_archive_dataset_manifest",
    "deterministic_manifest_json",
]
