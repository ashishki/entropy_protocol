"""Durable operator review decision schema."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReviewDecisionStatus(StrEnum):
    ACCEPTED = "accepted"
    FALSE_POSITIVE = "false_positive"
    FALSE_NEGATIVE = "false_negative"
    NEEDS_CONTEXT = "needs_context"
    UNSUPPORTED_PROVIDER = "unsupported_provider"
    MEDIA_BLOCKED = "media_blocked"


class ReviewEvidenceSpan(BaseModel):
    model_config = ConfigDict(strict=True)

    source_document_id: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(gt=0)
    excerpt: str = Field(min_length=1)


class ReviewDecision(BaseModel):
    model_config = ConfigDict(strict=True)

    decision_id: str = Field(min_length=1)
    claim_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    evidence_span: ReviewEvidenceSpan
    reviewer: str = Field(min_length=1)
    reviewed_at_utc: datetime
    status: ReviewDecisionStatus
    reason: str = Field(min_length=1)
    queue_id: str | None = None
    channel: str | None = None

    @field_validator("reviewed_at_utc", mode="before")
    @classmethod
    def _coerce_reviewed_at(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("reviewed_at_utc must be datetime or ISO string")

    @field_validator("evidence_span")
    @classmethod
    def _span_bounds_are_ordered(
        cls,
        value: ReviewEvidenceSpan,
    ) -> ReviewEvidenceSpan:
        if value.end_char <= value.start_char:
            raise ValueError("evidence_span end_char must be greater than start_char")
        return value

    def canonical_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def build_review_decision_id(
    *,
    claim_id: str,
    source_url: str,
    status: ReviewDecisionStatus,
    reviewer: str,
    reviewed_at_utc: datetime,
) -> str:
    payload = "|".join(
        [
            claim_id,
            source_url,
            status.value,
            reviewer,
            reviewed_at_utc.isoformat(),
        ]
    )
    return f"review-{hashlib.sha256(payload.encode()).hexdigest()[:16]}"
