"""Holdout access protocol contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = PROJECT_ROOT / "docs" / "protocols" / "HOLDOUT_ACCESS_PROTOCOL.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"

REQUIRED_STATES = (
    "DENIED_BY_DEFAULT",
    "PROTOCOL_INCOMPLETE",
    "APPROVAL_EVENT_ABSENT",
    "FUTURE_APPROVAL_REQUIRED",
)
REQUIRED_APPROVAL_EVIDENCE = (
    "human holdout approval event",
    "approval event schema",
    "holdout access audit logging contract",
    "leakage guard proof",
    "phase review",
)
ALLOWED_LOCAL_ONLY_OPERATIONS = (
    "write Markdown protocol contracts",
    "write schema fixtures",
    "write tests",
    "record evidence index",
    "review existing archive-only readiness artifacts",
)
FORBIDDEN_ACTIONS = (
    "opening a holdout file path",
    "reading holdout data",
    "unlocking holdout data",
    "deriving an OOS/performance claim",
    "treating protocol scaffolds as executable permission",
    "activating live feeds",
)
NON_APPROVAL_SOURCES = (
    "roadmap phases",
    "review recommendations",
    "passing local tests",
    "readiness docs",
    "archive evidence packets",
    "generated packet scaffolds",
    "Phase 8 readiness review",
    "Phase 9 protocol documents",
)


def test_holdout_protocol_records_denied_by_default_contract() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_ACCESS_DENIED_BY_DEFAULT" in text
    assert "Current state: DENIED_BY_DEFAULT" in text
    for state in REQUIRED_STATES:
        assert state in text
    for evidence in REQUIRED_APPROVAL_EVIDENCE:
        assert evidence in text
    for operation in ALLOWED_LOCAL_ONLY_OPERATIONS:
        assert operation in text
    for action in FORBIDDEN_ACTIONS:
        assert action in text
    for boundary in (
        "holdout read: blocked",
        "holdout unlock: blocked",
        "explicit human holdout approval event: absent",
        "OOS/performance approval: blocked",
    ):
        assert boundary in text
    assert "does not approve, unlock, open,\nor read holdout data" in text


def test_holdout_protocol_rejects_implicit_approval_sources() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    fail_closed = _section(text, "## Fail-Closed Rules")

    assert "must be rejected as implicit\napproval sources" in text
    for source in NON_APPROVAL_SOURCES:
        assert f"- {source}" in text
    assert "status is BLOCKED" in fail_closed
    assert "roadmap phase" in fail_closed
    assert "review recommendation" in fail_closed
    assert "passing test" in fail_closed
    assert "readiness artifact" in fail_closed
    assert "generated scaffold" in fail_closed


def test_prompt_and_handoff_record_protocol_only_phase() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "phase 9 is protocol-only" in combined
    assert "holdout read/unlock still blocked" in combined
    assert "active task: t66 local replay evidence delta decision" in handoff
    assert "t35 holdout access protocol deny-by-default contract completed" in prompt
    assert "t36 holdout approval event schema contract completed" in prompt
    assert "t37 holdout access audit logging contract completed" in prompt
    assert "t38 holdout leakage guard protocol fixture completed" in prompt
    assert "t39 holdout access protocol review completed" in prompt
    assert "t40 holdout approval request packet scaffold completed" in prompt
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "the only current approval is local_broker_sandbox_no_capital_replay" in prompt
    assert "real external side effects" in combined
    assert "holdout reads" in combined
    assert "holdout unlocks" in combined


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_section = text.find("\n## ", start + 1)
    return text[start:] if next_section == -1 else text[start:next_section]
