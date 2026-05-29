from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_three_channel_v1_metric_results_have_required_metric_groups() -> None:
    results = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_V1_METRIC_RESULTS.json").read_text(
            encoding="utf-8"
        )
    )

    assert results["status"] == "internal_v1_recompute"
    assert results["method"]["bulk_market_database_used"] is False
    assert results["method"]["external_delivery_approved"] is False
    for summary in results["channel_summaries"]:
        assert "v1_evaluable_claims" in summary
        assert "primary_hit_rate" in summary
        assert "avg_directional_return_pct" in summary
        assert "avg_mfe_pct" in summary
        assert "avg_mae_pct" in summary
        assert "rr_available_count" in summary
        assert "provider_coverage" in summary
        assert "exclusion_counts" in summary


def test_three_channel_v1_scorecard_separates_quality_dimensions() -> None:
    scorecard = (PROJECT_ROOT / "docs/pilot/three_channel_V1_SCORECARD.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Coverage",
        "Extraction quality",
        "Outcome quality",
        "Risk quality",
        "Evidence limitations",
        "Customer-facing use still requires the V1 external-ready gate",
    ):
        assert required in scorecard
