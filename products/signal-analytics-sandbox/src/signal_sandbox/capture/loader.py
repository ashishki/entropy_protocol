"""Load operator-captured public posts from disk."""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.sources.private_patterns import is_private_source_url


class CaptureLoaderError(Exception):
    """Base exception for capture loading failures."""


class CaptureChecksumMismatch(CaptureLoaderError):
    """Raised when raw_text does not match the declared SHA-256."""


class PrivateSourceForbidden(CaptureLoaderError):
    """Raised when a capture URL points at a private/restricted source."""


class CapturedPost(BaseModel):
    model_config = ConfigDict(strict=True)

    capture_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    capture_timestamp_utc: datetime
    raw_text: str
    text_sha256: str = Field(min_length=64, max_length=64)


def compute_text_sha256(raw_text: str) -> str:
    return hashlib.sha256(raw_text.encode("utf-8")).hexdigest()


def load_capture(path: Path) -> CapturedPost:
    post = CapturedPost.model_validate_json(path.read_bytes())

    if is_private_source_url(post.evidence_url):
        raise PrivateSourceForbidden("private source URL rejected")

    actual_sha = compute_text_sha256(post.raw_text)
    if actual_sha != post.text_sha256:
        raise CaptureChecksumMismatch(path.name)

    return post


def load_captures(workspace: Path, source_id: str) -> list[CapturedPost]:
    captures_dir = workspace / "captures" / source_id
    if not captures_dir.exists():
        return []

    posts = [load_capture(path) for path in sorted(captures_dir.glob("*.json"))]
    return sorted(posts, key=lambda post: (post.capture_timestamp_utc, post.capture_id))
