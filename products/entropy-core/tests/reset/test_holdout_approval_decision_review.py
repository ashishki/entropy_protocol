"""Holdout approval decision review contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "HOLDOUT_APPROVAL_DECISION_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_holdout_approval_decision_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Request Packet Summary",
        "## Intake Contract Summary",
        "## Denial Packet Summary",
        "## Regression Sweep Summary",
        "## No-Read Dry Run Summary",
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
    assert "438 passed, 20 skipped" in text
    assert "Holdout remains locked and unread" in text


def test_holdout_approval_decision_review_records_roadmap_evaluation() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    assert "Decision: block the future approved holdout evaluation phase" in text
    assert "local live-feed dry-run readiness" in text
    assert "Next active phase: Phase 11 Live-Feed Dry Run Readiness" in text
    assert "Next active task: T46 Live-Feed Boundary Contract" in text
    assert "must not\nplace orders" in text
    assert "No explicit human holdout approval event exists" in text


def test_holdout_approval_decision_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Phase: 11" in prompt
    assert "T45 Holdout Approval Decision Review completed" in prompt
    assert "T46 Live-Feed Boundary Contract" in prompt
    assert "Phase 11 Live-Feed Dry Run Readiness" in prompt
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T45")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T46")
    assert "Status:     active" in _task_section(tasks, "T47")
    assert "Status:     pending" in _task_section(tasks, "T48")
    assert "HOLDOUT-APPROVAL-DECISION" in audit_index
    assert "`docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md`" in audit_index


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
