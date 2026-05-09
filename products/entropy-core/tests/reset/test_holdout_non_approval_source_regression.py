"""Holdout non-approval source regression tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ACTIVE_DOCS = (
    "docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md",
    "docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md",
    "docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md",
    "docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md",
    "docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md",
    "docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md",
    "docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md",
    "docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md",
    "docs/CODEX_PROMPT.md",
    "PHASE_HANDOFF.md",
)

RESTRICTED_APPROVAL_MARKERS = (
    "status: approved",
    "status: production_ready",
    "status: capital_ready",
    "current holdout approval event: present",
    "explicit human holdout approval: present",
    "phase-gate approval: approved",
    "human approval granted",
    "approval event accepted",
    "holdout read: allowed",
    "holdout unlock: allowed",
    "holdout path opened: true",
    "holdout read executed: true",
    "holdout unlock requested: true",
    "oos/performance conclusion: approved",
    "production readiness: approved",
    "capital-ready conclusion: approved",
)

NON_APPROVAL_SOURCES = (
    "roadmap phases",
    "protocol documents",
    "review recommendations",
    "passing tests",
    "readiness artifacts",
    "generated scaffolds",
)


def _read(path: str) -> str:
    doc = PROJECT_ROOT / path
    assert doc.is_file(), path
    return doc.read_text(encoding="utf-8")


def test_phase10_docs_reject_implicit_approval_sources() -> None:
    docs = {path: _read(path).lower() for path in ACTIVE_DOCS}
    combined = "\n".join(docs.values())

    for path, text in docs.items():
        for marker in RESTRICTED_APPROVAL_MARKERS:
            assert marker not in text, f"{marker!r} found in {path}"
    for source in NON_APPROVAL_SOURCES:
        assert source in combined
    assert "not approval sources" in combined
    assert "cannot treat roadmap phases" in combined


def test_state_docs_record_no_current_approval_event() -> None:
    prompt = _read("docs/CODEX_PROMPT.md").lower()
    handoff = _read("PHASE_HANDOFF.md").lower()
    combined = f"{prompt}\n{handoff}"

    assert "no approval event currently exists" in combined
    assert "current active task is t45 holdout approval decision review" in prompt
    assert "active task: t45 holdout approval decision review" in handoff
    assert "current holdout approval event: present" not in combined
    assert "explicit human holdout approval: present" not in combined


def test_holdout_read_unlock_remain_blocked() -> None:
    combined = "\n".join(_read(path).lower() for path in ACTIVE_DOCS)

    assert "holdout: locked" in combined
    assert "holdout read: blocked" in combined
    assert "holdout unlock: blocked" in combined
    assert "holdout read/unlock still blocked" in combined
    assert "holdout path opened: true" not in combined
    assert "holdout read executed: true" not in combined
    assert "holdout unlock requested: true" not in combined
