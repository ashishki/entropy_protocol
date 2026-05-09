from __future__ import annotations

from datetime import UTC, datetime

import pytest

from signal_sandbox.market_data import (
    LocalMarketDataStore,
    MarketDataSnapshot,
    SnapshotAlreadyExists,
    SnapshotChecksumMismatch,
    make_operator_file_snapshot,
)


def test_snapshot_round_trip_with_checksum(tmp_path) -> None:
    store = LocalMarketDataStore(tmp_path)
    snapshot = make_snapshot(snapshot_id="btc-1d-001")

    store.write_snapshot(snapshot)
    loaded = store.load_snapshot("btc-1d-001")

    assert loaded == snapshot
    assert store.list_snapshots() == [snapshot.metadata]


def test_snapshot_metadata_required_fields() -> None:
    metadata = make_snapshot().metadata

    assert metadata.provider == "operator_file"
    assert metadata.canonical_asset_id == "CRYPTO:BTC"
    assert metadata.provider_symbol == "BTC/USDT"
    assert metadata.timeframe == "1d"
    assert metadata.source_range_start_utc == dt("2026-05-01T00:00:00+00:00")
    assert metadata.source_range_end_utc == dt("2026-05-03T00:00:00+00:00")
    assert metadata.captured_at_utc == dt("2026-05-04T00:00:00+00:00")
    assert len(metadata.data_sha256) == 64
    assert metadata.license == "operator_provided"
    assert metadata.provenance == "unit test fixture"


def test_snapshot_overwrite_rejected(tmp_path) -> None:
    store = LocalMarketDataStore(tmp_path)
    store.write_snapshot(make_snapshot(snapshot_id="same-id"))

    with pytest.raises(SnapshotAlreadyExists):
        store.write_snapshot(
            make_snapshot(snapshot_id="same-id", close="102", data_id="changed")
        )


def test_operator_file_fixture_supported(tmp_path) -> None:
    store = LocalMarketDataStore(tmp_path)
    snapshot = make_snapshot(snapshot_id="operator-fixture")

    path = store.write_snapshot(snapshot)

    assert (path / "ohlcv.parquet").is_file()
    assert (path / "metadata.json").is_file()
    assert store.load_snapshot("operator-fixture").metadata.provider == "operator_file"


def test_checksum_mismatch_rejected() -> None:
    snapshot = make_snapshot()

    with pytest.raises(SnapshotChecksumMismatch):
        MarketDataSnapshot(metadata=snapshot.metadata, data_bytes=b"changed")


def make_snapshot(
    *,
    snapshot_id: str = "btc-1d",
    close: str = "101",
    data_id: str = "base",
) -> MarketDataSnapshot:
    return make_operator_file_snapshot(
        snapshot_id=snapshot_id,
        canonical_asset_id="CRYPTO:BTC",
        provider_symbol="BTC/USDT",
        timeframe="1d",
        source_range_start_utc=dt("2026-05-01T00:00:00+00:00"),
        source_range_end_utc=dt("2026-05-03T00:00:00+00:00"),
        captured_at_utc=dt("2026-05-04T00:00:00+00:00"),
        rows=[
            {
                "asset": f"BTC-{data_id}",
                "timestamp_utc": "2026-05-01T00:00:00+00:00",
                "open": "100",
                "high": "105",
                "low": "99",
                "close": close,
                "volume": "10",
            }
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )


def dt(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed
