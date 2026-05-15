"""Unit tests for artifact governance CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli

runner = CliRunner()


def test_transition_records_append_only_event(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_GOVERNANCE_DIR", str(tmp_path / "governance"))

    first = runner.invoke(
        cli.app,
        ["governance", "transition", "artifact-001", "--to", "validated_internal"],
    )
    second = runner.invoke(
        cli.app,
        ["governance", "transition", "artifact-001", "--to", "blocked"],
    )

    assert first.exit_code == 0
    assert second.exit_code == 0
    first_payload = json.loads(first.stdout)
    second_payload = json.loads(second.stdout)
    assert first_payload["event"]["prior_state"] == "draft"
    assert first_payload["event"]["next_state"] == "validated_internal"
    assert second_payload["event"]["prior_state"] == "validated_internal"
    assert second_payload["event"]["prior_event_id"] == first_payload["event"]["event_id"]
    assert (tmp_path / "governance" / "events.jsonl").read_text(encoding="utf-8").count("\n") == 2


def test_invalid_transition_fails_before_write(tmp_path: Path, monkeypatch) -> None:
    governance_dir = tmp_path / "governance"
    monkeypatch.setenv("ENTROPY_GOVERNANCE_DIR", str(governance_dir))

    result = runner.invoke(
        cli.app,
        ["governance", "transition", "artifact-001", "--to", "approved_for_controlled_external_pilot"],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload == {
        "errors": [
            {
                "code": "artifact_governance.invalid_transition",
                "message": "Artifact governance transition is not allowed.",
                "path": "$",
                "severity": "P1",
            }
        ],
        "ok": False,
    }
    assert not (governance_dir / "events.jsonl").exists()


def test_history_prints_deterministic_transitions(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ENTROPY_GOVERNANCE_DIR", str(tmp_path / "governance"))
    first = runner.invoke(
        cli.app,
        ["governance", "transition", "artifact-001", "--to", "validated_internal"],
    )
    assert first.exit_code == 0
    second = runner.invoke(
        cli.app,
        [
            "governance",
            "transition",
            "artifact-001",
            "--to",
            "approved_for_controlled_external_pilot",
            "--approval-event-ref",
            "approval-event-001",
        ],
    )
    assert second.exit_code == 0

    result = runner.invoke(cli.app, ["governance", "history", "artifact-001"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert [event["next_state"] for event in payload["events"]] == [
        "validated_internal",
        "approved_for_controlled_external_pilot",
    ]
    assert payload["events"][1]["approval_event_ref"] == "approval-event-001"
