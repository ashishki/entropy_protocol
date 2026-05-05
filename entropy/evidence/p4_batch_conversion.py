"""P4 Binance archive batch conversion."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import polars as pl

from entropy.data.quality import DataQualityCheckResult, run_all_checks
from entropy.evidence.binance_canary import parse_binance_kline_zip
from entropy.evidence.p4_artifacts import (
    P4ArtifactInput,
    P4CoverageSummary,
    generate_p4_label_artifacts,
)
from entropy.hashing import compute_dataset_hash
from entropy.models.market import OHLCVBar

P4_BATCH_CONVERSION_ID = "P4-BINANCE-BATCH-CONVERT-v1"
P4_SYMBOL_CONVERSION_ID = "P4-BINANCE-SYMBOL-CONVERT-v1"


@dataclass(frozen=True)
class P4BatchConversionResult:
    """Result for one collected P4 batch conversion."""

    conversion_id: str
    collection_id: str
    plan_id: str
    plan_hash: str
    batch_index: int
    symbol: str
    interval: str
    source_item_count: int
    source_byte_count: int
    combined_source_sha256: str
    parquet_path: Path
    dataset_hash: str
    daily_bars: int
    first_bar_ts: datetime
    last_bar_ts: datetime
    data_quality_status: str
    data_quality_checks: tuple[DataQualityCheckResult, ...]
    p4_summary: P4CoverageSummary
    manifest_path: Path
    gate_claim_allowed: bool = False


@dataclass(frozen=True)
class P4SymbolConversionResult:
    """Result for one symbol conversion across collected batches."""

    conversion_id: str
    plan_id: str
    plan_hash: str
    symbol: str
    interval: str
    source_manifest_paths: tuple[Path, ...]
    source_item_count: int
    source_byte_count: int
    source_sequence_min: int
    source_sequence_max: int
    source_month_start: str
    source_month_end: str
    combined_source_sha256: str
    parquet_path: Path
    dataset_hash: str
    daily_bars: int
    first_bar_ts: datetime
    last_bar_ts: datetime
    data_quality_status: str
    data_quality_checks: tuple[DataQualityCheckResult, ...]
    p4_summary: P4CoverageSummary
    manifest_path: Path
    gate_claim_allowed: bool = False


def convert_p4_batch(
    *,
    batch_manifest_path: Path | str,
    output_dir: Path | str,
    label_generation_ts: datetime,
    required_labeled_weeks: int = 156,
) -> P4BatchConversionResult:
    """Convert a collected Binance archive batch into Parquet and partial P4 output."""
    manifest = _read_manifest(Path(batch_manifest_path))
    items = _done_items(manifest)
    symbol = _single_value(items, "symbol")
    interval = _single_interval(items)
    bars = _load_and_validate_source_bars(items)
    sorted_bars = _sort_unique_bars(bars)
    quality = run_all_checks(list(sorted_bars), max_gap_seconds=172_800)

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    parquet_path = (
        root / "datasets" / f"{symbol}-{interval}-batch_{manifest['batch_index']:03d}.parquet"
    )
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    _write_bars_parquet(sorted_bars, parquet_path)
    dataset_hash = compute_dataset_hash(parquet_path)
    p4_summary = generate_p4_label_artifacts(
        datasets={
            symbol: P4ArtifactInput(
                symbol=symbol,
                bars=sorted_bars,
                calendar_profile="continuous",
                dataset_hash=dataset_hash,
            )
        },
        target_universe=(symbol,),
        output_dir=root / "p4",
        label_generation_ts=label_generation_ts,
        required_assets=1,
        required_labeled_weeks=required_labeled_weeks,
    )
    manifest_path = root / f"P4_BATCH_{manifest['batch_index']:03d}_CONVERSION_MANIFEST.json"
    result = P4BatchConversionResult(
        conversion_id=P4_BATCH_CONVERSION_ID,
        collection_id=str(manifest["collection_id"]),
        plan_id=str(manifest["plan_id"]),
        plan_hash=str(manifest["plan_hash"]),
        batch_index=int(manifest["batch_index"]),
        symbol=symbol,
        interval=interval,
        source_item_count=len(items),
        source_byte_count=sum(int(item["byte_count"]) for item in items),
        combined_source_sha256=_combined_source_hash(items),
        parquet_path=parquet_path,
        dataset_hash=dataset_hash,
        daily_bars=len(sorted_bars),
        first_bar_ts=sorted_bars[0].timestamp,
        last_bar_ts=sorted_bars[-1].timestamp,
        data_quality_status=quality.status,
        data_quality_checks=tuple(quality.per_check_results),
        p4_summary=p4_summary,
        manifest_path=manifest_path,
    )
    manifest_path.write_text(
        json.dumps(conversion_manifest_payload(result), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def convert_symbol_from_batch_manifests(
    *,
    batch_manifest_paths: Sequence[Path | str],
    symbol: str,
    output_dir: Path | str,
    label_generation_ts: datetime,
    required_labeled_weeks: int = 156,
) -> P4SymbolConversionResult:
    """Convert one symbol across one or more collected batch manifests."""
    if not batch_manifest_paths:
        raise ValueError("batch_manifest_paths must not be empty")
    normalized_symbol = symbol.strip()
    if not normalized_symbol:
        raise ValueError("symbol must not be blank")

    manifest_paths = tuple(Path(path) for path in batch_manifest_paths)
    manifests = tuple(_read_manifest(path) for path in manifest_paths)
    plan_id = _single_manifest_value(manifests, "plan_id")
    plan_hash = _single_manifest_value(manifests, "plan_hash")
    items = tuple(
        item
        for manifest in manifests
        for item in _done_items(manifest)
        if str(item["symbol"]) == normalized_symbol
    )
    if not items:
        raise ValueError("no DONE items found for symbol " + normalized_symbol)
    interval = _single_interval(items)
    bars = _load_and_validate_source_bars(items)
    sorted_bars = _sort_unique_bars(bars)
    quality = run_all_checks(list(sorted_bars), max_gap_seconds=172_800)
    first_month, last_month = _source_month_range(items)

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    parquet_path = (
        root
        / "datasets"
        / f"{normalized_symbol}-{interval}-{first_month.replace('-', '_')}-{last_month.replace('-', '_')}.parquet"
    )
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    _write_bars_parquet(sorted_bars, parquet_path)
    dataset_hash = compute_dataset_hash(parquet_path)
    p4_summary = generate_p4_label_artifacts(
        datasets={
            normalized_symbol: P4ArtifactInput(
                symbol=normalized_symbol,
                bars=sorted_bars,
                calendar_profile="continuous",
                dataset_hash=dataset_hash,
            )
        },
        target_universe=(normalized_symbol,),
        output_dir=root / "p4",
        label_generation_ts=label_generation_ts,
        required_assets=1,
        required_labeled_weeks=required_labeled_weeks,
    )
    manifest_path = root / f"{normalized_symbol}_{interval}_SYMBOL_CONVERSION_MANIFEST.json"
    result = P4SymbolConversionResult(
        conversion_id=P4_SYMBOL_CONVERSION_ID,
        plan_id=plan_id,
        plan_hash=plan_hash,
        symbol=normalized_symbol,
        interval=interval,
        source_manifest_paths=manifest_paths,
        source_item_count=len(items),
        source_byte_count=sum(int(item["byte_count"]) for item in items),
        source_sequence_min=min(int(item["sequence"]) for item in items),
        source_sequence_max=max(int(item["sequence"]) for item in items),
        source_month_start=first_month,
        source_month_end=last_month,
        combined_source_sha256=_combined_source_hash(items),
        parquet_path=parquet_path,
        dataset_hash=dataset_hash,
        daily_bars=len(sorted_bars),
        first_bar_ts=sorted_bars[0].timestamp,
        last_bar_ts=sorted_bars[-1].timestamp,
        data_quality_status=quality.status,
        data_quality_checks=tuple(quality.per_check_results),
        p4_summary=p4_summary,
        manifest_path=manifest_path,
    )
    manifest_path.write_text(
        json.dumps(symbol_conversion_manifest_payload(result), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def conversion_manifest_payload(result: P4BatchConversionResult) -> dict[str, object]:
    """Return a JSON-serializable conversion manifest."""
    return {
        "conversion_id": result.conversion_id,
        "collection_id": result.collection_id,
        "plan_id": result.plan_id,
        "plan_hash": result.plan_hash,
        "batch_index": result.batch_index,
        "symbol": result.symbol,
        "interval": result.interval,
        "source_item_count": result.source_item_count,
        "source_byte_count": result.source_byte_count,
        "combined_source_sha256": result.combined_source_sha256,
        "parquet_path": result.parquet_path.as_posix(),
        "dataset_hash": result.dataset_hash,
        "daily_bars": result.daily_bars,
        "first_bar_ts": result.first_bar_ts.isoformat(),
        "last_bar_ts": result.last_bar_ts.isoformat(),
        "data_quality_status": result.data_quality_status,
        "data_quality_checks": [
            {
                "check_name": check.check_name,
                "status": check.status,
                "affected_bar_count": check.affected_bar_count,
                "message": check.message,
            }
            for check in result.data_quality_checks
        ],
        "p4_gate_evidence_complete": result.p4_summary.gate_evidence_complete,
        "p4_passing_assets": result.p4_summary.passing_assets,
        "p4_required_assets": result.p4_summary.required_assets,
        "p4_required_labeled_weeks": result.p4_summary.required_labeled_weeks,
        "p4_summary_path": result.p4_summary.summary_path.as_posix(),
        "gate_claim_allowed": result.gate_claim_allowed,
        "boundary": "partial_batch_conversion_not_phase_gate_evidence",
    }


def symbol_conversion_manifest_payload(result: P4SymbolConversionResult) -> dict[str, object]:
    """Return a JSON-serializable symbol conversion manifest."""
    return {
        "conversion_id": result.conversion_id,
        "plan_id": result.plan_id,
        "plan_hash": result.plan_hash,
        "symbol": result.symbol,
        "interval": result.interval,
        "source_manifest_paths": [path.as_posix() for path in result.source_manifest_paths],
        "source_item_count": result.source_item_count,
        "source_byte_count": result.source_byte_count,
        "source_sequence_min": result.source_sequence_min,
        "source_sequence_max": result.source_sequence_max,
        "source_month_start": result.source_month_start,
        "source_month_end": result.source_month_end,
        "combined_source_sha256": result.combined_source_sha256,
        "parquet_path": result.parquet_path.as_posix(),
        "dataset_hash": result.dataset_hash,
        "daily_bars": result.daily_bars,
        "first_bar_ts": result.first_bar_ts.isoformat(),
        "last_bar_ts": result.last_bar_ts.isoformat(),
        "data_quality_status": result.data_quality_status,
        "data_quality_checks": [
            {
                "check_name": check.check_name,
                "status": check.status,
                "affected_bar_count": check.affected_bar_count,
                "message": check.message,
            }
            for check in result.data_quality_checks
        ],
        "p4_gate_evidence_complete": result.p4_summary.gate_evidence_complete,
        "p4_passing_assets": result.p4_summary.passing_assets,
        "p4_required_assets": result.p4_summary.required_assets,
        "p4_required_labeled_weeks": result.p4_summary.required_labeled_weeks,
        "p4_summary_path": result.p4_summary.summary_path.as_posix(),
        "gate_claim_allowed": result.gate_claim_allowed,
        "boundary": "symbol_window_conversion_not_phase_gate_evidence",
    }


def render_p4_batch_conversion_summary(result: P4BatchConversionResult) -> str:
    """Render a deterministic Markdown conversion summary."""
    coverage_row = result.p4_summary.rows[0]
    lines = [
        "# P4 First Batch Conversion Summary",
        "",
        f"Conversion ID: `{result.conversion_id}`",
        f"Collection ID: `{result.collection_id}`",
        f"Plan ID: `{result.plan_id}`",
        f"Plan hash: `{result.plan_hash}`",
        f"Batch index: {result.batch_index}",
        f"Symbol: `{result.symbol}`",
        f"Interval: `{result.interval}`",
        f"Source files: {result.source_item_count}",
        f"Source bytes: {result.source_byte_count}",
        f"Combined source SHA-256: `{result.combined_source_sha256}`",
        f"Parquet path: `{result.parquet_path.as_posix()}`",
        f"Dataset hash: `{result.dataset_hash}`",
        f"Daily bars: {result.daily_bars}",
        f"First bar: `{result.first_bar_ts.isoformat()}`",
        f"Last bar: `{result.last_bar_ts.isoformat()}`",
        f"Data quality status: `{result.data_quality_status}`",
        f"P4 generated labels: {coverage_row.generated_labels}",
        f"P4 valid labeled weeks: {coverage_row.valid_labeled_weeks}",
        f"P4 reason: `{coverage_row.reason_code}`",
        f"P4 gate evidence complete: `{_bool(result.p4_summary.gate_evidence_complete)}`",
        f"Gate claim allowed: `{_bool(result.gate_claim_allowed)}`",
        "",
        "| Check | Status | Affected Bars | Message |",
        "|-------|--------|---------------|---------|",
    ]
    for check in result.data_quality_checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    check.check_name,
                    check.status,
                    str(check.affected_bar_count),
                    check.message or "",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Boundary: this is partial first-batch conversion only. It does not close "
            "P4 coverage, approve Phase 0, start Phase 1, or make performance claims.",
            "",
        ]
    )
    return "\n".join(lines)


def render_p4_symbol_conversion_summary(result: P4SymbolConversionResult) -> str:
    """Render a deterministic Markdown symbol conversion summary."""
    coverage_row = result.p4_summary.rows[0]
    lines = [
        "# P4 Symbol Conversion Summary",
        "",
        f"Conversion ID: `{result.conversion_id}`",
        f"Plan ID: `{result.plan_id}`",
        f"Plan hash: `{result.plan_hash}`",
        f"Symbol: `{result.symbol}`",
        f"Interval: `{result.interval}`",
        f"Source manifests: {len(result.source_manifest_paths)}",
        f"Source sequences: {result.source_sequence_min}-{result.source_sequence_max}",
        f"Source months: `{result.source_month_start}` through `{result.source_month_end}`",
        f"Source files: {result.source_item_count}",
        f"Source bytes: {result.source_byte_count}",
        f"Combined source SHA-256: `{result.combined_source_sha256}`",
        f"Parquet path: `{result.parquet_path.as_posix()}`",
        f"Dataset hash: `{result.dataset_hash}`",
        f"Daily bars: {result.daily_bars}",
        f"First bar: `{result.first_bar_ts.isoformat()}`",
        f"Last bar: `{result.last_bar_ts.isoformat()}`",
        f"Data quality status: `{result.data_quality_status}`",
        f"P4 generated labels: {coverage_row.generated_labels}",
        f"P4 valid labeled weeks: {coverage_row.valid_labeled_weeks}",
        f"P4 reason: `{coverage_row.reason_code}`",
        f"P4 gate evidence complete: `{_bool(result.p4_summary.gate_evidence_complete)}`",
        f"Gate claim allowed: `{_bool(result.gate_claim_allowed)}`",
        "",
        "| Check | Status | Affected Bars | Message |",
        "|-------|--------|---------------|---------|",
    ]
    for check in result.data_quality_checks:
        lines.append(
            "| "
            + " | ".join(
                [
                    check.check_name,
                    check.status,
                    str(check.affected_bar_count),
                    check.message or "",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Boundary: this is symbol-window conversion only. It does not close P4 "
            "coverage, approve Phase 0, start Phase 1, or make performance claims.",
            "",
        ]
    )
    return "\n".join(lines)


def _read_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    required_keys = {
        "collection_id",
        "plan_id",
        "plan_hash",
        "batch_index",
        "items",
    }
    missing = sorted(required_keys.difference(manifest))
    if missing:
        raise ValueError("batch manifest missing keys: " + ", ".join(missing))
    if not isinstance(manifest["items"], list):
        raise ValueError("batch manifest items must be a list")
    return manifest


def _single_manifest_value(manifests: Sequence[dict[str, Any]], key: str) -> str:
    values = {str(manifest[key]) for manifest in manifests}
    if len(values) != 1:
        raise ValueError("batch manifests must share one " + key)
    return next(iter(values))


def _done_items(manifest: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    items = tuple(item for item in manifest["items"] if item.get("status") == "DONE")
    if not items:
        raise ValueError("batch manifest has no DONE items to convert")
    return items


def _single_value(items: Sequence[dict[str, Any]], key: str) -> str:
    values = {str(item[key]) for item in items}
    if len(values) != 1:
        raise ValueError("batch conversion requires a single " + key)
    return next(iter(values))


def _single_interval(items: Sequence[dict[str, Any]]) -> str:
    intervals = {_interval_from_path(str(item["path"]), str(item["symbol"])) for item in items}
    if len(intervals) != 1:
        raise ValueError("batch conversion requires a single interval")
    return next(iter(intervals))


def _interval_from_path(path: str, symbol: str) -> str:
    file_name = Path(path).name.removesuffix(".zip")
    prefix = symbol + "-"
    if not file_name.startswith(prefix):
        raise ValueError("source archive filename does not match symbol")
    middle = file_name.removeprefix(prefix).rsplit("-", 2)[0]
    if not middle:
        raise ValueError("source archive filename does not include interval")
    return middle


def _load_and_validate_source_bars(items: Sequence[dict[str, Any]]) -> tuple[OHLCVBar, ...]:
    bars: list[OHLCVBar] = []
    for item in sorted(items, key=lambda value: int(value["sequence"])):
        path_value = item.get("path")
        source_sha256 = item.get("source_sha256")
        if path_value is None or source_sha256 is None:
            raise ValueError("DONE item must include path and source_sha256")
        payload = Path(str(path_value)).read_bytes()
        actual_sha256 = hashlib.sha256(payload).hexdigest()
        if actual_sha256 != source_sha256:
            raise ValueError("source SHA-256 mismatch for " + str(path_value))
        bars.extend(parse_binance_kline_zip(payload))
    return tuple(bars)


def _sort_unique_bars(bars: Sequence[OHLCVBar]) -> tuple[OHLCVBar, ...]:
    if not bars:
        raise ValueError("cannot convert an empty batch")
    sorted_bars = tuple(sorted(bars, key=lambda bar: bar.timestamp))
    seen: set[datetime] = set()
    for bar in sorted_bars:
        if bar.timestamp in seen:
            raise ValueError("duplicate daily bar timestamp: " + bar.timestamp.isoformat())
        seen.add(bar.timestamp)
    return sorted_bars


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


def _combined_source_hash(items: Sequence[dict[str, Any]]) -> str:
    payload = json.dumps(
        [
            {
                "sequence": int(item["sequence"]),
                "symbol": str(item["symbol"]),
                "year": int(item["year"]),
                "month": int(item["month"]),
                "source_sha256": str(item["source_sha256"]),
                "byte_count": int(item["byte_count"]),
            }
            for item in sorted(items, key=lambda value: int(value["sequence"]))
        ],
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _source_month_range(items: Sequence[dict[str, Any]]) -> tuple[str, str]:
    months = sorted((int(item["year"]), int(item["month"])) for item in items)
    first = months[0]
    last = months[-1]
    return f"{first[0]}-{first[1]:02d}", f"{last[0]}-{last[1]:02d}"


def _bool(value: bool) -> str:
    return "true" if value else "false"
