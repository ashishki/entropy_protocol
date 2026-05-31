"""Deterministic schema compatibility classification primitives."""

from __future__ import annotations

import re
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field


SCHEMA_COMPATIBILITY_CATEGORIES = (
    "same_version",
    "backward_compatible",
    "migration_required",
    "unsupported_major",
    "malformed_version",
)
SCHEMA_COMPATIBILITY_BLOCKED_SURFACES = (
    "public_sdk",
    "hosted_service",
    "live_execution",
    "holdout_access",
    "production_credentials",
    "capital",
    "external_compliance",
)
_SCHEMA_VERSION_RE = re.compile(
    r"^(?P<name>[a-z0-9][a-z0-9-]*)/v(?P<version>[0-9]+(?:\.[0-9]+){0,2})$"
)


class SchemaVersion(BaseModel):
    """Parsed schema identifier normalized for compatibility comparison."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    raw: str = Field(min_length=1)
    name: str = Field(min_length=1)
    major: int = Field(ge=0)
    minor: int = Field(ge=0)
    patch: int = Field(ge=0)

    @property
    def normalized(self) -> str:
        """Return a normalized `name/vMAJOR.MINOR.PATCH` identifier."""

        return f"{self.name}/v{self.major}.{self.minor}.{self.patch}"


class SchemaCompatibilityResult(BaseModel):
    """Safe operator-facing schema compatibility result."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    source_schema: str
    target_schema: str
    category: Literal[
        "same_version",
        "backward_compatible",
        "migration_required",
        "unsupported_major",
        "malformed_version",
    ]
    reason_code: str
    approval_state: Literal["not_approved"] = "not_approved"
    blocked_surfaces: tuple[str, ...] = SCHEMA_COMPATIBILITY_BLOCKED_SURFACES


def parse_schema_version(schema_id: str) -> SchemaVersion | None:
    """Parse a schema id or return None when it cannot be classified safely."""

    match = _SCHEMA_VERSION_RE.match(schema_id)
    if not match:
        return None
    version_parts = [int(part) for part in match.group("version").split(".")]
    if len(version_parts) == 1:
        version_parts.extend([0, 0])
    elif len(version_parts) == 2:
        version_parts.append(0)
    return SchemaVersion(
        raw=schema_id,
        name=match.group("name"),
        major=version_parts[0],
        minor=version_parts[1],
        patch=version_parts[2],
    )


def classify_schema_compatibility(
    source_schema: str,
    target_schema: str,
    *,
    supported_major_versions: tuple[int, ...] = (1,),
) -> SchemaCompatibilityResult:
    """Classify compatibility between two schema identifiers.

    The result is deliberately limited to local validation semantics. It never
    grants production, public, live, holdout, capital, or compliance approval.
    """

    source = parse_schema_version(source_schema)
    target = parse_schema_version(target_schema)
    if source is None or target is None:
        return SchemaCompatibilityResult(
            source_schema=source_schema,
            target_schema=target_schema,
            category="malformed_version",
            reason_code="schema_version_parse_failed",
        )
    if source.name != target.name:
        return SchemaCompatibilityResult(
            source_schema=source_schema,
            target_schema=target_schema,
            category="unsupported_major",
            reason_code="schema_name_mismatch",
        )
    if source.major not in supported_major_versions or target.major not in supported_major_versions:
        return SchemaCompatibilityResult(
            source_schema=source_schema,
            target_schema=target_schema,
            category="unsupported_major",
            reason_code="major_version_not_supported",
        )
    if source.normalized == target.normalized:
        return SchemaCompatibilityResult(
            source_schema=source_schema,
            target_schema=target_schema,
            category="same_version",
            reason_code="same_schema_version",
        )
    if source.major != target.major:
        return SchemaCompatibilityResult(
            source_schema=source_schema,
            target_schema=target_schema,
            category="migration_required",
            reason_code="major_version_change_requires_migration",
        )
    if (target.minor, target.patch) >= (source.minor, source.patch):
        return SchemaCompatibilityResult(
            source_schema=source_schema,
            target_schema=target_schema,
            category="backward_compatible",
            reason_code="target_minor_or_patch_is_forward_compatible",
        )
    return SchemaCompatibilityResult(
        source_schema=source_schema,
        target_schema=target_schema,
        category="migration_required",
        reason_code="target_version_is_older_than_source",
    )
