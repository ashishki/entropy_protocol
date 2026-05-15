"""Unit tests for artifact lineage graph building."""

from __future__ import annotations

import pytest

from entropy.artifacts import LineageGraphViolation, build_artifact_lineage_graph


def test_lineage_graph_is_deterministic() -> None:
    graph = build_artifact_lineage_graph(
        "artifacts/core/artifact-001.json",
        input_refs=("inputs/policy.json", "inputs/dataset.json"),
        generated_refs=("artifacts/core/report-001.json",),
        evidence_packet_refs=("docs/audit/generated/evidence/artifact-001.json",),
        validation_event_refs=("registry/events/validation-001.json",),
        governance_event_refs=("registry/events/governance-001.json",),
        reviewer_note_refs=("reviews/synthetic-review-001.md",),
        content_hashes=content_hashes(),
    )
    reordered = build_artifact_lineage_graph(
        "artifacts/core/artifact-001.json",
        input_refs=("inputs/dataset.json", "inputs/policy.json"),
        generated_refs=("artifacts/core/report-001.json",),
        evidence_packet_refs=("docs/audit/generated/evidence/artifact-001.json",),
        validation_event_refs=("registry/events/validation-001.json",),
        governance_event_refs=("registry/events/governance-001.json",),
        reviewer_note_refs=("reviews/synthetic-review-001.md",),
        content_hashes=content_hashes(),
    )

    assert graph.model_dump(mode="json") == reordered.model_dump(mode="json")
    assert [node.node_type for node in graph.nodes] == [
        "artifact",
        "input",
        "input",
        "artifact",
        "evidence_packet",
        "validation_event",
        "governance_event",
        "review_note",
    ]
    assert [edge.relationship for edge in graph.edges] == [
        "depends_on",
        "depends_on",
        "generates",
        "evidences",
        "validates",
        "governs",
        "reviews",
    ]


def test_lineage_graph_records_unresolved_refs() -> None:
    graph = build_artifact_lineage_graph(
        "artifacts/core/artifact-001.json",
        input_refs=("inputs/missing-policy.json",),
        evidence_packet_refs=("docs/audit/generated/evidence/artifact-001.json",),
        content_hashes={
            "artifacts/core/artifact-001.json": "sha256:artifact001",
            "docs/audit/generated/evidence/artifact-001.json": "sha256:evidence001",
        },
    )

    unresolved = tuple(node for node in graph.nodes if node.node_type == "unresolved")
    assert len(unresolved) == 1
    assert unresolved[0].ref == "inputs/missing-policy.json"
    assert unresolved[0].content_hash is None


def test_lineage_graph_avoids_private_payloads() -> None:
    graph = build_artifact_lineage_graph(
        "artifacts/core/artifact-001.json",
        input_refs=("inputs/synthetic-policy.json",),
        content_hashes={
            "artifacts/core/artifact-001.json": "sha256:artifact001",
            "inputs/synthetic-policy.json": "sha256:policy001",
        },
    )
    serialized = str(graph.model_dump(mode="json")).lower()

    assert "raw_payload" not in serialized
    assert "customer" not in serialized
    assert "secret" not in serialized

    with pytest.raises(LineageGraphViolation, match="raw private payload"):
        build_artifact_lineage_graph(
            "artifacts/core/artifact-001.json",
            input_refs=("raw_payload/customer-secret-strategy.json",),
            content_hashes={"artifacts/core/artifact-001.json": "sha256:artifact001"},
        )


def content_hashes() -> dict[str, str]:
    return {
        "artifacts/core/artifact-001.json": "sha256:artifact001",
        "inputs/dataset.json": "sha256:dataset001",
        "inputs/policy.json": "sha256:policy001",
        "artifacts/core/report-001.json": "sha256:report001",
        "docs/audit/generated/evidence/artifact-001.json": "sha256:evidence001",
        "registry/events/validation-001.json": "sha256:validation001",
        "registry/events/governance-001.json": "sha256:governance001",
        "reviews/synthetic-review-001.md": "sha256:review001",
    }
