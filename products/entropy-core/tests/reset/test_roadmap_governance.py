"""Roadmap governance contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TASKS = PROJECT_ROOT / "docs" / "tasks.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"
CODEX_LOOP = PROJECT_ROOT / "CODEX_LOOP.md"


def test_tasks_records_planned_roadmap_and_active_phase() -> None:
    text = TASKS.read_text(encoding="utf-8")

    for phase in (
        "Archive Reproducibility Hardening",
        "Phase-Gate Readiness Review",
        "Holdout Access Protocol",
        "Approved Holdout Evaluation Packet",
        "Live-Feed Dry Run Readiness",
        "Broker Sandbox and Execution Risk Audit",
        "Production and Capital Gate",
    ):
        assert phase in text
    assert "Phase boundaries are autonomous rollover points, not stop points" in text
    assert "open the next logical active phase, and continue automatically" in text
    assert "Status:     done 2026-05-08" in _task_section(text, "T26")
    assert "Status:     done 2026-05-08" in _task_section(text, "T27")
    assert "Status:     done 2026-05-08" in _task_section(text, "T28")
    assert "Status:     active" in _task_section(text, "T29")


def test_tasks_records_dynamic_roadmap_evaluation_rule() -> None:
    text = TASKS.read_text(encoding="utf-8")
    roadmap_section = text[text.index("## Roadmap Governance") :]

    assert "After every active phase closes" in roadmap_section
    assert (
        "run deep review, fix actionable findings, validate, evaluate the roadmap"
        in roadmap_section
    )
    assert "summarize what the completed phase changed" in roadmap_section
    assert (
        "keep the next planned phase, modify future planned phases, or open a better next active phase"
        in roadmap_section
    )
    assert (
        "real external side effects, live capital actions, live broker/exchange execution, and credentialed production deployment blocked"
        in roadmap_section
    )


def test_prompt_and_handoff_record_phase7_boundaries() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8")
    loop = CODEX_LOOP.read_text(encoding="utf-8")
    combined = f"{prompt}\n{handoff}\n{loop}".lower()

    assert "phase: 7" in prompt.lower()
    assert "t29 archive reproducibility hardening review" in prompt.lower()
    assert "t28 no-claim surface regression sweep completed" in prompt.lower()
    assert "t27 evidence hash reproducibility matrix completed" in prompt.lower()
    assert "t26 archive packet replay contract completed" in prompt.lower()
    assert "phase: 7 archive reproducibility hardening" in handoff.lower()
    assert "phase boundaries are not stop conditions" in combined
    assert "roadmap rewrite -> open next active phase -> next task" in combined
    assert "continue automatically" in combined
    for boundary in (
        "real external side effect",
        "live capital",
        "live broker/exchange",
        "credentialed production deployment",
    ):
        assert boundary in combined


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
