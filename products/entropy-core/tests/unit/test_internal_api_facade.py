"""Unit tests for internal artifact API facade."""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

import pytest

import entropy.artifacts.api as api_module
from entropy.artifacts import (
    ExpectedOutputHash,
    HashComparisonPolicy,
    ReproducibilityManifest,
)
from entropy.artifacts.governance import ArtifactGovernanceViolation

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"
OUTPUT_REF = "artifacts/reproducibility/artifact-001/report.json"


def test_facade_exposes_core_operations(tmp_path: Path) -> None:
    validation = api_module.validate_artifact(FIXTURES / "valid_artifact.json")
    record, _event = api_module.register_artifact(
        FIXTURES / "valid_artifact.json",
        tmp_path / "registry",
    )
    comparison = api_module.compare_artifact_output(
        manifest_for_payload({"ok": True}),
        OUTPUT_REF,
        {"ok": True},
        {"ok": True},
    )
    packet = api_module.build_evidence_packet(record)
    transition = api_module.transition_artifact_state(
        "artifact-001",
        "validated_internal",
        tmp_path / "governance",
    )

    assert validation.ok is True
    assert record.artifact_id.startswith("artifact-")
    assert comparison.status == "exact"
    assert packet.artifact_summary.artifact_id == record.artifact_id
    assert transition.next_state == "validated_internal"


def test_facade_matches_cli_error_semantics(tmp_path: Path) -> None:
    result = api_module.validate_artifact(
        FIXTURES / "valid_artifact.json",
        profile="trader-risk-audit",
    )

    assert result.ok is False
    assert result.errors[0].code == "artifact.profile_violation"
    assert "missing required no-claim boundaries" in result.errors[0].message
    with pytest.raises(ArtifactGovernanceViolation):
        api_module.transition_artifact_state(
            "artifact-001",
            "approved_for_controlled_external_pilot",
            tmp_path / "governance",
        )


def test_facade_has_no_service_surface() -> None:
    source = inspect.getsource(api_module).lower()

    assert "fastapi" not in source
    assert "requests" not in source
    assert "httpx" not in source
    assert "auth" not in source
    assert "tenant" not in source
    assert "socket" not in source


def manifest_for_payload(payload: object) -> ReproducibilityManifest:
    return ReproducibilityManifest.model_validate(
        {
            "artifact_id": "artifact-001",
            "rerun_command": ["python", "-m", "entropy.artifacts.replay_fixture", "artifact-001"],
            "input_refs": ["tests/fixtures/artifacts/valid_artifact.json"],
            "expected_output_refs": [OUTPUT_REF],
            "hash_policy": HashComparisonPolicy(
                expected_hashes=(
                    ExpectedOutputHash(output_ref=OUTPUT_REF, expected_hash=stable_hash(payload)),
                ),
            ),
            "reproducibility_status": "fully_reproducible",
        }
    )


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()
