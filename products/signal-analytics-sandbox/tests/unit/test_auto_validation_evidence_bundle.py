from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    MarketWindowRef,
    ModelExtractionSpan,
    SourceClass,
    TradeDirection,
)

SHA = "a" * 64
MARKET_SHA = "b" * 64


def test_evidence_bundle_requires_source_refs_fields_and_provenance() -> None:
    bundle = _bundle()

    assert bundle.source_url == "https://t.me/s/example/1"
    assert bundle.source_timestamp_utc == datetime(2026, 5, 1, 10, tzinfo=UTC)
    assert bundle.media_ref_id == "media-1"
    assert bundle.media_sha256 == SHA
    assert bundle.text_ref_id == "text-1"
    assert bundle.text_sha256 == SHA
    assert bundle.extracted_fields.asset == "MAGN"
    assert bundle.extracted_fields.direction == TradeDirection.LONG
    assert bundle.extracted_fields.targets == [Decimal("52.40")]
    assert bundle.provenance_version == "auto_validation_evidence.v1"


def test_evidence_bundle_rejects_missing_source_timestamp() -> None:
    payload = _bundle_payload()
    del payload["source_timestamp_utc"]

    with pytest.raises(ValidationError):
        AutoValidationEvidenceBundle.model_validate(payload)


def test_evidence_bundle_rejects_missing_text_or_media_checksum() -> None:
    payload = _bundle_payload()
    payload["text_sha256"] = None
    payload["media_sha256"] = None

    with pytest.raises(ValidationError, match="text or media ref with sha256"):
        AutoValidationEvidenceBundle.model_validate(payload)


def test_evidence_bundle_rejects_missing_extraction_evidence_ref() -> None:
    payload = _bundle_payload()
    payload["extracted_fields"]["evidence_ref_ids_by_field"]["entry"] = ["missing-ref"]

    with pytest.raises(ValidationError, match="evidence refs missing"):
        AutoValidationEvidenceBundle.model_validate(payload)


def test_evidence_bundle_rejects_unsupported_source_class() -> None:
    payload = _bundle_payload()
    payload["source_class"] = "private"

    with pytest.raises(ValidationError):
        AutoValidationEvidenceBundle.model_validate(payload)


def test_evidence_bundle_rejects_private_source_url() -> None:
    payload = _bundle_payload()
    payload["source_url"] = "https://t.me/+privateInvite"

    with pytest.raises(ValidationError, match="private or restricted"):
        AutoValidationEvidenceBundle.model_validate(payload)


def test_evidence_bundle_canonical_json_and_hash_are_deterministic() -> None:
    first = _bundle()
    second = AutoValidationEvidenceBundle.model_validate_json(first.canonical_json())

    assert first.canonical_json() == second.canonical_json()
    assert first.bundle_sha256() == second.bundle_sha256()
    assert first.canonical_json() == first.canonical_json()


def _bundle() -> AutoValidationEvidenceBundle:
    return AutoValidationEvidenceBundle.model_validate(_bundle_payload())


def _bundle_payload() -> dict[str, Any]:
    refs = [
        EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
        EvidenceRef(ref_id="direction-ref", ref_type="text_span", supports="direction"),
        EvidenceRef(ref_id="entry-ref", ref_type="chart_region", supports="entry"),
        EvidenceRef(ref_id="stop-ref", ref_type="chart_region", supports="stop"),
        EvidenceRef(ref_id="target-ref", ref_type="chart_region", supports="targets"),
    ]
    return {
        "candidate_id": "candidate-1",
        "source_id": "bablos79",
        "source_url": "https://t.me/s/example/1",
        "source_timestamp_utc": "2026-05-01T10:00:00+00:00",
        "source_document_id": "doc-1",
        "capture_id": "capture-1",
        "source_class": SourceClass.PUBLIC,
        "text_ref_id": "text-1",
        "text_sha256": SHA,
        "media_ref_id": "media-1",
        "media_sha256": SHA,
        "ocr_ref_ids": ["ocr-1"],
        "transcript_ref_ids": [],
        "chart_region_ref_ids": ["region-1"],
        "evidence_refs": refs,
        "extracted_fields": {
            "asset": "MAGN",
            "direction": TradeDirection.LONG,
            "entry": Decimal("50.10"),
            "stop": Decimal("48.90"),
            "targets": [Decimal("52.40")],
            "horizon": "intraday",
            "evidence_ref_ids_by_field": {
                "asset": ["asset-ref"],
                "direction": ["direction-ref"],
                "entry": ["entry-ref"],
                "stop": ["stop-ref"],
                "targets": ["target-ref"],
                "horizon": ["direction-ref"],
            },
        },
        "model_extraction_spans": [
            ModelExtractionSpan(
                span_id="span-1",
                model_id="review-model",
                field="asset",
                excerpt="MAGN",
                evidence_ref_ids=["asset-ref"],
                confidence=Decimal("0.87"),
            )
        ],
        "market_window_refs": [
            MarketWindowRef(
                ref_id="market-1",
                provider="moex",
                symbol="MAGN",
                window_start_utc=datetime(2026, 5, 1, 10, tzinfo=UTC),
                window_end_utc=datetime(2026, 5, 1, 14, tzinfo=UTC),
                data_sha256=MARKET_SHA,
            )
        ],
        "provenance_version": "auto_validation_evidence.v1",
    }
