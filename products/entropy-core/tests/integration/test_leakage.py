"""Integration tests for the walk-forward leakage checklist."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from entropy.walkforward import (
    CheckStatus,
    FeatureAudit,
    OptimizationAudit,
    RegimeLabelAudit,
    UniverseSelectionAudit,
    run_checklist,
)
from entropy.walkforward.splitter import BarLike


@dataclass(frozen=True)
class AuditBar:
    timestamp: datetime
    close: float
    symbol: str = "BTC-USD"


def make_windows() -> tuple[tuple[AuditBar, ...], tuple[AuditBar, ...]]:
    anchor = datetime(2026, 1, 1, tzinfo=timezone.utc)
    bars = tuple(
        AuditBar(
            timestamp=anchor + timedelta(hours=index),
            close=100.0 + index,
        )
        for index in range(10)
    )
    return bars[:6], bars[6:]


def normalize_on_full_series(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> FeatureAudit:
    return FeatureAudit(
        computed_through=oos_window[-1].timestamp,
        description="normalization used full series including OOS bars",
    )


def normalize_on_is_only(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> FeatureAudit:
    return FeatureAudit(
        computed_through=is_window[-1].timestamp,
        description="normalization used IS bars only",
    )


def label_using_post_oos_data(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> RegimeLabelAudit:
    return RegimeLabelAudit(
        data_through=oos_window[1].timestamp,
        description="regime label used post-OOS-start data",
    )


def label_using_is_only(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> RegimeLabelAudit:
    return RegimeLabelAudit(
        data_through=is_window[-1].timestamp,
        description="regime label used IS bars only",
    )


def select_using_oos_returns(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> UniverseSelectionAudit:
    return UniverseSelectionAudit(
        used_oos_returns=True,
        description="symbol universe selected with OOS returns",
    )


def select_without_oos_returns(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> UniverseSelectionAudit:
    return UniverseSelectionAudit(
        used_oos_returns=False,
        description="symbol universe selected before OOS",
    )


def refit_inside_oos(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> OptimizationAudit:
    return OptimizationAudit(
        refit_timestamps=(oos_window[0].timestamp,),
        description="parameters were refit inside OOS",
    )


def fit_before_oos(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
) -> OptimizationAudit:
    return OptimizationAudit(
        refit_timestamps=(is_window[-1].timestamp,),
        description="parameters were fixed before OOS",
    )


def test_leakage_normalization_detected() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        feature_fn=normalize_on_full_series,
    )

    assert report.normalization_leakage.status is CheckStatus.FAIL
    assert report.normalization_leakage.description
    assert report.overall_status is CheckStatus.FAIL


def test_leakage_normalization_clean() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        feature_fn=normalize_on_is_only,
    )

    assert report.normalization_leakage.status is CheckStatus.PASS


def test_leakage_regime_lookahead_detected() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        regime_label_fn=label_using_post_oos_data,
    )

    assert report.regime_label_lookahead.status is CheckStatus.FAIL
    assert report.regime_label_lookahead.description
    assert report.overall_status is CheckStatus.FAIL


def test_leakage_regime_lookahead_clean() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        regime_label_fn=label_using_is_only,
    )

    assert report.regime_label_lookahead.status is CheckStatus.PASS


def test_leakage_universe_selection_detected() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        universe_selector=select_using_oos_returns,
    )

    assert report.universe_selection_bias.status is CheckStatus.FAIL
    assert report.universe_selection_bias.description
    assert report.overall_status is CheckStatus.FAIL


def test_leakage_universe_selection_clean() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        universe_selector=select_without_oos_returns,
    )

    assert report.universe_selection_bias.status is CheckStatus.PASS


def test_leakage_within_window_optimization_detected() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        optimizer=refit_inside_oos,
    )

    assert report.within_window_optimization.status is CheckStatus.FAIL
    assert report.within_window_optimization.description
    assert report.overall_status is CheckStatus.FAIL


def test_leakage_within_window_optimization_clean() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        optimizer=fit_before_oos,
    )

    assert report.within_window_optimization.status is CheckStatus.PASS


def test_full_leakage_checklist() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(
        is_window,
        oos_window,
        feature_fn=normalize_on_is_only,
        regime_label_fn=label_using_is_only,
        universe_selector=select_without_oos_returns,
        optimizer=fit_before_oos,
    )

    assert report.total_check_count == 4
    assert report.overall_status is CheckStatus.PASS
    assert all(check.status is CheckStatus.PASS for check in report.checks)
    assert all(check.description for check in report.checks)


def test_full_leakage_checklist_requires_all_checks() -> None:
    is_window, oos_window = make_windows()

    report = run_checklist(is_window, oos_window)

    assert report.total_check_count == 4
    assert report.overall_status is CheckStatus.FAIL
    assert all(check.status is CheckStatus.FAIL for check in report.checks)
    assert all("not supplied" in check.description for check in report.checks)
