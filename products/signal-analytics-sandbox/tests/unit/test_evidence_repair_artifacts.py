from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_evidence_repair_capture_manifest_expands_public_corpus() -> None:
    manifest = json.loads(
        (
            PROJECT_ROOT / "docs/pilot/bablos79_EVIDENCE_REPAIR_CAPTURE_MANIFEST.json"
        ).read_text(encoding="utf-8")
    )

    summary = manifest["capture_summary"]
    assert manifest["source"]["source_class"] == "telegram_public"
    assert summary["text_rows_in_window"] >= 500
    assert summary["fresh_workspace_text_capture_files_written"] >= 400
    assert summary["total_workspace_text_captures_after_repair"] >= 500
    assert manifest["boundary"]["private_sources_used"] is False
    assert manifest["boundary"]["market_data_fetched"] is False
    assert manifest["boundary"]["outcomes_computed"] is False
    assert manifest["boundary"]["external_claims_created"] is False


def test_evidence_repair_review_queue_blocks_market_fetch_until_approval() -> None:
    queue = json.loads(
        (
            PROJECT_ROOT / "docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.json"
        ).read_text(encoding="utf-8")
    )

    summary = queue["summary"]
    assert summary["candidate_rows"] >= 100
    assert summary["position_disclosure_candidates"] >= 8
    assert summary["market_data_fetch_allowed_now"] == 0
    assert summary["external_eligible_now"] == 0
    assert all(
        candidate["market_data_fetch_allowed_now"] is False
        for candidate in queue["candidates"]
    )
    assert all(
        candidate["external_eligible_now"] is False for candidate in queue["candidates"]
    )
