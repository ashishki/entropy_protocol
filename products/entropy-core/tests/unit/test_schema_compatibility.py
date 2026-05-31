"""Unit tests for Core V2 schema compatibility primitives."""

from __future__ import annotations

from entropy.artifacts import (
    SCHEMA_COMPATIBILITY_BLOCKED_SURFACES,
    classify_schema_compatibility,
    parse_schema_version,
)


def test_schema_compatibility_classification() -> None:
    assert parse_schema_version("entropy-core-artifact/v1") is not None

    same = classify_schema_compatibility("entropy-core-artifact/v1", "entropy-core-artifact/v1.0.0")
    backward = classify_schema_compatibility(
        "entropy-core-artifact/v1.0.0",
        "entropy-core-artifact/v1.1.0",
    )
    migration = classify_schema_compatibility(
        "entropy-core-artifact/v1.1.0",
        "entropy-core-artifact/v2.0.0",
        supported_major_versions=(1, 2),
    )
    unsupported = classify_schema_compatibility(
        "entropy-core-artifact/v1.0.0",
        "entropy-core-artifact/v99.0.0",
    )
    malformed = classify_schema_compatibility(
        "entropy-core-artifact/v1",
        "entropy-core-artifact/latest",
    )

    assert same.category == "same_version"
    assert backward.category == "backward_compatible"
    assert migration.category == "migration_required"
    assert unsupported.category == "unsupported_major"
    assert malformed.category == "malformed_version"


def test_schema_compatibility_result_is_redacted() -> None:
    result = classify_schema_compatibility(
        "entropy-core-artifact/v1.1.0",
        "entropy-core-artifact/v1.0.0",
    )
    serialized = result.model_dump_json()

    assert result.category == "migration_required"
    assert result.reason_code == "target_version_is_older_than_source"
    assert "SECRET" not in serialized
    assert "payload" not in serialized
    assert "customer" not in serialized


def test_schema_compatibility_does_not_approve_restricted_surfaces() -> None:
    result = classify_schema_compatibility(
        "entropy-core-artifact/v1.0.0",
        "entropy-core-artifact/v1.1.0",
    )

    assert result.approval_state == "not_approved"
    assert result.blocked_surfaces == SCHEMA_COMPATIBILITY_BLOCKED_SURFACES
    for blocked in (
        "public_sdk",
        "hosted_service",
        "live_execution",
        "holdout_access",
        "production_credentials",
        "capital",
        "external_compliance",
    ):
        assert blocked in result.blocked_surfaces
