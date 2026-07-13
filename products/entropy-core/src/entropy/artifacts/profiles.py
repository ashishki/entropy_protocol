"""Product bridge profile overlays for artifact no-claim boundaries."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from entropy.artifacts.contract import ArtifactContractV1

ProductBridgeProfileId = Literal["generic", "trader-risk-audit", "signal-analytics-sandbox"]

KNOWN_PRODUCT_BRIDGE_PROFILE_IDS: tuple[ProductBridgeProfileId, ...] = (
    "generic",
    "trader-risk-audit",
    "signal-analytics-sandbox",
)


class ProductBridgeProfileViolation(ValueError):
    """Raised when a product bridge profile cannot validate an artifact."""


class ProductBridgeProfile(BaseModel):
    """Core-owned overlay for product-shaped artifact boundary validation."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    profile_id: ProductBridgeProfileId
    description: str = Field(min_length=1)
    required_no_claim_boundaries: tuple[str, ...] = ()
    forbidden_no_claim_labels: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_profile_shape(self) -> "ProductBridgeProfile":
        overlap = set(self.required_no_claim_boundaries).intersection(
            self.forbidden_no_claim_labels
        )
        if overlap:
            raise ProductBridgeProfileViolation(
                "Profile boundaries cannot be both required and forbidden."
            )
        return self


PRODUCT_BRIDGE_PROFILES: dict[str, ProductBridgeProfile] = {
    "generic": ProductBridgeProfile(
        profile_id="generic",
        description="Base entropy-core-artifact/v1 validation without product-specific overlay.",
    ),
    "trader-risk-audit": ProductBridgeProfile(
        profile_id="trader-risk-audit",
        description="Trader audit report boundary overlay without Trader runtime ownership.",
        required_no_claim_boundaries=(
            "not_order_blocking",
            "not_live_trading",
            "not_broker_exchange_execution",
            "not_production",
            "not_capital_ready",
            "not_investment_advice",
            "not_core_phase_gate_approval",
        ),
        forbidden_no_claim_labels=(
            "order_blocking",
            "live_trading",
            "broker_exchange_execution",
            "production",
            "capital_ready",
            "investment_advice",
            "core_phase_gate_approval",
        ),
    ),
    "signal-analytics-sandbox": ProductBridgeProfile(
        profile_id="signal-analytics-sandbox",
        description="Signal analytics report boundary overlay without Signal runtime ownership.",
        required_no_claim_boundaries=(
            "not_trading_advice",
            "not_investment_recommendation",
            "not_future_performance_prediction",
            "not_automated_signal_execution",
            "not_production",
            "not_capital_ready",
            "not_core_phase_gate_approval",
        ),
        forbidden_no_claim_labels=(
            "trading_advice",
            "investment_recommendation",
            "future_performance_prediction",
            "automated_signal_execution",
            "production",
            "capital_ready",
            "core_phase_gate_approval",
        ),
    ),
}


def get_product_bridge_profile(profile_id: str) -> ProductBridgeProfile:
    """Return a known product bridge profile by stable id."""
    try:
        return PRODUCT_BRIDGE_PROFILES[profile_id]
    except KeyError as exc:
        raise ProductBridgeProfileViolation("Unknown artifact profile: " + profile_id) from exc


def validate_artifact_profile(
    artifact: ArtifactContractV1,
    profile_id: str,
) -> ArtifactContractV1:
    """Validate an artifact against a profile overlay and return the unchanged artifact."""
    profile = get_product_bridge_profile(profile_id)
    boundaries = {_normalize_boundary(boundary) for boundary in artifact.no_claim_boundary}
    missing = tuple(
        boundary
        for boundary in profile.required_no_claim_boundaries
        if _normalize_boundary(boundary) not in boundaries
    )
    if missing:
        raise ProductBridgeProfileViolation(
            "Artifact profile is missing required no-claim boundaries: " + ", ".join(missing)
        )

    forbidden = tuple(
        label
        for label in profile.forbidden_no_claim_labels
        if _normalize_boundary(label) in boundaries
    )
    if forbidden:
        raise ProductBridgeProfileViolation(
            "Artifact profile contains forbidden no-claim labels: " + ", ".join(forbidden)
        )
    return artifact


def _normalize_boundary(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(normalized.split("_"))


__all__ = [
    "KNOWN_PRODUCT_BRIDGE_PROFILE_IDS",
    "PRODUCT_BRIDGE_PROFILES",
    "ProductBridgeProfile",
    "ProductBridgeProfileId",
    "ProductBridgeProfileViolation",
    "get_product_bridge_profile",
    "validate_artifact_profile",
]
