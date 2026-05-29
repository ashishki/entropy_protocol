from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from signal_sandbox.review import (
    ReviewDecision,
    ReviewDecisionStatus,
    ReviewEvidenceSpan,
    ReviewQueueArtifact,
    build_review_decision_id,
    export_review_decisions_json,
    export_review_decisions_markdown,
    load_review_queue,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_review_queue_loader_reads_full_queue_and_validates_required_fields() -> None:
    queue = load_review_queue(
        PROJECT_ROOT / "docs/pilot/three_channel_FULL_REVIEW_QUEUE.json"
    )

    assert queue.artifact_id == "three_channel_full_review_queue"
    assert len(queue.rows) == queue.summary["queue_rows_total"]
    assert queue.required_row_fields == [
        "queue_id",
        "channel",
        "source_url",
        "evidence_snippet",
        "suggested_claim_type",
        "current_decision",
        "required_reviewer_action",
        "blocker_reason",
    ]
    assert all(row.source_url for row in queue.rows)


def test_review_queue_loader_rejects_missing_required_fields() -> None:
    payload = {
        "artifact_id": "bad",
        "generated_at_utc": "2026-05-19T00:00:00Z",
        "status": "bad",
        "source_artifacts": ["source.json"],
        "required_row_fields": ["queue_id", "source_url"],
        "summary": {},
        "rows": [
            {
                "queue_id": "row-1",
                "row_kind": "source_text_row",
                "channel": "test",
                "source_url": "",
                "source_post_id": 1,
                "source_timestamp_utc": "2026-05-19T00:00:00Z",
                "evidence_snippet": "snippet",
                "suggested_claim_type": "directional_thesis",
                "current_decision": "needs_context",
                "required_reviewer_action": "review",
                "blocker_reason": "missing source url",
                "assets": [],
                "source_artifact": "source.json",
                "queue_tags": [],
                "external_delivery_eligible": False,
            }
        ],
    }

    with pytest.raises(ValidationError):
        ReviewQueueArtifact.model_validate(payload)


def test_review_decision_exports_are_stable_and_preserve_evidence() -> None:
    later = _decision("claim-2", status=ReviewDecisionStatus.NEEDS_CONTEXT)
    earlier = _decision(
        "claim-1",
        reviewed_at=datetime(2026, 5, 19, 11, 0, tzinfo=UTC),
    )

    exported_json = export_review_decisions_json([later, earlier])
    exported_markdown = export_review_decisions_markdown([later, earlier])
    payload = json.loads(exported_json)

    assert payload["decision_count"] == 2
    assert [row["claim_id"] for row in payload["decisions"]] == ["claim-1", "claim-2"]
    assert "https://t.me/channel/claim-1" in exported_markdown
    assert "source-doc-claim-1" in exported_markdown
    assert "evidence for claim-1" in exported_markdown
    assert exported_json == export_review_decisions_json([later, earlier])


def _decision(
    claim_id: str,
    *,
    status: ReviewDecisionStatus = ReviewDecisionStatus.ACCEPTED,
    reviewed_at: datetime | None = None,
) -> ReviewDecision:
    timestamp = reviewed_at or datetime(2026, 5, 19, 12, 0, tzinfo=UTC)
    source_url = f"https://t.me/channel/{claim_id}"
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
        evidence_span=ReviewEvidenceSpan(
            source_document_id=f"source-doc-{claim_id}",
            start_char=0,
            end_char=20,
            excerpt=f"evidence for {claim_id}",
        ),
        reviewer=reviewer,
        reviewed_at_utc=timestamp,
        status=status,
        reason=f"review reason for {claim_id}",
        queue_id=f"queue-{claim_id}",
        channel="channel",
    )
