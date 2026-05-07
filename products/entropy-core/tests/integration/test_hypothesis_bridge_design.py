"""Hypothesis/backtest bridge design contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRIDGE_DOC = PROJECT_ROOT / "docs" / "bridges" / "hypothesis-backtest.md"


def test_hypothesis_bridge_requires_human_registration() -> None:
    text = BRIDGE_DOC.read_text(encoding="utf-8")

    assert "Status: Design only" in text
    assert "human_registration_required" in text
    assert "human sponsor reviewed" in text
    assert "Trial Registry admission is explicit and append-only" in text
    assert "Dataset hash, code hash, policy hash, and parameter-lock hash" in text
    assert "Evaluation execution approval" in text
    assert "Drafts cannot enter the walk-forward harness" in text


def test_hypothesis_bridge_rejects_ai_owned_truth_fields() -> None:
    text = BRIDGE_DOC.read_text(encoding="utf-8")

    for forbidden_truth in (
        "registry_truth",
        "gate_decision",
        "metric_computation",
        "evidence_truth",
        "leakage_status",
        "holdout_status",
        "report_claim_status",
    ):
        assert forbidden_truth in text
    assert "AI output may draft candidate wording only" in text
    assert "It may not write registry records" in text
    assert "ai_registry_write" in text
    assert "ai_gate_decision" in text
    assert "ai_metric_computation" in text
    assert "ai_evidence_generation" in text


def test_hypothesis_bridge_records_required_boundaries() -> None:
    text = BRIDGE_DOC.read_text(encoding="utf-8")

    for boundary in (
        "Holdout boundary",
        "Leakage boundary",
        "No-claim boundary",
        "Runtime escalation boundary",
    ):
        assert boundary in text
    assert "Holdout remains locked by default" in text
    assert "Failed leakage checks block label creation" in text
    assert "not_oos_performance" in text
    assert "not_phase_gate_approval" in text
    assert "not_production" in text
    assert "not_capital_ready" in text
    assert "runtime_escalation_without_adr" in text
