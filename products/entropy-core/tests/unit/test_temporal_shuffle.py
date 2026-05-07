from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Sequence

import pytest

from entropy.walkforward import (
    CheckStatus,
    TEMPORAL_SHUFFLE_METHOD_ID,
    run_temporal_shuffle_audit,
)
from entropy.walkforward.splitter import BarLike


@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    close: float


def make_windows() -> tuple[tuple[Bar, ...], tuple[Bar, ...]]:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    bars = tuple(
        Bar(timestamp=start + timedelta(days=index), close=100 + index) for index in range(8)
    )
    return bars[:4], bars[4:]


def test_temporal_shuffle_passes_when_is_features_ignore_oos_order() -> None:
    is_window, oos_window = make_windows()

    result = run_temporal_shuffle_audit(
        is_window,
        oos_window,
        feature_hash_fn=_is_only_feature_hash,
    )

    assert result.method_id == TEMPORAL_SHUFFLE_METHOD_ID
    assert result.status is CheckStatus.PASS
    assert result.baseline_feature_hash == result.shuffled_feature_hash
    assert result.is_window_size == 4
    assert result.oos_window_size == 4


def test_temporal_shuffle_fails_when_is_features_depend_on_oos_order() -> None:
    is_window, oos_window = make_windows()

    result = run_temporal_shuffle_audit(
        is_window,
        oos_window,
        feature_hash_fn=_leaking_feature_hash,
    )

    assert result.status is CheckStatus.FAIL
    assert result.baseline_feature_hash != result.shuffled_feature_hash


def test_temporal_shuffle_rejects_blank_feature_hash() -> None:
    is_window, oos_window = make_windows()

    with pytest.raises(ValueError, match="baseline feature hash"):
        run_temporal_shuffle_audit(
            is_window,
            oos_window,
            feature_hash_fn=lambda _is_window, _oos_window: "",
        )


def _is_only_feature_hash(is_window: Sequence[BarLike], oos_window: Sequence[BarLike]) -> str:
    payload = ",".join(str(bar.timestamp.isoformat()) for bar in is_window)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _leaking_feature_hash(is_window: Sequence[BarLike], oos_window: Sequence[BarLike]) -> str:
    payload = ",".join(
        str(bar.timestamp.isoformat()) for bar in [*tuple(is_window), *tuple(oos_window)]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
