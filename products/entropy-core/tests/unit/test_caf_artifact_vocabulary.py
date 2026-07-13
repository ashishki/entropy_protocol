"""Unit tests for CAF artifact vocabulary boundaries."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    CAF_ARTIFACT_TYPES,
    CAF_FORBIDDEN_EXECUTION_FIELDS,
    CAF_REQUIRED_NO_CLAIM_LABELS,
    AllocationDecisionArtifact,
)


def test_caf_vocabulary_lists_required_artifacts() -> None:
    assert CAF_ARTIFACT_TYPES == (
        "allocation_decision",
        "risk_policy",
        "portfolio_constraint",
        "decision_rationale",
        "decision_evidence_bundle",
    )


def test_caf_artifacts_require_no_claim_labels() -> None:
    artifact = caf_decision()

    assert set(CAF_REQUIRED_NO_CLAIM_LABELS).issubset(artifact.no_claim_boundary)

    with pytest.raises(ValidationError, match="CAF artifacts require no-claim labels"):
        caf_decision(
            no_claim_boundary=tuple(
                label for label in CAF_REQUIRED_NO_CLAIM_LABELS if label != "not_live_allocation"
            )
        )


def test_caf_vocabulary_has_no_execution_fields() -> None:
    field_names = set(AllocationDecisionArtifact.model_fields)
    assert field_names.isdisjoint(CAF_FORBIDDEN_EXECUTION_FIELDS)

    with pytest.raises(ValidationError):
        AllocationDecisionArtifact.model_validate(
            caf_decision().model_dump(mode="json") | {"broker_id": "synthetic-broker"}
        )


def caf_decision(**overrides: object) -> AllocationDecisionArtifact:
    payload: dict[str, object] = {
        "decision_id": "SYNTH-CAF-DECISION-001",
        "portfolio_context_ref": "synthetic://caf/context/001",
        "constraint_refs": ("synthetic://caf/constraint/risk-budget",),
        "evidence_refs": ("synthetic://caf/evidence/bundle-001",),
        "rationale_refs": ("synthetic://caf/rationale/001",),
        "attribution_refs": {
            "stream_a_ref": "synthetic://caf/attribution/stream-a",
            "stream_b_ref": "synthetic://caf/attribution/stream-b",
            "stream_c_ref": "synthetic://caf/attribution/stream-c",
            "stream_d_ref": "synthetic://caf/attribution/stream-d",
        },
        "limitations": ("synthetic CAF decision evidence only",),
        "no_claim_boundary": CAF_REQUIRED_NO_CLAIM_LABELS,
    }
    payload.update(overrides)
    return AllocationDecisionArtifact.model_validate(payload)
