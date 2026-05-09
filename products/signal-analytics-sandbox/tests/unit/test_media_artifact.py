from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from signal_sandbox.media import (
    MediaArtifact,
    MediaModality,
    RetentionState,
    build_media_manifest,
)


def test_media_artifact_schema_requires_provenance() -> None:
    artifact = _artifact("media-1")

    assert artifact.media_id == "media-1"
    assert artifact.source_id == "bablos79"
    assert artifact.capture_id == "bablos79-10442"
    assert artifact.source_document_id == "bablos79:bablos79-10442"
    assert artifact.modality == MediaModality.VOICE
    assert artifact.original_url_or_file_id == "telegram-file-id-1"
    assert artifact.local_path == "workspace/media/bablos79/media-1.ogg"
    assert artifact.media_sha256 == "a" * 64
    assert artifact.mime_type == "audio/ogg"
    assert artifact.duration_seconds == 47
    assert artifact.image_width_px is None
    assert artifact.image_height_px is None
    assert artifact.retention_state == RetentionState.TEMPORARY
    assert artifact.draft_transcript_refs == ["workspace/transcripts/media-1.json"]
    assert artifact.draft_ocr_refs == []


def test_media_manifest_is_deterministically_sorted(tmp_path: Path) -> None:
    later_same_doc = _artifact("media-3", document_id="doc-2", minutes=2)
    earlier = _artifact("media-2", document_id="doc-1", minutes=1)
    earlier_second_media = _artifact("media-1", document_id="doc-1", minutes=1)

    manifest = build_media_manifest([later_same_doc, earlier, earlier_second_media])

    assert [row.media_id for row in manifest.rows] == ["media-1", "media-2", "media-3"]

    markdown_path = tmp_path / "media_manifest.md"
    json_path = tmp_path / "media_manifest.json"
    manifest.write_markdown(markdown_path)
    manifest.write_json(json_path)

    markdown = markdown_path.read_text(encoding="utf-8")
    assert "| media-1 | doc-1 | voice | temporary |" in markdown
    assert (
        "No Telegram, Whisper, OCR, provider, approved-ledger, or report output"
        in markdown
    )
    assert json_path.read_text(encoding="utf-8").startswith('{"rows"')


def test_media_artifact_rejects_unlinked_or_unhashed_media() -> None:
    with pytest.raises(ValidationError):
        _artifact("media-1", capture_id="")

    with pytest.raises(ValidationError):
        _artifact("media-1", media_sha256="")

    with pytest.raises(ValidationError):
        payload: dict[str, object] = _artifact("media-1").model_dump()
        payload["provider_output_path"] = "workspace/transcripts/raw-provider.json"
        MediaArtifact.model_validate(payload)


def _artifact(
    media_id: str,
    *,
    document_id: str = "bablos79:bablos79-10442",
    capture_id: str = "bablos79-10442",
    media_sha256: str = "a" * 64,
    minutes: int = 0,
) -> MediaArtifact:
    return MediaArtifact(
        media_id=media_id,
        source_id="bablos79",
        capture_id=capture_id,
        source_document_id=document_id,
        source_timestamp_utc=(
            datetime(2026, 5, 9, tzinfo=UTC) + timedelta(minutes=minutes)
        ),
        modality=MediaModality.VOICE,
        original_url_or_file_id="telegram-file-id-1",
        local_path=f"workspace/media/bablos79/{media_id}.ogg",
        media_sha256=media_sha256,
        mime_type="audio/ogg",
        duration_seconds=47,
        retention_state=RetentionState.TEMPORARY,
        created_at_utc=datetime(2026, 5, 9, 12, 0, tzinfo=UTC),
        draft_transcript_refs=[f"workspace/transcripts/{media_id}.json"],
    )
