from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CARDS_JSON = PROJECT_ROOT / "docs/pilot/preclient_FREE_DASHBOARD_CARDS.json"
CARDS_MD = PROJECT_ROOT / "docs/pilot/preclient_FREE_DASHBOARD_CARDS.md"


def test_preclient_dashboard_cards_have_one_card_per_channel() -> None:
    artifact = json.loads(CARDS_JSON.read_text(encoding="utf-8"))
    cards = artifact["cards"]

    assert artifact["summary"]["status"] == "internal_dashboard_card_dataset_draft"
    assert artifact["summary"]["card_count"] == 3
    assert artifact["summary"]["cards_are_customer_facing"] is False
    assert [card["source_id"] for card in cards] == [
        "bablos79",
        "nemphiscrypts",
        "pifagortrade",
    ]


def test_preclient_dashboard_cards_include_required_free_card_fields() -> None:
    cards = json.loads(CARDS_JSON.read_text(encoding="utf-8"))["cards"]
    required_fields = {
        "source_id",
        "source_type",
        "evaluated_window",
        "what_it_is",
        "primary_markets",
        "content_style",
        "measurable_claim_count",
        "measurable_claims",
        "sample_size_label",
        "signal_performance_summary",
        "setup_rr_status",
        "rr_setup_status",
        "media_coverage_summary",
        "media_coverage",
        "strengths",
        "weaknesses",
        "evidence_confidence",
        "gate_status",
        "allowed_audience",
        "blocked_claims",
    }

    for card in cards:
        assert required_fields.issubset(card)
        assert card["what_it_is"]
        assert card["strengths"]
        assert card["weaknesses"]
        assert card["measurable_claims"]["customer_facing_allowed"] is False
        assert card["media_coverage"]["customer_facing_allowed"] is False
        assert card["rr_setup_status"]["dashboard_safe_rr_count"] == 0
        assert card["evidence_confidence"]["score_label"] == "low"
        assert card["gate_status"] == "internal_only_not_dashboard_safe"
        assert card["allowed_audience"] == "internal_dashboard_prototype"
        assert card["blocked_claims"]


def test_preclient_dashboard_cards_keep_expected_metrics_and_media_counts() -> None:
    cards = {
        card["source_id"]: card
        for card in json.loads(CARDS_JSON.read_text(encoding="utf-8"))["cards"]
    }

    assert cards["bablos79"]["measurable_claim_count"] == 14
    assert cards["nemphiscrypts"]["measurable_claim_count"] == 49
    assert cards["pifagortrade"]["measurable_claim_count"] == 107
    assert cards["bablos79"]["media_coverage"]["public_media_refs"] == 196
    assert cards["nemphiscrypts"]["media_coverage"]["public_media_refs"] == 63
    assert cards["pifagortrade"]["media_coverage"]["public_media_refs"] == 36
    assert cards["bablos79"]["rr_setup_status"]["model_reviewed_candidate_count"] == 1
    assert (
        cards["nemphiscrypts"]["rr_setup_status"]["model_reviewed_candidate_count"] == 1
    )
    assert (
        cards["pifagortrade"]["rr_setup_status"]["model_reviewed_candidate_count"] == 7
    )


def test_preclient_dashboard_cards_avoid_forbidden_customer_wording() -> None:
    combined = (
        CARDS_JSON.read_text(encoding="utf-8")
        + "\n"
        + CARDS_MD.read_text(encoding="utf-8")
    ).lower()

    for forbidden in (
        "best channel",
        "guaranteed",
        "future profit",
        "investment advice",
        "follow this author",
        "leaderboard",
        "marketplace",
    ):
        assert forbidden not in combined
