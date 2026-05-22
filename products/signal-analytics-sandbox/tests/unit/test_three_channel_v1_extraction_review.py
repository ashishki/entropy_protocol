from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW_PATH = PROJECT_ROOT / "docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md"
CALIBRATION_PATH = PROJECT_ROOT / "docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md"


def test_v1_extraction_review_has_required_sample_sizes() -> None:
    review = REVIEW_PATH.read_text(encoding="utf-8")

    included_rows = [line for line in review.splitlines() if line.startswith("| inc-")]
    excluded_rows = [line for line in review.splitlines() if line.startswith("| exc-")]

    assert len(included_rows) >= 20
    assert len(excluded_rows) >= 20


def test_v1_extraction_review_uses_allowed_statuses_and_channels() -> None:
    review = REVIEW_PATH.read_text(encoding="utf-8")

    for channel in ("bablos79", "nemphiscrypts", "pifagortrade"):
        assert f"`{channel}`" in review

    for status in ("accepted", "false_positive", "false_negative", "needs_context"):
        assert f"`{status}`" in review


def test_v1_extractor_calibration_lists_required_rule_changes() -> None:
    calibration = CALIBRATION_PATH.read_text(encoding="utf-8")

    for rule in (
        "negation-aware direction parsing",
        "closed/reduced/moved-stop language",
        "conditional level language",
        "BTC/Bitcoin/BTCUSD",
        "Block known non-asset tokens",
        "same sentence or linked neighboring sentence",
        "provider/proxy expansion",
        "internal_only_pending_review",
    ):
        assert rule in calibration
