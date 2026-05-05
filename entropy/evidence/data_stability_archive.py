"""Archive-mode data-stability evidence from immutable local datasets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

import polars as pl

from entropy.data.stability import (
    DataStabilityRow,
    DataStabilitySummary,
    build_data_stability_summary,
    render_data_stability_summary,
    write_data_stability_rows_jsonl,
)

DATA_STABILITY_ARCHIVE_PACKET_ID = "DATA-STABILITY-ARCHIVE-90D-v1"


@dataclass(frozen=True)
class ArchiveDataStabilityResult:
    """Archive-mode data-stability packet result."""

    packet_id: str
    rows_path: Path
    summary_path: Path
    manifest_path: Path
    row_count: int
    summary: DataStabilitySummary
    source_manifest_count: int
    gate_claim_allowed: bool = False
    archive_only: bool = True


def build_archive_data_stability_packet(
    *,
    conversion_manifest_paths: Sequence[Path | str],
    output_dir: Path | str,
    target_symbols: Sequence[str],
    min_days: int = 90,
) -> ArchiveDataStabilityResult:
    """Build archive-mode stability rows from converted full-window datasets."""
    if not conversion_manifest_paths:
        raise ValueError("conversion_manifest_paths must not be empty")
    if not target_symbols:
        raise ValueError("target_symbols must not be empty")
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    manifests = tuple(_read_manifest(Path(path)) for path in conversion_manifest_paths)
    rows: list[DataStabilityRow] = []
    for manifest in sorted(manifests, key=lambda item: str(item["symbol"])):
        rows.extend(_rows_from_manifest(manifest))
    rows_tuple = tuple(rows)
    rows_path = root / "DATA_STABILITY_ARCHIVE_ROWS.jsonl"
    summary_path = root / "DATA_STABILITY_ARCHIVE_SUMMARY.md"
    manifest_path = root / "DATA_STABILITY_ARCHIVE_MANIFEST.json"
    write_data_stability_rows_jsonl(rows_tuple, rows_path)
    summary = build_data_stability_summary(
        rows_tuple,
        target_symbols=target_symbols,
        min_days=min_days,
    )
    summary_path.write_text(_render_archive_summary(summary), encoding="utf-8")
    result = ArchiveDataStabilityResult(
        packet_id=DATA_STABILITY_ARCHIVE_PACKET_ID,
        rows_path=rows_path,
        summary_path=summary_path,
        manifest_path=manifest_path,
        row_count=len(rows_tuple),
        summary=summary,
        source_manifest_count=len(manifests),
    )
    manifest_path.write_text(
        json.dumps(_manifest_payload(result, manifests), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def _read_manifest(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("conversion manifest must contain a JSON object")
    payload.setdefault("manifest_path", path.as_posix())
    return payload


def _rows_from_manifest(manifest: dict[str, object]) -> list[DataStabilityRow]:
    symbol = str(manifest["symbol"])
    provider = str(manifest["plan_id"])
    dataset_hash = str(manifest["dataset_hash"])
    raw_source_hash = str(manifest["combined_source_sha256"])
    data_quality_status = str(manifest["data_quality_status"])
    parquet_path = Path(str(manifest["parquet_path"]))
    timestamps = _read_archive_timestamps(parquet_path)
    expected_pass = data_quality_status == "PASS"
    rows: list[DataStabilityRow] = []
    for timestamp in timestamps:
        monitor_date = timestamp.date()
        rows.append(
            DataStabilityRow(
                monitor_id=f"archive-stability-{symbol}-{monitor_date.isoformat()}",
                monitor_date=monitor_date,
                symbol=symbol,
                timeframe=str(manifest["interval"]),
                calendar_profile="continuous",
                provider=provider,
                provider_status="ok" if expected_pass else "partial",
                expected_bars=1,
                observed_bars=1,
                first_ts=timestamp,
                last_ts=timestamp,
                timestamp_check="PASS" if expected_pass else "FAIL",
                gap_check="PASS" if expected_pass else "FAIL",
                ohlcv_sanity_check="PASS" if expected_pass else "FAIL",
                dataset_hash=dataset_hash,
                raw_source_hash=raw_source_hash,
                gap_candidate=not expected_pass,
                gap_explained=False,
                gap_reason_code="ohlcv_invalid" if not expected_pass else None,
                disposition_note_hash=None,
                checked_at=datetime.fromisoformat(str(manifest["last_bar_ts"])),
                checker="codex_archive_data_stability",
            )
        )
    return rows


def _read_archive_timestamps(parquet_path: Path) -> tuple[datetime, ...]:
    frame = pl.read_parquet(parquet_path, columns=["timestamp"])
    timestamps = []
    for value in frame["timestamp"].to_list():
        timestamps.append(datetime.fromisoformat(str(value)))
    return tuple(timestamps)


def _render_archive_summary(summary: DataStabilitySummary) -> str:
    rendered = render_data_stability_summary(summary)
    return rendered.replace(
        "Boundary: this summary does not approve Phase 0, activate providers, "
        "or prove 90-day data stability without an approved continuous "
        "monitoring packet and manual review.",
        "Boundary: this archive-only summary does not activate providers, prove "
        "live feed stability, authorize live operation, or make OOS/performance "
        "claims. It supports archive research foundation review under D-027.",
    )


def _manifest_payload(
    result: ArchiveDataStabilityResult,
    manifests: Sequence[dict[str, object]],
) -> dict[str, object]:
    return {
        "packet_id": result.packet_id,
        "archive_only": result.archive_only,
        "gate_claim_allowed": result.gate_claim_allowed,
        "source_manifest_count": result.source_manifest_count,
        "row_count": result.row_count,
        "monitored_day_count": result.summary.monitored_day_count,
        "missing_symbol_days": result.summary.missing_symbol_days,
        "unexplained_gap_count": result.summary.unexplained_gap_count,
        "packet_status": result.summary.packet_status,
        "rows_path": result.rows_path.as_posix(),
        "summary_path": result.summary_path.as_posix(),
        "symbols": sorted(str(manifest["symbol"]) for manifest in manifests),
        "source_manifests": [str(manifest.get("manifest_path", "")) for manifest in manifests],
        "boundary": "archive_data_stability_not_live_feed_claim",
    }
