"""Deterministic ledger Parquet I/O."""

from __future__ import annotations

import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any

import polars as pl

from signal_sandbox.ledger.record import SignalRecord, compute_dedup_key


class LedgerIOError(Exception):
    """Base exception for ledger I/O failures."""


class DuplicateSignalRecord(LedgerIOError):
    """Raised when multiple records share a dedup key."""


class LLMReviewRequired(LedgerIOError):
    """Raised when an LLM-sourced draft has not been human-reviewed."""


CANONICAL_COLUMNS = [
    "dedup_key",
    "source_id",
    "capture_id",
    "evidence_url",
    "text_sha256",
    "capture_timestamp_utc",
    "extracted_timestamp_utc",
    "asset_symbol",
    "direction",
    "entry",
    "stop",
    "target",
    "confidence_flags",
    "ambiguity_flags",
    "reviewer_id",
    "extraction_metadata",
]

LEDGER_SCHEMA = {
    "dedup_key": pl.String,
    "source_id": pl.String,
    "capture_id": pl.String,
    "evidence_url": pl.String,
    "text_sha256": pl.String,
    "capture_timestamp_utc": pl.String,
    "extracted_timestamp_utc": pl.String,
    "asset_symbol": pl.String,
    "direction": pl.String,
    "entry": pl.String,
    "stop": pl.String,
    "target": pl.String,
    "confidence_flags": pl.String,
    "ambiguity_flags": pl.String,
    "reviewer_id": pl.String,
    "extraction_metadata": pl.String,
}


def write_ledger(
    records: list[SignalRecord],
    path: Path,
    *,
    force_duplicate: bool = False,
) -> None:
    _ensure_llm_records_reviewed(records)
    normalized = _normalize_duplicates(records, force_duplicate=force_duplicate)
    rows = [_record_to_row(record) for record in normalized]
    rows.sort(key=lambda row: (row["dedup_key"], row["capture_id"], row["source_id"]))
    frame = pl.DataFrame(rows, schema=LEDGER_SCHEMA) if rows else _empty_frame()

    path.parent.mkdir(parents=True, exist_ok=True)
    frame.select(CANONICAL_COLUMNS).write_parquet(
        path,
        compression="zstd",
        statistics=False,
    )


def read_ledger(path: Path) -> list[SignalRecord]:
    frame = pl.read_parquet(path).select(CANONICAL_COLUMNS)
    records: list[SignalRecord] = []
    for row in frame.to_dicts():
        records.append(_row_to_record(row))
    return records


def _ensure_llm_records_reviewed(records: list[SignalRecord]) -> None:
    for record in records:
        adapter_id = record.extraction_metadata.get("adapter_id", "")
        if adapter_id.startswith("llm/") and record.reviewer_id is None:
            raise LLMReviewRequired(
                "LLM-sourced records require reviewer_id before ledger write"
            )


def _normalize_duplicates(
    records: list[SignalRecord],
    *,
    force_duplicate: bool,
) -> list[SignalRecord]:
    key_counts = Counter(compute_dedup_key(record) for record in records)
    duplicate_keys = {key for key, count in key_counts.items() if count > 1}
    if duplicate_keys and not force_duplicate:
        raise DuplicateSignalRecord("duplicate dedup_key")

    if not duplicate_keys:
        return records

    normalized: list[SignalRecord] = []
    for record in records:
        if compute_dedup_key(record) in duplicate_keys:
            normalized.append(
                record.model_copy(update={"ambiguity_flags": ["duplicate_dedup_key"]})
            )
        else:
            normalized.append(record)
    return normalized


def _record_to_row(record: SignalRecord) -> dict[str, str]:
    return {
        "dedup_key": compute_dedup_key(record),
        "source_id": record.source_id,
        "capture_id": record.capture_id,
        "evidence_url": record.evidence_url,
        "text_sha256": record.text_sha256,
        "capture_timestamp_utc": record.capture_timestamp_utc.isoformat(),
        "extracted_timestamp_utc": record.extracted_timestamp_utc.isoformat(),
        "asset_symbol": record.asset_symbol,
        "direction": record.direction.value,
        "entry": _decimal_to_string(record.entry),
        "stop": _decimal_to_string(record.stop),
        "target": _decimal_to_string(record.target),
        "confidence_flags": json.dumps(record.confidence_flags, sort_keys=True),
        "ambiguity_flags": json.dumps(record.ambiguity_flags, sort_keys=True),
        "reviewer_id": record.reviewer_id or "",
        "extraction_metadata": json.dumps(
            record.extraction_metadata,
            separators=(",", ":"),
            sort_keys=True,
        ),
    }


def _row_to_record(row: dict[str, Any]) -> SignalRecord:
    return SignalRecord.model_validate(
        {
            "source_id": row["source_id"],
            "capture_id": row["capture_id"],
            "evidence_url": row["evidence_url"],
            "text_sha256": row["text_sha256"],
            "capture_timestamp_utc": row["capture_timestamp_utc"],
            "extracted_timestamp_utc": row["extracted_timestamp_utc"],
            "asset_symbol": row["asset_symbol"],
            "direction": row["direction"],
            "entry": _string_to_decimal(row["entry"]),
            "stop": _string_to_decimal(row["stop"]),
            "target": _string_to_decimal(row["target"]),
            "confidence_flags": json.loads(row["confidence_flags"]),
            "ambiguity_flags": json.loads(row["ambiguity_flags"]),
            "reviewer_id": _empty_string_to_none(row["reviewer_id"]),
            "extraction_metadata": json.loads(row["extraction_metadata"]),
        }
    )


def _empty_frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            column: pl.Series(column, [], dtype=dtype)
            for column, dtype in LEDGER_SCHEMA.items()
        }
    )


def _decimal_to_string(value: Decimal | None) -> str:
    if value is None:
        return ""
    return str(value)


def _string_to_decimal(value: str) -> Decimal | None:
    if value == "":
        return None
    return Decimal(value)


def _empty_string_to_none(value: str) -> str | None:
    if value == "":
        return None
    return value
