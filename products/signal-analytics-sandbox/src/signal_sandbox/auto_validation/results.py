"""Validator result and audit-log schemas for auto-validation."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.auto_validation.evidence import SHA256_HEX_LENGTH

RESULT_SCHEMA_VERSION = "auto_validation_result.v1"
AUDIT_LOG_SCHEMA_VERSION = "auto_validation_audit_log.v1"


class ValidationStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    UNCERTAIN_NEEDS_HUMAN = "uncertain_needs_human"
    EXCLUDED_PROVIDER_GAP = "excluded_provider_gap"
    BLOCKED_CUSTOMER_FACING = "blocked_customer_facing"


class ValidationResult(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    validator_id: str = Field(min_length=1)
    validator_version: str = Field(min_length=1)
    candidate_id: str = Field(min_length=1)
    status: ValidationStatus
    confidence: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    evidence_ref_ids: list[str] = Field(min_length=1)
    blocker_reasons: list[str] = Field(default_factory=list)
    deterministic_input_sha256: str = Field(
        min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    rationale: str = Field(min_length=1)
    created_at_utc: datetime
    schema_version: str = Field(default=RESULT_SCHEMA_VERSION, min_length=1)

    @field_validator("created_at_utc", mode="before")
    @classmethod
    def _coerce_created_at(cls, value: object) -> datetime:
        return _coerce_datetime(value)

    @field_validator("deterministic_input_sha256")
    @classmethod
    def _validate_input_sha256(cls, value: str) -> str:
        return _validate_sha256(value, "deterministic_input_sha256")

    @model_validator(mode="after")
    def _validate_result_contract(self) -> Self:
        if any(not ref_id for ref_id in self.evidence_ref_ids):
            raise ValueError("evidence_ref_ids must contain non-empty refs")
        if self.status != ValidationStatus.PASSED and not self.blocker_reasons:
            raise ValueError("non-passed validator results require blocker_reasons")
        if any(not reason for reason in self.blocker_reasons):
            raise ValueError("blocker_reasons must contain non-empty reasons")
        return self


class ValidationAuditLog(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    audit_id: str = Field(min_length=1)
    candidate_id: str = Field(min_length=1)
    evidence_bundle_sha256: str = Field(
        min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    results: list[ValidationResult] = Field(min_length=1)
    created_at_utc: datetime
    schema_version: str = Field(default=AUDIT_LOG_SCHEMA_VERSION, min_length=1)

    @field_validator("created_at_utc", mode="before")
    @classmethod
    def _coerce_created_at(cls, value: object) -> datetime:
        return _coerce_datetime(value)

    @field_validator("evidence_bundle_sha256")
    @classmethod
    def _validate_bundle_sha256(cls, value: str) -> str:
        return _validate_sha256(value, "evidence_bundle_sha256")

    @model_validator(mode="after")
    def _validate_audit_contract(self) -> Self:
        mismatched = [
            result.validator_id
            for result in self.results
            if result.candidate_id != self.candidate_id
        ]
        if mismatched:
            raise ValueError(
                "all validation results must match audit candidate_id: "
                + ", ".join(mismatched)
            )

        validator_keys = [
            (result.validator_id, result.validator_version) for result in self.results
        ]
        if len(set(validator_keys)) != len(validator_keys):
            raise ValueError("audit log cannot contain duplicate validator results")
        return self

    def evidence_ref_ids(self) -> list[str]:
        refs = {ref_id for result in self.results for ref_id in result.evidence_ref_ids}
        return sorted(refs)

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", by_alias=False, exclude_none=True)
        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    def canonical_json_bytes(self) -> bytes:
        return self.canonical_json().encode("utf-8")

    def audit_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json_bytes()).hexdigest()


def _coerce_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError("timestamp fields must be datetime or ISO-8601 strings")


def _validate_sha256(value: str, field_name: str) -> str:
    if any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{field_name} must be lowercase hexadecimal")
    return value
