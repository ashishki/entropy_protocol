from __future__ import annotations

from pathlib import Path

from trader_risk_audit.intake import profile_csv_schema


def test_csv_profiler_maps_aliases_and_missing_fields(tmp_path: Path) -> None:
    csv_path = tmp_path / "export.csv"
    csv_path.write_text(
        "time,ticker,action,qty,fill_price,desk_note\n"
        "2026-03-01T10:00:00+00:00,BTCUSDT,buy,1,100,private raw note\n",
        encoding="utf-8",
    )

    profile = profile_csv_schema(
        csv_path,
        intake_session_id="intake_demo_001",
        source_timezone="UTC",
        display_timezone="Europe/Moscow",
    )
    serialized = profile.to_json()

    assert profile.canonical_field_map == {
        "price": "fill_price",
        "quantity": "qty",
        "side": "action",
        "symbol": "ticker",
        "timestamp": "time",
    }
    assert profile.missing_required_fields == ()
    assert profile.unsupported_columns == ("desk_note",)
    assert "private raw note" not in serialized
    assert "BTCUSDT" not in serialized
    assert "2026-03-01T10:00:00+00:00" not in serialized


def test_csv_profiler_reports_coverage(tmp_path: Path) -> None:
    csv_path = tmp_path / "coverage.csv"
    csv_path.write_text(
        "timestamp,symbol,side,quantity,price,fees,row_id,leverage,realized_pnl,"
        "strategy\n"
        "2026-03-01T10:00:00,BTCUSDT,buy,1,100,0,row-1,2,10,breakout\n"
        "2026-03-01T11:00:00,ETHUSDT,sell,2,200,1,row-1,3,-5,mean_revert\n",
        encoding="utf-8",
    )

    profile = profile_csv_schema(
        csv_path,
        intake_session_id="intake_demo_001",
        source_timezone="UTC",
        display_timezone="Europe/Moscow",
    )

    assert profile.row_count == 2
    assert profile.duplicate_row_id_risk is True
    assert profile.timestamp_timezone == "timezone_missing"
    assert profile.fee_available is True
    assert profile.leverage_available is True
    assert profile.pnl_available is True
    assert profile.unsupported_columns == ("leverage", "realized_pnl", "strategy")
