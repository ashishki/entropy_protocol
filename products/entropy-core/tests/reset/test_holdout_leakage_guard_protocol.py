"""Holdout leakage guard protocol fixture tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GUARD = PROJECT_ROOT / "docs" / "protocols" / "HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"

REQUIRED_INPUTS = (
    "candidate binding",
    "dataset partition proof",
    "code hash",
    "policy hash",
    "parameter hash",
    "training-window proof",
    "no-prior-holdout-read evidence",
)
FAIL_CLOSED_CASES = (
    "missing approval",
    "stale hashes",
    "partition overlap",
    "prior holdout read",
    "unresolved evidence",
)
REASON_CODES = (
    "MISSING_HUMAN_HOLDOUT_APPROVAL",
    "STALE_HASH_BINDING",
    "HOLDOUT_PARTITION_OVERLAP",
    "PRIOR_HOLDOUT_READ_DETECTED",
    "UNRESOLVED_GUARD_EVIDENCE",
)


def test_holdout_leakage_guard_lists_required_inputs() -> None:
    text = GUARD.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_LEAKAGE_GUARD_INCOMPLETE" in text
    for required_input in REQUIRED_INPUTS:
        assert required_input in text
    for source in (
        "`src/entropy/walkforward/leakage.py`",
        "`src/entropy/data/holdout.py`",
        "`docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`",
    ):
        assert source in text
    assert "Training and archive windows end before any holdout window begins" in text


def test_holdout_leakage_guard_records_fail_closed_behavior() -> None:
    text = GUARD.read_text(encoding="utf-8")
    fail_closed = _section(text, "## Fail-Closed Behavior")
    matrix = _section(text, "## Fixture Matrix")

    assert "fail closed" in text
    for case in FAIL_CLOSED_CASES:
        assert case in fail_closed
        assert f"| {case} | BLOCKED |" in matrix
    for reason_code in REASON_CODES:
        assert reason_code in matrix
    assert "expired approval" in fail_closed
    assert "revoked approval" in fail_closed
    assert "scope mismatch" in fail_closed


def test_state_docs_preserve_holdout_lock_during_guard_protocol() -> None:
    guard = GUARD.read_text(encoding="utf-8").lower()
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "guard status: incomplete" in guard
    assert "holdout path opened: false" in guard
    assert "holdout read executed: false" in guard
    assert "holdout unlock requested: false" in guard
    assert "holdout read: blocked" in guard
    assert "holdout unlock: blocked" in guard
    assert "current active task is t69 shared artifact contract freeze" in prompt
    assert "active task: t69 shared artifact contract freeze" in handoff
    assert "t38 holdout leakage guard protocol fixture completed" in prompt
    assert "t39 holdout access protocol review completed" in prompt
    assert "t40 holdout approval request packet scaffold completed" in prompt
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "holdout read/unlock still blocked" in combined


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_section = text.find("\n## ", start + 1)
    return text[start:] if next_section == -1 else text[start:next_section]
