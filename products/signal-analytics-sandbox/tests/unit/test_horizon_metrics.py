from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from signal_sandbox.market_data import (
    Direction,
    HorizonStatus,
    evaluate_horizon_metrics,
    make_operator_file_snapshot,
)


def test_horizon_returns_are_deterministic() -> None:
    metrics = evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        post_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        direction=Direction.LONG,
    )

    assert [metric.horizon for metric in metrics] == ["1d", "3d", "7d", "30d"]
    assert [metric.status for metric in metrics] == [HorizonStatus.EVALUATED] * 4
    assert [metric.return_pct for metric in metrics] == [
        Decimal("10.000000"),
        Decimal("30.000000"),
        Decimal("50.000000"),
        Decimal("50.000000"),
    ]
    assert metrics == evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        post_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        direction=Direction.LONG,
    )


def test_mfe_mae_by_horizon() -> None:
    long_metrics = evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        post_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        direction=Direction.LONG,
    )
    short_metrics = evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        post_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        direction=Direction.SHORT,
    )

    assert long_metrics[1].max_favorable_excursion_pct == Decimal("35.000000")
    assert long_metrics[1].max_adverse_excursion_pct == Decimal("-10.000000")
    assert short_metrics[1].max_favorable_excursion_pct == Decimal("10.000000")
    assert short_metrics[1].max_adverse_excursion_pct == Decimal("-35.000000")


def test_unresolved_cases_are_explicit() -> None:
    unresolved = evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:ETH",
        post_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        direction=Direction.LONG,
    )
    non_directional = evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        post_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        direction=Direction.UNKNOWN,
    )
    insufficient = evaluate_horizon_metrics(
        make_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        post_timestamp_utc=dt("2026-06-01T00:00:00+00:00"),
        direction=Direction.LONG,
    )

    assert {metric.status for metric in unresolved} == {HorizonStatus.UNRESOLVED_ASSET}
    assert {metric.status for metric in non_directional} == {
        HorizonStatus.NON_DIRECTIONAL
    }
    assert {metric.status for metric in insufficient} == {
        HorizonStatus.INSUFFICIENT_DATA
    }


def make_snapshot():
    return make_operator_file_snapshot(
        snapshot_id="btc-horizons",
        canonical_asset_id="CRYPTO:BTC",
        provider_symbol="BTC/USDT",
        timeframe="1d",
        source_range_start_utc=dt("2026-05-01T00:00:00+00:00"),
        source_range_end_utc=dt("2026-05-31T00:00:00+00:00"),
        captured_at_utc=dt("2026-06-01T00:00:00+00:00"),
        rows=[
            row("2026-05-01T00:00:00+00:00", "100", "105", "90", "100"),
            row("2026-05-02T00:00:00+00:00", "100", "115", "95", "110"),
            row("2026-05-04T00:00:00+00:00", "110", "135", "100", "130"),
            row("2026-05-08T00:00:00+00:00", "130", "160", "120", "150"),
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )


def row(timestamp: str, open_: str, high: str, low: str, close: str):
    return {
        "asset": "BTC",
        "timestamp_utc": timestamp,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": "1",
    }


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value)
