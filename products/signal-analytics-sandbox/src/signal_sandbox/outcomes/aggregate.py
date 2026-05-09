"""Deterministic aggregation over matched signal outcomes."""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from decimal import ROUND_HALF_EVEN, Decimal
from io import BytesIO
from typing import Any

import polars as pl
from pydantic import BaseModel, ConfigDict

from signal_sandbox.outcomes.matcher import OUTCOME_COLUMNS, Outcome, OutcomeRecord

ROUNDING_QUANT = Decimal("0.000001")


class SummaryRecord(BaseModel):
    model_config = ConfigDict(strict=True)

    total_signals: int
    evaluated_signals: int
    historical_wins: int
    historical_losses: int
    historical_timeouts: int
    excluded_ambiguous: int
    excluded_no_price: int
    historical_win_rate: Decimal
    historical_mean_return_pct: Decimal
    historical_median_return_pct: Decimal
    historical_max_drawdown_pct: Decimal

    def canonical_json_bytes(self) -> bytes:
        return summary_json_bytes(self)


def aggregate_outcomes(outcomes: Sequence[OutcomeRecord]) -> SummaryRecord:
    ordered = sorted(
        outcomes,
        key=lambda row: (row.extracted_timestamp_utc.isoformat(), row.dedup_key),
    )
    returns = [row.return_pct for row in ordered if row.return_pct is not None]
    wins = sum(1 for row in ordered if row.outcome == Outcome.TARGET_HIT)
    losses = sum(1 for row in ordered if row.outcome == Outcome.STOP_HIT)
    timeouts = sum(1 for row in ordered if row.outcome == Outcome.TIMEOUT_NO_HIT)
    win_loss_total = wins + losses

    return SummaryRecord(
        total_signals=len(ordered),
        evaluated_signals=wins + losses + timeouts,
        historical_wins=wins,
        historical_losses=losses,
        historical_timeouts=timeouts,
        excluded_ambiguous=sum(
            1 for row in ordered if row.outcome == Outcome.EXCLUDED_AMBIGUOUS
        ),
        excluded_no_price=sum(
            1 for row in ordered if row.outcome == Outcome.EXCLUDED_NO_PRICE
        ),
        historical_win_rate=_ratio(wins, win_loss_total),
        historical_mean_return_pct=_mean(returns),
        historical_median_return_pct=_median(returns),
        historical_max_drawdown_pct=_max_drawdown(returns),
    )


def aggregate_outcomes_parquet_bytes(parquet_bytes: bytes) -> SummaryRecord:
    frame = pl.read_parquet(BytesIO(parquet_bytes)).select(OUTCOME_COLUMNS)
    return aggregate_outcomes([_row_to_outcome(row) for row in frame.to_dicts()])


def summary_json_bytes(summary: SummaryRecord) -> bytes:
    payload = {
        field: _json_value(value)
        for field, value in summary.model_dump(mode="python").items()
    }
    return json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _ratio(numerator: int, denominator: int) -> Decimal:
    if denominator == 0:
        return Decimal("0.000000")
    return _round(Decimal(numerator) / Decimal(denominator))


def _mean(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal("0.000000")
    return _round(sum(values, Decimal("0")) / Decimal(len(values)))


def _median(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal("0.000000")
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return _round(ordered[midpoint])
    return _round((ordered[midpoint - 1] + ordered[midpoint]) / Decimal("2"))


def _max_drawdown(values: list[Decimal]) -> Decimal:
    cumulative = Decimal("0")
    peak = Decimal("0")
    max_drawdown = Decimal("0")
    for value in values:
        cumulative += value
        peak = max(peak, cumulative)
        max_drawdown = min(max_drawdown, cumulative - peak)
    return _round(max_drawdown)


def _round(value: Decimal) -> Decimal:
    return value.quantize(ROUNDING_QUANT, rounding=ROUND_HALF_EVEN)


def _json_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    return value


def _row_to_outcome(row: dict[str, Any]) -> OutcomeRecord:
    return OutcomeRecord.model_validate(
        {
            "dedup_key": str(row["dedup_key"]),
            "source_id": str(row["source_id"]),
            "asset_symbol": str(row["asset_symbol"]),
            "extracted_timestamp_utc": _string_to_datetime(
                row["extracted_timestamp_utc"]
            ),
            "outcome": str(row["outcome"]),
            "entry_fill_timestamp": _string_to_datetime(row["entry_fill_timestamp"]),
            "exit_timestamp": _string_to_datetime(row["exit_timestamp"]),
            "return_pct": _float_to_decimal(row["return_pct"]),
            "mae_pct": _float_to_decimal(row["mae_pct"]),
            "mfe_pct": _float_to_decimal(row["mfe_pct"]),
            "outcome_rule_id": str(row["outcome_rule_id"]),
            "snapshot_sha256": str(row["snapshot_sha256"]),
        }
    )


def _string_to_datetime(value: object) -> datetime | None:
    if value is None or value == "":
        return None
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def _float_to_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))
