"""Unit tests for audit data classification and reviewer role metadata."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    AUDIT_DATA_CLASSIFICATIONS,
    AuditDataClassificationRef,
    AuditReviewerRoleMetadata,
)


def test_data_classification_lists_required_categories() -> None:
    assert AUDIT_DATA_CLASSIFICATIONS == (
        "public",
        "internal",
        "confidential",
        "private_customer",
        "secret",
    )
    classification = AuditDataClassificationRef(
        ref="artifacts/core/artifact-001.json",
        classification="confidential",
        rationale="artifact metadata may contain internal governance references",
    )

    assert classification.classification == "confidential"

    with pytest.raises(ValidationError):
        AuditDataClassificationRef(
            ref="artifacts/core/artifact-001.json",
            classification="restricted",  # type: ignore[arg-type]
            rationale="not a frozen category",
        )


def test_reviewer_role_metadata_requires_review_fields() -> None:
    reviewed_at = datetime(2026, 5, 14, 12, 0, tzinfo=UTC)
    metadata = AuditReviewerRoleMetadata(
        reviewer_id="synthetic-reviewer-001",
        reviewer_ref="internal-reviewer/synthetic",
        role="audit_reviewer",
        reviewed_sections=("lineage", "limitations"),
        decision="accepted_with_limitations",
        reviewed_at=reviewed_at,
        limitations=("synthetic metadata only",),
    )

    assert metadata.reviewer_id == "synthetic-reviewer-001"
    assert metadata.role == "audit_reviewer"
    assert metadata.reviewed_sections == ("lineage", "limitations")
    assert metadata.decision == "accepted_with_limitations"
    assert metadata.reviewed_at == reviewed_at
    assert metadata.limitations == ("synthetic metadata only",)

    with pytest.raises(ValidationError):
        AuditReviewerRoleMetadata.model_validate(
            {
                "reviewer_id": "synthetic-reviewer-001",
                "reviewer_ref": "internal-reviewer/synthetic",
                "role": "audit_reviewer",
                "reviewed_sections": ("lineage",),
                "decision": "accepted",
                "limitations": ("missing timestamp",),
            }
        )


def test_model_has_no_auth_or_tenant_behavior() -> None:
    forbidden_field_markers = ("auth", "sso", "rbac", "tenant")
    classification_fields = set(AuditDataClassificationRef.model_fields)
    reviewer_fields = set(AuditReviewerRoleMetadata.model_fields)

    for marker in forbidden_field_markers:
        assert all(marker not in field for field in classification_fields)
        assert all(marker not in field for field in reviewer_fields)

    with pytest.raises(ValidationError):
        AuditReviewerRoleMetadata.model_validate(
            {
                "reviewer_id": "synthetic-reviewer-001",
                "reviewer_ref": "internal-reviewer/synthetic",
                "role": "audit_reviewer",
                "reviewed_sections": ("lineage",),
                "decision": "accepted",
                "reviewed_at": "2026-05-14T12:00:00Z",
                "limitations": ("synthetic metadata only",),
                "sso_provider": "not-supported",
            }
        )
