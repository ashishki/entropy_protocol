from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
    build_violation_id,
    serialize_violations,
    serialize_warnings,
)


def test_violation_ids_are_stable_hashes() -> None:
    violation = _violation(
        rule_id="rule_b",
        row_id="row_2",
        timestamp=datetime(2026, 1, 15, 10, 0, tzinfo=UTC),
    )

    first = build_violation_id("audit_demo", violation)
    second = build_violation_id("audit_demo", violation)

    assert first == second
    assert first.startswith("vio_")
    assert build_violation_id("audit_other", violation) != first


def test_violation_serialization_order_is_deterministic() -> None:
    later = _violation(
        rule_id="rule_a",
        row_id="row_3",
        timestamp=datetime(2026, 1, 15, 11, 0, tzinfo=UTC),
    )
    earlier = _violation(
        rule_id="rule_b",
        row_id="row_2",
        timestamp=datetime(2026, 1, 15, 10, 0, tzinfo=UTC),
    )

    serialized = serialize_violations("audit_demo", (later, earlier))
    payload = json.loads(serialized)

    assert [item["rule_id"] for item in payload] == ["rule_b", "rule_a"]
    assert payload[0]["violation_id"] == build_violation_id("audit_demo", earlier)
    assert payload[0]["evaluated_value"] == "15000"
    assert payload[0]["threshold"] == "10000"


def test_warnings_serialize_separately_from_violations() -> None:
    warning = UnsupportedDataWarning(
        rule_id="rule_max_leverage",
        rule_type="max_leverage",
        message_code="unsupported_leverage_data",
        missing_fields=("leverage",),
    )

    serialized = serialize_warnings((warning,))
    payload = json.loads(serialized)

    assert payload == [
        {
            "affected_source_fields": ["leverage"],
            "reason_code": "unsupported_leverage_data",
            "rule_id": "rule_max_leverage",
            "rule_type": "max_leverage",
        }
    ]
    assert "violation_id" not in payload[0]


def _violation(
    *,
    rule_id: str,
    row_id: str,
    timestamp: datetime,
) -> ViolationRecord:
    return ViolationRecord(
        rule_id=rule_id,
        rule_type="max_position_size",
        source_row_ids=(row_id,),
        timestamp=timestamp,
        evaluated_value=Decimal("15000"),
        threshold=Decimal("10000"),
        severity="breach",
        message_code="max_position_size_exceeded",
        symbol="BTCUSD",
    )
