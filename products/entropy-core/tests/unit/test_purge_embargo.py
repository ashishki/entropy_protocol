"""Unit tests for purge/embargo methodology."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest

from entropy.walkforward import (
    PURGE_EMBARGO_METHOD_ID,
    PurgeEmbargoSpec,
    derive_embargo_bars,
    split,
)


@dataclass(frozen=True)
class Bar:
    timestamp: datetime


def make_bars(count: int, *, step: timedelta) -> list[Bar]:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [Bar(timestamp=start + index * step) for index in range(count)]


def test_derive_embargo_uses_maximum_leak_relevant_horizon() -> None:
    spec = PurgeEmbargoSpec(
        feature_lookback=timedelta(days=2),
        label_horizon=timedelta(days=4),
        max_holding_period=timedelta(days=15),
        execution_lag=timedelta(hours=8),
    )

    result = derive_embargo_bars(spec=spec, bar_duration=timedelta(hours=4))

    assert result.method_id == PURGE_EMBARGO_METHOD_ID
    assert result.embargo_duration == timedelta(days=15)
    assert result.embargo_bars == 90
    assert result.max_holding_period == timedelta(days=15)


def test_derive_embargo_ceil_converts_partial_bars() -> None:
    spec = PurgeEmbargoSpec(
        feature_lookback=timedelta(hours=25),
        label_horizon=timedelta(hours=0),
        max_holding_period=timedelta(hours=0),
    )

    result = derive_embargo_bars(spec=spec, bar_duration=timedelta(days=1))

    assert result.embargo_duration == timedelta(hours=25)
    assert result.embargo_bars == 2


def test_derive_embargo_allows_zero_duration() -> None:
    spec = PurgeEmbargoSpec(
        feature_lookback=timedelta(0),
        label_horizon=timedelta(0),
        max_holding_period=timedelta(0),
    )

    result = derive_embargo_bars(spec=spec, bar_duration=timedelta(hours=4))

    assert result.embargo_duration == timedelta(0)
    assert result.embargo_bars == 0


def test_derive_embargo_rejects_negative_inputs() -> None:
    spec = PurgeEmbargoSpec(
        feature_lookback=timedelta(days=-1),
        label_horizon=timedelta(0),
        max_holding_period=timedelta(0),
    )

    with pytest.raises(ValueError, match="feature_lookback"):
        derive_embargo_bars(spec=spec, bar_duration=timedelta(hours=4))


def test_derive_embargo_rejects_nonpositive_bar_duration() -> None:
    spec = PurgeEmbargoSpec(
        feature_lookback=timedelta(days=1),
        label_horizon=timedelta(0),
        max_holding_period=timedelta(0),
    )

    with pytest.raises(ValueError, match="bar_duration"):
        derive_embargo_bars(spec=spec, bar_duration=timedelta(0))


def test_derived_embargo_integrates_with_splitter() -> None:
    bars = make_bars(120, step=timedelta(hours=4))
    oos_start = bars[100].timestamp
    spec = PurgeEmbargoSpec(
        feature_lookback=timedelta(days=2),
        label_horizon=timedelta(days=1),
        max_holding_period=timedelta(hours=12),
    )
    derived = derive_embargo_bars(spec=spec, bar_duration=timedelta(hours=4))

    result = split(bars, oos_start, embargo_bars=derived.embargo_bars)

    assert derived.embargo_bars == 12
    assert len(result.embargo_window) == 12
    assert result.is_cutoff == oos_start - timedelta(days=2)
