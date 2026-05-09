"""Telegram voice acquisition for operator-authorized public evidence."""

from __future__ import annotations

import hashlib
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.media.artifact import MediaArtifact, MediaModality, RetentionState


class MediaAuthorization(StrEnum):
    PUBLIC_TELEGRAM = "public_telegram"
    OPERATOR_FORWARDED_PUBLIC = "operator_forwarded_public"
    FORBIDDEN_PRIVATE = "forbidden_private"
    FORBIDDEN_AUTHENTICATED = "forbidden_authenticated"


class TelegramVoiceAcquisitionError(Exception):
    """Base error for Telegram voice acquisition failures."""


class UnauthorizedMediaError(TelegramVoiceAcquisitionError):
    """Raised when media is outside the ADR-004/legal memo authorization."""


class TelegramVoiceDownloadError(TelegramVoiceAcquisitionError):
    """Raised when Telegram file download fails before artifact creation."""


class TelegramDownloadableFile(Protocol):
    async def download_to_drive(self, custom_path: str) -> object:
        """Download file bytes to custom_path."""
        ...


class TelegramVoiceClient(Protocol):
    async def get_file(self, file_id: str) -> TelegramDownloadableFile:
        """Return a downloadable Telegram file handle."""
        ...


class TelegramVoiceAcquisitionRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    file_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_document_id: str = Field(min_length=1)
    source_timestamp_utc: datetime
    duration_seconds: int | None = Field(default=None, ge=0)
    authorization: MediaAuthorization
    legal_media_authorized: bool
    created_at_utc: datetime
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("source_timestamp_utc", "created_at_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp fields must be datetime or ISO-8601 strings")


async def acquire_telegram_voice_artifact(
    request: TelegramVoiceAcquisitionRequest,
    *,
    client: TelegramVoiceClient,
    media_dir: Path,
) -> MediaArtifact:
    _validate_authorization(request)
    media_dir.mkdir(parents=True, exist_ok=True)
    media_id = _media_id(request)
    final_path = media_dir / f"{media_id}.ogg"
    partial_path = media_dir / f"{media_id}.ogg.part"

    try:
        telegram_file = await client.get_file(request.file_id)
        await telegram_file.download_to_drive(custom_path=str(partial_path))
        media_sha256 = _sha256_file(partial_path)
        partial_path.replace(final_path)
    except Exception as exc:
        _cleanup_partial(partial_path)
        raise TelegramVoiceDownloadError("telegram voice download failed") from exc

    return MediaArtifact(
        media_id=media_id,
        source_id=request.source_id,
        capture_id=request.capture_id,
        source_document_id=request.source_document_id,
        source_timestamp_utc=request.source_timestamp_utc,
        modality=MediaModality.VOICE,
        original_url_or_file_id=request.file_id,
        local_path=str(final_path),
        media_sha256=media_sha256,
        mime_type="audio/ogg",
        duration_seconds=request.duration_seconds,
        retention_state=RetentionState.TEMPORARY,
        created_at_utc=request.created_at_utc,
    )


def _validate_authorization(request: TelegramVoiceAcquisitionRequest) -> None:
    if not request.legal_media_authorized:
        raise UnauthorizedMediaError("legal media authorization is required")
    if request.authorization not in {
        MediaAuthorization.PUBLIC_TELEGRAM,
        MediaAuthorization.OPERATOR_FORWARDED_PUBLIC,
    }:
        raise UnauthorizedMediaError("telegram media source is not authorized")


def _media_id(request: TelegramVoiceAcquisitionRequest) -> str:
    digest = hashlib.sha256(request.file_id.encode("utf-8")).hexdigest()[:16]
    return f"telegram_voice_{request.source_id}_{request.capture_id}_{digest}"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cleanup_partial(partial_path: Path) -> None:
    if partial_path.exists():
        partial_path.unlink()
