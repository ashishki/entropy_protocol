"""Deduplication and ambiguity flagging for signal records."""

from __future__ import annotations

import json
from collections import Counter
from decimal import Decimal

from signal_sandbox.ledger.record import SignalRecord, compute_dedup_key

DUPLICATE_DEDUP_KEY = "duplicate_dedup_key"
MISSING_ENTRY = "missing_entry"
MISSING_TARGET_AND_STOP = "missing_target_and_stop"
UNKNOWN_DIRECTION = "unknown_direction"


def deduplicate(records: list[SignalRecord]) -> list[SignalRecord]:
    key_counts = Counter(compute_dedup_key(record) for record in records)
    duplicate_keys = {key for key, count in key_counts.items() if count > 1}

    return [
        _with_flags(record, [DUPLICATE_DEDUP_KEY])
        if compute_dedup_key(record) in duplicate_keys
        else record
        for record in records
    ]


def flag_ambiguous(record: SignalRecord) -> SignalRecord:
    flags: list[str] = []
    if record.entry is None:
        flags.append(MISSING_ENTRY)
    if record.target is None and record.stop is None:
        flags.append(MISSING_TARGET_AND_STOP)
    if record.direction == "unknown":
        flags.append(UNKNOWN_DIRECTION)
    return _with_flags(record, flags)


def canonical_records_json(records: list[SignalRecord]) -> str:
    return json.dumps(
        [_record_payload(record) for record in records],
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _with_flags(record: SignalRecord, flags: list[str]) -> SignalRecord:
    if not flags:
        return record

    merged = list(record.ambiguity_flags)
    for flag in flags:
        if flag not in merged:
            merged.append(flag)
    return record.model_copy(update={"ambiguity_flags": merged})


def _record_payload(record: SignalRecord) -> dict[str, object]:
    return {
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
        "confidence_flags": record.confidence_flags,
        "ambiguity_flags": record.ambiguity_flags,
        "extraction_metadata": record.extraction_metadata,
    }


def _decimal_to_string(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value)
