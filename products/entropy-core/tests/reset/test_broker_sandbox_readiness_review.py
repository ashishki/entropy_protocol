"""Broker sandbox readiness review tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "BROKER_SANDBOX_READINESS_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_broker_sandbox_readiness_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Sandbox Boundary Summary",
        "## Fixture Manifest Summary",
        "## Risk Control Summary",
        "## Kill-Switch Summary",
        "## Dry Run Summary",
        "## Validation",
        "## Limitations",
        "## Open Findings",
        "## Roadmap Evaluation",
        "## Next Recommendation",
    ):
        assert section in text
    assert "PASS" in text
    assert "Stop-Ship: 0" in text
    assert "No open findings" in text
    assert "471 passed, 20 skipped" in text
    assert "Holdout remains locked and unread" in text


def test_broker_sandbox_readiness_review_records_roadmap_evaluation() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    assert "Decision: block the planned production/capital gate phase" in text
    assert "Next active phase: none" in text
    assert "Next active task: checkpoint before Phase 13 Production and Capital Gate" in text
    assert "do not open production/capital implementation work" in text
    assert "does not approve production, capital, live orders" in text


def test_broker_sandbox_readiness_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Phase: 27" in prompt
    assert "T56 Broker Sandbox Readiness Review completed" in prompt
    assert "T62 Product Hypothesis Confirmation Decision Review" in prompt
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T56")
    assert "BROKER-SANDBOX-READINESS" in audit_index
    assert "`docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md`" in audit_index


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
