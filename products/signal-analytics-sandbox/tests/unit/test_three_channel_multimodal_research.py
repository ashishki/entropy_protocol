from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = PROJECT_ROOT / "docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json"
QUEUE_PATH = PROJECT_ROOT / "docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json"
RR_PATH = PROJECT_ROOT / "docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json"
REPORT_PATH = PROJECT_ROOT / "docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md"
GITIGNORE_PATH = PROJECT_ROOT / ".gitignore"


def test_multimodal_media_manifest_covers_three_channels() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    summaries = {
        row["source_id"]: row for row in manifest["summary"]["channel_summaries"]
    }

    assert manifest["summary"]["totals"]["posts"] == 570
    assert manifest["summary"]["totals"]["text_rows"] == 527
    assert manifest["summary"]["totals"]["media_rows"] == 295
    assert manifest["summary"]["totals"]["draft_transcript_or_ocr_rows"] == 255
    assert set(summaries) == {"bablos79", "nemphiscrypts", "pifagortrade"}
    assert summaries["bablos79"]["media_by_modality"] == {
        "voice": 68,
        "image": 94,
        "video": 34,
    }
    assert summaries["nemphiscrypts"]["media_by_modality"] == {"image": 63}
    assert summaries["pifagortrade"]["media_by_modality"] == {
        "video": 6,
        "image": 28,
        "voice": 2,
    }


def test_processing_queue_records_media_extraction_and_video_blockers() -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))["processing_queue"]
    statuses = Counter(row["status"] for row in queue)
    draft_modalities = Counter(
        row["modality"] for row in queue if row["status"] == "draft_pending_review"
    )

    assert statuses == {
        "draft_pending_review": 255,
        "blocked_video_manual_review_required": 40,
    }
    assert draft_modalities == {"image": 185, "voice": 70}
    assert all(
        row["extracted_text"]
        for row in queue
        if row["status"] == "draft_pending_review"
    )


def test_rr_drafts_separate_internal_rr_from_customer_gate() -> None:
    rr = json.loads(RR_PATH.read_text(encoding="utf-8"))
    ready = [
        row for row in rr["rr_drafts"] if row["rr_status"] == "rr_ready_internal_draft"
    ]

    assert rr["summary"]["totals"]["rr_drafts"] == 549
    assert rr["summary"]["totals"]["rr_ready"] == 1
    assert len(ready) == 1
    assert ready[0]["source_id"] == "bablos79"
    assert ready[0]["post_id"] == 10450
    assert ready[0]["asset_candidates"][0]["asset"] == "MAGN"
    assert ready[0]["direction"] == "short"
    assert ready[0]["entry"] == "28400.000000"
    assert ready[0]["stop"] == "28600.000000"
    assert ready[0]["targets"] == ["26364.000000"]
    assert ready[0]["computed_rr"] == "10.180000"
    assert ready[0]["customer_metric_status"] == "blocked_media_review_required"


def test_report_and_ignore_policy_document_internal_boundary() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    gitignore = GITIGNORE_PATH.read_text(encoding="utf-8")

    assert "Three-Channel Multimodal Research Report" in report
    assert "draft_pending_review" in report
    assert "internal_research_only" in report
    assert "workspace/media/three_channel_multimodal/" in gitignore
    assert "docs/pilot/multimodal/" in gitignore
