from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKET_JSON = PROJECT_ROOT / "docs/pilot/preclient_MODEL_REVIEW_PACKET.json"
PACKET_MD = PROJECT_ROOT / "docs/pilot/preclient_MODEL_REVIEW_PACKET.md"


def test_preclient_model_review_packet_includes_model_accepted_rows() -> None:
    packet = json.loads(PACKET_JSON.read_text(encoding="utf-8"))
    summary = packet["summary"]
    rows = packet["review_packet"]
    post_keys = {(row["source_id"], row["post_id"]) for row in rows}

    assert summary["totals"]["unique_packet_rows"] == 9
    assert summary["totals"]["arbiter_accepted_rows"] == 9
    assert summary["totals"]["mass_accepted_rows"] == 1
    assert summary["totals"]["customer_facing_rows"] == 0
    assert summary["by_channel"] == {
        "bablos79": 1,
        "nemphiscrypts": 1,
        "pifagortrade": 7,
    }
    assert ("bablos79", 10450) in post_keys
    assert ("nemphiscrypts", 3958) in post_keys
    assert ("pifagortrade", 3225) in post_keys


def test_preclient_model_review_packet_rows_have_required_review_fields() -> None:
    rows = json.loads(PACKET_JSON.read_text(encoding="utf-8"))["review_packet"]

    for row in rows:
        assert row["source_url"].startswith("https://t.me/")
        assert row["media_ref_id"].startswith("media_")
        assert row["modality"] in {"image", "voice"}
        assert row["selected_evidence_types"]
        assert row["mass_review"]["present"] is True
        assert row["arbiter_review"]["present"] is True
        assert row["setup_fields"]["deterministic_rr_status"] in {
            "rr_ready_internal_draft",
            "rr_blocked",
            None,
        }
        assert row["required_operator_action"] in {
            "operator_review_for_setup_acceptance_and_market_recompute",
            "operator_review_missing_setup_fields",
            "operator_mark_post_factum_or_reject_as_predictive_signal",
            "operator_review_or_reject_candidate",
            "operator_review_for_rr_acceptance",
        }
        assert row["media_extracted_text_excerpt"]


def test_preclient_model_review_packet_blocks_customer_facing_use() -> None:
    packet = json.loads(PACKET_JSON.read_text(encoding="utf-8"))
    report = PACKET_MD.read_text(encoding="utf-8")

    assert "internal_operator_review_packet" in report
    assert "No row is customer-facing." in report
    assert "internal_only_pending_operator_review" in report
    for row in packet["review_packet"]:
        assert row["customer_facing_status"] == "blocked_pending_human_operator_review"
        assert row["reliability_status"] == "model_reviewed"
        assert row["blocked_from_customer_metrics"] is True
        assert "human_operator_review_required" in row["blockers"]
