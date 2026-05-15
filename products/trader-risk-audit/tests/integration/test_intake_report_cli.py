from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.intake import (
    build_intake_session,
    profile_csv_schema,
    write_csv_schema_profile,
    write_intake_session,
)


def test_intake_report_cli_writes_safe_markdown(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    profile_dir = tmp_path / "profile"
    report_dir = tmp_path / "report"
    csv_path = tmp_path / "private" / "customer_export.csv"
    csv_path.parent.mkdir()
    csv_path.write_text(
        "timestamp,symbol,side,quantity,price,comment\n"
        "2026-03-01T10:00:00+00:00,BTCUSDT,buy,1,100,private note\n",
        encoding="utf-8",
    )
    session = build_intake_session(
        prospect_label="safe_label_001",
        source_type="csv_export",
        source_file=csv_path,
        source_timezone="UTC",
        display_timezone="Europe/Moscow",
        session_start="00:00",
        session_end="23:59",
        account_currency="USDT",
        status="ready_for_schema_profile",
    )
    session_path = write_intake_session(session, session_dir)
    profile_path = write_csv_schema_profile(
        profile_csv_schema(
            csv_path,
            intake_session_id=session.session_id,
            source_timezone=session.source_timezone,
            display_timezone=session.display_timezone,
        ),
        profile_dir,
    )

    result = main(
        [
            "intake",
            "report",
            "--session",
            str(session_path),
            "--profile",
            str(profile_path),
            "--output-dir",
            str(report_dir),
        ]
    )

    report_path = report_dir / "intake_report.md"
    text = report_path.read_text(encoding="utf-8")

    assert result == 0
    assert "# Intake Report" in text
    assert "Status: runnable" in text
    assert "- timestamp: timestamp" in text
    assert "- comment" in text
    assert "Privacy: this report contains schema metadata only" in text
    assert "private note" not in text
    assert "BTCUSDT" not in text
    assert str(csv_path.parent) not in text

    payload = json.loads(profile_path.read_text(encoding="utf-8"))
    assert payload["unsupported_columns"] == ["comment"]
