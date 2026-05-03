"""Smoke tests for the project skeleton."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import duckdb

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback
    import tomli as tomllib

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
GITIGNORE_PATH = PROJECT_ROOT / ".gitignore"
CI_WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"
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
REQUIRED_CI_ENV_VARS = {
    "DATABASE_URL": "postgresql://entropy:entropy_test@localhost:5432/entropy_test",
    "ENTROPY_DATA_DIR": "/tmp/entropy_data",
    "ENTROPY_REGISTRY_DIR": "/tmp/entropy_registry",
    "LOG_LEVEL": "WARNING",
}
REQUIRED_CI_COMMANDS_IN_ORDER = [
    "ruff check entropy/ tests/",
    "ruff format --check entropy/ tests/",
    "pyright entropy/",
    "python3 -m pytest tests/ -q --tb=short",
]


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
    from entropy import cli
    from entropy.models import market, performance, registry

    assert cli is not None
    assert market is not None
    assert registry is not None
    assert performance is not None

    for module_name in SUBPACKAGES:
        module = importlib.import_module(module_name)
        assert module is not None


def test_postgres_connection_fixture(postgres_connection) -> None:
    assert postgres_connection.closed is False


def test_duckdb_embedded_query() -> None:
    result = duckdb.execute("SELECT 42 AS answer").fetchone()

    assert result is not None
    assert result[0] == 42


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


def test_ci_yml_declares_postgres_service() -> None:
    ci_text = CI_WORKFLOW_PATH.read_text(encoding="utf-8")

    assert CI_WORKFLOW_PATH.exists()
    assert "postgres:" in ci_text
    assert "image: postgres:16" in ci_text
    assert "POSTGRES_DB: entropy_test" in ci_text
    assert "POSTGRES_USER: entropy" in ci_text
    assert "POSTGRES_PASSWORD: entropy_test" in ci_text
    assert "- 5432:5432" in ci_text


def test_ci_yml_declares_required_env_vars() -> None:
    ci_text = CI_WORKFLOW_PATH.read_text(encoding="utf-8")

    for env_name, env_value in REQUIRED_CI_ENV_VARS.items():
        assert f"{env_name}: {env_value}" in ci_text


def test_ci_yml_includes_all_required_steps() -> None:
    ci_text = CI_WORKFLOW_PATH.read_text(encoding="utf-8")

    positions = [ci_text.index(command) for command in REQUIRED_CI_COMMANDS_IN_ORDER]
    assert positions == sorted(positions)


def test_ci_yml_triggers_on_push_and_pr() -> None:
    ci_text = CI_WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "on:" in ci_text
    assert "push:" in ci_text
    assert "- main" in ci_text
    assert "- master" in ci_text
    assert "pull_request:" in ci_text
