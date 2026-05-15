"""Unit tests for synthetic research artifact fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from entropy.artifacts import ResearchArtifact, validate_artifact_payload

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts" / "research"


def test_valid_research_artifact_fixture_passes() -> None:
    artifact = load_research_fixture("valid_research_artifact.json")
    contract = artifact.to_artifact_contract()
    result = validate_artifact_payload(contract.model_dump(mode="json"))

    assert artifact.candidate_id == "SYNTH-RESEARCH-001"
    assert result.ok is True
    assert result.artifact is not None
    assert "not_oos_performance" in result.artifact.no_claim_boundary


def test_unsafe_research_claim_variants_fail() -> None:
    for filename in ("unsafe_oos_performance.json", "unsafe_holdout_claim.json"):
        with pytest.raises(ValidationError, match="cannot claim OOS/performance"):
            load_research_fixture(filename)


def test_research_fixtures_are_synthetic() -> None:
    forbidden_terms = (
        "api_key",
        "authorization",
        "credential",
        "customer",
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


def load_research_fixture(filename: str) -> ResearchArtifact:
    return ResearchArtifact.model_validate(
        json.loads((FIXTURES / filename).read_text(encoding="utf-8"))
    )
