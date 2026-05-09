from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pytest

from signal_sandbox.media import MediaArtifact, MediaModality, RetentionState
from signal_sandbox.media.ocr import (
    ChartInterpretationForbidden,
    DraftOCRStatus,
    OCRClientResult,
    UnsupportedOCRMediaError,
    run_ocr_draft,
)


def test_ocr_uses_injected_client(tmp_path: Path) -> None:
    media = _image_artifact(tmp_path)
    client = FakeOCRClient(OCRClientResult(text="BTC target table"))

    artifact = run_ocr_draft(
        media,
        client=client,
        output_dir=tmp_path / "ocr",
    )

    assert client.calls == [(Path(media.local_path), "ocr-draft-v1")]
    assert artifact.media_id == media.media_id
    assert artifact.text == "BTC target table"
    assert artifact.status == DraftOCRStatus.DRAFT_PENDING_REVIEW
    assert artifact.reviewer_id == "pending"
    assert artifact.artifact_path is not None
    assert Path(artifact.artifact_path).exists()

    voice = media.model_copy(update={"modality": MediaModality.VOICE})
    with pytest.raises(UnsupportedOCRMediaError):
        run_ocr_draft(voice, client=client, output_dir=tmp_path / "ocr")


def test_ocr_preserves_media_provenance(tmp_path: Path) -> None:
    media = _image_artifact(tmp_path)
    text = "SBER support 270"
    client = FakeOCRClient(
        OCRClientResult(
            text=text,
            bounding_metadata=[{"text": "SBER", "x": "10", "y": "12"}],
        )
    )

    artifact = run_ocr_draft(
        media,
        client=client,
        output_dir=tmp_path / "ocr",
        provider="fake-ocr",
        model="ocr-test",
    )

    assert artifact.provider == "fake-ocr"
    assert artifact.model == "ocr-test"
    assert artifact.text_sha256 == hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert artifact.source_media_sha256 == media.media_sha256
    assert artifact.bounding_metadata == [{"text": "SBER", "x": "10", "y": "12"}]
    assert artifact.review_required is True


def test_chart_claims_are_review_required(tmp_path: Path) -> None:
    media = _image_artifact(tmp_path)
    client = FakeOCRClient(OCRClientResult(text="chart says breakout"))

    with pytest.raises(ChartInterpretationForbidden):
        run_ocr_draft(
            media,
            client=client,
            output_dir=tmp_path / "ocr",
            approved_chart_claims=["breakout confirmed"],
        )

    artifact = run_ocr_draft(
        media,
        client=client,
        output_dir=tmp_path / "ocr",
        chart_interpretation_notes=["possible chart level 270"],
    )

    assert artifact.status == DraftOCRStatus.DRAFT_PENDING_REVIEW
    assert artifact.reviewer_id == "pending"
    assert artifact.review_required is True
    assert artifact.review_required_notes == ["possible chart level 270"]
    assert not hasattr(artifact, "approved_chart_claims")


class FakeOCRClient:
    def __init__(self, result: OCRClientResult) -> None:
        self.result = result
        self.calls: list[tuple[Path, str]] = []

    def extract_text(self, media_path: Path, *, model: str) -> OCRClientResult:
        self.calls.append((media_path, model))
        return self.result


def _image_artifact(tmp_path: Path) -> MediaArtifact:
    media_path = tmp_path / "chart.png"
    media_bytes = b"image bytes"
    media_path.write_bytes(media_bytes)
    return MediaArtifact(
        media_id="telegram_image_bablos79_10442",
        source_id="bablos79",
        capture_id="bablos79-10442",
        source_document_id="bablos79:bablos79-10442",
        source_timestamp_utc=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
        modality=MediaModality.SCREENSHOT,
        original_url_or_file_id="telegram-photo-id-1",
        local_path=str(media_path),
        media_sha256=hashlib.sha256(media_bytes).hexdigest(),
        mime_type="image/png",
        image_width_px=1280,
        image_height_px=720,
        retention_state=RetentionState.TEMPORARY,
        created_at_utc=datetime(2026, 5, 9, 12, 0, tzinfo=UTC),
    )
