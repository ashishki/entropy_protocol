"""Unit tests for P1/P3 governance state machines."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from entropy.governance import GovernanceStateMachine, P1StateMachine, P3StateMachine, event_types
from entropy.models.registry import GovernanceEvent

UTC_TS = datetime(2026, 5, 5, 12, 0, tzinfo=timezone.utc)


def test_p1_trips_at_threshold_boundary() -> None:
    below = P1StateMachine(policy_hash="policy")
    below.update(drawdown_pct=0.119, timestamp=UTC_TS)

    at_threshold = P1StateMachine(policy_hash="policy")
    at_threshold.update(drawdown_pct=0.12, timestamp=UTC_TS)

    assert below.is_p1_active is False
    assert below.events == ()
    assert at_threshold.is_p1_active is True
    assert event_types(at_threshold.events) == ("P1_TRIP",)


def test_p1_blocks_new_positions() -> None:
    state_machine = P1StateMachine(policy_hash="policy")

    assert state_machine.can_open_new_position() is True

    state_machine.update(drawdown_pct=0.12, timestamp=UTC_TS)

    assert state_machine.can_open_new_position() is False

    state_machine.update(
        drawdown_pct=0.05,
        gap_from_hwm=0.079,
        business_days_elapsed=5,
        timestamp=UTC_TS,
    )

    assert state_machine.can_open_new_position() is True


def test_p1_reset_requires_both_conditions() -> None:
    gap_only = P1StateMachine(policy_hash="policy")
    gap_only.update(drawdown_pct=0.15, timestamp=UTC_TS)
    gap_only.update(
        drawdown_pct=0.05,
        gap_from_hwm=0.079,
        business_days_elapsed=4,
        timestamp=UTC_TS,
    )

    days_only = P1StateMachine(policy_hash="policy")
    days_only.update(drawdown_pct=0.15, timestamp=UTC_TS)
    days_only.update(
        drawdown_pct=0.05,
        gap_from_hwm=0.08,
        business_days_elapsed=5,
        timestamp=UTC_TS,
    )

    both = P1StateMachine(policy_hash="policy")
    both.update(drawdown_pct=0.15, timestamp=UTC_TS)
    both.update(
        drawdown_pct=0.05,
        gap_from_hwm=0.079,
        business_days_elapsed=5,
        timestamp=UTC_TS,
    )

    assert gap_only.is_p1_active is True
    assert days_only.is_p1_active is True
    assert both.is_p1_active is False
    assert event_types(both.events) == ("P1_TRIP", "P1_RESET")


def test_p1_trip_is_idempotent() -> None:
    state_machine = P1StateMachine(policy_hash="policy")

    state_machine.update(drawdown_pct=0.15, timestamp=UTC_TS)
    state_machine.update(drawdown_pct=0.15, timestamp=UTC_TS)

    assert state_machine.is_p1_active is True
    assert event_types(state_machine.events) == ("P1_TRIP",)


def test_p3_fire_and_clear_with_hysteresis() -> None:
    state_machine = P3StateMachine(policy_hash="policy")

    state_machine.update(rho_avg=0.55, timestamp=UTC_TS)
    assert state_machine.is_p3_active is False

    state_machine.update(rho_avg=0.56, timestamp=UTC_TS)
    assert state_machine.is_p3_active is True
    assert state_machine.gross_reduction == pytest.approx(0.35)

    state_machine.update(rho_avg=0.44, business_days_elapsed=2, timestamp=UTC_TS)
    assert state_machine.is_p3_active is True

    state_machine.update(rho_avg=0.44, business_days_elapsed=3, timestamp=UTC_TS)
    assert state_machine.is_p3_active is False
    assert event_types(state_machine.events) == ("P3_FIRE", "P3_CLEAR")


def test_p3_correlation_trigger_suite() -> None:
    low_reduction = P3StateMachine(policy_hash="policy")
    high_reduction = P3StateMachine(policy_hash="policy")
    p1_blocked = P3StateMachine(policy_hash="policy")

    low_reduction.update(rho_avg=0.65, timestamp=UTC_TS)
    high_reduction.update(rho_avg=0.66, timestamp=UTC_TS)

    assert low_reduction.is_p3_active is True
    assert low_reduction.gross_reduction == pytest.approx(0.35)
    assert high_reduction.is_p3_active is True
    assert high_reduction.gross_reduction == pytest.approx(0.50)

    low_reduction.update(rho_avg=0.60, business_days_elapsed=1, timestamp=UTC_TS)
    assert low_reduction.p3_ramp_progress == pytest.approx(1 / 3)

    low_reduction.update(rho_avg=0.60, p1_active=True, business_days_elapsed=1, timestamp=UTC_TS)
    assert low_reduction.p3_ramp_progress == pytest.approx(1 / 3)
    assert low_reduction.ramp_paused is True

    p1_blocked.update(rho_avg=0.56, p1_active=True, timestamp=UTC_TS)
    assert p1_blocked.is_p3_active is True
    assert p1_blocked.p3_ramp_progress == pytest.approx(0.0)
    assert p1_blocked.ramp_paused is True


def test_p1_p3_concurrent() -> None:
    state_machine = GovernanceStateMachine(policy_hash="policy")

    state_machine.update(drawdown_pct=0.02, rho_avg=0.56, timestamp=UTC_TS)
    state_machine.update(
        drawdown_pct=0.02,
        rho_avg=0.60,
        business_days_elapsed=1,
        timestamp=UTC_TS,
    )
    frozen_progress = state_machine.p3.p3_ramp_progress

    state_machine.update(
        drawdown_pct=0.12,
        rho_avg=0.60,
        business_days_elapsed=1,
        timestamp=UTC_TS,
    )

    assert state_machine.p1.is_p1_active is True
    assert state_machine.can_open_new_position() is False
    assert state_machine.p3.is_p3_active is True
    assert state_machine.p3.p3_ramp_progress == pytest.approx(frozen_progress)
    assert state_machine.p3.ramp_paused is True

    state_machine.update(
        drawdown_pct=0.05,
        rho_avg=0.60,
        gap_from_hwm=0.079,
        business_days_elapsed=5,
        timestamp=UTC_TS,
    )

    assert state_machine.p1.is_p1_active is False
    assert state_machine.p3.p3_ramp_progress == pytest.approx(frozen_progress)
    assert state_machine.p3.ramp_paused is False

    state_machine.update(
        drawdown_pct=0.05,
        rho_avg=0.60,
        business_days_elapsed=1,
        timestamp=UTC_TS,
    )

    assert state_machine.p3.p3_ramp_progress > frozen_progress


def test_p1_circuit_breaker_suite() -> None:
    emitted_events: list[GovernanceEvent] = []
    p1 = P1StateMachine(policy_hash="policy", event_sink=emitted_events.append)
    p3 = P3StateMachine(policy_hash="policy", event_sink=emitted_events.append)

    p1.update(drawdown_pct=0.12, timestamp=UTC_TS)
    p1.update(drawdown_pct=0.12, timestamp=UTC_TS)
    p1.update(
        drawdown_pct=0.05,
        gap_from_hwm=0.079,
        business_days_elapsed=5,
        timestamp=UTC_TS,
    )
    p3.update(rho_avg=0.56, timestamp=UTC_TS)
    p3.update(rho_avg=0.56, timestamp=UTC_TS)
    p3.update(rho_avg=0.44, business_days_elapsed=3, timestamp=UTC_TS)

    assert event_types(emitted_events) == ("P1_TRIP", "P1_RESET", "P3_FIRE", "P3_CLEAR")
    assert [event.prior_state for event in emitted_events] == [
        "P1_INACTIVE",
        "P1_ACTIVE",
        "P3_INACTIVE",
        "P3_ACTIVE",
    ]
    assert [event.next_state for event in emitted_events] == [
        "P1_ACTIVE",
        "P1_INACTIVE",
        "P3_ACTIVE",
        "P3_INACTIVE",
    ]
