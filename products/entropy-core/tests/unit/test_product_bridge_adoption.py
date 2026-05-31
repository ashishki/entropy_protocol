"""Unit tests for Core-side product bridge adoption readiness."""

from __future__ import annotations

import json
from pathlib import Path

from entropy.artifacts import (
    ARTIFACT_CONTRACT_VERSION,
    PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES,
    ProductBridgeAdoptionMetadata,
    validate_product_bridge_adoption_readiness,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts" / "adoption"


def trader_adoption_metadata(**overrides: object) -> ProductBridgeAdoptionMetadata:
    payload: dict[str, object] = {
        "profile_id": "trader-risk-audit",
        "artifact_contract_version": ARTIFACT_CONTRACT_VERSION,
        "synthetic_fixture_refs": ("tests/fixtures/artifacts/profiles/trader_valid.json",),
        "evidence_refs": ("T91-T94 Product Bridge Profiles",),
        "allowed_core_primitives": ("artifact_validation", "profile_overlay"),
        "forbidden_product_calls": (
            "product_runtime_ownership",
            "product_report_authorship",
            "product_workspace_edit",
            "external_delivery_approval",
        ),
        "no_claim_boundaries": (
            "not_order_blocking",
            "not_live_trading",
            "not_broker_exchange_execution",
            "not_production",
            "not_capital_ready",
            "not_investment_advice",
            "not_core_phase_gate_approval",
        ),
        "blocked_surfaces": PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES,
        "owner": "entropy-core",
        "reviewer": "internal-review",
    }
    payload.update(overrides)
    return ProductBridgeAdoptionMetadata.model_validate(payload)


def test_readiness_helper_validates_required_metadata() -> None:
    result = validate_product_bridge_adoption_readiness(trader_adoption_metadata())

    assert result.status == "ready"
    assert result.profile_id == "trader-risk-audit"
    assert result.reason_codes == ("core_local_readiness_metadata_valid",)
    assert result.approval_state == "not_approved"


def test_readiness_helper_rejects_missing_refs_and_unsafe_claims() -> None:
    missing_fixture = validate_product_bridge_adoption_readiness(
        trader_adoption_metadata(synthetic_fixture_refs=())
    )
    missing_evidence = validate_product_bridge_adoption_readiness(
        trader_adoption_metadata(evidence_refs=())
    )
    unsafe_claim = validate_product_bridge_adoption_readiness(
        trader_adoption_metadata(
            no_claim_boundaries=(
                "not_order_blocking",
                "not_live_trading",
                "not_broker_exchange_execution",
                "not_production",
                "not_capital_ready",
                "not_investment_advice",
                "not_core_phase_gate_approval",
                "live_trading",
            )
        )
    )

    assert missing_fixture.status == "blocked"
    assert "missing_synthetic_fixture_refs" in missing_fixture.reason_codes
    assert missing_evidence.status == "blocked"
    assert "missing_evidence_refs" in missing_evidence.reason_codes
    assert unsafe_claim.status == "blocked"
    assert "unsupported_claim_surface_live_trading" in unsafe_claim.reason_codes


def test_readiness_result_is_core_local_and_non_approving() -> None:
    result = validate_product_bridge_adoption_readiness(trader_adoption_metadata())
    serialized = result.model_dump_json()

    assert result.core_owns_product_runtime is False
    assert result.core_owns_product_report is False
    assert result.external_delivery_approved is False
    assert result.approval_state == "not_approved"
    assert result.blocked_surfaces == PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES
    assert "public_sdk" in result.blocked_surfaces
    assert "hosted_service" in result.blocked_surfaces
    assert "external_compliance" in result.blocked_surfaces
    assert "customer" not in serialized


def test_synthetic_adoption_fixtures_are_valid() -> None:
    valid_paths = (
        FIXTURES / "trader_valid.json",
        FIXTURES / "signal_valid.json",
    )

    for path in valid_paths:
        result = validate_product_bridge_adoption_readiness(load_fixture(path))

        assert result.status == "ready", path
        assert result.reason_codes == ("core_local_readiness_metadata_valid",)
        assert result.approval_state == "not_approved"


def test_unsafe_adoption_fixtures_are_rejected() -> None:
    expected_reason_by_fixture = {
        "unsafe_product_runtime_ownership.json": "missing_forbidden_product_call_product_runtime_ownership",
        "unsafe_product_report_authorship.json": "missing_forbidden_product_call_product_report_authorship",
        "unsafe_hosted_service.json": "missing_blocked_surface_hosted_service",
        "unsafe_external_delivery_approval.json": (
            "missing_forbidden_product_call_external_delivery_approval"
        ),
    }

    for fixture_name, expected_reason in expected_reason_by_fixture.items():
        result = validate_product_bridge_adoption_readiness(load_fixture(FIXTURES / fixture_name))

        assert result.status == "blocked", fixture_name
        assert expected_reason in result.reason_codes
        assert result.approval_state == "not_approved"


def test_adoption_fixtures_are_synthetic() -> None:
    forbidden_ref_terms = (
        "api_key",
        "authorization",
        "customer",
        "password",
        "private",
        "secret",
        "ssn",
        "token",
    )

    fixture_paths = tuple(sorted(FIXTURES.glob("*.json")))
    assert fixture_paths
    for path in fixture_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        refs = tuple(payload["synthetic_fixture_refs"]) + tuple(payload["evidence_refs"])
        assert refs
        for ref in refs:
            lowered_ref = ref.lower()
            assert (
                "synthetic" in lowered_ref
                or lowered_ref.startswith("docs/")
                or lowered_ref.startswith("tests/fixtures/artifacts/")
            )
            for term in forbidden_ref_terms:
                assert term not in lowered_ref, f"{path} contains forbidden ref marker {term!r}"


def load_fixture(path: Path) -> ProductBridgeAdoptionMetadata:
    return ProductBridgeAdoptionMetadata.model_validate_json(path.read_text(encoding="utf-8"))
