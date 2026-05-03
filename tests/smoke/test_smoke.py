"""Smoke tests for the project skeleton."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback
    import tomli as tomllib

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
GITIGNORE_PATH = PROJECT_ROOT / ".gitignore"
SUBPACKAGES = [
    "entropy.models",
    "entropy.db",
    "entropy.registry",
    "entropy.hashing",
    "entropy.data",
    "entropy.simbroker",
    "entropy.walkforward",
    "entropy.attribution",
    "entropy.governance",
    "entropy.stats",
    "entropy.evidence",
]
REQUIRED_RUNTIME_DEPS = {
    "pydantic>=2.0",
    "polars",
    "pyarrow",
    "duckdb",
    "sqlalchemy>=2.0",
    "alembic",
    "typer",
    "rich",
    "structlog",
    "opentelemetry-api",
}
REQUIRED_DEV_DEPS = {"pytest", "ruff", "pyright"}
REQUIRED_GITIGNORE_ENTRIES = {
    "__pycache__/",
    "*.pyc",
    ".env",
    "data/market/",
    ".pytest_cache/",
    "dist/",
    ".venv/",
}


def test_cli_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "entropy", "--help"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Entropy Protocol" in result.stdout
    assert "Usage" in result.stdout


def test_all_subpackages_importable() -> None:
    for module_name in SUBPACKAGES:
        module = importlib.import_module(module_name)
        assert module is not None


def test_pyproject_declares_required_deps() -> None:
    pyproject = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    project = pyproject["project"]
    runtime_deps = set(project["dependencies"])
    dev_deps = set(project["optional-dependencies"]["dev"])

    assert REQUIRED_RUNTIME_DEPS.issubset(runtime_deps)
    assert REQUIRED_DEV_DEPS.issubset(dev_deps)


def test_gitignore_has_required_entries() -> None:
    gitignore_entries = {
        line.strip()
        for line in GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }

    assert REQUIRED_GITIGNORE_ENTRIES.issubset(gitignore_entries)
