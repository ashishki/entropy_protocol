"""Media artifact metadata and deterministic manifest export."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MediaModality(StrEnum):
    VOICE = "voice"
    AUDIO = "audio"
    IMAGE = "image"
    SCREENSHOT = "screenshot"
    OTHER = "other"


class RetentionState(StrEnum):
    TEMPORARY = "temporary"
    RETAINED_EVIDENCE_SNAPSHOT = "retained_evidence_snapshot"
    DELETED = "deleted"


class MediaArtifact(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    media_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_document_id: str = Field(min_length=1)
    source_timestamp_utc: datetime
    modality: MediaModality
    original_url_or_file_id: str = Field(min_length=1)
    local_path: str = Field(min_length=1)
    media_sha256: str = Field(min_length=64, max_length=64)
    mime_type: str = Field(min_length=1)
    duration_seconds: int | None = Field(default=None, ge=0)
    image_width_px: int | None = Field(default=None, ge=1)
    image_height_px: int | None = Field(default=None, ge=1)
    retention_state: RetentionState
    created_at_utc: datetime
    draft_transcript_refs: list[str] = Field(default_factory=list)
    draft_ocr_refs: list[str] = Field(default_factory=list)

    @field_validator("source_timestamp_utc", "created_at_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp fields must be datetime or ISO-8601 strings")

    @field_validator("media_sha256")
    @classmethod
    def _validate_sha256(cls, value: str) -> str:
        if any(char not in "0123456789abcdef" for char in value):
            raise ValueError("media_sha256 must be lowercase hexadecimal")
        return value


class MediaManifest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    rows: list[MediaArtifact]

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_media_manifest_markdown(self), encoding="utf-8")

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.model_dump_json(by_alias=False, exclude_none=True),
            encoding="utf-8",
        )


def build_media_manifest(artifacts: list[MediaArtifact]) -> MediaManifest:
    return MediaManifest(
        rows=sorted(
            artifacts,
            key=lambda item: (
                item.source_timestamp_utc.isoformat(),
                item.source_document_id,
                item.media_id,
            ),
        )
    )


def render_media_manifest_markdown(manifest: MediaManifest) -> str:
    lines = [
        "# Media Artifact Manifest",
        "",
        "This artifact is internal review support. It is not customer-facing.",
        "",
        "## Summary",
        "",
        f"- Media artifacts: {len(manifest.rows)}",
        "",
        "## Rows",
        "",
        (
            "| media_id | source_document_id | modality | retention_state | "
            "local_path | draft_transcript_refs | draft_ocr_refs |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for row in manifest.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.media_id,
                    row.source_document_id,
                    row.modality.value,
                    row.retention_state.value,
                    row.local_path,
                    ", ".join(row.draft_transcript_refs) or "none",
                    ", ".join(row.draft_ocr_refs) or "none",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "No Telegram, Whisper, OCR, provider, approved-ledger, or report output "
            "is created by this manifest.",
        ]
    )
    return "\n".join(lines) + "\n"
