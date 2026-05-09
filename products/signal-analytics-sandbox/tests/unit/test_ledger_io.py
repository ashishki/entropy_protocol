from __future__ import annotations

import hashlib
from decimal import Decimal
from pathlib import Path

import polars as pl
import pytest

from signal_sandbox.ledger.io import (
    CANONICAL_COLUMNS,
    DuplicateSignalRecord,
    read_ledger,
    write_ledger,
)
from signal_sandbox.ledger.record import SignalRecord


def make_record(**overrides: object) -> SignalRecord:
    data: dict[str, object] = {
        "source_id": "bablos79",
        "capture_id": "cap-001",
        "evidence_url": "https://t.me/bablos79/1",
        "text_sha256": "a" * 64,
        "capture_timestamp_utc": "2026-05-07T09:00:00Z",
        "extracted_timestamp_utc": "2026-05-07T10:00:00Z",
        "asset_symbol": "BTC",
        "direction": "long",
        "entry": Decimal("100"),
        "stop": Decimal("95"),
        "target": Decimal("110"),
        "confidence_flags": [],
        "ambiguity_flags": [],
        "extraction_metadata": {"adapter_id": "manual/v1"},
    }
    data.update(overrides)
    return SignalRecord.model_validate(data)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_write_idempotent(tmp_path: Path) -> None:
    records = [
        make_record(
            capture_id="cap-002", extracted_timestamp_utc="2026-05-07T11:00:00Z"
        ),
        make_record(capture_id="cap-001"),
    ]
    first = tmp_path / "first.parquet"
    second = tmp_path / "second.parquet"

    write_ledger(records, first)
    write_ledger(list(reversed(records)), second)

    assert sha256(first) == sha256(second)
    assert pl.read_parquet(first).columns == CANONICAL_COLUMNS


def test_round_trip_byte_identical(tmp_path: Path) -> None:
    first = tmp_path / "first.parquet"
    second = tmp_path / "second.parquet"

    write_ledger([make_record()], first)
    write_ledger(read_ledger(first), second)

    assert sha256(first) == sha256(second)


def test_duplicate_handling(tmp_path: Path) -> None:
    records = [
        make_record(capture_id="cap-001"),
        make_record(capture_id="cap-002"),
    ]

    with pytest.raises(DuplicateSignalRecord):
        write_ledger(records, tmp_path / "blocked.parquet")

    forced_path = tmp_path / "forced.parquet"
    write_ledger(records, forced_path, force_duplicate=True)

    loaded = read_ledger(forced_path)
    assert [record.ambiguity_flags for record in loaded] == [
        ["duplicate_dedup_key"],
        ["duplicate_dedup_key"],
    ]


def test_empty_ledger_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "empty.parquet"

    write_ledger([], path)

    frame = pl.read_parquet(path)
    assert frame.columns == CANONICAL_COLUMNS
    assert frame.height == 0
    assert read_ledger(path) == []
