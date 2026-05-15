"""Price snapshot persistence and provenance metadata."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from signal_sandbox.prices.base import (
    PriceDataError,
    PriceSnapshot,
    SnapshotChecksumMismatch,
)

OhlcvFilename = "ohlcv.parquet"
MetadataFilename = "metadata.json"


class SnapshotAlreadyExists(PriceDataError):
    """Raised when a different snapshot is saved to an existing snapshot path."""


def save_snapshot(
    snapshot: PriceSnapshot,
    workspace: Path,
    *,
    snapshot_id: str | None = None,
) -> Path:
    """Persist a snapshot and deterministic provenance metadata."""

    effective_snapshot_id = snapshot_id or snapshot.sha256
    snapshot_dir = _snapshot_dir(workspace, effective_snapshot_id)
    metadata_bytes = _metadata_bytes(snapshot, effective_snapshot_id)
    ohlcv_path = snapshot_dir / OhlcvFilename
    metadata_path = snapshot_dir / MetadataFilename

    if snapshot_dir.exists():
        if (
            ohlcv_path.is_file()
            and metadata_path.is_file()
            and ohlcv_path.read_bytes() == snapshot.ohlcv_bytes
            and metadata_path.read_bytes() == metadata_bytes
        ):
            return snapshot_dir
        raise SnapshotAlreadyExists(
            f"snapshot_id already exists: {effective_snapshot_id}"
        )

    snapshot_dir.mkdir(parents=True)
    ohlcv_path.write_bytes(snapshot.ohlcv_bytes)
    metadata_path.write_bytes(metadata_bytes)
    return snapshot_dir


def load_snapshot(workspace: Path, snapshot_id: str) -> PriceSnapshot:
    """Load a persisted snapshot and verify its Parquet payload checksum."""

    snapshot_dir = _snapshot_dir(workspace, snapshot_id)
    ohlcv_bytes = (snapshot_dir / OhlcvFilename).read_bytes()
    metadata = json.loads((snapshot_dir / MetadataFilename).read_text())
    expected_sha = str(metadata["sha256"])
    actual_sha = hashlib.sha256(ohlcv_bytes).hexdigest()
    if actual_sha != expected_sha:
        raise SnapshotChecksumMismatch("persisted snapshot sha256 mismatch")

    return PriceSnapshot.model_validate(
        {
            "provider_id": metadata["provider_id"],
            "provider_status": metadata["provider_status"],
            "as_of_utc": metadata["as_of_utc"],
            "range_start_utc": metadata["range_start_utc"],
            "range_end_utc": metadata["range_end_utc"],
            "assets": metadata["assets"],
            "ohlcv_bytes": ohlcv_bytes,
            "sha256": expected_sha,
        }
    )


def _snapshot_dir(workspace: Path, snapshot_id: str) -> Path:
    if not snapshot_id or Path(snapshot_id).name != snapshot_id:
        raise ValueError("snapshot_id must be a single path segment")
    return workspace / "snapshots" / snapshot_id


def _metadata_bytes(snapshot: PriceSnapshot, snapshot_id: str) -> bytes:
    metadata: dict[str, Any] = {
        "assets": snapshot.assets,
        "as_of_utc": snapshot.as_of_utc.isoformat(),
        "provider_id": snapshot.provider_id,
        "provider_status": snapshot.provider_status,
        "range_end_utc": snapshot.range_end_utc.isoformat(),
        "range_start_utc": snapshot.range_start_utc.isoformat(),
        "sha256": snapshot.sha256,
        "snapshot_id": snapshot_id,
    }
    return json.dumps(
        metadata,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
