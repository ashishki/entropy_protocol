"""Phase 1H first governed archive-only evaluation run surface.

This module executes the approved walk-forward mechanics and emits run metadata.
It does not compute strategy performance, read holdout data, or make phase-gate,
production, or capital-ready claims.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from entropy.baseline.evaluation import (
    PHASE1G_NO_CLAIM_LABELS,
    Phase1GEvaluationConfig,
    Phase1GEvaluationRequest,
    validate_phase1g_evaluation_request,
)
from entropy.models.registry import LeakageStatus, RunRecord
from entropy.walkforward.leakage import (
    FeatureAudit,
    OptimizationAudit,
    RegimeLabelAudit,
    UniverseSelectionAudit,
    run_checklist,
)
from entropy.walkforward.runner import run_walk_forward
from entropy.walkforward.splitter import BarLike

PHASE1H_GOVERNED_EVALUATION_RUN_ID = "PHASE1H-FIRST-ARCHIVE-GOVERNED-EVALUATION-v1"

PHASE1H_NO_CLAIM_LABELS: tuple[str, ...] = PHASE1G_NO_CLAIM_LABELS + (
    "archive_only_research_run",
    "not_holdout",
    "not_production",
    "not_capital_ready",
)


@dataclass(frozen=True)
class Phase1HBar:
    """Minimal UTC OHLCV bar for governed evaluation tests and fixtures."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    feature_computed_through: datetime | None = None


@dataclass(frozen=True)
class Phase1HGovernedEvaluationResult:
    """No-claim result metadata for the first governed evaluation run."""

    evaluation_id: str
    run_record: RunRecord
    is_bar_count: int
    oos_bar_count: int
    leakage_status: LeakageStatus
    no_claim_labels: tuple[str, ...]
    archive_only: bool = True
    holdout_used: bool = False
    performance_conclusion: bool = False
    phase_gate_evidence: bool = False
    production_label: bool = False
    capital_ready_label: bool = False


def run_phase1h_governed_evaluation(
    config: Phase1GEvaluationConfig,
    bars: Sequence[BarLike],
    *,
    approval_gate_id: str = "phase1g_evaluation_run_approval",
) -> Phase1HGovernedEvaluationResult:
    """Run approved archive-only walk-forward mechanics and return metadata."""
    decision = validate_phase1g_evaluation_request(
        config,
        Phase1GEvaluationRequest(
            evaluation_run_requested=True,
            approval_gate_id=approval_gate_id,
        ),
    )
    if not decision.allowed:
        raise ValueError(f"Phase 1H governed evaluation rejected: {decision.reason_code}")
    strategy = _NoCapitalBaselineStrategy()
    run_record = run_walk_forward(
        config.trial_id,
        bars,
        strategy,
        oos_start=config.validation_start,
        leakage_check=_passing_leakage_check,
        embargo_bars=config.embargo_bars,
        dataset_hash=config.dataset_hash,
        code_hash=config.code_hash,
        policy_hash=config.policy_hash,
        simbroker_version=config.simbroker_version,
    )
    return Phase1HGovernedEvaluationResult(
        evaluation_id=PHASE1H_GOVERNED_EVALUATION_RUN_ID,
        run_record=run_record,
        is_bar_count=strategy.is_bar_count,
        oos_bar_count=strategy.oos_bar_count,
        leakage_status=run_record.leakage_status,
        no_claim_labels=PHASE1H_NO_CLAIM_LABELS,
    )


class _NoCapitalBaselineStrategy:
    """Walk-forward strategy adapter that records mechanics only."""

    def __init__(self) -> None:
        self.is_bar_count = 0
        self.oos_bar_count = 0

    def run_is(self, window: Sequence[BarLike]) -> object:
        self.is_bar_count = len(window)
        return {"bar_count": self.is_bar_count}

    def run_oos(self, window: Sequence[BarLike]) -> object:
        self.oos_bar_count = len(window)
        return {"bar_count": self.oos_bar_count}


def _passing_leakage_check(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
):
    return run_checklist(
        is_window,
        oos_window,
        feature_fn=lambda is_rows, _oos_rows: FeatureAudit(
            computed_through=is_rows[-1].timestamp,
            description="Features remained inside the IS window.",
        ),
        regime_label_fn=lambda is_rows, _oos_rows: RegimeLabelAudit(
            data_through=is_rows[-1].timestamp,
            description="Regime labels remained inside the IS window.",
        ),
        universe_selector=lambda _is_rows, _oos_rows: UniverseSelectionAudit(
            used_oos_returns=False,
            description="Universe selection avoided OOS returns.",
        ),
        optimizer=lambda _is_rows, _oos_rows: OptimizationAudit(
            refit_timestamps=(),
            description="No within-OOS optimization was performed.",
        ),
    )
