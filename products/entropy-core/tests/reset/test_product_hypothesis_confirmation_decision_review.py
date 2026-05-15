"""Product hypothesis confirmation decision review tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "PRODUCT_HYPOTHESIS_CONFIRMATION_DECISION_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_confirmation_decision_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Request Summary",
        "## Intake Summary",
        "## Validation Path Decision Summary",
        "## Non-Approval Regression Summary",
        "## Validation Plan Summary",
        "## Validation",
        "## Limitations",
        "## Open Findings",
        "## Confirmation Status",
        "## Next Human Decision",
        "## Next Recommendation",
    ):
        assert section in text
    assert "PASS" in text
    assert "Stop-Ship: 0" in text
    assert "No open findings" in text
    assert "489 passed, 20 skipped" in text


def test_confirmation_decision_review_records_status() -> None:
    text = REVIEW.read_text(encoding="utf-8").lower()

    for status in (
        "product hypothesis status: unconfirmed_pending_future_validation",
        "evidence sufficient for product confirmation: false",
        "evidence sufficient for local next-step planning: true",
        "next validation execution approved: false",
        "product hypothesis is not confirmed",
        "product hypothesis is not rejected",
    ):
        assert status in text
    for blocked in (
        "holdout read or unlock",
        "oos/performance conclusion",
        "live feed activation",
        "live order placement",
        "broker/exchange execution from code",
        "production credential loading",
        "live capital action",
        "production label",
        "capital-ready label",
    ):
        assert blocked in text


def test_confirmation_decision_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Phase: 27" in prompt
    assert "T62 Product Hypothesis Confirmation Decision Review completed" in prompt
    assert "product hypothesis status: unconfirmed_pending_future_validation" in prompt
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T62")
    assert "PRODUCT-HYPOTHESIS-CONFIRMATION-DECISION" in audit_index
    assert "`docs/audit/PRODUCT_HYPOTHESIS_CONFIRMATION_DECISION_REVIEW.md`" in audit_index


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
