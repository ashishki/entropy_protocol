from __future__ import annotations

from pathlib import Path

from signal_sandbox.claims import (
    FetchPlanStatus,
    ProviderProxyStatus,
    default_provider_proxy_config,
    plan_market_data_fetches,
)
from tests.unit.test_provider_proxy_config_v1 import _claim

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_futures_commodity_policy_defines_contract_rollover_provider_rules() -> None:
    policy = (PROJECT_ROOT / "docs/specs/FUTURES_COMMODITY_PROXY_POLICY.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Rollover rule",
        "Provider",
        "Direction semantics",
        "`BR`",
        "`NG`",
        "`GOLD`",
        "`SI`",
        "`MIX`",
        "`IMOEX`",
        "Do not use continuous futures without a rollover rule",
    ):
        assert required in policy


def test_futures_commodity_symbols_remain_provider_gap_exclusions() -> None:
    config = default_provider_proxy_config()

    for symbol in ("BR", "NG", "GOLD", "SI", "MIX", "IMOEX"):
        assert config.resolve(symbol).status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT

    plans = plan_market_data_fetches([_claim("claim-futures", ["BR", "GOLD"])])
    assert [plan.status for plan in plans] == [
        FetchPlanStatus.EXCLUDED_PROVIDER_GAP,
        FetchPlanStatus.EXCLUDED_PROVIDER_GAP,
    ]
    assert all(plan.provider is None for plan in plans)
