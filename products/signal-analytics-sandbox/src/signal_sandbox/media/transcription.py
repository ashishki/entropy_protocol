"""Gated draft transcription adapter for local voice media artifacts."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Mapping
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.media.artifact import MediaArtifact

TRANSCRIPTION_ENABLE_ENV = "SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION"
DEFAULT_WHISPER_MODEL = "whisper-1"


class DraftTranscriptStatus(StrEnum):
    DRAFT_PENDING_REVIEW = "draft_pending_review"


class TranscriptionRunStatus(StrEnum):
    SKIPPED = "skipped"
    DRAFT_PENDING_REVIEW = "draft_pending_review"
    PROVIDER_FAILED = "provider_failed"


class WhisperTranscriptionClientError(Exception):
    """Raised by fake or real transcription clients on provider failure."""


class WhisperTranscriptionClient(Protocol):
    def transcribe(self, media_path: Path, *, model: str) -> str:
        """Return transcript text for a local media file."""
        ...


class DraftTranscriptArtifact(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    transcript_id: str = Field(min_length=1)
    media_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    transcript_text: str
    transcript_sha256: str = Field(min_length=64, max_length=64)
    source_media_sha256: str = Field(min_length=64, max_length=64)
    status: DraftTranscriptStatus
    reviewer_id: str = Field(default="pending", min_length=1)
    review_required: bool = True
    created_at_utc: datetime
    raw_media_retention_action: str = Field(min_length=1)
    artifact_path: str | None = None


class TranscriptionRunResult(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    status: TranscriptionRunStatus
    media_id: str = Field(min_length=1)
    transcript: DraftTranscriptArtifact | None = None
    skipped_reason: str | None = None
    error_type: str | None = None


def run_whisper_transcription(
    media: MediaArtifact,
    *,
    client: WhisperTranscriptionClient,
    output_dir: Path,
    env: Mapping[str, str] | None = None,
    per_run_approved: bool,
    provider: str = "managed-whisper",
    model: str = DEFAULT_WHISPER_MODEL,
    delete_raw_on_success: bool = True,
    created_at_utc: datetime | None = None,
) -> TranscriptionRunResult:
    if not _env_enabled(env):
        return _skipped(media, "environment_disabled")
    if not per_run_approved:
        return _skipped(media, "per_run_approval_missing")

    try:
        transcript_text = client.transcribe(Path(media.local_path), model=model)
    except Exception as exc:
        return TranscriptionRunResult(
            status=TranscriptionRunStatus.PROVIDER_FAILED,
            media_id=media.media_id,
            error_type=type(exc).__name__,
        )

    transcript = _draft_transcript(
        media,
        transcript_text=transcript_text,
        provider=provider,
        model=model,
        output_dir=output_dir,
        delete_raw_on_success=delete_raw_on_success,
        created_at_utc=created_at_utc or datetime.now(UTC),
    )
    return TranscriptionRunResult(
        status=TranscriptionRunStatus.DRAFT_PENDING_REVIEW,
        media_id=media.media_id,
        transcript=transcript,
    )


def _env_enabled(env: Mapping[str, str] | None) -> bool:
    values = os.environ if env is None else env
    return values.get(TRANSCRIPTION_ENABLE_ENV, "").strip() == "1"


def _skipped(media: MediaArtifact, reason: str) -> TranscriptionRunResult:
    return TranscriptionRunResult(
        status=TranscriptionRunStatus.SKIPPED,
        media_id=media.media_id,
        skipped_reason=reason,
    )


def _draft_transcript(
    media: MediaArtifact,
    *,
    transcript_text: str,
    provider: str,
    model: str,
    output_dir: Path,
    delete_raw_on_success: bool,
    created_at_utc: datetime,
) -> DraftTranscriptArtifact:
    transcript_sha256 = hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
    transcript_id = _transcript_id(media.media_id, transcript_sha256)
    retention_action = _apply_success_retention(media, delete_raw_on_success)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / f"{transcript_id}.json"
    artifact = DraftTranscriptArtifact(
        transcript_id=transcript_id,
        media_id=media.media_id,
        provider=provider,
        model=model,
        transcript_text=transcript_text,
        transcript_sha256=transcript_sha256,
        source_media_sha256=media.media_sha256,
        status=DraftTranscriptStatus.DRAFT_PENDING_REVIEW,
        reviewer_id="pending",
        review_required=True,
        created_at_utc=created_at_utc,
        raw_media_retention_action=retention_action,
        artifact_path=str(artifact_path),
    )
    artifact_path.write_text(
        artifact.model_dump_json(by_alias=False, exclude_none=True),
        encoding="utf-8",
    )
    return artifact


def _transcript_id(media_id: str, transcript_sha256: str) -> str:
    digest = hashlib.sha256(f"{media_id}:{transcript_sha256}".encode())
    return f"transcript_{digest.hexdigest()[:16]}"


def _apply_success_retention(
    media: MediaArtifact,
    delete_raw_on_success: bool,
) -> str:
    media_path = Path(media.local_path)
    if delete_raw_on_success and media_path.exists():
        media_path.unlink()
        return "deleted_after_transcription"
    return "retained_by_policy"
