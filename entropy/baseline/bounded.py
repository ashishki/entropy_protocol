"""Phase 1E bounded long-only baseline logic.

The outputs in this module are formation-only observations. They are not
signals, scores, ranks, portfolio weights, backtests, or performance evidence.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import polars as pl

from entropy.baseline.formation import Phase1BFormationInputFrame
from entropy.baseline.implementation import (
    PHASE1D_FORBIDDEN_OUTPUT_COLUMNS,
    PHASE1D_IMPLEMENTATION_CONTRACT_ID,
    Phase1DImplementationContract,
    Phase1DImplementationRequest,
    validate_phase1d_implementation_request,
)
from entropy.baseline.long_only import Phase1BBaselineSurface
from entropy.evidence.phase1a_registration import PHASE1A_FORMATION_LABEL

PHASE1E_BOUNDED_BASELINE_LOGIC_ID = "PHASE1E-BOUNDED-LONG-ONLY-BASELINE-LOGIC-v1"
PHASE1E_BOUNDED_BASELINE_OUTPUT_ID = "PHASE1E-BOUNDED-OBSERVATION-OUTPUT-v1"

PHASE1E_REQUIRED_OUTPUT_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp_utc",
    "skill_family",
    "transform_family",
    "observation_name",
    "observation_status",
    "observation_value",
    "surface_id",
    "scaffold_id",
    "baseline_spec_hash",
    "logic_id",
    "no_claim_label",
)

PHASE1E_NO_CLAIM_LABELS: tuple[str, ...] = (
    "formation_only_observation",
    "not_alpha_score",
    "not_signal",
    "not_portfolio_weight",
    "not_backtest",
    "not_performance_evidence",
    "not_phase_gate_evidence",
)

_SKILL_TRANSFORMS: dict[str, tuple[str, str]] = {
    "trend_following": ("deterministic_lagged_ohlcv_transform", "lag1_close_change"),
    "breakout": ("deterministic_rolling_ohlcv_transform", "close_vs_prior_3d_high"),
    "mean_reversion": ("deterministic_rolling_ohlcv_transform", "close_vs_prior_3d_mean"),
    "volatility_filter": ("deterministic_rolling_ohlcv_transform", "lagged_range_ratio_3d_mean"),
    "regime_state_filter": ("deterministic_lagged_ohlcv_transform", "close_vs_lag3_close"),
    "cost_aware_risk_filter": ("deterministic_rolling_ohlcv_transform", "volume_vs_prior_3d_mean"),
}


@dataclass(frozen=True)
class Phase1EBoundedBaselineOutput:
    """Formation-only bounded baseline observations for one skill family."""

    output_id: str
    logic_id: str
    skill_family: str
    transform_family: str
    observation_name: str
    row_count: int
    columns: tuple[str, ...]
    output_hash: str
    no_claim_labels: tuple[str, ...]
    frame: pl.DataFrame
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False
    phase_gate_evidence: bool = False


def build_phase1e_bounded_baseline_output(
    surface: Phase1BBaselineSurface,
    formation_input: Phase1BFormationInputFrame,
    contract: Phase1DImplementationContract,
    *,
    skill_family: str,
    approval_gate_id: str = "phase1e_bounded_implementation_approval",
) -> Phase1EBoundedBaselineOutput:
    """Build formation-only observations for one registered skill family."""
    if formation_input.split_label != PHASE1A_FORMATION_LABEL:
        raise ValueError("Phase 1E bounded baseline only accepts formation input")
    if skill_family not in {skill.family for skill in surface.skill_interfaces}:
        raise ValueError("Phase 1E bounded baseline requires a registered skill family")
    if skill_family not in _SKILL_TRANSFORMS:
        raise ValueError("Phase 1E bounded baseline has no transform for skill family")
    transform_family, observation_name = _SKILL_TRANSFORMS[skill_family]
    _validate_contract_request(contract, transform_family, approval_gate_id)

    frame = _observation_frame(
        surface,
        formation_input.frame,
        skill_family=skill_family,
        transform_family=transform_family,
        observation_name=observation_name,
    )
    _validate_output_frame(frame)
    return Phase1EBoundedBaselineOutput(
        output_id=PHASE1E_BOUNDED_BASELINE_OUTPUT_ID,
        logic_id=PHASE1E_BOUNDED_BASELINE_LOGIC_ID,
        skill_family=skill_family,
        transform_family=transform_family,
        observation_name=observation_name,
        row_count=frame.height,
        columns=tuple(frame.columns),
        output_hash=_hash_dataframe(frame),
        no_claim_labels=PHASE1E_NO_CLAIM_LABELS,
        frame=frame,
    )


def build_phase1e_all_bounded_baseline_outputs(
    surface: Phase1BBaselineSurface,
    formation_input: Phase1BFormationInputFrame,
    contract: Phase1DImplementationContract,
    *,
    approval_gate_id: str = "phase1e_bounded_implementation_approval",
) -> tuple[Phase1EBoundedBaselineOutput, ...]:
    """Build formation-only observations for every registered skill family."""
    return tuple(
        build_phase1e_bounded_baseline_output(
            surface,
            formation_input,
            contract,
            skill_family=skill.family,
            approval_gate_id=approval_gate_id,
        )
        for skill in surface.skill_interfaces
    )


def _validate_contract_request(
    contract: Phase1DImplementationContract,
    transform_family: str,
    approval_gate_id: str,
) -> None:
    decision = validate_phase1d_implementation_request(
        contract,
        Phase1DImplementationRequest(
            transform_families=(transform_family,),
            requested_output_columns=PHASE1E_REQUIRED_OUTPUT_COLUMNS,
            replace_schema_only_stubs=True,
            approval_gate_id=approval_gate_id,
        ),
    )
    if not decision.allowed:
        raise ValueError(f"Phase 1E bounded baseline rejected: {decision.reason_code}")
    if contract.contract_id != PHASE1D_IMPLEMENTATION_CONTRACT_ID:
        raise ValueError("Phase 1E bounded baseline requires the Phase 1D contract")


def _observation_frame(
    surface: Phase1BBaselineSurface,
    rows: pl.DataFrame,
    *,
    skill_family: str,
    transform_family: str,
    observation_name: str,
) -> pl.DataFrame:
    sorted_rows = rows.sort(["symbol", "timestamp_utc"])
    values = _observation_expression(skill_family)
    return (
        sorted_rows.with_columns(values.alias("observation_value"))
        .select("symbol", "timestamp_utc", "observation_value")
        .with_columns(
            pl.lit(skill_family).alias("skill_family"),
            pl.lit(transform_family).alias("transform_family"),
            pl.lit(observation_name).alias("observation_name"),
            pl.lit("bounded_observation_no_signal_no_score").alias("observation_status"),
            pl.lit(surface.surface_id).alias("surface_id"),
            pl.lit(surface.scaffold_id).alias("scaffold_id"),
            pl.lit(surface.baseline_spec_hash).alias("baseline_spec_hash"),
            pl.lit(PHASE1E_BOUNDED_BASELINE_LOGIC_ID).alias("logic_id"),
            pl.lit("formation_only_observation").alias("no_claim_label"),
        )
        .select(list(PHASE1E_REQUIRED_OUTPUT_COLUMNS))
    )


def _observation_expression(skill_family: str) -> pl.Expr:
    close = pl.col("close")
    previous_close = pl.col("close").shift(1).over("symbol")
    prior_high = pl.col("high").shift(1).rolling_max(window_size=3).over("symbol")
    prior_mean_close = pl.col("close").shift(1).rolling_mean(window_size=3).over("symbol")
    lagged_range_ratio = ((pl.col("high") - pl.col("low")) / close).shift(1).over("symbol")
    prior_range_mean = lagged_range_ratio.rolling_mean(window_size=3).over("symbol")
    lag3_close = pl.col("close").shift(3).over("symbol")
    prior_mean_volume = pl.col("volume").shift(1).rolling_mean(window_size=3).over("symbol")
    expressions = {
        "trend_following": _safe_ratio(close - previous_close, previous_close),
        "breakout": _safe_ratio(close - prior_high, prior_high),
        "mean_reversion": _safe_ratio(prior_mean_close - close, prior_mean_close),
        "volatility_filter": prior_range_mean,
        "regime_state_filter": _safe_ratio(close - lag3_close, lag3_close),
        "cost_aware_risk_filter": _safe_ratio(
            pl.col("volume") - prior_mean_volume, prior_mean_volume
        ),
    }
    return expressions[skill_family].fill_null(0.0).fill_nan(0.0)


def _safe_ratio(numerator: pl.Expr, denominator: pl.Expr) -> pl.Expr:
    return pl.when(denominator.abs() > 0).then(numerator / denominator).otherwise(0.0)


def _validate_output_frame(frame: pl.DataFrame) -> None:
    missing = set(PHASE1E_REQUIRED_OUTPUT_COLUMNS).difference(frame.columns)
    if missing:
        raise ValueError("Phase 1E bounded output is missing required columns")
    forbidden = set(PHASE1D_FORBIDDEN_OUTPUT_COLUMNS).intersection(frame.columns)
    if forbidden:
        raise ValueError("Phase 1E bounded output contains forbidden columns")


def _hash_dataframe(frame: pl.DataFrame) -> str:
    canonical = json.dumps(frame.to_dicts(), sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
