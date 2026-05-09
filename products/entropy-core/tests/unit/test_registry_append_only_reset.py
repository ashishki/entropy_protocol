"""Reset-era append-only registry and governance tests."""

from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from entropy.models.registry import TrialSpec
from entropy.registry.write import MissingHashError, register_trial


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATHS = (
    PROJECT_ROOT / "src" / "entropy" / "registry",
    PROJECT_ROOT / "src" / "entropy" / "governance",
)
APPEND_ONLY_TABLES = ("trial_registry", "governance_events")


class NoTouchSession:
    """Session double that fails if validation reaches any database operation."""

    def execute(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("missing hash validation reached database execute")

    def add(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("missing hash validation attempted database add")

    def flush(self) -> None:
        raise AssertionError("missing hash validation attempted database flush")


def _python_files() -> list[Path]:
    return sorted(path for root in APP_PATHS for path in root.rglob("*.py"))


def test_registry_governance_have_no_update_delete_paths() -> None:
    """Registry and governance app code must not mutate append-only tables."""
    offenders: list[str] = []

    for path in _python_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        relative_path = path.relative_to(PROJECT_ROOT)

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "sqlalchemy":
                imported_mutators = {"update", "delete"} & {alias.name for alias in node.names}
                for imported_name in sorted(imported_mutators):
                    offenders.append(f"{relative_path}: imports sqlalchemy.{imported_name}")

            if isinstance(node, ast.Call):
                function = node.func
                if isinstance(function, ast.Attribute) and function.attr == "delete":
                    offenders.append(f"{relative_path}: calls .delete()")
                if isinstance(function, ast.Name) and function.id in {"update", "delete"}:
                    offenders.append(f"{relative_path}: calls sqlalchemy {function.id}()")

            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                statement_text = " ".join(node.value.upper().split())
                for verb in ("UPDATE", "DELETE"):
                    for table_name in APPEND_ONLY_TABLES:
                        if f"{verb} {table_name.upper()}" in statement_text:
                            offenders.append(f"{relative_path}: contains {verb} for {table_name}")
                        if f"{verb} FROM {table_name.upper()}" in statement_text:
                            offenders.append(f"{relative_path}: contains {verb} for {table_name}")

    assert offenders == []


def test_missing_hash_blocks_before_write() -> None:
    """A missing reproducibility hash fails before duplicate checks or inserts."""
    trial_spec = TrialSpec.model_construct(
        trial_id="trial-missing-hash",
        family_tag="mean-reversion",
        hypothesis="Mean reversion after large one-hour moves.",
        dataset_hash="",
        code_hash="code-sha",
        policy_hash="policy-sha",
        parameter_lock={"lookback": 24},
        registered_at=datetime(2026, 5, 7, 12, 0, tzinfo=timezone.utc),
    )

    with pytest.raises(MissingHashError, match="dataset_hash"):
        register_trial(NoTouchSession(), trial_spec)  # type: ignore[arg-type]
