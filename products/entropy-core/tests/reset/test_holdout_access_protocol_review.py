"""Holdout access protocol review contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "HOLDOUT_ACCESS_PROTOCOL_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_holdout_access_protocol_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Protocol Summary",
        "## Approval Schema Summary",
        "## Audit Logging Summary",
        "## Leakage Guard Summary",
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
    assert "420 passed, 20 skipped" in text
    assert "Holdout remains locked and unread" in text


def test_holdout_access_protocol_review_records_roadmap_evaluation() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    assert "Decision: modify the planned Phase 10 direction" in text
    assert "replace the planned approved holdout evaluation packet" in text
    assert "no-read approval decision packet phase" in text
    assert "Next active phase: Phase 10 Holdout Approval Decision Packet" in text
    assert "Next active task: T40 Holdout Approval Request Packet Scaffold" in text
    assert "must not open a holdout path" in text
    assert "No explicit human holdout approval event exists" in text


def test_holdout_access_protocol_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Phase: 13" in prompt
    assert "T39 Holdout Access Protocol Review completed" in prompt
    assert "T40 Holdout Approval Request Packet Scaffold" in prompt
    assert "Phase 10 Holdout Approval Decision Packet" in prompt
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T39")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T40")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T41")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T56")
    assert "HOLDOUT-ACCESS-PROTOCOL" in audit_index
    assert "`docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md`" in audit_index


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
