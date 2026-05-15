"""Local artifact-store abstractions."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import ClassVar, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field


class ArtifactStoreViolation(ValueError):
    """Raised when an artifact store operation is unsafe."""


class ArtifactStoreRef(BaseModel):
    """Stable reference returned by artifact stores."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    backend: Literal["filesystem"]
    ref: str = Field(min_length=1)
    sha256: str = Field(min_length=1)
    size_bytes: int = Field(ge=0)
    relative_path: str = Field(min_length=1)


class ObjectArtifactStore(Protocol):
    """Future object-store boundary; no runtime dependency is required."""

    def write_payload(self, payload: bytes | str, *, prefix: str = "payloads") -> ArtifactStoreRef:
        """Write an artifact payload and return a stable reference."""
        ...


class FilesystemArtifactStore:
    """Content-addressed local filesystem artifact store."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def write_payload(self, payload: bytes | str, *, prefix: str = "payloads") -> ArtifactStoreRef:
        """Write payload bytes under a content-addressed path."""
        payload_bytes = payload.encode("utf-8") if isinstance(payload, str) else payload
        digest = hashlib.sha256(payload_bytes).hexdigest()
        safe_prefix = _safe_relative_path(prefix)
        relative_path = safe_prefix / digest[:2] / digest
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(payload_bytes)
        return ArtifactStoreRef(
            backend="filesystem",
            ref="artifact://filesystem/" + relative_path.as_posix(),
            sha256="sha256:" + digest,
            size_bytes=len(payload_bytes),
            relative_path=relative_path.as_posix(),
        )


def _safe_relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not value.strip():
        raise ArtifactStoreViolation("Artifact store paths must be safe relative paths.")
    return path


__all__ = [
    "ArtifactStoreRef",
    "ArtifactStoreViolation",
    "FilesystemArtifactStore",
    "ObjectArtifactStore",
]
