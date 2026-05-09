"""Phase-gate readiness review contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "PHASE_GATE_READINESS_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_phase_gate_readiness_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Gap Matrix Summary",
        "## Readiness Packet Summary",
        "## Approval Checklist Summary",
        "## No-Holdout Dry Run Evidence",
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
    assert "405 passed, 20 skipped" in text
    assert "Holdout remains locked and unread" in text
    assert "Phase-gate approval is not granted" in text


def test_phase_gate_readiness_review_records_roadmap_evaluation() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Decision: keep the planned Phase 9 direction" in text
    assert "modified to protocol-only holdout access design" in text
    assert "Next active phase: Phase 9 Holdout Access Protocol" in text
    assert "Next active task: T35 Holdout Access Protocol Deny-By-Default Contract" in text
    assert "must not read a holdout path" in text
    assert "PHASE-GATE-READINESS-REVIEW" in audit_index
    assert "`docs/audit/PHASE_GATE_READINESS_REVIEW.md`" in audit_index


def test_phase_gate_readiness_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")

    assert "Phase: 9" in prompt
    assert "T34 Phase-Gate Readiness Review completed" in prompt
    assert "T35 Holdout Access Protocol Deny-By-Default Contract" in prompt
    assert "Phase 9 Holdout Access Protocol" in prompt
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T34")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T35")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T36")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T37")
    assert "Status:     active" in _task_section(tasks, "T38")
    assert "No holdout path may be opened or read" in _task_section(tasks, "T35")


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
