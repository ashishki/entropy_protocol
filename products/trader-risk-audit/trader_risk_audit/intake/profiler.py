from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from trader_risk_audit.trades.importers import (
    REQUIRED_CANONICAL_FIELDS,
    build_trade_column_map,
)

_OFFSET_PATTERN = re.compile(r"(Z|[+-][0-2][0-9]:?[0-5][0-9])$")
_LEVERAGE_ALIASES = frozenset({"leverage", "margin", "margin_mode"})
_PNL_ALIASES = frozenset(
    {
        "pnl",
        "p&l",
        "realized_pnl",
        "realised_pnl",
        "profit",
        "profit_loss",
    }
)


@dataclass(frozen=True)
class CsvSchemaProfile:
    intake_session_id: str
    source_file: str
    inspected_columns: tuple[str, ...]
    canonical_field_map: dict[str, str]
    missing_required_fields: tuple[str, ...]
    row_count: int
    duplicate_row_id_risk: bool
    timestamp_timezone: str
    source_timezone: str
    display_timezone: str
    fee_available: bool
    leverage_available: bool
    pnl_available: bool
    unsupported_columns: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def profile_csv_schema(
    csv_path: str | Path,
    *,
    intake_session_id: str,
    source_timezone: str,
    display_timezone: str,
) -> CsvSchemaProfile:
    source_path = Path(csv_path)
    with source_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = tuple(reader.fieldnames or ())
        column_map = build_trade_column_map(fieldnames)
        rows = list(reader)

    missing_required_fields = tuple(
        field for field in REQUIRED_CANONICAL_FIELDS if field not in column_map
    )
    unsupported_columns = _unsupported_columns(fieldnames, column_map)
    row_ids = _column_values(rows, column_map.get("row_id"))
    return CsvSchemaProfile(
        intake_session_id=intake_session_id,
        source_file=source_path.name,
        inspected_columns=fieldnames,
        canonical_field_map=dict(sorted(column_map.items())),
        missing_required_fields=missing_required_fields,
        row_count=len(rows),
        duplicate_row_id_risk=_has_duplicate_or_blank_row_ids(row_ids),
        timestamp_timezone=_timestamp_timezone_coverage(
            _column_values(rows, column_map.get("timestamp"))
        ),
        source_timezone=source_timezone,
        display_timezone=display_timezone,
        fee_available="fees" in column_map,
        leverage_available=_has_alias(fieldnames, _LEVERAGE_ALIASES),
        pnl_available=_has_alias(fieldnames, _PNL_ALIASES),
        unsupported_columns=unsupported_columns,
    )


def write_csv_schema_profile(profile: CsvSchemaProfile, output_dir: str | Path) -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / "schema_profile.json"
    output_path.write_text(profile.to_json(), encoding="utf-8")
    return output_path


def _unsupported_columns(
    fieldnames: tuple[str, ...],
    column_map: dict[str, str],
) -> tuple[str, ...]:
    mapped = set(column_map.values())
    return tuple(column for column in fieldnames if column not in mapped)


def _column_values(rows: list[dict[str, str]], column: str | None) -> tuple[str, ...]:
    if column is None:
        return ()
    return tuple(str(row.get(column, "")).strip() for row in rows)


def _has_duplicate_or_blank_row_ids(values: tuple[str, ...]) -> bool:
    if not values:
        return False
    if any(not value for value in values):
        return True
    return len(set(values)) != len(values)


def _timestamp_timezone_coverage(values: tuple[str, ...]) -> str:
    if not values:
        return "not_mapped"
    aware_count = sum(1 for value in values if _OFFSET_PATTERN.search(value))
    if aware_count == len(values):
        return "timezone_aware"
    if aware_count == 0:
        return "timezone_missing"
    return "mixed"


def _has_alias(fieldnames: tuple[str, ...], aliases: frozenset[str]) -> bool:
    normalized = {_normalize_column(fieldname) for fieldname in fieldnames}
    return bool(normalized & {_normalize_column(alias) for alias in aliases})


def profile_from_intake_session(
    csv_path: str | Path,
    session_payload: dict[str, Any],
) -> CsvSchemaProfile:
    return profile_csv_schema(
        csv_path,
        intake_session_id=str(session_payload["session_id"]),
        source_timezone=str(session_payload["source_timezone"]),
        display_timezone=str(session_payload["display_timezone"]),
    )


def _normalize_column(column: str) -> str:
    return column.strip().casefold().replace("-", "_").replace(" ", "_")
