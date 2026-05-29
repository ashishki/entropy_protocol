"""Deterministic V1 outcomes for structured claims."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal
from enum import StrEnum
from io import BytesIO
from typing import Any

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.claims.extractor import (
    ClaimDirection,
    StructuredClaim,
    StructuredClaimType,
)
from signal_sandbox.market_data.metrics import (
    Direction,
    HorizonStatus,
    evaluate_horizon_metrics,
)
from signal_sandbox.market_data.store import MarketDataSnapshot

ROUNDING_QUANT = Decimal("0.000001")


class ClaimOutcomeStatus(StrEnum):
    TARGET_HIT = "target_hit"
    STOPPED = "stopped"
    TIMEOUT = "timeout"
    ENTRY_NOT_FILLED = "entry_not_filled"
    EVALUATED = "evaluated"
    INSUFFICIENT_DATA = "insufficient_data"
    MISSING_REQUIRED_FIELDS = "missing_required_fields"
    REQUIRES_ORIGINAL_SETUP_LINK = "requires_original_setup_link"
    UNSUPPORTED_CLAIM_TYPE = "unsupported_claim_type"
    UNRESOLVED_ASSET = "unresolved_asset"
    NON_DIRECTIONAL = "non_directional"
    MISSING_BENCHMARK_DATA = "missing_benchmark_data"


class ClaimOutcome(BaseModel):
    model_config = ConfigDict(strict=True)

    claim_id: str = Field(min_length=1)
    status: ClaimOutcomeStatus
    canonical_asset_id: str = Field(min_length=1)
    snapshot_id: str = Field(min_length=1)
    metric_version: str = "claim_outcome.v1"
    entry_timestamp_utc: datetime | None = None
    exit_timestamp_utc: datetime | None = None
    entry_price: Decimal | None = None
    exit_price: Decimal | None = None
    return_pct: Decimal | None = None
    max_favorable_excursion_pct: Decimal | None = None
    max_adverse_excursion_pct: Decimal | None = None
    risk_reward: Decimal | None = None
    r_multiple: Decimal | None = None
    benchmark_relative_return_pct: Decimal | None = None
    exclusion_reason: str | None = None

    @field_validator("entry_timestamp_utc", "exit_timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime | None:
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be datetime or ISO string")


def evaluate_claim_outcome(
    claim: StructuredClaim,
    snapshot: MarketDataSnapshot,
    *,
    canonical_asset_id: str,
    timeout_days: int = 7,
    linked_original_setup_id: str | None = None,
    benchmark_snapshot: MarketDataSnapshot | None = None,
    canonical_benchmark_asset_id: str | None = None,
) -> ClaimOutcome:
    if canonical_asset_id != snapshot.metadata.canonical_asset_id:
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.UNRESOLVED_ASSET,
            "snapshot_asset_mismatch",
        )
    if claim.claim_type == StructuredClaimType.TRADE_MANAGEMENT:
        if linked_original_setup_id is None:
            return _status_outcome(
                claim,
                snapshot,
                canonical_asset_id,
                ClaimOutcomeStatus.REQUIRES_ORIGINAL_SETUP_LINK,
                "trade_management_requires_original_setup_link",
            )
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.UNSUPPORTED_CLAIM_TYPE,
            "linked_trade_management_replay_not_implemented",
        )
    if claim.claim_type == StructuredClaimType.DIRECTIONAL_THESIS:
        return _with_benchmark_relative(
            _evaluate_directional_thesis(claim, snapshot, canonical_asset_id),
            claim=claim,
            claim_snapshot=snapshot,
            canonical_asset_id=canonical_asset_id,
            benchmark_snapshot=benchmark_snapshot,
            canonical_benchmark_asset_id=canonical_benchmark_asset_id,
        )
    if claim.claim_type == StructuredClaimType.TRADE_SETUP:
        return _with_benchmark_relative(
            _evaluate_trade_setup(
                claim,
                snapshot,
                canonical_asset_id=canonical_asset_id,
                timeout_days=timeout_days,
            ),
            claim=claim,
            claim_snapshot=snapshot,
            canonical_asset_id=canonical_asset_id,
            benchmark_snapshot=benchmark_snapshot,
            canonical_benchmark_asset_id=canonical_benchmark_asset_id,
        )
    return _status_outcome(
        claim,
        snapshot,
        canonical_asset_id,
        ClaimOutcomeStatus.UNSUPPORTED_CLAIM_TYPE,
        "claim_type_not_outcome_evaluable",
    )


def _evaluate_directional_thesis(
    claim: StructuredClaim,
    snapshot: MarketDataSnapshot,
    canonical_asset_id: str,
) -> ClaimOutcome:
    direction = _metric_direction(claim.direction)
    if direction is None:
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.NON_DIRECTIONAL,
            "missing_or_mixed_direction",
        )
    metric = next(
        item
        for item in evaluate_horizon_metrics(
            snapshot,
            canonical_asset_id=canonical_asset_id,
            post_timestamp_utc=claim.source_timestamp_utc,
            direction=direction,
        )
        if item.horizon == "7d"
    )
    if metric.status == HorizonStatus.INSUFFICIENT_DATA:
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.INSUFFICIENT_DATA,
            "insufficient_horizon_data",
        )
    return ClaimOutcome(
        claim_id=claim.claim_id,
        status=ClaimOutcomeStatus.EVALUATED,
        canonical_asset_id=canonical_asset_id,
        snapshot_id=snapshot.metadata.snapshot_id,
        entry_timestamp_utc=metric.entry_timestamp_utc,
        exit_timestamp_utc=metric.horizon_end_utc,
        return_pct=metric.return_pct,
        max_favorable_excursion_pct=metric.max_favorable_excursion_pct,
        max_adverse_excursion_pct=metric.max_adverse_excursion_pct,
    )


def _evaluate_trade_setup(
    claim: StructuredClaim,
    snapshot: MarketDataSnapshot,
    *,
    canonical_asset_id: str,
    timeout_days: int,
) -> ClaimOutcome:
    if (
        claim.entry is None
        or claim.stop is None
        or claim.target is None
        or claim.direction not in {ClaimDirection.LONG, ClaimDirection.SHORT}
    ):
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.MISSING_REQUIRED_FIELDS,
            "entry_stop_target_direction_required",
        )
    initial_risk = _initial_risk(
        entry=claim.entry,
        stop=claim.stop,
        direction=claim.direction,
    )
    if initial_risk is None:
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.MISSING_REQUIRED_FIELDS,
            "valid_entry_stop_target_direction_required",
        )

    rows = [
        row
        for row in _snapshot_rows(snapshot)
        if claim.source_timestamp_utc
        <= row["timestamp_utc"]
        <= claim.source_timestamp_utc + timedelta(days=timeout_days)
    ]
    if not rows:
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.INSUFFICIENT_DATA,
            "no_rows_in_timeout_window",
        )

    filled_rows = [row for row in rows if row["low"] <= claim.entry <= row["high"]]
    if not filled_rows:
        return _status_outcome(
            claim,
            snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.ENTRY_NOT_FILLED,
            "entry_price_not_touched",
        )
    fill_index = rows.index(filled_rows[0])
    filled_window = rows[fill_index:]
    exit_row, exit_price, status = _setup_exit(
        filled_window,
        direction=claim.direction,
        stop=claim.stop,
        target=claim.target,
    )
    return_pct = _directional_return(
        entry=claim.entry,
        exit_price=exit_price,
        direction=claim.direction,
    )
    mfe, mae = _excursions(
        filled_window,
        entry=claim.entry,
        direction=claim.direction,
    )
    return ClaimOutcome(
        claim_id=claim.claim_id,
        status=status,
        canonical_asset_id=canonical_asset_id,
        snapshot_id=snapshot.metadata.snapshot_id,
        entry_timestamp_utc=filled_rows[0]["timestamp_utc"],
        exit_timestamp_utc=exit_row["timestamp_utc"],
        entry_price=claim.entry,
        exit_price=exit_price,
        return_pct=_round(return_pct),
        max_favorable_excursion_pct=mfe,
        max_adverse_excursion_pct=mae,
        risk_reward=_risk_reward(
            entry=claim.entry,
            stop=claim.stop,
            target=claim.target,
        ),
        r_multiple=_r_multiple(
            entry=claim.entry,
            exit_price=exit_price,
            direction=claim.direction,
            initial_risk=initial_risk,
        ),
    )


def _with_benchmark_relative(
    outcome: ClaimOutcome,
    *,
    claim: StructuredClaim,
    claim_snapshot: MarketDataSnapshot,
    canonical_asset_id: str,
    benchmark_snapshot: MarketDataSnapshot | None,
    canonical_benchmark_asset_id: str | None,
) -> ClaimOutcome:
    if canonical_benchmark_asset_id is None:
        return outcome
    if benchmark_snapshot is None:
        return _status_outcome(
            claim,
            claim_snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.MISSING_BENCHMARK_DATA,
            "benchmark_snapshot_required",
        )
    if outcome.return_pct is None:
        return outcome
    benchmark_metric = next(
        item
        for item in evaluate_horizon_metrics(
            benchmark_snapshot,
            canonical_asset_id=canonical_benchmark_asset_id,
            post_timestamp_utc=claim.source_timestamp_utc,
            direction=Direction.LONG,
        )
        if item.horizon == "7d"
    )
    if (
        benchmark_metric.status != HorizonStatus.EVALUATED
        or benchmark_metric.return_pct is None
    ):
        return _status_outcome(
            claim,
            claim_snapshot,
            canonical_asset_id,
            ClaimOutcomeStatus.MISSING_BENCHMARK_DATA,
            "benchmark_horizon_data_required",
        )
    return outcome.model_copy(
        update={
            "benchmark_relative_return_pct": _round(
                outcome.return_pct - benchmark_metric.return_pct
            )
        }
    )


def _setup_exit(
    rows: list[dict[str, Any]],
    *,
    direction: ClaimDirection,
    stop: Decimal,
    target: Decimal,
) -> tuple[dict[str, Any], Decimal, ClaimOutcomeStatus]:
    for row in rows:
        if direction == ClaimDirection.LONG:
            if row["low"] <= stop:
                return row, stop, ClaimOutcomeStatus.STOPPED
            if row["high"] >= target:
                return row, target, ClaimOutcomeStatus.TARGET_HIT
        if direction == ClaimDirection.SHORT:
            if row["high"] >= stop:
                return row, stop, ClaimOutcomeStatus.STOPPED
            if row["low"] <= target:
                return row, target, ClaimOutcomeStatus.TARGET_HIT
    return rows[-1], rows[-1]["close"], ClaimOutcomeStatus.TIMEOUT


def _snapshot_rows(snapshot: MarketDataSnapshot) -> list[dict[str, Any]]:
    frame = pl.read_parquet(BytesIO(snapshot.data_bytes))
    rows = []
    for row in frame.to_dicts():
        rows.append(
            {
                "timestamp_utc": datetime.fromisoformat(
                    str(row["timestamp_utc"]).replace("Z", "+00:00")
                ),
                "open": Decimal(str(row["open"])),
                "high": Decimal(str(row["high"])),
                "low": Decimal(str(row["low"])),
                "close": Decimal(str(row["close"])),
            }
        )
    return sorted(rows, key=lambda row: row["timestamp_utc"])


def _metric_direction(direction: ClaimDirection) -> Direction | None:
    if direction == ClaimDirection.LONG:
        return Direction.LONG
    if direction == ClaimDirection.SHORT:
        return Direction.SHORT
    return None


def _directional_return(
    *,
    entry: Decimal,
    exit_price: Decimal,
    direction: ClaimDirection,
) -> Decimal:
    raw = ((exit_price - entry) / entry) * Decimal("100")
    if direction == ClaimDirection.SHORT:
        return -raw
    return raw


def _excursions(
    rows: list[dict[str, Any]],
    *,
    entry: Decimal,
    direction: ClaimDirection,
) -> tuple[Decimal, Decimal]:
    highs = [row["high"] for row in rows]
    lows = [row["low"] for row in rows]
    if direction == ClaimDirection.SHORT:
        favorable = ((entry - min(lows)) / entry) * Decimal("100")
        adverse = ((entry - max(highs)) / entry) * Decimal("100")
        return _round(favorable), _round(adverse)
    favorable = ((max(highs) - entry) / entry) * Decimal("100")
    adverse = ((min(lows) - entry) / entry) * Decimal("100")
    return _round(favorable), _round(adverse)


def _risk_reward(
    *,
    entry: Decimal,
    stop: Decimal,
    target: Decimal,
) -> Decimal | None:
    risk = abs(entry - stop)
    if risk == Decimal("0"):
        return None
    reward = abs(target - entry)
    return _round(reward / risk)


def _initial_risk(
    *,
    entry: Decimal,
    stop: Decimal,
    direction: ClaimDirection,
) -> Decimal | None:
    if direction == ClaimDirection.LONG:
        risk = entry - stop
    elif direction == ClaimDirection.SHORT:
        risk = stop - entry
    else:
        return None
    if risk <= Decimal("0"):
        return None
    return risk


def _r_multiple(
    *,
    entry: Decimal,
    exit_price: Decimal,
    direction: ClaimDirection,
    initial_risk: Decimal,
) -> Decimal:
    if direction == ClaimDirection.SHORT:
        return _round((entry - exit_price) / initial_risk)
    return _round((exit_price - entry) / initial_risk)


def _status_outcome(
    claim: StructuredClaim,
    snapshot: MarketDataSnapshot,
    canonical_asset_id: str,
    status: ClaimOutcomeStatus,
    reason: str,
) -> ClaimOutcome:
    return ClaimOutcome(
        claim_id=claim.claim_id,
        status=status,
        canonical_asset_id=canonical_asset_id,
        snapshot_id=snapshot.metadata.snapshot_id,
        exclusion_reason=reason,
    )


def _round(value: Decimal) -> Decimal:
    return value.quantize(ROUNDING_QUANT, rounding=ROUND_HALF_EVEN)
