"""Integration-style tests for artifact metadata migration contracts."""

from __future__ import annotations

import ast
from pathlib import Path

from entropy.db.models import Base

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_PATH = PROJECT_ROOT / "migrations" / "versions"
ARTIFACT_TABLES = {
    "artifact_records",
    "artifact_validation_events",
    "artifact_reproducibility_events",
    "artifact_evidence_packets",
    "artifact_governance_transition_events",
}
APPEND_ONLY_ARTIFACT_EVENT_TABLES = {
    "artifact_validation_events",
    "artifact_reproducibility_events",
    "artifact_governance_transition_events",
}
SAAS_MARKERS = (
    "tenant_id",
    "account_id",
    "organization_id",
    "auth_token",
    "api_key",
    "hosted_service",
    "public_api",
)


def test_artifact_metadata_tables_exist() -> None:
    created_tables = _created_tables()
    model_tables = set(Base.metadata.tables)

    assert ARTIFACT_TABLES.issubset(created_tables)
    assert ARTIFACT_TABLES.issubset(model_tables)
    assert _foreign_key_targets("artifact_validation_events") == {"artifact_records.artifact_id"}
    assert _foreign_key_targets("artifact_reproducibility_events") == {
        "artifact_records.artifact_id"
    }
    assert _foreign_key_targets("artifact_governance_transition_events") == {
        "artifact_records.artifact_id"
    }


def test_artifact_event_tables_are_append_only() -> None:
    migration_text = _migration_text().upper()
    source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PROJECT_ROOT / "src" / "entropy").rglob("*.py")
    ).upper()

    for table_name in APPEND_ONLY_ARTIFACT_EVENT_TABLES:
        assert table_name in _created_tables()
        assert f"UPDATE {table_name.upper()}" not in migration_text
        assert f"DELETE FROM {table_name.upper()}" not in migration_text
        assert f"UPDATE {table_name.upper()}" not in source_text
        assert f"DELETE FROM {table_name.upper()}" not in source_text


def test_migration_has_no_saas_assumptions() -> None:
    migration_text = _migration_text().lower()

    for marker in SAAS_MARKERS:
        assert marker not in migration_text


def _migration_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(MIGRATIONS_PATH.glob("*.py"))
    )


def _created_tables() -> set[str]:
    table_names: set[str] = set()
    for path in sorted(MIGRATIONS_PATH.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            if (
                isinstance(function, ast.Attribute)
                and function.attr == "create_table"
                and isinstance(function.value, ast.Name)
                and function.value.id == "op"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                table_names.add(node.args[0].value)
    return table_names


def _foreign_key_targets(table_name: str) -> set[str]:
    table = Base.metadata.tables[table_name]
    return {
        ".".join(foreign_key.target_fullname.split(".")[-2:]) for foreign_key in table.foreign_keys
    }
