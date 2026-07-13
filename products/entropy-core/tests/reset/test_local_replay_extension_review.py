"""Local replay extension review tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "LOCAL_REPLAY_EXTENSION_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_local_replay_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for section in (
        "## Approval Event Summary",
        "## Replay Primitive Summary",
        "## Replay Evidence Summary",
        "## Evidence-Delta Decision Summary",
        "## Non-Approval Regression Summary",
        "## Validation",
        "## Limitations",
        "## Open Findings",
        "## Product Hypothesis Status",
        "## Roadmap Evaluation",
        "## Next Decision Point",
    ):
        assert section in text
    assert "PASS" in text
    assert "Stop-Ship: 0" in text
    assert "No open findings" in text
    assert "510 passed, 20 skipped" in text
    for ref in (
        "docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md",
        "src/entropy/simbroker/replay.py",
        "docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT.md",
        "docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md",
        "docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md",
        "tests/reset/test_replay_evidence_non_approval_regression.py",
    ):
        assert f"`{ref}`" in text
        assert (PROJECT_ROOT / ref).is_file()


def test_local_replay_review_records_hypothesis_status() -> None:
    text = REVIEW.read_text(encoding="utf-8").lower()

    for status in (
        "product hypothesis status after replay:",
        "local_evidence_strengthened_not_confirmed",
        "product hypothesis confirmation status: not_confirmed",
        "product hypothesis rejection status: not_rejected",
        "evidence sufficient for product confirmation: false",
        "evidence sufficient for restricted validation approval: false",
        "next validation execution approved: false",
    ):
        assert status in text
    for blocked in (
        "holdout read or unlock",
        "oos/performance conclusion",
        "sandbox order emission from code",
        "broker/exchange execution from code",
        "production credential loading",
        "live capital action",
        "production label",
        "capital-ready label",
    ):
        assert blocked in text


def test_local_replay_review_updates_state() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "Phase: 31" in prompt
    assert "T66-T68 remain pending but deferred" in prompt
    assert "Phase 14 replay work is complete through T65" in prompt
    assert "local_evidence_strengthened_not_confirmed" in prompt
    assert "Status:     deferred 2026-05-11 artifact-support override" in _task_section(
        tasks, "T68"
    )
    assert "LOCAL-REPLAY-EXTENSION" in audit_index
    assert "`docs/audit/LOCAL_REPLAY_EXTENSION_REVIEW.md`" in audit_index


def _task_section(text: str, task_id: str) -> str:
    start = text.index(f"## {task_id}:")
    next_task = text.find("\n## T", start + 1)
    return text[start:] if next_task == -1 else text[start:next_task]
