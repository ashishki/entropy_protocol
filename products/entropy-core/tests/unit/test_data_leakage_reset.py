"""Reset-era data, leakage, and holdout gate tests."""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

from entropy.data import HoldoutReadRequest, authorize_holdout_read
from entropy.hashing import compute_dataset_hash
from entropy.walkforward import (
    CheckStatus,
    LeakageCheckResult,
    LeakageReport,
    OOSLabelBlockedError,
    create_oos_label,
)


def test_dataset_hash_is_order_independent(tmp_path: Path) -> None:
    """Dataset hash is stable for identical rows in different orders."""
    first = tmp_path / "first.parquet"
    second = tmp_path / "second.parquet"
    rows = {
        "timestamp": ["2026-01-02T00:00:00Z", "2026-01-01T00:00:00Z"],
        "symbol": ["BTC-USD", "BTC-USD"],
        "close": [101.0, 100.0],
    }
    pl.DataFrame(rows).write_parquet(first)
    pl.DataFrame(rows).sort("timestamp").write_parquet(second)

    assert compute_dataset_hash(first) == compute_dataset_hash(second)


def test_leakage_failure_blocks_oos_label() -> None:
    """Failed leakage checks block OOS label creation and name failing checks."""
    report = LeakageReport(
        normalization_leakage=LeakageCheckResult(
            status=CheckStatus.FAIL,
            description="normalization used OOS data",
        ),
        regime_label_lookahead=LeakageCheckResult(status=CheckStatus.PASS, description="ok"),
        universe_selection_bias=LeakageCheckResult(status=CheckStatus.PASS, description="ok"),
        within_window_optimization=LeakageCheckResult(status=CheckStatus.PASS, description="ok"),
    )

    with pytest.raises(OOSLabelBlockedError) as exc_info:
        create_oos_label(report)

    assert exc_info.value.failing_check_ids == ("normalization_leakage",)


def test_holdout_lock_checked_before_path_open() -> None:
    """A locked holdout blocks before the reader can open the path."""
    read_attempted = False

    def reader(_path: str) -> None:
        nonlocal read_attempted
        read_attempted = True
        raise AssertionError("holdout path was opened")

    decision = authorize_holdout_read(
        HoldoutReadRequest(path="holdout.parquet", lock_status="LOCKED"),
        reader=reader,
    )

    assert decision.status == "BLOCKED"
    assert decision.reason_code == "HOLDOUT_LOCKED"
    assert read_attempted is False
