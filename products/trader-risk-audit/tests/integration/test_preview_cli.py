from __future__ import annotations

import json
import shutil
from pathlib import Path

from trader_risk_audit.audit_session.artifact_bundle import (
    build_artifact_bundle_index,
    write_artifact_bundle_index,
)
from trader_risk_audit.audit_session.runner import run_audit_session
from trader_risk_audit.cli import main


def test_preview_cli_writes_markdown(tmp_path: Path, capsys) -> None:
    input_dir = tmp_path / "input"
    run_dir = tmp_path / "run"
    output_dir = tmp_path / "preview"
    session_path = _write_session(input_dir)
    run_audit_session(
        session_path=session_path,
        policy_path="tests/fixtures/policies/position_asset_policy.yaml",
        input_dir=input_dir,
        output_dir=run_dir,
    )
    bundle = build_artifact_bundle_index(run_dir=run_dir)
    bundle_path = write_artifact_bundle_index(bundle, run_dir / "bundle_index.json")

    result = main(
        [
            "preview",
            "build",
            "--bundle",
            str(bundle_path),
            "--output-dir",
            str(output_dir),
        ]
    )

    stdout = capsys.readouterr().out
    preview_text = (output_dir / "preview.md").read_text(encoding="utf-8")
    assert result == 0
    assert "wrote preview:" in stdout
    assert "# Audit Preview" in preview_text
    assert "This audit is not investment advice" in preview_text
    assert "trade_" not in preview_text
    assert "BTCUSD" not in preview_text


def _write_session(input_dir: Path) -> Path:
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        "tests/fixtures/trades/attribution_overlap.csv",
        input_dir / "trades.csv",
    )
    session_path = input_dir / "intake_session.json"
    session_path.write_text(
        json.dumps(
            {
                "file_references": {
                    "source_export": "trades.csv",
                },
                "status": "ready_for_audit",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return session_path
