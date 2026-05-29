from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GATE_JSON = PROJECT_ROOT / "docs/pilot/preclient_ARTIFACT_SAFETY_GATE.json"
GATE_MD = PROJECT_ROOT / "docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md"


def _gate() -> dict:
    return json.loads(GATE_JSON.read_text(encoding="utf-8"))


def test_preclient_artifact_safety_gate_records_global_decision() -> None:
    gate = _gate()
    summary = gate["summary"]
    report = GATE_MD.read_text(encoding="utf-8")

    assert summary["status"] == "internal_artifact_safety_gate"
    assert summary["artifact_count"] == 14
    assert summary["forbidden_findings_total"] == 0
    assert summary["team_may_proceed_to_buyer_conversations"] is False
    assert summary["buyer_conversation_decision"] == "hold_until_phase37_deep_review"
    assert summary["gate_decision"] == "continue_internal_hardening"
    assert summary["dashboard_safe_now"] == []
    assert summary["paid_report_safe_now"] == []
    assert summary["global_blockers"] == [
        "phase37_deep_review_required",
        "external_gate_not_passed",
        "0 operator_accepted_media_claims",
        "0 dashboard_safe_rr_rows",
        "0 market_outcome_recomputed_candidates",
    ]
    assert "Buyer conversations now: `hold_until_phase37_deep_review`" in report
    assert "Dashboard-safe now: none" in report
    assert "Paid-report-safe now: none" in report


def test_preclient_artifact_safety_gate_covers_every_required_artifact() -> None:
    decisions = {
        decision["artifact_ref"]: decision for decision in _gate()["artifact_decisions"]
    }

    assert set(decisions) == {
        "docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md",
        "docs/pilot/preclient_MODEL_REVIEW_PACKET.md",
        "docs/pilot/preclient_MODEL_REVIEW_PACKET.json",
        "docs/pilot/preclient_EVIDENCE_APPENDIX.md",
        "docs/pilot/preclient_EVIDENCE_APPENDIX.json",
        "docs/pilot/preclient_FREE_DASHBOARD_CARDS.md",
        "docs/pilot/preclient_FREE_DASHBOARD_CARDS.json",
        "docs/pilot/preclient_CANDIDATE_OUTCOMES.md",
        "docs/pilot/preclient_CANDIDATE_OUTCOMES.json",
        "docs/pilot/preclient_dashboard/index.html",
        "docs/pilot/reports/preclient/bablos79_DEEP_REPORT_V0.md",
        "docs/pilot/reports/preclient/nemphiscrypts_DEEP_REPORT_V0.md",
        "docs/pilot/reports/preclient/pifagortrade_DEEP_REPORT_V0.md",
        "docs/pilot/reports/preclient/PAID_STYLE_DEMO_REPORT.md",
    }
    assert all(
        decision["showable_in_buyer_conversation_now"] is False
        for decision in decisions.values()
    )
    assert all(
        decision["forbidden_findings_count"] == 0 for decision in decisions.values()
    )


def test_preclient_artifact_safety_gate_marks_only_demo_candidates_for_review() -> None:
    decisions = {
        decision["artifact_ref"]: decision for decision in _gate()["artifact_decisions"]
    }
    candidate_refs = {
        ref
        for ref, decision in decisions.items()
        if decision["showable_after_phase37_deep_review_candidate"]
    }

    assert candidate_refs == {
        "docs/pilot/preclient_FREE_DASHBOARD_CARDS.md",
        "docs/pilot/preclient_FREE_DASHBOARD_CARDS.json",
        "docs/pilot/preclient_dashboard/index.html",
        "docs/pilot/reports/preclient/PAID_STYLE_DEMO_REPORT.md",
    }
    assert (
        decisions["docs/pilot/preclient_EVIDENCE_APPENDIX.md"][
            "showable_after_phase37_deep_review_candidate"
        ]
        is False
    )
    assert (
        decisions["docs/pilot/preclient_MODEL_REVIEW_PACKET.md"][
            "showable_after_phase37_deep_review_candidate"
        ]
        is False
    )
    assert (
        decisions["docs/pilot/preclient_CANDIDATE_OUTCOMES.md"][
            "showable_after_phase37_deep_review_candidate"
        ]
        is False
    )


def test_preclient_artifact_safety_gate_blocks_external_claim_language() -> None:
    gate = _gate()
    policy = gate["safety_scan_policy"]
    buyer_policy = gate["buyer_conversation_policy"]

    assert set(policy["blocked_categories"]) == {
        "advice",
        "future_profit",
        "payment_flow",
        "private_source_promise",
        "unsupported_ranking",
    }
    assert policy["bulk_market_history_storage_required"] is False
    assert buyer_policy["may_start_now"] is False
    assert (
        buyer_policy["required_next_gate"] == "SAS-PRECLIENT-010 Phase 37 Deep Review"
    )
    assert "Keep media/RR and post-factum caveats visible." in buyer_policy["wording"]
