from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from trader_risk_audit.policy.profiles import (
    PolicyProfileSelectionError,
    format_policy_profile_selector_copy,
    resolve_policy_profile,
)
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.telegram_bot.handlers import TelegramPilotHandlers
from trader_risk_audit.telegram_bot.storage import TelegramAuditStorage
from trader_risk_audit.workspace import create_audit_workspace


def test_selector_records_starter_profile_metadata(tmp_path: Path) -> None:
    selection = resolve_policy_profile("soft")
    workspace = create_audit_workspace(
        tmp_path,
        "audit_profile_soft",
        created_at=datetime(2026, 5, 9, 9, 0, tzinfo=UTC),
        file_references={"trades_export": "input/trades.csv"},
        policy_profile=selection,
    )
    metadata = json.loads(workspace.metadata_path.read_text(encoding="utf-8"))

    assert selection.policy_path == Path("templates/policies/starter_policy_soft.yaml")
    assert load_policy(selection.policy_path).rules
    assert metadata["policy_profile"] == {
        "policy_path": "templates/policies/starter_policy_soft.yaml",
        "policy_source": "starter_template",
        "selected_profile": "soft",
    }
    assert "timestamp,symbol,side,quantity,price" not in json.dumps(metadata)


def test_custom_profile_requires_user_rules(tmp_path: Path) -> None:
    with pytest.raises(PolicyProfileSelectionError, match="requires"):
        resolve_policy_profile("custom")

    selection = resolve_policy_profile(
        "custom",
        custom_policy_path=tmp_path / "written_rules.yaml",
    )

    assert selection.selected_profile == "custom"
    assert selection.policy_source == "custom_rules"
    assert selection.to_metadata()["policy_path"] == "written_rules.yaml"


def test_selector_copy_preserves_no_advice_boundary(tmp_path: Path) -> None:
    copy = format_policy_profile_selector_copy()
    response = TelegramPilotHandlers(TelegramAuditStorage(tmp_path)).handle_command(
        "/profiles"
    )
    text = f"{copy}\n{response.text}".casefold()

    required_phrases = (
        "soft",
        "medium",
        "hard",
        "custom",
        "customizable audit presets",
        "not trading advice",
        "not optimal risk settings",
        "trader custom rules",
        "prop/funded account rules",
        "written risk rules",
    )
    for phrase in required_phrases:
        assert phrase in text
