"""Signal record schema and canonical dedup-key computation.

Dedup key formula:
SHA-256 hex of canonical JSON with sorted keys and compact separators over:
`source_id`, `extracted_timestamp_utc`, `asset_symbol`, `direction`, `entry`,
`stop`, and `target`.

The formula intentionally preserves whitespace and case in `asset_symbol`.
Normalizing symbols would hide duplicate/ambiguity signals that the ledger must
surface explicitly.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Direction(StrEnum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"
    UNKNOWN = "unknown"


class SignalRecord(BaseModel):
    model_config = ConfigDict(strict=True)

    source_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)
    capture_timestamp_utc: datetime
    extracted_timestamp_utc: datetime
    asset_symbol: str = Field(min_length=1)
    direction: Direction
    entry: Decimal | None = None
    stop: Decimal | None = None
    target: Decimal | None = None
    confidence_flags: list[str] = Field(default_factory=list)
    ambiguity_flags: list[str] = Field(default_factory=list)
    extraction_metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("direction", mode="before")
    @classmethod
    def _coerce_direction(cls, value: object) -> Direction:
        if isinstance(value, Direction):
            return value
        if isinstance(value, str):
            return Direction(value)
        raise ValueError("direction must be a Direction or string")

    @field_validator("capture_timestamp_utc", "extracted_timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")

    def is_evaluable(self) -> bool:
        return not self.ambiguity_flags and self.direction in {
            Direction.LONG,
            Direction.SHORT,
        }


def _decimal_to_json(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value)


def canonical_dedup_payload(record: SignalRecord) -> dict[str, object]:
    return {
        "asset_symbol": record.asset_symbol,
        "direction": record.direction.value,
        "entry": _decimal_to_json(record.entry),
        "extracted_timestamp_utc": record.extracted_timestamp_utc.isoformat(),
        "source_id": record.source_id,
        "stop": _decimal_to_json(record.stop),
        "target": _decimal_to_json(record.target),
    }


def compute_dedup_key(record: SignalRecord) -> str:
    canonical_json = json.dumps(
        canonical_dedup_payload(record),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
