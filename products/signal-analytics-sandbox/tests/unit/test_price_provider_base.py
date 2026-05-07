from __future__ import annotations

import hashlib
from datetime import UTC, datetime

import pytest

from signal_sandbox.prices.base import (
    PriceDataProvider,
    PriceSnapshot,
    SnapshotChecksumMismatch,
    canonical_ohlcv_bytes,
    make_price_snapshot,
)


def ohlcv_rows() -> list[dict[str, object]]:
    return [
        {
            "asset": "BTC",
            "timestamp_utc": "2026-05-07T10:01:00+00:00",
            "open": "100",
            "high": "110",
            "low": "95",
            "close": "105",
            "volume": "12.5",
        },
        {
            "asset": "BTC",
            "timestamp_utc": "2026-05-07T10:00:00+00:00",
            "open": "90",
            "high": "101",
            "low": "89",
            "close": "100",
            "volume": "10",
        },
    ]


def test_abstract_method_required() -> None:
    missing_snapshot = type("MissingSnapshot", (PriceDataProvider,), {})

    with pytest.raises(TypeError):
        missing_snapshot()


def test_snapshot_checksum_validated() -> None:
    bytes_ = canonical_ohlcv_bytes(ohlcv_rows())

    snapshot = PriceSnapshot.model_validate(
        {
            "provider_id": "operator-file",
            "provider_status": "operator_supplied",
            "as_of_utc": "2026-05-07T12:00:00Z",
            "range_start_utc": "2026-05-07T10:00:00Z",
            "range_end_utc": "2026-05-07T11:00:00Z",
            "assets": ["BTC"],
            "ohlcv_bytes": bytes_,
            "sha256": hashlib.sha256(bytes_).hexdigest(),
        }
    )

    assert snapshot.canonical_bytes() == bytes_

    with pytest.raises(SnapshotChecksumMismatch):
        PriceSnapshot.model_validate(
            {
                "provider_id": "operator-file",
                "provider_status": "operator_supplied",
                "as_of_utc": "2026-05-07T12:00:00Z",
                "range_start_utc": "2026-05-07T10:00:00Z",
                "range_end_utc": "2026-05-07T11:00:00Z",
                "assets": ["BTC"],
                "ohlcv_bytes": bytes_,
                "sha256": "0" * 64,
            }
        )


def test_canonical_bytes_deterministic() -> None:
    first = make_price_snapshot(
        provider_id="operator-file",
        provider_status="operator_supplied",
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        assets=["BTC"],
        rows=ohlcv_rows(),
    )
    second = make_price_snapshot(
        provider_id="operator-file",
        provider_status="operator_supplied",
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        assets=["BTC"],
        rows=list(reversed(ohlcv_rows())),
    )

    assert first.canonical_bytes() == second.canonical_bytes()
    assert first.sha256 == second.sha256
