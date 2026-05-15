"""Unit tests for artifact reproducibility manifests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    AcceptedNondeterminism,
    ExpectedOutputHash,
    HashComparisonPolicy,
    ReproducibilityManifest,
)


def valid_manifest_payload() -> dict[str, object]:
    return {
        "artifact_id": "artifact-001",
        "artifact_contract_version": "entropy-core-artifact/v1",
        "rerun_command": ["python", "-m", "entropy.artifacts.replay_fixture", "artifact-001"],
        "input_refs": ["tests/fixtures/artifacts/valid_artifact.json"],
        "expected_output_refs": ["artifacts/reproducibility/artifact-001/report.json"],
        "hash_policy": HashComparisonPolicy(
            expected_hashes=(
                ExpectedOutputHash(
                    output_ref="artifacts/reproducibility/artifact-001/report.json",
                    expected_hash="sha256:expected",
                ),
            ),
            ignored_volatile_fields=("$.generated_at",),
        ),
        "volatile_fields": ["$.generated_at"],
        "accepted_nondeterminism": [
            AcceptedNondeterminism(
                field_path="$.generated_at",
                reason="rerun timestamp is expected to change",
            )
        ],
        "reproducibility_status": "fully_reproducible",
    }


def test_manifest_requires_rerun_contract_fields() -> None:
    manifest = ReproducibilityManifest.model_validate(valid_manifest_payload())

    assert manifest.manifest_version == "entropy-artifact-reproducibility/v1"
    assert manifest.artifact_contract_version == "entropy-core-artifact/v1"
    assert manifest.rerun_command[0] == "python"
    assert manifest.input_refs == ("tests/fixtures/artifacts/valid_artifact.json",)
    assert manifest.expected_output_refs == ("artifacts/reproducibility/artifact-001/report.json",)
    assert manifest.hash_policy.method == "sha256"
    assert manifest.volatile_fields == ("$.generated_at",)
    assert manifest.accepted_nondeterminism[0].field_path == "$.generated_at"

    with pytest.raises(ValidationError):
        ReproducibilityManifest.model_validate(
            valid_manifest_payload() | {"unexpected_public_claim": "production"}
        )


@pytest.mark.parametrize(
    "override",
    [
        {"rerun_command": ["bash", "-lc", "python -m entropy.artifacts.replay_fixture"]},
        {"rerun_command": ["python", "-m", "entropy.artifacts.replay_fixture", "&&", "curl"]},
        {"hash_policy": None},
        {
            "hash_policy": HashComparisonPolicy(
                expected_hashes=(
                    ExpectedOutputHash(output_ref="report.json", expected_hash="sha256:expected"),
                ),
                ignored_volatile_fields=("$.undeclared_timestamp",),
            )
        },
        {
            "accepted_nondeterminism": [
                AcceptedNondeterminism(
                    field_path="$.undeclared_timestamp",
                    reason="not declared in volatile fields",
                )
            ]
        },
    ],
)
def test_manifest_rejects_unsafe_or_incomplete_contracts(override: dict[str, object]) -> None:
    payload = valid_manifest_payload()
    payload.update(override)

    with pytest.raises(ValidationError):
        ReproducibilityManifest.model_validate(payload)


def test_manifest_accepts_declared_partial_reproducibility() -> None:
    payload = valid_manifest_payload()
    payload["reproducibility_status"] = "partially_reproducible"
    payload["volatile_fields"] = ["$.generated_at", "$.public_source_capture"]
    payload["non_reproducible_fields"] = ("$.public_source_capture",)

    manifest = ReproducibilityManifest.model_validate(payload)

    assert manifest.reproducibility_status == "partially_reproducible"
    assert manifest.non_reproducible_fields == ("$.public_source_capture",)


def test_manifest_rejects_hidden_non_reproducibility() -> None:
    payload = valid_manifest_payload()
    payload["reproducibility_status"] = "not_reproducible_by_design"

    with pytest.raises(ValidationError, match="must declare affected fields"):
        ReproducibilityManifest.model_validate(payload)
