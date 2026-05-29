from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.intake import build_intake_session, write_intake_session


def test_intake_profile_writes_schema_summary(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    output_dir = tmp_path / "profile"
    csv_path = tmp_path / "private" / "prospect_export.csv"
    csv_path.parent.mkdir()
    csv_path.write_text(
        "executed_at,instrument,side,size,execution_price,commission,comment\n"
        "2026-03-01T10:00:00+00:00,BTCUSDT,buy,1,100,0,raw comment\n",
        encoding="utf-8",
    )
    session_path = write_intake_session(
        build_intake_session(
            prospect_label="profile_cli_001",
            source_type="csv_export",
            source_file=csv_path,
            source_timezone="UTC",
            display_timezone="Europe/Moscow",
            session_start="00:00",
            session_end="23:59",
            account_currency="USDT",
            status="ready_for_schema_profile",
        ),
        session_dir,
    )

    result = main(
        [
            "intake",
            "profile",
            "--session",
            str(session_path),
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
        ]
    )

    profile_path = output_dir / "schema_profile.json"
    payload = json.loads(profile_path.read_text(encoding="utf-8"))
    serialized = profile_path.read_text(encoding="utf-8")

    assert result == 0
    assert payload["source_file"] == "prospect_export.csv"
    assert payload["canonical_field_map"] == {
        "fees": "commission",
        "price": "execution_price",
        "quantity": "size",
        "side": "side",
        "symbol": "instrument",
        "timestamp": "executed_at",
    }
    assert payload["missing_required_fields"] == []
    assert payload["row_count"] == 1
    assert payload["timestamp_timezone"] == "timezone_aware"
    assert payload["display_timezone"] == "Europe/Moscow"
    assert payload["unsupported_columns"] == ["comment"]
    assert "raw comment" not in serialized
    assert str(csv_path.parent) not in serialized
