"""Machine-readable evidence packets for governed artifacts."""

from __future__ import annotations

import json
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.artifacts.registry import ArtifactRegistryRecord
from entropy.artifacts.reproducibility import ReproductionCompareResult
from entropy.artifacts.validation import ArtifactValidationResult

ARTIFACT_EVIDENCE_PACKET_VERSION = "entropy-artifact-evidence/v1"
SUPPORTED_EVIDENCE_APPROVAL_STATES = ("not_approved", "internal_only")


class ArtifactEvidencePacketViolation(ValueError):
    """Raised when an evidence packet claims unsupported approval state."""


class ArtifactEvidenceSummary(BaseModel):
    """Safe artifact identity fields for an evidence packet."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    artifact_id: str = Field(min_length=1)
    artifact_contract_version: str = Field(min_length=1)
    product: str = Field(min_length=1)
    source_run_id: str = Field(min_length=1)


class ArtifactRegistryEvidenceStatus(BaseModel):
    """Registry status fields carried into evidence packets."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    validation_status: str = Field(min_length=1)
    current_governance_state: str = Field(min_length=1)


class ArtifactEvidencePacket(BaseModel):
    """Deterministic evidence packet for validated and registered artifacts."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    packet_version: Literal["entropy-artifact-evidence/v1"] = ARTIFACT_EVIDENCE_PACKET_VERSION
    artifact_summary: ArtifactEvidenceSummary
    validation_result: ArtifactValidationResult
    registry_status: ArtifactRegistryEvidenceStatus
    reproducibility_status: Literal[
        "exact",
        "materially_equivalent",
        "partial",
        "declared_non_reproducible",
        "failed",
        "not_checked",
    ]
    limitations: tuple[str, ...] = Field(min_length=1)
    claim_boundary: tuple[str, ...] = Field(min_length=1)
    review_refs: tuple[str, ...] = Field(min_length=1)
    approval_state: Literal["not_approved", "internal_only"] = "not_approved"

    @model_validator(mode="after")
    def validate_supported_state(self) -> "ArtifactEvidencePacket":
        if self.approval_state != "not_approved" and (
            self.registry_status.current_governance_state != "registered_internal"
        ):
            raise ArtifactEvidencePacketViolation(
                "Evidence approval state is not supported by registry history."
            )
        return self

    def to_deterministic_json(self) -> str:
        """Serialize packet deterministically."""
        return json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def build_artifact_evidence_packet(
    record: ArtifactRegistryRecord,
    *,
    reproducibility: ReproductionCompareResult | None = None,
    limitations: tuple[str, ...],
    review_refs: tuple[str, ...],
    approval_state: Literal["not_approved", "internal_only"] = "not_approved",
) -> ArtifactEvidencePacket:
    """Build a safe evidence packet from registry and optional reproducibility state."""
    return ArtifactEvidencePacket(
        artifact_summary=ArtifactEvidenceSummary(
            artifact_id=record.artifact_id,
            artifact_contract_version=record.artifact_contract_version,
            product=record.product,
            source_run_id=record.source_run_id,
        ),
        validation_result=record.validation_result,
        registry_status=ArtifactRegistryEvidenceStatus(
            validation_status=record.validation_status,
            current_governance_state=record.current_governance_state,
        ),
        reproducibility_status=reproducibility.status if reproducibility else "not_checked",
        limitations=limitations,
        claim_boundary=record.no_claim_boundary,
        review_refs=review_refs,
        approval_state=approval_state,
    )


__all__ = [
    "ARTIFACT_EVIDENCE_PACKET_VERSION",
    "SUPPORTED_EVIDENCE_APPROVAL_STATES",
    "ArtifactEvidencePacket",
    "ArtifactEvidencePacketViolation",
    "ArtifactEvidenceSummary",
    "ArtifactRegistryEvidenceStatus",
    "build_artifact_evidence_packet",
]
