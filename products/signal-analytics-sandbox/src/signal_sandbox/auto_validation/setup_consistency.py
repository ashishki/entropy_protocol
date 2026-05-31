"""OCR/level and setup-consistency validator."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    TradeDirection,
)
from signal_sandbox.auto_validation.results import ValidationResult, ValidationStatus

SETUP_VALIDATOR_ID = "setup_consistency"
SETUP_VALIDATOR_VERSION = "setup_consistency.v1"
DEFAULT_MIN_CONFIDENCE = Decimal("0.75")
LEVEL_REF_TYPES = {"ocr", "chart_region", "model_span"}
DIRECTION_REF_TYPES = {"ocr", "chart_region", "model_span", "text_span"}


def validate_setup_consistency(
    bundle: AutoValidationEvidenceBundle | None,
    *,
    min_model_confidence: Decimal = DEFAULT_MIN_CONFIDENCE,
    created_at_utc: datetime | None = None,
) -> ValidationResult:
    """Validate that extracted levels describe one coherent trade setup."""

    if bundle is None:
        return _uncertain_result(
            candidate_id="unknown",
            evidence_ref_ids=["missing-bundle"],
            blocker_reasons=["missing_evidence_bundle"],
            deterministic_input_sha256=_input_sha256(None, min_model_confidence),
            created_at_utc=created_at_utc,
        )

    fields = bundle.extracted_fields
    evidence_refs = {ref.ref_id: ref for ref in bundle.evidence_refs}
    field_refs = fields.evidence_ref_ids_by_field

    if fields.direction in {TradeDirection.UNKNOWN, TradeDirection.MIXED}:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=_all_field_refs(field_refs),
            blocker_reasons=["mixed_or_unknown_trade_direction"],
            deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
            created_at_utc=created_at_utc,
        )

    if fields.entry is None or fields.stop is None or not fields.targets:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=_all_field_refs(field_refs),
            blocker_reasons=["ambiguous_or_missing_levels"],
            deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
            created_at_utc=created_at_utc,
        )

    missing_refs = _missing_required_refs(field_refs, evidence_refs)
    if missing_refs:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=_all_field_refs(field_refs) or ["missing-level-ref"],
            blocker_reasons=["missing_ocr_or_bounding_box_level_evidence"],
            deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
            created_at_utc=created_at_utc,
        )

    if _has_low_confidence(bundle, min_model_confidence):
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=_all_field_refs(field_refs),
            blocker_reasons=["low_confidence_level_evidence"],
            deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
            created_at_utc=created_at_utc,
        )

    if _has_conflicting_targets(fields.direction, fields.entry, fields.targets):
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=_all_field_refs(field_refs),
            blocker_reasons=["conflicting_targets"],
            deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
            created_at_utc=created_at_utc,
        )

    if not _is_coherent_setup(
        fields.direction,
        fields.entry,
        fields.stop,
        fields.targets,
    ):
        return ValidationResult(
            validator_id=SETUP_VALIDATOR_ID,
            validator_version=SETUP_VALIDATOR_VERSION,
            candidate_id=bundle.candidate_id,
            status=ValidationStatus.FAILED,
            confidence=Decimal("1"),
            evidence_ref_ids=_all_field_refs(field_refs),
            blocker_reasons=["setup_math_inconsistent"],
            deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
            rationale="entry, stop, target, and direction do not form a valid setup",
            created_at_utc=created_at_utc or datetime.now(UTC),
        )

    return ValidationResult(
        validator_id=SETUP_VALIDATOR_ID,
        validator_version=SETUP_VALIDATOR_VERSION,
        candidate_id=bundle.candidate_id,
        status=ValidationStatus.PASSED,
        confidence=Decimal("1"),
        evidence_ref_ids=_all_field_refs(field_refs),
        blocker_reasons=[],
        deterministic_input_sha256=_input_sha256(bundle, min_model_confidence),
        rationale="levels have required evidence refs and coherent setup math",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _uncertain_result(
    *,
    candidate_id: str,
    evidence_ref_ids: list[str],
    blocker_reasons: list[str],
    deterministic_input_sha256: str,
    created_at_utc: datetime | None,
) -> ValidationResult:
    return ValidationResult(
        validator_id=SETUP_VALIDATOR_ID,
        validator_version=SETUP_VALIDATOR_VERSION,
        candidate_id=candidate_id,
        status=ValidationStatus.UNCERTAIN_NEEDS_HUMAN,
        confidence=Decimal("0"),
        evidence_ref_ids=evidence_ref_ids,
        blocker_reasons=blocker_reasons,
        deterministic_input_sha256=deterministic_input_sha256,
        rationale="setup consistency cannot be proven from available evidence",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _missing_required_refs(
    field_refs: dict[str, list[str]],
    evidence_refs: dict[str, EvidenceRef],
) -> list[str]:
    missing: list[str] = []
    for field in ("entry", "stop", "targets"):
        refs = field_refs.get(field, [])
        if not refs or not any(
            evidence_refs.get(ref_id) is not None
            and evidence_refs[ref_id].ref_type in LEVEL_REF_TYPES
            for ref_id in refs
        ):
            missing.append(field)

    direction_refs = field_refs.get("direction", [])
    if not direction_refs or not any(
        evidence_refs.get(ref_id) is not None
        and evidence_refs[ref_id].ref_type in DIRECTION_REF_TYPES
        for ref_id in direction_refs
    ):
        missing.append("direction")
    return missing


def _has_low_confidence(
    bundle: AutoValidationEvidenceBundle,
    min_model_confidence: Decimal,
) -> bool:
    checked_fields = {"direction", "entry", "stop", "target", "targets"}
    return any(
        span.field in checked_fields
        and span.confidence is not None
        and span.confidence < min_model_confidence
        for span in bundle.model_extraction_spans
    )


def _has_conflicting_targets(
    direction: TradeDirection,
    entry: Decimal,
    targets: list[Decimal],
) -> bool:
    if len(targets) < 2:
        return False
    if direction == TradeDirection.LONG:
        return any(target <= entry for target in targets) and any(
            target > entry for target in targets
        )
    if direction == TradeDirection.SHORT:
        return any(target >= entry for target in targets) and any(
            target < entry for target in targets
        )
    return False


def _is_coherent_setup(
    direction: TradeDirection,
    entry: Decimal,
    stop: Decimal,
    targets: list[Decimal],
) -> bool:
    if direction == TradeDirection.LONG:
        return stop < entry and all(entry < target for target in targets)
    if direction == TradeDirection.SHORT:
        return all(target < entry for target in targets) and entry < stop
    return False


def _all_field_refs(field_refs: dict[str, list[str]]) -> list[str]:
    refs = {ref_id for refs in field_refs.values() for ref_id in refs}
    return sorted(refs)


def _input_sha256(
    bundle: AutoValidationEvidenceBundle | None,
    min_model_confidence: Decimal,
) -> str:
    payload = {
        "bundle_sha256": bundle.bundle_sha256() if bundle is not None else None,
        "min_model_confidence": str(min_model_confidence),
        "validator_id": SETUP_VALIDATOR_ID,
        "validator_version": SETUP_VALIDATOR_VERSION,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
