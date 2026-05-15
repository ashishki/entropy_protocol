from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from trader_risk_audit.trades.schema import TradeRecord

REQUIRED_CANONICAL_FIELDS = ("timestamp", "symbol", "side", "quantity", "price")
TRADE_COLUMN_ALIASES: Mapping[str, tuple[str, ...]] = {
    "timestamp": ("timestamp", "time", "executed_at", "executed at"),
    "symbol": ("symbol", "ticker", "instrument"),
    "side": ("side", "action"),
    "quantity": ("quantity", "qty", "size"),
    "price": ("price", "fill_price", "fill price", "execution_price"),
    "fees": ("fees", "fee", "commission"),
    "account_id": ("account_id", "account", "account id"),
    "row_id": ("row_id", "source_row_id", "source row id"),
}


@dataclass(frozen=True)
class CsvImportError(ValueError):
    missing_fields: tuple[str, ...]
    inspected_columns: tuple[str, ...]

    def __str__(self) -> str:
        missing = ", ".join(self.missing_fields)
        inspected = ", ".join(self.inspected_columns)
        return f"missing canonical fields: {missing}; inspected columns: {inspected}"


def normalize_csv(path: str | Path) -> tuple[TradeRecord, ...]:
    source_path = Path(path)
    with source_path.open(newline="", encoding="utf-8") as trade_file:
        reader = csv.DictReader(trade_file)
        fieldnames = tuple(reader.fieldnames or ())
        column_map = _build_column_map(fieldnames)
        missing = tuple(
            field for field in REQUIRED_CANONICAL_FIELDS if field not in column_map
        )
        if missing:
            raise CsvImportError(
                missing_fields=missing,
                inspected_columns=fieldnames,
            )

        records = [
            TradeRecord.from_mapping(
                _canonical_row(row, column_map, source_path.name, source_row_number)
            )
            for source_row_number, row in enumerate(reader, start=2)
        ]
        _ensure_unique_row_ids(records)

    return tuple(
        sorted(
            records,
            key=lambda record: (record.timestamp, record.source_row_number),
        )
    )


def serialize_trade_records(records: Iterable[TradeRecord]) -> str:
    payload = [_trade_record_to_payload(record) for record in records]
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def build_trade_column_map(fieldnames: Iterable[str]) -> dict[str, str]:
    normalized_to_source = {_normalize_column(name): name for name in fieldnames}
    column_map: dict[str, str] = {}
    for canonical_field, aliases in TRADE_COLUMN_ALIASES.items():
        for alias in aliases:
            source_column = normalized_to_source.get(_normalize_column(alias))
            if source_column is not None:
                column_map[canonical_field] = source_column
                break
    return column_map


def _build_column_map(fieldnames: Iterable[str]) -> dict[str, str]:
    return build_trade_column_map(fieldnames)


def _normalize_column(column: str) -> str:
    return column.strip().casefold().replace("-", "_").replace(" ", "_")


def _canonical_row(
    row: Mapping[str, str],
    column_map: Mapping[str, str],
    source_file: str,
    source_row_number: int,
) -> dict[str, str | int]:
    canonical = {
        field: row[source_column]
        for field, source_column in column_map.items()
        if source_column in row
    }
    canonical.setdefault("fees", "0")
    canonical["source_file"] = source_file
    canonical["source_row_number"] = source_row_number
    return canonical


def _ensure_unique_row_ids(records: Iterable[TradeRecord]) -> None:
    seen: set[str] = set()
    for record in records:
        if record.row_id in seen:
            raise ValueError("duplicate row_id values are not allowed")
        seen.add(record.row_id)


def _trade_record_to_payload(record: TradeRecord) -> dict[str, Any]:
    return {
        "account_id": record.account_id,
        "fees": _serialize_decimal(record.fees),
        "price": _serialize_decimal(record.price),
        "quantity": _serialize_decimal(record.quantity),
        "row_id": record.row_id,
        "side": record.side,
        "source_file": record.source_file,
        "source_row_number": record.source_row_number,
        "symbol": record.symbol,
        "timestamp": _serialize_datetime(record.timestamp),
    }


def _serialize_decimal(value: Decimal) -> str:
    return format(value.normalize(), "f")


def _serialize_datetime(value: datetime) -> str:
    return value.isoformat()
