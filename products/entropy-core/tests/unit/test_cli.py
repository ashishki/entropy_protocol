"""Unit tests for CLI commands."""

from __future__ import annotations

import json

from typer.testing import CliRunner

from entropy import cli

runner = CliRunner()


def test_health_command_ok(monkeypatch) -> None:
    monkeypatch.setattr(cli, "check_postgres", lambda: {"name": "postgres", "status": "ok"})
    monkeypatch.setattr(cli, "check_duckdb", lambda: {"name": "duckdb", "status": "ok"})

    result = runner.invoke(cli.app, ["health"])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"status": "ok"}


def test_health_command_degraded_no_postgres(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(cli, "check_duckdb", lambda: {"name": "duckdb", "status": "ok"})

    result = runner.invoke(cli.app, ["health"])
    payload = json.loads(result.stdout)

    assert result.exit_code == 1
    assert payload["status"] == "degraded"
    assert payload["checks"] == [
        {"name": "postgres", "status": "fail", "error": "DATABASE_URL is not set"}
    ]


def test_health_command_output_is_valid_json(monkeypatch) -> None:
    monkeypatch.setattr(cli, "check_postgres", lambda: {"name": "postgres", "status": "ok"})
    monkeypatch.setattr(cli, "check_duckdb", lambda: {"name": "duckdb", "status": "ok"})

    result = runner.invoke(cli.app, ["health"])
    payload = json.loads(result.stdout)

    assert "status" in payload
