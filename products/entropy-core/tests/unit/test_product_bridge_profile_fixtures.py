"""Unit tests for synthetic product-shaped artifact fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from entropy.artifacts import ProductBridgeProfileViolation, validate_artifact_file, validate_artifact_profile

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts" / "profiles"


def test_trader_fixture_profile_behavior() -> None:
    valid_result = validate_artifact_file(FIXTURES / "trader_valid.json")
    unsafe_result = validate_artifact_file(FIXTURES / "trader_unsafe_claim.json")

    assert valid_result.ok is True
    assert valid_result.artifact is not None
    assert validate_artifact_profile(valid_result.artifact, "trader-risk-audit") is valid_result.artifact
    assert unsafe_result.ok is True
    assert unsafe_result.artifact is not None
    with pytest.raises(ProductBridgeProfileViolation, match="forbidden no-claim labels"):
        validate_artifact_profile(unsafe_result.artifact, "trader-risk-audit")


def test_signal_fixture_profile_behavior() -> None:
    valid_result = validate_artifact_file(FIXTURES / "signal_valid.json")
    unsafe_result = validate_artifact_file(FIXTURES / "signal_unsafe_claim.json")

    assert valid_result.ok is True
    assert valid_result.artifact is not None
    assert (
        validate_artifact_profile(valid_result.artifact, "signal-analytics-sandbox")
        is valid_result.artifact
    )
    assert unsafe_result.ok is True
    assert unsafe_result.artifact is not None
    with pytest.raises(ProductBridgeProfileViolation, match="forbidden no-claim labels"):
        validate_artifact_profile(unsafe_result.artifact, "signal-analytics-sandbox")


def test_profile_fixtures_are_synthetic() -> None:
    forbidden_terms = (
        "api_key",
        "authorization",
        "credential",
        "customer",
        "password",
        "private key",
        "secret",
        "ssn",
        "token",
    )

    fixture_paths = tuple(sorted(FIXTURES.glob("*.json")))
    assert fixture_paths
    for path in fixture_paths:
        text = path.read_text(encoding="utf-8").lower()
        assert "synthetic" in text
        for term in forbidden_terms:
            assert term not in text, f"{path} contains forbidden fixture marker {term!r}"
