"""Author Market Report V0 renderer."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.reports.disclaimers import CANONICAL_DISCLAIMER


class AuthorMarketReportError(Exception):
    """Base exception for Author Market Report rendering failures."""


class MissingReportProvenance(AuthorMarketReportError):
    """Raised when source-document or market-snapshot provenance is missing."""


class OutcomeCategory(StrEnum):
    TRADE_SETUP = "trade_setup"
    COMMENTARY = "commentary"


class SourceDocumentProvenance(BaseModel):
    model_config = ConfigDict(strict=True)

    document_id: str
    evidence_url: str
    text_sha256: str
    source_timestamp_utc: datetime


class MarketSnapshotProvenance(BaseModel):
    model_config = ConfigDict(strict=True)

    snapshot_id: str
    provider: str
    data_sha256: str
    captured_at_utc: datetime


class IdeaTaxonomyRow(BaseModel):
    model_config = ConfigDict(strict=True)

    idea_type: str = Field(min_length=1)
    count: int = Field(ge=0)


class OutcomeMetricRow(BaseModel):
    model_config = ConfigDict(strict=True)

    metric_id: str = Field(min_length=1)
    category: OutcomeCategory
    label: str = Field(min_length=1)
    value: str = Field(min_length=1)


class EvidenceExample(BaseModel):
    model_config = ConfigDict(strict=True)

    document_id: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    metric_ids: list[str] = Field(default_factory=list)


class AuthorMarketReport(BaseModel):
    model_config = ConfigDict(strict=True)

    channel_id: str = Field(min_length=1)
    profile_version: str = Field(min_length=1)
    source_documents: list[SourceDocumentProvenance]
    market_snapshots: list[MarketSnapshotProvenance]
    idea_taxonomy: list[IdeaTaxonomyRow]
    outcome_metrics: list[OutcomeMetricRow]
    evidence_examples: list[EvidenceExample]
    limitations: list[str]


def render_author_market_report(report: AuthorMarketReport) -> str:
    _validate_provenance(report)
    lines = [
        f"# Author Market Report: {report.channel_id}",
        "",
        "## Disclaimer",
        "",
        CANONICAL_DISCLAIMER,
        "",
        "## Channel Overview",
        "",
        f"- Channel: `{report.channel_id}`",
        f"- Profile version: `{report.profile_version}`",
        "",
        "## Data Coverage",
        "",
        f"- Source documents: {len(report.source_documents)}",
        f"- Market snapshots: {len(report.market_snapshots)}",
        "",
        "### Source Document Provenance",
        "",
        *_source_document_lines(report.source_documents),
        "",
        "### Market Snapshot Provenance",
        "",
        *_snapshot_lines(report.market_snapshots),
        "",
        "## Idea Taxonomy",
        "",
        *_taxonomy_lines(report.idea_taxonomy),
        "",
        "## Deterministic Outcomes",
        "",
        "### Explicit Trade Setup Performance",
        "",
        *_outcome_lines(report.outcome_metrics, OutcomeCategory.TRADE_SETUP),
        "",
        "### Broader Market Commentary Behavior",
        "",
        *_outcome_lines(report.outcome_metrics, OutcomeCategory.COMMENTARY),
        "",
        "## Evidence Examples",
        "",
        *_evidence_lines(report.evidence_examples),
        "",
        "## Limitations",
        "",
        *_limitation_lines(report.limitations),
        "",
    ]
    return "\n".join(lines)


def _validate_provenance(report: AuthorMarketReport) -> None:
    if not report.source_documents:
        raise MissingReportProvenance("at least one source document is required")
    if not report.market_snapshots:
        raise MissingReportProvenance("at least one market snapshot is required")
    for document in report.source_documents:
        if not document.document_id or not document.evidence_url:
            raise MissingReportProvenance("source document provenance is incomplete")
        if len(document.text_sha256) != 64:
            raise MissingReportProvenance("source document text_sha256 is invalid")
    for snapshot in report.market_snapshots:
        if not snapshot.snapshot_id or not snapshot.provider:
            raise MissingReportProvenance("market snapshot provenance is incomplete")
        if len(snapshot.data_sha256) != 64:
            raise MissingReportProvenance("market snapshot data_sha256 is invalid")


def _source_document_lines(documents: list[SourceDocumentProvenance]) -> list[str]:
    return [
        (
            f"- `{document.document_id}`: {document.source_timestamp_utc.isoformat()} "
            f"(evidence: {document.evidence_url}; text_sha256: "
            f"`{document.text_sha256}`)"
        )
        for document in sorted(documents, key=lambda item: item.document_id)
    ]


def _snapshot_lines(snapshots: list[MarketSnapshotProvenance]) -> list[str]:
    return [
        (
            f"- `{snapshot.snapshot_id}`: {snapshot.provider}, "
            f"captured_at_utc={snapshot.captured_at_utc.isoformat()}, "
            f"data_sha256=`{snapshot.data_sha256}`"
        )
        for snapshot in sorted(snapshots, key=lambda item: item.snapshot_id)
    ]


def _taxonomy_lines(rows: list[IdeaTaxonomyRow]) -> list[str]:
    if not rows:
        return ["- none"]
    return [
        f"- {row.idea_type}: {row.count}"
        for row in sorted(rows, key=lambda item: item.idea_type)
    ]


def _outcome_lines(
    metrics: list[OutcomeMetricRow],
    category: OutcomeCategory,
) -> list[str]:
    scoped = [metric for metric in metrics if metric.category == category]
    if not scoped:
        return ["- none"]
    return [
        f"- `{metric.metric_id}`: {metric.label} = {metric.value}"
        for metric in sorted(scoped, key=lambda item: item.metric_id)
    ]


def _evidence_lines(examples: list[EvidenceExample]) -> list[str]:
    if not examples:
        return ["- none"]
    return [
        (
            f"- `{example.document_id}`: {example.excerpt} "
            f"(metric IDs: {_join_or_none(example.metric_ids)})"
        )
        for example in sorted(examples, key=lambda item: item.document_id)
    ]


def _limitation_lines(limitations: list[str]) -> list[str]:
    if not limitations:
        return ["- none"]
    return [f"- {limitation}" for limitation in limitations]


def _join_or_none(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"
