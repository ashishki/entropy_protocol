"""Unit tests for synthetic CAF artifact fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from entropy.artifacts import AllocationDecisionArtifact, validate_artifact_payload

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts" / "caf"


def test_valid_caf_fixture_passes() -> None:
    artifact = load_caf_fixture("valid_allocation_decision.json")
    contract = artifact.to_artifact_contract()
    result = validate_artifact_payload(contract.model_dump(mode="json"))

    assert artifact.decision_id == "SYNTH-CAF-DECISION-001"
    assert artifact.artifact_type == "allocation_decision"
    assert result.ok is True
    assert result.artifact is not None
    assert result.artifact.product == "entropy-core-caf"


def test_unsafe_caf_variants_fail() -> None:
    for filename in (
        "unsafe_live_allocation.json",
        "unsafe_investment_advice.json",
        "unsafe_capital_ready.json",
    ):
        with pytest.raises(ValidationError, match="cannot claim advice"):
            load_caf_fixture(filename)


def test_caf_fixtures_are_synthetic() -> None:
    forbidden_terms = (
        "account",
        "api_key",
        "authorization",
        "broker_id",
        "capital_amount",
        "credential",
        "customer",
        "order_id",
        "password",
        "private",
        "raw_strategy",
        "secret",
        "token",
    )
    paths = tuple(sorted(FIXTURES.glob("*.json")))

    assert paths
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        assert "synthetic" in text
        for term in forbidden_terms:
            assert term not in text, f"{path} contains forbidden fixture marker {term!r}"


def load_caf_fixture(filename: str) -> AllocationDecisionArtifact:
    return AllocationDecisionArtifact.model_validate(
        json.loads((FIXTURES / filename).read_text(encoding="utf-8"))
    )
