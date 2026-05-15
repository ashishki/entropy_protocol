from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_ideas import (
    ApprovalState,
    CoverageStatus,
    IdeaOutcomeStatus,
    MarketIdeaDraft,
    MarketIdeaDraftExtractor,
    MarketIdeaOutcome,
    build_review_coverage_export,
)


def test_export_rows_are_complete_and_deterministically_sorted() -> None:
    extractor = MarketIdeaDraftExtractor()
    later = _document("doc-2", "#ETH bearish downside", minutes=2)
    earlier = _document("doc-1", "#BTC bullish upside", minutes=1)
    draft = _approved(extractor.extract(earlier))
    outcome = _outcome(draft)

    export = build_review_coverage_export(
        [later, earlier],
        drafts=[draft],
        outcomes=[outcome],
    )

    assert [row.source_document_id for row in export.rows] == ["doc-1", "doc-2"]
    ready = export.rows[0]
    missing = export.rows[1]
    assert ready.capture_id == "capture-doc-1"
    assert ready.market_idea_id == draft.idea_id
    assert ready.evidence_refs
    assert ready.deterministic_outcome_status == "evaluated"
    assert ready.missing_fields == []
    assert ready.review_status == CoverageStatus.READY_FOR_CUSTOMER_SAMPLE
    assert ready.reviewer_action == "eligible_for_customer_sample"
    assert missing.review_status == CoverageStatus.NEEDS_EVIDENCE_REVIEW
    assert missing.missing_fields == ["market_idea_draft"]


def test_status_buckets_do_not_mutate_truth_artifacts(tmp_path: Path) -> None:
    extractor = MarketIdeaDraftExtractor()
    evidence_missing = _document("doc-1", "#BTC bullish upside")
    metric_missing = _document("doc-2", "#ETH bearish downside")
    interpretation_missing = _document("doc-3", "stream starts at 19:00")
    ready_doc = _document("doc-4", "#BTC bullish upside")
    draft_without_evidence = extractor.extract(evidence_missing).model_copy(
        update={"evidence_spans": []}
    )
    draft_missing_metric = _approved(extractor.extract(metric_missing))
    draft_needs_interpretation = extractor.extract(interpretation_missing)
    ready_draft = _approved(extractor.extract(ready_doc))

    export = build_review_coverage_export(
        [evidence_missing, metric_missing, interpretation_missing, ready_doc],
        drafts=[
            draft_without_evidence,
            draft_missing_metric,
            draft_needs_interpretation,
            ready_draft,
        ],
        outcomes=[_outcome(ready_draft)],
    )
    export.write_markdown(tmp_path / "docs" / "pilot" / "coverage.md")

    statuses = {row.source_document_id: row.review_status for row in export.rows}
    assert statuses == {
        "doc-1": CoverageStatus.NEEDS_EVIDENCE_REVIEW,
        "doc-2": CoverageStatus.NEEDS_METRIC_SNAPSHOT,
        "doc-3": CoverageStatus.NEEDS_INTERPRETATION_REVIEW,
        "doc-4": CoverageStatus.READY_FOR_CUSTOMER_SAMPLE,
    }
    assert not (tmp_path / "ledgers").exists()
    assert not (tmp_path / "outcomes").exists()
    assert not (tmp_path / "reports").exists()
    assert not (tmp_path / "market_data").exists()


def test_markdown_summary_preserves_internal_review_boundary(tmp_path: Path) -> None:
    extractor = MarketIdeaDraftExtractor()
    document = _document("doc-1", "#BTC bullish upside")
    draft = extractor.extract(document)
    export = build_review_coverage_export([document], drafts=[draft], outcomes=[])

    rendered_path = tmp_path / "coverage.md"
    export.write_markdown(rendered_path)
    rendered = rendered_path.read_text(encoding="utf-8")

    assert "Source documents: 1" in rendered
    assert "reviewer_id" in rendered
    assert "pending" in rendered
    assert "not customer-facing" in rendered
    assert "expected return" not in rendered.casefold()


def _approved(draft: MarketIdeaDraft) -> MarketIdeaDraft:
    return draft.model_copy(
        update={"approval_state": ApprovalState.APPROVED, "review_required": False}
    )


def _outcome(draft: MarketIdeaDraft) -> MarketIdeaOutcome:
    return MarketIdeaOutcome(
        source_document_id=draft.source_document_id,
        market_idea_id=draft.idea_id,
        asset_id="CRYPTO:BTC",
        snapshot_id="snapshot-btc",
        status=IdeaOutcomeStatus.EVALUATED,
        asset_resolution_status="exact",
        horizon_metrics=[],
    )


def _document(document_id: str, text: str, *, minutes: int = 0) -> SourceDocument:
    return SourceDocument(
        document_id=document_id,
        capture_id=f"capture-{document_id}",
        source_id="bablos79",
        author="bablos79",
        timestamp_utc=datetime(2026, 5, 9, tzinfo=UTC) + timedelta(minutes=minutes),
        text=text,
        evidence_url=f"https://t.me/bablos79/{document_id}",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )
