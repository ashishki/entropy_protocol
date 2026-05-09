from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from trader_risk_audit.workspace import create_audit_workspace


def test_workspace_layout_creates_expected_directories(tmp_path: Path) -> None:
    workspace = create_audit_workspace(tmp_path, "audit_demo_001")

    assert workspace.root == tmp_path / "audit_demo_001"
    assert workspace.input_dir.is_dir()
    assert workspace.output_dir.is_dir()
    assert workspace.operator_notes_dir.is_dir()
    assert workspace.artifacts_dir.is_dir()
    assert workspace.metadata_path.exists()


def test_workspace_metadata_omits_raw_trade_data(tmp_path: Path) -> None:
    workspace = create_audit_workspace(
        tmp_path,
        "audit_demo_002",
        created_at=datetime(2026, 5, 7, 12, 0, tzinfo=UTC),
        status="ready_to_run",
        file_references={
            "trades_export": "input/trades.csv",
            "risk_rules": "input/risk_rules.md",
            "absolute_report": tmp_path / "pilot" / "output" / "report.md",
        },
    )

    metadata_text = workspace.metadata_path.read_text(encoding="utf-8")
    metadata = json.loads(metadata_text)

    assert metadata == {
        "audit_id": "audit_demo_002",
        "created_at": "2026-05-07T12:00:00+00:00",
        "file_references": {
            "absolute_report": "report.md",
            "risk_rules": "input/risk_rules.md",
            "trades_export": "input/trades.csv",
        },
        "status": "ready_to_run",
    }
    assert "timestamp,symbol,side,quantity,price" not in metadata_text
    assert "buy,1,100" not in metadata_text

    with pytest.raises(ValueError, match="single line"):
        create_audit_workspace(
            tmp_path,
            "audit_demo_003",
            file_references={
                "raw_rows": (
                    "timestamp,symbol,side,quantity,price\n2026-01-01,BTC,buy,1,100"
                )
            },
        )


def test_workspace_runbook_documents_required_layout() -> None:
    text = (
        Path("docs/AUDIT_WORKSPACE_RUNBOOK_RU.md")
        .read_text(encoding="utf-8")
        .casefold()
    )

    required_phrases = (
        "input/",
        "output/",
        "operator_notes/",
        "artifacts/",
        "metadata.json",
        "manual handoff",
        "intake request",
        "audit workflow",
        "no database",
        "no network dependency",
        "raw trade rows",
    )
    for phrase in required_phrases:
        assert phrase in text
