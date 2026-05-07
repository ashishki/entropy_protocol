"""Unit tests for Binance public archive canary helpers."""

from __future__ import annotations

import csv
import io
import zipfile
from datetime import datetime, timezone

import pytest

from entropy.evidence.binance_canary import (
    BINANCE_CANARY_ID,
    parse_binance_kline_zip,
    render_binance_canary_summary,
    run_binance_p4_canary,
)


def test_parse_binance_kline_zip_reads_ohlcv_rows() -> None:
    bars = parse_binance_kline_zip(_zip_payload())

    assert len(bars) == 7
    assert bars[0].timestamp == datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert bars[0].open == pytest.approx(100.0)
    assert bars[-1].close == pytest.approx(106.0)


def test_parse_binance_kline_zip_rejects_ambiguous_archive() -> None:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("first.csv", "1,2,3,4,5,6\n")
        archive.writestr("second.csv", "1,2,3,4,5,6\n")

    with pytest.raises(ValueError, match="exactly one CSV"):
        parse_binance_kline_zip(payload.getvalue())


def test_run_binance_p4_canary_writes_manifest_and_p4_summary(tmp_path) -> None:
    result = run_binance_p4_canary(
        zip_payload=_zip_payload(),
        symbol="BTCUSDT",
        interval="1d",
        year=2024,
        month=1,
        output_dir=tmp_path,
        label_generation_ts=datetime(2026, 5, 5, tzinfo=timezone.utc),
    )
    rendered = render_binance_canary_summary(result)

    assert result.canary_id == BINANCE_CANARY_ID
    assert result.daily_bars == 7
    assert result.data_quality_status == "PASS"
    assert result.parquet_path.exists()
    assert result.manifest_path.exists()
    assert result.p4_summary.gate_evidence_complete is False
    assert "canary evidence only" in rendered


def _zip_payload() -> bytes:
    payload = io.BytesIO()
    rows = []
    for day in range(1, 8):
        open_time_ms = int(datetime(2024, 1, day, tzinfo=timezone.utc).timestamp() * 1000)
        rows.append(
            [
                open_time_ms,
                99 + day,
                101 + day,
                98 + day,
                100 + day - 1,
                10 + day,
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
        archive.writestr("BTCUSDT-1d-2024-01.csv", csv_payload.getvalue())
    return payload.getvalue()
