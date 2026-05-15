from __future__ import annotations

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_declares_console_script() -> None:
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text())

    project = pyproject["project"]
    dependencies = set(project["dependencies"])

    assert project["name"] == "signal-sandbox"
    assert project["requires-python"] == ">=3.12"
    assert "pydantic>=2" in dependencies
    assert "polars" in dependencies
    assert "pandas" in dependencies
    assert "ccxt" in dependencies
    assert "click" in dependencies
    assert pyproject["project"]["scripts"]["signal-sandbox"] == (
        "signal_sandbox.cli:main"
    )


def test_subpackages_exist() -> None:
    package_root = PROJECT_ROOT / "src" / "signal_sandbox"
    subpackages = [
        "sources",
        "capture",
        "extraction",
        "ledger",
        "prices",
        "outcomes",
        "reports",
    ]

    for subpackage in subpackages:
        init_file = package_root / subpackage / "__init__.py"
        assert init_file.is_file(), f"missing {init_file.relative_to(PROJECT_ROOT)}"
