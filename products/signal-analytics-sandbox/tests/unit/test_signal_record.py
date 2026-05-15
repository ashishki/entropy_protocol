from __future__ import annotations

import hashlib
import json
from decimal import Decimal

import pytest
from pydantic import ValidationError

from signal_sandbox.ledger.record import (
    SignalRecord,
    canonical_dedup_payload,
    compute_dedup_key,
)


def make_record(**overrides: object) -> SignalRecord:
    data: dict[str, object] = {
        "source_id": "bablos79",
        "capture_id": "cap-001",
        "evidence_url": "https://t.me/bablos79/1",
        "text_sha256": "a" * 64,
        "capture_timestamp_utc": "2026-05-07T09:00:00Z",
        "extracted_timestamp_utc": "2026-05-07T10:00:00Z",
        "asset_symbol": "BTC",
        "direction": "long",
        "entry": Decimal("100"),
        "stop": Decimal("95"),
        "target": Decimal("110"),
        "confidence_flags": [],
        "ambiguity_flags": [],
        "extraction_metadata": {"adapter_id": "manual/v1"},
    }
    data.update(overrides)
    return SignalRecord.model_validate(data)


def test_direction_enum() -> None:
    for direction in ("long", "short", "flat", "unknown"):
        assert make_record(direction=direction).direction == direction

    with pytest.raises(ValueError):
        make_record(direction="up")


def test_ambiguous_records_not_evaluable() -> None:
    record = make_record(ambiguity_flags=["missing_entry"])

    assert record.is_evaluable() is False


def test_dedup_key_canonical() -> None:
    record = make_record()
    canonical_json = json.dumps(
        canonical_dedup_payload(record),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    expected = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    assert compute_dedup_key(record) == expected
    assert compute_dedup_key(record) == compute_dedup_key(make_record())


def test_dedup_key_sensitive_to_normalization() -> None:
    btc = make_record(asset_symbol="BTC")
    spaced = make_record(asset_symbol=" btc ")

    assert compute_dedup_key(btc) != compute_dedup_key(spaced)


def test_missing_required_fields_still_validate() -> None:
    with pytest.raises(ValidationError):
        SignalRecord.model_validate({"direction": "long"})
