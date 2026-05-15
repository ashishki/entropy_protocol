"""Reset-phase CI workflow contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CI_WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"


def _ci_text() -> str:
    return CI_WORKFLOW.read_text()


def _normalized_ci_text() -> str:
    return " ".join(_ci_text().split())


def test_ci_uses_python_312_and_dev_install() -> None:
    """CI installs the local package with reset-era Python tooling."""
    ci_text = _normalized_ci_text()

    assert 'python-version: "3.12"' in ci_text
    assert 'pip install -e ".[dev]"' in ci_text
    assert "working-directory: products/entropy-core" in ci_text


def test_ci_runs_required_quality_commands() -> None:
    """CI runs each required verification command as its own step."""
    ci_text = _ci_text()

    assert "run: python -m pytest -q tests/" in ci_text
    assert "run: ruff check src/entropy tests" in ci_text
    assert "run: ruff format --check src/entropy tests" in ci_text
    assert "run: pyright src/entropy" in ci_text


def test_ci_has_no_live_trading_credentials() -> None:
    """CI may define only local test service credentials, never live trading secrets."""
    ci_text = _ci_text()
    lower_ci_text = ci_text.lower()

    assert "image: postgres:16" in ci_text
    assert "postgres:" in lower_ci_text

    forbidden_fragments = {
        "broker_api",
        "broker_key",
        "broker_secret",
        "exchange_api",
        "exchange_key",
        "exchange_secret",
        "live_data",
        "live_feed",
        "live_trading",
        "binance_api",
        "coinbase_api",
        "alpaca_api",
        "kraken_api",
    }
    assert not any(fragment in lower_ci_text for fragment in forbidden_fragments)
