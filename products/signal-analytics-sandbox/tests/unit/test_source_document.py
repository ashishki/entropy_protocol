from __future__ import annotations

from datetime import datetime

from signal_sandbox.capture.loader import CapturedPost
from signal_sandbox.corpus import SourceDocument, from_captured_post


def test_source_document_required_fields() -> None:
    document = SourceDocument(
        document_id="bablos79:10442",
        capture_id="bablos79-10442",
        source_id="bablos79",
        author="bablos79",
        timestamp_utc=dt("2026-05-07T18:51:32+00:00"),
        text="public post text",
        evidence_url="https://t.me/bablos79/10442",
        text_sha256="a" * 64,
        media_refs=["workspace/media/chart.png"],
        transcript_refs=["workspace/transcripts/voice.txt"],
        ocr_refs=["workspace/ocr/chart.txt"],
        metadata={"source_type": "telegram_public"},
    )

    assert document.capture_id == "bablos79-10442"
    assert document.source_id == "bablos79"
    assert document.author == "bablos79"
    assert document.text == "public post text"
    assert document.evidence_url == "https://t.me/bablos79/10442"
    assert document.text_sha256 == "a" * 64
    assert document.media_refs == ["workspace/media/chart.png"]
    assert document.transcript_refs == ["workspace/transcripts/voice.txt"]
    assert document.ocr_refs == ["workspace/ocr/chart.txt"]
    assert document.metadata == {"source_type": "telegram_public"}


def test_captured_post_conversion_preserves_evidence() -> None:
    post = CapturedPost(
        capture_id="bablos79-10442",
        source_id="bablos79",
        evidence_url="https://t.me/bablos79/10442",
        capture_timestamp_utc=dt("2026-05-07T18:51:32+00:00"),
        raw_text="☄️ По #X5 кто то жестко набирает",
        text_sha256="b3efd9207df62a8bc98381986770a9856d6a895fd6eba5d1d845a235ec50bb39",
    )

    document = from_captured_post(post, metadata={"capture_loader": "v1"})

    assert document.document_id == "bablos79:bablos79-10442"
    assert document.capture_id == post.capture_id
    assert document.source_id == post.source_id
    assert document.author == post.source_id
    assert document.timestamp_utc == post.capture_timestamp_utc
    assert document.text == post.raw_text
    assert document.evidence_url == post.evidence_url
    assert document.text_sha256 == post.text_sha256
    assert document.metadata == {"capture_loader": "v1"}


def test_modal_refs_are_optional() -> None:
    document = SourceDocument(
        document_id="bablos79:empty-modal",
        capture_id="bablos79-empty-modal",
        source_id="bablos79",
        author="bablos79",
        timestamp_utc=dt("2026-05-07T18:51:32+00:00"),
        text="text-only public post",
        evidence_url="https://t.me/bablos79/1",
        text_sha256="c" * 64,
    )

    assert document.media_refs == []
    assert document.transcript_refs == []
    assert document.ocr_refs == []


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value)
