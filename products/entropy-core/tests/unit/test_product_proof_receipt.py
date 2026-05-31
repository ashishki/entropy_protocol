from __future__ import annotations

from datetime import UTC, datetime

import pytest

from entropy.artifacts import (
    PRODUCT_PROOF_RECEIPT_SCHEMA_VERSION,
    ProductProofReceiptViolation,
    validate_product_proof_receipt,
)


def test_product_proof_receipt_contract_accepts_portable_receipt() -> None:
    receipt = validate_product_proof_receipt(
        {
            "schema_version": PRODUCT_PROOF_RECEIPT_SCHEMA_VERSION,
            "product_id": "workflow-to-agent-studio",
            "receipt_type": "blueprint_proof_receipt",
            "artifact_ref": "exports/blueprints/example.md",
            "artifact_sha256": "a" * 64,
            "generated_at": datetime(2026, 5, 31, tzinfo=UTC),
            "evidence_refs": [
                {
                    "ref_id": "src-1:chk-1",
                    "ref_type": "source_chunk",
                    "supports": "workflow_summary",
                    "checksum_sha256": "b" * 64,
                }
            ],
            "verifier_status": "passed",
            "entropy_core_level": "schema_compatible",
        }
    )

    assert receipt.product_id == "workflow-to-agent-studio"
    assert receipt.verifier_status == "passed"
    assert len(receipt.receipt_sha256()) == 64


def test_product_proof_receipt_contract_rejects_missing_evidence() -> None:
    with pytest.raises(ProductProofReceiptViolation):
        validate_product_proof_receipt(
            {
                "schema_version": PRODUCT_PROOF_RECEIPT_SCHEMA_VERSION,
                "product_id": "demand-to-mvp-radar",
                "receipt_type": "weekly_report_receipt",
                "artifact_ref": "reports/weekly.md",
                "artifact_sha256": "a" * 64,
                "generated_at": datetime(2026, 5, 31, tzinfo=UTC),
                "evidence_refs": [],
                "verifier_status": "failed",
                "verifier_notes": ("no evidence",),
                "entropy_core_level": "evidence_lookup_compatible",
            }
        )


def test_product_proof_receipt_contract_requires_notes_for_non_passed_status() -> None:
    with pytest.raises(ProductProofReceiptViolation, match="verifier_notes"):
        validate_product_proof_receipt(
            {
                "schema_version": PRODUCT_PROOF_RECEIPT_SCHEMA_VERSION,
                "product_id": "signal-analytics-sandbox",
                "receipt_type": "signal_auto_validation_receipt",
                "artifact_ref": "docs/pilot/audit.json",
                "artifact_sha256": "a" * 64,
                "generated_at": datetime(2026, 5, 31, tzinfo=UTC),
                "evidence_refs": [
                    {
                        "ref_id": "claim-1",
                        "ref_type": "text_span",
                        "supports": "asset",
                    }
                ],
                "verifier_status": "needs_review",
                "entropy_core_level": "evidence_lookup_compatible",
            }
        )
