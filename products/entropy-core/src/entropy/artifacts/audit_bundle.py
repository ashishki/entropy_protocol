"""Exportable audit bundle schemas for governed artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

AUDIT_BUNDLE_SCHEMA_VERSION = "entropy-audit-bundle/v1"
AUDIT_BUNDLE_EXTERNAL_CERTIFICATION_STATUS = "not_claimed"
AUDIT_DATA_CLASSIFICATIONS = (
    "public",
    "internal",
    "confidential",
    "private_customer",
    "secret",
)
AUDIT_REVIEWER_ROLES = (
    "author",
    "validator",
    "risk_reviewer",
    "governance_reviewer",
    "audit_reviewer",
)
UNSUPPORTED_AUDIT_BUNDLE_CLAIM_LABELS = (
    "soc2",
    "soc_2",
    "regulatory_certification",
    "external_certification",
    "investment_advice_compliance",
    "enterprise_ready",
    "enterprise_readiness",
    "enterprise_sla",
)


class AuditBundleViolation(ValueError):
    """Raised when an audit bundle broadens its assurance claims."""


class AuditLineageNode(BaseModel):
    """One safe lineage graph node by reference, without raw payload data."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    node_id: str = Field(min_length=1)
    node_type: Literal[
        "artifact",
        "input",
        "evidence_packet",
        "validation_event",
        "governance_event",
        "review_note",
        "unresolved",
    ]
    ref: str = Field(min_length=1)
    content_hash: str | None = Field(default=None, min_length=1)


class AuditLineageEdge(BaseModel):
    """One deterministic relationship between lineage graph nodes."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    source_node_id: str = Field(min_length=1)
    target_node_id: str = Field(min_length=1)
    relationship: Literal["depends_on", "validates", "governs", "evidences", "reviews", "generates"]


class AuditLineageGraph(BaseModel):
    """Deterministic lineage graph embedded in an audit bundle."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    nodes: tuple[AuditLineageNode, ...] = Field(min_length=1)
    edges: tuple[AuditLineageEdge, ...] = ()

    @model_validator(mode="after")
    def validate_graph_refs(self) -> "AuditLineageGraph":
        node_ids = tuple(node.node_id for node in self.nodes)
        if len(set(node_ids)) != len(node_ids):
            raise AuditBundleViolation("Lineage graph node ids must be unique.")
        missing_refs = tuple(
            node_id
            for edge in self.edges
            for node_id in (edge.source_node_id, edge.target_node_id)
            if node_id not in node_ids
        )
        if missing_refs:
            raise AuditBundleViolation(
                "Lineage graph edges must reference known nodes: "
                + ", ".join(sorted(set(missing_refs)))
            )
        return self


class AuditBundleContentHash(BaseModel):
    """Content hash bound to an audit bundle artifact reference."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    ref: str = Field(min_length=1)
    sha256: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_sha256_prefix(self) -> "AuditBundleContentHash":
        if not self.sha256.startswith("sha256:"):
            raise AuditBundleViolation("Audit bundle content hashes must use sha256: prefix.")
        return self


class AuditBundleValidationEvent(BaseModel):
    """Validation event metadata carried by an audit bundle."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    event_id: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    validation_status: Literal["ok", "failed", "not_checked"]
    validation_ref: str = Field(min_length=1)


class AuditBundleGovernanceEvent(BaseModel):
    """Governance event metadata carried by an audit bundle."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    event_id: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    prior_state: str = Field(min_length=1)
    next_state: str = Field(min_length=1)
    event_ref: str = Field(min_length=1)


class AuditBundleReviewerNote(BaseModel):
    """Reviewer note reference and decision metadata."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    note_id: str = Field(min_length=1)
    reviewer_ref: str = Field(min_length=1)
    section_ref: str = Field(min_length=1)
    decision: Literal["accepted", "accepted_with_limitations", "needs_follow_up", "rejected"]
    notes_ref: str = Field(min_length=1)
    limitations: tuple[str, ...] = Field(min_length=1)


class AuditDataClassificationRef(BaseModel):
    """Data classification metadata for one bundle reference."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    ref: str = Field(min_length=1)
    classification: Literal["public", "internal", "confidential", "private_customer", "secret"]
    rationale: str = Field(min_length=1)


class AuditReviewerRoleMetadata(BaseModel):
    """Reviewer role metadata without implementing authorization behavior."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    reviewer_id: str = Field(min_length=1)
    reviewer_ref: str = Field(min_length=1)
    role: Literal["author", "validator", "risk_reviewer", "governance_reviewer", "audit_reviewer"]
    reviewed_sections: tuple[str, ...] = Field(min_length=1)
    decision: Literal["accepted", "accepted_with_limitations", "needs_follow_up", "rejected"]
    reviewed_at: datetime
    limitations: tuple[str, ...] = Field(min_length=1)


class AuditBundle(BaseModel):
    """Exportable audit package for one governed artifact."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    audit_bundle_version: Literal["entropy-audit-bundle/v1"] = AUDIT_BUNDLE_SCHEMA_VERSION
    bundle_id: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    lineage_graph: AuditLineageGraph
    evidence_packet_refs: tuple[str, ...] = Field(min_length=1)
    validation_events: tuple[AuditBundleValidationEvent, ...] = Field(min_length=1)
    governance_events: tuple[AuditBundleGovernanceEvent, ...] = Field(min_length=1)
    reviewer_notes: tuple[AuditBundleReviewerNote, ...] = Field(min_length=1)
    limitations: tuple[str, ...] = Field(min_length=1)
    claim_boundary: tuple[str, ...] = Field(min_length=1)
    content_hashes: tuple[AuditBundleContentHash, ...] = Field(min_length=1)
    data_classifications: tuple[AuditDataClassificationRef, ...] = ()
    reviewer_roles: tuple[AuditReviewerRoleMetadata, ...] = ()
    external_certification_status: Literal["not_claimed"] = (
        AUDIT_BUNDLE_EXTERNAL_CERTIFICATION_STATUS
    )

    @model_validator(mode="after")
    def validate_audit_claim_boundary(self) -> "AuditBundle":
        unsafe = tuple(label for label in self.claim_boundary if _is_unsupported_unblocked(label))
        if unsafe:
            raise AuditBundleViolation(
                "Audit bundles cannot claim external certification, investment-advice "
                "compliance, enterprise readiness, or enterprise SLA: "
                + ", ".join(unsafe)
            )
        return self

    def to_deterministic_json(self) -> str:
        """Serialize this audit bundle deterministically."""
        return json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))

    def bundle_hash(self) -> str:
        """Return a stable hash of the deterministic bundle payload."""
        digest = hashlib.sha256(self.to_deterministic_json().encode("utf-8")).hexdigest()
        return "sha256:" + digest


def _is_unsupported_unblocked(label: str) -> bool:
    normalized = _normalize_label(label)
    if normalized.startswith(("not_", "no_", "non_", "blocked_", "without_")):
        return False
    return any(claim in normalized for claim in UNSUPPORTED_AUDIT_BUNDLE_CLAIM_LABELS)


def _normalize_label(value: str) -> str:
    normalized = "".join(character if character.isalnum() else "_" for character in value.lower())
    return "_".join(part for part in normalized.split("_") if part)


__all__ = [
    "AUDIT_DATA_CLASSIFICATIONS",
    "AUDIT_BUNDLE_EXTERNAL_CERTIFICATION_STATUS",
    "AUDIT_BUNDLE_SCHEMA_VERSION",
    "AUDIT_REVIEWER_ROLES",
    "UNSUPPORTED_AUDIT_BUNDLE_CLAIM_LABELS",
    "AuditBundle",
    "AuditBundleContentHash",
    "AuditDataClassificationRef",
    "AuditBundleGovernanceEvent",
    "AuditBundleReviewerNote",
    "AuditReviewerRoleMetadata",
    "AuditBundleValidationEvent",
    "AuditBundleViolation",
    "AuditLineageEdge",
    "AuditLineageGraph",
    "AuditLineageNode",
]
