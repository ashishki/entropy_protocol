"""Unit tests for deterministic P4 regime labeler."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from entropy.governance import (
    P4_METHOD_ID,
    P4_PARAM_HASH,
    P4_WEEKLY_RESAMPLE_VERSION,
    build_p4_weekly_bars,
    label_p4_regimes,
)
from entropy.models.market import OHLCVBar

UTC_TS = datetime(2026, 5, 5, 12, 0, tzinfo=timezone.utc)
MONDAY = datetime(2020, 1, 6, tzinfo=timezone.utc)


def make_weekday_bars(closes: list[float]) -> list[OHLCVBar]:
    bars: list[OHLCVBar] = []
    for week_index, weekly_close in enumerate(closes):
        week_start = MONDAY + timedelta(days=7 * week_index)
        for day_index in range(5):
            close = weekly_close if day_index == 4 else weekly_close * 0.999
            bars.append(
                OHLCVBar(
                    timestamp=week_start + timedelta(days=day_index),
                    open=close,
                    high=max(close, weekly_close) * 1.001,
                    low=min(close, weekly_close) * 0.999,
                    close=close,
                    volume=1000.0 + week_index,
                )
            )
    return bars


def make_continuous_bars(closes: list[float]) -> list[OHLCVBar]:
    bars: list[OHLCVBar] = []
    for week_index, weekly_close in enumerate(closes):
        week_start = MONDAY + timedelta(days=7 * week_index)
        for day_index in range(7):
            close = weekly_close if day_index == 6 else weekly_close * 0.999
            bars.append(
                OHLCVBar(
                    timestamp=week_start + timedelta(days=day_index),
                    open=close,
                    high=max(close, weekly_close) * 1.001,
                    low=min(close, weekly_close) * 0.999,
                    close=close,
                    volume=1000.0 + week_index,
                )
            )
    return bars


def test_weekly_resample_uses_complete_weekday_weeks() -> None:
    bars = make_weekday_bars([100.0, 101.0])
    second_week_wednesday = MONDAY + timedelta(days=9)
    incomplete_second_week = [bar for bar in bars if bar.timestamp != second_week_wednesday]

    weekly = build_p4_weekly_bars(incomplete_second_week, calendar_profile="weekday")

    assert len(weekly) == 1
    assert weekly[0].open == bars[0].open
    assert weekly[0].high == max(bar.high for bar in bars[:5])
    assert weekly[0].low == min(bar.low for bar in bars[:5])
    assert weekly[0].close == bars[4].close
    assert weekly[0].volume == sum(bar.volume for bar in bars[:5])
    assert weekly[0].week_close_ts == bars[4].timestamp


def test_weekly_resample_supports_continuous_weeks() -> None:
    bars = make_continuous_bars([100.0])

    weekly = build_p4_weekly_bars(bars, calendar_profile="continuous")

    assert len(weekly) == 1
    assert weekly[0].week_close_ts.weekday() == 6
    assert weekly[0].close == 100.0


def test_p4_warmup_rows_are_unlabeled_until_156_completed_weeks() -> None:
    labels = label_p4_regimes(
        symbol="SPY",
        bars=make_weekday_bars([100.0] * 156),
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )

    assert len(labels) == 156
    assert all(label.p4_state == "UNLABELED" for label in labels[:155])
    assert labels[155].p4_state == "mean_reverting"


def test_p4_assigns_trending_after_warmup() -> None:
    closes = [100.0] * 143
    closes.extend(100.0 * (1.01**index) for index in range(1, 14))

    labels = label_p4_regimes(
        symbol="SPY",
        bars=make_weekday_bars(closes),
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )

    assert labels[-1].p4_state == "trending"


def test_p4_stress_has_priority() -> None:
    closes = [100.0] * 155 + [80.0]

    labels = label_p4_regimes(
        symbol="SPY",
        bars=make_weekday_bars(closes),
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )

    assert labels[-1].p4_state == "stress"


def test_p4_zero_efficiency_denominator_is_mean_reverting() -> None:
    labels = label_p4_regimes(
        symbol="SPY",
        bars=make_weekday_bars([100.0] * 160),
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )

    assert labels[-1].p4_state == "mean_reverting"


def test_p4_labels_include_vintage_metadata() -> None:
    labels = label_p4_regimes(
        symbol="SPY",
        bars=make_weekday_bars([100.0] * 156),
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )

    label = labels[-1]
    assert label.symbol == "SPY"
    assert label.calendar_profile == "weekday"
    assert label.p4_version == P4_METHOD_ID
    assert label.p4_param_hash == P4_PARAM_HASH
    assert label.label_generation_ts == UTC_TS
    assert label.dataset_hash == "dataset"
    assert label.p4_weekly_resample_version == P4_WEEKLY_RESAMPLE_VERSION


def test_p4_labeling_does_not_change_when_future_bars_are_appended() -> None:
    prefix_bars = make_weekday_bars([100.0] * 160)
    extended_bars = make_weekday_bars([100.0] * 170)

    prefix_labels = label_p4_regimes(
        symbol="SPY",
        bars=prefix_bars,
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )
    extended_labels = label_p4_regimes(
        symbol="SPY",
        bars=extended_bars,
        calendar_profile="weekday",
        dataset_hash="dataset",
        label_generation_ts=UTC_TS,
    )

    assert extended_labels[: len(prefix_labels)] == prefix_labels
