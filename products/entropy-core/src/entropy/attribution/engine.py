"""Deterministic P&L attribution engine."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from math import sqrt
from typing import Final

from entropy.models.performance import DrawdownRecord, NetSharpe, PerformanceMetrics, PnLStreams
from entropy.models.registry import FillLog

STUB_REASON_CODE: Final = "stub_pending_formula_verification"
ZERO: Final = Decimal("0")
ONE: Final = Decimal("1")


class AttributionError(Exception):
    """Base error for attribution engine failures."""


class StreamBoundaryError(AttributionError):
    """Raised when a caller bypasses the canonical Net Sharpe stream boundary."""


@dataclass(frozen=True)
class AttributionInput:
    """One attribution observation paired with its realized fill log."""

    fill_log: FillLog
    stream_a_return: Decimal
    stream_b_return: Decimal = ZERO
    stream_d_return: Decimal = ZERO


def compute_streams(entries: Sequence[AttributionInput]) -> PnLStreams:
    """Compute protocol P&L streams from already-realized fill logs."""
    if not entries:
        raise ValueError("entries must not be empty")

    return PnLStreams(
        stream_a=tuple(entry.stream_a_return for entry in entries),
        stream_b=tuple(entry.stream_b_return for entry in entries),
        stream_c=tuple(_cost_drag_return(entry.fill_log) for entry in entries),
        stream_d=tuple(entry.stream_d_return for entry in entries),
    )


def compute_net_sharpe(
    pnl_streams: PnLStreams,
    *,
    confidence_interval_68: tuple[float, float],
    M_total: int = 0,
) -> NetSharpe:
    """Compute raw Net Sharpe from active streams only.

    The confidence interval is deliberately caller-supplied. T23 owns CI
    estimation; T21 only preserves the CI metadata on the NetSharpe model.
    """
    if not isinstance(pnl_streams, PnLStreams):
        raise StreamBoundaryError("compute_net_sharpe requires PnLStreams, not raw streams")

    returns = tuple(float(value) for value in pnl_streams.net_sharpe_streams)
    value = _sample_sharpe(returns)
    return NetSharpe(
        value=value,
        confidence_interval_68=confidence_interval_68,
        sample_length=len(returns),
        M_total=M_total,
    )


def compute_drawdown_records(
    returns: Sequence[Decimal],
    timestamps: Sequence[datetime],
    *,
    initial_equity: Decimal = ONE,
) -> tuple[DrawdownRecord, ...]:
    """Generate drawdown records from a deterministic cumulative equity sequence."""
    if len(returns) != len(timestamps):
        raise ValueError("returns and timestamps must have the same length")
    if initial_equity <= ZERO:
        raise ValueError("initial_equity must be positive")

    records: list[DrawdownRecord] = []
    equity = initial_equity
    peak_value = initial_equity
    peak_ts: datetime | None = None
    active_drawdown: _DrawdownState | None = None

    for period_return, timestamp in zip(returns, timestamps, strict=True):
        equity *= ONE + period_return
        if equity >= peak_value:
            if active_drawdown is not None:
                records.append(active_drawdown.to_record(recovery_ts=timestamp))
                active_drawdown = None
            peak_value = equity
            peak_ts = timestamp
            continue

        drawdown_start_ts = peak_ts if peak_ts is not None else timestamp
        if active_drawdown is None:
            active_drawdown = _DrawdownState(
                start_ts=drawdown_start_ts,
                end_ts=timestamp,
                peak_value=peak_value,
                trough_value=equity,
            )
        elif equity < active_drawdown.trough_value:
            active_drawdown = _DrawdownState(
                start_ts=active_drawdown.start_ts,
                end_ts=timestamp,
                peak_value=active_drawdown.peak_value,
                trough_value=equity,
            )

    if active_drawdown is not None:
        records.append(active_drawdown.to_record(recovery_ts=None))

    return tuple(records)


def compute_performance_metrics(
    pnl_streams: PnLStreams,
    drawdown_returns: Sequence[Decimal],
    timestamps: Sequence[datetime],
    *,
    confidence_interval_68: tuple[float, float],
    calmar_ratio: float,
    M_total: int = 0,
    reason_code: str = STUB_REASON_CODE,
) -> PerformanceMetrics:
    """Assemble T21 performance metrics with unresolved statistical fields stubbed."""
    net_sharpe = compute_net_sharpe(
        pnl_streams,
        confidence_interval_68=confidence_interval_68,
        M_total=M_total,
    )
    drawdowns = compute_drawdown_records(drawdown_returns, timestamps)
    if not drawdowns:
        raise ValueError("at least one drawdown is required to compute max_drawdown")

    max_drawdown = max(drawdowns, key=lambda record: record.drawdown_pct)

    return PerformanceMetrics(
        net_sharpe=net_sharpe,
        max_drawdown=max_drawdown,
        calmar_ratio=calmar_ratio,
        n_eff=None,
        harvey_liu_deflated_sharpe=None,
        reason_code=reason_code,
    )


@dataclass(frozen=True)
class _DrawdownState:
    start_ts: datetime
    end_ts: datetime
    peak_value: Decimal
    trough_value: Decimal

    def to_record(self, *, recovery_ts: datetime | None) -> DrawdownRecord:
        drawdown_pct = float((self.peak_value - self.trough_value) / self.peak_value)
        return DrawdownRecord(
            start_ts=self.start_ts,
            end_ts=self.end_ts,
            peak_value=self.peak_value,
            trough_value=self.trough_value,
            drawdown_pct=drawdown_pct,
            recovery_ts=recovery_ts,
        )


def _cost_drag_return(fill_log: FillLog) -> Decimal:
    notional = fill_log.fill_price * fill_log.quantity
    cost = (
        fill_log.commission
        + fill_log.slippage
        + fill_log.market_impact
        + fill_log.borrow_rate
        + fill_log.funding_rate
    )
    return -cost / notional


def _sample_sharpe(returns: Sequence[float]) -> float:
    if len(returns) < 2:
        raise ValueError("at least two return observations are required")

    mean_return = sum(returns) / len(returns)
    sample_variance = sum((value - mean_return) ** 2 for value in returns) / (len(returns) - 1)
    if sample_variance == 0.0:
        raise ValueError("return observations must have non-zero sample variance")
    return mean_return / sqrt(sample_variance)
