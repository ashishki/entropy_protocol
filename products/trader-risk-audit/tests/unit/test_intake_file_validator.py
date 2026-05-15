from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.intake import (
    MAX_INTAKE_FILE_BYTES,
    IntakeFile,
    validate_intake_files,
)
from trader_risk_audit.policy.profiles import resolve_policy_profile
from trader_risk_audit.workspace import create_audit_workspace


def test_validator_reports_actionable_errors_without_raw_rows() -> None:
    raw_rows = (
        "timestamp,symbol,side,quantity\n2026-03-01T10:00:00+00:00,EURUSD,hold,1\n"
    )
    result = validate_intake_files(
        (
            IntakeFile("trades.csv", raw_rows.encode("utf-8")),
            IntakeFile("notes.exe", b"not allowed"),
            IntakeFile("huge.csv", b"0" * (MAX_INTAKE_FILE_BYTES + 1)),
        ),
        selected_profile=None,
    )
    feedback = result.safe_feedback().casefold()

    assert result.status == "needs_user_fix"
    assert "select soft, medium, hard, or custom policy profile" in feedback
    assert "missing canonical fields: price" in feedback
    assert "unsupported file type" in feedback
    assert "file exceeds size limit" in feedback
    assert "2026-03-01t10:00:00+00:00,eurusd,hold,1" not in feedback
    assert "timestamp,symbol,side,quantity" not in feedback


def test_custom_profile_requires_policy_file() -> None:
    result = validate_intake_files(
        (
            IntakeFile(
                "trades.csv",
                b"timestamp,symbol,side,quantity,price,account_id\n"
                b"2026-03-01T10:00:00+00:00,EURUSD,buy,1,100,acct_demo\n",
            ),
        ),
        selected_profile="custom",
    )

    assert result.status == "needs_user_fix"
    assert "custom profile requires written risk rules" in result.safe_feedback()


def test_valid_intake_can_be_marked_operator_ready(tmp_path: Path) -> None:
    selection = resolve_policy_profile("hard")
    result = validate_intake_files(
        (
            IntakeFile(
                "trades.csv",
                b"timestamp,symbol,side,quantity,price,account_id\n"
                b"2026-03-01T10:00:00+00:00,EURUSD,buy,1,100,acct_demo\n",
            ),
        ),
        selected_profile=selection.selected_profile,
    )
    workspace = create_audit_workspace(
        tmp_path,
        "audit_ready_001",
        status=result.status,
        file_references={"trades_export": "input/trades.csv"},
        policy_profile=selection,
    )
    metadata = json.loads(workspace.metadata_path.read_text(encoding="utf-8"))

    assert result.is_operator_ready
    assert metadata["status"] == "operator_ready"
    assert metadata["policy_profile"]["selected_profile"] == "hard"
    assert workspace.root == tmp_path / "audit_ready_001"
