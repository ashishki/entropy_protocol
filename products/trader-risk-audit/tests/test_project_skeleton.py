from __future__ import annotations

import subprocess
import sys

import pytest

import trader_risk_audit
from trader_risk_audit.config import ConfigError, load_settings


def test_package_exposes_version() -> None:
    assert isinstance(trader_risk_audit.__version__, str)
    assert trader_risk_audit.__version__


def test_module_version_command() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "trader_risk_audit", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert trader_risk_audit.__version__ in result.stdout


def test_config_rejects_live_trading_flags() -> None:
    defaults = load_settings({})
    assert defaults.live_broker_api_enabled is False
    assert defaults.order_blocking_enabled is False

    with pytest.raises(ConfigError, match="TRA_LIVE_BROKER_API_ENABLED"):
        load_settings({"TRA_LIVE_BROKER_API_ENABLED": "true"})

    with pytest.raises(ConfigError, match="TRA_ORDER_BLOCKING_ENABLED"):
        load_settings({"TRA_ORDER_BLOCKING_ENABLED": "true"})
