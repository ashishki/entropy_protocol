from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase_27_task_graph_lists_full_v1_flow() -> None:
    tasks = (PROJECT_ROOT / "docs/tasks.md").read_text(encoding="utf-8")

    assert "## Phase 27 — Three-Channel V1 Metric Report" in tasks
    for task_id in (
        "SAS-V1-001",
        "SAS-V1-002",
        "SAS-V1-003",
        "SAS-V1-004",
        "SAS-V1-005",
        "SAS-V1-006",
        "SAS-V1-007",
        "SAS-V1-008",
        "SAS-V1-009",
    ):
        assert task_id in tasks


def test_phase_27_roadmap_covers_v1_required_improvements() -> None:
    roadmap = (PROJECT_ROOT / "docs/pilot/THREE_CHANNEL_V1_ROADMAP.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Human/operator review of extraction quality",
        "Structured fields beyond direction",
        "Level-aware outcomes",
        "Multimodal evidence",
        "Provider/proxy expansion",
        "Customer-facing gate",
    ):
        assert required in roadmap


def test_phase_27_roadmap_preserves_no_overclaim_boundaries() -> None:
    roadmap = (PROJECT_ROOT / "docs/pilot/THREE_CHANNEL_V1_ROADMAP.md").read_text(
        encoding="utf-8"
    )

    assert "No private Telegram scraping" in roadmap
    assert "No bulk market-history database" in roadmap
    assert "No future-profit claims" in roadmap
    assert "No investment advice" in roadmap
    assert "No unreviewed transcript/OCR/chart claims" in roadmap
