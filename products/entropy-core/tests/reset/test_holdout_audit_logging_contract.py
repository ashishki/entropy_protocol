"""Holdout access audit logging contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "protocols" / "HOLDOUT_AUDIT_LOGGING_CONTRACT.md"
EVIDENCE_INDEX = PROJECT_ROOT / "docs" / "EVIDENCE_INDEX.md"

REQUIRED_AUDIT_FIELDS = (
    "audit_event_id",
    "request_id",
    "approval_reference",
    "candidate_hash",
    "evidence_hash",
    "access_decision",
    "path_fingerprint",
    "denial_reason",
    "timestamp_utc",
    "actor",
    "source_documents",
)
DENIED_ATTEMPT_FIELDS = (
    "access_decision: BLOCKED",
    "approval_reference: absent",
    "holdout_path_opened: false",
    "holdout_read_executed: false",
    "holdout_unlock_requested: false",
)
DENIAL_REASONS = (
    "MISSING_HUMAN_HOLDOUT_APPROVAL",
    "APPROVAL_EVENT_INVALID",
    "AUDIT_LOGGING_INCOMPLETE",
    "LEAKAGE_GUARD_INCOMPLETE",
)


def test_holdout_audit_logging_contract_lists_required_fields() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_AUDIT_LOGGING_CONTRACT_ONLY" in text
    for field in REQUIRED_AUDIT_FIELDS:
        assert f"`{field}`" in text
    for reason in DENIAL_REASONS:
        assert reason in text
    assert "immutable timezone-aware UTC audit timestamp" in text
    assert "non-reversible fingerprint" in text


def test_holdout_audit_logging_contract_preserves_no_read_boundary() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    privacy = _section(text, "## Path Privacy Boundary")
    denied = _section(text, "## Denied Attempt Contract")
    boundary = _section(text, "## Current Boundary")

    assert "does not approve holdout access" in text
    assert "open holdout data" in text
    assert "read holdout contents" in text
    assert "must not store raw holdout paths" in privacy
    assert "path contents" in privacy
    assert "data previews" in privacy
    for field in DENIED_ATTEMPT_FIELDS:
        assert field in denied
    assert "holdout path opened: false" in boundary
    assert "holdout read executed: false" in boundary
    assert "holdout unlock requested: false" in boundary
    assert "holdout read: blocked" in boundary
    assert "holdout unlock: blocked" in boundary


def test_evidence_index_records_holdout_audit_logging_contract() -> None:
    text = EVIDENCE_INDEX.read_text(encoding="utf-8")

    assert "T37 Holdout Access Audit Logging Contract" in text
    assert "`docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md`" in text
    assert (
        "`tests/reset/test_holdout_audit_logging_contract.py::test_holdout_audit_logging_contract_lists_required_fields`"
        in text
    )
    assert "path fingerprint" in text
    assert "denied attempts" in text
    assert "blocked holdout read/unlock" in text


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_section = text.find("\n## ", start + 1)
    return text[start:] if next_section == -1 else text[start:next_section]
