"""Core-local examples for product receipt evidence lookup and bridge adoption."""

from __future__ import annotations

from pathlib import Path

from entropy.artifacts import (
    EVIDENCE_LOOKUP_BLOCKED_SURFACES,
    PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES,
    ProductBridgeAdoptionMetadata,
    ProductProofReceipt,
    lookup_evidence_index,
    lookup_packet_evidence_refs,
    validate_product_bridge_adoption_readiness,
)


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"
RECEIPT = FIXTURES / "product_receipts" / "signal_auto_validation_valid.json"
EVIDENCE_INDEX = FIXTURES / "product_receipts" / "signal_auto_validation_evidence_index.md"
ADOPTION = FIXTURES / "adoption" / "signal_receipt_valid.json"


def test_product_receipt_fixture_validates_without_product_runtime_logic() -> None:
    receipt = _receipt_fixture()

    assert receipt.product_id == "signal-analytics-sandbox"
    assert receipt.receipt_type == "signal_auto_validation_receipt"
    assert receipt.entropy_core_level == "evidence_lookup_compatible"
    assert receipt.verifier_status == "passed"
    assert {ref.ref_id for ref in receipt.evidence_refs} == {
        "signal-auto-validation:asset-ref",
        "signal-auto-validation:market-1",
    }


def test_product_receipt_evidence_refs_resolve_to_local_metadata_only() -> None:
    receipt = _receipt_fixture()
    evidence_index = EVIDENCE_INDEX.read_text(encoding="utf-8")

    results = lookup_packet_evidence_refs(
        evidence_index,
        tuple(ref.ref_id for ref in receipt.evidence_refs),
    )

    assert {result.status for result in results} == {"found"}
    assert {result.artifact_type for result in results} == {"Product receipt evidence example"}
    assert {result.approval_state for result in results} == {"not_approved"}
    for result in results:
        assert result.blocked_surfaces == EVIDENCE_LOOKUP_BLOCKED_SURFACES
        assert "runtime_rag" in result.blocked_surfaces
        assert "hosted_search" in result.blocked_surfaces
        assert "public_api" in result.blocked_surfaces


def test_missing_product_receipt_evidence_ref_stays_insufficient() -> None:
    result = lookup_evidence_index(
        EVIDENCE_INDEX.read_text(encoding="utf-8"),
        "signal-auto-validation:missing-ref",
    )

    assert result.status == "insufficient_evidence"
    assert result.reason_code == "evidence_topic_not_found"
    assert result.approval_state == "not_approved"
    assert result.blocked_surfaces == EVIDENCE_LOOKUP_BLOCKED_SURFACES


def test_product_receipt_bridge_adoption_fixture_stays_core_side_only() -> None:
    metadata = ProductBridgeAdoptionMetadata.model_validate_json(
        ADOPTION.read_text(encoding="utf-8")
    )
    result = validate_product_bridge_adoption_readiness(metadata)

    assert result.status == "ready"
    assert result.reason_codes == ("core_local_readiness_metadata_valid",)
    assert result.approval_state == "not_approved"
    assert result.core_owns_product_runtime is False
    assert result.core_owns_product_report is False
    assert result.external_delivery_approved is False
    assert result.blocked_surfaces == PRODUCT_BRIDGE_ADOPTION_BLOCKED_SURFACES
    assert "hosted_service" in result.blocked_surfaces
    assert "live_execution" in result.blocked_surfaces
    assert "capital" in result.blocked_surfaces


def _receipt_fixture() -> ProductProofReceipt:
    return ProductProofReceipt.model_validate_json(RECEIPT.read_text(encoding="utf-8"))
