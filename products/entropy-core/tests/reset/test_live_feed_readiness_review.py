"""Live-feed readiness review tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "LIVE_FEED_READINESS_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_live_feed_readiness_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Boundary Summary",
        "## Fixture Manifest Summary",
        "## Adapter Contract Summary",
        "## Observability Packet Summary",
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
    assert "453 passed, 20 skipped" in text
    assert "Holdout remains locked and unread" in text


def test_live_feed_readiness_review_records_roadmap_evaluation() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    assert "Decision: modify the broker sandbox phase" in text
    assert "sandbox-only execution risk audit work" in text
    assert "Next active phase: Phase 12 Broker Sandbox and Execution Risk Audit" in text
    assert "Next active task: T51 Broker Sandbox Boundary Contract" in text
    assert "must not connect to live broker/exchange execution" in text
    assert "No live capital action was approved" in text


def test_live_feed_readiness_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Phase: 31" in prompt
    assert "T50 Live-Feed Dry Run Readiness Review completed" in prompt
    assert "T51 Broker Sandbox Boundary Contract" in prompt
    assert "Phase 12 Broker Sandbox and Execution Risk Audit" in prompt
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T50")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T51")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T55")
    assert "Status:     done 2026-05-09" in _task_section(tasks, "T56")
    assert "LIVE-FEED-READINESS" in audit_index
    assert "`docs/audit/LIVE_FEED_READINESS_REVIEW.md`" in audit_index


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
