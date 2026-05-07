"""Purge/embargo methodology for walk-forward evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

PURGE_EMBARGO_METHOD_ID = "PE-MAX-HORIZON-v1"


@dataclass(frozen=True)
class PurgeEmbargoSpec:
    """Inputs required to derive a conservative embargo length."""

    feature_lookback: timedelta
    label_horizon: timedelta
    max_holding_period: timedelta
    execution_lag: timedelta = timedelta(0)
    method_id: str = PURGE_EMBARGO_METHOD_ID


@dataclass(frozen=True)
class PurgeEmbargoResult:
    """Derived purge/embargo length and its governing duration."""

    embargo_duration: timedelta
    embargo_bars: int
    bar_duration: timedelta
    method_id: str
    feature_lookback: timedelta
    label_horizon: timedelta
    max_holding_period: timedelta
    execution_lag: timedelta


def derive_embargo_bars(
    *,
    spec: PurgeEmbargoSpec,
    bar_duration: timedelta,
) -> PurgeEmbargoResult:
    """Derive embargo bars from the max leak-relevant horizon.

    Formula:
    embargo_duration = max(feature_lookback, label_horizon,
                           max_holding_period, execution_lag)
    embargo_bars = ceil(embargo_duration / bar_duration)
    """
    _validate_spec(spec)
    if bar_duration <= timedelta(0):
        raise ValueError("bar_duration must be positive")
    embargo_duration = max(
        spec.feature_lookback,
        spec.label_horizon,
        spec.max_holding_period,
        spec.execution_lag,
    )
    return PurgeEmbargoResult(
        embargo_duration=embargo_duration,
        embargo_bars=_ceil_timedelta_division(embargo_duration, bar_duration),
        bar_duration=bar_duration,
        method_id=spec.method_id,
        feature_lookback=spec.feature_lookback,
        label_horizon=spec.label_horizon,
        max_holding_period=spec.max_holding_period,
        execution_lag=spec.execution_lag,
    )


def _validate_spec(spec: PurgeEmbargoSpec) -> None:
    if not spec.method_id.strip():
        raise ValueError("method_id must not be blank")
    for name, value in (
        ("feature_lookback", spec.feature_lookback),
        ("label_horizon", spec.label_horizon),
        ("max_holding_period", spec.max_holding_period),
        ("execution_lag", spec.execution_lag),
    ):
        if value < timedelta(0):
            raise ValueError(f"{name} must be nonnegative")


def _ceil_timedelta_division(numerator: timedelta, denominator: timedelta) -> int:
    numerator_us = numerator // timedelta(microseconds=1)
    denominator_us = denominator // timedelta(microseconds=1)
    return int((numerator_us + denominator_us - 1) // denominator_us)
