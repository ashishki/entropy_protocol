"""Unit tests for artifact file loading and redacted validation results."""

from __future__ import annotations

import json
from pathlib import Path

from entropy.artifacts import validate_artifact_file

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"


def test_json_and_yaml_load_to_same_model() -> None:
    json_result = validate_artifact_file(FIXTURES / "valid_artifact.json")
    yaml_result = validate_artifact_file(FIXTURES / "valid_artifact.yaml")

    assert json_result.ok is True
    assert yaml_result.ok is True
    assert json_result.artifact is not None
    assert yaml_result.artifact is not None
    assert json_result.artifact.model_dump(mode="json") == yaml_result.artifact.model_dump(
        mode="json"
    )


def test_invalid_artifact_returns_deterministic_errors() -> None:
    first_result = validate_artifact_file(FIXTURES / "invalid_artifact.json")
    second_result = validate_artifact_file(FIXTURES / "invalid_artifact.json")

    assert first_result.ok is False
    assert first_result.artifact is None
    assert first_result == second_result

    errors = [error.model_dump(mode="json") for error in first_result.errors]
    assert errors == sorted(errors, key=lambda error: (error["path"], error["code"], error["message"]))
    assert {
        "path": "$.external_delivery_approval_status",
        "code": "artifact.invalid_state",
        "severity": "P1",
        "message": "Artifact field uses a value outside the frozen vocabulary.",
    } in errors
    assert {
        "path": "$.manual_validation_status",
        "code": "artifact.invalid_state",
        "severity": "P1",
        "message": "Artifact field uses a value outside the frozen vocabulary.",
    } in errors
    assert {
        "path": "$.unexpected_claim_surface",
        "code": "artifact.extra_field",
        "severity": "P1",
        "message": "Unknown artifact field is not allowed.",
    } in errors


def test_validation_errors_do_not_leak_payloads(tmp_path: Path) -> None:
    private_payload = {
        "artifact_contract_version": "entropy-core-artifact/v1",
        "product": "internal-core-fixture",
        "run_id": "run-with-private-payload",
        "input_refs": ["PRIVATE CUSTOMER ROW: SECRET_TOKEN_123"],
        "policy_config_hash": "sha256:policy",
        "code_version_ref": "git:abcdef123456",
        "generated_artifact_refs": ["reports/internal-fixture.md"],
        "limitations": ["synthetic fixture only"],
        "no_claim_boundary": ["production SECRET_TOKEN_123"],
        "manual_validation_status": "not_reviewed",
        "error_register_ref": "error-registers/internal-fixture.md",
        "external_delivery_approval_status": "not_requested",
    }
    artifact_path = tmp_path / "private-invalid-artifact.json"
    artifact_path.write_text(json.dumps(private_payload), encoding="utf-8")

    result = validate_artifact_file(artifact_path)
    serialized_result = result.model_dump_json()

    assert result.ok is False
    assert "SECRET_TOKEN_123" not in serialized_result
    assert "PRIVATE CUSTOMER ROW" not in serialized_result
