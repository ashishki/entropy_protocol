"""Post-factum and closed-position cue detector."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.auto_validation.evidence import AutoValidationEvidenceBundle
from signal_sandbox.auto_validation.results import ValidationResult, ValidationStatus

POST_FACTUM_VALIDATOR_ID = "post_factum"
POST_FACTUM_VALIDATOR_VERSION = "post_factum.v1"
DEFAULT_MIN_CONFIDENCE = Decimal("0.80")
POST_FACTUM_RISK = "post_factum_risk"
AUTO_REJECTED_FOR_PREDICTIVE_METRICS = "auto_rejected_for_predictive_metrics"


class CueFamily(StrEnum):
    POST_FACTUM = "post_factum"
    PREDICTIVE = "predictive"
    UNKNOWN = "unknown"


class PostFactumCueEvidence(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    evidence_ref_id: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    confidence: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))


POST_FACTUM_PATTERNS: tuple[str, ...] = (
    "pnl",
    "profit",
    "closed",
    "закрыл",
    "закрыта",
    "закрыли",
    "тейк",
    "take profit",
    "tp hit",
    "take-profit",
    "стоп в безубыток",
    "перенес стоп",
    "уже",
    "отработал",
    "отработка",
    "результат",
)
PREDICTIVE_PATTERNS: tuple[str, ...] = (
    "если",
    "план",
    "жду",
    "вход",
    "entry",
    "target",
    "looking for",
    "will",
)


def detect_post_factum_cues(
    bundle: AutoValidationEvidenceBundle | None,
    *,
    cue_evidence: Iterable[PostFactumCueEvidence],
    min_confidence: Decimal = DEFAULT_MIN_CONFIDENCE,
    created_at_utc: datetime | None = None,
) -> ValidationResult:
    """Detect post-factum evidence that cannot enter predictive metrics."""

    cues = list(cue_evidence)
    if bundle is None:
        return _uncertain_result(
            candidate_id="unknown",
            evidence_ref_ids=["missing-bundle"],
            blocker_reasons=["missing_evidence_bundle"],
            deterministic_input_sha256=_input_sha256(None, cues, min_confidence),
            created_at_utc=created_at_utc,
        )

    cited_refs = sorted({cue.evidence_ref_id for cue in cues}) or [
        bundle.source_document_id
    ]
    classified = [(cue, _classify(cue.excerpt)) for cue in cues]
    post_factum = [cue for cue, family in classified if family == CueFamily.POST_FACTUM]
    predictive = [cue for cue, family in classified if family == CueFamily.PREDICTIVE]

    if post_factum and predictive:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=cited_refs,
            blocker_reasons=["mixed_predictive_and_post_factum_cues"],
            deterministic_input_sha256=_input_sha256(bundle, cues, min_confidence),
            created_at_utc=created_at_utc,
        )

    if any(cue.confidence < min_confidence for cue in post_factum):
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=cited_refs,
            blocker_reasons=["low_confidence_post_factum_cues"],
            deterministic_input_sha256=_input_sha256(bundle, cues, min_confidence),
            created_at_utc=created_at_utc,
        )

    if post_factum:
        return ValidationResult(
            validator_id=POST_FACTUM_VALIDATOR_ID,
            validator_version=POST_FACTUM_VALIDATOR_VERSION,
            candidate_id=bundle.candidate_id,
            status=ValidationStatus.FAILED,
            confidence=max(cue.confidence for cue in post_factum),
            evidence_ref_ids=cited_refs,
            blocker_reasons=[POST_FACTUM_RISK, AUTO_REJECTED_FOR_PREDICTIVE_METRICS],
            deterministic_input_sha256=_input_sha256(bundle, cues, min_confidence),
            rationale="high-confidence post-factum cues block predictive metrics",
            created_at_utc=created_at_utc or datetime.now(UTC),
        )

    return ValidationResult(
        validator_id=POST_FACTUM_VALIDATOR_ID,
        validator_version=POST_FACTUM_VALIDATOR_VERSION,
        candidate_id=bundle.candidate_id,
        status=ValidationStatus.PASSED,
        confidence=Decimal("1"),
        evidence_ref_ids=cited_refs,
        blocker_reasons=[],
        deterministic_input_sha256=_input_sha256(bundle, cues, min_confidence),
        rationale="no post-factum or closed-position cue detected",
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
        validator_id=POST_FACTUM_VALIDATOR_ID,
        validator_version=POST_FACTUM_VALIDATOR_VERSION,
        candidate_id=candidate_id,
        status=ValidationStatus.UNCERTAIN_NEEDS_HUMAN,
        confidence=Decimal("0"),
        evidence_ref_ids=evidence_ref_ids,
        blocker_reasons=blocker_reasons,
        deterministic_input_sha256=deterministic_input_sha256,
        rationale="post-factum cue classification needs human review",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _classify(excerpt: str) -> CueFamily:
    folded = excerpt.casefold()
    if any(pattern in folded for pattern in POST_FACTUM_PATTERNS):
        return CueFamily.POST_FACTUM
    if any(pattern in folded for pattern in PREDICTIVE_PATTERNS):
        return CueFamily.PREDICTIVE
    return CueFamily.UNKNOWN


def _input_sha256(
    bundle: AutoValidationEvidenceBundle | None,
    cues: list[PostFactumCueEvidence],
    min_confidence: Decimal,
) -> str:
    payload = {
        "bundle_sha256": bundle.bundle_sha256() if bundle is not None else None,
        "cues": [
            cue.model_dump(mode="json", by_alias=False, exclude_none=True)
            for cue in cues
        ],
        "min_confidence": str(min_confidence),
        "validator_id": POST_FACTUM_VALIDATOR_ID,
        "validator_version": POST_FACTUM_VALIDATOR_VERSION,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
