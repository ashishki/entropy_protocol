"""Reset-era no-claim report boundary tests."""

from __future__ import annotations

import pytest

from entropy.baseline.decision import build_phase1j_research_decision, build_phase1k_closure_packet
from entropy.baseline.report import (
    PHASE1I_STAT_FIELD_STATUS,
    build_phase1i_evaluation_report,
    phase1i_evaluation_report_payload,
)
from tests.unit.test_phase1i_j_k_packets import _build_report_inputs


def test_archive_only_reports_have_no_performance_conclusion_status(tmp_path) -> None:
    """Archive-only stat fields serialize an explicit no-conclusion status."""
    preregistration, config, evaluation = _build_report_inputs(tmp_path)

    report = build_phase1i_evaluation_report(config, preregistration, evaluation)
    payload = phase1i_evaluation_report_payload(report)

    assert payload["performance_conclusion"] is False
    assert payload["oos_label"] is False
    assert payload["stat_field_statuses"]
    assert {
        item["status"]
        for item in payload["stat_field_statuses"]  # type: ignore[index]
    } == {PHASE1I_STAT_FIELD_STATUS}


@pytest.mark.parametrize(
    "claim_field",
    ["production_label", "capital_ready_label", "oos_label"],
)
def test_report_builders_reject_claim_labels_without_gate_evidence(
    tmp_path, claim_field: str
) -> None:
    """Downstream report decisions reject claim labels when gates are absent."""
    preregistration, config, evaluation = _build_report_inputs(tmp_path)
    report = build_phase1i_evaluation_report(config, preregistration, evaluation)
    claimed_report = report.__class__(**{**report.__dict__, claim_field: True})

    with pytest.raises(ValueError, match="no-claim report"):
        build_phase1j_research_decision(claimed_report)


def test_dk_baseline_report_remains_no_claim(tmp_path) -> None:
    """Current D-K report, decision, and closure surfaces remain archive-only."""
    preregistration, config, evaluation = _build_report_inputs(tmp_path)

    report = build_phase1i_evaluation_report(config, preregistration, evaluation)
    decision = build_phase1j_research_decision(report)
    closure = build_phase1k_closure_packet(decision)
    payload = phase1i_evaluation_report_payload(report)

    assert payload["no_claim_labels"] == [
        "research_report_packet",
        "not_phase_gate_approval",
        "not_holdout_unlock",
        "not_production",
        "not_capital_ready",
    ]
    assert report.performance_conclusion is False
    assert report.phase_gate_evidence is False
    assert report.production_label is False
    assert report.capital_ready_label is False
    assert report.oos_label is False
    assert decision.holdout_gate_opened is False
    assert decision.production_label is False
    assert decision.capital_ready_label is False
    assert closure.holdout_executed is False
    assert closure.production_label is False
    assert closure.capital_ready_label is False
