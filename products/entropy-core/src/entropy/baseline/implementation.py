"""Phase 1D long-only baseline implementation contract guards.

This module is contract code only. It does not implement alpha logic, portfolio
allocation, backtests, evaluation metrics, validation reads, or holdout reads.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass

from entropy.baseline.long_only import PHASE1B_BASELINE_SURFACE_ID
from entropy.baseline.readiness import (
    PHASE1C_FORBIDDEN_LABELS,
    PHASE1C_FORBIDDEN_REQUEST_FIELDS,
    PHASE1C_PREFLIGHT_CHECKLIST_ID,
    PHASE1C_READINESS_CONTRACT_ID,
    PHASE1C_READINESS_NO_CLAIM_LABELS,
    Phase1CChecklistResult,
    Phase1CReadinessContract,
)
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_VALIDATION_LABEL,
)

PHASE1D_IMPLEMENTATION_CONTRACT_ID = "PHASE1D-LONG-ONLY-IMPLEMENTATION-CONTRACT-v1"
PHASE1D_IMPLEMENTATION_APPROVAL_GUARD_ID = "PHASE1D-IMPLEMENTATION-APPROVAL-GUARD-v1"
PHASE1D_IMPLEMENTATION_CONTRACT_PAYLOAD_ID = "PHASE1D-IMPLEMENTATION-CONTRACT-PAYLOAD-v1"

PHASE1D_ALLOWED_TRANSFORM_FAMILIES: tuple[str, ...] = (
    "formation_schema_binding",
    "deterministic_lagged_ohlcv_transform",
    "deterministic_rolling_ohlcv_transform",
    "schema_only_skill_binding",
)

PHASE1D_NO_CLAIM_LABELS: tuple[str, ...] = PHASE1C_READINESS_NO_CLAIM_LABELS + (
    "implementation_contract_only",
    "not_strategy_selection",
)

PHASE1D_FORBIDDEN_OUTPUT_COLUMNS: tuple[str, ...] = PHASE1C_FORBIDDEN_REQUEST_FIELDS + (
    "rank",
    "alpha_rank",
    "selection_rank",
    "portfolio_weight",
    "trade",
    "order",
    "fill",
)

PHASE1D_FORBIDDEN_LABELS: tuple[str, ...] = PHASE1C_FORBIDDEN_LABELS + (
    "strategy_selected",
    "ready_for_backtest",
    "ready_for_trading",
)


@dataclass(frozen=True)
class Phase1DImplementationContract:
    """Machine-readable boundary for future bounded baseline implementation."""

    contract_id: str
    readiness_contract_id: str
    preflight_checklist_id: str
    surface_id: str
    baseline_spec_hash: str
    allowed_split_labels: tuple[str, ...]
    denied_split_labels: tuple[str, ...]
    allowed_transform_families: tuple[str, ...]
    forbidden_output_columns: tuple[str, ...]
    forbidden_labels: tuple[str, ...]
    required_approval_gates: tuple[str, ...]
    no_claim_labels: tuple[str, ...]
    executable_logic_approved: bool = False
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False
    phase_gate_evidence: bool = False


@dataclass(frozen=True)
class Phase1DImplementationRequest:
    """Request to validate against the Phase 1D implementation contract."""

    split_label: str = PHASE1A_FORMATION_LABEL
    purpose: str = "long_only_implementation_contract_check"
    transform_families: tuple[str, ...] = ()
    requested_output_columns: tuple[str, ...] = ()
    requested_labels: tuple[str, ...] = ()
    replace_schema_only_stubs: bool = False
    approval_gate_id: str | None = None
    validation_read_requested: bool = False
    holdout_read_requested: bool = False
    evaluation_requested: bool = False
    portfolio_requested: bool = False
    performance_metrics_requested: bool = False
    live_feed_requested: bool = False
    broker_requested: bool = False
    runtime_escalation_requested: bool = False


@dataclass(frozen=True)
class Phase1DImplementationDecision:
    """Allow/deny result for a Phase 1D contract request."""

    allowed: bool
    reason_code: str


def build_phase1d_implementation_contract(
    readiness_contract: Phase1CReadinessContract,
    checklist: Phase1CChecklistResult,
) -> Phase1DImplementationContract:
    """Build the Phase 1D implementation contract from Phase 1C readiness state."""
    _validate_readiness_inputs(readiness_contract, checklist)
    return Phase1DImplementationContract(
        contract_id=PHASE1D_IMPLEMENTATION_CONTRACT_ID,
        readiness_contract_id=readiness_contract.contract_id,
        preflight_checklist_id=checklist.checklist_id,
        surface_id=readiness_contract.surface_id,
        baseline_spec_hash=readiness_contract.baseline_spec_hash,
        allowed_split_labels=(PHASE1A_FORMATION_LABEL,),
        denied_split_labels=(PHASE1A_VALIDATION_LABEL, PHASE1A_HOLDOUT_LABEL),
        allowed_transform_families=PHASE1D_ALLOWED_TRANSFORM_FAMILIES,
        forbidden_output_columns=PHASE1D_FORBIDDEN_OUTPUT_COLUMNS,
        forbidden_labels=PHASE1D_FORBIDDEN_LABELS,
        required_approval_gates=(
            "phase1d_contract_approval",
            "phase1e_bounded_implementation_approval",
            "phase1g_evaluation_approval",
            "holdout_unlock_approval",
        ),
        no_claim_labels=PHASE1D_NO_CLAIM_LABELS,
    )


def validate_phase1d_implementation_request(
    contract: Phase1DImplementationContract,
    request: Phase1DImplementationRequest,
) -> Phase1DImplementationDecision:
    """Validate a future implementation request without running baseline logic."""
    if contract.contract_id != PHASE1D_IMPLEMENTATION_CONTRACT_ID:
        return Phase1DImplementationDecision(False, "CONTRACT_ID_NOT_ALLOWED")
    if request.purpose != "long_only_implementation_contract_check":
        return Phase1DImplementationDecision(False, "PURPOSE_NOT_ALLOWED")
    if request.split_label in contract.denied_split_labels:
        return Phase1DImplementationDecision(False, "SPLIT_LABEL_DENIED")
    if request.split_label not in contract.allowed_split_labels:
        return Phase1DImplementationDecision(False, "SPLIT_LABEL_NOT_ALLOWED")

    transform_families = set(_nonblank_str_sequence(request.transform_families))
    if not transform_families.issubset(contract.allowed_transform_families):
        return Phase1DImplementationDecision(False, "TRANSFORM_FAMILY_NOT_ALLOWED")

    output_columns = set(_nonblank_str_sequence(request.requested_output_columns))
    if output_columns.intersection(contract.forbidden_output_columns):
        return Phase1DImplementationDecision(False, "FORBIDDEN_OUTPUT_COLUMN")

    labels = set(_nonblank_str_sequence(request.requested_labels))
    if labels.intersection(contract.forbidden_labels):
        return Phase1DImplementationDecision(False, "FORBIDDEN_LABEL")

    if (
        request.replace_schema_only_stubs
        and request.approval_gate_id != "phase1e_bounded_implementation_approval"
    ):
        return Phase1DImplementationDecision(False, "IMPLEMENTATION_APPROVAL_REQUIRED")
    if request.validation_read_requested:
        return Phase1DImplementationDecision(False, "VALIDATION_READ_NOT_ALLOWED")
    if request.holdout_read_requested:
        return Phase1DImplementationDecision(False, "HOLDOUT_READ_NOT_ALLOWED")
    if request.evaluation_requested:
        return Phase1DImplementationDecision(False, "EVALUATION_NOT_ALLOWED")
    if request.portfolio_requested:
        return Phase1DImplementationDecision(False, "PORTFOLIO_NOT_ALLOWED")
    if request.performance_metrics_requested:
        return Phase1DImplementationDecision(False, "PERFORMANCE_METRICS_NOT_ALLOWED")
    if request.live_feed_requested:
        return Phase1DImplementationDecision(False, "LIVE_FEED_NOT_ALLOWED")
    if request.broker_requested:
        return Phase1DImplementationDecision(False, "BROKER_NOT_ALLOWED")
    if request.runtime_escalation_requested:
        return Phase1DImplementationDecision(False, "RUNTIME_ESCALATION_NOT_ALLOWED")
    return Phase1DImplementationDecision(True, "IMPLEMENTATION_CONTRACT_REQUEST_ALLOWED")


def phase1d_implementation_contract_payload(
    contract: Phase1DImplementationContract,
) -> dict[str, object]:
    """Return a deterministic payload for the Phase 1D contract."""
    return {
        "payload_id": PHASE1D_IMPLEMENTATION_CONTRACT_PAYLOAD_ID,
        "contract_id": contract.contract_id,
        "readiness_contract_id": contract.readiness_contract_id,
        "preflight_checklist_id": contract.preflight_checklist_id,
        "surface_id": contract.surface_id,
        "baseline_spec_hash": contract.baseline_spec_hash,
        "allowed_split_labels": list(contract.allowed_split_labels),
        "denied_split_labels": list(contract.denied_split_labels),
        "allowed_transform_families": list(contract.allowed_transform_families),
        "forbidden_output_columns": list(contract.forbidden_output_columns),
        "forbidden_labels": list(contract.forbidden_labels),
        "required_approval_gates": list(contract.required_approval_gates),
        "no_claim_labels": list(contract.no_claim_labels),
        "executable_logic_approved": contract.executable_logic_approved,
        "evaluation_allowed": contract.evaluation_allowed,
        "gate_claim_allowed": contract.gate_claim_allowed,
        "phase_gate_evidence": contract.phase_gate_evidence,
    }


def phase1d_implementation_contract_hash(contract: Phase1DImplementationContract) -> str:
    """Hash the deterministic Phase 1D contract payload."""
    canonical = json.dumps(
        phase1d_implementation_contract_payload(contract),
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_readiness_inputs(
    readiness_contract: Phase1CReadinessContract,
    checklist: Phase1CChecklistResult,
) -> None:
    if readiness_contract.contract_id != PHASE1C_READINESS_CONTRACT_ID:
        raise ValueError("Phase 1D requires the Phase 1C readiness contract")
    if readiness_contract.surface_id != PHASE1B_BASELINE_SURFACE_ID:
        raise ValueError("Phase 1D requires the Phase 1B baseline surface")
    if checklist.checklist_id != PHASE1C_PREFLIGHT_CHECKLIST_ID:
        raise ValueError("Phase 1D requires the Phase 1C preflight checklist")
    if checklist.status != "READY_FOR_HUMAN_REVIEW":
        raise ValueError("Phase 1D requires a ready Phase 1C preflight checklist")
    if (
        readiness_contract.evaluation_allowed
        or readiness_contract.gate_claim_allowed
        or readiness_contract.phase_gate_evidence
        or checklist.evaluation_allowed
        or checklist.gate_claim_allowed
        or checklist.phase_gate_evidence
    ):
        raise ValueError("Phase 1D requires no-claim Phase 1C readiness state")
    if PHASE1A_VALIDATION_LABEL not in readiness_contract.denied_split_labels:
        raise ValueError("Phase 1D requires validation split to remain denied")
    if PHASE1A_HOLDOUT_LABEL not in readiness_contract.denied_split_labels:
        raise ValueError("Phase 1D requires holdout split to remain denied")


def _nonblank_str_sequence(values: Sequence[str]) -> tuple[str, ...]:
    if not all(isinstance(value, str) and value.strip() for value in values):
        raise ValueError("Phase 1D request values must be nonblank strings")
    return tuple(values)
