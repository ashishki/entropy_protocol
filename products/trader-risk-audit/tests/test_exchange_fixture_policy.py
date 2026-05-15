from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

POLICY = Path("docs/EXCHANGE_FIXTURE_POLICY_RU.md")
FIXTURE_DIR = Path("tests/fixtures/exchange")

_SENSITIVE_KEY_PATTERNS = (
    "apikey",
    "apisecret",
    "passphrase",
    "accesstoken",
    "bearertoken",
    "sessioncookie",
    "seedphrase",
    "privatekey",
    "signature",
    "signedquery",
    "accountid",
    "userid",
    "subaccountid",
    "walletid",
    "accountbalance",
    "availablebalance",
    "marginbalance",
    "customeridentifier",
    "email",
    "phone",
    "telegram",
    "privatenote",
    "remark",
)
_SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{12,}"),
    re.compile(r"AKIA[0-9A-Z]{12,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{12,}", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9_]*api[_-]?secret[A-Za-z0-9_]*", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9_]*api[_-]?key[A-Za-z0-9_]*", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
)


def test_exchange_fixture_policy_rejects_sensitive_fields() -> None:
    bad_payload = {
        "fixture_label": "synthetic_exchange_fixture",
        "exchange": "bybit",
        "records": [
            {
                "api_key": "fixture_api_key_123",
                "signature": "fixture_signature_456",
                "account_id": "fixture_account_id_789",
                "available_balance": "100000",
                "customer_email": "trader@example.com",
                "private_note": "real trader note",
            }
        ],
    }

    findings = _scan_fixture_payload(bad_payload)

    assert "records.0.api_key" in findings
    assert "records.0.signature" in findings
    assert "records.0.account_id" in findings
    assert "records.0.available_balance" in findings
    assert "records.0.customer_email" in findings
    assert "records.0.private_note" in findings


def test_committed_exchange_fixtures_are_sanitized() -> None:
    fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))

    assert fixture_paths, "expected at least one committed exchange fixture"
    for fixture_path in fixture_paths:
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        findings = _scan_fixture_payload(payload)

        assert findings == [], f"{fixture_path} has sensitive fields: {findings}"
        assert payload["fixture_label"] in {
            "synthetic_exchange_fixture",
            "sanitized_exchange_fixture",
        }
        assert payload["source_type"] in {"synthetic", "sanitized"}
        assert payload["intended_use"] == "regression_test_only"
        assert payload["records"]


def test_exchange_fixture_policy_documents_allowed_raw_execution_fields() -> None:
    text = " ".join(POLICY.read_text(encoding="utf-8").casefold().split())

    required_phrases = (
        "allowed raw execution fields",
        "synthetic_exchange_fixture",
        "sanitized_exchange_fixture",
        "regression_test_only",
        "api keys",
        "request signatures",
        "account ids",
        "account balances",
        "private notes",
        "exec_id",
        "trade_id",
        "order_id",
        "exec_time",
        "exec_qty",
        "exec_price",
        "commission",
        "source_row_id",
        "this policy does not approve exchange network calls",
    )
    for phrase in required_phrases:
        assert phrase in text


def _scan_fixture_payload(payload: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    _scan_value(payload, path=(), findings=findings)
    return findings


def _scan_value(value: Any, *, path: tuple[str, ...], findings: list[str]) -> None:
    if path and path[-1] == "fields_removed":
        return
    if isinstance(value, dict):
        for key, child in value.items():
            key_path = (*path, str(key))
            normalized_key = _normalize_token(str(key))
            if any(pattern in normalized_key for pattern in _SENSITIVE_KEY_PATTERNS):
                findings.append(_format_path(key_path))
            _scan_value(child, path=key_path, findings=findings)
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _scan_value(child, path=(*path, str(index)), findings=findings)
        return
    if isinstance(value, str) and any(
        pattern.search(value) for pattern in _SENSITIVE_VALUE_PATTERNS
    ):
        findings.append(_format_path(path))


def _normalize_token(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def _format_path(path: tuple[str, ...]) -> str:
    return ".".join(path)
