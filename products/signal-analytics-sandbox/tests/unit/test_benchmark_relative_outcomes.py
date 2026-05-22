from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.claims import (
    ClaimOutcomeStatus,
    StructuredClaimType,
    evaluate_claim_outcome,
)
from signal_sandbox.market_data import make_operator_file_snapshot
from tests.unit.test_claim_outcomes_v1 import _claim, dt, row


def test_benchmark_relative_return_subtracts_benchmark_return() -> None:
    outcome = evaluate_claim_outcome(
        _claim(
            StructuredClaimType.DIRECTIONAL_THESIS,
            entry=None,
            stop=None,
            target=None,
        ),
        _claim_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        benchmark_snapshot=_benchmark_snapshot(),
        canonical_benchmark_asset_id="BENCH:SPY",
    )

    assert outcome.status == ClaimOutcomeStatus.EVALUATED
    assert outcome.return_pct == Decimal("50.000000")
    assert outcome.benchmark_relative_return_pct == Decimal("40.000000")


def test_missing_benchmark_data_is_explicit_exclusion() -> None:
    outcome = evaluate_claim_outcome(
        _claim(
            StructuredClaimType.DIRECTIONAL_THESIS,
            entry=None,
            stop=None,
            target=None,
        ),
        _claim_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        canonical_benchmark_asset_id="BENCH:SPY",
    )

    assert outcome.status == ClaimOutcomeStatus.MISSING_BENCHMARK_DATA
    assert outcome.exclusion_reason == "benchmark_snapshot_required"
    assert outcome.benchmark_relative_return_pct is None


def _claim_snapshot():
    return make_operator_file_snapshot(
        snapshot_id="btc-benchmark-relative",
        canonical_asset_id="CRYPTO:BTC",
        provider_symbol="BTC/USDT",
        timeframe="1d",
        source_range_start_utc=dt("2026-05-01T00:00:00+00:00"),
        source_range_end_utc=dt("2026-05-10T00:00:00+00:00"),
        captured_at_utc=dt("2026-05-11T00:00:00+00:00"),
        rows=[
            row("2026-05-01T00:00:00+00:00", "100", "105", "95", "100"),
            row("2026-05-08T00:00:00+00:00", "100", "160", "90", "150"),
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )


def _benchmark_snapshot():
    return make_operator_file_snapshot(
        snapshot_id="spy-benchmark-relative",
        canonical_asset_id="BENCH:SPY",
        provider_symbol="SPY",
        timeframe="1d",
        source_range_start_utc=datetime(2026, 5, 1, tzinfo=UTC),
        source_range_end_utc=datetime(2026, 5, 10, tzinfo=UTC),
        captured_at_utc=datetime(2026, 5, 11, tzinfo=UTC),
        rows=[
            row("2026-05-01T00:00:00+00:00", "100", "101", "99", "100"),
            row("2026-05-08T00:00:00+00:00", "100", "112", "98", "110"),
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )
