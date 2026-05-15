from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_ideas import (
    MarketIdeaDraftExtractor,
    export_market_idea_drafts,
)
from signal_sandbox.profiles import ChannelProfileRegistry, import_bablos79_profile


def test_batch_export_one_row_per_document() -> None:
    export = export_market_idea_drafts(
        [
            _document("doc-1", "#BTC bullish upside for the week"),
            _document("doc-2", "stream starts at 19:00"),
        ],
        _extractor(),
    )

    assert [row.source_document_id for row in export.rows] == ["doc-1", "doc-2"]
    assert {row.final_review_status for row in export.rows} == {"pending"}
    assert {row.draft_approval_state for row in export.rows} == {"queued_for_review"}


def test_review_queue_policy() -> None:
    export = export_market_idea_drafts(
        [
            _document("doc-1", "#BTC #ETH bullish upside"),
            _document("doc-2", "#BTC market update"),
            _document("doc-3", "#BTC guaranteed profit strong upside"),
        ],
        _extractor(),
    )

    reasons = {
        row.source_document_id: set(row.review_queue_reasons) for row in export.rows
    }

    assert "ambiguous_asset" in reasons["doc-1"]
    assert "unsupported_direction" in reasons["doc-2"]
    assert "customer_facing_claim" in reasons["doc-3"]
    assert "high_impact_claim" in reasons["doc-3"]


def test_export_has_no_approved_side_effects(tmp_path: Path) -> None:
    export = export_market_idea_drafts(
        [_document("doc-1", "#BTC bullish upside")],
        _extractor(),
    )

    export.write_markdown(tmp_path / "MARKET_IDEA_DRAFTS_BABLOS79.md")

    assert (tmp_path / "MARKET_IDEA_DRAFTS_BABLOS79.md").is_file()
    assert not (tmp_path / "ledgers").exists()
    assert not (tmp_path / "outcomes").exists()
    assert not (tmp_path / "reports").exists()


def _extractor() -> MarketIdeaDraftExtractor:
    profile = import_bablos79_profile(
        Path("workspace/lexicons/bablos79_lexicon_draft.json")
    )
    return MarketIdeaDraftExtractor(ChannelProfileRegistry([profile]))


def _document(document_id: str, text: str) -> SourceDocument:
    return SourceDocument(
        document_id=document_id,
        capture_id=f"capture-{document_id}",
        source_id="bablos79",
        author="bablos79",
        timestamp_utc=datetime(2026, 5, 9, tzinfo=UTC),
        text=text,
        evidence_url=f"https://t.me/bablos79/{document_id}",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )
