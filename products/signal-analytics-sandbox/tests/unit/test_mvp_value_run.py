from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VALUE_RUN_JSON = PROJECT_ROOT / "docs/pilot/MVP_VALUE_RUN_2026-05-31.json"
VALUE_RUN_MD = PROJECT_ROOT / "docs/pilot/MVP_VALUE_RUN_2026-05-31.md"
CARDS_JSON = PROJECT_ROOT / "docs/pilot/preclient_FREE_DASHBOARD_CARDS.json"
AUTO_EVAL_JSON = PROJECT_ROOT / "docs/pilot/clientready_AUTO_VALIDATION_EVAL.json"
DISCOVERY_GATE_JSON = PROJECT_ROOT / "docs/pilot/clientready_DISCOVERY_GATE.json"


def _value_run() -> dict:
    return json.loads(VALUE_RUN_JSON.read_text(encoding="utf-8"))


def test_mvp_value_run_records_internal_but_not_customer_facing_verdict() -> None:
    artifact = _value_run()
    summary = artifact["summary"]

    assert summary["status"] == "internal_mvp_value_assessment"
    assert summary["internal_value_ready"] is True
    assert summary["customer_facing_value_ready"] is False
    assert summary["paid_mvp_ready"] is False
    assert (
        summary["verdict"]
        == "valuable_as_internal_diligence_mvp_not_customer_facing_mvp"
    )


def test_mvp_value_run_matches_current_source_artifact_counts() -> None:
    artifact = _value_run()
    cards = json.loads(CARDS_JSON.read_text(encoding="utf-8"))["cards"]
    auto_eval = json.loads(AUTO_EVAL_JSON.read_text(encoding="utf-8"))["summary"]
    discovery = json.loads(DISCOVERY_GATE_JSON.read_text(encoding="utf-8"))["summary"]

    text_metrics = artifact["observed_evidence"]["v1_text_metrics"]
    assert text_metrics["evaluable_claims"] == sum(
        card["measurable_claims"]["v1_evaluable_claims"] for card in cards
    )
    assert text_metrics["confirmed_hits"] == sum(
        card["measurable_claims"]["confirmed_hits"] for card in cards
    )
    assert text_metrics["contradicted_misses"] == sum(
        card["measurable_claims"]["contradicted_misses"] for card in cards
    )

    media = artifact["observed_evidence"]["media_validation"]
    assert media["candidate_count"] == auto_eval["candidate_count"]
    assert media["auto_accepted"] == auto_eval["decision_counts"]["auto_accepted"]
    assert media["auto_rejected"] == auto_eval["decision_counts"]["auto_rejected"]
    assert media["needs_human"] == auto_eval["decision_counts"]["needs_human"]
    assert media["customer_facing_rows"] == auto_eval["customer_facing_rows"]
    assert (
        artifact["observed_evidence"]["gates"]["ready_for_discovery"]
        is (discovery["ready_for_discovery"])
    )


def test_mvp_value_run_keeps_next_experiments_bounded_and_safe() -> None:
    artifact = _value_run()
    report = VALUE_RUN_MD.read_text(encoding="utf-8")

    assert artifact["go_no_go"]["continue_building"] is True
    assert artifact["go_no_go"]["start_paid_customer_facing_metrics"] is False
    assert artifact["go_no_go"]["start_public_dashboard"] is False
    assert len(artifact["next_experiments"]) == 3
    assert "Do not launch a public dashboard." in report
    assert "Do not sell paid performance metrics." in report
    assert "concierge source-diligence validation" in report
