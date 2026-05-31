"""Portable product proof receipt contract."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

PRODUCT_PROOF_RECEIPT_SCHEMA_VERSION = "entropy_core.product_receipt.v1"
PRODUCT_PROOF_RECEIPT_STATUSES = ("passed", "needs_review", "failed")
PRODUCT_PROOF_RECEIPT_LEVELS = (
    "receipt_compatible",
    "schema_compatible",
    "evidence_lookup_compatible",
)
SHA256_HEX_LENGTH = 64


class ProductProofReceiptViolation(ValueError):
    """Raised when a product proof receipt violates the portable contract."""


class ProductProofEvidenceRef(BaseModel):
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


class ProductProofReceipt(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    schema_version: Literal["entropy_core.product_receipt.v1"] = (
        PRODUCT_PROOF_RECEIPT_SCHEMA_VERSION
    )
    product_id: str = Field(min_length=1)
    receipt_type: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    artifact_sha256: str = Field(min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH)
    generated_at: datetime
    evidence_refs: list[ProductProofEvidenceRef] = Field(min_length=1)
    verifier_status: Literal["passed", "needs_review", "failed"]
    verifier_notes: tuple[str, ...] = ()
    entropy_core_level: Literal[
        "receipt_compatible",
        "schema_compatible",
        "evidence_lookup_compatible",
    ]

    @field_validator("artifact_sha256")
    @classmethod
    def artifact_hash_must_be_sha256(cls, value: str) -> str:
        if any(char not in "0123456789abcdef" for char in value):
            raise ValueError("artifact_sha256 must be lowercase hexadecimal")
        return value

    @model_validator(mode="after")
    def non_passed_status_requires_notes(self) -> ProductProofReceipt:
        if self.verifier_status != "passed" and not self.verifier_notes:
            raise ValueError("non-passed product proof receipts require verifier_notes")
        return self

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", exclude_none=True)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

    def receipt_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def validate_product_proof_receipt(payload: object) -> ProductProofReceipt:
    try:
        return ProductProofReceipt.model_validate(payload)
    except ValueError as exc:
        raise ProductProofReceiptViolation(str(exc)) from exc
