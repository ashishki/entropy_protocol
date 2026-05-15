"""Unit tests for the entropy-core-artifact/v1 contract schema."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import ArtifactContractV1


def valid_artifact_payload() -> dict[str, object]:
    return {
        "artifact_contract_version": "entropy-core-artifact/v1",
        "product": "internal-core-fixture",
        "run_id": "run-2026-05-14-001",
        "input_refs": ["fixtures/artifacts/input-manifest.json"],
        "input_hashes": ["sha256:input"],
        "policy_config_hash": "sha256:policy",
        "code_version_ref": "git:abcdef123456",
        "generated_artifact_refs": ["reports/internal-fixture.md"],
        "limitations": ["synthetic fixture only"],
        "no_claim_boundary": [
            "not_production",
            "not_capital_ready",
            "not_investment_advice",
            "no_holdout_approval",
            "blocked_live_execution",
            "not_future_performance",
        ],
        "manual_validation_status": "not_reviewed",
        "error_register_ref": "error-registers/internal-fixture.md",
        "external_delivery_approval_status": "not_requested",
    }


def test_contract_accepts_required_fields_and_rejects_extra() -> None:
    artifact = ArtifactContractV1.model_validate(valid_artifact_payload())

    assert artifact.artifact_contract_version == "entropy-core-artifact/v1"
    assert artifact.input_refs == ("fixtures/artifacts/input-manifest.json",)

    payload_with_extra = valid_artifact_payload() | {"public_sdk_status": "approved"}
    with pytest.raises(ValidationError):
        ArtifactContractV1.model_validate(payload_with_extra)


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("manual_validation_status", "validated_for_public_release"),
        ("external_delivery_approval_status", "approved_for_production"),
    ],
)
def test_contract_rejects_unknown_decision_states(field_name: str, bad_value: str) -> None:
    payload = valid_artifact_payload()
    payload[field_name] = bad_value

    with pytest.raises(ValidationError):
        ArtifactContractV1.model_validate(payload)


@pytest.mark.parametrize(
    "unsafe_label",
    [
        "production",
        "capital-ready",
        "investment advice",
        "holdout approval",
        "live execution",
        "future performance",
    ],
)
def test_contract_rejects_unsafe_claim_labels(unsafe_label: str) -> None:
    payload = valid_artifact_payload()
    payload["no_claim_boundary"] = [unsafe_label]

    with pytest.raises(ValidationError, match="Unsafe claim labels"):
        ArtifactContractV1.model_validate(payload)
