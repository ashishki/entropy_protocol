from __future__ import annotations

import json
import subprocess
import sys

from trader_risk_audit.observability import get_tracer


def test_import_has_no_heavy_runtime_dependencies() -> None:
    script = """
import importlib
import json
import sys

importlib.import_module("trader_risk_audit")
forbidden = {"pandas", "polars", "requests", "httpx", "aiohttp", "telegram"}
loaded = sorted(name for name in sys.modules if name.split(".")[0] in forbidden)
print(json.dumps(loaded))
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout) == []


def test_cli_help_lists_initial_command_surface() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "trader_risk_audit", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "audit" in result.stdout
    assert "manifest" in result.stdout
    assert "retention" in result.stdout


def test_shared_tracer_interface_exists() -> None:
    tracer = get_tracer()

    assert hasattr(tracer, "start_as_current_span")
    with tracer.start_as_current_span("baseline-smoke"):
        pass
