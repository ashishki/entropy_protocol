"""Reset tests for local broker sandbox replay approval event."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APPROVAL_EVENT = (
    PROJECT_ROOT / "docs" / "approvals" / "LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md"
)


def test_local_replay_approval_event_records_operator_scope() -> None:
    text = APPROVAL_EVENT.read_text()

    assert "LOCAL_BROKER_SANDBOX_REPLAY_APPROVED_NO_EFFECT" in text
    assert "explicit_user_message_2026-05-09" in text
    assert "approved scope: local_broker_sandbox_no_capital_replay" in text
    assert "maximum allowed effect: local_no_effect_only" in text


def test_local_replay_approval_event_blocks_restricted_actions() -> None:
    text = APPROVAL_EVENT.read_text()

    for blocked in (
        "sandbox order emission from code: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "broker/exchange network connection: blocked",
        "production credential loading: blocked",
        "live capital action: blocked",
        "holdout read: blocked",
        "OOS/performance conclusion: blocked",
    ):
        assert blocked in text


def test_local_replay_approval_event_preserves_unconfirmed_hypothesis() -> None:
    text = APPROVAL_EVENT.read_text()

    assert "product hypothesis confirmation status before replay: not_confirmed" in text
    assert "product hypothesis rejection status before replay: not_rejected" in text
    assert "permitted evidence delta: local_evidence_strengthened_not_confirmed" in text
    assert "restricted validation execution: not_approved" in text
