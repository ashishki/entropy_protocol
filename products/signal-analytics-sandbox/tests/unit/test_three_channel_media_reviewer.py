from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = PROJECT_ROOT / "docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json"
REPORT_PATH = PROJECT_ROOT / "docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md"
SCRIPT_PATH = PROJECT_ROOT / "scripts/three_channel_media_reviewer.py"


def test_media_review_results_record_models_and_totals() -> None:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    summary = results["summary"]

    assert summary["models"] == {
        "mass_review_model": "gpt-4.1-mini",
        "arbiter_model": "gpt-4.1",
    }
    assert summary["totals"]["mass_review_rows"] == 255
    assert summary["totals"]["arbiter_review_rows"] == 35
    assert summary["totals"]["accepted_internal_candidates"] == 1
    assert summary["totals"]["arbiter_accepted_internal_candidates"] == 9
    assert summary["method"]["customer_facing"] is False
    assert summary["method"]["human_operator_required_for_customer_metrics"] is True


def test_media_review_channel_findings_are_three_channel() -> None:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    summaries = {
        row["source_id"]: row for row in results["summary"]["channel_summaries"]
    }

    assert set(summaries) == {"bablos79", "nemphiscrypts", "pifagortrade"}
    assert summaries["bablos79"]["evidence_types"]["macro_context"] == 58
    assert summaries["nemphiscrypts"]["evidence_types"]["explicit_trade_setup"] == 9
    assert summaries["pifagortrade"]["arbiter_accepted_internal_candidates"] == 7
    assert summaries["pifagortrade"]["avg_usefulness_score"] == "1.833"


def test_media_review_arbiter_examples_include_cross_channel_candidates() -> None:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    accepted = [
        row
        for row in results["arbiter_reviews"]
        if row["decision"] == "accept_internal_claim_candidate"
    ]
    accepted_posts = {(row["source_id"], row["post_id"]) for row in accepted}

    assert ("pifagortrade", 3214) in accepted_posts
    assert ("pifagortrade", 3225) in accepted_posts
    assert ("bablos79", 10450) in accepted_posts
    assert ("nemphiscrypts", 3958) in accepted_posts


def test_media_review_report_and_script_preserve_internal_gate() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    script = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "Mass reviewer: `gpt-4.1-mini`" in report
    assert "Arbiter reviewer: `gpt-4.1`" in report
    assert "internal_research_only" in report
    assert "human_operator_required_for_customer_metrics" in script
