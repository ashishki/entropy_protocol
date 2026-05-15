"""Unit tests for artifact reproducibility CLI commands."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli

runner = CliRunner()


def test_compare_prints_reproduction_status(tmp_path: Path, monkeypatch) -> None:
    artifact_id = "artifact-001"
    expected_path = tmp_path / "expected.json"
    actual_path = tmp_path / "actual.json"
    expected = {"finding": "same", "generated_at": "2026-05-14T10:00:00Z"}
    actual = {"finding": "same", "generated_at": "2026-05-14T11:00:00Z"}
    expected_path.write_text(json.dumps(expected), encoding="utf-8")
    actual_path.write_text(json.dumps(actual), encoding="utf-8")
    write_manifest(tmp_path, artifact_id, expected_path, expected)
    monkeypatch.setenv("ENTROPY_REPRODUCIBILITY_MANIFEST_DIR", str(tmp_path / "manifests"))

    result = runner.invoke(cli.app, ["artifact", "compare", artifact_id, "--against", str(actual_path)])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["artifact_id"] == artifact_id
    assert payload["result"]["status"] == "materially_equivalent"
    assert payload["result"]["ignored_volatile_fields"] == ["$.generated_at"]


def test_reproduce_requires_manifest(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REPRODUCIBILITY_MANIFEST_DIR", str(tmp_path / "manifests"))

    result = runner.invoke(cli.app, ["artifact", "reproduce", "artifact-missing"])

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {
        "errors": [
            {
                "code": "artifact_reproducibility.manifest_not_found",
                "message": "Approved local reproducibility manifest was not found.",
                "path": "$",
                "severity": "P1",
            }
        ],
        "ok": False,
    }


def test_cli_records_limitations(tmp_path: Path, monkeypatch) -> None:
    artifact_id = "artifact-001"
    expected_path = tmp_path / "expected.json"
    actual_path = tmp_path / "actual.json"
    expected = {"finding": "same", "generated_at": "2026-05-14T10:00:00Z"}
    actual = {"finding": "same", "generated_at": "2026-05-14T11:00:00Z"}
    expected_path.write_text(json.dumps(expected), encoding="utf-8")
    actual_path.write_text(json.dumps(actual), encoding="utf-8")
    write_manifest(tmp_path, artifact_id, expected_path, expected)
    monkeypatch.setenv("ENTROPY_REPRODUCIBILITY_MANIFEST_DIR", str(tmp_path / "manifests"))

    result = runner.invoke(cli.app, ["artifact", "compare", artifact_id, "--against", str(actual_path)])
    payload = json.loads(result.stdout)

    assert payload["limitations"] == {"direct_rerun_execution": "blocked"}
    assert payload["declared_nondeterminism"] == [
        {
            "field_path": "$.generated_at",
            "reason": "rerun timestamp is expected to change",
        }
    ]
    assert payload["non_reproducible_fields"] == []


def write_manifest(
    tmp_path: Path,
    artifact_id: str,
    expected_path: Path,
    expected_payload: object,
) -> None:
    manifest_dir = tmp_path / "manifests"
    manifest_dir.mkdir()
    manifest = {
        "artifact_id": artifact_id,
        "rerun_command": ["python", "-m", "entropy.artifacts.replay_fixture", artifact_id],
        "input_refs": ["tests/fixtures/artifacts/valid_artifact.json"],
        "expected_output_refs": [str(expected_path)],
        "hash_policy": {
            "expected_hashes": [
                {"output_ref": str(expected_path), "expected_hash": stable_hash(expected_payload)}
            ],
            "ignored_volatile_fields": ["$.generated_at"],
        },
        "volatile_fields": ["$.generated_at"],
        "accepted_nondeterminism": [
            {
                "field_path": "$.generated_at",
                "reason": "rerun timestamp is expected to change",
            }
        ],
        "reproducibility_status": "fully_reproducible",
    }
    (manifest_dir / f"{artifact_id}.json").write_text(json.dumps(manifest), encoding="utf-8")


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()
