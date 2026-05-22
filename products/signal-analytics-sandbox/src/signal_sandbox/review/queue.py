"""Review queue import and decision export helpers."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from signal_sandbox.review.decisions import ReviewDecision


class ReviewQueueRow(BaseModel):
    model_config = ConfigDict(strict=True)

    queue_id: str = Field(min_length=1)
    row_kind: str = Field(min_length=1)
    channel: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    source_post_id: int | str
    source_timestamp_utc: str = Field(min_length=1)
    evidence_snippet: str = Field(min_length=1)
    suggested_claim_type: str = Field(min_length=1)
    current_decision: str = Field(min_length=1)
    required_reviewer_action: str = Field(min_length=1)
    blocker_reason: str = Field(min_length=1)
    assets: list[str] = Field(default_factory=list)
    claim_id: str | None = None
    provider: str | None = None
    provider_symbol: str | None = None
    review_reference: dict[str, Any] | None = None
    source_artifact: str = Field(min_length=1)
    queue_tags: list[str] = Field(default_factory=list)
    external_delivery_eligible: bool


class ReviewQueueArtifact(BaseModel):
    model_config = ConfigDict(strict=True)

    artifact_id: str = Field(min_length=1)
    generated_at_utc: str = Field(min_length=1)
    status: str = Field(min_length=1)
    source_artifacts: list[str] = Field(min_length=1)
    required_row_fields: list[str] = Field(min_length=1)
    summary: dict[str, Any]
    rows: list[ReviewQueueRow]

    @model_validator(mode="after")
    def _required_fields_are_present(self) -> ReviewQueueArtifact:
        for row in self.rows:
            payload = row.model_dump()
            missing = [
                field
                for field in self.required_row_fields
                if payload.get(field) in (None, "")
            ]
            if missing:
                raise ValueError(f"{row.queue_id} missing required fields: {missing}")
        return self


def load_review_queue(path: str | Path) -> ReviewQueueArtifact:
    return ReviewQueueArtifact.model_validate_json(
        Path(path).read_text(encoding="utf-8")
    )


def export_review_decisions_json(decisions: Iterable[ReviewDecision]) -> str:
    ordered = _ordered_decisions(decisions)
    payload = {
        "artifact_id": "review_decisions_export",
        "decision_count": len(ordered),
        "decisions": [decision.model_dump(mode="json") for decision in ordered],
    }
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def export_review_decisions_markdown(decisions: Iterable[ReviewDecision]) -> str:
    ordered = _ordered_decisions(decisions)
    rows = [
        (
            f"| `{decision.decision_id}` | `{decision.status.value}` | "
            f"`{decision.claim_id}` | {decision.source_url} | "
            f"`{decision.evidence_span.source_document_id}` | "
            f"{_escape(decision.evidence_span.excerpt)} | "
            f"{_escape(decision.reason)} |"
        )
        for decision in ordered
    ]
    table_rows = "\n".join(rows) if rows else "| none | - | - | - | - | - | - |"
    return "\n".join(
        [
            "# Review Decisions Export",
            "",
            f"Decision count: {len(ordered)}",
            "",
            (
                "| decision_id | status | claim_id | source_url | "
                "source_document_id | evidence_excerpt | reason |"
            ),
            "|---|---|---|---|---|---|---|",
            table_rows,
            "",
        ]
    )


def _ordered_decisions(decisions: Iterable[ReviewDecision]) -> list[ReviewDecision]:
    return sorted(
        decisions,
        key=lambda decision: (
            decision.reviewed_at_utc.isoformat(),
            decision.decision_id,
        ),
    )


def _escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
