"""Holdout decision no-read dry run tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DRY_RUN = PROJECT_ROOT / "docs" / "approvals" / "HOLDOUT_DECISION_DRY_RUN.md"

REQUIRED_ARTIFACTS = (
    "docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md",
    "docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md",
    "docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md",
    "docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md",
    "docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md",
    "docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md",
    "docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md",
    "docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md",
    "tests/reset/test_holdout_non_approval_source_regression.py",
)

RESTRICTED_FLAGS = (
    "holdout path opened: true",
    "holdout read executed: true",
    "holdout unlock requested: true",
    "raw holdout path inspected: true",
    "holdout read: allowed",
    "holdout unlock: allowed",
    "holdout read approval flag: present",
    "holdout unlock approval flag: present",
    "OOS/performance approval flag: present",
    "OOS/performance conclusion: approved",
    "production readiness: approved",
    "capital-ready conclusion: approved",
)


def test_decision_dry_run_uses_no_read_artifacts() -> None:
    text = DRY_RUN.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_DECISION_DRY_RUN_DENIED_NO_READ" in text
    assert "dry run mode: local no-read assembly" in text
    for artifact in REQUIRED_ARTIFACTS:
        assert f"`{artifact}`" in text
        assert (PROJECT_ROOT / artifact).is_file()
    assert "holdout path opened: false" in text
    assert "raw holdout path inspected: false" in text


def test_decision_dry_run_rejects_restricted_flags() -> None:
    text = DRY_RUN.read_text(encoding="utf-8")
    lower = text.lower()

    for flag in RESTRICTED_FLAGS:
        assert flag.lower() not in lower
    assert "holdout read approval flag: absent" in text
    assert "holdout unlock approval flag: absent" in text
    assert "OOS/performance approval flag: absent" in text
    assert "holdout read: blocked" in text
    assert "holdout unlock: blocked" in text


def test_decision_dry_run_records_denial_state() -> None:
    text = DRY_RUN.read_text(encoding="utf-8")

    assert "decision: DENIED" in text
    assert "access_decision: BLOCKED" in text
    assert "approval reference: absent" in text
    assert "current holdout approval event: absent" in text
    for prerequisite in (
        "explicit human holdout approval: missing",
        "explicit human phase-gate approval: missing",
        "approval intake accepted event: missing",
        "leakage guard status: incomplete",
        "current approval event: absent",
    ):
        assert prerequisite in text
