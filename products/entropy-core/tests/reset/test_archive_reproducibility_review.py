"""Archive reproducibility hardening review contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "ARCHIVE_REPRODUCIBILITY_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_archive_reproducibility_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Replay Evidence",
        "## Reproducibility Matrix",
        "## No-Claim Sweep",
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
    assert "390 passed, 20 skipped" in text
    assert "Holdout remains locked and unread" in text


def test_archive_reproducibility_review_records_roadmap_evaluation() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Decision: keep the planned Phase 8 direction" in text
    assert "Next active phase: Phase 8 Phase-Gate Readiness Review" in text
    assert "Next active task: T30 Archive Evidence Sufficiency Gap Matrix" in text
    assert "Roadmap action: keep Phase 8 focused on readiness and gap analysis only" in text
    assert "ARCHIVE-REPRODUCIBILITY-HARDENING" in audit_index
    assert "`docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`" in audit_index


def test_codex_prompt_records_phase7_review_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")

    assert "Phase: 31" in prompt
    assert "T29 Archive Reproducibility Hardening Review completed" in prompt
    assert "T34 Phase-Gate Readiness Review completed" in prompt
    assert "T35 Holdout Access Protocol Deny-By-Default Contract" in prompt
    assert "Phase 8 Phase-Gate Readiness Review" in prompt
    assert "Status:     done 2026-05-08" in _task_section(tasks, "T29")
    assert "Status:     done 2026-05-08" in _task_section(tasks, "T30")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T31")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T32")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T33")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T34")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T35")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T36")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T37")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T38")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T39")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T40")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T41")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T56")


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
