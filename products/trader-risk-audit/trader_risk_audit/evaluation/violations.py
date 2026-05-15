from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class ViolationRecord:
    rule_id: str
    rule_type: str
    source_row_ids: tuple[str, ...]
    timestamp: datetime
    evaluated_value: Decimal | str
    threshold: Decimal | str
    severity: str
    message_code: str
    symbol: str | None = None
    details: dict[str, Any] | None = None


@dataclass(frozen=True)
class UnsupportedDataWarning:
    rule_id: str
    rule_type: str
    message_code: str
    missing_fields: tuple[str, ...]


def build_violation_id(audit_id: str, violation: ViolationRecord) -> str:
    payload = {
        "audit_id": audit_id,
        "rule_id": violation.rule_id,
        "rule_type": violation.rule_type,
        "source_row_ids": sorted(violation.source_row_ids),
        "timestamp": violation.timestamp.isoformat(),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"vio_{digest}"


def serialize_violations(
    audit_id: str,
    violations: tuple[ViolationRecord, ...],
) -> str:
    payload = [
        _violation_to_payload(audit_id, violation)
        for violation in sorted(
            violations,
            key=lambda item: (
                item.timestamp,
                item.rule_id,
                build_violation_id(audit_id, item),
            ),
        )
    ]
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def serialize_warnings(warnings: tuple[UnsupportedDataWarning, ...]) -> str:
    payload = [
        {
            "affected_source_fields": list(warning.missing_fields),
            "reason_code": warning.message_code,
            "rule_id": warning.rule_id,
            "rule_type": warning.rule_type,
        }
        for warning in sorted(
            warnings,
            key=lambda item: (item.rule_id, item.message_code, item.missing_fields),
        )
    ]
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _violation_to_payload(
    audit_id: str,
    violation: ViolationRecord,
) -> dict[str, Any]:
    return {
        "details": _canonical_value(violation.details or {}),
        "evaluated_value": _canonical_value(violation.evaluated_value),
        "message_code": violation.message_code,
        "rule_id": violation.rule_id,
        "rule_type": violation.rule_type,
        "severity": violation.severity,
        "source_row_ids": list(violation.source_row_ids),
        "symbol": violation.symbol,
        "threshold": _canonical_value(violation.threshold),
        "timestamp": violation.timestamp.isoformat(),
        "violation_id": build_violation_id(audit_id, violation),
    }


def _canonical_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return format(value.normalize(), "f")
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _canonical_value(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_canonical_value(item) for item in value]
    return value
