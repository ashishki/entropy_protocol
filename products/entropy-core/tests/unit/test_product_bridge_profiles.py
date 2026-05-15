"""Unit tests for Core product bridge artifact profiles."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from entropy.artifacts import (
    ArtifactContractV1,
    KNOWN_PRODUCT_BRIDGE_PROFILE_IDS,
    PRODUCT_BRIDGE_PROFILES,
    ProductBridgeProfileViolation,
    get_product_bridge_profile,
    validate_artifact_profile,
)

VALID_ARTIFACT = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts" / "valid_artifact.json"


def test_known_profiles_exist() -> None:
    assert KNOWN_PRODUCT_BRIDGE_PROFILE_IDS == (
        "generic",
        "trader-risk-audit",
        "signal-analytics-sandbox",
    )
    assert tuple(PRODUCT_BRIDGE_PROFILES) == KNOWN_PRODUCT_BRIDGE_PROFILE_IDS
    assert get_product_bridge_profile("generic").required_no_claim_boundaries == ()
    assert get_product_bridge_profile("trader-risk-audit").forbidden_no_claim_labels
    assert get_product_bridge_profile("signal-analytics-sandbox").forbidden_no_claim_labels


def test_profiles_overlay_claim_boundaries() -> None:
    base_fields = tuple(ArtifactContractV1.model_fields)
    trader_artifact = artifact_with_boundaries(
        "not_order_blocking",
        "not_live_trading",
        "not_broker_exchange_execution",
        "not_core_phase_gate_approval",
    )
    signal_artifact = artifact_with_boundaries(
        "not_trading_advice",
        "not_investment_recommendation",
        "not_future_performance_prediction",
        "not_automated_signal_execution",
        "not_core_phase_gate_approval",
    )

    assert validate_artifact_profile(trader_artifact, "trader-risk-audit") is trader_artifact
    assert (
        validate_artifact_profile(signal_artifact, "signal-analytics-sandbox") is signal_artifact
    )
    assert tuple(ArtifactContractV1.model_fields) == base_fields
    assert "profile" not in ArtifactContractV1.model_fields

    with pytest.raises(ProductBridgeProfileViolation, match="missing required"):
        validate_artifact_profile(base_artifact(), "trader-risk-audit")

    unsafe_signal = artifact_with_boundaries(
        "not_trading_advice",
        "not_investment_recommendation",
        "not_future_performance_prediction",
        "not_automated_signal_execution",
        "not_core_phase_gate_approval",
        "automated_signal_execution",
    )
    with pytest.raises(ProductBridgeProfileViolation, match="forbidden no-claim labels"):
        validate_artifact_profile(unsafe_signal, "signal-analytics-sandbox")


def test_unknown_profile_rejected() -> None:
    with pytest.raises(ProductBridgeProfileViolation) as exc_info:
        get_product_bridge_profile("unknown-profile")

    assert str(exc_info.value) == "Unknown artifact profile: unknown-profile"

    with pytest.raises(ProductBridgeProfileViolation, match="Unknown artifact profile"):
        validate_artifact_profile(base_artifact(), "unknown-profile")


def base_artifact() -> ArtifactContractV1:
    return ArtifactContractV1.model_validate(json.loads(VALID_ARTIFACT.read_text(encoding="utf-8")))


def artifact_with_boundaries(*extra_boundaries: str) -> ArtifactContractV1:
    payload = base_artifact().model_dump(mode="json")
    payload["no_claim_boundary"] = [*payload["no_claim_boundary"], *extra_boundaries]
    return ArtifactContractV1.model_validate(payload)
