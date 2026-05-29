from __future__ import annotations

from decimal import Decimal

from signal_sandbox.runs import RunStepMetric, build_run_operational_metrics


def test_run_metrics_record_duration_provider_calls_cache_hits_and_cost() -> None:
    metrics = build_run_operational_metrics(
        run_id="run-three-channel-v2",
        steps=[
            RunStepMetric(
                step_name="report",
                duration_ms=300,
                provider_calls=0,
                cache_hits=2,
                estimated_cost_usd=Decimal("0.00"),
            ),
            RunStepMetric(
                step_name="market_data",
                duration_ms=1200,
                provider_calls=3,
                cache_hits=1,
                estimated_cost_usd=Decimal("0.125"),
            ),
        ],
    )

    assert [step.step_name for step in metrics.steps] == ["market_data", "report"]
    assert metrics.total_duration_ms == 1500
    assert metrics.total_provider_calls == 3
    assert metrics.total_cache_hits == 3
    assert metrics.total_estimated_cost_usd == Decimal("0.125000")
    assert len(metrics.metrics_sha256()) == 64


def test_run_metrics_cost_is_unknown_when_any_step_cost_is_missing() -> None:
    metrics = build_run_operational_metrics(
        run_id="run-three-channel-v2",
        steps=[
            RunStepMetric(
                step_name="capture",
                duration_ms=100,
                provider_calls=1,
                cache_hits=0,
                estimated_cost_usd=None,
            ),
            RunStepMetric(
                step_name="review",
                duration_ms=200,
                provider_calls=0,
                cache_hits=1,
                estimated_cost_usd=Decimal("0.05"),
            ),
        ],
    )

    assert metrics.total_duration_ms == 300
    assert metrics.total_provider_calls == 1
    assert metrics.total_cache_hits == 1
    assert metrics.total_estimated_cost_usd is None
