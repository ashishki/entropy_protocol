"""Internal Python facade over stable artifact operations."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from entropy.artifacts.evidence import ArtifactEvidencePacket, build_artifact_evidence_packet
from entropy.artifacts.governance import (
    ArtifactGovernanceState,
    ArtifactGovernanceTransitionEvent,
    ArtifactGovernanceViolation,
    record_artifact_governance_transition,
)
from entropy.artifacts.profiles import ProductBridgeProfileViolation, validate_artifact_profile
from entropy.artifacts.registry import (
    ArtifactRegistryEvent,
    ArtifactRegistryRecord,
    register_artifact_file,
)
from entropy.artifacts.reproducibility import (
    ArtifactHashCompareRunner,
    ReproductionCompareResult,
    ReproducibilityManifest,
)
from entropy.artifacts.validation import (
    ArtifactValidationError,
    ArtifactValidationResult,
    validate_artifact_file,
)


def validate_artifact(path: str | Path, *, profile: str = "generic") -> ArtifactValidationResult:
    """Validate an artifact file with optional internal profile overlay."""
    result = validate_artifact_file(path)
    if not result.ok or result.artifact is None:
        return result
    try:
        validate_artifact_profile(result.artifact, profile)
    except ProductBridgeProfileViolation as exc:
        return ArtifactValidationResult(
            ok=False,
            errors=(
                ArtifactValidationError(
                    path="$",
                    code="artifact.profile_violation",
                    severity="P1",
                    message=str(exc),
                ),
            ),
        )
    return result


def register_artifact(
    path: str | Path,
    registry_dir: str | Path,
    *,
    profile: str = "generic",
) -> tuple[ArtifactRegistryRecord, ArtifactRegistryEvent]:
    """Validate profile boundaries and register an artifact."""
    result = validate_artifact(path, profile=profile)
    if not result.ok:
        raise ProductBridgeProfileViolation("Artifact could not be validated for profile.")
    return register_artifact_file(path, registry_dir)


def compare_artifact_output(
    manifest: ReproducibilityManifest,
    output_ref: str,
    expected_payload: dict[str, Any],
    actual_payload: dict[str, Any],
) -> ReproductionCompareResult:
    """Compare one actual payload against a reproducibility manifest."""
    return ArtifactHashCompareRunner().compare_json_output(
        manifest,
        output_ref,
        expected_payload,
        actual_payload,
    )


def build_evidence_packet(
    record: ArtifactRegistryRecord,
    *,
    limitations: tuple[str, ...] | None = None,
    review_refs: tuple[str, ...] = ("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",),
) -> ArtifactEvidencePacket:
    """Build an internal artifact evidence packet."""
    artifact = record.validation_result.artifact
    resolved_limitations = limitations
    if resolved_limitations is None and artifact is not None:
        resolved_limitations = artifact.limitations
    return build_artifact_evidence_packet(
        record,
        limitations=resolved_limitations or ("internal evidence packet",),
        review_refs=review_refs,
    )


def transition_artifact_state(
    artifact_id: str,
    next_state: str,
    governance_dir: str | Path,
    *,
    approval_event_ref: str | None = None,
    reason: str = "internal facade governance transition",
) -> ArtifactGovernanceTransitionEvent:
    """Record an internal governance transition using the same state rules as CLI."""
    try:
        return record_artifact_governance_transition(
            artifact_id,
            cast(ArtifactGovernanceState, next_state),
            governance_dir,
            approval_event_ref=approval_event_ref,
            reason=reason,
        )
    except ValueError as exc:
        raise ArtifactGovernanceViolation("Artifact governance transition is not allowed.") from exc


__all__ = [
    "build_evidence_packet",
    "compare_artifact_output",
    "register_artifact",
    "transition_artifact_state",
    "validate_artifact",
]
