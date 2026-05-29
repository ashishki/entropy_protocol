from __future__ import annotations

import json
import shutil
from pathlib import Path

from trader_risk_audit.cli import main


def test_runner_writes_complete_status(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    session_path = _write_session(input_dir, status="ready_for_audit")

    result = main(
        [
            "audit-session",
            "run",
            "--session",
            str(session_path),
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    status = _read_status(output_dir)
    assert status["status"] == "complete"
    assert status["reason_code"] is None
    assert status["intake_status"] == "ready_for_audit"
    assert status["policy_status"] == "approved"
    assert status["source_export_ref"] == "trades.csv"
    assert status["policy_ref"] == "position_asset_policy.yaml"
    assert status["artifacts"] == {
        "attribution_summary": "attribution_summary.json",
        "delivery_packet": "telegram_packet.txt",
        "manifest": "manifest.json",
        "normalized_trades": "normalized_trades.json",
        "report_markdown": "report.md",
        "violations": "violations.json",
    }
    for artifact_ref in status["artifacts"].values():
        assert (output_dir / artifact_ref).exists()


def test_runner_blocks_unready_inputs(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    intake_blocked_output = tmp_path / "intake_blocked"
    policy_blocked_output = tmp_path / "policy_blocked"
    intake_blocked_session = _write_session(input_dir, status="ready_for_rules")
    ready_session = _write_session(input_dir, status="ready_for_audit")

    intake_result = main(
        [
            "audit-session",
            "run",
            "--session",
            str(intake_blocked_session),
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(intake_blocked_output),
        ]
    )
    policy_result = main(
        [
            "audit-session",
            "run",
            "--session",
            str(ready_session),
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(policy_blocked_output),
            "--policy-status",
            "draft",
        ]
    )

    assert intake_result == 2
    assert policy_result == 2
    assert _read_status(intake_blocked_output)["reason_code"] == "intake_not_ready"
    assert _read_status(policy_blocked_output)["reason_code"] == "policy_not_ready"
    assert not (intake_blocked_output / "report.md").exists()
    assert not (intake_blocked_output / "manifest.json").exists()
    assert not (policy_blocked_output / "report.md").exists()
    assert not (policy_blocked_output / "manifest.json").exists()


def test_runner_status_is_safe(tmp_path: Path, capsys) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    session_path = _write_session(input_dir, status="ready_for_audit")
    private_marker = "private raw trade row credential_marker"
    _append_private_note_column(input_dir / "trades.csv", private_marker)

    result = main(
        [
            "audit-session",
            "run",
            "--session",
            str(session_path),
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ]
    )

    stdout = capsys.readouterr().out
    status_text = (output_dir / "run_status.json").read_text(encoding="utf-8")
    assert result == 0
    assert private_marker not in stdout
    assert private_marker not in status_text
    assert "BTCUSD" not in stdout
    assert "BTCUSD" not in status_text


def _write_session(input_dir: Path, *, status: str) -> Path:
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        "tests/fixtures/trades/attribution_overlap.csv",
        input_dir / "trades.csv",
    )
    session_path = input_dir / f"intake_session_{status}.json"
    session_path.write_text(
        json.dumps(
            {
                "session_id": "intake_test_session",
                "status": status,
                "file_references": {
                    "source_export": "trades.csv",
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return session_path


def _append_private_note_column(csv_path: Path, private_marker: str) -> None:
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    header, *rows = lines
    rewritten = [f"{header},private_note"]
    rewritten.extend(f"{row},{private_marker}" for row in rows)
    csv_path.write_text("\n".join(rewritten) + "\n", encoding="utf-8")


def _read_status(output_dir: Path) -> dict[str, object]:
    return json.loads((output_dir / "run_status.json").read_text(encoding="utf-8"))
