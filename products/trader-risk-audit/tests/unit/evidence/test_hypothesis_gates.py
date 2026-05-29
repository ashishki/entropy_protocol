from __future__ import annotations

from trader_risk_audit.evidence import (
    HypothesisDashboardSummary,
    evaluate_hypothesis_gate,
)


def test_gate_evaluator_proceed() -> None:
    decision = evaluate_hypothesis_gate(
        _summary(
            qualified_prospects=10,
            valid_exports=5,
            paid_reports=3,
            repeat_commitments=2,
        )
    )

    assert decision.status == "proceed"
    assert "paid, repeat, and referral thresholds met" in decision.reasons[0]
    assert "T93" in decision.next_action


def test_gate_evaluator_needs_more_or_pivot() -> None:
    needs_more = evaluate_hypothesis_gate(
        _summary(
            qualified_prospects=8,
            valid_exports=4,
            paid_reports=1,
            repeat_commitments=0,
        )
    )
    pivot = evaluate_hypothesis_gate(
        _summary(
            qualified_prospects=10,
            valid_exports=7,
            paid_reports=0,
            repeat_commitments=0,
            blocker_tags=(("no_export", 3), ("wants_live_blocking", 2)),
        )
    )

    assert needs_more.status == "needs_more_evidence"
    assert "qualified prospects 8/10" in needs_more.reasons
    assert "paid reports 1/3" in needs_more.reasons
    assert "qualify more market prospects" == needs_more.next_action
    assert pivot.status == "pivot"
    assert "blocking objections dominate" in pivot.reasons[0]
    assert "no paid reports recorded" in pivot.reasons


def _summary(
    *,
    qualified_prospects: int,
    valid_exports: int,
    paid_reports: int,
    repeat_commitments: int,
    referrals: int = 0,
    blocker_tags: tuple[tuple[str, int], ...] = (),
) -> HypothesisDashboardSummary:
    return HypothesisDashboardSummary(
        qualified_prospects=qualified_prospects,
        intake_started=qualified_prospects,
        valid_exports=valid_exports,
        policy_built=valid_exports,
        audit_run=valid_exports,
        preview_generated=valid_exports,
        cta_accepted=paid_reports,
        paid_reports=paid_reports,
        repeat_commitments=repeat_commitments,
        referrals=referrals,
        demo_artifact_events=0,
        objection_tags=(),
        blocker_tags=blocker_tags,
        gate_status="ready_for_decision",
        next_action="prepare review",
    )
