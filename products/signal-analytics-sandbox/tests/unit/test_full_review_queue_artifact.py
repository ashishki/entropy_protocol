from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _queue() -> dict[str, Any]:
    return json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_FULL_REVIEW_QUEUE.json").read_text(
            encoding="utf-8"
        )
    )


def test_full_review_queue_covers_v1_claims_text_rows_and_media_blockers() -> None:
    queue = _queue()
    summary = queue["summary"]

    assert queue["status"] == "internal_full_corpus_review_queue_external_blocked"
    assert summary["external_delivery_approved"] is False
    assert summary["queue_rows_total"] == len(queue["rows"])
    assert summary["v1_included_claim_rows"] == 172
    assert summary["v1_evaluable_claims"] == 170
    assert summary["source_text_rows"] == 1534
    assert summary["pending_false_negative_rows"] == 5
    assert summary["media_blocked_rows"] == 4
    assert summary["provider_gap_rows"] >= 200


def test_full_review_queue_rows_have_required_review_fields() -> None:
    queue = _queue()
    required_fields = set(queue["required_row_fields"])

    for row in queue["rows"]:
        missing = [field for field in required_fields if row.get(field) in (None, "")]
        assert missing == [], f"{row['queue_id']} missing {missing}"
        assert row["external_delivery_eligible"] is False


def test_full_review_queue_keeps_blockers_and_gate_boundary_explicit() -> None:
    queue = _queue()
    markdown = (
        PROJECT_ROOT / "docs/pilot/three_channel_FULL_REVIEW_QUEUE.md"
    ).read_text(encoding="utf-8")

    decisions = queue["summary"]["current_decision_counts"]
    assert decisions["excluded_pending_false_negative"] == 5
    assert decisions["media_blocked"] == 4
    assert decisions["included_primary_horizon_pending"] == 2
    assert "External delivery remains blocked" in markdown
    assert "three_channel_V1_EXTERNAL_READY_GATE.md" in markdown
