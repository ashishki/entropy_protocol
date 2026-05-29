from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from signal_sandbox.claims import (
    MediaClaimStatus,
    StructuredClaimType,
    extract_reviewed_multimodal_claims,
)
from signal_sandbox.corpus import SourceDocument

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_three_channel_media_inventory_records_review_status() -> None:
    inventory = (
        PROJECT_ROOT / "docs/pilot/three_channel_V1_MEDIA_INVENTORY.md"
    ).read_text(encoding="utf-8")

    for channel in ("bablos79", "nemphiscrypts", "pifagortrade"):
        assert f"`{channel}`" in inventory
    assert "llm_reviewed_internal" in inventory
    assert "no reviewed OCR refs" in inventory
    assert "excluded from customer-facing metrics" in inventory


def test_reviewed_transcript_refs_produce_structured_claim_drafts() -> None:
    document = _document(
        "voice transcript: #BTC long entry 100 stop 90 target 120",
        transcript_refs=["transcript-1"],
    )

    drafts = extract_reviewed_multimodal_claims(
        document,
        accepted_media_refs={"transcript-1"},
    )

    assert len(drafts) == 1
    assert drafts[0].status == MediaClaimStatus.EXTRACTED
    assert drafts[0].media_refs == ["transcript-1"]
    assert drafts[0].source_document_id == document.document_id
    assert drafts[0].claim is not None
    assert drafts[0].claim.claim_type == StructuredClaimType.TRADE_SETUP
    assert drafts[0].customer_metric_eligible is True


def test_unreviewed_transcript_and_ocr_refs_remain_excluded() -> None:
    document = _document(
        "#ETH bullish from OCR chart",
        transcript_refs=["transcript-draft"],
        ocr_refs=["ocr-draft"],
    )

    drafts = extract_reviewed_multimodal_claims(document, accepted_media_refs=set())

    assert len(drafts) == 1
    assert drafts[0].status == MediaClaimStatus.EXCLUDED_UNREVIEWED
    assert drafts[0].claim is None
    assert drafts[0].customer_metric_eligible is False
    assert drafts[0].exclusion_reason == "media_ref_not_human_operator_reviewed"


def _document(
    text: str,
    *,
    transcript_refs: list[str] | None = None,
    ocr_refs: list[str] | None = None,
) -> SourceDocument:
    return SourceDocument(
        document_id="doc-media-1",
        capture_id="capture-media-1",
        source_id="test_channel",
        author="test_channel",
        timestamp_utc=datetime(2026, 5, 19, tzinfo=UTC),
        text=text,
        evidence_url="https://t.me/test/media-1",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
        transcript_refs=transcript_refs or [],
        ocr_refs=ocr_refs or [],
    )
