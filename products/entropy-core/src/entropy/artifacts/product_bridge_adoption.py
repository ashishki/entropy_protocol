"""Core-side product bridge adoption readiness checks."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from entropy.artifacts.contract import ARTIFACT_CONTRACT_VERSION
from entropy.artifacts.profiles import get_product_bridge_profile


PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES = (
    "product_workspace_edits",
    "product_runtime_ownership",
    "product_report_authorship",
    "external_delivery_approval",
    "public_sdk",
    "hosted_service",
    "live_execution",
    "holdout_access",
    "production_credentials",
    "capital",
    "external_compliance",
)
REQUIRED_FORBIDDEN_PRODUCT_CALLS = (
    "product_runtime_ownership",
    "product_report_authorship",
    "product_workspace_edit",
    "external_delivery_approval",
)


class ProductBridgeAdoptionMetadata(BaseModel):
    """Core-owned adoption metadata for one product bridge profile."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    profile_id: str = Field(min_length=1)
    artifact_contract_version: str = ARTIFACT_CONTRACT_VERSION
    synthetic_fixture_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    allowed_core_primitives: tuple[str, ...] = Field(min_length=1)
    forbidden_product_calls: tuple[str, ...] = Field(min_length=1)
    no_claim_boundaries: tuple[str, ...] = Field(min_length=1)
    blocked_surfaces: tuple[str, ...] = PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES
    owner: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)


class ProductBridgeAdoptionReadiness(BaseModel):
    """Safe readiness result for Core-side product bridge adoption."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    profile_id: str
    status: Literal["ready", "blocked", "needs_manual_review"]
    reason_codes: tuple[str, ...]
    approval_state: Literal["not_approved"] = "not_approved"
    core_owns_product_runtime: Literal[False] = False
    core_owns_product_report: Literal[False] = False
    external_delivery_approved: Literal[False] = False
    blocked_surfaces: tuple[str, ...] = PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES


def validate_product_bridge_adoption_readiness(
    metadata: ProductBridgeAdoptionMetadata,
) -> ProductBridgeAdoptionReadiness:
    """Validate Core-side product bridge adoption readiness metadata."""

    reason_codes: list[str] = []
    try:
        profile = get_product_bridge_profile(metadata.profile_id)
    except ValueError:
        return _blocked(metadata.profile_id, "unknown_profile")

    if metadata.artifact_contract_version != ARTIFACT_CONTRACT_VERSION:
        reason_codes.append("unsupported_artifact_contract_version")
    if not metadata.synthetic_fixture_refs:
        reason_codes.append("missing_synthetic_fixture_refs")
    if not metadata.evidence_refs:
        reason_codes.append("missing_evidence_refs")

    forbidden_calls = {_normalize(value) for value in metadata.forbidden_product_calls}
    for required in REQUIRED_FORBIDDEN_PRODUCT_CALLS:
        if required not in forbidden_calls:
            reason_codes.append("missing_forbidden_product_call_" + required)

    boundaries = {_normalize(value) for value in metadata.no_claim_boundaries}
    for required_boundary in profile.required_no_claim_boundaries:
        if _normalize(required_boundary) not in boundaries:
            reason_codes.append("missing_no_claim_boundary_" + _normalize(required_boundary))
    for forbidden_label in profile.forbidden_no_claim_labels:
        if _normalize(forbidden_label) in boundaries:
            reason_codes.append("unsupported_claim_surface_" + _normalize(forbidden_label))

    blocked = {_normalize(value) for value in metadata.blocked_surfaces}
    for required_surface in PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES:
        if required_surface not in blocked:
            reason_codes.append("missing_blocked_surface_" + required_surface)

    if reason_codes:
        return ProductBridgeAdoptionReadiness(
            profile_id=metadata.profile_id,
            status="blocked",
            reason_codes=tuple(reason_codes),
            blocked_surfaces=metadata.blocked_surfaces,
        )
    return ProductBridgeAdoptionReadiness(
        profile_id=metadata.profile_id,
        status="ready",
        reason_codes=("core_local_readiness_metadata_valid",),
        blocked_surfaces=metadata.blocked_surfaces,
    )


def _blocked(profile_id: str, reason_code: str) -> ProductBridgeAdoptionReadiness:
    return ProductBridgeAdoptionReadiness(
        profile_id=profile_id,
        status="blocked",
        reason_codes=(reason_code,),
    )


def _normalize(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(normalized.split("_"))
