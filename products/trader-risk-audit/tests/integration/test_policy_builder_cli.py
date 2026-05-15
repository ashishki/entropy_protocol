from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from trader_risk_audit.policy.schema import load_policy


def test_policy_builder_cli_writes_yaml(tmp_path: Path) -> None:
    session_path = tmp_path / "intake_session.json"
    output_dir = tmp_path / "out"
    session_path.write_text(
        json.dumps(
            {
                "source_timezone": "UTC",
                "session": {
                    "start": "07:00",
                    "end": "16:00",
                },
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trader_risk_audit",
            "policy",
            "build",
            "--session",
            str(session_path),
            "--profile",
            "hard",
            "--account-id",
            "acct_cli_001",
            "--output-dir",
            str(output_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    policy_path = output_dir / "policy.yaml"
    assert result.returncode == 0
    assert result.stdout == f"wrote generated policy: {policy_path}\n"
    first_output = policy_path.read_text(encoding="utf-8")

    second_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trader_risk_audit",
            "policy",
            "build",
            "--session",
            str(session_path),
            "--profile",
            "hard",
            "--account-id",
            "acct_cli_001",
            "--output-dir",
            str(output_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    policy = load_policy(policy_path)

    assert second_result.returncode == 0
    assert policy_path.read_text(encoding="utf-8") == first_output
    assert policy.account_scope == ("acct_cli_001",)
    assert policy.timezone == "UTC"
    assert policy.session.start == "07:00"
    assert policy.session.end == "16:00"
    assert policy.rules[0].rule_id == "starter_hard_max_daily_loss"
