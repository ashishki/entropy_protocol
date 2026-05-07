"""Reset-era migration append-only contract tests."""

from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_PATH = PROJECT_ROOT / "migrations" / "versions"
APPEND_ONLY_TABLES = ("trial_registry", "governance_events")


def _migration_files() -> list[Path]:
    return sorted(MIGRATIONS_PATH.glob("*.py"))


def test_migrations_preserve_append_only_tables() -> None:
    """Migrations create append-only tables without mutation triggers."""
    migration_text = "\n".join(path.read_text() for path in _migration_files())
    normalized_text = " ".join(migration_text.upper().split())
    created_tables = _created_tables()

    for table_name in APPEND_ONLY_TABLES:
        assert table_name in created_tables
        assert "CREATE TRIGGER" not in normalized_text
        assert "CREATE RULE" not in normalized_text
        assert f"UPDATE {table_name.upper()}" not in normalized_text
        assert f"DELETE FROM {table_name.upper()}" not in normalized_text


def _created_tables() -> set[str]:
    table_names: set[str] = set()
    for path in _migration_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            is_create_table = (
                isinstance(function, ast.Attribute)
                and function.attr == "create_table"
                and isinstance(function.value, ast.Name)
                and function.value.id == "op"
            )
            if not is_create_table or not node.args:
                continue
            table_arg = node.args[0]
            if isinstance(table_arg, ast.Constant) and isinstance(table_arg.value, str):
                table_names.add(table_arg.value)
    return table_names
