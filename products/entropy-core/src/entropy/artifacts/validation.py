"""Deterministic artifact file loading and validation results."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from entropy.artifacts.contract import ArtifactContractV1

ERROR_SEVERITY = "P1"
SUPPORTED_ARTIFACT_SUFFIXES = (".json", ".yaml", ".yml")


class ArtifactValidationError(BaseModel):
    """Stable redacted validation error for artifact operators."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    path: str
    code: str
    severity: Literal["P0", "P1", "P2", "P3"]
    message: str


class ArtifactValidationResult(BaseModel):
    """Validation outcome that avoids echoing private artifact payloads."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    ok: bool
    artifact: ArtifactContractV1 | None = None
    errors: tuple[ArtifactValidationError, ...] = ()


def validate_artifact_file(path: str | Path) -> ArtifactValidationResult:
    """Load and validate a JSON or YAML artifact file."""
    artifact_path = Path(path)
    try:
        payload = load_artifact_payload(artifact_path)
    except ArtifactPayloadError as exc:
        return ArtifactValidationResult(
            ok=False,
            errors=(
                ArtifactValidationError(
                    path="$",
                    code=exc.code,
                    severity=ERROR_SEVERITY,
                    message=exc.safe_message,
                ),
            ),
        )

    return validate_artifact_payload(payload)


def validate_artifact_payload(payload: object) -> ArtifactValidationResult:
    """Validate an artifact payload object without exposing raw invalid values."""
    try:
        artifact = ArtifactContractV1.model_validate(payload)
    except ValidationError as exc:
        errors = tuple(sorted(_redacted_errors(exc), key=_error_sort_key))
        return ArtifactValidationResult(ok=False, errors=errors)

    return ArtifactValidationResult(ok=True, artifact=artifact)


def load_artifact_payload(path: str | Path) -> dict[str, object]:
    """Load a JSON or YAML artifact payload from disk."""
    artifact_path = Path(path)
    suffix = artifact_path.suffix.lower()
    if suffix not in SUPPORTED_ARTIFACT_SUFFIXES:
        raise ArtifactPayloadError(
            "artifact.unsupported_format", "Unsupported artifact file format."
        )

    try:
        raw = artifact_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ArtifactPayloadError(
            "artifact.read_error", "Artifact file could not be read."
        ) from exc

    try:
        if suffix == ".json":
            loaded = json.loads(raw)
        else:
            loaded = _load_yaml(raw)
    except (ValueError, TypeError) as exc:
        raise ArtifactPayloadError(
            "artifact.parse_error", "Artifact file could not be parsed."
        ) from exc

    if not isinstance(loaded, dict):
        raise ArtifactPayloadError("artifact.root_type", "Artifact file root must be an object.")
    return loaded


class ArtifactPayloadError(ValueError):
    """Internal load failure with a deterministic public error code."""

    def __init__(self, code: str, safe_message: str) -> None:
        super().__init__(safe_message)
        self.code = code
        self.safe_message = safe_message


def _redacted_errors(exc: ValidationError) -> tuple[ArtifactValidationError, ...]:
    return tuple(
        ArtifactValidationError(
            path=_loc_to_path(error.get("loc", ())),
            code=_error_code(error),
            severity=ERROR_SEVERITY,
            message=_error_message(error),
        )
        for error in exc.errors(include_input=False, include_context=False, include_url=False)
    )


def _loc_to_path(loc: object) -> str:
    if not isinstance(loc, tuple) or not loc:
        return "$"

    path = "$"
    for part in loc:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def _error_code(error: Mapping[str, Any]) -> str:
    error_type = str(error.get("type", "validation_error")).replace("-", "_")
    if error_type == "extra_forbidden":
        return "artifact.extra_field"
    if error_type == "missing":
        return "artifact.required"
    if error_type == "literal_error":
        return "artifact.invalid_state"
    if error_type == "value_error":
        return "artifact.boundary_violation"
    return "artifact." + error_type


def _error_message(error: Mapping[str, Any]) -> str:
    code = _error_code(error)
    if code == "artifact.extra_field":
        return "Unknown artifact field is not allowed."
    if code == "artifact.required":
        return "Required artifact field is missing."
    if code == "artifact.invalid_state":
        return "Artifact field uses a value outside the frozen vocabulary."
    if code == "artifact.boundary_violation":
        return "Artifact violates a Core boundary rule."
    return "Artifact field failed schema validation."


def _error_sort_key(error: ArtifactValidationError) -> tuple[str, str, str]:
    return (error.path, error.code, error.message)


def _load_yaml(raw: str) -> object:
    try:
        import yaml  # type: ignore[import-untyped]
    except ModuleNotFoundError:
        return _load_simple_yaml(raw)

    return yaml.safe_load(raw)


def _load_simple_yaml(raw: str) -> dict[str, object]:
    payload: dict[str, object] = {}
    current_list_key: str | None = None

    for line_number, raw_line in enumerate(raw.splitlines(), start=1):
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError(f"Unexpected list item on line {line_number}")
            value = payload[current_list_key]
            if not isinstance(value, list):
                raise ValueError(f"Unexpected scalar/list mix on line {line_number}")
            value.append(_parse_yaml_scalar(line[4:].strip()))
            continue
        if line.startswith(" "):
            raise ValueError(f"Unsupported YAML indentation on line {line_number}")

        key, separator, value = line.partition(":")
        if not separator or not key.strip():
            raise ValueError(f"Invalid YAML mapping on line {line_number}")

        current_list_key = None
        normalized_key = key.strip()
        stripped_value = value.strip()
        if stripped_value:
            payload[normalized_key] = _parse_yaml_scalar(stripped_value)
        else:
            payload[normalized_key] = []
            current_list_key = normalized_key

    return payload


def _parse_yaml_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


__all__ = [
    "ArtifactValidationError",
    "ArtifactValidationResult",
    "load_artifact_payload",
    "validate_artifact_file",
    "validate_artifact_payload",
]
