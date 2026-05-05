"""Temporal-shuffling leakage audit for walk-forward features."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from entropy.walkforward.leakage import CheckStatus
from entropy.walkforward.splitter import BarLike

TEMPORAL_SHUFFLE_METHOD_ID = "TS-OOS-SHUFFLE-v1"

FeatureHashFn = Callable[[Sequence[BarLike], Sequence[BarLike]], str]
OOSShuffleFn = Callable[[Sequence[BarLike]], tuple[BarLike, ...]]


@dataclass(frozen=True)
class TemporalShuffleAuditResult:
    """Result of an OOS temporal-shuffling leakage audit."""

    method_id: str
    status: CheckStatus
    baseline_feature_hash: str
    shuffled_feature_hash: str
    is_window_size: int
    oos_window_size: int
    description: str


def reverse_oos_window(oos_window: Sequence[BarLike]) -> tuple[BarLike, ...]:
    """Deterministically reverse the OOS window."""
    return tuple(reversed(oos_window))


def run_temporal_shuffle_audit(
    is_window: Sequence[BarLike],
    oos_window: Sequence[BarLike],
    *,
    feature_hash_fn: FeatureHashFn,
    shuffle_fn: OOSShuffleFn = reverse_oos_window,
) -> TemporalShuffleAuditResult:
    """Verify IS feature output is invariant to OOS temporal shuffling."""
    if not is_window:
        raise ValueError("is_window must be nonempty")
    if not oos_window:
        raise ValueError("oos_window must be nonempty")
    baseline_hash = _validate_hash(feature_hash_fn(is_window, oos_window), "baseline")
    shuffled_oos = shuffle_fn(oos_window)
    if len(shuffled_oos) != len(oos_window):
        raise ValueError("shuffle_fn must preserve OOS window length")
    shuffled_hash = _validate_hash(feature_hash_fn(is_window, shuffled_oos), "shuffled")
    status = CheckStatus.PASS if baseline_hash == shuffled_hash else CheckStatus.FAIL
    description = (
        "IS feature hash is invariant to OOS temporal shuffling."
        if status is CheckStatus.PASS
        else "IS feature hash changed after OOS temporal shuffling."
    )
    return TemporalShuffleAuditResult(
        method_id=TEMPORAL_SHUFFLE_METHOD_ID,
        status=status,
        baseline_feature_hash=baseline_hash,
        shuffled_feature_hash=shuffled_hash,
        is_window_size=len(is_window),
        oos_window_size=len(oos_window),
        description=description,
    )


def _validate_hash(value: str, name: str) -> str:
    if not value.strip():
        raise ValueError(f"{name} feature hash must not be blank")
    return value
