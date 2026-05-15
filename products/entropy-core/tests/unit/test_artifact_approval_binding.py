"""Unit tests for artifact governance approval-event binding."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    ALLOWED_ARTIFACT_APPROVAL_SCOPES,
    REQUIRED_APPROVAL_BLOCKED_SURFACES,
    ArtifactGovernanceApprovalEvent,
    ArtifactGovernanceViolation,
    bind_approval_event_to_transition,
)

APPROVED_AT = datetime(2026, 5, 14, 14, 0, tzinfo=UTC)


def approval_event(**overrides: object) -> ArtifactGovernanceApprovalEvent:
    payload: dict[str, object] = {
        "approval_id": "approval-event-001",
        "approver": "human-reviewer",
        "scope": "controlled_external_pilot",
        "maximum_effect": "mark_controlled_external_pilot_metadata",
        "approved_at": APPROVED_AT,
        "blocked_surfaces": REQUIRED_APPROVAL_BLOCKED_SURFACES,
    }
    payload.update(overrides)
    return ArtifactGovernanceApprovalEvent.model_validate(payload)


def test_approval_bound_transitions_require_event_fields() -> None:
    event = approval_event()
    transition = bind_approval_event_to_transition(
        "validated_internal",
        "approved_for_controlled_external_pilot",
        event,
    )

    assert transition.approval_event_ref == event.approval_id
    assert transition.next_state == "approved_for_controlled_external_pilot"
    with pytest.raises(ValidationError):
        ArtifactGovernanceApprovalEvent.model_validate(
            {
                "approval_id": "approval-event-001",
                "scope": "controlled_external_pilot",
                "maximum_effect": "mark_controlled_external_pilot_metadata",
                "approved_at": APPROVED_AT,
                "blocked_surfaces": REQUIRED_APPROVAL_BLOCKED_SURFACES,
            }
        )


def test_approval_binding_rejects_scope_expansion() -> None:
    assert ALLOWED_ARTIFACT_APPROVAL_SCOPES == (
        "artifact_validation",
        "controlled_external_pilot",
    )
    with pytest.raises(ValidationError):
        approval_event(scope="production_release")
    with pytest.raises(ValidationError, match="matching maximum effect"):
        approval_event(maximum_effect="validate_artifact_metadata")
    with pytest.raises(ArtifactGovernanceViolation, match="controlled external pilot scope"):
        bind_approval_event_to_transition(
            "validated_internal",
            "approved_for_controlled_external_pilot",
            approval_event(
                scope="artifact_validation",
                maximum_effect="validate_artifact_metadata",
            ),
        )


def test_approval_binding_preserves_restricted_boundaries() -> None:
    assert REQUIRED_APPROVAL_BLOCKED_SURFACES == (
        "live_execution",
        "holdout_access",
        "broker_exchange_execution",
        "production",
        "capital_ready",
    )
    with pytest.raises(ValidationError, match="must preserve blocked surfaces"):
        approval_event(blocked_surfaces=("live_execution", "production", "capital_ready"))
