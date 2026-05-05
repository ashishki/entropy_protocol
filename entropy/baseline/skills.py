"""No-claim skill interface stubs for Phase 1B baseline readiness."""

from __future__ import annotations

import time
import tracemalloc
from dataclasses import dataclass

import polars as pl

from entropy.baseline.formation import Phase1BFormationInputFrame, prepare_phase1b_formation_input
from entropy.baseline.long_only import (
    PHASE1B_BASELINE_NO_CLAIM_LABELS,
    PHASE1B_FORBIDDEN_OUTPUT_COLUMNS,
    PHASE1B_REQUIRED_OUTPUT_COLUMNS,
    Phase1BBaselineSurface,
)

PHASE1B_SKILL_STUB_OUTPUT_ID = "PHASE1B-SKILL-STUB-OUTPUT-v1"
PHASE1B_BASELINE_BENCHMARK_ID = "PHASE1B-BASELINE-SURFACE-BENCHMARK-v1"


@dataclass(frozen=True)
class Phase1BSkillStubOutput:
    """Schema-only output for one Phase 1B skill interface."""

    output_id: str
    skill_family: str
    row_count: int
    columns: tuple[str, ...]
    no_claim_labels: tuple[str, ...]
    frame: pl.DataFrame
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False


@dataclass(frozen=True)
class Phase1BBaselineBenchmarkResult:
    """Mechanics-only benchmark for Phase 1B surface + formation + stubs."""

    benchmark_id: str
    row_count: int
    skill_family_count: int
    output_row_count: int
    wall_clock_seconds: float
    peak_memory_bytes: int
    backend: str = "python_polars_compatible"
    no_claim_labels: tuple[str, ...] = PHASE1B_BASELINE_NO_CLAIM_LABELS
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False


def build_phase1b_skill_stub_output(
    surface: Phase1BBaselineSurface,
    formation_input: Phase1BFormationInputFrame,
    *,
    skill_family: str,
) -> Phase1BSkillStubOutput:
    """Build schema-only no-claim rows for one registered skill family."""
    if skill_family not in {skill.family for skill in surface.skill_interfaces}:
        raise ValueError("Phase 1B skill stub requires a registered skill family")
    frame = formation_input.frame.select("symbol", "timestamp_utc").with_columns(
        pl.lit(skill_family).alias("skill_family"),
        pl.lit("schema_only_no_signal_no_score_no_weight").alias("observation_status"),
        pl.lit(surface.surface_id).alias("surface_id"),
        pl.lit(surface.scaffold_id).alias("scaffold_id"),
        pl.lit(surface.baseline_spec_hash).alias("baseline_spec_hash"),
        pl.lit("not_alpha_logic").alias("no_claim_label"),
    )
    _validate_stub_output_columns(frame)
    return Phase1BSkillStubOutput(
        output_id=PHASE1B_SKILL_STUB_OUTPUT_ID,
        skill_family=skill_family,
        row_count=frame.height,
        columns=tuple(frame.columns),
        no_claim_labels=PHASE1B_BASELINE_NO_CLAIM_LABELS,
        frame=frame,
    )


def build_phase1b_all_skill_stub_outputs(
    surface: Phase1BBaselineSurface,
    formation_input: Phase1BFormationInputFrame,
) -> tuple[Phase1BSkillStubOutput, ...]:
    """Build schema-only outputs for every registered skill family."""
    return tuple(
        build_phase1b_skill_stub_output(
            surface,
            formation_input,
            skill_family=skill.family,
        )
        for skill in surface.skill_interfaces
    )


def run_phase1b_baseline_surface_benchmark(
    surface: Phase1BBaselineSurface,
    *,
    row_count: int = 1_000,
) -> Phase1BBaselineBenchmarkResult:
    """Run a mechanics-only synthetic benchmark for the Phase 1B baseline surface."""
    if row_count <= 0:
        raise ValueError("Phase 1B benchmark row_count must be positive")
    synthetic = _synthetic_formation_rows(row_count)
    tracemalloc.start()
    start = time.perf_counter()
    formation = prepare_phase1b_formation_input(surface, synthetic)
    outputs = build_phase1b_all_skill_stub_outputs(surface, formation)
    wall_clock_seconds = time.perf_counter() - start
    _, peak_memory_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return Phase1BBaselineBenchmarkResult(
        benchmark_id=PHASE1B_BASELINE_BENCHMARK_ID,
        row_count=formation.row_count,
        skill_family_count=len(outputs),
        output_row_count=sum(output.row_count for output in outputs),
        wall_clock_seconds=wall_clock_seconds,
        peak_memory_bytes=peak_memory_bytes,
    )


def _validate_stub_output_columns(frame: pl.DataFrame) -> None:
    missing = set(PHASE1B_REQUIRED_OUTPUT_COLUMNS).difference(frame.columns)
    if missing:
        raise ValueError("Phase 1B skill stub output is missing required columns")
    forbidden = set(PHASE1B_FORBIDDEN_OUTPUT_COLUMNS).intersection(frame.columns)
    if forbidden:
        raise ValueError("Phase 1B skill stub output contains forbidden columns")


def _synthetic_formation_rows(row_count: int) -> pl.DataFrame:
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
    return pl.DataFrame(
        {
            "symbol": [symbols[index % len(symbols)] for index in range(row_count)],
            "timestamp_utc": [f"2021-01-{(index % 28) + 1:02d}T00:00:00Z" for index in range(row_count)],
            "open": [100.0 + float(index % 10) for index in range(row_count)],
            "high": [101.0 + float(index % 10) for index in range(row_count)],
            "low": [99.0 + float(index % 10) for index in range(row_count)],
            "close": [100.5 + float(index % 10) for index in range(row_count)],
            "volume": [1_000.0 + float(index) for index in range(row_count)],
            "dataset_hash": ["synthetic_non_claim_hash" for _ in range(row_count)],
        }
    )
