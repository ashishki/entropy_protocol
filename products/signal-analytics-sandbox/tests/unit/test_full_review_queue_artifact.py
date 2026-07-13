from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_FIXTURE = (
    PROJECT_ROOT / "tests/fixtures/review/synthetic_full_review_queue.json"
)
BOUNDARY_DOC = PROJECT_ROOT / "docs/CI_EVIDENCE_BOUNDARY.md"


def _queue() -> dict[str, Any]:
    return json.loads(CONTRACT_FIXTURE.read_text(encoding="utf-8"))


def test_synthetic_queue_contract_is_internally_consistent_and_blocked() -> None:
    queue = _queue()
    summary = queue["summary"]
    decision_counts = Counter(row["current_decision"] for row in queue["rows"])

    assert queue["status"] == "synthetic_contract_fixture_external_blocked"
    assert summary["evidence_class"] == "synthetic_ci_contract"
    assert summary["pilot_or_user_evidence"] is False
    assert summary["external_delivery_approved"] is False
    assert summary["queue_rows_total"] == len(queue["rows"])
    assert summary["current_decision_counts"] == dict(decision_counts)
    assert summary["pending_false_negative_rows"] == sum(
        row["current_decision"] == "excluded_pending_false_negative"
        for row in queue["rows"]
    )
    assert summary["provider_gap_rows"] == sum(
        row["provider"] is None for row in queue["rows"]
    )


def test_synthetic_queue_rows_have_required_review_fields() -> None:
    queue = _queue()
    required_fields = set(queue["required_row_fields"])

    for row in queue["rows"]:
        missing = [field for field in required_fields if row.get(field) in (None, "")]
        assert missing == [], f"{row['queue_id']} missing {missing}"
        assert row["external_delivery_eligible"] is False


def test_synthetic_queue_keeps_evidence_boundary_explicit() -> None:
    queue = _queue()
    boundary = " ".join(BOUNDARY_DOC.read_text(encoding="utf-8").split())
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")

    decisions = queue["summary"]["current_decision_counts"]
    assert decisions == {
        "excluded_pending_false_negative": 1,
        "included_primary_horizon_pending": 1,
        "media_blocked": 1,
    }
    assert "not pilot or user evidence" in boundary
    assert "does not validate historical full-corpus counts" in boundary
    assert "external delivery remains blocked" in boundary
    assert "docs/pilot/*FULL_REVIEW_QUEUE.*" in gitignore
