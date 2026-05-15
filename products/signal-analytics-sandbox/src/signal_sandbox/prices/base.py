"""Price-data provider interface and snapshot contract."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from datetime import datetime
from io import BytesIO
from typing import Any

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PriceDataError(Exception):
    """Base exception for price-data failures."""


class SnapshotChecksumMismatch(PriceDataError):
    """Raised when snapshot bytes do not match the declared SHA-256."""


OHLCV_COLUMNS = [
    "asset",
    "timestamp_utc",
    "open",
    "high",
    "low",
    "close",
    "volume",
]

OHLCV_SCHEMA = {
    "asset": pl.String,
    "timestamp_utc": pl.String,
    "open": pl.String,
    "high": pl.String,
    "low": pl.String,
    "close": pl.String,
    "volume": pl.String,
}


class PriceSnapshot(BaseModel):
    model_config = ConfigDict(strict=True)

    provider_id: str = Field(min_length=1)
    provider_status: str = Field(min_length=1)
    as_of_utc: datetime
    range_start_utc: datetime
    range_end_utc: datetime
    assets: list[str] = Field(min_length=1)
    ohlcv_bytes: bytes
    sha256: str = Field(min_length=64, max_length=64)

    @field_validator("as_of_utc", "range_start_utc", "range_end_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")

    @model_validator(mode="after")
    def _validate_checksum(self) -> PriceSnapshot:
        actual = hashlib.sha256(self.ohlcv_bytes).hexdigest()
        if actual != self.sha256:
            raise SnapshotChecksumMismatch("snapshot sha256 mismatch")
        return self

    def canonical_bytes(self) -> bytes:
        return self.ohlcv_bytes


class PriceDataProvider(ABC):
    @abstractmethod
    def snapshot(
        self,
        assets: list[str],
        range_start_utc: datetime,
        range_end_utc: datetime,
        as_of_utc: datetime,
    ) -> PriceSnapshot:
        """Return a deterministic snapshot for the requested range."""


def canonical_ohlcv_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    normalized_rows = [_normalize_ohlcv_row(row) for row in rows]
    normalized_rows.sort(key=lambda row: (row["asset"], row["timestamp_utc"]))
    frame = pl.DataFrame(normalized_rows, schema=OHLCV_SCHEMA)

    buffer = BytesIO()
    frame.select(OHLCV_COLUMNS).write_parquet(
        buffer,
        compression="zstd",
        statistics=False,
    )
    return buffer.getvalue()


def make_price_snapshot(
    *,
    provider_id: str,
    provider_status: str,
    as_of_utc: datetime,
    range_start_utc: datetime,
    range_end_utc: datetime,
    assets: list[str],
    rows: Sequence[Mapping[str, Any]],
) -> PriceSnapshot:
    ohlcv_bytes = canonical_ohlcv_bytes(rows)
    return PriceSnapshot(
        provider_id=provider_id,
        provider_status=provider_status,
        as_of_utc=as_of_utc,
        range_start_utc=range_start_utc,
        range_end_utc=range_end_utc,
        assets=sorted(assets),
        ohlcv_bytes=ohlcv_bytes,
        sha256=hashlib.sha256(ohlcv_bytes).hexdigest(),
    )


def _normalize_ohlcv_row(row: Mapping[str, Any]) -> dict[str, str]:
    return {column: _value_to_string(row[column]) for column in OHLCV_COLUMNS}


def _value_to_string(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)
