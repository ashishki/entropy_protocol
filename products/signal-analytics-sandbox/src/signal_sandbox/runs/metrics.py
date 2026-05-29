"""Operational time/cost metrics for report runs."""

from __future__ import annotations

import hashlib
from decimal import ROUND_HALF_EVEN, Decimal

from pydantic import BaseModel, ConfigDict, Field

ROUNDING_QUANT = Decimal("0.000001")


class RunStepMetric(BaseModel):
    model_config = ConfigDict(strict=True)

    step_name: str = Field(min_length=1)
    duration_ms: int = Field(ge=0)
    provider_calls: int = Field(default=0, ge=0)
    cache_hits: int = Field(default=0, ge=0)
    estimated_cost_usd: Decimal | None = Field(default=None, ge=0)


class RunOperationalMetrics(BaseModel):
    model_config = ConfigDict(strict=True)

    run_id: str = Field(min_length=1)
    steps: list[RunStepMetric] = Field(min_length=1)

    @property
    def total_duration_ms(self) -> int:
        return sum(step.duration_ms for step in self.steps)

    @property
    def total_provider_calls(self) -> int:
        return sum(step.provider_calls for step in self.steps)

    @property
    def total_cache_hits(self) -> int:
        return sum(step.cache_hits for step in self.steps)

    @property
    def total_estimated_cost_usd(self) -> Decimal | None:
        costs = [step.estimated_cost_usd for step in self.steps]
        if any(cost is None for cost in costs):
            return None
        return _round(sum((cost for cost in costs if cost is not None), Decimal("0")))

    def canonical_json_bytes(self) -> bytes:
        return self.model_dump_json().encode("utf-8")

    def metrics_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json_bytes()).hexdigest()


def build_run_operational_metrics(
    *,
    run_id: str,
    steps: list[RunStepMetric],
) -> RunOperationalMetrics:
    return RunOperationalMetrics(
        run_id=run_id,
        steps=sorted(steps, key=lambda step: step.step_name),
    )


def _round(value: Decimal) -> Decimal:
    return value.quantize(ROUNDING_QUANT, rounding=ROUND_HALF_EVEN)
