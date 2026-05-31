"""Holdout approval event schema contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA = PROJECT_ROOT / "docs" / "protocols" / "HOLDOUT_APPROVAL_EVENT_SCHEMA.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"

REQUIRED_FIELDS = (
    "approval_id",
    "approver_identity",
    "approval_scope",
    "candidate_hash",
    "evidence_hash",
    "policy_hash",
    "expires_at_utc",
    "revocation_state",
    "audit_metadata",
)
INVALID_FIXTURE_CLASSES = (
    "generated approval event",
    "inferred approval event",
    "expired approval event",
    "revoked approval event",
    "incomplete approval event",
)
REJECTION_REASON_CODES = (
    "GENERATED_APPROVAL_NOT_ALLOWED",
    "INFERRED_APPROVAL_NOT_ALLOWED",
    "APPROVAL_EXPIRED",
    "APPROVAL_REVOKED",
    "APPROVAL_EVENT_INCOMPLETE",
)


def test_holdout_approval_event_schema_requires_governance_fields() -> None:
    text = SCHEMA.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_APPROVAL_EVENT_ABSENT" in text
    assert "does not create, imply, infer,\nor activate any approval event" in text
    for field in REQUIRED_FIELDS:
        assert f"`{field}`" in text
    for requirement in (
        "`approval_source` is `explicit_human_governance_event`",
        "`approval_scope.boundary` is `holdout_access`",
        "`revocation_state` is `not_revoked`",
    ):
        assert requirement in text


def test_holdout_approval_event_schema_rejects_invalid_approval_events() -> None:
    text = SCHEMA.read_text(encoding="utf-8")
    invalid_section = _section(text, "## Invalid Fixture Classes")

    for fixture_class in INVALID_FIXTURE_CLASSES:
        assert fixture_class in invalid_section
    for reason_code in REJECTION_REASON_CODES:
        assert reason_code in text
    assert "roadmap-derived approval event" in invalid_section
    assert "review-recommendation-derived approval event" in invalid_section
    assert "passing-test-derived approval event" in invalid_section
    assert "placeholder hash approval event" in invalid_section
    assert "scope-mismatch approval event" in invalid_section


def test_state_docs_record_no_current_holdout_approval_event() -> None:
    schema = SCHEMA.read_text(encoding="utf-8").lower()
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "current holdout approval event: absent" in schema
    assert "explicit human holdout approval: absent" in schema
    assert "holdout read: blocked" in schema
    assert "holdout unlock: blocked" in schema
    assert "t122 core v1 productization review completed" in prompt
    assert "active task:" in handoff
    assert "t36 holdout approval event schema contract completed" in prompt
    assert "t37 holdout access audit logging contract completed" in prompt
    assert "t38 holdout leakage guard protocol fixture completed" in prompt
    assert "t39 holdout access protocol review completed" in prompt
    assert "t40 holdout approval request packet scaffold completed" in prompt
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "no approval event currently exists" in combined
    assert "holdout read/unlock still blocked" in combined


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_section = text.find("\n## ", start + 1)
    return text[start:] if next_section == -1 else text[start:next_section]
