from __future__ import annotations

from trader_risk_audit.exchange.binance import (
    BINANCE_SPOT_MY_TRADES_ENDPOINT,
    BINANCE_SPOT_MY_TRADES_PATH,
    plan_binance_spot_trade_fetches,
)


def test_binance_fetch_plan_is_deterministic() -> None:
    plan = plan_binance_spot_trade_fetches(
        symbols=("ethusdt", "BTCUSDT", "ethusdt"),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-03T06:00:00Z",
    )
    repeated = plan_binance_spot_trade_fetches(
        symbols=("ETHUSDT", "btcusdt"),
        start_time="2026-04-01T00:00:00+00:00",
        end_time="2026-04-03T06:00:00+00:00",
    )

    assert plan == repeated
    assert [(window.symbol, window.start_time, window.end_time) for window in plan] == [
        ("BTCUSDT", "2026-04-01T00:00:00Z", "2026-04-02T00:00:00Z"),
        ("BTCUSDT", "2026-04-02T00:00:00Z", "2026-04-03T00:00:00Z"),
        ("BTCUSDT", "2026-04-03T00:00:00Z", "2026-04-03T06:00:00Z"),
        ("ETHUSDT", "2026-04-01T00:00:00Z", "2026-04-02T00:00:00Z"),
        ("ETHUSDT", "2026-04-02T00:00:00Z", "2026-04-03T00:00:00Z"),
        ("ETHUSDT", "2026-04-03T00:00:00Z", "2026-04-03T06:00:00Z"),
    ]

    first_window_metadata = plan[0].to_source_metadata()
    assert first_window_metadata["endpoint_label"] == BINANCE_SPOT_MY_TRADES_ENDPOINT
    assert first_window_metadata["method"] == "GET"
    assert first_window_metadata["path"] == BINANCE_SPOT_MY_TRADES_PATH
    assert first_window_metadata["market"] == "spot"
    assert plan[0].to_request_params(timestamp_ms=1775210400000) == {
        "symbol": "BTCUSDT",
        "startTime": plan[0].start_time_ms,
        "endTime": plan[0].end_time_ms,
        "timestamp": 1775210400000,
        "recvWindow": 5000,
        "limit": 1000,
    }


def test_binance_fetch_order_is_stable() -> None:
    plan = plan_binance_spot_trade_fetches(
        symbols=("ETHUSDT", "BTCUSDT"),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-02T01:00:00Z",
    )

    assert [window.request_number for window in plan] == [1, 2, 3, 4]
    assert [(window.symbol, window.start_time, window.end_time) for window in plan] == [
        ("BTCUSDT", "2026-04-01T00:00:00Z", "2026-04-02T00:00:00Z"),
        ("BTCUSDT", "2026-04-02T00:00:00Z", "2026-04-02T01:00:00Z"),
        ("ETHUSDT", "2026-04-01T00:00:00Z", "2026-04-02T00:00:00Z"),
        ("ETHUSDT", "2026-04-02T00:00:00Z", "2026-04-02T01:00:00Z"),
    ]
