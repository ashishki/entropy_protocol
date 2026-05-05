"""Bounded long-only baseline implementation surface for Phase 1B.

This module defines interfaces and schema guards only. It does not compute
alpha, scores, weights, P&L, backtests, OOS labels, or phase-gate evidence.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass

from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_VALIDATION_LABEL,
)
from entropy.evidence.phase1a_scaffold import (
    PHASE1A_BASELINE_SCAFFOLD_ID,
    PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY,
    Phase1ABaselineScaffold,
)

PHASE1B_BASELINE_SURFACE_ID = "PHASE1B-LONG-ONLY-BASELINE-SURFACE-v1"

PHASE1B_BASELINE_NO_CLAIM_LABELS: tuple[str, ...] = (
    "implementation_surface_only",
    "not_alpha_logic",
    "not_portfolio_allocation",
    "not_backtest",
    "not_oos",
    "not_performance_evidence",
    "not_phase_gate_evidence",
)

PHASE1B_BASELINE_ALLOWED_BACKENDS: tuple[str, ...] = (
    "python_polars_compatible",
    "python_schema_only",
)

PHASE1B_REQUIRED_OUTPUT_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp_utc",
    "skill_family",
    "observation_status",
    "surface_id",
    "scaffold_id",
    "baseline_spec_hash",
    "no_claim_label",
)

PHASE1B_FORBIDDEN_OUTPUT_COLUMNS: tuple[str, ...] = (
    "alpha",
    "alpha_score",
    "score",
    "signal",
    "signal_score",
    "weight",
    "target_weight",
    "position_size",
    "pnl",
    "return",
    "returns",
    "sharpe",
    "drawdown",
    "oos_label",
    "performance_metric",
    "phase_gate_status",
)


@dataclass(frozen=True)
class Phase1BSkillInterface:
    """Interface state for one long-only baseline skill family."""

    family: str
    interface_id: str
    implementation_status: str = "interface_only_no_alpha_logic"
    input_status: str = "formation_schema_allowed"
    output_status: str = "schema_only_no_signal_no_score_no_weight"


@dataclass(frozen=True)
class Phase1BBaselineSurface:
    """Bounded Phase 1B long-only baseline implementation surface."""

    surface_id: str
    scaffold_id: str
    registration_id: str
    registration_instance_id: str
    spec_id: str
    baseline_spec_hash: str
    validation_registration_hash: str
    allowed_split_labels: tuple[str, ...]
    denied_split_labels: tuple[str, ...]
    skill_interfaces: tuple[Phase1BSkillInterface, ...]
    required_output_columns: tuple[str, ...]
    forbidden_output_columns: tuple[str, ...]
    no_claim_labels: tuple[str, ...]
    workload_boundary: str
    gate_claim_allowed: bool = False
    evaluation_allowed: bool = False
    archive_only: bool = True


@dataclass(frozen=True)
class Phase1BBaselineSurfaceRequest:
    """Request to use the Phase 1B baseline surface."""

    split_label: str
    requested_skill_families: tuple[str, ...]
    output_columns: tuple[str, ...]
    purpose: str = "baseline_implementation_surface"
    backend: str = "python_polars_compatible"


@dataclass(frozen=True)
class Phase1BBaselineSurfaceDecision:
    """Allow/deny result for Phase 1B baseline surface use."""

    allowed: bool
    reason_code: str


def build_phase1b_long_only_baseline_surface(
    scaffold: Phase1ABaselineScaffold,
) -> Phase1BBaselineSurface:
    """Build a bounded implementation surface from the Phase 1A scaffold."""
    _validate_scaffold_boundary(scaffold)
    skill_interfaces = tuple(
        Phase1BSkillInterface(
            family=placeholder.family,
            interface_id=f"P1B-IFACE-{index:02d}-{placeholder.family}",
        )
        for index, placeholder in enumerate(scaffold.skill_placeholders, start=1)
    )
    return Phase1BBaselineSurface(
        surface_id=PHASE1B_BASELINE_SURFACE_ID,
        scaffold_id=scaffold.scaffold_id,
        registration_id=scaffold.registration_id,
        registration_instance_id=scaffold.registration_instance_id,
        spec_id=scaffold.spec_id,
        baseline_spec_hash=scaffold.baseline_spec_hash,
        validation_registration_hash=scaffold.validation_registration_hash,
        allowed_split_labels=(PHASE1A_FORMATION_LABEL,),
        denied_split_labels=(PHASE1A_VALIDATION_LABEL, PHASE1A_HOLDOUT_LABEL),
        skill_interfaces=skill_interfaces,
        required_output_columns=PHASE1B_REQUIRED_OUTPUT_COLUMNS,
        forbidden_output_columns=PHASE1B_FORBIDDEN_OUTPUT_COLUMNS,
        no_claim_labels=PHASE1B_BASELINE_NO_CLAIM_LABELS,
        workload_boundary=PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY,
    )


def validate_phase1b_baseline_surface_request(
    surface: Phase1BBaselineSurface,
    request: Phase1BBaselineSurfaceRequest,
) -> Phase1BBaselineSurfaceDecision:
    """Validate a Phase 1B surface request without executing baseline logic."""
    if request.purpose != "baseline_implementation_surface":
        return Phase1BBaselineSurfaceDecision(False, "PURPOSE_NOT_ALLOWED")
    if request.backend not in PHASE1B_BASELINE_ALLOWED_BACKENDS:
        return Phase1BBaselineSurfaceDecision(False, "BACKEND_NOT_ALLOWED")
    if request.split_label in surface.denied_split_labels:
        return Phase1BBaselineSurfaceDecision(False, "SPLIT_LABEL_DENIED")
    if request.split_label not in surface.allowed_split_labels:
        return Phase1BBaselineSurfaceDecision(False, "SPLIT_LABEL_NOT_ALLOWED")

    allowed_families = {skill.family for skill in surface.skill_interfaces}
    requested_families = set(_nonempty_str_sequence(request.requested_skill_families))
    if not requested_families:
        return Phase1BBaselineSurfaceDecision(False, "NO_SKILL_FAMILIES_REQUESTED")
    if not requested_families.issubset(allowed_families):
        return Phase1BBaselineSurfaceDecision(False, "UNKNOWN_SKILL_FAMILY")

    normalized_columns = set(_nonempty_str_sequence(request.output_columns))
    forbidden_columns = normalized_columns.intersection(surface.forbidden_output_columns)
    if forbidden_columns:
        return Phase1BBaselineSurfaceDecision(False, "FORBIDDEN_OUTPUT_COLUMN")
    missing_columns = set(surface.required_output_columns).difference(normalized_columns)
    if missing_columns:
        return Phase1BBaselineSurfaceDecision(False, "MISSING_REQUIRED_OUTPUT_COLUMN")
    return Phase1BBaselineSurfaceDecision(True, "SURFACE_REQUEST_ALLOWED")


def phase1b_surface_schema_payload(surface: Phase1BBaselineSurface) -> dict[str, object]:
    """Return a deterministic schema payload for audit and replay checks."""
    return {
        "surface_id": surface.surface_id,
        "scaffold_id": surface.scaffold_id,
        "registration_instance_id": surface.registration_instance_id,
        "spec_id": surface.spec_id,
        "baseline_spec_hash": surface.baseline_spec_hash,
        "allowed_split_labels": list(surface.allowed_split_labels),
        "denied_split_labels": list(surface.denied_split_labels),
        "skill_families": [skill.family for skill in surface.skill_interfaces],
        "required_output_columns": list(surface.required_output_columns),
        "forbidden_output_columns": list(surface.forbidden_output_columns),
        "no_claim_labels": list(surface.no_claim_labels),
        "evaluation_allowed": surface.evaluation_allowed,
        "gate_claim_allowed": surface.gate_claim_allowed,
        "archive_only": surface.archive_only,
    }


def phase1b_surface_schema_hash(surface: Phase1BBaselineSurface) -> str:
    """Hash the deterministic Phase 1B surface schema payload."""
    canonical = json.dumps(
        phase1b_surface_schema_payload(surface),
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_scaffold_boundary(scaffold: Phase1ABaselineScaffold) -> None:
    if scaffold.scaffold_id != PHASE1A_BASELINE_SCAFFOLD_ID:
        raise ValueError("Phase 1B baseline surface requires the Phase 1A scaffold")
    if scaffold.archive_only is not True:
        raise ValueError("Phase 1B baseline surface requires archive_only scaffold")
    if scaffold.gate_claim_allowed is not False:
        raise ValueError("Phase 1B baseline surface must not allow gate claims")
    if scaffold.direction != "long_only":
        raise ValueError("Phase 1B baseline surface requires long_only scaffold")
    if scaffold.workload_boundary != PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY:
        raise ValueError("Phase 1B baseline surface requires the P1A workload boundary")
    if len(scaffold.skill_placeholders) != 6:
        raise ValueError("Phase 1B baseline surface requires six skill placeholders")


def _nonempty_str_sequence(values: Sequence[str]) -> tuple[str, ...]:
    if not all(isinstance(value, str) and value.strip() for value in values):
        raise ValueError("Phase 1B surface request values must be nonblank strings")
    return tuple(values)
