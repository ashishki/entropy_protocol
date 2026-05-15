"""Capital Allocation Framework artifact vocabulary and schemas."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.artifacts.contract import ARTIFACT_CONTRACT_VERSION, ArtifactContractV1

CAF_ARTIFACT_SCHEMA_VERSION = "entropy-caf-artifact/v1"
CAF_ARTIFACT_TYPES = (
    "allocation_decision",
    "risk_policy",
    "portfolio_constraint",
    "decision_rationale",
    "decision_evidence_bundle",
)
CAF_REQUIRED_NO_CLAIM_LABELS = (
    "not_investment_advice",
    "not_live_allocation",
    "not_capital_ready",
    "not_automated_execution",
)
CAF_FORBIDDEN_EXECUTION_FIELDS = (
    "broker_id",
    "order_id",
    "execution_venue",
    "capital_amount",
    "account_id",
)
CAF_UNSAFE_CLAIM_LABELS = (
    "investment_advice",
    "live_allocation",
    "capital_ready",
    "automated_execution",
    "future_performance",
)


class CAFArtifactViolation(ValueError):
    """Raised when a CAF artifact would imply execution or advice."""


class FourStreamAttributionRefs(BaseModel):
    """Four-stream attribution references without treasury blending."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    stream_a_ref: str = Field(min_length=1)
    stream_b_ref: str = Field(min_length=1)
    stream_c_ref: str = Field(min_length=1)
    stream_d_ref: str = Field(min_length=1)
    net_sharpe_streams: tuple[Literal["stream_a", "stream_b", "stream_c"], ...] = Field(
        default=("stream_a", "stream_b", "stream_c"),
        min_length=1,
    )


class AllocationDecisionArtifact(BaseModel):
    """Governed no-execution allocation decision artifact."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    caf_artifact_version: Literal["entropy-caf-artifact/v1"] = CAF_ARTIFACT_SCHEMA_VERSION
    artifact_contract_version: Literal["entropy-core-artifact/v1"] = ARTIFACT_CONTRACT_VERSION
    artifact_type: Literal["allocation_decision"] = "allocation_decision"
    decision_id: str = Field(min_length=1)
    portfolio_context_ref: str = Field(min_length=1)
    constraint_refs: tuple[str, ...] = Field(min_length=1)
    evidence_refs: tuple[str, ...] = Field(min_length=1)
    rationale_refs: tuple[str, ...] = Field(min_length=1)
    attribution_refs: FourStreamAttributionRefs
    limitations: tuple[str, ...] = Field(min_length=1)
    no_claim_boundary: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_caf_boundaries(self) -> "AllocationDecisionArtifact":
        missing = set(CAF_REQUIRED_NO_CLAIM_LABELS).difference(self.no_claim_boundary)
        if missing:
            raise CAFArtifactViolation(
                "CAF artifacts require no-claim labels: " + ", ".join(sorted(missing))
            )
        unsafe = tuple(label for label in self.no_claim_boundary if _is_unsafe_unblocked(label))
        if unsafe:
            raise CAFArtifactViolation(
                "CAF artifacts cannot claim advice, execution, capital-ready, or future performance: "
                + ", ".join(unsafe)
            )
        return self

    def to_artifact_contract(self) -> ArtifactContractV1:
        """Render this CAF artifact as the base Core artifact contract."""
        attribution_refs = (
            self.attribution_refs.stream_a_ref,
            self.attribution_refs.stream_b_ref,
            self.attribution_refs.stream_c_ref,
            self.attribution_refs.stream_d_ref,
        )
        return ArtifactContractV1(
            product="entropy-core-caf",
            run_id=self.decision_id,
            input_refs=(
                self.portfolio_context_ref,
                *self.constraint_refs,
                *self.evidence_refs,
                *self.rationale_refs,
                *attribution_refs,
            ),
            policy_config_hash="sha256:synthetic-caf-policy-v1",
            code_version_ref="git:entropy-core-caf-schema-v1",
            generated_artifact_refs=(f"artifacts/caf/{self.decision_id}.json",),
            limitations=self.limitations,
            no_claim_boundary=self.no_claim_boundary,
            manual_validation_status="not_reviewed",
            error_register_ref="error-registers/caf-artifact.md",
            external_delivery_approval_status="not_requested",
        )


def _is_unsafe_unblocked(label: str) -> bool:
    normalized = _normalize_label(label)
    if normalized.startswith(("not_", "no_", "non_", "blocked_", "without_")):
        return False
    return any(claim in normalized for claim in CAF_UNSAFE_CLAIM_LABELS)


def _normalize_label(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(part for part in normalized.split("_") if part)


__all__ = [
    "CAF_ARTIFACT_SCHEMA_VERSION",
    "CAF_ARTIFACT_TYPES",
    "CAF_FORBIDDEN_EXECUTION_FIELDS",
    "CAF_REQUIRED_NO_CLAIM_LABELS",
    "CAF_UNSAFE_CLAIM_LABELS",
    "AllocationDecisionArtifact",
    "CAFArtifactViolation",
    "FourStreamAttributionRefs",
]
