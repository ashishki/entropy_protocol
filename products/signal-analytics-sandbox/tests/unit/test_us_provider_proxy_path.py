from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from signal_sandbox.claims import (
    ClaimDirection,
    FetchPlanStatus,
    StructuredClaim,
    StructuredClaimType,
    default_provider_proxy_config,
    plan_market_data_fetches,
)


def test_us_equity_and_fund_symbols_resolve_to_internal_provider_route() -> None:
    config = default_provider_proxy_config()

    assert config.resolve("SPY").provider == "yfinance_dev"
    assert config.resolve("QQQ").provider_symbol == "QQQ"
    assert config.resolve("AAPL").asset_class == "us_equity"
    assert config.resolve("NVDA").provider_symbol == "NVDA"


def test_us_provider_fetch_planning_is_on_demand_and_window_scoped() -> None:
    plans = plan_market_data_fetches(
        [_claim("claim-spy", ["SPY"]), _claim("claim-aapl", ["AAPL"])],
        lookback_days=1,
        forward_days=3,
    )

    assert [plan.status for plan in plans] == [
        FetchPlanStatus.PLANNED,
        FetchPlanStatus.PLANNED,
    ]
    assert [(plan.provider, plan.provider_symbol) for plan in plans] == [
        ("yfinance_dev", "SPY"),
        ("yfinance_dev", "AAPL"),
    ]
    assert plans[0].range_start_utc == "2026-05-18T12:00:00+00:00"
    assert plans[0].range_end_utc == "2026-05-22T12:00:00+00:00"


def test_us_provider_gaps_remain_exclusions() -> None:
    plans = plan_market_data_fetches(
        [
            _claim("claim-spyf", ["SPYF"]),
            _claim("claim-unknown", ["OPENAI"]),
            _claim("claim-mixed", ["SPY"], direction=ClaimDirection.MIXED),
        ]
    )

    assert [plan.status for plan in plans] == [
        FetchPlanStatus.EXCLUDED_PROVIDER_GAP,
        FetchPlanStatus.EXCLUDED_PROVIDER_GAP,
        FetchPlanStatus.EXCLUDED_NON_DIRECTIONAL,
    ]
    assert all(plan.provider is None for plan in plans)


def _claim(
    claim_id: str,
    assets: list[str],
    *,
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
        source_timestamp_utc=datetime(2026, 5, 19, 12, tzinfo=UTC),
        claim_type=StructuredClaimType.DIRECTIONAL_THESIS,
        assets=assets,
        direction=direction,
    )
