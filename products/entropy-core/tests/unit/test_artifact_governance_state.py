"""Unit tests for artifact governance state transition model."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    ALLOWED_ARTIFACT_GOVERNANCE_TRANSITIONS,
    APPROVAL_BOUND_ARTIFACT_STATES,
    ARTIFACT_GOVERNANCE_STATES,
    ArtifactGovernanceTransition,
    ArtifactGovernanceViolation,
    validate_artifact_governance_transition,
)


def test_state_model_lists_required_states() -> None:
    assert ARTIFACT_GOVERNANCE_STATES == (
        "draft",
        "validated_internal",
        "blocked",
        "needs_manual_review",
        "approved_for_controlled_external_pilot",
        "rejected",
        "superseded",
    )
    assert APPROVAL_BOUND_ARTIFACT_STATES == ("approved_for_controlled_external_pilot",)
    assert ALLOWED_ARTIFACT_GOVERNANCE_TRANSITIONS["draft"] == (
        "validated_internal",
        "needs_manual_review",
        "blocked",
        "rejected",
    )
    assert ALLOWED_ARTIFACT_GOVERNANCE_TRANSITIONS["superseded"] == ()


def test_forbidden_transitions_rejected() -> None:
    transition = validate_artifact_governance_transition(
        "draft",
        "validated_internal",
    )

    assert transition.prior_state == "draft"
    assert transition.next_state == "validated_internal"
    assert transition.approval_event_ref is None

    with pytest.raises(ValidationError, match="Forbidden artifact governance transition"):
        validate_artifact_governance_transition(
            "draft",
            "approved_for_controlled_external_pilot",
            approval_event_ref="approval-event-001",
        )
    with pytest.raises(ValidationError, match="Forbidden artifact governance transition"):
        validate_artifact_governance_transition("superseded", "validated_internal")
    with pytest.raises(ValidationError, match="Input should be"):
        ArtifactGovernanceTransition(
            prior_state="invalid",  # type: ignore[arg-type]
            next_state="validated_internal",
        )


def test_external_pilot_requires_human_approval_event() -> None:
    with pytest.raises(ValidationError, match="human approval event reference"):
        validate_artifact_governance_transition(
            "validated_internal",
            "approved_for_controlled_external_pilot",
        )

    transition = validate_artifact_governance_transition(
        "validated_internal",
        "approved_for_controlled_external_pilot",
        approval_event_ref="approval-event-001",
    )

    assert transition.approval_event_ref == "approval-event-001"
    with pytest.raises(ValidationError, match="only accepted for approval-bound"):
        validate_artifact_governance_transition(
            "validated_internal",
            "blocked",
            approval_event_ref="approval-event-001",
        )
    assert issubclass(ArtifactGovernanceViolation, ValueError)
