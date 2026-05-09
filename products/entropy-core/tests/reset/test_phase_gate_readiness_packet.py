"""Phase-gate readiness packet scaffold contract tests."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKET = PROJECT_ROOT / "docs" / "readiness" / "PHASE_GATE_READINESS_PACKET.md"
DISALLOWED_APPROVAL_PATTERNS = (
    re.compile(r"\bholdout_unlock:\s*True\b"),
    re.compile(r"\boos_performance_approval:\s*True\b"),
    re.compile(r"\bphase_gate_approval:\s*True\b"),
    re.compile(r"\bproduction_approval:\s*True\b"),
    re.compile(r"\bcapital_ready_approval:\s*True\b"),
    re.compile(r"\blive_feed_approval:\s*True\b"),
    re.compile(r"\bbroker_exchange_approval:\s*True\b"),
    re.compile(r"\bStatus:\s*(?:APPROVED|PRODUCTION_READY|CAPITAL_READY)\b"),
)


def test_readiness_packet_contains_required_sections() -> None:
    text = PACKET.read_text(encoding="utf-8")

    for section in (
        "## Evidence Summary",
        "## Missing Controls",
        "## Limitations",
        "## Required Human Approvals",
        "## Non-Approval Boundary",
        "## Next Review Input",
    ):
        assert section in text
    assert "Status: READINESS_SCAFFOLD_NO_APPROVAL" in text
    assert "Explicit human phase-gate approval is absent" in text
    assert "Approval boundary checklist is pending" in text
    assert "No-holdout readiness dry run is pending" in text


def test_readiness_packet_rejects_approval_labels() -> None:
    text = PACKET.read_text(encoding="utf-8")

    for pattern in DISALLOWED_APPROVAL_PATTERNS:
        assert pattern.search(text) is None, pattern.pattern
    for boundary in (
        "holdout_unlock: False",
        "oos_performance_approval: False",
        "phase_gate_approval: False",
        "production_approval: False",
        "capital_ready_approval: False",
        "live_feed_approval: False",
        "broker_exchange_approval: False",
    ):
        assert boundary in text
    assert "must not grant approval" in text


def test_readiness_packet_references_gap_matrix_and_review() -> None:
    text = PACKET.read_text(encoding="utf-8")

    assert "`docs/readiness/PHASE_GATE_GAP_MATRIX.md`" in text
    assert "`docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`" in text
    assert "`docs/research/REPRODUCIBILITY_MATRIX.md`" in text
    assert "`tests/reset/test_phase_gate_readiness_gap_matrix.py`" in text
