from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_metric_robustness_appendix_covers_horizon_and_provider_sensitivity() -> None:
    appendix = (
        PROJECT_ROOT / "docs/pilot/three_channel_V2_ROBUSTNESS_APPENDIX.md"
    ).read_text(encoding="utf-8")

    for required in (
        "## Horizon Sensitivity",
        "`1d`",
        "`3d`",
        "`7d`",
        "`14d`",
        "horizon_not_recomputed",
        "horizon_instability",
        "## Provider Sensitivity",
        "provider_gap_material",
        "single_provider_only",
        "proxy_not_approved",
    ):
        assert required in appendix


def test_metric_robustness_appendix_flags_small_samples_without_overclaiming() -> None:
    appendix = (
        PROJECT_ROOT / "docs/pilot/three_channel_V2_ROBUSTNESS_APPENDIX.md"
    ).read_text(encoding="utf-8")

    for required in (
        "## Sample-Size Sensitivity",
        "thin_sample",
        "provisional_sample",
        "small_type_bucket",
        "Small samples must not be overclaimed",
        "Robustness decision: `not_robust_for_external_delivery`",
        "They cannot support public sales claims",
    ):
        assert required in appendix
