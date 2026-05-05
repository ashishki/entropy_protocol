"""Phase 1A archive dataset freeze manifest builder."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

PHASE1A_ARCHIVE_FREEZE_ID = "PHASE1A-ARCHIVE-FREEZE-v1"
PHASE1A_ALLOWED_SYMBOLS = (
    "ADAUSDT",
    "ALGOUSDT",
    "ATOMUSDT",
    "BCHUSDT",
    "BNBUSDT",
    "BTCUSDT",
    "DOGEUSDT",
    "ETCUSDT",
    "ETHUSDT",
    "LINKUSDT",
    "LTCUSDT",
    "TRXUSDT",
    "VETUSDT",
    "XLMUSDT",
    "XRPUSDT",
)


@dataclass(frozen=True)
class Phase1AArchiveFreezeResult:
    """Result for a Phase 1A archive freeze manifest."""

    freeze_id: str
    manifest_path: Path
    summary_path: Path
    manifest_hash: str
    dataset_count: int
    symbol_count: int
    gate_claim_allowed: bool = False
    archive_only: bool = True


def build_phase1a_archive_freeze_manifest(
    *,
    conversion_manifest_paths: Sequence[Path | str],
    archive_stability_manifest_path: Path | str,
    output_dir: Path | str,
    contract_path: Path | str,
) -> Phase1AArchiveFreezeResult:
    """Build the machine-readable Phase 1A archive freeze manifest."""
    if not conversion_manifest_paths:
        raise ValueError("conversion_manifest_paths must not be empty")
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    conversion_manifests = tuple(
        _read_json_object(Path(path)) | {"manifest_path": Path(path).as_posix()}
        for path in conversion_manifest_paths
    )
    stability_manifest = _read_json_object(Path(archive_stability_manifest_path))
    datasets = tuple(_dataset_entry(manifest) for manifest in conversion_manifests)
    _validate_datasets(datasets)
    _validate_stability_manifest(stability_manifest)

    manifest_path = root / "PHASE1A_ARCHIVE_FREEZE_MANIFEST.json"
    summary_path = root / "PHASE1A_ARCHIVE_FREEZE_SUMMARY.md"
    payload = _manifest_payload(
        datasets=datasets,
        archive_stability_manifest_path=Path(archive_stability_manifest_path),
        contract_path=Path(contract_path),
        stability_manifest=stability_manifest,
    )
    manifest_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    manifest_hash = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()
    summary_path.write_text(
        _render_summary(
            manifest_hash=manifest_hash,
            datasets=datasets,
            payload=payload,
        ),
        encoding="utf-8",
    )
    return Phase1AArchiveFreezeResult(
        freeze_id=PHASE1A_ARCHIVE_FREEZE_ID,
        manifest_path=manifest_path,
        summary_path=summary_path,
        manifest_hash=manifest_hash,
        dataset_count=len(datasets),
        symbol_count=len({str(dataset["symbol"]) for dataset in datasets}),
    )


def _read_json_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _dataset_entry(manifest: dict[str, object]) -> dict[str, object]:
    return {
        "symbol": str(manifest["symbol"]),
        "timeframe": str(manifest["interval"]),
        "calendar_profile": "continuous",
        "window_start": str(manifest["first_bar_ts"])[:10],
        "window_end": str(manifest["last_bar_ts"])[:10],
        "daily_bars": _required_int(manifest, "daily_bars"),
        "dataset_hash": str(manifest["dataset_hash"]),
        "combined_source_sha256": str(manifest["combined_source_sha256"]),
        "data_quality_status": str(manifest["data_quality_status"]),
        "parquet_path": str(manifest["parquet_path"]),
        "conversion_manifest_path": str(manifest["manifest_path"]),
        "gate_claim_allowed": False,
    }


def _validate_datasets(datasets: Sequence[dict[str, object]]) -> None:
    symbols = tuple(str(dataset["symbol"]) for dataset in datasets)
    if tuple(sorted(symbols)) != PHASE1A_ALLOWED_SYMBOLS:
        raise ValueError("dataset symbols must match the Phase 1A allowed universe")
    for dataset in datasets:
        if dataset["timeframe"] != "1d":
            raise ValueError("Phase 1A initial freeze only allows 1d datasets")
        if dataset["window_start"] != "2020-01-01" or dataset["window_end"] != "2025-12-31":
            raise ValueError("Phase 1A initial freeze requires 2020-01-01..2025-12-31")
        if dataset["daily_bars"] != 2192:
            raise ValueError("Phase 1A initial freeze requires 2192 daily bars per symbol")
        if dataset["data_quality_status"] != "PASS":
            raise ValueError("all Phase 1A frozen datasets must have PASS data quality")


def _validate_stability_manifest(stability_manifest: dict[str, object]) -> None:
    expected = {
        "archive_only": True,
        "gate_claim_allowed": False,
        "source_manifest_count": 15,
        "row_count": 32880,
        "monitored_day_count": 2192,
        "missing_symbol_days": 0,
        "unexplained_gap_count": 0,
        "packet_status": "PACKET_READY_FOR_REVIEW",
    }
    for key, value in expected.items():
        if stability_manifest.get(key) != value:
            raise ValueError(f"archive stability manifest has invalid {key}")
    symbols = stability_manifest.get("symbols")
    if not isinstance(symbols, list) or not all(isinstance(symbol, str) for symbol in symbols):
        raise ValueError("archive stability symbols must be a string list")
    if tuple(symbols) != PHASE1A_ALLOWED_SYMBOLS:
        raise ValueError("archive stability symbols must match Phase 1A allowed universe")


def _required_int(manifest: dict[str, object], key: str) -> int:
    value = manifest[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


def _manifest_payload(
    *,
    datasets: Sequence[dict[str, object]],
    archive_stability_manifest_path: Path,
    contract_path: Path,
    stability_manifest: dict[str, object],
) -> dict[str, object]:
    return {
        "freeze_id": PHASE1A_ARCHIVE_FREEZE_ID,
        "archive_only": True,
        "gate_claim_allowed": False,
        "contract_path": contract_path.as_posix(),
        "archive_stability_manifest_path": archive_stability_manifest_path.as_posix(),
        "source_packet_id": stability_manifest["packet_id"],
        "dataset_count": len(datasets),
        "symbol_count": len({str(dataset["symbol"]) for dataset in datasets}),
        "symbols": PHASE1A_ALLOWED_SYMBOLS,
        "timeframe": "1d",
        "window_start": "2020-01-01",
        "window_end": "2025-12-31",
        "split_policy": {
            "archive_formation": {
                "label": "ARCHIVE_FORMATION",
                "window_start": "2020-01-01",
                "window_end": "2022-12-31",
            },
            "archive_validation": {
                "label": "ARCHIVE_VALIDATION",
                "window_start": "2023-01-01",
                "window_end": "2024-12-31",
            },
            "archive_holdout": {
                "label": "ARCHIVE_HOLDOUT",
                "window_start": "2025-01-01",
                "window_end": "2025-12-31",
                "read_restriction": "forbidden_before_registration_boundary",
            },
        },
        "datasets": sorted(datasets, key=lambda item: str(item["symbol"])),
        "allowed_report_labels": (
            "archive-only",
            "archive-formation",
            "archive-validation",
            "archive-holdout",
            "implementation-evidence",
            "not_phase_gate_approval",
        ),
        "forbidden_report_labels": (
            "live",
            "production",
            "capital-ready",
            "OOS performance",
            "validated alpha",
            "RDL telemetry closed",
            "K-report closed",
            "RBE activated",
        ),
        "boundary": "manifest_only_no_strategy_no_portfolio_no_performance_claim",
    }


def _render_summary(
    *,
    manifest_hash: str,
    datasets: Sequence[dict[str, object]],
    payload: dict[str, object],
) -> str:
    lines = [
        "# Phase 1A Archive Freeze Summary",
        "",
        f"Freeze ID: `{payload['freeze_id']}`",
        f"Manifest hash: `{manifest_hash}`",
        "Status: `FROZEN_FOR_P1A_MANIFEST_ONLY`",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Dataset count | {payload['dataset_count']} |",
        f"| Symbol count | {payload['symbol_count']} |",
        f"| Timeframe | {payload['timeframe']} |",
        f"| Window | {payload['window_start']} through {payload['window_end']} |",
        f"| Archive only | {payload['archive_only']} |",
        f"| Gate claim allowed | {payload['gate_claim_allowed']} |",
        "",
        "| Symbol | Dataset hash | Rows | Manifest |",
        "|---|---|---:|---|",
    ]
    for dataset in sorted(datasets, key=lambda item: str(item["symbol"])):
        lines.append(
            "| "
            f"{dataset['symbol']} | "
            f"`{dataset['dataset_hash']}` | "
            f"{dataset['daily_bars']} | "
            f"`{dataset['conversion_manifest_path']}` |"
        )
    lines.extend(
        [
            "",
            "Boundary: this freeze manifest does not implement strategies, run archive "
            "evaluation, activate live feeds, activate RDL/RBE, or make OOS/performance "
            "claims.",
        ]
    )
    return "\n".join(lines) + "\n"
