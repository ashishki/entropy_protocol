"""Research artifact schemas compatible with the Core artifact contract."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.artifacts.contract import ARTIFACT_CONTRACT_VERSION, ArtifactContractV1
from entropy.evidence.first_research_packet import FirstResearchEvidencePacket

RESEARCH_ARTIFACT_SCHEMA_VERSION = "entropy-research-artifact/v1"
REQUIRED_RESEARCH_NO_CLAIM_LABELS = (
    "archive_only_research",
    "not_holdout_unlock",
    "not_oos_performance",
    "not_production",
    "not_capital_ready",
)
UNSUPPORTED_RESEARCH_CLAIM_LABELS = (
    "holdout",
    "holdout_access",
    "holdout_unlock",
    "oos",
    "oos_performance",
    "performance",
    "performance_claim",
    "production",
    "capital_ready",
)


class ResearchArtifactViolation(ValueError):
    """Raised when a research artifact would broaden claim scope."""


class ResearchArtifact(BaseModel):
    """Artifact-contract-compatible representation of Core research outputs."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    research_artifact_version: Literal["entropy-research-artifact/v1"] = (
        RESEARCH_ARTIFACT_SCHEMA_VERSION
    )
    artifact_contract_version: Literal["entropy-core-artifact/v1"] = ARTIFACT_CONTRACT_VERSION
    artifact_kind: Literal["candidate", "dataset", "evaluation", "report"]
    candidate_id: str = Field(min_length=1)
    dataset_hash: str = Field(min_length=1)
    code_hash: str = Field(min_length=1)
    policy_hash: str = Field(min_length=1)
    report_hash: str | None = Field(default=None, min_length=1)
    leakage_status: Literal["PASS", "FAIL", "not_checked"]
    no_claim_labels: tuple[str, ...] = Field(min_length=1)
    source_refs: tuple[str, ...] = Field(min_length=1)
    generated_artifact_refs: tuple[str, ...] = Field(min_length=1)
    limitations: tuple[str, ...] = Field(min_length=1)
    holdout_gate_status: Literal["absent", "approved"] = "absent"
    oos_performance_gate_status: Literal["absent", "approved"] = "absent"
    error_register_ref: str = "error-registers/research-artifact.md"

    @model_validator(mode="after")
    def validate_research_artifact(self) -> "ResearchArtifact":
        for name, value in (
            ("dataset_hash", self.dataset_hash),
            ("code_hash", self.code_hash),
            ("policy_hash", self.policy_hash),
        ):
            _require_bound_hash(name, value)
        if self.report_hash is not None:
            _require_bound_hash("report_hash", self.report_hash)

        missing_labels = set(REQUIRED_RESEARCH_NO_CLAIM_LABELS).difference(self.no_claim_labels)
        if missing_labels:
            raise ResearchArtifactViolation(
                "Research artifacts require no-claim labels: " + ", ".join(sorted(missing_labels))
            )

        if (
            self.holdout_gate_status != "approved"
            or self.oos_performance_gate_status != "approved"
            or self.leakage_status != "PASS"
        ):
            unsupported = tuple(
                label for label in self.no_claim_labels if _is_unsupported_unblocked_claim(label)
            )
            if unsupported:
                raise ResearchArtifactViolation(
                    "Research artifacts cannot claim OOS/performance or production surfaces "
                    "without gates: " + ", ".join(unsupported)
                )
        return self

    def to_artifact_contract(self) -> ArtifactContractV1:
        """Render this research artifact as the base Core artifact contract."""
        return ArtifactContractV1(
            product="entropy-core-research",
            run_id=self.candidate_id,
            input_refs=self.source_refs,
            input_hashes=tuple(
                hash_value
                for hash_value in (self.dataset_hash, self.report_hash)
                if hash_value is not None
            ),
            policy_config_hash=self.policy_hash,
            code_version_ref=self.code_hash,
            generated_artifact_refs=self.generated_artifact_refs,
            limitations=self.limitations,
            no_claim_boundary=self.no_claim_labels,
            manual_validation_status="not_reviewed",
            error_register_ref=self.error_register_ref,
            external_delivery_approval_status="not_requested",
        )


def research_artifact_from_archive_packet(packet: FirstResearchEvidencePacket) -> ResearchArtifact:
    """Represent an existing archive-only research packet without changing its meaning."""
    return ResearchArtifact(
        artifact_kind="report",
        candidate_id=packet.candidate_id,
        dataset_hash=packet.dataset_hash,
        code_hash=packet.code_hash,
        policy_hash=packet.policy_hash,
        report_hash=packet.evidence_packet_hash,
        leakage_status=packet.leakage_status,
        no_claim_labels=("archive_only_research", *packet.no_claim_labels),
        source_refs=packet.artifact_refs,
        generated_artifact_refs=packet.artifact_refs,
        limitations=("archive-only historical research packet representation",),
    )


def archive_packet_to_artifact_payload(packet: FirstResearchEvidencePacket) -> dict[str, object]:
    """Convert an archive-only research packet into a base artifact payload."""
    return (
        research_artifact_from_archive_packet(packet).to_artifact_contract().model_dump(mode="json")
    )


def _require_bound_hash(name: str, value: str) -> None:
    if not value.strip() or value.startswith("PENDING_"):
        raise ResearchArtifactViolation(name + " must be bound.")


def _is_unsupported_unblocked_claim(label: str) -> bool:
    normalized = _normalize_claim_label(label)
    if normalized.startswith(("not_", "no_", "non_", "blocked_", "without_")):
        return False
    return any(claim in normalized for claim in UNSUPPORTED_RESEARCH_CLAIM_LABELS)


def _normalize_claim_label(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(part for part in normalized.split("_") if part)


__all__ = [
    "REQUIRED_RESEARCH_NO_CLAIM_LABELS",
    "RESEARCH_ARTIFACT_SCHEMA_VERSION",
    "UNSUPPORTED_RESEARCH_CLAIM_LABELS",
    "ResearchArtifact",
    "ResearchArtifactViolation",
    "archive_packet_to_artifact_payload",
    "research_artifact_from_archive_packet",
]
