"""Holdout approval evidence intake contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "approvals" / "HOLDOUT_APPROVAL_INTAKE_CONTRACT.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"

REQUIRED_FIELDS = (
    "approval_id",
    "approver_identity",
    "approval_source",
    "approval_scope",
    "candidate_hash",
    "evidence_hash",
    "policy_hash",
    "parameter_hash",
    "expires_at_utc",
    "revocation_state",
    "audit_metadata",
)
REJECTED_FIXTURES = (
    "absent approval evidence",
    "generated approval evidence",
    "inferred approval evidence",
    "expired approval evidence",
    "revoked approval evidence",
    "stale hash evidence",
    "scope-mismatched evidence",
)
REASON_CODES = (
    "APPROVAL_EVENT_ABSENT",
    "GENERATED_APPROVAL_NOT_ALLOWED",
    "INFERRED_APPROVAL_NOT_ALLOWED",
    "APPROVAL_EXPIRED",
    "APPROVAL_REVOKED",
    "STALE_HASH_BINDING",
    "APPROVAL_SCOPE_MISMATCH",
)


def test_holdout_approval_intake_lists_required_fields() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_APPROVAL_INTAKE_CONTRACT_NO_EVENT" in text
    for field in REQUIRED_FIELDS:
        assert f"`{field}`" in text
    for binding in (
        "candidate hash matches",
        "evidence hash matches",
        "policy hash matches",
        "parameter hash matches",
        "approval scope references",
    ):
        assert binding in text


def test_holdout_approval_intake_rejects_invalid_evidence() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    fixtures = _section(text, "## Rejected Intake Fixtures")

    for fixture in REJECTED_FIXTURES:
        assert fixture in fixtures
        assert f"| {fixture} | REJECTED |" in fixtures
    for reason_code in REASON_CODES:
        assert reason_code in fixtures


def test_state_docs_preserve_no_approval_event() -> None:
    contract = CONTRACT.read_text(encoding="utf-8").lower()
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "current holdout approval event: absent" in contract
    assert "intake decision: rejected" in contract
    assert "holdout read: blocked" in contract
    assert "holdout unlock: blocked" in contract
    assert "current active task is t49 live-feed observability packet" in prompt
    assert "active task: t49 live-feed observability packet" in handoff
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "no approval event currently exists" in combined
    assert "holdout read/unlock still blocked" in combined


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_section = text.find("\n## ", start + 1)
    return text[start:] if next_section == -1 else text[start:next_section]
