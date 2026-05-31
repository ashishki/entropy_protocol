from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from signal_sandbox.auto_validation.audit_export import (
    export_validation_audit_with_receipt,
    load_signal_auto_validation_receipt,
)
from signal_sandbox.auto_validation.core_receipt import (
    build_signal_auto_validation_receipt,
)
from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    ExtractedSetupFields,
    MarketWindowRef,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.results import (
    ValidationAuditLog,
    ValidationResult,
    ValidationStatus,
)

SHA = "a" * 64
MARKET_SHA = "b" * 64
INPUT_SHA = "c" * 64
CREATED = datetime(2026, 5, 31, 9, tzinfo=UTC)


def test_core_receipt_links_bundle_audit_validators_and_evidence_refs() -> None:
    bundle = _bundle()
    audit = _audit(bundle)

    receipt = build_signal_auto_validation_receipt(
        bundle=bundle,
        audit=audit,
        generated_at_utc=CREATED,
    )

    assert receipt.type == "signal_auto_validation_receipt"
    assert receipt.schema_version == "entropy_core.product_receipt.v1"
    assert receipt.product_id == "signal-analytics-sandbox"
    assert receipt.candidate_id == "candidate-1"
    assert receipt.evidence_bundle_sha256 == bundle.bundle_sha256()
    assert receipt.audit_sha256 == audit.audit_sha256()
    assert receipt.validator_ids == ["pre_outcome_timing"]
    assert receipt.verifier_status == "passed"
    assert {ref.ref_id for ref in receipt.evidence_refs} >= {"asset-ref", "market-1"}
    assert len(receipt.receipt_sha256()) == 64


def test_core_receipt_rejects_audit_bundle_hash_mismatch() -> None:
    bundle = _bundle()
    audit = _audit(bundle, evidence_bundle_sha256="d" * 64)

    with pytest.raises(ValueError, match="evidence_bundle_sha256"):
        build_signal_auto_validation_receipt(bundle=bundle, audit=audit)


def test_core_receipt_rejects_audit_refs_missing_from_bundle() -> None:
    bundle = _bundle()
    audit = _audit(bundle, evidence_ref_ids=["missing-ref"])

    with pytest.raises(ValueError, match="missing from bundle"):
        build_signal_auto_validation_receipt(bundle=bundle, audit=audit)


def test_export_writes_receipt_next_to_validation_audit_log(tmp_path: Path) -> None:
    bundle = _bundle()
    audit = _audit(bundle)

    export = export_validation_audit_with_receipt(
        bundle=bundle,
        audit=audit,
        output_dir=tmp_path,
        generated_at_utc=CREATED,
    )
    receipt = load_signal_auto_validation_receipt(export.receipt_path)
    audit_payload = json.loads(export.audit_log_path.read_text(encoding="utf-8"))

    assert export.audit_log_path == tmp_path / "audit-1.audit.json"
    assert export.receipt_path == tmp_path / "audit-1.receipt.json"
    assert audit_payload["audit_id"] == "audit-1"
    assert audit_payload["evidence_bundle_sha256"] == bundle.bundle_sha256()
    assert receipt.audit_sha256 == audit.audit_sha256()
    assert receipt.receipt_sha256() == export.receipt_sha256
    assert export.audit_sha256 == audit.audit_sha256()


def test_export_rejects_pathlike_artifact_stem(tmp_path: Path) -> None:
    bundle = _bundle()
    audit = _audit(bundle)

    with pytest.raises(ValueError, match="single file-name component"):
        export_validation_audit_with_receipt(
            bundle=bundle,
            audit=audit,
            output_dir=tmp_path,
            stem="../audit-1",
        )


def _bundle() -> AutoValidationEvidenceBundle:
    return AutoValidationEvidenceBundle(
        candidate_id="candidate-1",
        source_id="bablos79",
        source_url="https://t.me/s/example/1",
        source_timestamp_utc=CREATED,
        source_document_id="doc-1",
        capture_id="capture-1",
        source_class=SourceClass.PUBLIC,
        text_ref_id="text-1",
        text_sha256=SHA,
        evidence_refs=[
            EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
            EvidenceRef(
                ref_id="direction-ref", ref_type="text_span", supports="direction"
            ),
        ],
        extracted_fields=ExtractedSetupFields(
            asset="BTC",
            direction=TradeDirection.LONG,
            evidence_ref_ids_by_field={
                "asset": ["asset-ref"],
                "direction": ["direction-ref"],
            },
        ),
        market_window_refs=[
            MarketWindowRef(
                ref_id="market-1",
                provider="binance",
                symbol="BTCUSDT",
                window_start_utc=datetime(2026, 5, 31, 9, tzinfo=UTC),
                window_end_utc=datetime(2026, 5, 31, 10, tzinfo=UTC),
                data_sha256=MARKET_SHA,
            )
        ],
    )


def _audit(
    bundle: AutoValidationEvidenceBundle,
    *,
    evidence_bundle_sha256: str | None = None,
    evidence_ref_ids: list[str] | None = None,
) -> ValidationAuditLog:
    return ValidationAuditLog(
        audit_id="audit-1",
        candidate_id=bundle.candidate_id,
        evidence_bundle_sha256=evidence_bundle_sha256 or bundle.bundle_sha256(),
        results=[
            ValidationResult(
                validator_id="pre_outcome_timing",
                validator_version="timing.v1",
                candidate_id=bundle.candidate_id,
                status=ValidationStatus.PASSED,
                confidence=Decimal("0.92"),
                evidence_ref_ids=evidence_ref_ids or ["asset-ref", "market-1"],
                deterministic_input_sha256=INPUT_SHA,
                rationale="source timestamp precedes market window",
                created_at_utc=CREATED,
            )
        ],
        created_at_utc=CREATED,
    )
