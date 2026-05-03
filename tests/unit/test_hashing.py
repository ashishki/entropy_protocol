"""Unit tests for deterministic hashing helpers."""

from __future__ import annotations

import re
from pathlib import Path

import polars as pl

from entropy.hashing import compute_dataset_hash, compute_policy_hash, compute_run_hash

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def write_dataset(path: Path, rows: list[dict[str, object]]) -> None:
    """Write rows to a Parquet file."""
    pl.DataFrame(rows).write_parquet(path)


def test_dataset_hash_is_row_order_independent(tmp_path: Path) -> None:
    first_path = tmp_path / "first.parquet"
    second_path = tmp_path / "second.parquet"
    rows = [
        {"timestamp": "2026-05-03T00:00:00Z", "symbol": "BTC-USD", "close": 100.0},
        {"timestamp": "2026-05-03T01:00:00Z", "symbol": "BTC-USD", "close": 101.0},
        {"timestamp": "2026-05-03T02:00:00Z", "symbol": "BTC-USD", "close": 102.0},
    ]
    write_dataset(first_path, rows)
    write_dataset(second_path, list(reversed(rows)))

    dataset_hash = compute_dataset_hash(first_path)

    assert dataset_hash == compute_dataset_hash(first_path)
    assert dataset_hash == compute_dataset_hash(second_path)
    assert SHA256_RE.fullmatch(dataset_hash)


def test_dataset_hash_detects_row_change(tmp_path: Path) -> None:
    original_path = tmp_path / "original.parquet"
    changed_path = tmp_path / "changed.parquet"
    write_dataset(
        original_path,
        [
            {"timestamp": "2026-05-03T00:00:00Z", "symbol": "BTC-USD", "close": 100.0},
            {"timestamp": "2026-05-03T01:00:00Z", "symbol": "BTC-USD", "close": 101.0},
        ],
    )
    write_dataset(
        changed_path,
        [
            {"timestamp": "2026-05-03T00:00:00Z", "symbol": "BTC-USD", "close": 100.0},
            {"timestamp": "2026-05-03T01:00:00Z", "symbol": "BTC-USD", "close": 999.0},
        ],
    )

    assert compute_dataset_hash(original_path) != compute_dataset_hash(changed_path)


def test_dataset_hash_detects_schema_change(tmp_path: Path) -> None:
    original_path = tmp_path / "original.parquet"
    changed_path = tmp_path / "changed.parquet"
    write_dataset(
        original_path,
        [{"timestamp": "2026-05-03T00:00:00Z", "symbol": "BTC-USD", "close": 100.0}],
    )
    write_dataset(
        changed_path,
        [
            {
                "timestamp": "2026-05-03T00:00:00Z",
                "symbol": "BTC-USD",
                "close": 100.0,
                "volume": 10.0,
            }
        ],
    )

    assert compute_dataset_hash(original_path) != compute_dataset_hash(changed_path)


def test_run_hash_is_deterministic() -> None:
    run_hash = compute_run_hash(dataset_hash="aaa", code_hash="bbb", policy_hash="ccc")

    assert run_hash == compute_run_hash(dataset_hash="aaa", code_hash="bbb", policy_hash="ccc")
    assert run_hash != compute_run_hash(dataset_hash="aaa", code_hash="changed", policy_hash="ccc")
    assert SHA256_RE.fullmatch(run_hash)


def test_policy_hash_is_key_order_independent() -> None:
    first_policy = {"risk": {"max_drawdown": 0.12, "gross": 1.0}, "symbols": ["BTC", "ETH"]}
    second_policy = {"symbols": ["BTC", "ETH"], "risk": {"gross": 1.0, "max_drawdown": 0.12}}

    policy_hash = compute_policy_hash(first_policy)

    assert policy_hash == compute_policy_hash(second_policy)
    assert SHA256_RE.fullmatch(policy_hash)
