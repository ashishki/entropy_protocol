"""Source manifest schema and eligibility loading."""

from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class SourceManifestError(Exception):
    """Base exception for source manifest failures."""


class SourceNotApproved(SourceManifestError):
    """Raised when a source exists but is not approved for downstream use."""


class SourceType(StrEnum):
    TELEGRAM_PUBLIC = "telegram_public"
    X_PUBLIC = "x_public"
    WEBSITE_PUBLIC = "website_public"


class EligibilityVerdict(StrEnum):
    APPROVED = "approved"
    BLOCKED = "blocked"
    PENDING = "pending"


class SourceManifest(BaseModel):
    model_config = ConfigDict(strict=True)

    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    source_type: SourceType
    capture_method: str = Field(min_length=1)
    tos_reference: str = Field(min_length=1)
    eligibility_verdict: EligibilityVerdict
    operator_notes: str = ""

    @field_validator("source_type", mode="before")
    @classmethod
    def _coerce_source_type(cls, value: object) -> SourceType:
        if isinstance(value, SourceType):
            return value
        if isinstance(value, str):
            return SourceType(value)
        raise ValueError("source_type must be a SourceType or string")

    @field_validator("eligibility_verdict", mode="before")
    @classmethod
    def _coerce_eligibility_verdict(cls, value: object) -> EligibilityVerdict:
        if isinstance(value, EligibilityVerdict):
            return value
        if isinstance(value, str):
            return EligibilityVerdict(value)
        raise ValueError("eligibility_verdict must be an EligibilityVerdict or string")

    def model_dump_json(
        self, *args: Any, sort_keys: bool = False, **kwargs: Any
    ) -> str:
        if not sort_keys:
            return super().model_dump_json(*args, **kwargs)

        by_alias = kwargs.pop("by_alias", None)
        exclude_none = bool(kwargs.pop("exclude_none", False))
        data = self.model_dump(
            mode="json",
            by_alias=by_alias,
            exclude_none=exclude_none,
        )
        return json.dumps(
            data, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )

    @classmethod
    def from_json_bytes(cls, content: bytes) -> Self:
        try:
            return cls.model_validate_json(content)
        except ValidationError:
            raise


def manifest_path(workspace: Path, source_id: str) -> Path:
    return workspace / "sources" / f"{source_id}.json"


def save_source_manifest(manifest: SourceManifest, workspace: Path) -> Path:
    path = manifest_path(workspace, manifest.source_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        manifest.model_dump_json(by_alias=False, sort_keys=True), encoding="utf-8"
    )
    return path


def load_source_manifest(workspace: Path, source_id: str) -> SourceManifest:
    return SourceManifest.from_json_bytes(
        manifest_path(workspace, source_id).read_bytes()
    )


def load_source(workspace: Path, source_id: str) -> SourceManifest:
    manifest = load_source_manifest(workspace, source_id)
    if manifest.eligibility_verdict != EligibilityVerdict.APPROVED:
        raise SourceNotApproved(source_id)
    return manifest
