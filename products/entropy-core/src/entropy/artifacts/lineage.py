"""Deterministic artifact lineage graph builder."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Literal

from entropy.artifacts.audit_bundle import AuditLineageEdge, AuditLineageGraph, AuditLineageNode

LineageNodeType = Literal[
    "artifact",
    "input",
    "evidence_packet",
    "validation_event",
    "governance_event",
    "review_note",
    "unresolved",
]
LineageRelationship = Literal[
    "depends_on",
    "validates",
    "governs",
    "evidences",
    "reviews",
    "generates",
]

FORBIDDEN_LINEAGE_REF_MARKERS = (
    "api_key",
    "authorization",
    "credential",
    "customer",
    "password",
    "private_payload",
    "raw_payload",
    "raw_strategy",
    "secret",
    "token",
)


class LineageGraphViolation(ValueError):
    """Raised when lineage graph inputs would expose raw sensitive payloads."""


def build_artifact_lineage_graph(
    artifact_ref: str,
    *,
    input_refs: tuple[str, ...] = (),
    generated_refs: tuple[str, ...] = (),
    evidence_packet_refs: tuple[str, ...] = (),
    validation_event_refs: tuple[str, ...] = (),
    governance_event_refs: tuple[str, ...] = (),
    reviewer_note_refs: tuple[str, ...] = (),
    content_hashes: Mapping[str, str] | None = None,
) -> AuditLineageGraph:
    """Build a deterministic reference-only artifact lineage graph."""
    hashes = dict(content_hashes or {})
    artifact_node = _lineage_node(artifact_ref, "artifact", hashes)
    nodes: list[AuditLineageNode] = [artifact_node]
    edges: list[AuditLineageEdge] = []

    for ref in _unique_sorted(input_refs):
        node = _lineage_node(ref, "input", hashes)
        nodes.append(node)
        edges.append(_edge(artifact_node.node_id, node.node_id, "depends_on"))

    for ref in _unique_sorted(generated_refs):
        node = _lineage_node(ref, "artifact", hashes)
        nodes.append(node)
        edges.append(_edge(artifact_node.node_id, node.node_id, "generates"))

    for ref in _unique_sorted(evidence_packet_refs):
        node = _lineage_node(ref, "evidence_packet", hashes)
        nodes.append(node)
        edges.append(_edge(node.node_id, artifact_node.node_id, "evidences"))

    for ref in _unique_sorted(validation_event_refs):
        node = _lineage_node(ref, "validation_event", hashes)
        nodes.append(node)
        edges.append(_edge(node.node_id, artifact_node.node_id, "validates"))

    for ref in _unique_sorted(governance_event_refs):
        node = _lineage_node(ref, "governance_event", hashes)
        nodes.append(node)
        edges.append(_edge(node.node_id, artifact_node.node_id, "governs"))

    for ref in _unique_sorted(reviewer_note_refs):
        node = _lineage_node(ref, "review_note", hashes)
        nodes.append(node)
        edges.append(_edge(node.node_id, artifact_node.node_id, "reviews"))

    return AuditLineageGraph(nodes=tuple(nodes), edges=tuple(edges))


def _lineage_node(
    ref: str,
    node_type: LineageNodeType,
    content_hashes: Mapping[str, str],
) -> AuditLineageNode:
    _validate_safe_ref(ref)
    content_hash = content_hashes.get(ref)
    resolved_type = node_type if content_hash else "unresolved"
    return AuditLineageNode(
        node_id=_node_id(resolved_type, ref),
        node_type=resolved_type,
        ref=ref,
        content_hash=content_hash,
    )


def _edge(
    source_node_id: str,
    target_node_id: str,
    relationship: LineageRelationship,
) -> AuditLineageEdge:
    return AuditLineageEdge(
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        relationship=relationship,
    )


def _node_id(node_type: str, ref: str) -> str:
    digest = hashlib.sha256(ref.encode("utf-8")).hexdigest()[:16]
    return f"{node_type}:{digest}"


def _unique_sorted(refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(refs)))


def _validate_safe_ref(ref: str) -> None:
    normalized = _normalize_ref(ref)
    forbidden = tuple(marker for marker in FORBIDDEN_LINEAGE_REF_MARKERS if marker in normalized)
    if forbidden:
        raise LineageGraphViolation(
            "Lineage graph refs must not contain raw private payload markers: "
            + ", ".join(forbidden)
        )


def _normalize_ref(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(part for part in normalized.split("_") if part)


__all__ = [
    "FORBIDDEN_LINEAGE_REF_MARKERS",
    "LineageGraphViolation",
    "build_artifact_lineage_graph",
]
