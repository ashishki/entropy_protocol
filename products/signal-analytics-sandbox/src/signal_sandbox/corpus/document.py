"""Normalized source document schema for public captures."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.capture.loader import CapturedPost


class SourceDocument(BaseModel):
    model_config = ConfigDict(strict=True)

    document_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    author: str = Field(min_length=1)
    timestamp_utc: datetime
    text: str
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)
    media_refs: list[str] = Field(default_factory=list)
    transcript_refs: list[str] = Field(default_factory=list)
    ocr_refs: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp_utc must be a datetime or ISO-8601 string")


def from_captured_post(
    post: CapturedPost,
    *,
    author: str | None = None,
    metadata: dict[str, str] | None = None,
) -> SourceDocument:
    return SourceDocument(
        document_id=f"{post.source_id}:{post.capture_id}",
        capture_id=post.capture_id,
        source_id=post.source_id,
        author=author or post.source_id,
        timestamp_utc=post.capture_timestamp_utc,
        text=post.raw_text,
        evidence_url=post.evidence_url,
        text_sha256=post.text_sha256,
        metadata=metadata or {},
    )
