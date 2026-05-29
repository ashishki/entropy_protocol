from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _json(relative_path: str) -> dict[str, Any]:
    return json.loads((PROJECT_ROOT / relative_path).read_text(encoding="utf-8"))


def test_phase36_transcript_acceptance_excludes_unaccepted_media() -> None:
    artifact = _json("docs/pilot/bablos79_PHASE36_TRANSCRIPT_ACCEPTANCE.json")
    summary = artifact["summary"]

    assert summary["transcript_refs_reviewed"] == 2
    assert summary["human_operator_accepted"] == 0
    assert summary["needs_context"] == 2
    assert summary["media_backed_claims_customer_facing_allowed"] == 0
    assert all(
        row["phase36_acceptance_status"] == "needs_context" for row in artifact["rows"]
    )


def test_phase36_ocr_drafts_are_blocked_without_source_linkage() -> None:
    artifact = _json("docs/pilot/bablos79_PHASE36_OCR_DRAFTS.json")
    summary = artifact["summary"]

    assert summary["source_linked_image_artifacts"] == 0
    assert summary["source_linked_chart_artifacts"] == 0
    assert summary["ocr_drafts_created"] == 0
    assert artifact["policy_result"]["ocr_allowed_now"] is False


def test_phase36_claim_ledger_has_no_new_accepted_media_claims() -> None:
    ledger = _json("docs/pilot/bablos79_PHASE36_CLAIM_LEDGER.json")
    summary = ledger["summary"]

    assert summary["accepted_transcript_claims_added"] == 0
    assert summary["accepted_ocr_claims_added"] == 0
    assert summary["deterministic_outcome_ready_rows"] == 0
    assert summary["customer_report_eligible_rows"] == 0
    assert ledger["deterministic_candidates"] == []


def test_phase36_outcomes_and_gate_reject_external_delivery() -> None:
    outcomes = _json("docs/pilot/bablos79_PHASE36_OUTCOMES.json")
    gate = (
        PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_EXTERNAL_READY_GATE.md"
    ).read_text(encoding="utf-8")
    review = (PROJECT_ROOT / "docs/archive/PHASE36_BABLOS79_DEEP_REVIEW.md").read_text(
        encoding="utf-8"
    )

    assert outcomes["summary"]["computed_outcomes"] == 0
    assert outcomes["summary"]["provider_gaps_counted_as_losses"] == 0
    assert outcomes["exclusion_policy"]["provider_gaps_are_losses"] is False
    assert "Decision: `reject_external_delivery`" in gate
    assert "pass_internal_only_reject_external" in review
