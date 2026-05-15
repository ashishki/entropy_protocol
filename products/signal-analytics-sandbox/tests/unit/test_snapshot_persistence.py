from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from signal_sandbox.prices.base import SnapshotChecksumMismatch, make_price_snapshot
from signal_sandbox.prices.snapshot import (
    SnapshotAlreadyExists,
    load_snapshot,
    save_snapshot,
)


def make_snapshot(close: str = "105"):
    return make_price_snapshot(
        provider_id="operator-file",
        provider_status="operator_supplied",
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        assets=["BTC"],
        rows=[
            {
                "asset": "BTC",
                "timestamp_utc": "2026-05-07T10:00:00+00:00",
                "open": "90",
                "high": "110",
                "low": "89",
                "close": close,
                "volume": "10",
            }
        ],
    )


def test_metadata_sha_matches_file(tmp_path: Path) -> None:
    snapshot = make_snapshot()

    snapshot_dir = save_snapshot(snapshot, tmp_path)

    ohlcv_bytes = (snapshot_dir / "ohlcv.parquet").read_bytes()
    metadata = json.loads((snapshot_dir / "metadata.json").read_text())
    assert metadata["sha256"] == hashlib.sha256(ohlcv_bytes).hexdigest()
    assert metadata["provider_id"] == "operator-file"
    assert metadata["provider_status"] == "operator_supplied"
    assert metadata["assets"] == ["BTC"]


def test_idempotent_and_immutable(tmp_path: Path) -> None:
    first = make_snapshot(close="105")
    second = make_snapshot(close="106")

    snapshot_dir = save_snapshot(first, tmp_path, snapshot_id="fixed-id")
    first_ohlcv_bytes = (snapshot_dir / "ohlcv.parquet").read_bytes()
    first_metadata_bytes = (snapshot_dir / "metadata.json").read_bytes()

    same_dir = save_snapshot(first, tmp_path, snapshot_id="fixed-id")

    assert same_dir == snapshot_dir
    assert (snapshot_dir / "ohlcv.parquet").read_bytes() == first_ohlcv_bytes
    assert (snapshot_dir / "metadata.json").read_bytes() == first_metadata_bytes

    with pytest.raises(SnapshotAlreadyExists):
        save_snapshot(second, tmp_path, snapshot_id="fixed-id")


def test_load_verifies_checksum(tmp_path: Path) -> None:
    snapshot = make_snapshot()
    snapshot_dir = save_snapshot(snapshot, tmp_path, snapshot_id="fixed-id")

    loaded = load_snapshot(tmp_path, "fixed-id")
    assert loaded == snapshot

    metadata_path = snapshot_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["sha256"] = "0" * 64
    metadata_path.write_text(json.dumps(metadata, sort_keys=True))

    with pytest.raises(SnapshotChecksumMismatch):
        load_snapshot(tmp_path, "fixed-id")
