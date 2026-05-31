from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TASKS = PROJECT_ROOT / "docs/tasks.md"
SPEC = PROJECT_ROOT / "docs/specs/AUTO_VALIDATION_EVIDENCE.md"
ADR = PROJECT_ROOT / "docs/adr/ADR-005-auto-validation-evidence-engine.md"
PROMPT = PROJECT_ROOT / "docs/CODEX_PROMPT.md"


def test_auto_validation_phases_are_in_task_graph() -> None:
    tasks = TASKS.read_text(encoding="utf-8")

    for phase in (
        "## Phase 40 — Auto-Validation Evidence Contract",
        "## Phase 41 — Auto-Validation Validator Stack",
        "## Phase 42 — Auto-Accept Decision Engine And Evaluation",
    ):
        assert phase in tasks

    for task_id in (
        "SAS-AUTOVAL-001",
        "SAS-AUTOVAL-002",
        "SAS-AUTOVAL-003",
        "SAS-AUTOVAL-004",
        "SAS-AUTOVAL-005",
        "SAS-AUTOVAL-006",
        "SAS-AUTOVAL-007",
        "SAS-AUTOVAL-008",
        "SAS-AUTOVAL-009",
        "SAS-AUTOVAL-010",
        "SAS-AUTOVAL-011",
    ):
        assert task_id in tasks


def test_auto_validation_contract_keeps_model_review_as_triage() -> None:
    contract = ADR.read_text(encoding="utf-8") + "\n" + SPEC.read_text(encoding="utf-8")

    assert "Model review alone remains triage" in contract
    assert "auto_accepted" in contract
    assert "auto_rejected" in contract
    assert "excluded_provider_gap" in contract
    assert "needs_human" in contract
    assert "blocked_customer_facing" in contract
    assert "Any uncertainty" in contract
    assert "routes to `needs_human`" in contract


def test_active_state_points_to_auto_validation_route() -> None:
    prompt = PROMPT.read_text(encoding="utf-8")

    assert "Active route: Phase 41 auto-validation validator stack." in prompt
    assert "Next task: `SAS-AUTOVAL-004`" in prompt
    assert "buyer outreach remains blocked" in prompt
