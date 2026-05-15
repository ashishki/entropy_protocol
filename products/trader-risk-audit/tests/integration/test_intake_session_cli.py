from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main


def test_intake_session_create_writes_safe_metadata(tmp_path: Path) -> None:
    output_dir = tmp_path / "intake"

    result = main(
        [
            "intake",
            "create",
            "--output-dir",
            str(output_dir),
            "--prospect-label",
            "pilot_export_001",
            "--source-type",
            "csv_export",
            "--source-file",
            str(tmp_path / "private" / "trades.csv"),
            "--risk-rules-file",
            "rules.md",
            "--source-timezone",
            "UTC",
            "--session-start",
            "09:30",
            "--session-end",
            "16:00",
            "--currency",
            "usd",
        ]
    )

    metadata_path = output_dir / "intake_session.json"
    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    serialized = metadata_path.read_text(encoding="utf-8")

    assert result == 0
    assert payload["session_id"].startswith("intake_")
    assert payload["prospect_label"] == "pilot_export_001"
    assert payload["source_type"] == "csv_export"
    assert payload["file_references"] == {
        "risk_rules": "rules.md",
        "source_export": "trades.csv",
    }
    assert payload["source_timezone"] == "UTC"
    assert payload["display_timezone"] == "Europe/Moscow"
    assert payload["session"] == {"start": "09:30", "end": "16:00"}
    assert payload["account_currency"] == "USD"
    assert payload["status"] == "ready_for_schema_profile"
    assert "timestamp,symbol,side,quantity,price" not in serialized
    assert str(tmp_path / "private") not in serialized
