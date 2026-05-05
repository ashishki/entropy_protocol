"""Deterministic P4 weekly regime labeler."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import log, sqrt
from statistics import stdev
from typing import Literal, Sequence

from entropy.models.market import OHLCVBar

P4_METHOD_ID = "P4-RBL-v1"
P4_WEEKLY_RESAMPLE_VERSION = "p4_weekly_resample_v1"
P4_VERSION = P4_METHOD_ID
P4_PARAM_HASH = hashlib.sha256(
    json.dumps(
        {
            "method_id": P4_METHOD_ID,
            "weekly_resample_version": P4_WEEKLY_RESAMPLE_VERSION,
            "stress": {
                "r_4w_lte": -0.08,
                "dd_26w_lte": -0.15,
                "vol_pct_156w_gte": 0.80,
                "vol_stress_r_4w_lt": -0.03,
            },
            "trending": {"abs_r_13w_gte": 0.08, "eff_13w_gte": 0.35},
            "warmup_completed_weeks": 156,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()

CalendarProfile = Literal["weekday", "continuous"]
P4State = Literal["UNLABELED", "stress", "trending", "mean_reverting"]


@dataclass(frozen=True)
class WeeklyBar:
    """Complete weekly OHLCV bar built from daily UTC bars."""

    week_close_ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class P4Label:
    """Vintage-locked P4 label output."""

    symbol: str
    calendar_profile: CalendarProfile
    week_close_ts: datetime
    p4_state: P4State
    p4_version: str
    p4_param_hash: str
    label_generation_ts: datetime
    dataset_hash: str
    p4_weekly_resample_version: str


def label_p4_regimes(
    *,
    symbol: str,
    bars: Sequence[OHLCVBar],
    calendar_profile: CalendarProfile,
    dataset_hash: str,
    label_generation_ts: datetime,
) -> tuple[P4Label, ...]:
    """Assign deterministic `P4-RBL-v1` weekly labels from UTC daily bars."""
    if not symbol.strip():
        raise ValueError("symbol must not be blank")
    if not dataset_hash.strip():
        raise ValueError("dataset_hash must not be blank")
    _require_utc(label_generation_ts, "label_generation_ts")

    weekly_bars = build_p4_weekly_bars(bars, calendar_profile=calendar_profile)
    weekly_returns = _weekly_log_returns(weekly_bars)
    vol_13w_values = {
        index: _vol_13w(weekly_returns, index) for index in range(13, len(weekly_bars))
    }

    labels: list[P4Label] = []
    for index, weekly_bar in enumerate(weekly_bars):
        state: P4State = "UNLABELED"
        if index >= 155:
            state = _classify_week(weekly_bars, weekly_returns, vol_13w_values, index)
        labels.append(
            P4Label(
                symbol=symbol,
                calendar_profile=calendar_profile,
                week_close_ts=weekly_bar.week_close_ts,
                p4_state=state,
                p4_version=P4_VERSION,
                p4_param_hash=P4_PARAM_HASH,
                label_generation_ts=label_generation_ts,
                dataset_hash=dataset_hash,
                p4_weekly_resample_version=P4_WEEKLY_RESAMPLE_VERSION,
            )
        )
    return tuple(labels)


def build_p4_weekly_bars(
    bars: Sequence[OHLCVBar],
    *,
    calendar_profile: CalendarProfile,
) -> tuple[WeeklyBar, ...]:
    """Build complete P4 weekly bars using the locked resampling rule."""
    if calendar_profile not in ("weekday", "continuous"):
        raise ValueError("calendar_profile must be 'weekday' or 'continuous'")
    if not bars:
        return ()
    ordered_bars = tuple(sorted(bars, key=lambda bar: bar.timestamp))
    _validate_strictly_increasing_daily_bars(ordered_bars)

    weeks: dict[tuple[int, int], list[OHLCVBar]] = {}
    for bar in ordered_bars:
        iso = bar.timestamp.isocalendar()
        weeks.setdefault((iso.year, iso.week), []).append(bar)

    weekly_bars: list[WeeklyBar] = []
    required_weekdays = {0, 1, 2, 3, 4} if calendar_profile == "weekday" else set(range(7))
    for week_key in sorted(weeks):
        week_bars = sorted(weeks[week_key], key=lambda bar: bar.timestamp)
        weekdays = {bar.timestamp.weekday() for bar in week_bars}
        if weekdays != required_weekdays:
            continue
        if len(week_bars) != len(required_weekdays):
            raise ValueError("duplicate daily bars found in a P4 week")
        weekly_bars.append(
            WeeklyBar(
                week_close_ts=week_bars[-1].timestamp,
                open=week_bars[0].open,
                high=max(bar.high for bar in week_bars),
                low=min(bar.low for bar in week_bars),
                close=week_bars[-1].close,
                volume=sum(bar.volume for bar in week_bars),
            )
        )
    return tuple(weekly_bars)


def _classify_week(
    weekly_bars: Sequence[WeeklyBar],
    weekly_returns: Sequence[float],
    vol_13w_values: dict[int, float],
    index: int,
) -> P4State:
    close = weekly_bars[index].close
    r_4w = log(close / weekly_bars[index - 4].close)
    r_13w = log(close / weekly_bars[index - 13].close)
    dd_26w = close / max(bar.close for bar in weekly_bars[index - 25 : index + 1]) - 1
    current_vol = vol_13w_values[index]
    trailing_vols = [
        vol_13w_values[vol_index]
        for vol_index in range(max(13, index - 155), index + 1)
        if vol_index in vol_13w_values
    ]
    vol_pct_156w = _weak_percentile_rank(current_vol, trailing_vols)
    eff_13w = _efficiency_13w(r_13w, weekly_returns, index)

    if r_4w <= -0.08 or dd_26w <= -0.15 or (vol_pct_156w >= 0.80 and r_4w < -0.03):
        return "stress"
    if abs(r_13w) >= 0.08 and eff_13w >= 0.35:
        return "trending"
    return "mean_reverting"


def _weekly_log_returns(weekly_bars: Sequence[WeeklyBar]) -> tuple[float, ...]:
    return tuple(
        log(current.close / previous.close)
        for previous, current in zip(weekly_bars, weekly_bars[1:])
    )


def _vol_13w(weekly_returns: Sequence[float], index: int) -> float:
    returns = weekly_returns[index - 13 : index]
    return stdev(returns) * sqrt(52)


def _efficiency_13w(r_13w: float, weekly_returns: Sequence[float], index: int) -> float:
    denominator = sum(abs(value) for value in weekly_returns[index - 13 : index])
    if denominator == 0:
        return 0.0
    return abs(r_13w) / denominator


def _weak_percentile_rank(current: float, values: Sequence[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(1 for value in values if value <= current) / len(values)


def _validate_strictly_increasing_daily_bars(bars: Sequence[OHLCVBar]) -> None:
    previous_date = None
    for previous, current in zip(bars, bars[1:]):
        if current.timestamp <= previous.timestamp:
            raise ValueError("bars must have strictly increasing timestamps")
    for bar in bars:
        _require_utc(bar.timestamp, "bar timestamp")
        current_date = bar.timestamp.date()
        if previous_date is not None and current_date <= previous_date:
            raise ValueError("P4 input must contain at most one daily bar per UTC date")
        previous_date = current_date


def _require_utc(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"{name} must be timezone-aware UTC")
