from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from trader_risk_audit.policy.review import build_review_packet
from trader_risk_audit.policy.schema import RiskPolicy, load_policy

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "STARTER_POLICY_PROFILES_RU.md"
TEMPLATE_DIR = ROOT / "templates" / "policies"


def test_starter_policy_doc_explains_profiles_and_customization() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    assert "soft" in content
    assert "medium" in content
    assert "hard" in content
    assert "Кастомизация приветствуется" in content
    assert "Trader custom rules" in content
    assert "Prop/funded account rules" in content
    assert "не инвестиционный совет" in content
    assert "not trading advice" in content
    assert "100000 USD" in content


def test_starter_policy_templates_are_valid_and_review_ready() -> None:
    for profile in ("soft", "medium", "hard"):
        policy = load_policy(TEMPLATE_DIR / f"starter_policy_{profile}.yaml")

        assert isinstance(policy, RiskPolicy)
        assert policy.account_scope == ("acct_public_sample_001",)
        assert not build_review_packet(policy).unresolved_items
        assert {rule.type for rule in policy.rules} == {
            "cooldown_after_loss",
            "forbidden_assets",
            "max_daily_loss",
            "max_drawdown",
            "max_position_size",
        }


def test_starter_policy_profiles_get_stricter_from_soft_to_hard() -> None:
    soft = _rules_by_type(load_policy(TEMPLATE_DIR / "starter_policy_soft.yaml"))
    medium = _rules_by_type(load_policy(TEMPLATE_DIR / "starter_policy_medium.yaml"))
    hard = _rules_by_type(load_policy(TEMPLATE_DIR / "starter_policy_hard.yaml"))

    assert soft["max_daily_loss"].threshold == Decimal("3000")
    assert medium["max_daily_loss"].threshold == Decimal("2000")
    assert hard["max_daily_loss"].threshold == Decimal("1000")

    assert soft["max_drawdown"].threshold == Decimal("8000")
    assert medium["max_drawdown"].threshold == Decimal("5000")
    assert hard["max_drawdown"].threshold == Decimal("3000")

    assert soft["max_position_size"].threshold == Decimal("25000")
    assert medium["max_position_size"].threshold == Decimal("15000")
    assert hard["max_position_size"].threshold == Decimal("10000")

    assert soft["cooldown_after_loss"].params["cooldown_minutes"] == 15
    assert medium["cooldown_after_loss"].params["cooldown_minutes"] == 30
    assert hard["cooldown_after_loss"].params["cooldown_minutes"] == 60


def test_phase_7_docs_reference_starter_profiles_for_internal_validation() -> None:
    codex_prompt = (ROOT / "docs" / "CODEX_PROMPT.md").read_text(encoding="utf-8")
    tasks = (ROOT / "docs" / "tasks.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for content in (codex_prompt, tasks, readme):
        assert "soft" in content
        assert "medium" in content
        assert "hard" in content
        assert "STARTER_POLICY_PROFILES_RU.md" in content


def _rules_by_type(policy: RiskPolicy):
    return {rule.type: rule for rule in policy.rules}
