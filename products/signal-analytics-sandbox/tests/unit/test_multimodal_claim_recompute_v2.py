from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_reviewed_media_claims_have_v2_provenance_schema() -> None:
    artifact = _artifact()
    required_fields = set(artifact["media_claim_inclusion_schema"]["required_fields"])

    assert artifact["method"]["reviewed_media_claims_included"] is True
    assert artifact["media_claim_inclusion_schema"]["required_review_status"] == (
        "human_claim_accepted"
    )
    assert {
        "media_id",
        "source_media_sha256",
        "transcript_ref_or_ocr_ref",
        "transcript_sha256_or_ocr_text_sha256",
        "reviewer_id",
        "accepted_claim_boundary",
        "external_claim_ready",
    }.issubset(required_fields)
    assert artifact["totals"]["reviewed_media_claims_included"] == 0
    assert artifact["reviewed_media_claims"] == []


def test_unreviewed_media_remains_excluded_from_v2_metrics() -> None:
    artifact = _artifact()

    assert artifact["method"]["unreviewed_media_excluded"] is True
    assert artifact["totals"]["v2_evaluable_claims"] == 170
    assert artifact["totals"]["delta_from_v1_evaluable_claims"] == 0
    assert artifact["totals"]["unreviewed_media_claims_excluded"] == 2
    assert artifact["totals"]["blocked_or_unacquired_media_rows"] == 6
    assert len(artifact["excluded_media"]) == 8
    assert all(
        item["review_status"] != "human_claim_accepted"
        for item in artifact["excluded_media"]
    )
    assert {
        summary["source_id"]: summary["reviewed_media_claims_included"]
        for summary in artifact["channel_summaries"]
    } == {"bablos79": 0, "nemphiscrypts": 0, "pifagortrade": 0}


def _artifact() -> dict:
    return json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_V2_METRIC_RESULTS.json").read_text(
            encoding="utf-8"
        )
    )
