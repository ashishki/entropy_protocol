"""Review-required OCR draft adapter for local image media artifacts."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.media.artifact import MediaArtifact, MediaModality

DEFAULT_OCR_MODEL = "ocr-draft-v1"


class DraftOCRStatus(StrEnum):
    DRAFT_PENDING_REVIEW = "draft_pending_review"


class UnsupportedOCRMediaError(ValueError):
    """Raised when OCR is requested for non-image media."""


class ChartInterpretationForbidden(ValueError):
    """Raised when caller attempts to store chart interpretation as truth."""


class OCRClientResult(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    text: str
    bounding_metadata: list[dict[str, str]] = Field(default_factory=list)
    review_required_notes: list[str] = Field(default_factory=list)


class OCRClient(Protocol):
    def extract_text(self, media_path: Path, *, model: str) -> OCRClientResult:
        """Extract draft OCR text from a local image path."""
        ...


class DraftOCRArtifact(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    ocr_id: str = Field(min_length=1)
    media_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    text: str
    text_sha256: str = Field(min_length=64, max_length=64)
    source_media_sha256: str = Field(min_length=64, max_length=64)
    bounding_metadata: list[dict[str, str]] = Field(default_factory=list)
    status: DraftOCRStatus
    reviewer_id: str = Field(default="pending", min_length=1)
    review_required: bool = True
    review_required_notes: list[str] = Field(default_factory=list)
    created_at_utc: datetime
    artifact_path: str | None = None


def run_ocr_draft(
    media: MediaArtifact,
    *,
    client: OCRClient,
    output_dir: Path,
    provider: str = "injected-ocr",
    model: str = DEFAULT_OCR_MODEL,
    chart_interpretation_notes: list[str] | None = None,
    approved_chart_claims: list[str] | None = None,
    created_at_utc: datetime | None = None,
) -> DraftOCRArtifact:
    _validate_media(media)
    if approved_chart_claims:
        raise ChartInterpretationForbidden(
            "chart-derived claims must be review-required notes"
        )

    result = client.extract_text(Path(media.local_path), model=model)
    notes = [*result.review_required_notes, *(chart_interpretation_notes or [])]
    text_sha256 = hashlib.sha256(result.text.encode("utf-8")).hexdigest()
    ocr_id = _ocr_id(media.media_id, text_sha256)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / f"{ocr_id}.json"
    artifact = DraftOCRArtifact(
        ocr_id=ocr_id,
        media_id=media.media_id,
        provider=provider,
        model=model,
        text=result.text,
        text_sha256=text_sha256,
        source_media_sha256=media.media_sha256,
        bounding_metadata=result.bounding_metadata,
        status=DraftOCRStatus.DRAFT_PENDING_REVIEW,
        reviewer_id="pending",
        review_required=True,
        review_required_notes=notes,
        created_at_utc=created_at_utc or datetime.now(UTC),
        artifact_path=str(artifact_path),
    )
    artifact_path.write_text(
        artifact.model_dump_json(by_alias=False, exclude_none=True),
        encoding="utf-8",
    )
    return artifact


def _validate_media(media: MediaArtifact) -> None:
    if media.modality not in {MediaModality.IMAGE, MediaModality.SCREENSHOT}:
        raise UnsupportedOCRMediaError("OCR requires image or screenshot media")


def _ocr_id(media_id: str, text_sha256: str) -> str:
    digest = hashlib.sha256(f"{media_id}:{text_sha256}".encode())
    return f"ocr_{digest.hexdigest()[:16]}"
