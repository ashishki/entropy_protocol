from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pytest

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.media import MediaArtifact, MediaModality, RetentionState
from signal_sandbox.media.ocr import DraftOCRArtifact, DraftOCRStatus
from signal_sandbox.media.source_join import (
    MediaJoinMismatchError,
    join_multimodal_source_document,
)
from signal_sandbox.media.transcription import (
    DraftTranscriptArtifact,
    DraftTranscriptStatus,
)


def test_join_preserves_original_source_document() -> None:
    document = _document()
    media = _media("media-1", document)
    transcript = _transcript(media)
    ocr = _ocr(media)

    enriched = join_multimodal_source_document(
        document,
        media_artifacts=[media],
        transcript_artifacts=[transcript],
        ocr_artifacts=[ocr],
    )

    assert enriched is not document
    assert enriched.text == document.text
    assert enriched.evidence_url == document.evidence_url
    assert enriched.text_sha256 == document.text_sha256
    assert enriched.media_refs == [media.local_path]
    assert enriched.transcript_refs == [transcript.artifact_path]
    assert enriched.ocr_refs == [ocr.artifact_path]


def test_join_rejects_mismatched_media_refs() -> None:
    document = _document()
    media = _media("media-1", document)
    mismatched_checksum = _transcript(media).model_copy(
        update={"source_media_sha256": "b" * 64}
    )
    mismatched_capture = media.model_copy(update={"capture_id": "other-capture"})

    with pytest.raises(MediaJoinMismatchError):
        join_multimodal_source_document(
            document,
            media_artifacts=[media],
            transcript_artifacts=[mismatched_checksum],
            ocr_artifacts=[],
        )

    with pytest.raises(MediaJoinMismatchError):
        join_multimodal_source_document(
            document,
            media_artifacts=[mismatched_capture],
            transcript_artifacts=[],
            ocr_artifacts=[],
        )


def test_join_has_no_truth_artifact_side_effects(tmp_path: Path) -> None:
    document = _document()
    media = _media("media-1", document)
    transcript = _transcript(media)

    enriched = join_multimodal_source_document(
        document,
        media_artifacts=[media],
        transcript_artifacts=[transcript],
        ocr_artifacts=[],
    )

    assert enriched.transcript_refs == [transcript.artifact_path]
    assert not (tmp_path / "market_ideas").exists()
    assert not (tmp_path / "outcomes").exists()
    assert not (tmp_path / "reports").exists()
    assert not (tmp_path / "ledgers").exists()


def test_join_preserves_existing_refs_and_dedupes_additive_refs() -> None:
    document = _document().model_copy(
        update={
            "media_refs": ["workspace/media/existing.png"],
            "transcript_refs": ["workspace/transcripts/existing.json"],
        }
    )
    media = _media("media-1", document)
    transcript = _transcript(media)

    enriched = join_multimodal_source_document(
        document,
        media_artifacts=[media, media],
        transcript_artifacts=[transcript, transcript],
        ocr_artifacts=[],
    )

    assert enriched.text == document.text
    assert enriched.evidence_url == document.evidence_url
    assert enriched.text_sha256 == document.text_sha256
    assert enriched.media_refs == [
        "workspace/media/existing.png",
        "workspace/media/media-1.png",
    ]
    assert enriched.transcript_refs == [
        "workspace/transcripts/existing.json",
        "workspace/transcripts/transcript-1.json",
    ]


def _document() -> SourceDocument:
    text = "public source text"
    return SourceDocument(
        document_id="bablos79:bablos79-10442",
        capture_id="bablos79-10442",
        source_id="bablos79",
        author="bablos79",
        timestamp_utc=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
        text=text,
        evidence_url="https://t.me/bablos79/10442",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )


def _media(media_id: str, document: SourceDocument) -> MediaArtifact:
    media_bytes = b"media bytes"
    return MediaArtifact(
        media_id=media_id,
        source_id=document.source_id,
        capture_id=document.capture_id,
        source_document_id=document.document_id,
        source_timestamp_utc=document.timestamp_utc,
        modality=MediaModality.SCREENSHOT,
        original_url_or_file_id="fixture_image_ref",
        local_path=f"workspace/media/{media_id}.png",
        media_sha256=hashlib.sha256(media_bytes).hexdigest(),
        mime_type="image/png",
        image_width_px=1280,
        image_height_px=720,
        retention_state=RetentionState.TEMPORARY,
        created_at_utc=datetime(2026, 5, 9, 12, 0, tzinfo=UTC),
    )


def _transcript(media: MediaArtifact) -> DraftTranscriptArtifact:
    return DraftTranscriptArtifact(
        transcript_id="transcript-1",
        media_id=media.media_id,
        provider="fake-whisper",
        model="whisper-test",
        transcript_text="voice draft",
        transcript_sha256=hashlib.sha256(b"voice draft").hexdigest(),
        source_media_sha256=media.media_sha256,
        status=DraftTranscriptStatus.DRAFT_PENDING_REVIEW,
        reviewer_id="pending",
        review_required=True,
        created_at_utc=datetime(2026, 5, 9, 12, 1, tzinfo=UTC),
        raw_media_retention_action="retained_by_policy",
        artifact_path="workspace/transcripts/transcript-1.json",
    )


def _ocr(media: MediaArtifact) -> DraftOCRArtifact:
    return DraftOCRArtifact(
        ocr_id="ocr-1",
        media_id=media.media_id,
        provider="fake-ocr",
        model="ocr-test",
        text="ocr draft",
        text_sha256=hashlib.sha256(b"ocr draft").hexdigest(),
        source_media_sha256=media.media_sha256,
        bounding_metadata=[],
        status=DraftOCRStatus.DRAFT_PENDING_REVIEW,
        reviewer_id="pending",
        review_required=True,
        created_at_utc=datetime(2026, 5, 9, 12, 2, tzinfo=UTC),
        artifact_path="workspace/ocr/ocr-1.json",
    )
