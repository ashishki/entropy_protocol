"""Performance and attribution domain models."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

NET_SHARPE_METHOD_ID = "CI-SR-ACF-v1"


class PnLStreams(BaseModel):
    """Protocol NN-2 four-stream P&L decomposition."""

    stream_a: tuple[Decimal, ...]
    stream_b: tuple[Decimal, ...]
    stream_c: tuple[Decimal, ...]
    stream_d: tuple[Decimal, ...]

    @property
    def net_sharpe_streams(self) -> tuple[Decimal, ...]:
        """Return only active trading book streams (a)+(b)+(c)."""
        return tuple(
            stream_a + stream_b + stream_c
            for stream_a, stream_b, stream_c in zip(
                self.stream_a,
                self.stream_b,
                self.stream_c,
                strict=True,
            )
        )

    @model_validator(mode="after")
    def validate_stream_lengths(self) -> "PnLStreams":
        """Require every stream to have the same observation count."""
        lengths = {
            len(self.stream_a),
            len(self.stream_b),
            len(self.stream_c),
            len(self.stream_d),
        }
        if len(lengths) != 1:
            raise ValueError("all P&L streams must have the same length")
        return self


class NetSharpe(BaseModel):
    """Net Sharpe estimate with canonical 68% confidence interval metadata."""

    value: float
    confidence_interval_68: tuple[float, float]
    method_id: Literal["CI-SR-ACF-v1"] = NET_SHARPE_METHOD_ID
    sample_length: int = Field(gt=0)
    M_total: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_confidence_interval(self) -> "NetSharpe":
        """Require confidence interval bounds to be ordered."""
        lower, upper = self.confidence_interval_68
        if upper < lower:
            raise ValueError("confidence_interval_68 upper bound must be >= lower bound")
        return self


class DrawdownRecord(BaseModel):
    """One drawdown interval with peak/trough and recovery metadata."""

    start_ts: datetime
    end_ts: datetime
    peak_value: Decimal = Field(gt=Decimal("0"))
    trough_value: Decimal = Field(ge=Decimal("0"))
    drawdown_pct: float = Field(ge=0.0, le=1.0)
    recovery_ts: datetime | None = None

    @field_validator("start_ts", "end_ts", "recovery_ts")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime | None) -> datetime | None:
        """Require timezone-aware UTC timestamps when present."""
        if value is None:
            return value
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("drawdown timestamps must be timezone-aware UTC")
        return value

    @model_validator(mode="after")
    def validate_values(self) -> "DrawdownRecord":
        """Require chronological drawdown windows and trough <= peak."""
        if self.end_ts < self.start_ts:
            raise ValueError("end_ts must be on or after start_ts")
        if self.trough_value > self.peak_value:
            raise ValueError("trough_value must be <= peak_value")
        if self.recovery_ts is not None and self.recovery_ts < self.end_ts:
            raise ValueError("recovery_ts must be on or after end_ts")
        return self


class PerformanceMetrics(BaseModel):
    """Aggregated performance metrics with explicit Phase 0 formula stubs."""

    net_sharpe: NetSharpe
    max_drawdown: DrawdownRecord
    calmar_ratio: float
    n_eff: float | None = Field(default=None, ge=0)
    harvey_liu_deflated_sharpe: float | None = None
    reason_code: str | None = None

    @model_validator(mode="after")
    def require_reason_for_stub_fields(self) -> "PerformanceMetrics":
        """Require an explanation when Phase 0 stub metrics are not populated."""
        has_stub = self.n_eff is None or self.harvey_liu_deflated_sharpe is None
        if has_stub and (self.reason_code is None or not self.reason_code.strip()):
            raise ValueError("reason_code is required when stub metrics are None")
        return self
