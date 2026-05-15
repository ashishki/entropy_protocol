"""Validation helpers for draft extraction pseudo-labels."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from signal_sandbox.capture.loader import CapturedPost


class PseudoLabelValidationError(ValueError):
    """Raised when a pseudo-label is not supported by its raw capture text."""


def validate_pseudo_label(
    post: CapturedPost, pseudo_label: Mapping[str, Any]
) -> Mapping[str, Any]:
    """Validate that pseudo-label spans and candidate fields are text-supported."""

    if pseudo_label.get("capture_id") != post.capture_id:
        raise PseudoLabelValidationError("capture_id does not match post")

    raw_text = post.raw_text.casefold()
    spans = _require_sequence(pseudo_label.get("evidence_spans"), "evidence_spans")
    span_fields = _validate_spans(raw_text, spans)

    candidate_fields = _require_mapping(
        pseudo_label.get("candidate_fields"), "candidate_fields"
    )
    _validate_candidate_fields(raw_text, candidate_fields, span_fields)

    return pseudo_label


def _validate_spans(raw_text: str, spans: Sequence[object]) -> dict[str, list[str]]:
    span_fields: dict[str, list[str]] = {}
    for span in spans:
        span_mapping = _require_mapping(span, "evidence_spans[]")
        field = _require_str(span_mapping.get("field"), "evidence_spans[].field")
        text = _require_str(span_mapping.get("text"), "evidence_spans[].text")
        if text.casefold() not in raw_text:
            raise PseudoLabelValidationError(
                f"evidence span for {field!r} is absent from raw text"
            )
        span_fields.setdefault(field, []).append(text.casefold())
    return span_fields


def _validate_candidate_fields(
    raw_text: str,
    candidate_fields: Mapping[str, object],
    span_fields: Mapping[str, list[str]],
) -> None:
    for asset in _optional_str_sequence(candidate_fields.get("asset_candidates")):
        if not _is_supported_value(raw_text, span_fields, "asset_candidates", asset):
            raise PseudoLabelValidationError(
                f"asset candidate {asset!r} is absent from raw text"
            )

    direction = candidate_fields.get("direction_candidate")
    if isinstance(direction, str) and direction not in {"", "unknown"}:
        if "direction_candidate" not in span_fields:
            raise PseudoLabelValidationError(
                "direction candidate requires direction evidence span"
            )

    for field in ("entry_candidate", "stop_candidate", "target_candidate"):
        value = candidate_fields.get(field)
        if value is None or value == "":
            continue
        if not _is_supported_value(raw_text, span_fields, field, str(value)):
            raise PseudoLabelValidationError(
                f"{field} value {value!r} is absent from raw text"
            )


def _is_supported_value(
    raw_text: str,
    span_fields: Mapping[str, list[str]],
    field: str,
    value: str,
) -> bool:
    folded = value.casefold()
    return (
        folded in raw_text
        or f"#{folded}" in raw_text
        or any(folded in span for span in span_fields.get(field, []))
    )


def _require_mapping(value: object, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PseudoLabelValidationError(f"{field_name} must be an object")
    return value


def _require_sequence(value: object, field_name: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise PseudoLabelValidationError(f"{field_name} must be a list")
    return value


def _require_str(value: object, field_name: str) -> str:
    if not isinstance(value, str) or value == "":
        raise PseudoLabelValidationError(f"{field_name} must be a non-empty string")
    return value


def _optional_str_sequence(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise PseudoLabelValidationError("asset_candidates must be a list")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise PseudoLabelValidationError("asset_candidates must contain strings")
        result.append(item)
    return result
