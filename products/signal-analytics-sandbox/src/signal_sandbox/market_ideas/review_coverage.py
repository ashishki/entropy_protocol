"""Reviewer coverage export for MarketIdea report readiness."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_ideas.extractor import ApprovalState, MarketIdeaDraft
from signal_sandbox.market_ideas.outcomes import IdeaOutcomeStatus, MarketIdeaOutcome


class CoverageStatus(StrEnum):
    NEEDS_EVIDENCE_REVIEW = "needs_evidence_review"
    NEEDS_METRIC_SNAPSHOT = "needs_metric_snapshot"
    NEEDS_INTERPRETATION_REVIEW = "needs_interpretation_review"
    READY_FOR_CUSTOMER_SAMPLE = "ready_for_customer_sample"


class ReviewCoverageRow(BaseModel):
    model_config = ConfigDict(strict=True)

    source_document_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_timestamp_utc: datetime
    market_idea_id: str = Field(min_length=1)
    idea_type: str = Field(min_length=1)
    review_status: CoverageStatus
    draft_review_status: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    deterministic_outcome_status: str = Field(min_length=1)
    missing_fields: list[str] = Field(default_factory=list)
    reviewer_action: str = Field(min_length=1)
    reviewer_id: str = Field(default="pending", min_length=1)


class ReviewCoverageExport(BaseModel):
    model_config = ConfigDict(strict=True)

    rows: list[ReviewCoverageRow]

    def summary_counts(self) -> dict[str, int]:
        counts = {status.value: 0 for status in CoverageStatus}
        for row in self.rows:
            counts[row.review_status.value] += 1
        return counts

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_review_coverage_markdown(self), encoding="utf-8")


def build_review_coverage_export(
    documents: list[SourceDocument],
    *,
    drafts: list[MarketIdeaDraft],
    outcomes: list[MarketIdeaOutcome],
) -> ReviewCoverageExport:
    drafts_by_document = {draft.source_document_id: draft for draft in drafts}
    outcomes_by_idea = {outcome.market_idea_id: outcome for outcome in outcomes}
    rows = [
        _coverage_row(
            document,
            draft=drafts_by_document.get(document.document_id),
            outcomes_by_idea=outcomes_by_idea,
        )
        for document in sorted(
            documents,
            key=lambda item: (
                item.timestamp_utc.isoformat(),
                item.document_id,
                item.capture_id,
            ),
        )
    ]
    return ReviewCoverageExport(rows=rows)


def render_review_coverage_markdown(export: ReviewCoverageExport) -> str:
    counts = export.summary_counts()
    lines = [
        "# Reviewer Coverage Pack - bablos79",
        "",
        "This artifact is internal review support. It is not customer-facing.",
        "",
        "## Summary",
        "",
        f"- Source documents: {len(export.rows)}",
        (
            "- needs_evidence_review: "
            f"{counts[CoverageStatus.NEEDS_EVIDENCE_REVIEW.value]}"
        ),
        (
            "- needs_metric_snapshot: "
            f"{counts[CoverageStatus.NEEDS_METRIC_SNAPSHOT.value]}"
        ),
        (
            "- needs_interpretation_review: "
            f"{counts[CoverageStatus.NEEDS_INTERPRETATION_REVIEW.value]}"
        ),
        (
            "- ready_for_customer_sample: "
            f"{counts[CoverageStatus.READY_FOR_CUSTOMER_SAMPLE.value]}"
        ),
        "",
        "## Rows",
        "",
        (
            "| source_document_id | capture_id | review_status | market_idea_id | "
            "outcome_status | missing_fields | reviewer_action | reviewer_id |"
        ),
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in export.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.source_document_id,
                    row.capture_id,
                    row.review_status.value,
                    row.market_idea_id,
                    row.deterministic_outcome_status,
                    ", ".join(row.missing_fields) or "none",
                    row.reviewer_action,
                    row.reviewer_id,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "No approved ledger rows, reports, market data, or provider calls are "
            "created by this export.",
        ]
    )
    return "\n".join(lines) + "\n"


def _coverage_row(
    document: SourceDocument,
    *,
    draft: MarketIdeaDraft | None,
    outcomes_by_idea: dict[str, MarketIdeaOutcome],
) -> ReviewCoverageRow:
    if draft is None:
        return ReviewCoverageRow(
            source_document_id=document.document_id,
            capture_id=document.capture_id,
            source_timestamp_utc=document.timestamp_utc,
            market_idea_id="missing",
            idea_type="missing",
            review_status=CoverageStatus.NEEDS_EVIDENCE_REVIEW,
            draft_review_status="missing_draft",
            deterministic_outcome_status="missing",
            missing_fields=["market_idea_draft"],
            reviewer_action="create_market_idea_draft",
        )

    evidence_refs = [
        f"{span.source_document_id}:{span.start_char}-{span.end_char}"
        for span in draft.evidence_spans
    ]
    outcome = outcomes_by_idea.get(draft.idea_id)
    missing_fields = _missing_fields(draft, evidence_refs, outcome)
    review_status = _review_status(missing_fields)
    return ReviewCoverageRow(
        source_document_id=document.document_id,
        capture_id=document.capture_id,
        source_timestamp_utc=document.timestamp_utc,
        market_idea_id=draft.idea_id,
        idea_type=draft.idea_type.value,
        review_status=review_status,
        draft_review_status=draft.approval_state.value,
        evidence_refs=evidence_refs,
        deterministic_outcome_status=(
            outcome.status.value if outcome is not None else "missing"
        ),
        missing_fields=missing_fields,
        reviewer_action=_reviewer_action(review_status),
        reviewer_id=(
            "not_required"
            if review_status == CoverageStatus.READY_FOR_CUSTOMER_SAMPLE
            else "pending"
        ),
    )


def _missing_fields(
    draft: MarketIdeaDraft,
    evidence_refs: list[str],
    outcome: MarketIdeaOutcome | None,
) -> list[str]:
    missing: list[str] = []
    if not evidence_refs:
        missing.append("evidence_refs")
    if draft.asset_mentions and outcome is None:
        missing.append("deterministic_outcome")
    if outcome is not None and outcome.status in {
        IdeaOutcomeStatus.NO_SNAPSHOT,
        IdeaOutcomeStatus.UNRESOLVED_ASSET,
        IdeaOutcomeStatus.AMBIGUOUS_ASSET,
    }:
        missing.append("market_snapshot_or_asset_resolution")
    if draft.review_required or draft.approval_state != ApprovalState.APPROVED:
        missing.append("human_review")
    return sorted(set(missing))


def _review_status(missing_fields: list[str]) -> CoverageStatus:
    if any(field in missing_fields for field in ("market_idea_draft", "evidence_refs")):
        return CoverageStatus.NEEDS_EVIDENCE_REVIEW
    if any(
        field in missing_fields
        for field in ("deterministic_outcome", "market_snapshot_or_asset_resolution")
    ):
        return CoverageStatus.NEEDS_METRIC_SNAPSHOT
    if "human_review" in missing_fields:
        return CoverageStatus.NEEDS_INTERPRETATION_REVIEW
    return CoverageStatus.READY_FOR_CUSTOMER_SAMPLE


def _reviewer_action(status: CoverageStatus) -> str:
    if status == CoverageStatus.NEEDS_EVIDENCE_REVIEW:
        return "attach_or_correct_market_idea_evidence"
    if status == CoverageStatus.NEEDS_METRIC_SNAPSHOT:
        return "attach_market_snapshot_or_outcome"
    if status == CoverageStatus.NEEDS_INTERPRETATION_REVIEW:
        return "complete_human_interpretation_review"
    return "eligible_for_customer_sample"
