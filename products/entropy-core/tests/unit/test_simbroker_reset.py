"""Reset-era SimBroker regression tests."""

from __future__ import annotations

import ast
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from entropy.models.market import OHLCVBar
from entropy.models.registry import FillSide
from entropy.simbroker import CostModelConfig, FillSignal, process_fill


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SIMBROKER_ROOT = PROJECT_ROOT / "src" / "entropy" / "simbroker"
UTC_TS = datetime(2026, 5, 7, 12, 0, tzinfo=timezone.utc)


def test_simbroker_fill_logs_are_deterministic() -> None:
    """Identical fill inputs produce byte-identical fill logs."""
    signal = FillSignal(
        symbol="BTC-USD",
        side=FillSide.BUY,
        quantity=2.5,
        proposed_price=101.25,
    )
    bar = _bar()
    cost_config = _cost_config()

    first = process_fill(signal=signal, bar=bar, cost_config=cost_config)
    second = process_fill(signal=signal, bar=bar, cost_config=cost_config)

    assert first == second
    assert first.model_dump_json() == second.model_dump_json()


def test_simbroker_cost_components_are_separate() -> None:
    """Fill logs serialize cost components without merging them."""
    fill = process_fill(
        signal=FillSignal(
            symbol="BTC-USD",
            side=FillSide.SELL,
            quantity=3.0,
            proposed_price=99.5,
        ),
        bar=_bar(),
        cost_config=_cost_config(),
    )
    payload = fill.model_dump()

    for field_name in ("commission", "slippage", "market_impact", "borrow_rate", "funding_rate"):
        assert field_name in payload
    assert payload["commission"] > 0
    assert payload["slippage"] > 0
    assert payload["market_impact"] > 0
    assert payload["borrow_rate"] > 0
    assert payload["funding_rate"] > 0
    separated_total = (
        payload["commission"]
        + payload["slippage"]
        + payload["market_impact"]
        + payload["borrow_rate"]
        + payload["funding_rate"]
    )
    assert abs(payload["total_cost"] - separated_total) <= Decimal("1e-12")


def test_simbroker_has_no_live_broker_imports() -> None:
    """SimBroker must not import live broker or exchange API clients."""
    forbidden_fragments = {
        "alpaca",
        "binance",
        "ccxt",
        "coinbase",
        "ib_insync",
        "kraken",
    }
    offenders: list[str] = []

    for path in sorted(SIMBROKER_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            module_names: list[str] = []
            if isinstance(node, ast.Import):
                module_names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                module_names.append(node.module)
            for module_name in module_names:
                lowered = module_name.lower()
                if any(fragment in lowered for fragment in forbidden_fragments):
                    offenders.append(f"{path.relative_to(PROJECT_ROOT)} imports {module_name}")

    assert offenders == []


def _bar() -> OHLCVBar:
    return OHLCVBar(
        timestamp=UTC_TS,
        open=100.0,
        high=102.0,
        low=98.0,
        close=101.0,
        volume=1_000.0,
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
