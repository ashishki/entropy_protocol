"""Mechanics-only Phase 1A scaffold benchmark probe."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path

import polars as pl

from entropy.evidence.phase1a_scaffold import Phase1ABaselineScaffold

PHASE1A_SCAFFOLD_PROBE_ID = "PHASE1A-SCAFFOLD-PROBE-v1"
PHASE1A_SCAFFOLD_PROBE_TASK_ID = "P1A-009"
PHASE1A_SCAFFOLD_PROBE_NO_CLAIM_LABELS = (
    "implementation_benchmark_only",
    "not_phase_gate_evidence",
    "not_oos",
    "not_performance_evidence",
)
PHASE1A_SCAFFOLD_PROBE_ALLOWED_BOUNDARIES = (
    "metadata_only",
    "formation_only",
    "synthetic_non_claim",
)


@dataclass(frozen=True)
class Phase1AScaffoldProbeConfig:
    """Configuration for a mechanics-only scaffold probe."""

    workload_id: str = "W3"
    row_count: int = 1_000
    symbol_count: int = 15
    trial_shape_count: int = 60
    data_boundary: str = "synthetic_non_claim"
    backend: str = "polars"
    command: str = "run_phase1a_scaffold_performance_probe"


@dataclass(frozen=True)
class Phase1AScaffoldProbeResult:
    """Result for one mechanics-only scaffold probe."""

    benchmark_id: str
    manifest_path: Path
    artifact_path: Path
    replay_hash: str
    wall_clock_seconds: float
    peak_memory_bytes: int
    row_count: int
    artifact_size_bytes: int
    rows_per_second: float
    trial_shapes_per_hour: float
    no_claim_labels: tuple[str, ...] = PHASE1A_SCAFFOLD_PROBE_NO_CLAIM_LABELS


def run_phase1a_scaffold_performance_probe(
    *,
    scaffold: Phase1ABaselineScaffold,
    output_dir: Path | str,
    config: Phase1AScaffoldProbeConfig | None = None,
) -> Phase1AScaffoldProbeResult:
    """Run a mechanics-only scaffold benchmark without strategy semantics."""
    probe_config = config or Phase1AScaffoldProbeConfig()
    _validate_config(probe_config)

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    artifact_path = root / "PHASE1A_SCAFFOLD_PROBE_SYNTHETIC.parquet"
    manifest_path = root / "PHASE1A_SCAFFOLD_PROBE_MANIFEST.json"

    tracemalloc.start()
    start = time.perf_counter()
    frame = _build_probe_frame(scaffold=scaffold, config=probe_config)
    frame.write_parquet(artifact_path)
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    elapsed = time.perf_counter() - start
    tracemalloc.stop()
    del current_memory

    artifact_size = artifact_path.stat().st_size
    replay_hash = _replay_hash(scaffold=scaffold, config=probe_config)
    rows_per_second = probe_config.row_count / elapsed if elapsed > 0.0 else 0.0
    trial_shapes_per_hour = (
        probe_config.trial_shape_count / (elapsed / 3600.0) if elapsed > 0.0 else 0.0
    )
    payload = _manifest_payload(
        scaffold=scaffold,
        config=probe_config,
        artifact_path=artifact_path,
        artifact_size=artifact_size,
        replay_hash=replay_hash,
        wall_clock_seconds=elapsed,
        peak_memory_bytes=peak_memory,
        rows_per_second=rows_per_second,
        trial_shapes_per_hour=trial_shapes_per_hour,
    )
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return Phase1AScaffoldProbeResult(
        benchmark_id=PHASE1A_SCAFFOLD_PROBE_ID,
        manifest_path=manifest_path,
        artifact_path=artifact_path,
        replay_hash=replay_hash,
        wall_clock_seconds=elapsed,
        peak_memory_bytes=peak_memory,
        row_count=probe_config.row_count,
        artifact_size_bytes=artifact_size,
        rows_per_second=rows_per_second,
        trial_shapes_per_hour=trial_shapes_per_hour,
    )


def _build_probe_frame(
    *,
    scaffold: Phase1ABaselineScaffold,
    config: Phase1AScaffoldProbeConfig,
) -> pl.DataFrame:
    row_index = pl.int_range(0, config.row_count, eager=True)
    skill_count = len(scaffold.skill_placeholders)
    return pl.DataFrame({"row_index": row_index}).with_columns(
        (pl.col("row_index") % config.symbol_count).alias("symbol_slot"),
        (pl.col("row_index") % skill_count).alias("skill_slot"),
        pl.lit(scaffold.scaffold_id).alias("scaffold_id"),
        pl.lit(scaffold.baseline_spec_hash).alias("baseline_spec_hash"),
        pl.lit(config.workload_id).alias("workload_id"),
        pl.lit(config.data_boundary).alias("data_boundary"),
    )


def _manifest_payload(
    *,
    scaffold: Phase1ABaselineScaffold,
    config: Phase1AScaffoldProbeConfig,
    artifact_path: Path,
    artifact_size: int,
    replay_hash: str,
    wall_clock_seconds: float,
    peak_memory_bytes: int,
    rows_per_second: float,
    trial_shapes_per_hour: float,
) -> dict[str, object]:
    return {
        "benchmark_id": PHASE1A_SCAFFOLD_PROBE_ID,
        "task_id": PHASE1A_SCAFFOLD_PROBE_TASK_ID,
        "data_boundary": config.data_boundary,
        "command": config.command,
        "environment": _environment_summary(),
        "backend": config.backend,
        "wall_clock_seconds": wall_clock_seconds,
        "peak_memory_bytes": peak_memory_bytes,
        "rows_processed": config.row_count,
        "rows_per_second": rows_per_second,
        "trial_shape_count": config.trial_shape_count,
        "trial_shapes_per_hour": trial_shapes_per_hour,
        "artifact_path": artifact_path.as_posix(),
        "artifact_bytes_written": artifact_size,
        "replay_hash": replay_hash,
        "code_hash": _code_hash(),
        "policy_hash": _policy_hash(scaffold),
        "input_hashes": {
            "baseline_spec_hash": scaffold.baseline_spec_hash,
            "validation_registration_hash": scaffold.validation_registration_hash,
            "boundary_manifest_hash": scaffold.boundary_manifest_hash,
        },
        "workload": asdict(config),
        "no_claim_labels": list(PHASE1A_SCAFFOLD_PROBE_NO_CLAIM_LABELS),
        "forbidden_outputs_absent": True,
    }


def _validate_config(config: Phase1AScaffoldProbeConfig) -> None:
    if config.backend != "polars":
        raise ValueError("P1A-009 scaffold probe currently supports only polars backend")
    if config.data_boundary not in PHASE1A_SCAFFOLD_PROBE_ALLOWED_BOUNDARIES:
        raise ValueError("P1A-009 scaffold probe data_boundary is not allowed")
    if config.row_count < 1:
        raise ValueError("row_count must be positive")
    if config.symbol_count < 1:
        raise ValueError("symbol_count must be positive")
    if config.trial_shape_count < 1:
        raise ValueError("trial_shape_count must be positive")
    if not config.workload_id.strip():
        raise ValueError("workload_id must not be blank")
    if not config.command.strip():
        raise ValueError("command must not be blank")


def _environment_summary() -> dict[str, object]:
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "polars_version": pl.__version__,
    }


def _code_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _policy_hash(scaffold: Phase1ABaselineScaffold) -> str:
    return _hash_payload(
        {
            "workload_boundary": scaffold.workload_boundary,
            "archive_only": scaffold.archive_only,
            "gate_claim_allowed": scaffold.gate_claim_allowed,
            "no_claim_labels": PHASE1A_SCAFFOLD_PROBE_NO_CLAIM_LABELS,
        }
    )


def _replay_hash(
    *,
    scaffold: Phase1ABaselineScaffold,
    config: Phase1AScaffoldProbeConfig,
) -> str:
    return _hash_payload(
        {
            "benchmark_id": PHASE1A_SCAFFOLD_PROBE_ID,
            "scaffold_id": scaffold.scaffold_id,
            "baseline_spec_hash": scaffold.baseline_spec_hash,
            "validation_registration_hash": scaffold.validation_registration_hash,
            "boundary_manifest_hash": scaffold.boundary_manifest_hash,
            "placeholder_ids": [item.placeholder_id for item in scaffold.skill_placeholders],
            "config": asdict(config),
        }
    )


def _hash_payload(payload: dict[str, object]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
