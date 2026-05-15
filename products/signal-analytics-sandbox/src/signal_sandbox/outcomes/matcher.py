"""Deterministic signal outcome matching."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from decimal import ROUND_HALF_EVEN, Decimal
from enum import StrEnum
from io import BytesIO
from pathlib import Path
from typing import Any

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.ledger.record import Direction, SignalRecord, compute_dedup_key
from signal_sandbox.outcomes.rule_registry import (
    EXCLUDED_AMBIGUOUS_RULE_ID,
    EXCLUDED_NO_PRICE_RULE_ID,
    LONG_TARGET_STOP_RULE_ID,
    RULE_REGISTRY_VERSION,
    RULES,
)
from signal_sandbox.prices.base import OHLCV_COLUMNS, PriceSnapshot

ROUNDING_QUANT = Decimal("0.000001")


class Outcome(StrEnum):
    TARGET_HIT = "target_hit"
    STOP_HIT = "stop_hit"
    TIMEOUT_NO_HIT = "timeout_no_hit"
    EXCLUDED_AMBIGUOUS = "excluded_ambiguous"
    EXCLUDED_NO_PRICE = "excluded_no_price"


class OutcomeRecord(BaseModel):
    model_config = ConfigDict(strict=True)

    dedup_key: str = Field(min_length=64, max_length=64)
    source_id: str = Field(min_length=1)
    asset_symbol: str = Field(min_length=1)
    extracted_timestamp_utc: datetime
    outcome: Outcome
    entry_fill_timestamp: datetime | None = None
    exit_timestamp: datetime | None = None
    return_pct: Decimal | None = None
    mae_pct: Decimal | None = None
    mfe_pct: Decimal | None = None
    outcome_rule_id: str = Field(min_length=1)
    snapshot_sha256: str = Field(min_length=64, max_length=64)

    @field_validator(
        "extracted_timestamp_utc",
        "entry_fill_timestamp",
        "exit_timestamp",
        mode="before",
    )
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")

    @field_validator("outcome", mode="before")
    @classmethod
    def _coerce_outcome(cls, value: object) -> Outcome:
        if isinstance(value, Outcome):
            return value
        if isinstance(value, str):
            return Outcome(value)
        raise ValueError("outcome must be an Outcome or string")

    @model_validator(mode="after")
    def _validate_rule_id(self) -> OutcomeRecord:
        assert_known_rule(self.outcome_rule_id)
        return self


OUTCOME_COLUMNS = [
    "dedup_key",
    "source_id",
    "asset_symbol",
    "extracted_timestamp_utc",
    "outcome",
    "entry_fill_timestamp",
    "exit_timestamp",
    "return_pct",
    "mae_pct",
    "mfe_pct",
    "outcome_rule_id",
    "snapshot_sha256",
]

OUTCOME_SCHEMA = {
    "dedup_key": pl.String,
    "source_id": pl.String,
    "asset_symbol": pl.String,
    "extracted_timestamp_utc": pl.String,
    "outcome": pl.String,
    "entry_fill_timestamp": pl.String,
    "exit_timestamp": pl.String,
    "return_pct": pl.Float64,
    "mae_pct": pl.Float64,
    "mfe_pct": pl.Float64,
    "outcome_rule_id": pl.String,
    "snapshot_sha256": pl.String,
}


def match_outcomes(
    records: Sequence[SignalRecord],
    snapshot: PriceSnapshot,
) -> list[OutcomeRecord]:
    price_rows = _price_rows_by_asset(snapshot)
    outcomes = [_match_record(record, snapshot, price_rows) for record in records]
    outcomes.sort(
        key=lambda row: (row.extracted_timestamp_utc.isoformat(), row.dedup_key)
    )
    return outcomes


def outcomes_parquet_bytes(outcomes: Sequence[OutcomeRecord]) -> bytes:
    rows = [_outcome_to_row(outcome) for outcome in outcomes]
    rows.sort(key=lambda row: (row["extracted_timestamp_utc"], row["dedup_key"]))
    frame = pl.DataFrame(rows, schema=OUTCOME_SCHEMA) if rows else _empty_frame()

    buffer = BytesIO()
    frame.select(OUTCOME_COLUMNS).write_parquet(
        buffer,
        compression="zstd",
        statistics=False,
        metadata={"rule_registry_version": RULE_REGISTRY_VERSION},
    )
    return buffer.getvalue()


def write_outcomes(outcomes: Sequence[OutcomeRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(outcomes_parquet_bytes(outcomes))


def _match_record(
    record: SignalRecord,
    snapshot: PriceSnapshot,
    price_rows: dict[str, list[dict[str, Any]]],
) -> OutcomeRecord:
    if _is_excluded_ambiguous(record):
        return _excluded(
            record,
            snapshot,
            Outcome.EXCLUDED_AMBIGUOUS,
            EXCLUDED_AMBIGUOUS_RULE_ID,
        )

    rows = [
        row
        for row in price_rows.get(record.asset_symbol, [])
        if row["timestamp_utc"] >= record.extracted_timestamp_utc
    ]
    if record.asset_symbol not in snapshot.assets or not rows:
        return _excluded(
            record,
            snapshot,
            Outcome.EXCLUDED_NO_PRICE,
            EXCLUDED_NO_PRICE_RULE_ID,
        )

    return _directional_outcome(record, snapshot, rows)


def _directional_outcome(
    record: SignalRecord,
    snapshot: PriceSnapshot,
    rows: list[dict[str, Any]],
) -> OutcomeRecord:
    entry = _required_decimal(record.entry)
    stop = _required_decimal(record.stop)
    target = _required_decimal(record.target)
    entry_fill_timestamp = rows[0]["timestamp_utc"]
    exit_timestamp = rows[-1]["timestamp_utc"]
    exit_price = rows[-1]["close"]
    outcome = Outcome.TIMEOUT_NO_HIT
    lows: list[Decimal] = []
    highs: list[Decimal] = []

    for row in rows:
        lows.append(row["low"])
        highs.append(row["high"])
        if record.direction == Direction.LONG:
            target_hit = row["high"] >= target
            stop_hit = row["low"] <= stop
        else:
            target_hit = row["low"] <= target
            stop_hit = row["high"] >= stop

        if stop_hit:
            outcome = Outcome.STOP_HIT
            exit_timestamp = row["timestamp_utc"]
            exit_price = stop
            break
        if target_hit:
            outcome = Outcome.TARGET_HIT
            exit_timestamp = row["timestamp_utc"]
            exit_price = target
            break

    return_pct, mae_pct, mfe_pct = _directional_metrics(
        direction=record.direction,
        entry=entry,
        exit_price=exit_price,
        lows=lows,
        highs=highs,
    )

    return OutcomeRecord(
        dedup_key=compute_dedup_key(record),
        source_id=record.source_id,
        asset_symbol=record.asset_symbol,
        extracted_timestamp_utc=record.extracted_timestamp_utc,
        outcome=outcome,
        entry_fill_timestamp=entry_fill_timestamp,
        exit_timestamp=exit_timestamp,
        return_pct=return_pct,
        mae_pct=mae_pct,
        mfe_pct=mfe_pct,
        outcome_rule_id=LONG_TARGET_STOP_RULE_ID,
        snapshot_sha256=snapshot.sha256,
    )


def _is_excluded_ambiguous(record: SignalRecord) -> bool:
    return (
        record.direction in {Direction.FLAT, Direction.UNKNOWN}
        or bool(record.ambiguity_flags)
        or record.entry is None
        or record.stop is None
        or record.target is None
    )


def _excluded(
    record: SignalRecord,
    snapshot: PriceSnapshot,
    outcome: Outcome,
    rule_id: str,
) -> OutcomeRecord:
    return OutcomeRecord(
        dedup_key=compute_dedup_key(record),
        source_id=record.source_id,
        asset_symbol=record.asset_symbol,
        extracted_timestamp_utc=record.extracted_timestamp_utc,
        outcome=outcome,
        outcome_rule_id=rule_id,
        snapshot_sha256=snapshot.sha256,
    )


def _price_rows_by_asset(snapshot: PriceSnapshot) -> dict[str, list[dict[str, Any]]]:
    frame = pl.read_parquet(BytesIO(snapshot.ohlcv_bytes)).select(OHLCV_COLUMNS)
    rows_by_asset: dict[str, list[dict[str, Any]]] = {}
    for row in frame.to_dicts():
        asset = str(row["asset"])
        rows_by_asset.setdefault(asset, []).append(
            {
                "asset": asset,
                "timestamp_utc": datetime.fromisoformat(
                    str(row["timestamp_utc"]).replace("Z", "+00:00")
                ),
                "open": Decimal(str(row["open"])),
                "high": Decimal(str(row["high"])),
                "low": Decimal(str(row["low"])),
                "close": Decimal(str(row["close"])),
                "volume": Decimal(str(row["volume"])),
            }
        )

    for rows in rows_by_asset.values():
        rows.sort(key=lambda row: row["timestamp_utc"])
    return rows_by_asset


def _outcome_to_row(outcome: OutcomeRecord) -> dict[str, Any]:
    return {
        "dedup_key": outcome.dedup_key,
        "source_id": outcome.source_id,
        "asset_symbol": outcome.asset_symbol,
        "extracted_timestamp_utc": outcome.extracted_timestamp_utc.isoformat(),
        "outcome": outcome.outcome.value,
        "entry_fill_timestamp": _datetime_to_string(outcome.entry_fill_timestamp),
        "exit_timestamp": _datetime_to_string(outcome.exit_timestamp),
        "return_pct": _decimal_to_float(outcome.return_pct),
        "mae_pct": _decimal_to_float(outcome.mae_pct),
        "mfe_pct": _decimal_to_float(outcome.mfe_pct),
        "outcome_rule_id": outcome.outcome_rule_id,
        "snapshot_sha256": outcome.snapshot_sha256,
    }


def _empty_frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            column: pl.Series(column, [], dtype=dtype)
            for column, dtype in OUTCOME_SCHEMA.items()
        }
    )


def _datetime_to_string(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.isoformat()


def _decimal_to_float(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _required_decimal(value: Decimal | None) -> Decimal:
    if value is None:
        raise ValueError("expected non-null decimal after exclusion check")
    return value


def _round_pct(value: Decimal) -> Decimal:
    return (value * Decimal("100")).quantize(ROUNDING_QUANT, rounding=ROUND_HALF_EVEN)


def _directional_metrics(
    *,
    direction: Direction,
    entry: Decimal,
    exit_price: Decimal,
    lows: list[Decimal],
    highs: list[Decimal],
) -> tuple[Decimal, Decimal, Decimal]:
    if direction == Direction.SHORT:
        return (
            _round_pct((entry - exit_price) / entry),
            _round_pct((entry - max(highs)) / entry),
            _round_pct((entry - min(lows)) / entry),
        )
    return (
        _round_pct((exit_price - entry) / entry),
        _round_pct((min(lows) - entry) / entry),
        _round_pct((max(highs) - entry) / entry),
    )


def assert_known_rule(rule_id: str) -> None:
    if rule_id not in RULES:
        raise ValueError(f"unknown outcome rule_id: {rule_id}")
