"""Unit tests for artifact validation CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli

runner = CliRunner()
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"


def test_artifact_validate_accepts_valid_artifact() -> None:
    result = runner.invoke(cli.app, ["artifact", "validate", str(FIXTURES / "valid_artifact.json")])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["errors"] == []
    assert payload["artifact"]["artifact_contract_version"] == "entropy-core-artifact/v1"


def test_artifact_validate_rejects_invalid_artifact() -> None:
    result = runner.invoke(
        cli.app, ["artifact", "validate", str(FIXTURES / "invalid_artifact.json")]
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    error_codes = {error["code"] for error in payload["errors"]}
    assert payload["ok"] is False
    assert "artifact.invalid_state" in error_codes
    assert "artifact.extra_field" in error_codes


def test_artifact_cli_help_preserves_existing_commands() -> None:
    result = runner.invoke(cli.app, ["--help"])

    assert result.exit_code == 0
    assert "artifact" in result.stdout
    assert "health" in result.stdout
    assert "version" in result.stdout
