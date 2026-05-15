from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from trader_risk_audit.policy.schema import load_policy


def test_rule_builder_noninteractive(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trader_risk_audit",
            "policy",
            "flow",
            "--profile",
            "medium",
            "--account-id",
            "acct_flow_001",
            "--source-timezone",
            "UTC",
            "--session-start",
            "08:00",
            "--session-end",
            "17:00",
            "--threshold",
            "max_daily_loss=1500:USD",
            "--output-dir",
            str(output_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    policy_path = output_dir / "policy.yaml"
    policy = load_policy(policy_path)
    daily_loss = next(rule for rule in policy.rules if rule.type == "max_daily_loss")

    assert result.returncode == 0
    assert result.stdout == f"wrote generated policy: {policy_path}\n"
    assert policy.account_scope == ("acct_flow_001",)
    assert policy.timezone == "UTC"
    assert policy.session.start == "08:00"
    assert policy.session.end == "17:00"
    assert daily_loss.threshold == 1500


def test_rule_builder_interactive_safe_output(tmp_path: Path) -> None:
    output_dir = tmp_path / "interactive"
    stdin = "\n".join(
        (
            "soft",
            "acct_interactive_001",
            "UTC",
            "09:00",
            "18:00",
            "private raw trade row credential_marker telegram_handle_marker",
        )
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trader_risk_audit",
            "policy",
            "flow",
            "--interactive",
            "--output-dir",
            str(output_dir),
        ],
        input=stdin,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "wrote generated policy:" in result.stdout
    assert "private raw trade row" not in result.stdout
    assert "credential_marker" not in result.stdout
    assert "telegram_handle_marker" not in result.stdout
    assert load_policy(output_dir / "policy.yaml").account_scope == (
        "acct_interactive_001",
    )


def test_rule_builder_flow_reports_unavailable_rules(tmp_path: Path) -> None:
    profile_path = tmp_path / "schema_profile.json"
    profile_path.write_text(
        json.dumps(
            {
                "missing_required_fields": (),
                "fee_available": False,
                "leverage_available": False,
                "pnl_available": False,
                "account_balance_available": False,
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
            "flow",
            "--profile",
            "hard",
            "--account-id",
            "acct_flow_002",
            "--source-timezone",
            "UTC",
            "--session-start",
            "08:00",
            "--session-end",
            "17:00",
            "--schema-profile",
            str(profile_path),
            "--output-dir",
            str(tmp_path / "out"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Unavailable rules:" in result.stdout
    assert "max_daily_loss: unavailable because pnl_available, fee_available" in (
        result.stdout
    )
    assert "manual review" in result.stdout
