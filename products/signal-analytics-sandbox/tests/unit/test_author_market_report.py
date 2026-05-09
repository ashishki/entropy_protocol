from __future__ import annotations

from datetime import UTC, datetime

import pytest

from signal_sandbox.reports import (
    AuthorMarketReport,
    EvidenceExample,
    IdeaTaxonomyRow,
    MarketSnapshotProvenance,
    MissingReportProvenance,
    OutcomeCategory,
    OutcomeMetricRow,
    SourceDocumentProvenance,
    render_author_market_report,
)
from signal_sandbox.reports.disclaimers import CANONICAL_DISCLAIMER


def test_report_sections() -> None:
    rendered = render_author_market_report(_report())

    assert "## Channel Overview" in rendered
    assert "## Data Coverage" in rendered
    assert "## Idea Taxonomy" in rendered
    assert "## Deterministic Outcomes" in rendered
    assert "## Evidence Examples" in rendered
    assert "## Limitations" in rendered
    assert CANONICAL_DISCLAIMER in rendered


def test_missing_provenance_blocks_report() -> None:
    with pytest.raises(MissingReportProvenance, match="source document"):
        render_author_market_report(_report(source_documents=[]))
    with pytest.raises(MissingReportProvenance, match="market snapshot"):
        render_author_market_report(_report(market_snapshots=[]))


def test_trade_and_commentary_metrics_separate() -> None:
    rendered = render_author_market_report(_report())
    trade_section = rendered.split(
        "### Explicit Trade Setup Performance", maxsplit=1
    )[1].split("### Broader Market Commentary Behavior", maxsplit=1)[0]
    commentary_section = rendered.split(
        "### Broader Market Commentary Behavior", maxsplit=1
    )[1].split("## Evidence Examples", maxsplit=1)[0]

    assert "metric-trade-hit-rate" in trade_section
    assert "metric-commentary-coverage" not in trade_section
    assert "metric-commentary-coverage" in commentary_section
    assert "metric-trade-hit-rate" not in commentary_section


def _report(
    *,
    source_documents: list[SourceDocumentProvenance] | None = None,
    market_snapshots: list[MarketSnapshotProvenance] | None = None,
) -> AuthorMarketReport:
    return AuthorMarketReport(
        channel_id="bablos79",
        profile_version="channel-profile-v1",
        source_documents=(
            [_source_document()] if source_documents is None else source_documents
        ),
        market_snapshots=(
            [_market_snapshot()] if market_snapshots is None else market_snapshots
        ),
        idea_taxonomy=[
            IdeaTaxonomyRow(idea_type="trade_setup", count=2),
            IdeaTaxonomyRow(idea_type="market_regime", count=4),
        ],
        outcome_metrics=[
            OutcomeMetricRow(
                metric_id="metric-trade-hit-rate",
                category=OutcomeCategory.TRADE_SETUP,
                label="directional_hit_rate",
                value="0.500000",
            ),
            OutcomeMetricRow(
                metric_id="metric-commentary-coverage",
                category=OutcomeCategory.COMMENTARY,
                label="market_regime_rows",
                value="4",
            ),
        ],
        evidence_examples=[
            EvidenceExample(
                document_id="doc-1",
                excerpt="BTC thesis with an explicit risk caveat.",
                metric_ids=["metric-trade-hit-rate"],
            )
        ],
        limitations=[
            "The report is historical research, not investment advice.",
            "Coverage depends on reviewed public-source corpus rows.",
        ],
    )


def _source_document() -> SourceDocumentProvenance:
    return SourceDocumentProvenance(
        document_id="doc-1",
        evidence_url="https://t.me/bablos79/1",
        text_sha256="a" * 64,
        source_timestamp_utc=datetime(2026, 5, 9, tzinfo=UTC),
    )


def _market_snapshot() -> MarketSnapshotProvenance:
    return MarketSnapshotProvenance(
        snapshot_id="snapshot-btc-1d",
        provider="operator_file",
        data_sha256="b" * 64,
        captured_at_utc=datetime(2026, 5, 9, tzinfo=UTC),
    )
