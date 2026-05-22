"""Provider/proxy config and on-demand fetch planning for V1 claims."""

from __future__ import annotations

from datetime import timedelta
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.claims.extractor import (
    ClaimDirection,
    StructuredClaim,
    StructuredClaimType,
)


class ProviderProxyStatus(StrEnum):
    APPROVED = "approved"
    NEEDS_OPERATOR_INPUT = "needs_operator_input"
    UNSUPPORTED = "unsupported"


class FetchPlanStatus(StrEnum):
    PLANNED = "planned"
    RETRY_PROVIDER_FAILURE = "retry_provider_failure"
    EXCLUDED_PROVIDER_FAILURE = "excluded_provider_failure"
    EXCLUDED_PROVIDER_GAP = "excluded_provider_gap"
    EXCLUDED_NON_DIRECTIONAL = "excluded_non_directional"
    EXCLUDED_UNSUPPORTED_CLAIM_TYPE = "excluded_unsupported_claim_type"


class ProviderProxyRule(BaseModel):
    model_config = ConfigDict(strict=True)

    symbol: str = Field(min_length=1)
    asset_class: str = Field(min_length=1)
    status: ProviderProxyStatus
    provider: str | None = None
    provider_symbol: str | None = None
    timeframe: str = "1d"
    rationale: str = Field(min_length=1)


class MarketDataFetchPlan(BaseModel):
    model_config = ConfigDict(strict=True)

    claim_id: str = Field(min_length=1)
    asset: str = Field(min_length=1)
    status: FetchPlanStatus
    provider: str | None = None
    provider_symbol: str | None = None
    timeframe: str | None = None
    range_start_utc: str | None = None
    range_end_utc: str | None = None
    exclusion_reason: str | None = None
    provider_error_code: str | None = None
    retryable: bool | None = None


class ProviderProxyConfig(BaseModel):
    model_config = ConfigDict(strict=True)

    rules: dict[str, ProviderProxyRule]

    def resolve(self, symbol: str) -> ProviderProxyRule:
        normalized = symbol.upper()
        return self.rules.get(
            normalized,
            ProviderProxyRule(
                symbol=normalized,
                asset_class="unknown",
                status=ProviderProxyStatus.UNSUPPORTED,
                rationale="no approved provider/proxy mapping",
            ),
        )


def default_provider_proxy_config() -> ProviderProxyConfig:
    rules: dict[str, ProviderProxyRule] = {}
    for symbol in ("BTC", "ETH", "TON", "AVAX", "ARB", "SOL", "SUI", "DOT"):
        rules[symbol] = ProviderProxyRule(
            symbol=symbol,
            asset_class="crypto",
            status=ProviderProxyStatus.APPROVED,
            provider="binance",
            provider_symbol=f"{symbol}USDT",
            rationale="approved Binance public daily kline path",
        )
    for symbol in (
        "LKOH",
        "SBER",
        "SBRF",
        "SMLT",
        "CHMF",
        "MAGN",
        "PHOR",
        "VTBR",
        "NVTK",
        "LENT",
        "GAZP",
        "X5",
        "SFIN",
        "WUSH",
    ):
        provider_symbol = "SBER" if symbol == "SBRF" else symbol
        rules[symbol] = ProviderProxyRule(
            symbol=symbol,
            asset_class="moex_share",
            status=ProviderProxyStatus.APPROVED,
            provider="moex_iss",
            provider_symbol=provider_symbol,
            rationale="approved MOEX ISS public daily candle path",
        )
    for symbol, asset_class in {
        "BR": "futures_proxy",
        "SI": "futures_proxy",
        "NG": "futures_proxy",
        "MIX": "benchmark_index",
        "IMOEX": "benchmark_index",
        "GOLD": "commodity_proxy",
        "CNY": "fx_proxy",
        "CN": "fx_proxy",
    }.items():
        rules[symbol] = ProviderProxyRule(
            symbol=symbol,
            asset_class=asset_class,
            status=ProviderProxyStatus.NEEDS_OPERATOR_INPUT,
            rationale="provider/proxy semantics not approved for V1",
        )
    for symbol in ("SPY", "QQQ"):
        rules[symbol] = ProviderProxyRule(
            symbol=symbol,
            asset_class="us_fund",
            status=ProviderProxyStatus.APPROVED,
            provider="yfinance_dev",
            provider_symbol=symbol,
            rationale=(
                "approved internal yfinance-dev daily route for liquid US fund symbols"
            ),
        )
    for symbol in ("AAPL", "MSFT", "NVDA", "TSLA", "AMD"):
        rules[symbol] = ProviderProxyRule(
            symbol=symbol,
            asset_class="us_equity",
            status=ProviderProxyStatus.APPROVED,
            provider="yfinance_dev",
            provider_symbol=symbol,
            rationale=(
                "approved internal yfinance-dev daily route for liquid "
                "US equity symbols"
            ),
        )
    rules["SPYF"] = ProviderProxyRule(
        symbol="SPYF",
        asset_class="ambiguous_fund_alias",
        status=ProviderProxyStatus.NEEDS_OPERATOR_INPUT,
        rationale="ambiguous fund alias; exact venue/provider mapping not approved",
    )
    return ProviderProxyConfig(rules=rules)


def plan_market_data_fetches(
    claims: list[StructuredClaim],
    *,
    config: ProviderProxyConfig | None = None,
    lookback_days: int = 2,
    forward_days: int = 7,
) -> list[MarketDataFetchPlan]:
    provider_config = config or default_provider_proxy_config()
    plans: list[MarketDataFetchPlan] = []
    for claim in claims:
        if claim.claim_type not in {
            StructuredClaimType.TRADE_SETUP,
            StructuredClaimType.DIRECTIONAL_THESIS,
            StructuredClaimType.POSITION_DISCLOSURE,
        }:
            plans.extend(_unsupported_claim_plans(claim))
            continue
        if claim.direction not in {ClaimDirection.LONG, ClaimDirection.SHORT}:
            plans.extend(_non_directional_plans(claim))
            continue
        for asset in claim.assets:
            rule = provider_config.resolve(asset)
            if rule.status != ProviderProxyStatus.APPROVED:
                plans.append(
                    MarketDataFetchPlan(
                        claim_id=claim.claim_id,
                        asset=asset,
                        status=FetchPlanStatus.EXCLUDED_PROVIDER_GAP,
                        exclusion_reason=rule.rationale,
                    )
                )
                continue
            start = claim.source_timestamp_utc - timedelta(days=lookback_days)
            end = claim.source_timestamp_utc + timedelta(days=forward_days)
            plans.append(
                MarketDataFetchPlan(
                    claim_id=claim.claim_id,
                    asset=asset,
                    status=FetchPlanStatus.PLANNED,
                    provider=rule.provider,
                    provider_symbol=rule.provider_symbol,
                    timeframe=rule.timeframe,
                    range_start_utc=start.isoformat(),
                    range_end_utc=end.isoformat(),
                )
            )
    return plans


def _unsupported_claim_plans(claim: StructuredClaim) -> list[MarketDataFetchPlan]:
    assets = claim.assets or ["unresolved"]
    return [
        MarketDataFetchPlan(
            claim_id=claim.claim_id,
            asset=asset,
            status=FetchPlanStatus.EXCLUDED_UNSUPPORTED_CLAIM_TYPE,
            exclusion_reason="claim_type_not_fetch_evaluable",
        )
        for asset in assets
    ]


def _non_directional_plans(claim: StructuredClaim) -> list[MarketDataFetchPlan]:
    assets = claim.assets or ["unresolved"]
    return [
        MarketDataFetchPlan(
            claim_id=claim.claim_id,
            asset=asset,
            status=FetchPlanStatus.EXCLUDED_NON_DIRECTIONAL,
            exclusion_reason="missing_or_mixed_direction",
        )
        for asset in assets
    ]


def mark_provider_fetch_failure(
    plan: MarketDataFetchPlan,
    *,
    error_code: str,
    retryable: bool,
    reason: str,
) -> MarketDataFetchPlan:
    return plan.model_copy(
        update={
            "status": (
                FetchPlanStatus.RETRY_PROVIDER_FAILURE
                if retryable
                else FetchPlanStatus.EXCLUDED_PROVIDER_FAILURE
            ),
            "exclusion_reason": reason,
            "provider_error_code": error_code,
            "retryable": retryable,
        }
    )
