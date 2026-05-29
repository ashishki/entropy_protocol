from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUEUE_JSON = PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.json"
QUEUE_MD = PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md"


def _queue() -> dict[str, Any]:
    return json.loads(QUEUE_JSON.read_text(encoding="utf-8"))


def test_phase36_media_linkage_queue_counts_and_gate() -> None:
    queue = _queue()
    summary = queue["summary"]
    rows = queue["rows"]

    assert summary["total_candidates"] == 8
    assert summary["source_linked_audio_candidates"] == 2
    assert summary["ocr_ready_now"] == 0
    assert summary["transcript_external_ready_now"] == 0
    assert summary["customer_facing_media_claims_allowed"] == 0
    assert len(rows) == 8
    assert all(row["customer_facing_allowed"] is False for row in rows)


def test_phase36_media_linkage_queue_routes_audio_only_to_review() -> None:
    rows = _queue()["rows"]
    transcript_ready_rows = [
        row for row in rows if row["transcript_review_ready"] is True
    ]

    assert {row["media_id"] for row in transcript_ready_rows} == {
        "public_voice_bablos79_10476",
        "public_voice_bablos79_10478",
    }
    assert all(row["ocr_ready"] is False for row in rows)
    assert {
        row["capture_id"] for row in rows if row["linkage_status"].startswith("blocked")
    } >= {
        "bablos79-10486",
        "bablos79-10465",
        "unlinked-channel-level:image-screenshot",
        "unlinked-channel-level:chart-screenshot",
        "gap:pre-seed-window",
        "gap:post-seed-window",
    }


def test_phase36_media_linkage_queue_preserves_review_policy() -> None:
    queue = _queue()
    policy_text = " ".join(queue["policy"].values())
    queue_md = QUEUE_MD.read_text(encoding="utf-8")

    for required in (
        "source-document linkage",
        "transcript acceptance",
        "manual-review-only",
        "not wins, losses, weak evidence, or strong evidence",
    ):
        assert required in policy_text

    for required in (
        "SAS-BABLOS-004 Transcript Acceptance Pass",
        "OCR-ready now | 0",
        "Chart interpretation is manual-review-only",
    ):
        assert required in queue_md
