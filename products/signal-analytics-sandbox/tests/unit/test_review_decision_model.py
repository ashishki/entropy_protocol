from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from signal_sandbox.review import (
    ReviewDecision,
    ReviewDecisionStatus,
    ReviewEvidenceSpan,
    build_review_decision_id,
)


def test_review_decision_schema_records_required_operator_fields() -> None:
    decision = _decision()

    assert decision.claim_id == "claim-btc-1"
    assert decision.reviewer == "operator-alpha"
    assert decision.status == ReviewDecisionStatus.ACCEPTED
    assert decision.source_url == "https://t.me/channel/1"
    assert decision.evidence_span.excerpt == "BTC long thesis"
    assert decision.reason == "Evidence supports the extracted BTC long thesis."


def test_review_decision_statuses_cover_phase_29_workflow() -> None:
    assert {status.value for status in ReviewDecisionStatus} == {
        "accepted",
        "false_positive",
        "false_negative",
        "needs_context",
        "unsupported_provider",
        "media_blocked",
    }


def test_review_decision_is_deterministic_and_json_serializable() -> None:
    reviewed_at = datetime(2026, 5, 19, 12, 0, tzinfo=UTC)
    first = _decision(reviewed_at=reviewed_at)
    second = _decision(reviewed_at=reviewed_at)

    assert first.decision_id == second.decision_id
    assert first.canonical_json() == second.canonical_json()
    payload = json.loads(first.canonical_json())
    assert list(payload) == sorted(payload)
    assert payload["status"] == "accepted"
    assert payload["reviewed_at_utc"] == "2026-05-19T12:00:00Z"


def test_review_decision_rejects_empty_reason_and_invalid_span() -> None:
    with pytest.raises(ValidationError):
        _decision(reason="")
    with pytest.raises(ValidationError):
        _decision(
            evidence_span=ReviewEvidenceSpan(
                source_document_id="doc-1",
                start_char=4,
                end_char=4,
                excerpt="bad",
            )
        )


def _decision(
    *,
    reviewed_at: datetime | None = None,
    reason: str = "Evidence supports the extracted BTC long thesis.",
    evidence_span: ReviewEvidenceSpan | None = None,
) -> ReviewDecision:
    timestamp = reviewed_at or datetime(2026, 5, 19, 12, 0, tzinfo=UTC)
    status = ReviewDecisionStatus.ACCEPTED
    claim_id = "claim-btc-1"
    source_url = "https://t.me/channel/1"
    reviewer = "operator-alpha"
    return ReviewDecision(
        decision_id=build_review_decision_id(
            claim_id=claim_id,
            source_url=source_url,
            status=status,
            reviewer=reviewer,
            reviewed_at_utc=timestamp,
        ),
        claim_id=claim_id,
        source_url=source_url,
        evidence_span=evidence_span
        or ReviewEvidenceSpan(
            source_document_id="doc-1",
            start_char=0,
            end_char=15,
            excerpt="BTC long thesis",
        ),
        reviewer=reviewer,
        reviewed_at_utc=timestamp,
        status=status,
        reason=reason,
        queue_id="frq-source-channel-1",
        channel="channel",
    )
