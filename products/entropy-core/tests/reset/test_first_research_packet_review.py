"""First research packet review contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW = PROJECT_ROOT / "docs" / "audit" / "FIRST_RESEARCH_PACKET_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"


def test_first_research_packet_review_contains_required_sections() -> None:
    text = REVIEW.read_text(encoding="utf-8")
    audit_index = AUDIT_INDEX.read_text(encoding="utf-8")

    for heading in (
        "## Candidate",
        "## Evidence",
        "## Validation",
        "## Limitations",
        "## Open Findings",
        "## Next Recommendation",
    ):
        assert heading in text
    assert "FRC-001-VC-BREAKOUT-CONTINUATION" in text
    assert "RESEARCH_EVIDENCE_PACKET.md" in text
    assert "351 passed, 20 skipped" in text
    assert "No open findings" in text
    assert "FIRST-RESEARCH-PACKET" in audit_index
    assert "`docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`" in audit_index


def test_first_research_packet_review_preserves_boundaries() -> None:
    text = REVIEW.read_text(encoding="utf-8")

    for boundary in (
        "Holdout remains locked and unread",
        "Live feeds are not approved",
        "Broker/exchange integration is not approved",
        "Production and capital-ready labels are not approved",
        "OOS/performance claims remain unapproved",
        "does not approve a phase gate",
    ):
        assert boundary in text


def test_codex_prompt_records_first_packet_review_state() -> None:
    text = CODEX_PROMPT.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "First Research Evidence Packet block complete through T19" in text
    assert "Human decision required after T19" in text
    assert "T19 First Research Packet Review completed" in text
    assert (
        "holdout, live feeds, broker/exchange, production, capital-ready, and "
        "oos/performance remain unapproved"
    ) in lower_text
