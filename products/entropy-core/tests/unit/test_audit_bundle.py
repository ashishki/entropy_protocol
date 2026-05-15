"""Unit tests for exportable artifact audit bundles."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    AUDIT_BUNDLE_SCHEMA_VERSION,
    AuditBundle,
    AuditLineageGraph,
)


def test_audit_bundle_requires_lineage_sections() -> None:
    bundle = audit_bundle()

    assert bundle.audit_bundle_version == AUDIT_BUNDLE_SCHEMA_VERSION
    assert isinstance(bundle.lineage_graph, AuditLineageGraph)
    assert bundle.evidence_packet_refs == ("docs/audit/generated/evidence/artifact-001.json",)
    assert bundle.validation_events[0].validation_status == "ok"
    assert bundle.governance_events[0].next_state == "validated_internal"
    assert bundle.reviewer_notes[0].decision == "accepted_with_limitations"
    assert bundle.limitations == ("internal audit readiness bundle only",)

    with pytest.raises(ValidationError):
        audit_bundle(evidence_packet_refs=())

    with pytest.raises(ValidationError):
        audit_bundle(reviewer_notes=())


def test_audit_bundle_serializes_deterministically() -> None:
    bundle = audit_bundle()
    duplicate = audit_bundle()

    assert bundle.to_deterministic_json() == duplicate.to_deterministic_json()
    assert json.dumps(
        bundle.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    ) == bundle.to_deterministic_json()
    assert bundle.bundle_hash().startswith("sha256:")
    assert bundle.bundle_hash() == duplicate.bundle_hash()
    assert bundle.content_hashes[0].sha256 == "sha256:artifact001"

    with pytest.raises(ValidationError, match="sha256"):
        audit_bundle(content_hashes=({"ref": "artifact-001", "sha256": "artifact001"},))


@pytest.mark.parametrize(
    "unsafe_claim",
    (
        "soc2_certified",
        "regulatory_certification",
        "investment_advice_compliance",
        "enterprise_ready",
        "enterprise_sla",
    ),
)
def test_audit_bundle_rejects_external_certification_claims(unsafe_claim: str) -> None:
    with pytest.raises(ValidationError, match="cannot claim external certification"):
        audit_bundle(claim_boundary=(*base_claim_boundary(), unsafe_claim))

    with pytest.raises(ValidationError):
        audit_bundle(external_certification_status="soc2_certified")


def audit_bundle(**overrides: object) -> AuditBundle:
    payload: dict[str, object] = {
        "bundle_id": "SYNTH-AUDIT-BUNDLE-001",
        "artifact_ref": "artifacts/core/artifact-001.json",
        "lineage_graph": {
            "nodes": (
                {
                    "node_id": "artifact-001",
                    "node_type": "artifact",
                    "ref": "artifacts/core/artifact-001.json",
                    "content_hash": "sha256:artifact001",
                },
                {
                    "node_id": "evidence-001",
                    "node_type": "evidence_packet",
                    "ref": "docs/audit/generated/evidence/artifact-001.json",
                    "content_hash": "sha256:evidence001",
                },
            ),
            "edges": (
                {
                    "source_node_id": "evidence-001",
                    "target_node_id": "artifact-001",
                    "relationship": "evidences",
                },
            ),
        },
        "evidence_packet_refs": ("docs/audit/generated/evidence/artifact-001.json",),
        "validation_events": (
            {
                "event_id": "validation-001",
                "artifact_ref": "artifacts/core/artifact-001.json",
                "validation_status": "ok",
                "validation_ref": "registry/events/validation-001.json",
            },
        ),
        "governance_events": (
            {
                "event_id": "governance-001",
                "artifact_ref": "artifacts/core/artifact-001.json",
                "prior_state": "draft",
                "next_state": "validated_internal",
                "event_ref": "registry/events/governance-001.json",
            },
        ),
        "reviewer_notes": (
            {
                "note_id": "review-001",
                "reviewer_ref": "internal-reviewer/synthetic",
                "section_ref": "sections/limitations",
                "decision": "accepted_with_limitations",
                "notes_ref": "reviews/synthetic-review-001.md",
                "limitations": ("synthetic internal review note only",),
            },
        ),
        "limitations": ("internal audit readiness bundle only",),
        "claim_boundary": base_claim_boundary(),
        "content_hashes": (
            {"ref": "artifacts/core/artifact-001.json", "sha256": "sha256:artifact001"},
            {"ref": "docs/audit/generated/evidence/artifact-001.json", "sha256": "sha256:evidence001"},
        ),
    }
    payload.update(overrides)
    return AuditBundle.model_validate(payload)


def base_claim_boundary() -> tuple[str, ...]:
    return (
        "not_soc2_certified",
        "not_regulatory_certification",
        "not_investment_advice_compliance",
        "not_enterprise_ready",
        "not_enterprise_sla",
    )
