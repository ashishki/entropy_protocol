from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_channel_utility_score_v2_separates_metric_dimensions() -> None:
    scorecard = (PROJECT_ROOT / "docs/pilot/three_channel_V2_SCORECARD.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "## Coverage",
        "## Clarity",
        "## Extraction Quality",
        "## Outcome Quality",
        "## Risk Quality",
        "## Limitations",
        "`bablos79`",
        "`nemphiscrypts`",
        "`pifagortrade`",
        "Does not produce a single composite score.",
        "No approved setup-level risk sample yet",
    ):
        assert required in scorecard


def test_channel_utility_score_v2_has_warnings_without_ordering_language() -> None:
    scorecard = (PROJECT_ROOT / "docs/pilot/three_channel_V2_SCORECARD.md").read_text(
        encoding="utf-8"
    )
    normalized = scorecard.lower()

    for required in (
        "## Confidence And Sample Warnings",
        "thin_sample",
        "provisional_sample",
        "small_type_bucket",
        "low_review_coverage",
        "low_provider_coverage",
        "missing_recall_audit",
        "Confidence tier describes evidence strength only.",
    ):
        assert required in scorecard

    for forbidden in (
        "leaderboard",
        "winner",
        "best channel",
        "top channel",
        "ranking",
        "ranked",
    ):
        assert forbidden not in normalized
