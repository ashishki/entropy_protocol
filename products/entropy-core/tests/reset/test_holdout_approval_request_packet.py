"""Holdout approval request packet contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKET = PROJECT_ROOT / "docs" / "approvals" / "HOLDOUT_APPROVAL_REQUEST_PACKET.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"

REQUIRED_EVIDENCE = (
    "docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md",
    "docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md",
    "docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md",
    "docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md",
    "docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md",
)


def test_holdout_approval_request_packet_lists_required_evidence() -> None:
    text = PACKET.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_APPROVAL_REQUEST_SCAFFOLD_NO_APPROVAL" in text
    for evidence in REQUIRED_EVIDENCE:
        assert f"`{evidence}`" in text
        assert (PROJECT_ROOT / evidence).is_file()
    assert "approval evidence intake" in text
    assert "approval-absent denial" in text
    assert "no-read decision dry run" in text


def test_holdout_approval_request_packet_preserves_no_approval_state() -> None:
    text = PACKET.read_text(encoding="utf-8").lower()

    assert "does not create,\nrequest, infer, or grant approval" in text
    assert "explicit human holdout approval event: absent" in text
    assert "phase-gate approval: absent" in text
    assert "holdout read: blocked" in text
    assert "holdout unlock: blocked" in text
    assert "holdout path opened: false" in text
    assert "holdout read executed: false" in text
    assert "holdout unlock requested: false" in text
    assert "oos/performance approval: blocked" in text


def test_state_docs_record_phase10_no_read_decision_work() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "phase: 13" in prompt
    assert "phase 11 live-feed dry run readiness" in combined
    assert (
        "current active task is checkpoint after phase 13 product hypothesis confirmation decision"
        in prompt
    )
    assert (
        "active task: checkpoint after phase 13 product hypothesis confirmation decision" in handoff
    )
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "t40 holdout approval request packet scaffold completed" in prompt
    assert "no approval event currently exists" in combined
    assert "holdout read/unlock still blocked" in combined
