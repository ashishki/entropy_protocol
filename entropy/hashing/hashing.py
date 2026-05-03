"""Deterministic SHA-256 hashing helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import polars as pl

HASH_VERSION = "entropy-hash-v1"


def _sha256_hex(payload: bytes) -> str:
    """Return a lowercase SHA-256 hex digest."""
    return hashlib.sha256(payload).hexdigest()


def _canonical_json(value: Any) -> bytes:
    """Serialize JSON-compatible values in a deterministic byte representation."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    ).encode("utf-8")


def _schema_fingerprint(frame: pl.DataFrame) -> list[dict[str, str]]:
    """Return a deterministic schema fingerprint."""
    return [
        {"name": column_name, "dtype": str(frame.schema[column_name])}
        for column_name in sorted(frame.schema)
    ]


def _sorted_frame(frame: pl.DataFrame) -> pl.DataFrame:
    """Sort rows by every column so row insertion order cannot affect the hash."""
    if not frame.columns:
        return frame
    return frame.select(sorted(frame.columns)).sort(sorted(frame.columns))


def compute_dataset_hash(path: str | Path) -> str:
    """Compute SHA-256(sorted Parquet rows + schema fingerprint)."""
    frame = pl.read_parquet(path)
    sorted_frame = _sorted_frame(frame)
    payload = {
        "version": HASH_VERSION,
        "kind": "dataset",
        "schema": _schema_fingerprint(frame),
        "rows": sorted_frame.to_dicts(),
    }
    return _sha256_hex(_canonical_json(payload))


def compute_run_hash(dataset_hash: str, code_hash: str, policy_hash: str) -> str:
    """Compute a deterministic hash for a run identity triple."""
    payload = {
        "version": HASH_VERSION,
        "kind": "run",
        "dataset_hash": dataset_hash,
        "code_hash": code_hash,
        "policy_hash": policy_hash,
    }
    return _sha256_hex(_canonical_json(payload))


def compute_policy_hash(policy_config: dict[str, Any]) -> str:
    """Compute a deterministic hash for a policy configuration."""
    payload = {
        "version": HASH_VERSION,
        "kind": "policy",
        "policy": policy_config,
    }
    return _sha256_hex(_canonical_json(payload))
