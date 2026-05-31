"""Pre-outcome timing validator for auto-validation candidates."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    MarketWindowRef,
)
from signal_sandbox.auto_validation.results import ValidationResult, ValidationStatus

TIMING_VALIDATOR_ID = "pre_outcome_timing"
TIMING_VALIDATOR_VERSION = "pre_outcome_timing.v1"
FAILED_POST_FACTUM_OR_LATE = "failed_post_factum_or_late"


class TimingOutcomeKind(StrEnum):
    TARGET_TOUCH = "target_touch"
    STOP_TOUCH = "stop_touch"
    RELEVANT_MARKET_MOVE = "relevant_market_move"
    POST_FACTUM_EVIDENCE = "post_factum_evidence"


class TimingOutcomeEvidence(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    market_window_ref_id: str = Field(min_length=1)
    evidence_ref_id: str = Field(min_length=1)
    outcome_kind: TimingOutcomeKind
    observed_at_utc: datetime

    @field_validator("observed_at_utc", mode="before")
    @classmethod
    def _coerce_observed_at(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("observed_at_utc must be datetime or ISO-8601 string")

    @model_validator(mode="after")
    def _validate_timezone(self) -> TimingOutcomeEvidence:
        if self.observed_at_utc.tzinfo is None:
            raise ValueError("observed_at_utc must be timezone-aware")
        return self


def validate_pre_outcome_timing(
    bundle: AutoValidationEvidenceBundle | None,
    *,
    outcome_evidence: Iterable[TimingOutcomeEvidence],
    approved_providers: set[str],
    created_at_utc: datetime | None = None,
) -> ValidationResult:
    """Validate that source evidence precedes market outcome evidence."""

    if bundle is None:
        return _uncertain_result(
            candidate_id="unknown",
            evidence_ref_ids=["missing-bundle"],
            blocker_reasons=["missing_evidence_bundle_or_source_timestamp"],
            deterministic_input_sha256=_input_sha256(None, []),
            created_at_utc=created_at_utc,
        )

    outcomes = list(outcome_evidence)
    source_refs = _source_timestamp_refs(bundle)
    if not source_refs:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=[bundle.source_document_id],
            blocker_reasons=["missing_source_timestamp_evidence_ref"],
            deterministic_input_sha256=_input_sha256(bundle, outcomes),
            created_at_utc=created_at_utc,
        )

    if not outcomes or not bundle.market_window_refs:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=source_refs,
            blocker_reasons=["missing_market_data"],
            deterministic_input_sha256=_input_sha256(bundle, outcomes),
            created_at_utc=created_at_utc,
        )

    windows = {window.ref_id: window for window in bundle.market_window_refs}
    unsupported = [
        outcome.market_window_ref_id
        for outcome in outcomes
        if not _is_approved_window(
            windows.get(outcome.market_window_ref_id), approved_providers
        )
    ]
    if unsupported:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=[
                *source_refs,
                *[item.evidence_ref_id for item in outcomes],
            ],
            blocker_reasons=["unsupported_provider_or_market_window"],
            deterministic_input_sha256=_input_sha256(bundle, outcomes),
            created_at_utc=created_at_utc,
        )

    late_outcomes = [
        outcome
        for outcome in outcomes
        if outcome.observed_at_utc <= bundle.source_timestamp_utc
    ]
    if late_outcomes:
        return ValidationResult(
            validator_id=TIMING_VALIDATOR_ID,
            validator_version=TIMING_VALIDATOR_VERSION,
            candidate_id=bundle.candidate_id,
            status=ValidationStatus.FAILED,
            confidence=Decimal("1"),
            evidence_ref_ids=_timing_evidence_refs(source_refs, outcomes),
            blocker_reasons=[FAILED_POST_FACTUM_OR_LATE],
            deterministic_input_sha256=_input_sha256(bundle, outcomes),
            rationale="target/stop/market move evidence is not after source timestamp",
            created_at_utc=created_at_utc or datetime.now(UTC),
        )

    return ValidationResult(
        validator_id=TIMING_VALIDATOR_ID,
        validator_version=TIMING_VALIDATOR_VERSION,
        candidate_id=bundle.candidate_id,
        status=ValidationStatus.PASSED,
        confidence=Decimal("1"),
        evidence_ref_ids=_timing_evidence_refs(source_refs, outcomes),
        blocker_reasons=[],
        deterministic_input_sha256=_input_sha256(bundle, outcomes),
        rationale="source timestamp precedes approved market outcome evidence",
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
        validator_id=TIMING_VALIDATOR_ID,
        validator_version=TIMING_VALIDATOR_VERSION,
        candidate_id=candidate_id,
        status=ValidationStatus.UNCERTAIN_NEEDS_HUMAN,
        confidence=Decimal("0"),
        evidence_ref_ids=evidence_ref_ids,
        blocker_reasons=blocker_reasons,
        deterministic_input_sha256=deterministic_input_sha256,
        rationale="timing cannot be proven from available public evidence",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _source_timestamp_refs(bundle: AutoValidationEvidenceBundle) -> list[str]:
    refs = [
        ref.ref_id
        for ref in bundle.evidence_refs
        if ref.supports in {"source_timestamp", "timestamp", "source_time"}
    ]
    return sorted(refs)


def _is_approved_window(
    window: MarketWindowRef | None,
    approved_providers: set[str],
) -> bool:
    return window is not None and window.provider in approved_providers


def _timing_evidence_refs(
    source_refs: list[str],
    outcomes: list[TimingOutcomeEvidence],
) -> list[str]:
    refs = {*source_refs}
    for outcome in outcomes:
        refs.add(outcome.evidence_ref_id)
        refs.add(outcome.market_window_ref_id)
    return sorted(refs)


def _input_sha256(
    bundle: AutoValidationEvidenceBundle | None,
    outcomes: list[TimingOutcomeEvidence],
) -> str:
    payload = {
        "bundle_sha256": bundle.bundle_sha256() if bundle is not None else None,
        "outcome_evidence": [
            outcome.model_dump(mode="json", by_alias=False, exclude_none=True)
            for outcome in outcomes
        ],
        "validator_id": TIMING_VALIDATOR_ID,
        "validator_version": TIMING_VALIDATOR_VERSION,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
