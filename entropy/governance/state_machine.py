"""Deterministic P1/P3 governance state machines."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from entropy.db.models import GovernanceEvent as GovernanceEventRow
from entropy.models.registry import GovernanceEvent, GovernanceEventType


EventSink = Callable[[GovernanceEvent], None]

DEFAULT_TRIAL_ID = "portfolio"
DEFAULT_ACTOR = "governance_state_machine"


@dataclass(frozen=True)
class P1Config:
    """Policy parameters for the P1 drawdown circuit breaker."""

    trip_drawdown_pct: float = 0.12
    reset_gap_from_hwm: float = 0.08
    reset_business_days: int = 5


@dataclass(frozen=True)
class P3Config:
    """Policy parameters for the P3 correlation trigger."""

    fire_rho_avg: float = 0.55
    clear_rho_avg: float = 0.45
    high_reduction_rho_avg: float = 0.65
    low_gross_reduction: float = 0.35
    high_gross_reduction: float = 0.50
    cooldown_business_days: int = 3
    ramp_business_days: int = 3


class _GovernanceEventRecorder:
    """Emit domain events and optionally persist them through a DB session."""

    def __init__(
        self,
        *,
        trial_id: str,
        policy_hash: str,
        actor: str = DEFAULT_ACTOR,
        event_sink: EventSink | None = None,
        session: Session | None = None,
    ) -> None:
        self.trial_id = trial_id
        self.policy_hash = policy_hash
        self.actor = actor
        self._event_sink = event_sink
        self._session = session
        self.events: list[GovernanceEvent] = []

    def emit(
        self,
        event_type: GovernanceEventType,
        *,
        timestamp: datetime | None,
        reason: str,
        prior_state: str,
        next_state: str,
    ) -> GovernanceEvent:
        event = GovernanceEvent(
            event_type=event_type,
            timestamp=_utc_timestamp(timestamp),
            trial_id=self.trial_id,
            actor=self.actor,
            reason=reason,
            policy_hash=self.policy_hash,
            prior_state=prior_state,
            next_state=next_state,
        )
        self.events.append(event)
        if self._event_sink is not None:
            self._event_sink(event)
        if self._session is not None:
            self._session.add(
                GovernanceEventRow(
                    event_id=uuid4().hex,
                    trial_id=event.trial_id,
                    event_type=event.event_type.value,
                    timestamp=event.timestamp,
                    actor=event.actor,
                    reason=event.reason,
                    policy_hash=event.policy_hash,
                    prior_state=event.prior_state,
                    next_state=event.next_state,
                )
            )
            self._session.flush()
        return event


class P1StateMachine:
    """P1 drawdown circuit breaker.

    The state machine is deterministic and emits exactly one event per state
    transition. Repeated updates inside the same state are no-ops.
    """

    def __init__(
        self,
        *,
        config: P1Config | None = None,
        trial_id: str = DEFAULT_TRIAL_ID,
        policy_hash: str = "policy_hash",
        actor: str = DEFAULT_ACTOR,
        event_sink: EventSink | None = None,
        session: Session | None = None,
    ) -> None:
        self.config = config or P1Config()
        self.is_p1_active = False
        self._recorder = _GovernanceEventRecorder(
            trial_id=trial_id,
            policy_hash=policy_hash,
            actor=actor,
            event_sink=event_sink,
            session=session,
        )

    @property
    def events(self) -> tuple[GovernanceEvent, ...]:
        return tuple(self._recorder.events)

    def can_open_new_position(self) -> bool:
        return not self.is_p1_active

    def update(
        self,
        *,
        drawdown_pct: float,
        gap_from_hwm: float | None = None,
        business_days_elapsed: int = 0,
        timestamp: datetime | None = None,
    ) -> bool:
        if not self.is_p1_active and drawdown_pct >= self.config.trip_drawdown_pct:
            self.is_p1_active = True
            self._recorder.emit(
                GovernanceEventType.P1_TRIP,
                timestamp=timestamp,
                reason="drawdown_threshold_reached",
                prior_state="P1_INACTIVE",
                next_state="P1_ACTIVE",
            )
            return self.is_p1_active

        if (
            self.is_p1_active
            and gap_from_hwm is not None
            and gap_from_hwm < self.config.reset_gap_from_hwm
            and business_days_elapsed >= self.config.reset_business_days
        ):
            self.is_p1_active = False
            self._recorder.emit(
                GovernanceEventType.P1_RESET,
                timestamp=timestamp,
                reason="drawdown_recovery_confirmed",
                prior_state="P1_ACTIVE",
                next_state="P1_INACTIVE",
            )
        return self.is_p1_active


class P3StateMachine:
    """P3 correlation trigger with hysteresis, cooldown, and ramp pause support."""

    def __init__(
        self,
        *,
        config: P3Config | None = None,
        trial_id: str = DEFAULT_TRIAL_ID,
        policy_hash: str = "policy_hash",
        actor: str = DEFAULT_ACTOR,
        event_sink: EventSink | None = None,
        session: Session | None = None,
    ) -> None:
        self.config = config or P3Config()
        self.is_p3_active = False
        self.gross_reduction = 0.0
        self.p3_ramp_progress = 0.0
        self.ramp_paused = False
        self._recorder = _GovernanceEventRecorder(
            trial_id=trial_id,
            policy_hash=policy_hash,
            actor=actor,
            event_sink=event_sink,
            session=session,
        )

    @property
    def events(self) -> tuple[GovernanceEvent, ...]:
        return tuple(self._recorder.events)

    def update(
        self,
        *,
        rho_avg: float,
        business_days_elapsed: int = 0,
        p1_active: bool = False,
        timestamp: datetime | None = None,
    ) -> bool:
        if p1_active and self.is_p3_active:
            self.ramp_paused = True
            return self.is_p3_active

        if self.is_p3_active:
            self.ramp_paused = False
            if (
                rho_avg < self.config.clear_rho_avg
                and business_days_elapsed >= self.config.cooldown_business_days
            ):
                self.is_p3_active = False
                self.gross_reduction = 0.0
                self.p3_ramp_progress = 0.0
                self._recorder.emit(
                    GovernanceEventType.P3_CLEAR,
                    timestamp=timestamp,
                    reason="correlation_recovery_confirmed",
                    prior_state="P3_ACTIVE",
                    next_state="P3_INACTIVE",
                )
                return self.is_p3_active
            self._advance_ramp(business_days_elapsed)
            return self.is_p3_active

        if rho_avg > self.config.fire_rho_avg:
            self.is_p3_active = True
            self.gross_reduction = self._gross_reduction_for(rho_avg)
            self.p3_ramp_progress = 0.0
            self.ramp_paused = p1_active
            self._recorder.emit(
                GovernanceEventType.P3_FIRE,
                timestamp=timestamp,
                reason="correlation_threshold_reached",
                prior_state="P3_INACTIVE",
                next_state="P3_ACTIVE",
            )
        return self.is_p3_active

    def _gross_reduction_for(self, rho_avg: float) -> float:
        if rho_avg > self.config.high_reduction_rho_avg:
            return self.config.high_gross_reduction
        return self.config.low_gross_reduction

    def _advance_ramp(self, business_days_elapsed: int) -> None:
        if business_days_elapsed <= 0:
            return
        increment = business_days_elapsed / self.config.ramp_business_days
        self.p3_ramp_progress = min(1.0, self.p3_ramp_progress + increment)


class GovernanceStateMachine:
    """Coordinator for concurrent P1/P3 transition semantics."""

    def __init__(
        self,
        *,
        p1_config: P1Config | None = None,
        p3_config: P3Config | None = None,
        trial_id: str = DEFAULT_TRIAL_ID,
        policy_hash: str = "policy_hash",
        actor: str = DEFAULT_ACTOR,
        event_sink: EventSink | None = None,
        session: Session | None = None,
    ) -> None:
        self.p1 = P1StateMachine(
            config=p1_config,
            trial_id=trial_id,
            policy_hash=policy_hash,
            actor=actor,
            event_sink=event_sink,
            session=session,
        )
        self.p3 = P3StateMachine(
            config=p3_config,
            trial_id=trial_id,
            policy_hash=policy_hash,
            actor=actor,
            event_sink=event_sink,
            session=session,
        )

    def can_open_new_position(self) -> bool:
        return self.p1.can_open_new_position()

    def update(
        self,
        *,
        drawdown_pct: float,
        rho_avg: float,
        gap_from_hwm: float | None = None,
        business_days_elapsed: int = 0,
        timestamp: datetime | None = None,
    ) -> None:
        was_p1_active = self.p1.is_p1_active
        self.p1.update(
            drawdown_pct=drawdown_pct,
            gap_from_hwm=gap_from_hwm,
            business_days_elapsed=business_days_elapsed,
            timestamp=timestamp,
        )
        p3_elapsed = 0 if was_p1_active and not self.p1.is_p1_active else business_days_elapsed
        self.p3.update(
            rho_avg=rho_avg,
            business_days_elapsed=p3_elapsed,
            p1_active=self.p1.is_p1_active,
            timestamp=timestamp,
        )


def _utc_timestamp(timestamp: datetime | None) -> datetime:
    if timestamp is None:
        return datetime.now(timezone.utc)
    if timestamp.tzinfo is None or timestamp.utcoffset() != timezone.utc.utcoffset(timestamp):
        raise ValueError("governance event timestamp must be timezone-aware UTC")
    return timestamp


def event_types(events: tuple[GovernanceEvent, ...] | list[GovernanceEvent]) -> tuple[str, ...]:
    """Return event type values for compact assertions and reports."""
    return tuple(event.event_type.value for event in events)


__all__ = [
    "GovernanceStateMachine",
    "P1Config",
    "P1StateMachine",
    "P3Config",
    "P3StateMachine",
    "event_types",
]
