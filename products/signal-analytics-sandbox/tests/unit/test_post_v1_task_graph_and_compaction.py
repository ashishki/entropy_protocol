from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_post_v1_task_graph_lists_next_phases_and_active_task() -> None:
    tasks = (PROJECT_ROOT / "docs/tasks.md").read_text(encoding="utf-8")
    prompt = (PROJECT_ROOT / "docs/CODEX_PROMPT.md").read_text(encoding="utf-8")

    for task_id in (
        "SAS-NEXT-001",
        "SAS-NEXT-004",
        "SAS-NEXT-032",
        "SAS-IMPACT-001",
        "SAS-BABLOS-001",
        "SAS-PRECLIENT-001",
        "SAS-PRECLIENT-002",
        "SAS-PRECLIENT-003",
        "SAS-PRECLIENT-004",
        "SAS-PRECLIENT-005",
        "SAS-PRECLIENT-006",
        "SAS-PRECLIENT-007",
        "SAS-PRECLIENT-008",
        "SAS-PRECLIENT-009",
        "SAS-PRECLIENT-010",
        "SAS-CLIENTREADY-001",
        "SAS-CLIENTREADY-002",
        "SAS-CLIENTREADY-003",
        "SAS-CLIENTREADY-004",
        "SAS-AUTOVAL-001",
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

    assert "## Phase 28 — External-Ready Review Sprint" in tasks
    assert "## Phase 35 — Reliability And Scaling" in tasks
    assert (
        "## Phase 36 — Channel Impact Framework And Cross-Channel Completion" in tasks
    )
    assert "## Phase 37 — Pre-Client Artifact Hardening" in tasks
    assert "## Phase 38 — Client-Readiness Evidence Acceptance" in tasks
    latest_completed = "Latest completed: `MVP Value Run - 2026-05-31`"
    assert latest_completed in prompt
    assert "Active route: post-Phase-42 MVP value assessment." in prompt


def test_active_state_files_are_compacted_to_current_links() -> None:
    compacted_files = [
        "docs/CODEX_PROMPT.md",
        "AGENT_NOTES.md",
        "PHASE_HANDOFF.md",
        "ORCHESTRATOR_CHECKPOINT.md",
    ]

    for relative_path in compacted_files:
        line_count = len(
            (PROJECT_ROOT / relative_path).read_text(encoding="utf-8").splitlines()
        )
        assert line_count <= 100

    archive = (
        PROJECT_ROOT / "docs/archive/POST_V1_STATE_COMPACTION_2026-05-19.md"
    ).read_text(encoding="utf-8")
    assert "active-state-compacted" in archive
    assert "SAS-NEXT-001 Full-Corpus Human Review Queue" in archive
