"""Unit tests for artifact registry CLI commands."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli
from entropy.artifacts import ArtifactRegistryEvent

runner = CliRunner()
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"


def test_register_writes_append_only_event(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))

    result = runner.invoke(cli.app, ["artifact", "register", str(FIXTURES / "valid_artifact.json")])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    artifact_id = payload["artifact"]["artifact_id"]
    assert payload["ok"] is True
    assert artifact_id.startswith("artifact-")
    assert payload["event"]["event_type"] == "registered"
    assert payload["event"]["artifact_id"] == artifact_id

    events = (tmp_path / "registry" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    records = (tmp_path / "registry" / "records.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(events) == 1
    assert len(records) == 1
    assert json.loads(events[0])["event_type"] == "registered"


def test_show_prints_safe_metadata(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))
    artifact_path = tmp_path / "private-ref-artifact.json"
    private_marker = "PRIVATE CUSTOMER ROW SECRET_TOKEN_123"
    artifact_path.write_text(
        json.dumps(
            {
                "artifact_contract_version": "entropy-core-artifact/v1",
                "product": "internal-core-fixture",
                "run_id": "run-private-ref",
                "input_refs": [private_marker],
                "input_hashes": ["sha256:input"],
                "policy_config_hash": "sha256:policy",
                "code_version_ref": "git:abcdef123456",
                "generated_artifact_refs": ["reports/internal-fixture.md"],
                "limitations": ["synthetic fixture only"],
                "no_claim_boundary": [
                    "not_production",
                    "not_capital_ready",
                    "not_investment_advice",
                ],
                "manual_validation_status": "not_reviewed",
                "error_register_ref": "error-registers/internal-fixture.md",
                "external_delivery_approval_status": "not_requested",
            }
        ),
        encoding="utf-8",
    )

    register_result = runner.invoke(cli.app, ["artifact", "register", str(artifact_path)])
    artifact_id = json.loads(register_result.stdout)["artifact"]["artifact_id"]
    show_result = runner.invoke(cli.app, ["artifact", "show", artifact_id])

    assert show_result.exit_code == 0
    payload = json.loads(show_result.stdout)
    assert payload["ok"] is True
    assert payload["artifact"]["artifact_id"] == artifact_id
    assert payload["artifact"]["validation_status"] == "valid"
    assert "validation_result" not in payload["artifact"]
    assert "input_refs" not in payload["artifact"]
    assert private_marker not in show_result.stdout
    assert "SECRET_TOKEN_123" not in show_result.stdout


def test_duplicate_registration_is_deterministic(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))

    first = runner.invoke(cli.app, ["artifact", "register", str(FIXTURES / "valid_artifact.json")])
    second = runner.invoke(cli.app, ["artifact", "register", str(FIXTURES / "valid_artifact.json")])

    assert first.exit_code == 0
    assert second.exit_code == 1
    payload = json.loads(second.stdout)
    assert payload == {
        "errors": [
            {
                "code": "artifact_registry.duplicate",
                "message": "Artifact is already registered.",
                "path": "$",
                "severity": "P1",
            }
        ],
        "ok": False,
    }
    assert (
        len((tmp_path / "registry" / "events.jsonl").read_text(encoding="utf-8").splitlines()) == 1
    )


def test_list_prints_safe_summary(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))
    private_marker = "PRIVATE CUSTOMER ROW SECRET_TOKEN_456"
    artifact_path = tmp_path / "private-list-artifact.json"
    artifact_path.write_text(
        json.dumps(
            {
                "artifact_contract_version": "entropy-core-artifact/v1",
                "product": "internal-core-fixture",
                "run_id": "run-private-list",
                "input_refs": [private_marker],
                "input_hashes": ["sha256:input"],
                "policy_config_hash": "sha256:policy",
                "code_version_ref": "git:abcdef123456",
                "generated_artifact_refs": ["reports/internal-fixture.md"],
                "limitations": ["synthetic fixture only"],
                "no_claim_boundary": ["not_production", "not_capital_ready"],
                "manual_validation_status": "not_reviewed",
                "error_register_ref": "error-registers/internal-fixture.md",
                "external_delivery_approval_status": "not_requested",
            }
        ),
        encoding="utf-8",
    )
    register_result = runner.invoke(cli.app, ["artifact", "register", str(artifact_path)])
    artifact_id = json.loads(register_result.stdout)["artifact"]["artifact_id"]

    result = runner.invoke(cli.app, ["artifact", "list"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert [artifact["artifact_id"] for artifact in payload["artifacts"]] == [artifact_id]
    assert payload["artifacts"][0]["product"] == "internal-core-fixture"
    assert payload["artifacts"][0]["source_run_id"] == "run-private-list"
    assert payload["artifacts"][0]["validation_status"] == "valid"
    assert payload["artifacts"][0]["artifact_contract_version"] == "entropy-core-artifact/v1"
    assert "validation_result" not in payload["artifacts"][0]
    assert "input_refs" not in payload["artifacts"][0]
    assert private_marker not in result.stdout
    assert "SECRET_TOKEN_456" not in result.stdout


def test_history_prints_append_only_events(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))
    register_result = runner.invoke(
        cli.app, ["artifact", "register", str(FIXTURES / "valid_artifact.json")]
    )
    artifact_id = json.loads(register_result.stdout)["artifact"]["artifact_id"]
    correction_event = ArtifactRegistryEvent(
        event_id="event-correction-001",
        artifact_id=artifact_id,
        event_type="correction_appended",
        created_at=datetime(2026, 5, 14, 13, 0, tzinfo=UTC),
        actor="core-operator",
        reason="append reviewed correction record",
        new_governance_state="superseded_by_correction",
        correction_record_id="artifact-correction-001",
    )
    with (tmp_path / "registry" / "events.jsonl").open("a", encoding="utf-8") as file:
        file.write(correction_event.model_dump_json() + "\n")

    result = runner.invoke(cli.app, ["artifact", "history", artifact_id])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["artifact_id"] == artifact_id
    assert [event["event_type"] for event in payload["events"]] == [
        "registered",
        "correction_appended",
    ]
    assert payload["events"][1]["correction_record_id"] == "artifact-correction-001"


def test_history_rejects_missing_id(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_REGISTRY_DIR", str(tmp_path / "registry"))

    result = runner.invoke(cli.app, ["artifact", "history", "artifact-missing"])

    assert result.exit_code == 1
    assert json.loads(result.stdout) == {
        "errors": [
            {
                "code": "artifact_registry.not_found",
                "message": "Artifact was not found.",
                "path": "$",
                "severity": "P1",
            }
        ],
        "ok": False,
    }
