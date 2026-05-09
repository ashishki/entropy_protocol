"""Internal analyst memo export with citation validation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AnalystMemoScope(BaseModel):
    model_config = ConfigDict(strict=True)

    channel_id: str = Field(min_length=1)
    window_start_utc: datetime
    window_end_utc: datetime


class CorpusCoverage(BaseModel):
    model_config = ConfigDict(strict=True)

    total_source_documents: int = Field(ge=0)
    retrieved_document_count: int = Field(ge=0)
    indexed_document_ids: list[str] = Field(default_factory=list)


class RetrievedEvidence(BaseModel):
    model_config = ConfigDict(strict=True)

    document_id: str = Field(min_length=1)
    snippet: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)


class DeterministicMetricRef(BaseModel):
    model_config = ConfigDict(strict=True)

    metric_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value: str = Field(min_length=1)
    source: str = Field(min_length=1)


class InterpretiveClaim(BaseModel):
    model_config = ConfigDict(strict=True)

    claim_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    citations: list[str] = Field(min_length=1)


class ReviewQueueItem(BaseModel):
    model_config = ConfigDict(strict=True)

    item_id: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)


class InternalAnalystMemo(BaseModel):
    model_config = ConfigDict(strict=True)

    title: str = Field(min_length=1)
    scope: AnalystMemoScope
    corpus_coverage: CorpusCoverage
    retrieved_evidence: list[RetrievedEvidence]
    deterministic_metrics: list[DeterministicMetricRef]
    interpretation: list[InterpretiveClaim]
    limitations: list[str]
    review_queue: list[ReviewQueueItem]
    internal_only: bool = True

    @model_validator(mode="after")
    def _validate_internal_and_citations(self) -> InternalAnalystMemo:
        if not self.internal_only:
            raise ValueError("analyst memo must remain internal-only")
        valid_citations = {
            evidence.document_id for evidence in self.retrieved_evidence
        } | {metric.metric_id for metric in self.deterministic_metrics}
        for claim in self.interpretation:
            missing = sorted(set(claim.citations) - valid_citations)
            if missing:
                raise ValueError(
                    f"interpretive claim {claim.claim_id} has unknown citations: "
                    + ", ".join(missing)
                )
        return self

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_internal_analyst_memo(self), encoding="utf-8")


def render_internal_analyst_memo(memo: InternalAnalystMemo) -> str:
    lines = [
        f"# {memo.title}",
        "",
        "**Audience:** Internal only. Not customer-facing.",
        "",
        "## Scope",
        "",
        f"- Channel: `{memo.scope.channel_id}`",
        f"- Window start UTC: `{memo.scope.window_start_utc.isoformat()}`",
        f"- Window end UTC: `{memo.scope.window_end_utc.isoformat()}`",
        "",
        "## Corpus Coverage",
        "",
        f"- Total source documents: {memo.corpus_coverage.total_source_documents}",
        f"- Retrieved documents: {memo.corpus_coverage.retrieved_document_count}",
        "- Indexed document IDs: "
        + _join_or_none(memo.corpus_coverage.indexed_document_ids),
        "",
        "## Retrieved Evidence",
        "",
    ]
    lines.extend(_evidence_lines(memo.retrieved_evidence))
    lines.extend(["", "## Deterministic Metrics", ""])
    lines.extend(_metric_lines(memo.deterministic_metrics))
    lines.extend(["", "## Interpretation", ""])
    lines.extend(_claim_lines(memo.interpretation))
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in memo.limitations)
    lines.extend(["", "## Review Queue", ""])
    lines.extend(_review_queue_lines(memo.review_queue))
    return "\n".join(lines) + "\n"


def _evidence_lines(evidence_items: list[RetrievedEvidence]) -> list[str]:
    if not evidence_items:
        return ["- none"]
    return [
        (
            f"- `{item.document_id}`: {item.snippet} "
            f"(evidence: {item.evidence_url}; text_sha256: `{item.text_sha256}`)"
        )
        for item in evidence_items
    ]


def _metric_lines(metrics: list[DeterministicMetricRef]) -> list[str]:
    if not metrics:
        return ["- none"]
    return [
        f"- `{metric.metric_id}`: {metric.label} = {metric.value} ({metric.source})"
        for metric in metrics
    ]


def _claim_lines(claims: list[InterpretiveClaim]) -> list[str]:
    if not claims:
        return ["- none"]
    return [
        f"- `{claim.claim_id}`: {claim.text} [cites: {_join_or_none(claim.citations)}]"
        for claim in claims
    ]


def _review_queue_lines(items: list[ReviewQueueItem]) -> list[str]:
    if not items:
        return ["- none"]
    return [
        (
            f"- `{item.item_id}`: {item.reason} "
            f"(evidence refs: {_join_or_none(item.evidence_refs)})"
        )
        for item in items
    ]


def _join_or_none(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"
