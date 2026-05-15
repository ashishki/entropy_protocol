"""Unit tests for artifact evidence CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli

runner = CliRunner()
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"


def test_evidence_build_writes_packet(tmp_path: Path, monkeypatch) -> None:
    artifact_id = register_fixture(tmp_path, monkeypatch)

    result = runner.invoke(cli.app, ["evidence", "build", artifact_id])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    packet_path = Path(payload["path"])
    assert payload["ok"] is True
    assert packet_path.exists()
    assert payload["packet"]["artifact_summary"]["artifact_id"] == artifact_id
    assert json.loads(packet_path.read_text(encoding="utf-8"))["packet_version"] == (
        "entropy-artifact-evidence/v1"
    )


def test_evidence_inspect_prints_safe_summary(tmp_path: Path, monkeypatch) -> None:
    artifact_id = register_fixture(tmp_path, monkeypatch)
    build_result = runner.invoke(cli.app, ["evidence", "build", artifact_id])
    assert build_result.exit_code == 0

    result = runner.invoke(cli.app, ["evidence", "inspect", artifact_id])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["packet"]["artifact_summary"]["artifact_id"] == artifact_id
    assert payload["packet"]["registry_status"]["validation_status"] == "valid"
    assert payload["packet"]["reproducibility_status"] == "not_checked"
    assert "validation_result" not in payload["packet"]


def test_evidence_build_fails_inconsistent_prerequisites(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))
    monkeypatch.setenv("ENTROPY_EVIDENCE_DIR", str(tmp_path / "evidence"))

    result = runner.invoke(cli.app, ["evidence", "build", "artifact-missing"])

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {
        "errors": [
            {
                "code": "artifact_evidence.inconsistent_prerequisites",
                "message": "Evidence packet prerequisites are inconsistent.",
                "path": "$",
                "severity": "P1",
            }
        ],
        "ok": False,
    }


def register_fixture(tmp_path: Path, monkeypatch) -> str:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))
    monkeypatch.setenv("ENTROPY_EVIDENCE_DIR", str(tmp_path / "evidence"))
    result = runner.invoke(cli.app, ["artifact", "register", str(FIXTURES / "valid_artifact.json")])
    assert result.exit_code == 0
    return str(json.loads(result.stdout)["artifact"]["artifact_id"])
