from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_quant_metrics_v2_spec_defines_required_formulas() -> None:
    spec = (PROJECT_ROOT / "docs/specs/CHANNEL_QUANT_METRICS_V2.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "precision = accepted_extracted_claims / reviewed_extracted_claims",
        "recall = accepted_extracted_claims / accepted_claims_in_reviewed_corpus",
        "hit_rate_by_type = confirmed_count / (confirmed_count + contradicted_count)",
        "mfe_pct = max(direction_adjusted_path_change_pct)",
        "mae_pct = min(direction_adjusted_path_change_pct)",
        "rr = abs(target_price - entry_price) / abs(entry_price - stop_price)",
        "r_multiple = realized_directional_pnl / initial_risk",
        "benchmark_relative_return_pct = claim_return_pct - benchmark_return_pct",
        "drawdown_t = cumulative_metric_t - running_peak_t",
        "max_drawdown = min(drawdown_t)",
    ):
        assert required in spec


def test_quant_metrics_v2_spec_defines_confidence_and_sample_warnings() -> None:
    spec = (PROJECT_ROOT / "docs/specs/CHANNEL_QUANT_METRICS_V2.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "thin_sample",
        "provisional_sample",
        "small_type_bucket",
        "low_review_coverage",
        "low_provider_coverage",
        "missing_recall_audit",
        "media_unreviewed",
        "benchmark_incomplete",
        "`high`: at least 100 evaluable outcomes",
        "`medium`: at least 30 evaluable outcomes",
        "`low`: fewer than 30 evaluable outcomes",
    ):
        assert required in spec
