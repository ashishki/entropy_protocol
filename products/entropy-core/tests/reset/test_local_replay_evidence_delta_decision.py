"""Local replay evidence delta decision tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DECISION = PROJECT_ROOT / "docs" / "approvals" / "LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md"


def test_replay_delta_decision_compares_evidence() -> None:
    text = DECISION.read_text(encoding="utf-8")

    assert "Status: LOCAL_REPLAY_EVIDENCE_DELTA_DECISION_NO_APPROVAL" in text
    assert "## Evidence Comparison" in text
    for ref in (
        "docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md",
        "docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md",
        "docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT.md",
        "docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md",
        "src/entropy/simbroker/replay.py",
    ):
        assert f"`{ref}`" in text
        assert (PROJECT_ROOT / ref).is_file()
    assert "plan_only_not_executed" in text
    assert "deterministic_no_effect_replay_recorded" in text
    assert "9b3681de22bf73160baadb022cc4b8af289b144449ca421ffa0f6457910c4c7e" in text


def test_replay_delta_decision_preserves_unconfirmed_status() -> None:
    text = DECISION.read_text(encoding="utf-8").lower()

    for status in (
        "decision status: local_evidence_strengthened_not_confirmed",
        "product hypothesis confirmation status: not_confirmed",
        "product hypothesis rejection status: not_rejected",
        "local evidence status: strengthened_by_deterministic_no_effect_replay",
        "evidence sufficient for product confirmation: false",
        "evidence sufficient for product rejection: false",
        "evidence sufficient for restricted validation approval: false",
        "evidence sufficient for next local regression: true",
    ):
        assert status in text


def test_replay_delta_decision_keeps_restricted_actions_blocked() -> None:
    text = DECISION.read_text(encoding="utf-8").lower()

    for boundary in (
        "no production readiness claimed: true",
        "no capital-ready status claimed: true",
        "no oos/performance conclusion claimed: true",
        "no holdout evidence claimed: true",
        "no live execution evidence claimed: true",
        "no approval event created: true",
        "no restricted validation executed: true",
        "no external side effect executed: true",
    ):
        assert boundary in text
    for blocked in (
        "next bounded option: replay_evidence_non_approval_regression",
        "next task: t67 replay evidence non-approval regression",
        "next option status: local_test_only",
        "sandbox order emission from code: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "broker/exchange network connection: blocked",
        "production credential loading: blocked",
        "live capital action: blocked",
        "holdout read: blocked",
        "holdout unlock: blocked",
        "oos/performance conclusion: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
    ):
        assert blocked in text
