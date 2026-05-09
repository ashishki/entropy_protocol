"""Batch export for review-pending MarketIdea drafts."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.market_ideas.extractor import (
    Direction,
    IdeaType,
    MarketIdeaDraft,
    MarketIdeaDraftExtractor,
)


class MarketIdeaExportRow(BaseModel):
    model_config = ConfigDict(strict=True)

    source_document_id: str = Field(min_length=1)
    idea_id: str = Field(min_length=1)
    idea_type: IdeaType
    parser_status: str = Field(min_length=1)
    draft_approval_state: str = Field(min_length=1)
    final_review_status: str = Field(min_length=1)
    review_queue_reasons: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    candidate_assets: list[str] = Field(default_factory=list)
    suggested_evaluation_horizons: list[str] = Field(default_factory=list)


class MarketIdeaBatchExport(BaseModel):
    model_config = ConfigDict(strict=True)

    rows: list[MarketIdeaExportRow]

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_market_idea_export_markdown(self), encoding="utf-8")


def export_market_idea_drafts(
    documents: list[SourceDocument],
    extractor: MarketIdeaDraftExtractor,
) -> MarketIdeaBatchExport:
    rows = [
        _row_from_draft(document, extractor.extract(document))
        for document in sorted(documents, key=lambda item: item.document_id)
    ]
    return MarketIdeaBatchExport(rows=rows)


def render_market_idea_export_markdown(export: MarketIdeaBatchExport) -> str:
    lines = [
        "# MarketIdea Draft Export - bablos79",
        "",
        (
            "| source_document_id | idea_type | parser_status | final_review_status | "
            "review_queue_reasons | candidate_assets | horizons |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for row in export.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.source_document_id,
                    row.idea_type.value,
                    row.parser_status,
                    row.final_review_status,
                    ", ".join(row.review_queue_reasons) or "none",
                    ", ".join(row.candidate_assets) or "none",
                    ", ".join(row.suggested_evaluation_horizons) or "none",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            (
                "All rows are draft parser output. `final_review_status=pending` "
                "means no row is approved."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _row_from_draft(
    document: SourceDocument,
    draft: MarketIdeaDraft,
) -> MarketIdeaExportRow:
    return MarketIdeaExportRow(
        source_document_id=draft.source_document_id,
        idea_id=draft.idea_id,
        idea_type=draft.idea_type,
        parser_status=_parser_status(draft),
        draft_approval_state=draft.approval_state.value,
        final_review_status="pending",
        review_queue_reasons=_review_queue_reasons(document, draft),
        evidence_refs=[
            f"{span.source_document_id}:{span.start_char}-{span.end_char}"
            for span in draft.evidence_spans
        ],
        candidate_assets=draft.asset_mentions,
        suggested_evaluation_horizons=draft.horizon_hint,
    )


def _parser_status(draft: MarketIdeaDraft) -> str:
    if draft.idea_type == IdeaType.NON_MARKET:
        return "draft_excluded_candidate"
    if draft.ambiguity_flags:
        return "draft_needs_review"
    return "draft_candidate"


def _review_queue_reasons(
    document: SourceDocument,
    draft: MarketIdeaDraft,
) -> list[str]:
    reasons = list(draft.ambiguity_flags)
    if len(draft.asset_mentions) > 1:
        reasons.append("ambiguous_asset")
    if draft.direction in {Direction.UNKNOWN, Direction.MIXED}:
        reasons.append("unsupported_direction")
    if _customer_facing_claim(document.text):
        reasons.append("customer_facing_claim")
    if _high_impact_claim(document.text, draft):
        reasons.append("high_impact_claim")
    return sorted(set(reasons)) or ["review_required"]


def _customer_facing_claim(text: str) -> bool:
    folded = text.casefold()
    return any(term in folded for term in ("profit", "guaranteed", "win rate", "x"))


def _high_impact_claim(text: str, draft: MarketIdeaDraft) -> bool:
    folded = text.casefold()
    return draft.idea_type in {
        IdeaType.TRADE_SETUP,
        IdeaType.DIRECTIONAL_THESIS,
        IdeaType.CATALYST_REACTION,
    } and any(term in folded for term in ("strong", "must", "guaranteed", "profit"))
