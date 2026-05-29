from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_impact_framework_defines_truth_layers() -> None:
    framework = (PROJECT_ROOT / "docs/specs/CHANNEL_IMPACT_FRAMEWORK.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Author statement",
        "Interpretation",
        "Market outcome",
        "Product conclusion",
        "LLM/OCR/transcript output is draft until",
    ):
        assert required in framework


def test_impact_framework_lists_non_pnl_dimensions() -> None:
    framework = (PROJECT_ROOT / "docs/specs/CHANNEL_IMPACT_FRAMEWORK.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Trend Sense",
        "Insight Depth",
        "Trading Methodology",
        "Risk Management",
        "Practical Usefulness",
        "Creativity / Differentiation",
        "Evidence Confidence",
    ):
        assert required in framework


def test_impact_framework_defines_dashboard_and_paid_report_boundary() -> None:
    framework = (PROJECT_ROOT / "docs/specs/CHANNEL_IMPACT_FRAMEWORK.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Dashboard Score Shape",
        "Paid Deep Report Boundary",
        "Do not combine dimensions into a single leaderboard score",
        "Never produce investment advice or future-profit language",
    ):
        assert required in framework


def test_cross_channel_loop_covers_three_channels() -> None:
    loop = (
        PROJECT_ROOT / "docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md"
    ).read_text(encoding="utf-8")

    for required in (
        "bablos79",
        "nemphiscrypts",
        "pifagortrade",
        "Source Coverage",
        "Impact Scoring",
        "Cross-Channel Comparison",
    ):
        assert required in loop


def test_cross_channel_loop_separates_dashboard_and_paid_report() -> None:
    loop = (
        PROJECT_ROOT / "docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md"
    ).read_text(encoding="utf-8")

    for required in (
        "Dashboard:",
        "Paid deep report:",
        "compact dimension scores",
        "paid-report evidence appendix",
    ):
        assert required in loop
