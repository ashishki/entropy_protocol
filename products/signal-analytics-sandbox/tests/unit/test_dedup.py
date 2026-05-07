from __future__ import annotations

from decimal import Decimal

from signal_sandbox.ledger.dedup import (
    canonical_records_json,
    deduplicate,
    flag_ambiguous,
)
from signal_sandbox.ledger.record import SignalRecord


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


def test_grouping_and_flagging() -> None:
    records = [
        make_record(capture_id="cap-001"),
        make_record(capture_id="cap-002"),
        make_record(
            capture_id="cap-003",
            extracted_timestamp_utc="2026-05-07T11:00:00Z",
        ),
    ]

    result = deduplicate(records)

    assert result[0].ambiguity_flags == ["duplicate_dedup_key"]
    assert result[1].ambiguity_flags == ["duplicate_dedup_key"]
    assert result[2].ambiguity_flags == []


def test_flag_combinations() -> None:
    record = make_record(
        direction="unknown",
        entry=None,
        stop=None,
        target=None,
        ambiguity_flags=["manual_review"],
    )

    result = flag_ambiguous(flag_ambiguous(record))

    assert result.ambiguity_flags == [
        "manual_review",
        "missing_entry",
        "missing_target_and_stop",
        "unknown_direction",
    ]


def test_deterministic() -> None:
    records = [
        make_record(capture_id="cap-001"),
        make_record(capture_id="cap-002"),
        make_record(
            capture_id="cap-003",
            entry=None,
            stop=None,
            target=None,
        ),
    ]

    first = [flag_ambiguous(record) for record in deduplicate(records)]
    second = [flag_ambiguous(record) for record in deduplicate(records)]

    assert canonical_records_json(first) == canonical_records_json(second)
