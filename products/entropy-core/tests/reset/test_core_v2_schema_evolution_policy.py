"""Core V2 schema evolution policy contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
POLICY = PROJECT_ROOT / "docs" / "core" / "SCHEMA_EVOLUTION_POLICY.md"


def _policy_text() -> str:
    return POLICY.read_text(encoding="utf-8").lower()


def test_policy_defines_version_taxonomy_and_compatibility() -> None:
    text = _policy_text()

    for heading in (
        "## version taxonomy",
        "## compatibility categories",
        "## change rules",
    ):
        assert heading in text

    for version_part in ("major", "minor", "patch"):
        assert version_part in text

    for category in (
        "same_version",
        "backward_compatible",
        "migration_required",
        "unsupported_major",
        "malformed_version",
    ):
        assert category in text


def test_policy_defines_migration_records_and_append_only_evidence() -> None:
    text = _policy_text()

    assert "## migration record requirements" in text
    assert "## evidence binding" in text
    assert "append-only" in text
    assert "must not update or\ndelete prior migration records" in text

    for field in (
        "migration_id",
        "source_schema",
        "target_schema",
        "artifact_id",
        "source_artifact_hash",
        "target_artifact_hash",
        "migration_policy_hash",
        "migration_code_hash",
        "compatibility_category",
        "evidence_refs",
    ):
        assert field in text


def test_policy_preserves_blocked_surfaces() -> None:
    text = _policy_text()

    assert "## blocked surfaces" in text
    for blocked in (
        "holdout read or unlock",
        "oos/performance conclusions",
        "live feeds by default",
        "broker/exchange execution",
        "order placement or order blocking",
        "live capital",
        "production credentials",
        "production labels",
        "capital-ready labels",
        "public sdk",
        "hosted service or saas",
        "auth, sso, rbac, or tenant isolation",
        "external compliance certification",
        "enterprise sla claims",
    ):
        assert blocked in text

    assert "compatibility status is not an approval state" in text
