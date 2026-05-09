from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.assets import seed_asset_registry
from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_data.metrics import HorizonMetric, HorizonStatus
from signal_sandbox.market_ideas import (
    IdeaOutcomeStatus,
    MarketIdeaDraftExtractor,
    MarketIdeaOutcome,
    aggregate_author_metrics,
)


def test_counts_by_type_and_status() -> None:
    extractor = MarketIdeaDraftExtractor()
    drafts = [
        extractor.extract(_document("doc-1", "#BTC bullish upside")),
        extractor.extract(_document("doc-2", "stream starts at 19:00")),
    ]
    outcomes = [_outcome(drafts[0], return_pct=Decimal("2"))]

    metrics = aggregate_author_metrics(
        drafts,
        outcomes,
        asset_registry=seed_asset_registry(),
    )

    assert metrics.counts_by_idea_type["directional_thesis"] == 1
    assert metrics.counts_by_idea_type["non_market"] == 1
    assert metrics.counts_by_asset_type["crypto"] == 1
    assert metrics.counts_by_horizon_status["evaluated"] == 1
    assert metrics.counts_by_review_status["queued_for_review"] == 2


def test_hit_rate_excludes_non_directional() -> None:
    extractor = MarketIdeaDraftExtractor()
    long_draft = extractor.extract(_document("doc-1", "#BTC bullish upside"))
    flat_draft = extractor.extract(_document("doc-2", "#BTC range neutral"))

    metrics = aggregate_author_metrics(
        [long_draft, flat_draft],
        [
            _outcome(long_draft, return_pct=Decimal("2")),
            _outcome(flat_draft, return_pct=Decimal("-2")),
        ],
        asset_registry=seed_asset_registry(),
    )

    assert metrics.directional_evaluable_count == 1
    assert metrics.directional_hit_rate == Decimal("1.000000")


def test_null_content_rate_separate() -> None:
    extractor = MarketIdeaDraftExtractor()
    drafts = [
        extractor.extract(_document("doc-1", "stream starts at 19:00")),
        extractor.extract(_document("doc-2", "#BTC bullish upside")),
    ]

    metrics = aggregate_author_metrics(
        drafts,
        [],
        asset_registry=seed_asset_registry(),
    )

    assert metrics.null_content_count == 1
    assert metrics.null_content_rate == Decimal("0.500000")
    assert metrics.counts_by_idea_type["non_market"] == 1


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


def _outcome(
    draft,
    *,
    return_pct: Decimal,
) -> MarketIdeaOutcome:
    return MarketIdeaOutcome(
        source_document_id=draft.source_document_id,
        market_idea_id=draft.idea_id,
        asset_id="CRYPTO:BTC",
        snapshot_id="snapshot-btc",
        status=IdeaOutcomeStatus.EVALUATED,
        asset_resolution_status="exact",
        horizon_metrics=[
            HorizonMetric(
                horizon="1d",
                status=HorizonStatus.EVALUATED,
                canonical_asset_id="CRYPTO:BTC",
                return_pct=return_pct,
            )
        ],
    )
