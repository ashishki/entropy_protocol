from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_ideas import (
    ApprovalState,
    IdeaType,
    MarketIdeaDraftExtractor,
)
from signal_sandbox.profiles import ChannelProfileRegistry, import_bablos79_profile


def test_market_idea_categories() -> None:
    extractor = _extractor()
    cases = {
        "long #BTC entry 100 stop 90 target 130": IdeaType.TRADE_SETUP,
        "#BTC bullish upside for the week": IdeaType.DIRECTIONAL_THESIS,
        "market regime is risk-off with volatility rising": IdeaType.MARKET_REGIME,
        "watchlist #ETH wait for signs": IdeaType.WATCHLIST,
        "#BTC ETF news changes flows": IdeaType.CATALYST_REACTION,
        "#BTC risk warning no trade after invalidation": IdeaType.RISK_WARNING,
        "stream starts at 19:00": IdeaType.NON_MARKET,
    }

    for index, (text, idea_type) in enumerate(cases.items(), start=1):
        draft = extractor.extract(_document(f"doc-{index}", text))
        assert draft.idea_type == idea_type


def test_evidence_spans_preserved() -> None:
    text = "#BTC long entry 100 stop 90 target 130 after ETF catalyst 7d"
    draft = _extractor().extract(_document("doc-1", text))

    spans = {span.supports: span for span in draft.evidence_spans}

    assert spans["asset"].excerpt == "#BTC"
    assert spans["direction"].excerpt == "long"
    assert spans["stop_or_invalidation"].excerpt == "stop"
    assert spans["target_or_horizon"].excerpt in {"7d", "target"}
    assert spans["catalyst"].excerpt == "ETF"
    for span in draft.evidence_spans:
        assert text[span.start_char : span.end_char] == span.excerpt


def test_drafts_are_unapproved() -> None:
    draft = _extractor().extract(_document("doc-1", "#BTC bullish upside"))

    assert draft.approval_state != ApprovalState.APPROVED
    assert draft.approval_state == ApprovalState.QUEUED_FOR_REVIEW
    assert draft.review_required is True


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
