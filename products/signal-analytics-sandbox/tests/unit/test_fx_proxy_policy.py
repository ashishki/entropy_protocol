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


def test_fx_proxy_policy_defines_pair_direction_provider_and_exclusions() -> None:
    policy = (PROJECT_ROOT / "docs/specs/FX_PROXY_POLICY.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Pair",
        "Direction semantics",
        "Provider",
        "Horizon",
        "Exclusions",
        "Do not silently map `CNY`, `CN`, `USD`, `EUR`",
    ):
        assert required in policy


def test_fx_shorthand_is_not_silently_mapped_to_provider_route() -> None:
    config = default_provider_proxy_config()

    assert config.resolve("CNY").status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT
    assert config.resolve("CN").status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT
    assert config.resolve("USD").status == ProviderProxyStatus.UNSUPPORTED

    plans = plan_market_data_fetches([_claim("claim-cny", ["CNY"])])
    assert plans[0].status == FetchPlanStatus.EXCLUDED_PROVIDER_GAP
    assert plans[0].provider is None
