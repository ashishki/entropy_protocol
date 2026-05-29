from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from signal_sandbox.claims import (
    ClaimDirection,
    FetchPlanStatus,
    ProviderProxyStatus,
    StructuredClaim,
    StructuredClaimType,
    default_provider_proxy_config,
    plan_market_data_fetches,
)


def test_provider_proxy_config_maps_approved_and_unsupported_classes() -> None:
    config = default_provider_proxy_config()

    assert config.resolve("BTC").provider == "binance"
    assert config.resolve("SBER").provider == "moex_iss"
    assert config.resolve("SBRF").provider_symbol == "SBER"
    assert config.resolve("SPY").provider == "yfinance_dev"
    assert config.resolve("SPYF").status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT
    assert config.resolve("BR").status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT
    assert config.resolve("IMOEX").status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT
    assert config.resolve("UNKNOWN").status == ProviderProxyStatus.UNSUPPORTED


def test_market_data_fetch_planning_uses_only_approved_claim_windows() -> None:
    plans = plan_market_data_fetches(
        [
            _claim("claim-btc", ["BTC"]),
            _claim("claim-sber", ["SBRF"]),
            _claim("claim-spy", ["SPY"]),
            _claim("claim-unknown-us", ["SPYF"]),
        ]
    )

    planned = [plan for plan in plans if plan.status == FetchPlanStatus.PLANNED]
    excluded = [
        plan for plan in plans if plan.status == FetchPlanStatus.EXCLUDED_PROVIDER_GAP
    ]

    assert [(plan.provider, plan.provider_symbol) for plan in planned] == [
        ("binance", "BTCUSDT"),
        ("moex_iss", "SBER"),
        ("yfinance_dev", "SPY"),
    ]
    assert excluded[0].asset == "SPYF"
    assert excluded[0].provider is None


def test_provider_gaps_are_exclusions_not_win_loss_rows() -> None:
    plans = plan_market_data_fetches(
        [
            _claim("claim-ng", ["NG"]),
            _claim("claim-risk", ["BTC"], claim_type=StructuredClaimType.RISK_WARNING),
            _claim("claim-mixed", ["BTC"], direction=ClaimDirection.MIXED),
        ]
    )

    assert [plan.status for plan in plans] == [
        FetchPlanStatus.EXCLUDED_PROVIDER_GAP,
        FetchPlanStatus.EXCLUDED_UNSUPPORTED_CLAIM_TYPE,
        FetchPlanStatus.EXCLUDED_NON_DIRECTIONAL,
    ]
    assert all(plan.provider is None for plan in plans)


def _claim(
    claim_id: str,
    assets: list[str],
    *,
    claim_type: StructuredClaimType = StructuredClaimType.DIRECTIONAL_THESIS,
    direction: ClaimDirection = ClaimDirection.LONG,
) -> StructuredClaim:
    text_sha = hashlib.sha256(claim_id.encode()).hexdigest()
    return StructuredClaim(
        claim_id=claim_id,
        source_id="test",
        capture_id=f"capture-{claim_id}",
        source_document_id=f"doc-{claim_id}",
        evidence_url=f"https://t.me/test/{claim_id}",
        text_sha256=text_sha,
        source_timestamp_utc=datetime(2026, 5, 19, tzinfo=UTC),
        claim_type=claim_type,
        assets=assets,
        direction=direction,
    )
