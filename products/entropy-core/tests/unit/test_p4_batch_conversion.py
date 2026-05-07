"""Unit tests for P4 batch conversion artifacts."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from entropy.evidence.p4_batch_conversion import (
    P4_BATCH_CONVERSION_ID,
    P4_SYMBOL_CONVERSION_ID,
    convert_p4_batch,
    convert_symbol_from_batch_manifests,
    render_p4_batch_conversion_summary,
    render_p4_symbol_conversion_summary,
)

UTC_TS = datetime(2026, 5, 5, tzinfo=timezone.utc)


def test_convert_p4_batch_writes_dataset_manifest_and_partial_p4(tmp_path: Path) -> None:
    batch_dir = tmp_path / "batch"
    first = _write_zip(
        batch_dir / "BTCUSDT" / "BTCUSDT-1d-2023-01.zip",
        manifest_year=2023,
        manifest_month=1,
        start_ts=datetime(2023, 1, 1, tzinfo=timezone.utc),
        day_count=7,
    )
    second = _write_zip(
        batch_dir / "BTCUSDT" / "BTCUSDT-1d-2023-02.zip",
        manifest_year=2023,
        manifest_month=2,
        start_ts=datetime(2023, 1, 8, tzinfo=timezone.utc),
        day_count=7,
    )
    manifest_path = _write_manifest(batch_dir, [first, second])

    result = convert_p4_batch(
        batch_manifest_path=manifest_path,
        output_dir=tmp_path / "converted",
        label_generation_ts=UTC_TS,
    )
    rendered = render_p4_batch_conversion_summary(result)

    assert result.conversion_id == P4_BATCH_CONVERSION_ID
    assert result.symbol == "BTCUSDT"
    assert result.interval == "1d"
    assert result.source_item_count == 2
    assert result.daily_bars == 14
    assert result.data_quality_status == "PASS"
    assert result.parquet_path.exists()
    assert result.manifest_path.exists()
    assert result.p4_summary.summary_path.exists()
    assert result.p4_summary.gate_evidence_complete is False
    assert "partial first-batch conversion only" in rendered


def test_convert_p4_batch_rejects_source_hash_mismatch(tmp_path: Path) -> None:
    batch_dir = tmp_path / "batch"
    item = _write_zip(
        batch_dir / "BTCUSDT" / "BTCUSDT-1d-2023-01.zip",
        manifest_year=2023,
        manifest_month=1,
        start_ts=datetime(2023, 1, 1, tzinfo=timezone.utc),
        day_count=7,
    )
    broken_item = {**item, "source_sha256": "0" * 64}
    manifest_path = _write_manifest(batch_dir, [broken_item])

    with pytest.raises(ValueError, match="source SHA-256 mismatch"):
        convert_p4_batch(
            batch_manifest_path=manifest_path,
            output_dir=tmp_path / "converted",
            label_generation_ts=UTC_TS,
        )


def test_convert_symbol_from_batch_manifests_filters_symbol_and_writes_outputs(
    tmp_path: Path,
) -> None:
    first_batch = tmp_path / "batch_001"
    second_batch = tmp_path / "batch_002"
    first_btc = _write_zip(
        first_batch / "BTCUSDT" / "BTCUSDT-1d-2023-01.zip",
        manifest_year=2023,
        manifest_month=1,
        start_ts=datetime(2023, 1, 1, tzinfo=timezone.utc),
        day_count=7,
    )
    second_btc = {
        **_write_zip(
            second_batch / "BTCUSDT" / "BTCUSDT-1d-2023-02.zip",
            manifest_year=2023,
            manifest_month=2,
            start_ts=datetime(2023, 1, 8, tzinfo=timezone.utc),
            day_count=7,
        ),
        "sequence": 2,
    }
    eth_item = {
        **_write_zip(
            second_batch / "ETHUSDT" / "ETHUSDT-1d-2023-01.zip",
            manifest_year=2023,
            manifest_month=1,
            start_ts=datetime(2023, 1, 1, tzinfo=timezone.utc),
            day_count=7,
        ),
        "sequence": 3,
        "symbol": "ETHUSDT",
    }
    first_manifest = _write_manifest(first_batch, [first_btc])
    second_manifest = _write_manifest(second_batch, [second_btc, eth_item])

    result = convert_symbol_from_batch_manifests(
        batch_manifest_paths=(first_manifest, second_manifest),
        symbol="BTCUSDT",
        output_dir=tmp_path / "converted",
        label_generation_ts=UTC_TS,
    )
    rendered = render_p4_symbol_conversion_summary(result)

    assert result.conversion_id == P4_SYMBOL_CONVERSION_ID
    assert result.symbol == "BTCUSDT"
    assert result.source_item_count == 2
    assert result.source_sequence_min == 1
    assert result.source_sequence_max == 2
    assert result.daily_bars == 14
    assert result.data_quality_status == "PASS"
    assert result.parquet_path.exists()
    assert result.manifest_path.exists()
    assert result.p4_summary.gate_evidence_complete is False
    assert "symbol-window conversion only" in rendered


def _write_zip(
    path: Path,
    *,
    manifest_year: int,
    manifest_month: int,
    start_ts: datetime,
    day_count: int,
) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = io.BytesIO()
    rows = []
    for offset in range(day_count):
        open_ts = start_ts + timedelta(days=offset)
        open_time_ms = int(open_ts.timestamp() * 1000)
        rows.append(
            [
                open_time_ms,
                100 + offset,
                102 + offset,
                99 + offset,
                101 + offset,
                10 + offset,
                open_time_ms + 86_399_999,
                0,
                1,
                0,
                0,
                0,
            ]
        )
    csv_payload = io.StringIO()
    writer = csv.writer(csv_payload)
    writer.writerows(rows)
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr(path.name.replace(".zip", ".csv"), csv_payload.getvalue())
    path.write_bytes(payload.getvalue())
    return {
        "sequence": 1 if manifest_month == 1 else 2,
        "symbol": "BTCUSDT",
        "year": manifest_year,
        "month": manifest_month,
        "url": "https://data.binance.vision/example.zip",
        "status": "DONE",
        "path": path.as_posix(),
        "source_sha256": hashlib.sha256(payload.getvalue()).hexdigest(),
        "byte_count": len(payload.getvalue()),
        "error": None,
    }


def _write_manifest(batch_dir: Path, items: list[dict[str, object]]) -> Path:
    manifest_path = batch_dir / "P4_BATCH_001_MANIFEST.json"
    manifest = {
        "collection_id": "P4-BINANCE-BATCH-COLLECT-v1",
        "plan_id": "P4-BINANCE-SCALE-PLAN-v1",
        "plan_hash": "plan-hash",
        "batch_index": 1,
        "requested_items": len(items),
        "done_count": len(items),
        "failed_count": 0,
        "output_dir": batch_dir.as_posix(),
        "gate_claim_allowed": False,
        "items": items,
    }
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
    return manifest_path
