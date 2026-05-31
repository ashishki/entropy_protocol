"""Unit tests for local evidence lookup primitives."""

from __future__ import annotations

from pathlib import Path

from entropy.artifacts import (
    EVIDENCE_LOOKUP_BLOCKED_SURFACES,
    lookup_evidence_index,
    lookup_packet_evidence_refs,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_INDEX = PROJECT_ROOT / "docs" / "EVIDENCE_INDEX.md"


def test_lookup_returns_exact_evidence_metadata() -> None:
    text = _evidence_index_text()
    result = lookup_evidence_index(text, "T125 Schema Compatibility Primitives")

    assert result.status == "found"
    assert result.topic == "T125 Schema Compatibility Primitives"
    assert result.artifact_type == "Test result"
    assert "src/entropy/artifacts/schema_compatibility.py" in result.locations
    assert result.canonical is True
    assert result.reason_code == "exact_evidence_match"
    assert result.approval_state == "not_approved"


def test_lookup_returns_insufficient_evidence_for_missing_topic() -> None:
    result = lookup_evidence_index(_evidence_index_text(), "T999 Missing Evidence")

    assert result.status == "insufficient_evidence"
    assert result.topic is None
    assert result.locations == ()
    assert result.reason_code == "evidence_topic_not_found"
    assert result.approval_state == "not_approved"


def test_lookup_result_is_redacted_and_non_approving() -> None:
    result = lookup_evidence_index(_evidence_index_text(), "T127 Evidence Lookup Policy Contract")
    serialized = result.model_dump_json()

    assert result.status == "found"
    assert result.blocked_surfaces == EVIDENCE_LOOKUP_BLOCKED_SURFACES
    for blocked in (
        "runtime_rag",
        "hosted_search",
        "public_api",
        "public_sdk",
        "live_execution",
        "holdout_access",
        "production_credentials",
        "capital",
        "external_compliance",
    ):
        assert blocked in result.blocked_surfaces
    assert "SECRET" not in serialized
    assert "customer" not in serialized
    assert "raw payload" not in serialized


def test_packet_lookup_metadata_alignment() -> None:
    results = lookup_packet_evidence_refs(
        _evidence_index_text(),
        ("T128 Local Evidence Lookup Primitives",),
    )

    assert len(results) == 1
    result = results[0]
    assert result.status == "found"
    assert result.topic == "T128 Local Evidence Lookup Primitives"
    assert result.artifact_type == "Test result"
    assert result.approval_state == "not_approved"


def test_missing_packet_refs_remain_insufficient_evidence() -> None:
    results = lookup_packet_evidence_refs(
        _evidence_index_text(),
        ("docs/audit/missing_packet.json",),
    )

    assert len(results) == 1
    assert results[0].status == "insufficient_evidence"
    assert results[0].reason_code == "evidence_topic_not_found"


def test_packet_lookup_alignment_is_non_approving() -> None:
    results = lookup_packet_evidence_refs(
        _evidence_index_text(),
        ("T127 Evidence Lookup Policy Contract", "missing-topic"),
    )

    assert {result.approval_state for result in results} == {"not_approved"}
    for result in results:
        assert result.blocked_surfaces == EVIDENCE_LOOKUP_BLOCKED_SURFACES


def _evidence_index_text() -> str:
    return EVIDENCE_INDEX.read_text(encoding="utf-8")
