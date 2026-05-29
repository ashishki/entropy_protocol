from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = PROJECT_ROOT / "docs/pilot/three_channel_2M_METRIC_RESULTS.json"
REPORT_PATH = PROJECT_ROOT / "docs/pilot/three_channel_2M_METRIC_REPORT.md"
SUMMARY_PATH = PROJECT_ROOT / "docs/pilot/three_channel_2M_RUN_SUMMARY.md"


def test_two_month_metric_results_record_window_and_totals() -> None:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))

    assert results["method"]["start_date"] == "2026-03-22"
    assert results["method"]["end_date"] == "2026-05-22"
    assert results["totals"]["public_text_rows"] == 526
    assert results["totals"]["normalized_claims"] == 37
    assert results["totals"]["primary_evaluable_claims"] == 28
    assert results["totals"]["confirmed_hits"] == 19
    assert results["totals"]["contradicted_misses"] == 9


def test_two_month_channel_summaries_are_three_channel_and_internal_only() -> None:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    summaries = {row["source_id"]: row for row in results["channel_summaries"]}
    report = REPORT_PATH.read_text(encoding="utf-8")
    summary = SUMMARY_PATH.read_text(encoding="utf-8")

    assert set(summaries) == {"bablos79", "nemphiscrypts", "pifagortrade"}
    assert summaries["bablos79"]["primary_evaluable_claims"] == 17
    assert (
        summaries["nemphiscrypts"]["evaluation_status_counts"]["no_primary_horizon"]
        == 4
    )
    assert summaries["pifagortrade"]["primary_hit_rate"] == "83.333333"
    assert "Date window: `2026-03-22` through `2026-05-22` inclusive." in report
    assert "internal_historical_research_not_external_ready" in summary
    assert "not investment advice" in summary
