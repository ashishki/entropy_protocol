"""Executable schema for entropy-core-artifact/v1 payloads."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ARTIFACT_CONTRACT_VERSION = "entropy-core-artifact/v1"

MANUAL_VALIDATION_STATUSES = (
    "not_reviewed",
    "review_in_progress",
    "validated_internal_only",
    "validated_for_controlled_external_pilot",
    "blocked_by_errors",
    "rejected",
)

EXTERNAL_DELIVERY_APPROVAL_STATUSES = (
    "not_requested",
    "blocked",
    "approved_for_internal_demo",
    "approved_for_controlled_external_pilot",
)

UNSAFE_CLAIM_LABELS = (
    "production",
    "capital_ready",
    "capital-ready",
    "investment_advice",
    "investment advice",
    "holdout_approval",
    "holdout approval",
    "live_execution",
    "live execution",
    "future_performance",
    "future performance",
)

BLOCKED_UNSAFE_CLAIM_BOUNDARY_PREFIXES = (
    "blocked",
    "blocked_by",
    "forbidden",
    "no",
    "non",
    "not",
    "unsupported",
    "without",
)


class ArtifactContractViolation(ValueError):
    """Raised when an artifact contract boundary is violated."""


class ArtifactContractV1(BaseModel):
    """Frozen Core artifact contract described in docs/core/ARTIFACT_CONTRACT.md."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    artifact_contract_version: Literal["entropy-core-artifact/v1"] = ARTIFACT_CONTRACT_VERSION
    product: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    input_refs: tuple[str, ...] = Field(min_length=1)
    input_hashes: tuple[str, ...] = ()
    policy_config_hash: str = Field(min_length=1)
    code_version_ref: str = Field(min_length=1)
    generated_artifact_refs: tuple[str, ...] = Field(min_length=1)
    limitations: tuple[str, ...] = Field(min_length=1)
    no_claim_boundary: tuple[str, ...] = Field(min_length=1)
    manual_validation_status: Literal[
        "not_reviewed",
        "review_in_progress",
        "validated_internal_only",
        "validated_for_controlled_external_pilot",
        "blocked_by_errors",
        "rejected",
    ]
    error_register_ref: str = Field(min_length=1)
    external_delivery_approval_status: Literal[
        "not_requested",
        "blocked",
        "approved_for_internal_demo",
        "approved_for_controlled_external_pilot",
    ]

    @model_validator(mode="after")
    def reject_unsafe_claim_labels(self) -> "ArtifactContractV1":
        """Allow unsafe surfaces only when they are explicitly blocked."""
        unsafe_boundaries = tuple(
            boundary
            for boundary in self.no_claim_boundary
            if _contains_unsafe_claim(boundary) and not _is_blocked_boundary(boundary)
        )
        if unsafe_boundaries:
            raise ArtifactContractViolation(
                "Unsafe claim labels must be represented as blocked no-claim boundaries."
            )
        return self


def contains_unsafe_claim_label(value: str) -> bool:
    """Return whether a boundary label references an unsafe claim surface."""
    return _contains_unsafe_claim(value)


def is_blocked_no_claim_boundary(value: str) -> bool:
    """Return whether a label represents a blocked no-claim boundary."""
    return _is_blocked_boundary(value)


def _contains_unsafe_claim(value: str) -> bool:
    normalized = _normalize_claim_label(value)
    return any(_normalize_claim_label(label) in normalized for label in UNSAFE_CLAIM_LABELS)


def _is_blocked_boundary(value: str) -> bool:
    tokens = tuple(token for token in _normalize_claim_label(value).split("_") if token)
    return bool(tokens) and tokens[0] in BLOCKED_UNSAFE_CLAIM_BOUNDARY_PREFIXES


def _normalize_claim_label(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(normalized.split())


__all__ = [
    "ARTIFACT_CONTRACT_VERSION",
    "BLOCKED_UNSAFE_CLAIM_BOUNDARY_PREFIXES",
    "EXTERNAL_DELIVERY_APPROVAL_STATUSES",
    "MANUAL_VALIDATION_STATUSES",
    "UNSAFE_CLAIM_LABELS",
    "ArtifactContractV1",
    "ArtifactContractViolation",
    "contains_unsafe_claim_label",
    "is_blocked_no_claim_boundary",
]
