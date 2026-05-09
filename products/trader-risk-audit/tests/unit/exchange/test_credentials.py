from __future__ import annotations

import json

from trader_risk_audit.exchange.credentials import (
    APPROVED_READ_ONLY,
    NEEDS_OPERATOR_REVIEW,
    REJECTED_WRITE_SCOPE,
    ExchangeCredentials,
    build_exchange_import_safe_metadata,
    inspect_bybit_api_key_metadata,
    inspect_exchange_permissions,
)


def test_permission_contract_rejects_write_scopes() -> None:
    read_write_review = inspect_bybit_api_key_metadata(
        {
            "result": {
                "readOnly": 0,
                "permissions": {
                    "Spot": ["SpotTrade"],
                },
            }
        }
    )
    write_scope_review = inspect_exchange_permissions(
        exchange="bybit",
        read_only=True,
        permissions={
            "Wallet": ["AccountTransfer", "Withdraw"],
            "ContractTrade": ["OrderWrite"],
            "Nested": {"Transfer": True},
            "Withdraw": True,
        },
    )
    unverifiable_review = inspect_exchange_permissions(
        exchange="binance",
        read_only=None,
        permissions={},
    )

    assert read_write_review.status == REJECTED_WRITE_SCOPE
    assert read_write_review.reason == "exchange reports the key is not read-only"
    assert write_scope_review.status == REJECTED_WRITE_SCOPE
    assert write_scope_review.rejected_permissions == (
        "ContractTrade:OrderWrite",
        "Nested:Transfer",
        "Wallet:AccountTransfer",
        "Wallet:Withdraw",
        "Withdraw:<enabled>",
    )
    assert unverifiable_review.status == NEEDS_OPERATOR_REVIEW
    assert unverifiable_review.reason == "read-only permission could not be verified"


def test_permission_contract_approves_verified_read_only_key() -> None:
    review = inspect_bybit_api_key_metadata(
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

    assert review.status == APPROVED_READ_ONLY
    assert review.read_only is True
    assert review.rejected_permissions == ()


def test_credentials_are_redacted_in_output() -> None:
    credentials = ExchangeCredentials(
        exchange="bybit",
        api_key="fixture_api_key_123",
        api_secret="fixture_api_secret_456",
        passphrase="fixture_passphrase_789",
        account_id="fixture_account_id_999",
    )
    safe_metadata = build_exchange_import_safe_metadata(
        credentials=credentials,
        permission_review=inspect_exchange_permissions(
            exchange="bybit",
            read_only=True,
            permissions={},
        ),
    )
    rendered = "\n".join(
        (
            repr(credentials),
            json.dumps(credentials.to_safe_metadata(), sort_keys=True),
            json.dumps(safe_metadata, sort_keys=True),
        )
    )

    assert "fixture_api_key_123" not in rendered
    assert "fixture_api_secret_456" not in rendered
    assert "fixture_passphrase_789" not in rendered
    assert "fixture_account_id_999" not in rendered
    assert "<redacted>" in rendered
    assert "api_key_fingerprint" in rendered
    assert "account_id_fingerprint" in rendered
