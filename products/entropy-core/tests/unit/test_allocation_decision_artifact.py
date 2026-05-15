"""Unit tests for CAF allocation decision artifacts."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    CAF_ARTIFACT_SCHEMA_VERSION,
    CAF_REQUIRED_NO_CLAIM_LABELS,
    AllocationDecisionArtifact,
    validate_artifact_payload,
)


def test_allocation_decision_requires_governed_fields() -> None:
    artifact = allocation_decision()
    contract = artifact.to_artifact_contract()
    result = validate_artifact_payload(contract.model_dump(mode="json"))

    assert artifact.caf_artifact_version == CAF_ARTIFACT_SCHEMA_VERSION
    assert artifact.decision_id == "SYNTH-CAF-DECISION-001"
    assert artifact.portfolio_context_ref == "synthetic://caf/context/001"
    assert artifact.constraint_refs == ("synthetic://caf/constraint/risk-budget",)
    assert artifact.evidence_refs == ("synthetic://caf/evidence/bundle-001",)
    assert artifact.rationale_refs == ("synthetic://caf/rationale/001",)
    assert artifact.limitations == ("synthetic CAF decision evidence only",)
    assert set(CAF_REQUIRED_NO_CLAIM_LABELS).issubset(artifact.no_claim_boundary)
    assert result.ok is True
    assert result.artifact is not None
    assert result.artifact.product == "entropy-core-caf"


@pytest.mark.parametrize(
    "unsafe_claim",
    ("future_performance", "investment_advice", "capital_ready", "automated_execution"),
)
def test_allocation_decision_rejects_unsafe_claims(unsafe_claim: str) -> None:
    with pytest.raises(ValidationError, match="cannot claim advice"):
        allocation_decision(no_claim_boundary=(*CAF_REQUIRED_NO_CLAIM_LABELS, unsafe_claim))


def test_allocation_decision_preserves_four_stream_boundary() -> None:
    artifact = allocation_decision()

    assert artifact.attribution_refs.stream_d_ref == "synthetic://caf/attribution/stream-d"
    assert artifact.attribution_refs.net_sharpe_streams == (
        "stream_a",
        "stream_b",
        "stream_c",
    )

    payload = allocation_decision().model_dump(mode="json")
    payload["attribution_refs"]["net_sharpe_streams"] = ["stream_a", "stream_d"]
    with pytest.raises(ValidationError, match="stream_d"):
        AllocationDecisionArtifact.model_validate(payload)


def allocation_decision(**overrides: object) -> AllocationDecisionArtifact:
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
