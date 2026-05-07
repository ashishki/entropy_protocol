from __future__ import annotations

from pathlib import Path

import yaml

INTAKE_CONTRACT = Path("docs/PILOT_INTAKE_CONTRACT_RU.md")
INTAKE_TEMPLATE = Path("templates/intake_request.yaml")
RISK_RULES_TEMPLATE = Path("templates/risk_rules_template_ru.md")
PRIVACY_DISCLAIMER = Path("templates/privacy_disclaimer_ru.md")


def test_intake_contract_mentions_required_fields() -> None:
    contract_text = INTAKE_CONTRACT.read_text(encoding="utf-8").casefold()
    intake_payload = yaml.safe_load(INTAKE_TEMPLATE.read_text(encoding="utf-8"))

    required_contract_phrases = (
        "required files",
        ".csv",
        ".xlsx",
        "timezone",
        "session_start",
        "session_end",
        "broker_or_platform",
        "account_currency",
        "audit_period_start",
        "audit_period_end",
        "written risk rules",
    )
    for phrase in required_contract_phrases:
        assert phrase in contract_text

    assert set(intake_payload) >= {
        "broker_or_platform",
        "export_file_type",
        "account_currency",
        "timezone",
        "session_start",
        "session_end",
        "audit_period_start",
        "audit_period_end",
        "risk_rules_file",
    }


def test_risk_rules_template_preserves_human_approval_boundary() -> None:
    template_text = RISK_RULES_TEMPLATE.read_text(encoding="utf-8").casefold()

    required_phrases = (
        "своими словами",
        "current rules",
        "past rules",
        "ambiguous rules",
        "operator approval",
        "до evaluation",
        "не интерпретируются автоматически",
    )
    for phrase in required_phrases:
        assert phrase in template_text


def test_privacy_disclaimer_contains_required_boundaries() -> None:
    disclaimer_text = PRIVACY_DISCLAIMER.read_text(encoding="utf-8").casefold()

    required_phrases = (
        "local-only",
        "not investment advice",
        "does not control live trading",
        "does not block orders",
        "does not connect to broker or exchange api",
    )
    for phrase in required_phrases:
        assert phrase in disclaimer_text

    forbidden_scope = (
        "create account",
        "oauth",
        "bot token",
        "send telegram message",
        "payment funnel",
    )
    for phrase in forbidden_scope:
        assert phrase not in disclaimer_text
