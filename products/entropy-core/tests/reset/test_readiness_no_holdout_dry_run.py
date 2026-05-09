"""No-holdout readiness dry-run contract tests."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKET = PROJECT_ROOT / "docs" / "readiness" / "PHASE_GATE_READINESS_PACKET.md"
ARCHIVE_ARTIFACTS = (
    "docs/research/first-packet/CANDIDATE_PACKET.md",
    "docs/research/first-packet/DATASET_MANIFEST.md",
    "docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md",
    "docs/research/second-packet/CANDIDATE_PACKET.md",
    "docs/research/second-packet/DATASET_MANIFEST.md",
    "docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md",
    "docs/research/REPRODUCIBILITY_MATRIX.md",
    "docs/readiness/PHASE_GATE_GAP_MATRIX.md",
    "docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md",
    "docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md",
)
RESTRICTED_TRUE_FLAGS = (
    re.compile(r"\bholdout_unlock:\s*True\b"),
    re.compile(r"\boos_performance_approval:\s*True\b"),
    re.compile(r"\bphase_gate_approval:\s*True\b"),
    re.compile(r"\bproduction_approval:\s*True\b"),
    re.compile(r"\bcapital_ready_approval:\s*True\b"),
    re.compile(r"\blive_feed_approval:\s*True\b"),
    re.compile(r"\bbroker_exchange_approval:\s*True\b"),
    re.compile(r"\bHoldout path opened:\s*True\b"),
    re.compile(r"\bHoldout read executed:\s*True\b"),
    re.compile(r"\bClaim conclusion produced:\s*True\b"),
)


def test_readiness_dry_run_uses_archive_only_artifacts() -> None:
    text = PACKET.read_text(encoding="utf-8")

    assert "Dry-run status: ARCHIVE_ONLY_NO_HOLDOUT_READ" in text
    for artifact in ARCHIVE_ARTIFACTS:
        assert f"`{artifact}`" in text
        assert (PROJECT_ROOT / artifact).is_file()
    assert "holdout/" not in _dry_run_section(text).lower()


def test_readiness_dry_run_rejects_restricted_flags() -> None:
    text = PACKET.read_text(encoding="utf-8")

    for pattern in RESTRICTED_TRUE_FLAGS:
        assert pattern.search(text) is None, pattern.pattern
    for boundary in (
        "holdout_unlock: False",
        "oos_performance_approval: False",
        "phase_gate_approval: False",
        "production_approval: False",
        "capital_ready_approval: False",
        "live_feed_approval: False",
        "broker_exchange_approval: False",
        "Holdout path opened: False",
        "Holdout read executed: False",
        "Holdout unlock requested: False",
        "Claim conclusion produced: False",
    ):
        assert boundary in text


def test_readiness_dry_run_records_limitations() -> None:
    text = PACKET.read_text(encoding="utf-8")
    dry_run = _dry_run_section(text)

    for prerequisite in (
        "explicit human phase-gate approval",
        "explicit human holdout approval",
        "holdout access protocol",
        "Phase 8 readiness review",
    ):
        assert f"Missing prerequisite: {prerequisite}" in dry_run
    assert "No performance conclusion may be inferred" in text
    assert "not executable permission" in text


def _dry_run_section(text: str) -> str:
    start = text.index("## No-Holdout Dry Run Output")
    next_section = text.find("\n## ", start + 1)
    return text[start:] if next_section == -1 else text[start:next_section]
