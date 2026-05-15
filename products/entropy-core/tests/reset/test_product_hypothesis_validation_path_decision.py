"""Product hypothesis validation path decision tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DECISION = PROJECT_ROOT / "docs" / "approvals" / "PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md"


def test_validation_path_decision_compares_options() -> None:
    text = DECISION.read_text(encoding="utf-8")

    assert "Status: PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION_LOCAL_ONLY" in text
    for ref in (
        "docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md",
        "docs/approvals/PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md",
        "docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md",
        "docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md",
        "docs/audit/LIVE_FEED_READINESS_REVIEW.md",
    ):
        assert f"`{ref}`" in text
        assert (PROJECT_ROOT / ref).is_file()
    for option in (
        "Archive-only reproducibility extension",
        "No-read holdout approval decision packet",
        "Live-feed fixture replay extension",
        "Broker sandbox no-capital replay extension",
        "Holdout/OOS evaluation",
        "Broker/exchange sandbox execution from code",
        "Production/capital validation",
    ):
        assert option in text


def test_validation_path_decision_selects_safe_next_step() -> None:
    text = DECISION.read_text(encoding="utf-8").lower()

    assert "selected path: local_next_validation_plan_packet" in text
    assert "selected path status: approved_for_local_planning_only" in text
    assert "restricted action execution: not_approved" in text
    assert "validation execution: not_started" in text
    for blocked in (
        "holdout read: blocked",
        "holdout unlock: blocked",
        "oos/performance conclusion: blocked",
        "live feed activation: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "production credential loading: blocked",
        "live capital action: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
    ):
        assert blocked in text


def test_validation_path_decision_records_not_confirmed() -> None:
    text = DECISION.read_text(encoding="utf-8").lower()

    for status in (
        "product hypothesis confirmation status: not_confirmed",
        "product hypothesis rejection status: not_rejected",
        "evidence status: sufficient_for_local_planning_only",
        "holdout/oos evidence status: absent",
        "live execution evidence status: absent",
        "capital deployment evidence status: absent",
        "no approval event created: true",
        "no product hypothesis confirmation claimed: true",
        "no restricted validation executed: true",
        "no external side effect executed: true",
    ):
        assert status in text
