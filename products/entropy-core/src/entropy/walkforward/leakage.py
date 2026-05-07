"""Machine-checkable leakage audit checklist for walk-forward runs."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from entropy.walkforward.splitter import BarLike


class CheckStatus(str, Enum):
    """PASS/FAIL status for one leakage check."""

    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class FeatureAudit:
    """Evidence for feature computation boundary checks."""

    computed_through: datetime | None = None
    description: str = ""


@dataclass(frozen=True)
class RegimeLabelAudit:
    """Evidence for regime-label look-ahead checks."""

    data_through: datetime | None = None
    description: str = ""


@dataclass(frozen=True)
class UniverseSelectionAudit:
    """Evidence for universe-selection bias checks."""

    used_oos_returns: bool = False
    description: str = ""


@dataclass(frozen=True)
class OptimizationAudit:
    """Evidence for within-OOS optimization checks."""

    refit_timestamps: tuple[datetime, ...] = ()
    description: str = ""


@dataclass(frozen=True)
class LeakageCheckResult:
    """Single leakage check verdict."""

    status: CheckStatus
    description: str


@dataclass(frozen=True)
class LeakageReport:
    """Full four-check leakage report."""

    normalization_leakage: LeakageCheckResult
    regime_label_lookahead: LeakageCheckResult
    universe_selection_bias: LeakageCheckResult
    within_window_optimization: LeakageCheckResult

    @property
    def total_check_count(self) -> int:
        return 4

    @property
    def overall_status(self) -> CheckStatus:
        if all(result.status is CheckStatus.PASS for result in self.checks):
            return CheckStatus.PASS
        return CheckStatus.FAIL

    @property
    def checks(self) -> tuple[LeakageCheckResult, ...]:
        return (
            self.normalization_leakage,
            self.regime_label_lookahead,
            self.universe_selection_bias,
            self.within_window_optimization,
        )


FeatureFn = Callable[[Sequence[BarLike], Sequence[BarLike]], FeatureAudit]
RegimeLabelFn = Callable[[Sequence[BarLike], Sequence[BarLike]], RegimeLabelAudit]
UniverseSelector = Callable[[Sequence[BarLike], Sequence[BarLike]], UniverseSelectionAudit]
Optimizer = Callable[[Sequence[BarLike], Sequence[BarLike]], OptimizationAudit]


def run_checklist(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
    *,
    feature_fn: FeatureFn | None = None,
    regime_label_fn: RegimeLabelFn | None = None,
    universe_selector: UniverseSelector | None = None,
    optimizer: Optimizer | None = None,
) -> LeakageReport:
    """Run all four Phase 0 leakage checks over an IS/OOS pair."""

    if not is_window:
        raise ValueError("is_window must be nonempty")
    if not oos_window:
        raise ValueError("oos_window must be nonempty")
    oos_start = _oos_start(oos_window)

    return LeakageReport(
        normalization_leakage=_check_normalization(
            feature_fn,
            is_window,
            oos_window,
            oos_start,
        ),
        regime_label_lookahead=_check_regime_label(
            regime_label_fn,
            is_window,
            oos_window,
            oos_start,
        ),
        universe_selection_bias=_check_universe_selection(
            universe_selector,
            is_window,
            oos_window,
        ),
        within_window_optimization=_check_optimizer(
            optimizer,
            is_window,
            oos_window,
            oos_start,
        ),
    )


def _check_normalization(
    feature_fn: FeatureFn | None,
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
    oos_start: datetime,
) -> LeakageCheckResult:
    if feature_fn is None:
        return _fail("Normalization leakage check was not supplied.")
    evidence = feature_fn(is_window, oos_window)
    if evidence.computed_through is not None and evidence.computed_through >= oos_start:
        return _fail(
            evidence.description or "Feature computation used data at or after the OOS start."
        )
    return _pass(evidence.description or "Feature computation stayed within IS data.")


def _check_regime_label(
    regime_label_fn: RegimeLabelFn | None,
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
    oos_start: datetime,
) -> LeakageCheckResult:
    if regime_label_fn is None:
        return _fail("Regime label look-ahead check was not supplied.")
    evidence = regime_label_fn(is_window, oos_window)
    if evidence.data_through is not None and evidence.data_through >= oos_start:
        return _fail(evidence.description or "Regime label used data at or after the OOS start.")
    return _pass(evidence.description or "Regime labels stayed within IS data.")


def _check_universe_selection(
    universe_selector: UniverseSelector | None,
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> LeakageCheckResult:
    if universe_selector is None:
        return _fail("Universe selection bias check was not supplied.")
    evidence = universe_selector(is_window, oos_window)
    if evidence.used_oos_returns:
        return _fail(evidence.description or "Universe selection used OOS return data.")
    return _pass(evidence.description or "Universe selection avoided OOS return data.")


def _check_optimizer(
    optimizer: Optimizer | None,
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
    oos_start: datetime,
) -> LeakageCheckResult:
    if optimizer is None:
        return _fail("Within-window optimization check was not supplied.")
    evidence = optimizer(is_window, oos_window)
    if any(timestamp >= oos_start for timestamp in evidence.refit_timestamps):
        return _fail(evidence.description or "Optimizer refit parameters inside the OOS window.")
    return _pass(evidence.description or "Optimizer did not refit inside OOS.")


def _oos_start(oos_window: Sequence[BarLike]) -> datetime:
    return min(bar.timestamp for bar in oos_window)


def _pass(description: str) -> LeakageCheckResult:
    return LeakageCheckResult(status=CheckStatus.PASS, description=description)


def _fail(description: str) -> LeakageCheckResult:
    return LeakageCheckResult(status=CheckStatus.FAIL, description=description)
