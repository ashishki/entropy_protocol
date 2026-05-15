"""Archive evidence expansion review contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"


def test_archive_evidence_expansion_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    for heading in (
        "## Packet Set",
        "## Evidence",
        "## Validation",
        "## Limitations",
        "## Open Findings",
        "## Next Recommendation",
    ):
        assert heading in text
    assert "FRC-001-VC-BREAKOUT-CONTINUATION" in text
    assert "SRC-001-STRUCTURE-RETEST-BOUNCE" in text
    assert "Volatility Compression" in text
    assert "Structure Levels" in text
    assert "374 passed, 20 skipped" in text
    assert "No open findings" in text
    assert "ARCHIVE-EVIDENCE-EXPANSION" in audit_index
    assert "`docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`" in audit_index


def test_archive_evidence_expansion_review_preserves_boundaries() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for boundary in (
        "Holdout remains locked and unread",
        "Live feeds are not approved",
        "Broker/exchange integration is not approved",
        "Production and capital-ready labels are not approved",
        "Phase-gate approval is not granted",
        "OOS/performance claims remain unapproved",
        "archive-only implementation evidence",
    ):
        assert boundary in text


def test_codex_prompt_records_archive_expansion_review_state() -> None:
    text = CODEX_PROMPT.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "Archive Evidence Expansion block complete through T24" in text
    assert "Human decision required after T24" in text
    assert "T24 Archive Evidence Expansion Review completed" in text
    assert (
        "holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, "
        "and oos/performance remain unapproved"
    ) in lower_text
