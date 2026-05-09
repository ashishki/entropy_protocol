from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from signal_sandbox.batch_analyst import (
    AnalystMemoScope,
    CorpusCoverage,
    DeterministicMetricRef,
    InternalAnalystMemo,
    InterpretiveClaim,
    RetrievedEvidence,
    ReviewQueueItem,
    render_internal_analyst_memo,
)


def test_memo_sections() -> None:
    rendered = render_internal_analyst_memo(_memo())

    assert "## Scope" in rendered
    assert "## Corpus Coverage" in rendered
    assert "## Retrieved Evidence" in rendered
    assert "## Deterministic Metrics" in rendered
    assert "## Interpretation" in rendered
    assert "## Limitations" in rendered
    assert "## Review Queue" in rendered


def test_interpretive_claims_are_cited() -> None:
    memo = _memo()

    assert memo.interpretation[0].citations == ["doc-bablos79-001", "metric-hit-rate"]
    with pytest.raises(ValidationError, match="unknown citations"):
        _memo(
            interpretation=[
                InterpretiveClaim(
                    claim_id="claim-uncited",
                    text=(
                        "Momentum commentary appears stronger than the sample "
                        "supports."
                    ),
                    citations=["missing-doc"],
                )
            ]
        )
    with pytest.raises(ValidationError):
        InterpretiveClaim(
            claim_id="claim-empty",
            text="This should not validate without citations.",
            citations=[],
        )


def test_memo_internal_only() -> None:
    rendered = render_internal_analyst_memo(_memo())

    assert "Internal only. Not customer-facing." in rendered
    with pytest.raises(ValidationError, match="internal-only"):
        _memo(internal_only=False)


def _memo(
    *,
    interpretation: list[InterpretiveClaim] | None = None,
    internal_only: bool = True,
) -> InternalAnalystMemo:
    return InternalAnalystMemo(
        title="BABLOS79 Internal Market Memo",
        scope=AnalystMemoScope(
            channel_id="bablos79",
            window_start_utc=datetime(2026, 5, 1, tzinfo=UTC),
            window_end_utc=datetime(2026, 5, 9, tzinfo=UTC),
        ),
        corpus_coverage=CorpusCoverage(
            total_source_documents=60,
            retrieved_document_count=1,
            indexed_document_ids=["doc-bablos79-001"],
        ),
        retrieved_evidence=[
            RetrievedEvidence(
                document_id="doc-bablos79-001",
                snippet="BTC upside thesis with explicit risk caveat.",
                evidence_url="https://t.me/bablos79/1",
                text_sha256="a" * 64,
            )
        ],
        deterministic_metrics=[
            DeterministicMetricRef(
                metric_id="metric-hit-rate",
                label="directional_hit_rate",
                value="0.500000",
                source="AuthorMetrics.directional_hit_rate",
            )
        ],
        interpretation=interpretation
        or [
            InterpretiveClaim(
                claim_id="claim-1",
                text=(
                    "The sample contains a cited BTC thesis, but deterministic "
                    "coverage is still too small for external conclusions."
                ),
                citations=["doc-bablos79-001", "metric-hit-rate"],
            )
        ],
        limitations=[
            "Pilot corpus is limited to the captured public Telegram text sample.",
            "No customer-facing report claim is approved by this memo.",
        ],
        review_queue=[
            ReviewQueueItem(
                item_id="review-1",
                reason="Human review required before using interpretation externally.",
                evidence_refs=["doc-bablos79-001"],
            )
        ],
        internal_only=internal_only,
    )
