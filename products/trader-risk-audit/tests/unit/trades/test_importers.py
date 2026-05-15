from __future__ import annotations

from pathlib import Path

import pytest

from trader_risk_audit.trades.importers import (
    CsvImportError,
    normalize_csv,
    serialize_trade_records,
)


def test_supported_csv_normalizes_to_canonical_records() -> None:
    records = normalize_csv("tests/fixtures/trades/supported_export.csv")

    assert [
        (record.timestamp.isoformat(), record.source_row_number) for record in records
    ] == [
        ("2026-01-15T09:30:00+00:00", 3),
        ("2026-01-15T10:45:00+00:00", 2),
    ]
    assert [record.symbol for record in records] == ["EURUSD", "GBPUSD"]
    assert [record.side for record in records] == ["buy", "sell"]
    assert {record.source_file for record in records} == {"supported_export.csv"}


def test_missing_source_columns_return_inspected_columns() -> None:
    with pytest.raises(CsvImportError) as error:
        normalize_csv("tests/fixtures/trades/missing_columns_export.csv")

    assert error.value.missing_fields == ("timestamp", "price")
    assert error.value.inspected_columns == ("Ticker", "Action", "Qty", "Account")
    message = str(error.value)
    assert "timestamp" in message
    assert "price" in message
    assert "Ticker" in message


def test_import_output_is_byte_identical_across_runs() -> None:
    fixture = Path("tests/fixtures/trades/supported_export.csv")

    first = serialize_trade_records(normalize_csv(fixture))
    second = serialize_trade_records(normalize_csv(fixture))

    assert first == second
    assert first.encode("utf-8") == second.encode("utf-8")


def test_duplicate_imported_row_ids_are_rejected(tmp_path: Path) -> None:
    fixture = tmp_path / "duplicate_row_ids.csv"
    fixture.write_text(
        "\n".join(
            (
                "row_id,timestamp,symbol,side,quantity,price,fees,account_id",
                "bybit_exec_duplicate,2026-04-01T12:00:00+00:00,BTCUSDT,buy,1,1,0,acct",
                "bybit_exec_duplicate,2026-04-01T12:01:00+00:00,BTCUSDT,sell,1,2,0,acct",
                "",
            )
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate row_id values are not allowed"):
        normalize_csv(fixture)
