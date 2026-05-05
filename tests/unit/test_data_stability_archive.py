from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone

import polars as pl

from entropy.evidence.data_stability_archive import build_archive_data_stability_packet


def test_build_archive_data_stability_packet_accepts_continuous_archive(tmp_path) -> None:
    manifest_paths = []
    for symbol in ("BTCUSDT", "ETHUSDT"):
        manifest_paths.append(_write_archive_fixture(tmp_path, symbol=symbol, day_count=90))

    result = build_archive_data_stability_packet(
        conversion_manifest_paths=manifest_paths,
        output_dir=tmp_path / "packet",
        target_symbols=("BTCUSDT", "ETHUSDT"),
    )

    assert result.archive_only is True
    assert result.gate_claim_allowed is False
    assert result.source_manifest_count == 2
    assert result.row_count == 180
    assert result.summary.monitored_day_count == 90
    assert result.summary.missing_symbol_days == 0
    assert result.summary.unexplained_gap_count == 0
    assert result.summary.packet_status == "PACKET_READY_FOR_REVIEW"
    assert result.rows_path.exists()
    assert result.summary_path.exists()
    assert result.manifest_path.exists()
    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert payload["source_manifests"] == [path.as_posix() for path in manifest_paths]
    summary_text = result.summary_path.read_text(encoding="utf-8")
    assert "archive-only summary" in summary_text
    assert "prove live feed stability" in summary_text


def test_build_archive_data_stability_packet_flags_missing_symbol_days(tmp_path) -> None:
    manifest_paths = (
        _write_archive_fixture(tmp_path, symbol="BTCUSDT", day_count=90),
        _write_archive_fixture(tmp_path, symbol="ETHUSDT", day_count=89),
    )

    result = build_archive_data_stability_packet(
        conversion_manifest_paths=manifest_paths,
        output_dir=tmp_path / "packet",
        target_symbols=("BTCUSDT", "ETHUSDT"),
    )

    assert result.summary.missing_symbol_days == 1
    assert result.summary.packet_status == "INCOMPLETE"


def _write_archive_fixture(tmp_path, *, symbol: str, day_count: int):
    start = date(2026, 1, 1)
    rows = []
    for index in range(day_count):
        timestamp = datetime.combine(
            start + timedelta(days=index),
            datetime.min.time(),
            tzinfo=timezone.utc,
        )
        rows.append(
            {
                "timestamp": timestamp.isoformat(),
                "open": 100.0,
                "high": 101.0,
                "low": 99.0,
                "close": 100.5,
                "volume": 1000.0,
            }
        )
    parquet_path = tmp_path / f"{symbol}.parquet"
    pl.DataFrame(rows).write_parquet(parquet_path)
    manifest_path = tmp_path / f"{symbol}_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "symbol": symbol,
                "interval": "1d",
                "plan_id": "fixture_archive_plan",
                "dataset_hash": f"{symbol}_dataset_hash",
                "combined_source_sha256": f"{symbol}_source_hash",
                "data_quality_status": "PASS",
                "last_bar_ts": rows[-1]["timestamp"],
                "parquet_path": parquet_path.as_posix(),
                "manifest_path": manifest_path.as_posix(),
            }
        ),
        encoding="utf-8",
    )
    return manifest_path
