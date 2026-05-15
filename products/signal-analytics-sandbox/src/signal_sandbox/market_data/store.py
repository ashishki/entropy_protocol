"""Immutable local market-data snapshot store."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.prices.base import canonical_ohlcv_bytes

DATA_FILENAME = "ohlcv.parquet"
METADATA_FILENAME = "metadata.json"


class MarketDataStoreError(Exception):
    """Base exception for market-data store failures."""


class SnapshotAlreadyExists(MarketDataStoreError):
    """Raised when a different snapshot is written to an existing snapshot ID."""


class SnapshotChecksumMismatch(MarketDataStoreError):
    """Raised when stored bytes do not match metadata checksum."""


class MarketDataSnapshotMetadata(BaseModel):
    model_config = ConfigDict(strict=True)

    snapshot_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    canonical_asset_id: str = Field(min_length=1)
    provider_symbol: str = Field(min_length=1)
    timeframe: str = Field(min_length=1)
    source_range_start_utc: datetime
    source_range_end_utc: datetime
    captured_at_utc: datetime
    data_sha256: str = Field(min_length=64, max_length=64)
    license: str = Field(min_length=1)
    provenance: str = Field(min_length=1)

    @field_validator(
        "source_range_start_utc",
        "source_range_end_utc",
        "captured_at_utc",
        mode="before",
    )
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")


class MarketDataSnapshot(BaseModel):
    model_config = ConfigDict(strict=True)

    metadata: MarketDataSnapshotMetadata
    data_bytes: bytes

    @model_validator(mode="after")
    def _validate_checksum(self) -> MarketDataSnapshot:
        actual = hashlib.sha256(self.data_bytes).hexdigest()
        if actual != self.metadata.data_sha256:
            raise SnapshotChecksumMismatch("market-data snapshot sha256 mismatch")
        return self


class MarketDataStoreProtocol(Protocol):
    def write_snapshot(self, snapshot: MarketDataSnapshot) -> Path:
        """Persist a snapshot immutably."""
        ...

    def load_snapshot(self, snapshot_id: str) -> MarketDataSnapshot:
        """Load a snapshot and verify checksum."""
        ...

    def list_snapshots(self) -> list[MarketDataSnapshotMetadata]:
        """Return snapshot metadata sorted by snapshot ID."""
        ...


class LocalMarketDataStore:
    def __init__(self, workspace: Path):
        self._root = workspace / "market_data" / "snapshots"

    def write_snapshot(self, snapshot: MarketDataSnapshot) -> Path:
        snapshot_dir = self._snapshot_dir(snapshot.metadata.snapshot_id)
        metadata_bytes = _metadata_bytes(snapshot.metadata)
        data_path = snapshot_dir / DATA_FILENAME
        metadata_path = snapshot_dir / METADATA_FILENAME

        if snapshot_dir.exists():
            if (
                data_path.is_file()
                and metadata_path.is_file()
                and data_path.read_bytes() == snapshot.data_bytes
                and metadata_path.read_bytes() == metadata_bytes
            ):
                return snapshot_dir
            raise SnapshotAlreadyExists(
                f"market-data snapshot_id already exists: "
                f"{snapshot.metadata.snapshot_id}"
            )

        snapshot_dir.mkdir(parents=True)
        data_path.write_bytes(snapshot.data_bytes)
        metadata_path.write_bytes(metadata_bytes)
        return snapshot_dir

    def load_snapshot(self, snapshot_id: str) -> MarketDataSnapshot:
        snapshot_dir = self._snapshot_dir(snapshot_id)
        data_bytes = (snapshot_dir / DATA_FILENAME).read_bytes()
        metadata = MarketDataSnapshotMetadata.model_validate_json(
            (snapshot_dir / METADATA_FILENAME).read_text(encoding="utf-8")
        )
        return MarketDataSnapshot(metadata=metadata, data_bytes=data_bytes)

    def list_snapshots(self) -> list[MarketDataSnapshotMetadata]:
        if not self._root.exists():
            return []
        metadata = [
            MarketDataSnapshotMetadata.model_validate_json(
                (snapshot_dir / METADATA_FILENAME).read_text(encoding="utf-8")
            )
            for snapshot_dir in sorted(self._root.iterdir())
            if snapshot_dir.is_dir() and (snapshot_dir / METADATA_FILENAME).is_file()
        ]
        return sorted(metadata, key=lambda item: item.snapshot_id)

    def _snapshot_dir(self, snapshot_id: str) -> Path:
        if not snapshot_id or Path(snapshot_id).name != snapshot_id:
            raise ValueError("snapshot_id must be a single path segment")
        return self._root / snapshot_id


def make_operator_file_snapshot(
    *,
    snapshot_id: str,
    canonical_asset_id: str,
    provider_symbol: str,
    timeframe: str,
    source_range_start_utc: datetime,
    source_range_end_utc: datetime,
    captured_at_utc: datetime,
    rows: list[dict[str, Any]],
    license: str,
    provenance: str,
) -> MarketDataSnapshot:
    data_bytes = canonical_ohlcv_bytes(rows)
    metadata = MarketDataSnapshotMetadata(
        snapshot_id=snapshot_id,
        provider="operator_file",
        canonical_asset_id=canonical_asset_id,
        provider_symbol=provider_symbol,
        timeframe=timeframe,
        source_range_start_utc=source_range_start_utc,
        source_range_end_utc=source_range_end_utc,
        captured_at_utc=captured_at_utc,
        data_sha256=hashlib.sha256(data_bytes).hexdigest(),
        license=license,
        provenance=provenance,
    )
    return MarketDataSnapshot(metadata=metadata, data_bytes=data_bytes)


def _metadata_bytes(metadata: MarketDataSnapshotMetadata) -> bytes:
    return json.dumps(
        metadata.model_dump(mode="json"),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
