from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main


def test_bundle_summary_is_safe(tmp_path: Path, capsys) -> None:
    run_dir = _write_complete_run(tmp_path)
    limitation_register = run_dir / "unsupported_rules.md"
    limitation_register.write_text(
        "manual_review_required: raw private request marker\n",
        encoding="utf-8",
    )

    result = main(
        [
            "audit-session",
            "bundle",
            "--run-dir",
            str(run_dir),
            "--limitation-register",
            str(limitation_register),
        ]
    )

    stdout = capsys.readouterr().out
    bundle_text = (run_dir / "bundle_index.json").read_text(encoding="utf-8")
    assert result == 0
    assert "Status: complete" in stdout
    assert "Bundle index: bundle_index.json" in stdout
    assert "raw private request marker" not in stdout
    assert "raw_private_row_marker" not in stdout
    assert "raw private request marker" not in bundle_text
    assert "raw_private_row_marker" not in bundle_text


def _write_complete_run(tmp_path: Path) -> Path:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    artifacts = {
        "normalized_trades": "normalized_trades.json",
        "violations": "violations.json",
        "attribution_summary": "attribution_summary.json",
        "report_markdown": "report.md",
        "delivery_packet": "telegram_packet.txt",
        "manifest": "manifest.json",
    }
    for name, ref in artifacts.items():
        content = f"{name}\n"
        if name == "normalized_trades":
            content = "raw_private_row_marker\n"
        (run_dir / ref).write_text(content, encoding="utf-8")
    (run_dir / "run_status.json").write_text(
        json.dumps(
            {
                "artifacts": artifacts,
                "policy_ref": "policy.yaml",
                "reason_code": None,
                "source_export_ref": "trades.csv",
                "status": "complete",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return run_dir
