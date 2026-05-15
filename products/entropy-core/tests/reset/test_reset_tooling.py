"""Reset-phase tooling contract tests."""

from __future__ import annotations

import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_requires_python_312() -> None:
    """The reset baseline runs on Python 3.12 tooling."""
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text())

    assert pyproject["project"]["requires-python"] == ">=3.12"
    assert pyproject["tool"]["ruff"]["target-version"] == "py312"
