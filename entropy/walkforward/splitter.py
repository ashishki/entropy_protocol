"""Strict IS/OOS splitting helpers for walk-forward evaluation."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Generic, Protocol, TypeVar


class LeakageError(ValueError):
    """Raised when in-sample data contains future-derived feature values."""


class BarLike(Protocol):
    """Minimal bar contract required by the splitter."""

    timestamp: datetime


TBar = TypeVar("TBar", bound=BarLike)


@dataclass(frozen=True)
class SplitResult(Generic[TBar]):
    """Walk-forward split result.

    Iteration preserves the historical two-value unpacking style:
    ``is_window, oos_window = split(...)``.
    """

    is_window: tuple[TBar, ...]
    oos_window: tuple[TBar, ...]
    embargo_window: tuple[TBar, ...]
    is_cutoff: datetime
    oos_start: datetime
    embargo_bars: int
    bar_duration: timedelta

    def __iter__(self) -> Iterator[tuple[TBar, ...]]:
        yield self.is_window
        yield self.oos_window


def split(
    bars: Sequence[TBar],
    oos_start: datetime,
    *,
    embargo_bars: int = 0,
) -> SplitResult[TBar]:
    """Split bars into IS and OOS windows with a pre-OOS embargo.

    Embargo formula assumption: pending final independent purge/embargo
    derivation, Phase 0 treats ``embargo_bars`` as N consecutive bars
    immediately preceding the first OOS bar. This preserves a strict timestamp
    cutoff and excludes exactly N bars from both IS and OOS when the input bars
    are regular, validated OHLCV bars.
    """

    if embargo_bars < 0:
        raise ValueError("embargo_bars must be nonnegative")
    if not bars:
        raise ValueError("bars must be nonempty")
    _require_utc(oos_start, "oos_start")

    timestamps = [_timestamp(bar) for bar in bars]
    _validate_strictly_increasing(timestamps)

    oos_index = _first_oos_index(timestamps, oos_start)
    if oos_index == 0:
        raise ValueError("IS window would be empty")

    bar_duration = _infer_bar_duration(timestamps, oos_index)
    is_end_index = oos_index - embargo_bars
    if is_end_index <= 0:
        raise ValueError("IS window would be empty after embargo")

    is_window = tuple(bars[:is_end_index])
    embargo_window = tuple(bars[is_end_index:oos_index])
    oos_window = tuple(bars[oos_index:])
    if not oos_window:
        raise ValueError("OOS window would be empty")

    is_cutoff = oos_start if embargo_bars == 0 else _timestamp(bars[is_end_index])
    _validate_no_window_overlap(is_window, oos_window, is_cutoff, oos_start)
    _validate_no_feature_leakage(is_window, is_cutoff)

    return SplitResult(
        is_window=is_window,
        oos_window=oos_window,
        embargo_window=embargo_window,
        is_cutoff=is_cutoff,
        oos_start=oos_start,
        embargo_bars=embargo_bars,
        bar_duration=bar_duration,
    )


def _timestamp(bar: BarLike) -> datetime:
    value = bar.timestamp
    if not isinstance(value, datetime):
        raise TypeError("bar timestamp must be a datetime")
    _require_utc(value, "bar timestamp")
    return value


def _require_utc(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"{name} must be timezone-aware UTC")


def _validate_strictly_increasing(timestamps: Sequence[datetime]) -> None:
    for previous, current in zip(timestamps, timestamps[1:]):
        if current <= previous:
            raise ValueError("bars must be sorted by strictly increasing timestamp")


def _first_oos_index(timestamps: Sequence[datetime], oos_start: datetime) -> int:
    for index, timestamp in enumerate(timestamps):
        if timestamp >= oos_start:
            return index
    raise ValueError("OOS window would be empty")


def _infer_bar_duration(
    timestamps: Sequence[datetime],
    oos_index: int,
) -> timedelta:
    if len(timestamps) < 2:
        raise ValueError("at least two bars are required to infer bar duration")
    if oos_index > 0:
        duration = timestamps[oos_index] - timestamps[oos_index - 1]
    else:
        duration = timestamps[1] - timestamps[0]
    if duration <= timedelta(0):
        raise ValueError("bar duration must be positive")
    return duration


def _validate_no_window_overlap(
    is_window: Sequence[TBar],
    oos_window: Sequence[TBar],
    is_cutoff: datetime,
    oos_start: datetime,
) -> None:
    if any(_timestamp(bar) >= is_cutoff for bar in is_window):
        raise LeakageError("IS window overlaps embargo cutoff")
    if any(_timestamp(bar) < oos_start for bar in oos_window):
        raise LeakageError("OOS window starts before oos_start")


def _validate_no_feature_leakage(
    is_window: Sequence[TBar],
    is_cutoff: datetime,
) -> None:
    for bar in is_window:
        computed_through = _feature_computed_through(bar)
        if computed_through is not None and computed_through >= is_cutoff:
            raise LeakageError("IS feature was computed using data at or after the IS cutoff")


def _feature_computed_through(bar: object) -> datetime | None:
    value = _mapping_or_attr(bar, "feature_computed_through")
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise TypeError("feature_computed_through must be a datetime when present")
    _require_utc(value, "feature_computed_through")
    return value


def _mapping_or_attr(source: object, name: str) -> Any | None:
    if isinstance(source, Mapping):
        return source.get(name)
    return getattr(source, name, None)
