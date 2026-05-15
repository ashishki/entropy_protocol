from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal
from io import BytesIO

import polars as pl

from signal_sandbox.assets import seed_asset_registry
from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_data.metrics import HorizonStatus
from signal_sandbox.market_data.store import (
    MarketDataSnapshot,
    MarketDataSnapshotMetadata,
)
from signal_sandbox.market_ideas import (
    IdeaOutcomeStatus,
    MarketIdeaDraftExtractor,
    evaluate_market_idea_outcome,
)


def test_asset_resolution_statuses() -> None:
    extractor = MarketIdeaDraftExtractor()
    registry = seed_asset_registry()

    unresolved = evaluate_market_idea_outcome(
        extractor.extract(_document("doc-1", "#UNKNOWN bullish upside")),
        asset_registry=registry,
        snapshots_by_asset={},
    )
    ambiguous = evaluate_market_idea_outcome(
        extractor.extract(_document("doc-2", "#BTC #ETH bullish upside")),
        asset_registry=registry,
        snapshots_by_asset={},
    )

    assert unresolved.status == IdeaOutcomeStatus.UNRESOLVED_ASSET
    assert unresolved.asset_resolution_status == "unresolved"
    assert ambiguous.status == IdeaOutcomeStatus.AMBIGUOUS_ASSET
    assert ambiguous.asset_resolution_status == "ambiguous"


def test_outcomes_use_horizon_metrics() -> None:
    extractor = MarketIdeaDraftExtractor()
    registry = seed_asset_registry()
    draft = extractor.extract(_document("doc-1", "#BTC bullish upside"))
    snapshot = _snapshot()

    outcome = evaluate_market_idea_outcome(
        draft,
        asset_registry=registry,
        snapshots_by_asset={"CRYPTO:BTC": snapshot},
    )

    first = outcome.horizon_metrics[0]
    assert outcome.status == IdeaOutcomeStatus.EVALUATED
    assert first.status == HorizonStatus.EVALUATED
    assert first.return_pct == Decimal("10.000000")


def test_outcome_provenance_required() -> None:
    extractor = MarketIdeaDraftExtractor()
    registry = seed_asset_registry()
    draft = extractor.extract(_document("doc-1", "#BTC bullish upside"))
    snapshot = _snapshot()

    outcome = evaluate_market_idea_outcome(
        draft,
        asset_registry=registry,
        snapshots_by_asset={"CRYPTO:BTC": snapshot},
    )

    assert outcome.source_document_id == draft.source_document_id
    assert outcome.market_idea_id == draft.idea_id
    assert outcome.asset_id == "CRYPTO:BTC"
    assert outcome.snapshot_id == "snapshot-btc"
    assert outcome.metric_version == "market-idea-outcomes-v1"


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


def _snapshot() -> MarketDataSnapshot:
    data = BytesIO()
    pl.DataFrame(
        [
            {
                "timestamp_utc": "2026-05-09T00:00:00+00:00",
                "open": "100",
                "high": "110",
                "low": "99",
                "close": "100",
            },
            {
                "timestamp_utc": "2026-05-10T00:00:00+00:00",
                "open": "100",
                "high": "112",
                "low": "98",
                "close": "110",
            },
        ]
    ).write_parquet(data, compression="zstd", statistics=False)
    data_bytes = data.getvalue()
    return MarketDataSnapshot(
        metadata=MarketDataSnapshotMetadata(
            snapshot_id="snapshot-btc",
            provider="operator_file",
            canonical_asset_id="CRYPTO:BTC",
            provider_symbol="BTC/USDT",
            timeframe="1d",
            source_range_start_utc=datetime(2026, 5, 9, tzinfo=UTC),
            source_range_end_utc=datetime(2026, 5, 10, tzinfo=UTC),
            captured_at_utc=datetime(2026, 5, 9, tzinfo=UTC),
            data_sha256=hashlib.sha256(data_bytes).hexdigest(),
            license="operator provided",
            provenance="unit test",
        ),
        data_bytes=data_bytes,
    )
