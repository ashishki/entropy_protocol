"""Machine-readable evidence bundles for auto-validation candidates."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.sources.private_patterns import is_private_source_url

PROVENANCE_VERSION = "auto_validation_evidence.v1"
SHA256_HEX_LENGTH = 64


class SourceClass(StrEnum):
    PUBLIC = "public"
    OPERATOR_AUTHORIZED_PUBLIC = "operator_authorized_public"


class TradeDirection(StrEnum):
    LONG = "long"
    SHORT = "short"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class EvidenceRef(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    ref_id: str = Field(min_length=1)
    ref_type: str = Field(
        pattern=(
            "^(source_document|capture|text_span|media|ocr|transcript|"
            "chart_region|model_span|market_window)$"
        )
    )
    supports: str = Field(min_length=1)
    checksum_sha256: str | None = Field(
        default=None, min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )

    @field_validator("checksum_sha256")
    @classmethod
    def _validate_optional_sha256(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _validate_sha256(value, "checksum_sha256")


class ModelExtractionSpan(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    span_id: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    field: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    evidence_ref_ids: list[str] = Field(min_length=1)
    confidence: Decimal | None = Field(default=None, ge=Decimal("0"), le=Decimal("1"))


class MarketWindowRef(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    ref_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    window_start_utc: datetime
    window_end_utc: datetime
    data_sha256: str = Field(min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH)

    @field_validator("window_start_utc", "window_end_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        return _coerce_datetime(value)

    @field_validator("data_sha256")
    @classmethod
    def _validate_data_sha256(cls, value: str) -> str:
        return _validate_sha256(value, "data_sha256")

    @model_validator(mode="after")
    def _validate_window_order(self) -> Self:
        if self.window_end_utc <= self.window_start_utc:
            raise ValueError("window_end_utc must be after window_start_utc")
        return self


class ExtractedSetupFields(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    asset: str | None = Field(default=None, min_length=1)
    direction: TradeDirection = TradeDirection.UNKNOWN
    entry: Decimal | None = None
    stop: Decimal | None = None
    targets: list[Decimal] = Field(default_factory=list)
    horizon: str | None = Field(default=None, min_length=1)
    evidence_ref_ids_by_field: dict[str, list[str]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_field_refs(self) -> Self:
        required_fields: list[str] = []
        if self.asset is not None:
            required_fields.append("asset")
        if self.direction != TradeDirection.UNKNOWN:
            required_fields.append("direction")
        if self.entry is not None:
            required_fields.append("entry")
        if self.stop is not None:
            required_fields.append("stop")
        if self.targets:
            required_fields.append("targets")
        if self.horizon is not None:
            required_fields.append("horizon")

        missing = [
            field
            for field in required_fields
            if not self.evidence_ref_ids_by_field.get(field)
        ]
        if missing:
            raise ValueError(
                "extracted fields require evidence refs: " + ", ".join(missing)
            )

        for field, ref_ids in self.evidence_ref_ids_by_field.items():
            if not field or not ref_ids or any(not ref_id for ref_id in ref_ids):
                raise ValueError("evidence_ref_ids_by_field values must be non-empty")
        return self


class AutoValidationEvidenceBundle(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    candidate_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    source_timestamp_utc: datetime
    source_document_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_class: SourceClass
    text_ref_id: str | None = Field(default=None, min_length=1)
    text_sha256: str | None = Field(
        default=None, min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    media_ref_id: str | None = Field(default=None, min_length=1)
    media_sha256: str | None = Field(
        default=None, min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    ocr_ref_ids: list[str] = Field(default_factory=list)
    transcript_ref_ids: list[str] = Field(default_factory=list)
    chart_region_ref_ids: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)
    extracted_fields: ExtractedSetupFields
    model_extraction_spans: list[ModelExtractionSpan] = Field(default_factory=list)
    market_window_refs: list[MarketWindowRef] = Field(default_factory=list)
    provenance_version: str = Field(default=PROVENANCE_VERSION, min_length=1)

    @field_validator("source_timestamp_utc", mode="before")
    @classmethod
    def _coerce_source_timestamp(cls, value: object) -> datetime:
        return _coerce_datetime(value)

    @field_validator("text_sha256", "media_sha256")
    @classmethod
    def _validate_optional_bundle_sha256(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _validate_sha256(value, "bundle checksum")

    @model_validator(mode="after")
    def _validate_bundle_contract(self) -> Self:
        if is_private_source_url(self.source_url):
            raise ValueError("source_url must not be private or restricted")

        has_text = self.text_ref_id is not None and self.text_sha256 is not None
        has_media = self.media_ref_id is not None and self.media_sha256 is not None
        if not has_text and not has_media:
            raise ValueError("bundle requires a text or media ref with sha256")

        ref_ids = {ref.ref_id for ref in self.evidence_refs}
        missing_refs = [
            ref_id
            for refs in self.extracted_fields.evidence_ref_ids_by_field.values()
            for ref_id in refs
            if ref_id not in ref_ids
        ]
        if missing_refs:
            raise ValueError(
                "extracted field evidence refs missing from bundle: "
                + ", ".join(sorted(set(missing_refs)))
            )

        span_missing_refs = [
            ref_id
            for span in self.model_extraction_spans
            for ref_id in span.evidence_ref_ids
            if ref_id not in ref_ids
        ]
        if span_missing_refs:
            raise ValueError(
                "model span evidence refs missing from bundle: "
                + ", ".join(sorted(set(span_missing_refs)))
            )
        return self

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", by_alias=False, exclude_none=True)
        return json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )

    def canonical_json_bytes(self) -> bytes:
        return self.canonical_json().encode("utf-8")

    def bundle_sha256(self) -> str:
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
