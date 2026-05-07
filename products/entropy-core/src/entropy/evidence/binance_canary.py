"""Binance public archive OHLCV canary helpers."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

import polars as pl

from entropy.data.quality import run_all_checks
from entropy.evidence.p4_artifacts import (
    P4ArtifactInput,
    P4CoverageSummary,
    generate_p4_label_artifacts,
)
from entropy.evidence.source_selection import build_binance_monthly_klines_urls, validate_source_use
from entropy.hashing import compute_dataset_hash
from entropy.models.market import OHLCVBar

BINANCE_CANARY_ID = "BINANCE-P4-CANARY-v1"


@dataclass(frozen=True)
class BinanceKlineCanaryResult:
    """Result of a tiny Binance archive OHLCV canary run."""

    canary_id: str
    source_url: str
    source_sha256: str
    parquet_path: Path
    dataset_hash: str
    daily_bars: int
    data_quality_status: str
    p4_summary: P4CoverageSummary
    manifest_path: Path


def parse_binance_kline_zip(zip_payload: bytes) -> tuple[OHLCVBar, ...]:
    """Parse one Binance public archive kline zip payload into UTC OHLCV bars."""
    rows: list[OHLCVBar] = []
    with zipfile.ZipFile(io.BytesIO(zip_payload)) as archive:
        csv_names = sorted(name for name in archive.namelist() if name.endswith(".csv"))
        if len(csv_names) != 1:
            raise ValueError("Binance kline zip must contain exactly one CSV file")
        with archive.open(csv_names[0]) as handle:
            text = io.TextIOWrapper(handle, encoding="utf-8")
            for raw_row in csv.reader(text):
                if not raw_row:
                    continue
                if len(raw_row) < 6:
                    raise ValueError("Binance kline row must contain at least 6 columns")
                rows.append(
                    OHLCVBar(
                        timestamp=_binance_timestamp_to_utc(int(raw_row[0])),
                        open=float(raw_row[1]),
                        high=float(raw_row[2]),
                        low=float(raw_row[3]),
                        close=float(raw_row[4]),
                        volume=float(raw_row[5]),
                    )
                )
    return tuple(rows)


def run_binance_p4_canary(
    *,
    zip_payload: bytes,
    symbol: str,
    interval: str,
    year: int,
    month: int,
    output_dir: Path | str,
    label_generation_ts: datetime,
) -> BinanceKlineCanaryResult:
    """Run canary data-quality and P4 artifact tooling from a Binance archive zip."""
    url = build_binance_monthly_klines_urls(
        symbol=symbol,
        interval=interval,
        start_year=year,
        start_month=month,
        end_year=year,
        end_month=month,
    )[0]
    validate_source_use(
        source_id="binance_public_archive",
        use_case="p4_label_coverage",
        domain="data.binance.vision",
    )
    bars = parse_binance_kline_zip(zip_payload)
    quality = run_all_checks(list(bars), max_gap_seconds=172_800)
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    zip_path = root / f"{symbol}-{interval}-{year}-{month:02d}.zip"
    zip_path.write_bytes(zip_payload)
    parquet_path = root / f"{symbol}-{interval}-{year}-{month:02d}.parquet"
    _write_bars_parquet(bars, parquet_path)
    dataset_hash = compute_dataset_hash(parquet_path)
    p4_summary = generate_p4_label_artifacts(
        datasets={
            symbol: P4ArtifactInput(
                symbol=symbol,
                bars=bars,
                calendar_profile="continuous",
                dataset_hash=dataset_hash,
            )
        },
        target_universe=(symbol,),
        output_dir=root / "p4",
        label_generation_ts=label_generation_ts,
        required_assets=1,
        required_labeled_weeks=156,
    )
    manifest_path = root / "BINANCE_P4_CANARY_MANIFEST.json"
    manifest = {
        "canary_id": BINANCE_CANARY_ID,
        "source_url": url,
        "source_sha256": hashlib.sha256(zip_payload).hexdigest(),
        "parquet_path": parquet_path.as_posix(),
        "dataset_hash": dataset_hash,
        "daily_bars": len(bars),
        "data_quality_status": quality.status,
        "p4_gate_evidence_complete": p4_summary.gate_evidence_complete,
        "boundary": "canary_only_not_phase_gate_evidence",
    }
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return BinanceKlineCanaryResult(
        canary_id=BINANCE_CANARY_ID,
        source_url=url,
        source_sha256=manifest["source_sha256"],
        parquet_path=parquet_path,
        dataset_hash=dataset_hash,
        daily_bars=len(bars),
        data_quality_status=quality.status,
        p4_summary=p4_summary,
        manifest_path=manifest_path,
    )


def render_binance_canary_summary(result: BinanceKlineCanaryResult) -> str:
    """Render a deterministic Markdown canary summary."""
    return "\n".join(
        [
            "# Binance P4 Canary Summary",
            "",
            f"Canary ID: `{result.canary_id}`",
            f"Source URL: `{result.source_url}`",
            f"Source SHA-256: `{result.source_sha256}`",
            f"Dataset hash: `{result.dataset_hash}`",
            f"Daily bars: {result.daily_bars}",
            f"Data quality status: `{result.data_quality_status}`",
            f"P4 gate evidence complete: `{str(result.p4_summary.gate_evidence_complete).lower()}`",
            "",
            "Boundary: this is canary evidence only. It does not close P4 coverage, "
            "approve Phase 0, start Phase 1, or make performance claims.",
            "",
        ]
    )


def _binance_timestamp_to_utc(timestamp: int) -> datetime:
    divisor = 1_000_000 if timestamp >= 10_000_000_000_000 else 1_000
    return datetime.fromtimestamp(timestamp / divisor, tz=UTC)


def _write_bars_parquet(bars: Sequence[OHLCVBar], path: Path) -> None:
    frame = pl.DataFrame(
        {
            "timestamp": [bar.timestamp.isoformat() for bar in bars],
            "open": [bar.open for bar in bars],
            "high": [bar.high for bar in bars],
            "low": [bar.low for bar in bars],
            "close": [bar.close for bar in bars],
            "volume": [bar.volume for bar in bars],
        }
    )
    frame.write_parquet(path)
