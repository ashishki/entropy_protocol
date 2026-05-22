from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_transcript_review_workflow_defines_accept_reject_decision_fields() -> None:
    workflow = (
        PROJECT_ROOT / "docs/pilot/three_channel_TRANSCRIPT_REVIEW.md"
    ).read_text(encoding="utf-8")

    for required in (
        "`decision_status`: one of `accepted`, `rejected`, `needs_context`,",
        "`reviewer_id`",
        "`reason`",
        "`source_media_sha256`",
        "`transcript_sha256`",
        "`accepted` requires a non-`pending` `reviewer_id`",
        "`rejected` requires a non-`pending` `reviewer_id`",
        "`external_claim_ready` remains `false`",
    ):
        assert required in workflow


def test_transcript_review_workflow_queues_current_refs_without_external_use() -> None:
    workflow = (
        PROJECT_ROOT / "docs/pilot/three_channel_TRANSCRIPT_REVIEW.md"
    ).read_text(encoding="utf-8")

    for required in (
        "docs/pilot/transcripts/transcript_57b6461001b54e10.json",
        "docs/pilot/transcripts/transcript_92ad5bf2e9088056.json",
        "pending_human_review",
        "Current human/operator accepted transcript refs: 0.",
        "Current rejected transcript refs: 0.",
        "Current pending transcript refs: 2.",
        "No transcript-backed customer-facing claim is eligible.",
    ):
        assert required in workflow
