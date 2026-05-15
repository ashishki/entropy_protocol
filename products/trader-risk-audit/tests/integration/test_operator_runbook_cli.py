from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main


def test_operator_prepare_shows_safe_next_action(
    tmp_path: Path,
    capsys,
) -> None:
    queue_file = tmp_path / "queue.json"
    workspace_root = tmp_path / "workspaces"

    result = main(
        [
            "operator",
            "prepare",
            "--queue-file",
            str(queue_file),
            "--workspace-root",
            str(workspace_root),
            "--audit-id",
            "audit_operator_001",
            "--trades",
            "tests/fixtures/pilot/trades.csv",
            "--policy",
            "tests/fixtures/pilot/policy.yaml",
            "--profile",
            "hard",
        ]
    )
    output = capsys.readouterr().out.casefold()
    queue = json.loads(queue_file.read_text(encoding="utf-8"))

    assert result == 0
    assert "status: ready_to_run" in output
    assert "selected policy profile: hard" in output
    assert "next action: operator run" in output
    assert "input/trades.csv" in output
    assert "timestamp,symbol,side,quantity,price" not in output
    assert queue["requests"]["audit_operator_001"]["status"] == "ready_to_run"


def test_operator_run_registers_audit_outputs(tmp_path: Path, capsys) -> None:
    queue_file = tmp_path / "queue.json"
    workspace_root = tmp_path / "workspaces"
    assert (
        main(
            [
                "operator",
                "prepare",
                "--queue-file",
                str(queue_file),
                "--workspace-root",
                str(workspace_root),
                "--audit-id",
                "audit_operator_002",
                "--trades",
                "tests/fixtures/pilot/trades.csv",
                "--policy",
                "tests/fixtures/pilot/policy.yaml",
                "--profile",
                "medium",
            ]
        )
        == 0
    )
    capsys.readouterr()

    result = main(
        [
            "operator",
            "run",
            "--queue-file",
            str(queue_file),
            "--workspace-root",
            str(workspace_root),
            "--audit-id",
            "audit_operator_002",
        ]
    )
    output = capsys.readouterr().out.casefold()
    queue = json.loads(queue_file.read_text(encoding="utf-8"))
    request = queue["requests"]["audit_operator_002"]
    output_dir = workspace_root / "audit_operator_002" / "output"

    assert result == 0
    assert request["status"] == "ready_for_review"
    assert request["file_references"]["report_markdown"] == "output/report.md"
    assert request["file_references"]["delivery_packet"] == "output/telegram_packet.txt"
    assert request["file_references"]["manifest"] == "output/manifest.json"
    assert (output_dir / "report.md").exists()
    assert (output_dir / "telegram_packet.txt").exists()
    assert (output_dir / "manifest.json").exists()
    assert "status: ready_for_review" in output


def test_operator_runbook_cli_is_local_first() -> None:
    text = Path("docs/AUDIT_WORKSPACE_RUNBOOK_RU.md").read_text(encoding="utf-8")

    required_boundaries = (
        "no database",
        "hosted queue",
        "background workers",
        "network services",
        "raw trade rows",
    )
    lowered = text.casefold()
    for phrase in required_boundaries:
        assert phrase in lowered
