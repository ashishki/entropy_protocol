"""Deterministic artifact governance states and transition validation."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ArtifactGovernanceState = Literal[
    "draft",
    "validated_internal",
    "blocked",
    "needs_manual_review",
    "approved_for_controlled_external_pilot",
    "rejected",
    "superseded",
]

ARTIFACT_GOVERNANCE_STATES: tuple[ArtifactGovernanceState, ...] = (
    "draft",
    "validated_internal",
    "blocked",
    "needs_manual_review",
    "approved_for_controlled_external_pilot",
    "rejected",
    "superseded",
)

APPROVAL_BOUND_ARTIFACT_STATES: tuple[ArtifactGovernanceState, ...] = (
    "approved_for_controlled_external_pilot",
)

ALLOWED_ARTIFACT_APPROVAL_SCOPES = (
    "artifact_validation",
    "controlled_external_pilot",
)

ALLOWED_ARTIFACT_APPROVAL_MAXIMUM_EFFECTS = (
    "validate_artifact_metadata",
    "mark_controlled_external_pilot_metadata",
)

REQUIRED_APPROVAL_BLOCKED_SURFACES = (
    "live_execution",
    "holdout_access",
    "broker_exchange_execution",
    "production",
    "capital_ready",
)

ALLOWED_ARTIFACT_GOVERNANCE_TRANSITIONS: dict[
    ArtifactGovernanceState,
    tuple[ArtifactGovernanceState, ...],
] = {
    "draft": ("validated_internal", "needs_manual_review", "blocked", "rejected"),
    "validated_internal": (
        "needs_manual_review",
        "approved_for_controlled_external_pilot",
        "blocked",
        "rejected",
        "superseded",
    ),
    "needs_manual_review": ("validated_internal", "blocked", "rejected"),
    "blocked": ("needs_manual_review", "rejected"),
    "approved_for_controlled_external_pilot": ("blocked", "superseded"),
    "rejected": ("superseded",),
    "superseded": (),
}


class ArtifactGovernanceViolation(ValueError):
    """Raised when a governance state transition is not allowed."""


class ArtifactGovernanceTransition(BaseModel):
    """One validated deterministic governance transition request."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    prior_state: ArtifactGovernanceState
    next_state: ArtifactGovernanceState
    approval_event_ref: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_transition(self) -> "ArtifactGovernanceTransition":
        allowed_next_states = ALLOWED_ARTIFACT_GOVERNANCE_TRANSITIONS[self.prior_state]
        if self.next_state not in allowed_next_states:
            raise ArtifactGovernanceViolation(
                f"Forbidden artifact governance transition: {self.prior_state} -> {self.next_state}"
            )
        if self.next_state in APPROVAL_BOUND_ARTIFACT_STATES and not self.approval_event_ref:
            raise ArtifactGovernanceViolation(
                "External pilot approval transitions require a human approval event reference."
            )
        if self.next_state not in APPROVAL_BOUND_ARTIFACT_STATES and self.approval_event_ref:
            raise ArtifactGovernanceViolation(
                "Approval event references are only accepted for approval-bound transitions."
            )
        return self


class ArtifactGovernanceTransitionEvent(BaseModel):
    """Append-only artifact governance transition event."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    event_version: Literal["entropy-artifact-governance-event/v1"] = (
        "entropy-artifact-governance-event/v1"
    )
    event_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    prior_state: ArtifactGovernanceState
    next_state: ArtifactGovernanceState
    created_at: datetime
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    approval_event_ref: str | None = Field(default=None, min_length=1)
    prior_event_id: str | None = Field(default=None, min_length=1)


class ArtifactGovernanceApprovalEvent(BaseModel):
    """Explicit human approval event metadata for approval-bound transitions."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    approval_id: str = Field(min_length=1)
    approver: str = Field(min_length=1)
    scope: Literal["artifact_validation", "controlled_external_pilot"]
    maximum_effect: Literal[
        "validate_artifact_metadata",
        "mark_controlled_external_pilot_metadata",
    ]
    approved_at: datetime
    blocked_surfaces: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_approval_event(self) -> "ArtifactGovernanceApprovalEvent":
        blocked_surfaces = set(self.blocked_surfaces)
        missing_blocks = tuple(
            surface
            for surface in REQUIRED_APPROVAL_BLOCKED_SURFACES
            if surface not in blocked_surfaces
        )
        if missing_blocks:
            raise ArtifactGovernanceViolation(
                "Approval events must preserve blocked surfaces: " + ", ".join(missing_blocks)
            )
        if (
            self.scope == "controlled_external_pilot"
            and self.maximum_effect != "mark_controlled_external_pilot_metadata"
        ):
            raise ArtifactGovernanceViolation(
                "Controlled external pilot approvals require matching maximum effect."
            )
        return self


def validate_artifact_governance_transition(
    prior_state: ArtifactGovernanceState,
    next_state: ArtifactGovernanceState,
    *,
    approval_event_ref: str | None = None,
) -> ArtifactGovernanceTransition:
    """Validate one deterministic artifact governance transition."""
    return ArtifactGovernanceTransition(
        prior_state=prior_state,
        next_state=next_state,
        approval_event_ref=approval_event_ref,
    )


def bind_approval_event_to_transition(
    prior_state: ArtifactGovernanceState,
    next_state: ArtifactGovernanceState,
    approval_event: ArtifactGovernanceApprovalEvent,
) -> ArtifactGovernanceTransition:
    """Validate an approval-bound transition against an explicit approval event."""
    if next_state not in APPROVAL_BOUND_ARTIFACT_STATES:
        raise ArtifactGovernanceViolation(
            "Approval binding is only valid for approval-bound states."
        )
    if approval_event.scope != "controlled_external_pilot":
        raise ArtifactGovernanceViolation(
            "External pilot approval requires controlled external pilot scope."
        )
    return validate_artifact_governance_transition(
        prior_state,
        next_state,
        approval_event_ref=approval_event.approval_id,
    )


def record_artifact_governance_transition(
    artifact_id: str,
    next_state: ArtifactGovernanceState,
    governance_dir: str | Path,
    *,
    prior_state: ArtifactGovernanceState | None = None,
    approval_event_ref: str | None = None,
    created_at: datetime | None = None,
    actor: str = "local-operator",
    reason: str = "local governance transition",
) -> ArtifactGovernanceTransitionEvent:
    """Validate and append one artifact governance transition event."""
    history = read_artifact_governance_history(artifact_id, governance_dir)
    resolved_prior_state = prior_state or current_artifact_governance_state(history)
    transition = validate_artifact_governance_transition(
        resolved_prior_state,
        next_state,
        approval_event_ref=approval_event_ref,
    )
    prior_event_id = history[-1].event_id if history else None
    event = ArtifactGovernanceTransitionEvent(
        event_id=_transition_event_id(
            artifact_id,
            transition.prior_state,
            transition.next_state,
            approval_event_ref,
            len(history),
        ),
        artifact_id=artifact_id,
        prior_state=transition.prior_state,
        next_state=transition.next_state,
        created_at=created_at or datetime.now().astimezone(),
        actor=actor,
        reason=reason,
        approval_event_ref=approval_event_ref,
        prior_event_id=prior_event_id,
    )
    _append_jsonl(_events_path(Path(governance_dir)), event.model_dump(mode="json"))
    return event


def read_artifact_governance_history(
    artifact_id: str,
    governance_dir: str | Path,
) -> tuple[ArtifactGovernanceTransitionEvent, ...]:
    """Read append-only governance transition events for one artifact."""
    return tuple(
        event for event in _read_events(Path(governance_dir)) if event.artifact_id == artifact_id
    )


def current_artifact_governance_state(
    history: tuple[ArtifactGovernanceTransitionEvent, ...],
) -> ArtifactGovernanceState:
    """Return the current governance state from append-only history."""
    if not history:
        return "draft"
    return history[-1].next_state


def _read_events(governance_dir: Path) -> tuple[ArtifactGovernanceTransitionEvent, ...]:
    path = _events_path(governance_dir)
    if not path.exists():
        return ()
    return tuple(
        ArtifactGovernanceTransitionEvent.model_validate(json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def _append_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


def _events_path(governance_dir: Path) -> Path:
    return governance_dir / "events.jsonl"


def _transition_event_id(
    artifact_id: str,
    prior_state: ArtifactGovernanceState,
    next_state: ArtifactGovernanceState,
    approval_event_ref: str | None,
    sequence: int,
) -> str:
    payload = f"{artifact_id}:{prior_state}:{next_state}:{approval_event_ref or ''}:{sequence}"
    return "governance-event-" + hashlib.sha256(payload.encode()).hexdigest()[:16]


__all__ = [
    "ALLOWED_ARTIFACT_GOVERNANCE_TRANSITIONS",
    "ALLOWED_ARTIFACT_APPROVAL_MAXIMUM_EFFECTS",
    "ALLOWED_ARTIFACT_APPROVAL_SCOPES",
    "APPROVAL_BOUND_ARTIFACT_STATES",
    "ARTIFACT_GOVERNANCE_STATES",
    "REQUIRED_APPROVAL_BLOCKED_SURFACES",
    "ArtifactGovernanceApprovalEvent",
    "ArtifactGovernanceState",
    "ArtifactGovernanceTransition",
    "ArtifactGovernanceTransitionEvent",
    "ArtifactGovernanceViolation",
    "bind_approval_event_to_transition",
    "current_artifact_governance_state",
    "read_artifact_governance_history",
    "record_artifact_governance_transition",
    "validate_artifact_governance_transition",
]
