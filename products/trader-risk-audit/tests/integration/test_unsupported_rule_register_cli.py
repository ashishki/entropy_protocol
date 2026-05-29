from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_rejects_sensitive_unsupported_rule_text(tmp_path: Path) -> None:
    register_path = tmp_path / "unsupported_rules.md"

    blocked = subprocess.run(
        [
            sys.executable,
            "-m",
            "trader_risk_audit",
            "policy",
            "unsupported",
            "append",
            "--register",
            str(register_path),
            "--reason",
            "free_text_rule",
            "--text",
            "please store this api key value",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert blocked.returncode == 2
    assert not register_path.exists()
    assert "credentials, handles, or private notes" in blocked.stdout
    assert "api key value" not in blocked.stdout

    accepted = subprocess.run(
        [
            sys.executable,
            "-m",
            "trader_risk_audit",
            "policy",
            "unsupported",
            "append",
            "--register",
            str(register_path),
            "--reason",
            "free_text_rule",
            "--text",
            "Track revenge trading after market news",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    register_text = register_path.read_text(encoding="utf-8")
    assert accepted.returncode == 0
    assert accepted.stdout == f"unsupported rule registered: {register_path}\n"
    assert "Track revenge trading after market news" in register_text
    assert "manual_review_required" in register_text
