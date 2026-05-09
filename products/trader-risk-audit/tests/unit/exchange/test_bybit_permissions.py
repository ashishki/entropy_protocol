from __future__ import annotations

import json

import pytest

from trader_risk_audit.exchange.bybit import (
    BybitPermissionError,
    check_bybit_api_key_permissions,
    require_bybit_read_only_permissions,
)
from trader_risk_audit.exchange.credentials import (
    APPROVED_READ_ONLY,
    NEEDS_OPERATOR_REVIEW,
    REJECTED_WRITE_SCOPE,
    ExchangeCredentials,
)


def test_bybit_permission_checker_requires_read_only() -> None:
    approved = check_bybit_api_key_permissions(
        {
            "retCode": 0,
            "result": {
                "readOnly": 1,
                "permissions": {
                    "Spot": ["SpotTrade"],
                    "Wallet": [],
                },
            },
        }
    )
    rejected = check_bybit_api_key_permissions(
        {
            "retCode": 0,
            "result": {
                "readOnly": 0,
                "permissions": {"Spot": ["SpotTrade"]},
            },
        }
    )
    unverifiable = check_bybit_api_key_permissions(
        {"retCode": 0, "result": {"permissions": {}}}
    )

    assert approved.approved is True
    assert approved.permission_review.status == APPROVED_READ_ONLY
    assert rejected.approved is False
    assert rejected.permission_review.status == REJECTED_WRITE_SCOPE
    assert (
        rejected.permission_review.reason == "exchange reports the key is not read-only"
    )
    assert unverifiable.permission_review.status == NEEDS_OPERATOR_REVIEW


def test_bybit_permission_checker_rejects_write_scopes() -> None:
    check = check_bybit_api_key_permissions(
        {
            "retCode": 0,
            "result": {
                "readOnly": 1,
                "permissions": {
                    "ContractTrade": ["OrderWrite"],
                    "User": ["AccountMutation"],
                    "Wallet": ["AccountTransfer", "Withdraw"],
                },
            },
        }
    )

    assert check.approved is False
    assert check.permission_review.status == REJECTED_WRITE_SCOPE
    assert check.permission_review.reason == (
        "exchange metadata contains write/control permissions"
    )
    assert check.permission_review.rejected_permissions == (
        "ContractTrade:OrderWrite",
        "User:AccountMutation",
        "Wallet:AccountTransfer",
        "Wallet:Withdraw",
    )


def test_bybit_permission_errors_are_redacted() -> None:
    credentials = ExchangeCredentials(
        exchange="bybit",
        api_key="fixture_bybit_api_key_123",
        api_secret="fixture_bybit_api_secret_456",
        passphrase="fixture_bybit_passphrase_789",
        account_id="fixture_bybit_account_id_999",
    )
    metadata = {
        "retCode": 0,
        "result": {
            "readOnly": 0,
            "permissions": {"Wallet": ["Withdraw"]},
        },
    }

    check = check_bybit_api_key_permissions(metadata, credentials=credentials)
    with pytest.raises(BybitPermissionError) as error:
        require_bybit_read_only_permissions(metadata, credentials=credentials)

    rendered = "\n".join(
        (
            str(error.value),
            json.dumps(check.safe_metadata, sort_keys=True),
        )
    )
    assert "fixture_bybit_api_key_123" not in rendered
    assert "fixture_bybit_api_secret_456" not in rendered
    assert "fixture_bybit_passphrase_789" not in rendered
    assert "fixture_bybit_account_id_999" not in rendered
    assert "<redacted>" in rendered
    assert "api_key_fingerprint" in rendered
    assert "account_id_fingerprint" in rendered
