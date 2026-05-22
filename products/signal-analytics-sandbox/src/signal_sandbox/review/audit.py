"""Review decision audit helpers."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.review.decisions import ReviewDecision, ReviewDecisionStatus
from signal_sandbox.review.queue import ReviewQueueArtifact, ReviewQueueRow


class ReviewAuditResult(BaseModel):
    model_config = ConfigDict(strict=True)

    queue_rows_total: int = Field(ge=0)
    decision_count: int = Field(ge=0)
    missing_review_count: int = Field(ge=0)
    accepted_decision_count: int = Field(ge=0)
    accepted_missing_required_evidence_count: int = Field(ge=0)
    external_gate_blocked: bool
    missing_review_by_decision: dict[str, int]
    missing_review_examples: list[str]


def build_review_audit(
    queue: ReviewQueueArtifact,
    decisions: Sequence[ReviewDecision],
    *,
    example_limit: int = 20,
) -> ReviewAuditResult:
    decisions_by_queue_id = {
        decision.queue_id for decision in decisions if decision.queue_id is not None
    }
    missing_rows = [
        row for row in queue.rows if row.queue_id not in decisions_by_queue_id
    ]
    accepted = [
        decision
        for decision in decisions
        if decision.status == ReviewDecisionStatus.ACCEPTED
    ]
    accepted_missing_required_evidence = [
        decision
        for decision in accepted
        if not (
            decision.reviewer and decision.source_url and decision.evidence_span.excerpt
        )
    ]
    missing_counts = Counter(row.current_decision for row in missing_rows)
    return ReviewAuditResult(
        queue_rows_total=len(queue.rows),
        decision_count=len(decisions),
        missing_review_count=len(missing_rows),
        accepted_decision_count=len(accepted),
        accepted_missing_required_evidence_count=len(
            accepted_missing_required_evidence
        ),
        external_gate_blocked=bool(missing_rows or accepted_missing_required_evidence),
        missing_review_by_decision=dict(sorted(missing_counts.items())),
        missing_review_examples=[row.queue_id for row in missing_rows[:example_limit]],
    )


def render_review_audit_markdown(
    queue: ReviewQueueArtifact,
    audit: ReviewAuditResult,
) -> str:
    counts = "\n".join(
        f"| `{decision}` | {count} |"
        for decision, count in audit.missing_review_by_decision.items()
    )
    examples = "\n".join(
        f"| `{row.queue_id}` | `{row.channel}` | {row.source_url} | "
        f"`{row.current_decision}` | {row.blocker_reason.replace('|', '/')} |"
        for row in _example_rows(queue, audit.missing_review_examples)
    )
    if not examples:
        examples = "| none | - | - | - | - |"
    return f"""# Three-Channel Review Audit

Date: 2026-05-19
Status: external_gate_blocked

## Summary

Accepted decisions missing required evidence:
`{audit.accepted_missing_required_evidence_count}`.

| Metric | Count |
|---|---:|
| Queue rows | {audit.queue_rows_total} |
| Review decisions | {audit.decision_count} |
| Missing review decisions | {audit.missing_review_count} |
| Accepted decisions | {audit.accepted_decision_count} |

External gate blocked: `{str(audit.external_gate_blocked).lower()}`.

## Missing Review By Current Decision

| Current decision | Missing rows |
|---|---:|
{counts}

## Missing Review Examples

| queue_id | channel | source | current decision | blocker |
|---|---|---|---|---|
{examples}

## Accepted Evidence Rule

No accepted customer-facing claim may lack reviewer, source URL, and evidence
span. Current accepted decisions missing required evidence:
`{audit.accepted_missing_required_evidence_count}`.

## Gate Decision

The external gate remains blocked while missing review decisions are greater
than zero.
"""


def _example_rows(
    queue: ReviewQueueArtifact,
    queue_ids: Sequence[str],
) -> list[ReviewQueueRow]:
    rows_by_id = {row.queue_id: row for row in queue.rows}
    return [rows_by_id[queue_id] for queue_id in queue_ids]
