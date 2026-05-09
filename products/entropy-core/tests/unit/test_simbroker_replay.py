"""Unit tests for local no-capital SimBroker replay."""

from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path

import pytest

from entropy.models.market import OHLCVBar
from entropy.models.registry import FillSide
from entropy.simbroker import (
    LOCAL_REPLAY_SCOPE,
    PRODUCT_HYPOTHESIS_DELTA,
    CostModelConfig,
    FillSignal,
    SandboxReplayScenario,
    run_no_capital_sandbox_replay,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPLAY_MODULE = PROJECT_ROOT / "src" / "entropy" / "simbroker" / "replay.py"
UTC_TS = datetime(2026, 5, 9, 14, 0, tzinfo=timezone.utc)


def test_no_capital_sandbox_replay_is_deterministic_and_hash_bound() -> None:
    scenarios = _scenarios()
    cost_config = _cost_config()

    first = run_no_capital_sandbox_replay(
        scenarios=scenarios,
        cost_config=cost_config,
        approval_scope=LOCAL_REPLAY_SCOPE,
    )
    second = run_no_capital_sandbox_replay(
        scenarios=scenarios,
        cost_config=cost_config,
        approval_scope=LOCAL_REPLAY_SCOPE,
    )

    assert first == second
    assert first.replay_hash == second.replay_hash
    assert len(first.replay_hash) == 64
    assert first.scenario_count == 2
    assert len(first.fill_logs) == 2


def test_no_capital_sandbox_replay_preserves_no_effect_boundaries() -> None:
    result = run_no_capital_sandbox_replay(
        scenarios=_scenarios(),
        cost_config=_cost_config(),
        approval_scope=LOCAL_REPLAY_SCOPE,
    )

    assert result.no_order_emission is True
    assert result.no_broker_exchange_connection is True
    assert result.no_credential_loading is True
    assert result.no_capital_activation is True
    assert result.no_holdout_access is True
    assert result.product_hypothesis_delta == PRODUCT_HYPOTHESIS_DELTA
    assert result.product_hypothesis_delta != "confirmed"


def test_no_capital_sandbox_replay_rejects_invalid_scope_and_empty_scenarios() -> None:
    with pytest.raises(ValueError, match="approval_scope must be"):
        run_no_capital_sandbox_replay(
            scenarios=_scenarios(),
            cost_config=_cost_config(),
            approval_scope="production_capital_validation",
        )

    with pytest.raises(ValueError, match="at least one replay scenario"):
        run_no_capital_sandbox_replay(
            scenarios=(),
            cost_config=_cost_config(),
            approval_scope=LOCAL_REPLAY_SCOPE,
        )


def test_no_capital_sandbox_replay_rejects_duplicate_scenario_ids() -> None:
    scenario = _scenario(
        scenario_id="duplicate-scenario",
        side=FillSide.BUY,
        quantity=1.0,
        proposed_price=101.0,
    )

    with pytest.raises(ValueError, match="scenario_id values must be unique"):
        run_no_capital_sandbox_replay(
            scenarios=(scenario, scenario),
            cost_config=_cost_config(),
            approval_scope=LOCAL_REPLAY_SCOPE,
        )


def test_replay_module_has_no_live_broker_imports() -> None:
    forbidden_fragments = {
        "alpaca",
        "binance",
        "ccxt",
        "coinbase",
        "ib_insync",
        "kraken",
        "requests",
        "websocket",
    }
    tree = ast.parse(REPLAY_MODULE.read_text(), filename=str(REPLAY_MODULE))
    offenders: list[str] = []

    for node in ast.walk(tree):
        module_names: list[str] = []
        if isinstance(node, ast.Import):
            module_names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            module_names.append(node.module)
        for module_name in module_names:
            lowered = module_name.lower()
            if any(fragment in lowered for fragment in forbidden_fragments):
                offenders.append(module_name)

    assert offenders == []


def _scenarios() -> tuple[SandboxReplayScenario, ...]:
    return (
        _scenario(
            scenario_id="accepted-buy-fixture-fill",
            side=FillSide.BUY,
            quantity=1.25,
            proposed_price=101.25,
        ),
        _scenario(
            scenario_id="constrained-sell-fixture-fill",
            side=FillSide.SELL,
            quantity=0.75,
            proposed_price=98.0,
        ),
    )


def _scenario(
    *,
    scenario_id: str,
    side: FillSide,
    quantity: float,
    proposed_price: float,
) -> SandboxReplayScenario:
    return SandboxReplayScenario(
        scenario_id=scenario_id,
        signal=FillSignal(
            symbol="BTC-USD",
            side=side,
            quantity=quantity,
            proposed_price=proposed_price,
        ),
        bar=OHLCVBar(
            timestamp=UTC_TS,
            open=100.0,
            high=102.0,
            low=99.0,
            close=101.0,
            volume=1_000.0,
        ),
    )


def _cost_config() -> CostModelConfig:
    return CostModelConfig(
        fixed_commission=0.25,
        pct_commission=0.001,
        slippage_linear=0.0002,
        sqrt_impact_coef=0.0003,
        borrow_rate=0.0001,
        funding_rate=0.0004,
    )
