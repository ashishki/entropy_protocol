from __future__ import annotations

from signal_sandbox.claims import (
    FetchPlanStatus,
    mark_provider_fetch_failure,
    plan_market_data_fetches,
)
from tests.unit.test_provider_proxy_config_v1 import _claim


def test_retryable_provider_error_produces_retry_state_not_outcome() -> None:
    plan = plan_market_data_fetches([_claim("claim-btc-provider-fail", ["BTC"])])[0]

    failed = mark_provider_fetch_failure(
        plan,
        error_code="http_429",
        retryable=True,
        reason="provider_rate_limited",
    )

    assert failed.status == FetchPlanStatus.RETRY_PROVIDER_FAILURE
    assert failed.provider == "binance"
    assert failed.provider_symbol == "BTCUSDT"
    assert failed.provider_error_code == "http_429"
    assert failed.retryable is True
    assert failed.exclusion_reason == "provider_rate_limited"
    assert "win" not in failed.status.value
    assert "loss" not in failed.status.value


def test_terminal_provider_error_produces_exclusion_not_win_loss() -> None:
    plan = plan_market_data_fetches([_claim("claim-spy-provider-fail", ["SPY"])])[0]

    failed = mark_provider_fetch_failure(
        plan,
        error_code="symbol_not_found",
        retryable=False,
        reason="provider_symbol_unavailable",
    )

    assert failed.status == FetchPlanStatus.EXCLUDED_PROVIDER_FAILURE
    assert failed.provider == "yfinance_dev"
    assert failed.provider_error_code == "symbol_not_found"
    assert failed.retryable is False
    assert failed.exclusion_reason == "provider_symbol_unavailable"
    assert "win" not in failed.status.value
    assert "loss" not in failed.status.value
