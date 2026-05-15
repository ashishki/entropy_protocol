from __future__ import annotations

import json

import pytest

from trader_risk_audit.intake import (
    IntakePrivacyFlags,
    IntakeSessionError,
    build_intake_session,
    transition_intake_session,
)


def test_intake_session_records_safe_metadata() -> None:
    session = build_intake_session(
        prospect_label="prop_firm_trial_001",
        source_type="csv_export",
        source_file="/private/customer/raw_export.csv",
        risk_rules_file="rules.md",
        source_timezone="UTC",
        display_timezone="Europe/Moscow",
        session_start="09:30",
        session_end="16:00",
        account_currency="usd",
        status="ready_for_schema_profile",
    )
    payload = session.to_dict()
    serialized = session.to_json()

    assert session.session_id.startswith("intake_")
    assert payload["source_type"] == "csv_export"
    assert payload["file_references"] == {
        "risk_rules": "rules.md",
        "source_export": "raw_export.csv",
    }
    assert payload["source_timezone"] == "UTC"
    assert payload["display_timezone"] == "Europe/Moscow"
    assert payload["session"] == {"start": "09:30", "end": "16:00"}
    assert payload["account_currency"] == "USD"
    assert payload["privacy_flags"] == {
        "no_credentials_confirmed": True,
        "no_pii_confirmed": True,
        "raw_rows_stay_local": True,
    }
    assert payload["status"] == "ready_for_schema_profile"
    assert "2026-03-01T10:00:00+00:00,BTCUSDT,buy,1,100" not in serialized
    assert "/private/customer" not in serialized


def test_intake_session_rejects_sensitive_metadata() -> None:
    cases = (
        {"prospect_label": "@real_trader_handle"},
        {"source_file": "export_api_key.csv"},
        {"risk_rules_file": "private_notes.txt"},
        {
            "privacy_flags": IntakePrivacyFlags(
                no_pii_confirmed=True,
                no_credentials_confirmed=False,
                raw_rows_stay_local=True,
            )
        },
        {"status": "live_control_enabled"},
    )

    for override in cases:
        with pytest.raises(IntakeSessionError):
            build_intake_session(**(_valid_kwargs() | override))


def test_intake_session_json_is_deterministic() -> None:
    first = build_intake_session(**_valid_kwargs())
    second = build_intake_session(**_valid_kwargs())

    assert first.session_id == second.session_id
    assert json.loads(first.to_json()) == json.loads(second.to_json())


def test_intake_session_status_transitions_are_explicit() -> None:
    session = build_intake_session(**_valid_kwargs())
    ready = transition_intake_session(session, "ready_for_schema_profile")

    assert ready.status == "ready_for_schema_profile"
    assert ready.session_id == session.session_id
    with pytest.raises(IntakeSessionError):
        transition_intake_session(session, "ready_for_audit")


def _valid_kwargs() -> dict[str, object]:
    return {
        "prospect_label": "desk_trial_001",
        "source_type": "csv_export",
        "source_file": "input/export.csv",
        "risk_rules_file": "input/rules.md",
        "source_timezone": "UTC",
        "display_timezone": "Europe/Moscow",
        "session_start": "00:00",
        "session_end": "23:59",
        "account_currency": "USDT",
        "status": "created",
    }
