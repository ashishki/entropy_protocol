"""Entropy Core-compatible receipts for auto-validation audits."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.auto_validation.evidence import (
    SHA256_HEX_LENGTH,
    AutoValidationEvidenceBundle,
)
from signal_sandbox.auto_validation.results import ValidationAuditLog, ValidationStatus

PROOF_RECEIPT_SCHEMA_VERSION = "entropy_core.product_receipt.v1"
PRODUCT_ID = "signal-analytics-sandbox"


class SignalProofEvidenceRef(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    ref_id: str = Field(min_length=1)
    ref_type: str = Field(min_length=1)
    supports: str = Field(min_length=1)
    checksum_sha256: str | None = Field(
        default=None, min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )

    @field_validator("checksum_sha256")
    @classmethod
    def checksum_must_be_sha256(cls, value: str | None) -> str | None:
        if value is not None and any(char not in "0123456789abcdef" for char in value):
            raise ValueError("checksum_sha256 must be lowercase hexadecimal")
        return value


class SignalAutoValidationProofReceipt(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    type: Literal["signal_auto_validation_receipt"] = "signal_auto_validation_receipt"
    schema_version: Literal["entropy_core.product_receipt.v1"] = (
        PROOF_RECEIPT_SCHEMA_VERSION
    )
    product_id: Literal["signal-analytics-sandbox"] = PRODUCT_ID
    candidate_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    evidence_bundle_sha256: str = Field(
        min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    audit_sha256: str = Field(
        min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    evidence_refs: list[SignalProofEvidenceRef] = Field(min_length=1)
    validator_ids: list[str] = Field(min_length=1)
    verifier_status: Literal["passed", "needs_review", "failed"]
    verifier_notes: list[str] = Field(default_factory=list)
    generated_at_utc: datetime
    entropy_core_level: Literal["evidence_lookup_compatible"] = (
        "evidence_lookup_compatible"
    )

    @field_validator("evidence_bundle_sha256", "audit_sha256")
    @classmethod
    def hash_fields_must_be_sha256(cls, value: str) -> str:
        if any(char not in "0123456789abcdef" for char in value):
            raise ValueError("hash fields must be lowercase hexadecimal")
        return value

    @field_validator("generated_at_utc", mode="before")
    @classmethod
    def coerce_generated_at_utc(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("generated_at_utc must be datetime or ISO-8601 string")

    @model_validator(mode="after")
    def non_passed_status_requires_notes(self) -> SignalAutoValidationProofReceipt:
        if self.verifier_status != "passed" and not self.verifier_notes:
            raise ValueError("non-passed receipts require verifier_notes")
        return self

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", exclude_none=True)
        return json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )

    def receipt_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def build_signal_auto_validation_receipt(
    *,
    bundle: AutoValidationEvidenceBundle,
    audit: ValidationAuditLog,
    generated_at_utc: datetime | None = None,
) -> SignalAutoValidationProofReceipt:
    bundle_sha256 = bundle.bundle_sha256()
    if audit.candidate_id != bundle.candidate_id:
        raise ValueError("audit candidate_id must match evidence bundle candidate_id")
    if audit.evidence_bundle_sha256 != bundle_sha256:
        raise ValueError("audit evidence_bundle_sha256 must match evidence bundle hash")

    bundle_ref_ids = {ref.ref_id for ref in bundle.evidence_refs}
    market_ref_ids = {ref.ref_id for ref in bundle.market_window_refs}
    missing_audit_refs = [
        ref_id
        for ref_id in audit.evidence_ref_ids()
        if ref_id not in bundle_ref_ids and ref_id not in market_ref_ids
    ]
    if missing_audit_refs:
        raise ValueError(
            "audit evidence refs missing from bundle: " + ", ".join(missing_audit_refs)
        )

    evidence_refs = [
        SignalProofEvidenceRef(
            ref_id=ref.ref_id,
            ref_type=ref.ref_type,
            supports=ref.supports,
            checksum_sha256=ref.checksum_sha256,
        )
        for ref in bundle.evidence_refs
    ]
    evidence_refs.extend(
        SignalProofEvidenceRef(
            ref_id=ref.ref_id,
            ref_type="market_window",
            supports=f"{ref.provider}:{ref.symbol}",
            checksum_sha256=ref.data_sha256,
        )
        for ref in bundle.market_window_refs
    )

    verifier_status, notes = _audit_status(audit)
    return SignalAutoValidationProofReceipt(
        candidate_id=bundle.candidate_id,
        source_id=bundle.source_id,
        source_url=bundle.source_url,
        evidence_bundle_sha256=bundle_sha256,
        audit_sha256=audit.audit_sha256(),
        evidence_refs=evidence_refs,
        validator_ids=[result.validator_id for result in audit.results],
        verifier_status=verifier_status,
        verifier_notes=notes,
        generated_at_utc=generated_at_utc or datetime.now(UTC),
    )


def _audit_status(
    audit: ValidationAuditLog,
) -> tuple[Literal["passed", "needs_review", "failed"], list[str]]:
    statuses = {result.status for result in audit.results}
    if statuses == {ValidationStatus.PASSED}:
        return "passed", []
    blockers = [reason for result in audit.results for reason in result.blocker_reasons]
    if (
        ValidationStatus.FAILED in statuses
        or ValidationStatus.BLOCKED_CUSTOMER_FACING in statuses
    ):
        return "failed", blockers
    return "needs_review", blockers or ["one or more validators did not pass"]
