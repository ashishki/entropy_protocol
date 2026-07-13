from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from signal_sandbox.review import (
    ReviewDecision,
    ReviewDecisionStatus,
    ReviewEvidenceSpan,
    build_review_audit,
    build_review_decision_id,
    load_review_queue,
    render_review_audit_markdown,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_FIXTURE = (
    PROJECT_ROOT / "tests/fixtures/review/synthetic_full_review_queue.json"
)


def test_review_audit_artifact_lists_missing_review_blockers() -> None:
    audit = (PROJECT_ROOT / "docs/pilot/three_channel_REVIEW_AUDIT.md").read_text(
        encoding="utf-8"
    )

    assert "Status: external_gate_blocked" in audit
    assert "| Queue rows | 1710 |" in audit
    assert "| Review decisions | 0 |" in audit
    assert "| Missing review decisions | 1710 |" in audit
    assert "`excluded_provider_gap`" in audit
    assert "`included_v1_evaluable`" in audit


def test_review_audit_blocks_external_gate_when_coverage_is_incomplete() -> None:
    queue = load_review_queue(CONTRACT_FIXTURE)
    audit = build_review_audit(queue, [])

    assert audit.external_gate_blocked is True
    assert audit.missing_review_count == len(queue.rows)
    assert audit.accepted_missing_required_evidence_count == 0


def test_review_audit_tracks_accepted_decision_required_evidence() -> None:
    queue = load_review_queue(CONTRACT_FIXTURE)
    decision = _decision(queue.rows[0].queue_id)
    audit = build_review_audit(queue, [decision])
    markdown = render_review_audit_markdown(queue, audit)

    assert audit.accepted_decision_count == 1
    assert audit.accepted_missing_required_evidence_count == 0
    assert audit.missing_review_count == len(queue.rows) - 1
    assert "No accepted customer-facing claim may lack reviewer" in markdown


def _decision(queue_id: str) -> ReviewDecision:
    timestamp = datetime(2026, 5, 19, 12, 0, tzinfo=UTC)
    status = ReviewDecisionStatus.ACCEPTED
    claim_id = "claim-audit-1"
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
        evidence_span=ReviewEvidenceSpan(
            source_document_id="source-doc-1",
            start_char=0,
            end_char=8,
            excerpt="evidence",
        ),
        reviewer=reviewer,
        reviewed_at_utc=timestamp,
        status=status,
        reason="accepted with source evidence",
        queue_id=queue_id,
        channel="channel",
    )
