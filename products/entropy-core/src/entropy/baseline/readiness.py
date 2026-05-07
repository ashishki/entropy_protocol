"""Phase 1C evaluation-readiness preflight guards.

This module checks metadata readiness only. It does not run evaluation, read
validation or holdout data, compute performance metrics, or emit phase-gate
evidence.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass

from entropy.baseline.features import PHASE1B_FEATURE_CONTRACT_ID
from entropy.baseline.formation import PHASE1B_FORMATION_INPUT_ADAPTER_ID
from entropy.baseline.long_only import (
    PHASE1B_BASELINE_NO_CLAIM_LABELS,
    PHASE1B_BASELINE_SURFACE_ID,
    PHASE1B_FORBIDDEN_OUTPUT_COLUMNS,
    Phase1BBaselineSurface,
)
from entropy.baseline.skills import (
    PHASE1B_BASELINE_BENCHMARK_ID,
    PHASE1B_SKILL_STUB_OUTPUT_ID,
    Phase1BBaselineBenchmarkResult,
)
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_VALIDATION_LABEL,
)

PHASE1C_READINESS_CONTRACT_ID = "PHASE1C-EVALUATION-READINESS-CONTRACT-v1"
PHASE1C_PREFLIGHT_CHECKLIST_ID = "PHASE1C-PREFLIGHT-CHECKLIST-v1"
PHASE1C_HOLDOUT_CLAIM_GUARD_ID = "PHASE1C-HOLDOUT-CLAIM-GUARD-v1"
PHASE1C_READINESS_PAYLOAD_ID = "PHASE1C-NO-CLAIM-READINESS-PAYLOAD-v1"

PHASE1C_READINESS_NO_CLAIM_LABELS: tuple[str, ...] = (
    "preflight_only",
    "not_evaluation",
    "not_backtest",
    "not_oos",
    "not_performance_evidence",
    "not_phase_gate_evidence",
    "not_capital_ready",
)

PHASE1C_FORBIDDEN_REQUEST_FIELDS: tuple[str, ...] = PHASE1B_FORBIDDEN_OUTPUT_COLUMNS + (
    "oos_claim",
    "validated_alpha",
    "production_label",
    "capital_ready_label",
    "phase1_evaluation_status",
    "holdout_unlock_id",
)

PHASE1C_FORBIDDEN_LABELS: tuple[str, ...] = (
    "oos",
    "performance",
    "validated_alpha",
    "production",
    "capital_ready",
    "phase_gate_evidence",
)


@dataclass(frozen=True)
class Phase1CReadinessContract:
    """Machine-readable contract for Phase 1C readiness preflight."""

    contract_id: str
    surface_id: str
    baseline_spec_hash: str
    feature_contract_id: str
    formation_adapter_id: str
    skill_stub_output_id: str
    benchmark_id: str
    allowed_split_labels: tuple[str, ...]
    denied_split_labels: tuple[str, ...]
    forbidden_request_fields: tuple[str, ...]
    forbidden_labels: tuple[str, ...]
    required_human_gates: tuple[str, ...]
    no_claim_labels: tuple[str, ...]
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False
    phase_gate_evidence: bool = False


@dataclass(frozen=True)
class Phase1CPreflightRequest:
    """Request to run Phase 1C readiness preflight checks."""

    split_label: str = PHASE1A_FORMATION_LABEL
    purpose: str = "evaluation_readiness_preflight"
    requested_fields: tuple[str, ...] = ()
    requested_labels: tuple[str, ...] = ()
    live_feed_requested: bool = False
    broker_requested: bool = False
    growth_rdl_rbe_requested: bool = False
    runtime_escalation_requested: bool = False
    phase1_evaluation_requested: bool = False
    holdout_unlock_requested: bool = False


@dataclass(frozen=True)
class Phase1CGuardDecision:
    """Allow/deny result for a Phase 1C preflight request."""

    allowed: bool
    reason_code: str


@dataclass(frozen=True)
class Phase1CReadinessArtifacts:
    """Metadata artifacts required by Phase 1C preflight."""

    surface: Phase1BBaselineSurface | None
    benchmark: Phase1BBaselineBenchmarkResult | None
    feature_contract_id: str | None = PHASE1B_FEATURE_CONTRACT_ID
    formation_adapter_id: str | None = PHASE1B_FORMATION_INPUT_ADAPTER_ID
    skill_stub_output_id: str | None = PHASE1B_SKILL_STUB_OUTPUT_ID


@dataclass(frozen=True)
class Phase1CChecklistItem:
    """One deterministic Phase 1C preflight checklist item."""

    item_id: str
    status: str
    reason_code: str


@dataclass(frozen=True)
class Phase1CChecklistResult:
    """Phase 1C preflight checklist result."""

    checklist_id: str
    status: str
    items: tuple[Phase1CChecklistItem, ...]
    no_claim_labels: tuple[str, ...]
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False
    phase_gate_evidence: bool = False


def build_phase1c_readiness_contract(
    surface: Phase1BBaselineSurface,
) -> Phase1CReadinessContract:
    """Build the Phase 1C readiness contract from the Phase 1B surface."""
    _validate_surface(surface)
    return Phase1CReadinessContract(
        contract_id=PHASE1C_READINESS_CONTRACT_ID,
        surface_id=surface.surface_id,
        baseline_spec_hash=surface.baseline_spec_hash,
        feature_contract_id=PHASE1B_FEATURE_CONTRACT_ID,
        formation_adapter_id=PHASE1B_FORMATION_INPUT_ADAPTER_ID,
        skill_stub_output_id=PHASE1B_SKILL_STUB_OUTPUT_ID,
        benchmark_id=PHASE1B_BASELINE_BENCHMARK_ID,
        allowed_split_labels=(PHASE1A_FORMATION_LABEL,),
        denied_split_labels=(PHASE1A_VALIDATION_LABEL, PHASE1A_HOLDOUT_LABEL),
        forbidden_request_fields=PHASE1C_FORBIDDEN_REQUEST_FIELDS,
        forbidden_labels=PHASE1C_FORBIDDEN_LABELS,
        required_human_gates=(
            "phase1_implementation_approval",
            "phase1_evaluation_approval",
            "holdout_unlock_approval",
        ),
        no_claim_labels=PHASE1C_READINESS_NO_CLAIM_LABELS,
    )


def validate_phase1c_preflight_request(
    contract: Phase1CReadinessContract,
    request: Phase1CPreflightRequest,
) -> Phase1CGuardDecision:
    """Validate that a request stays within Phase 1C preflight boundaries."""
    if contract.contract_id != PHASE1C_READINESS_CONTRACT_ID:
        return Phase1CGuardDecision(False, "CONTRACT_ID_NOT_ALLOWED")
    if request.purpose != "evaluation_readiness_preflight":
        return Phase1CGuardDecision(False, "PURPOSE_NOT_ALLOWED")
    if request.split_label in contract.denied_split_labels:
        return Phase1CGuardDecision(False, "SPLIT_LABEL_DENIED")
    if request.split_label not in contract.allowed_split_labels:
        return Phase1CGuardDecision(False, "SPLIT_LABEL_NOT_ALLOWED")

    requested_fields = set(_nonblank_str_sequence(request.requested_fields))
    if requested_fields.intersection(contract.forbidden_request_fields):
        return Phase1CGuardDecision(False, "FORBIDDEN_REQUEST_FIELD")

    requested_labels = set(_nonblank_str_sequence(request.requested_labels))
    if requested_labels.intersection(contract.forbidden_labels):
        return Phase1CGuardDecision(False, "FORBIDDEN_REQUEST_LABEL")

    if request.live_feed_requested:
        return Phase1CGuardDecision(False, "LIVE_FEED_NOT_ALLOWED")
    if request.broker_requested:
        return Phase1CGuardDecision(False, "BROKER_NOT_ALLOWED")
    if request.growth_rdl_rbe_requested:
        return Phase1CGuardDecision(False, "GROWTH_RDL_RBE_NOT_ALLOWED")
    if request.runtime_escalation_requested:
        return Phase1CGuardDecision(False, "RUNTIME_ESCALATION_NOT_ALLOWED")
    if request.phase1_evaluation_requested:
        return Phase1CGuardDecision(False, "PHASE1_EVALUATION_NOT_ALLOWED")
    if request.holdout_unlock_requested:
        return Phase1CGuardDecision(False, "HOLDOUT_UNLOCK_NOT_ALLOWED")
    return Phase1CGuardDecision(True, "PREFLIGHT_REQUEST_ALLOWED")


def run_phase1c_preflight_checklist(
    contract: Phase1CReadinessContract,
    artifacts: Phase1CReadinessArtifacts,
    request: Phase1CPreflightRequest | None = None,
) -> Phase1CChecklistResult:
    """Run deterministic metadata-only readiness checks."""
    active_request = request or Phase1CPreflightRequest()
    request_decision = validate_phase1c_preflight_request(contract, active_request)
    items = (
        _check_surface(contract, artifacts.surface),
        _check_feature_contract(contract, artifacts.feature_contract_id),
        _check_formation_adapter(contract, artifacts.formation_adapter_id),
        _check_skill_stub(contract, artifacts.skill_stub_output_id),
        _check_benchmark(contract, artifacts.benchmark),
        Phase1CChecklistItem(
            "preflight_request_guard",
            "PASS" if request_decision.allowed else "FAIL",
            request_decision.reason_code,
        ),
    )
    status = "READY_FOR_HUMAN_REVIEW" if all(item.status == "PASS" for item in items) else "BLOCKED"
    return Phase1CChecklistResult(
        checklist_id=PHASE1C_PREFLIGHT_CHECKLIST_ID,
        status=status,
        items=items,
        no_claim_labels=PHASE1C_READINESS_NO_CLAIM_LABELS,
    )


def phase1c_readiness_payload(
    contract: Phase1CReadinessContract,
    checklist: Phase1CChecklistResult,
) -> dict[str, object]:
    """Build a deterministic no-claim readiness payload."""
    return {
        "payload_id": PHASE1C_READINESS_PAYLOAD_ID,
        "contract_id": contract.contract_id,
        "checklist_id": checklist.checklist_id,
        "status": checklist.status,
        "surface_id": contract.surface_id,
        "baseline_spec_hash": contract.baseline_spec_hash,
        "allowed_split_labels": list(contract.allowed_split_labels),
        "denied_split_labels": list(contract.denied_split_labels),
        "required_human_gates": list(contract.required_human_gates),
        "no_claim_labels": list(checklist.no_claim_labels),
        "items": [
            {
                "item_id": item.item_id,
                "status": item.status,
                "reason_code": item.reason_code,
            }
            for item in checklist.items
        ],
        "evaluation_allowed": checklist.evaluation_allowed,
        "gate_claim_allowed": checklist.gate_claim_allowed,
        "phase_gate_evidence": checklist.phase_gate_evidence,
    }


def phase1c_readiness_payload_hash(
    contract: Phase1CReadinessContract,
    checklist: Phase1CChecklistResult,
) -> str:
    """Hash the deterministic no-claim readiness payload."""
    canonical = json.dumps(
        phase1c_readiness_payload(contract, checklist),
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _check_surface(
    contract: Phase1CReadinessContract,
    surface: Phase1BBaselineSurface | None,
) -> Phase1CChecklistItem:
    if surface is None:
        return Phase1CChecklistItem("phase1b_surface", "FAIL", "SURFACE_MISSING")
    if (
        surface.surface_id != contract.surface_id
        or surface.surface_id != PHASE1B_BASELINE_SURFACE_ID
    ):
        return Phase1CChecklistItem("phase1b_surface", "FAIL", "SURFACE_ID_MISMATCH")
    if surface.baseline_spec_hash != contract.baseline_spec_hash:
        return Phase1CChecklistItem("phase1b_surface", "FAIL", "BASELINE_SPEC_HASH_MISMATCH")
    if surface.evaluation_allowed or surface.gate_claim_allowed:
        return Phase1CChecklistItem("phase1b_surface", "FAIL", "SURFACE_CLAIM_FLAGS_NOT_ALLOWED")
    return Phase1CChecklistItem("phase1b_surface", "PASS", "SURFACE_READY")


def _check_feature_contract(
    contract: Phase1CReadinessContract,
    feature_contract_id: str | None,
) -> Phase1CChecklistItem:
    if feature_contract_id != contract.feature_contract_id:
        return Phase1CChecklistItem("feature_contract", "FAIL", "FEATURE_CONTRACT_MISMATCH")
    return Phase1CChecklistItem("feature_contract", "PASS", "FEATURE_CONTRACT_READY")


def _check_formation_adapter(
    contract: Phase1CReadinessContract,
    formation_adapter_id: str | None,
) -> Phase1CChecklistItem:
    if formation_adapter_id != contract.formation_adapter_id:
        return Phase1CChecklistItem("formation_adapter", "FAIL", "FORMATION_ADAPTER_MISMATCH")
    return Phase1CChecklistItem("formation_adapter", "PASS", "FORMATION_ADAPTER_READY")


def _check_skill_stub(
    contract: Phase1CReadinessContract,
    skill_stub_output_id: str | None,
) -> Phase1CChecklistItem:
    if skill_stub_output_id != contract.skill_stub_output_id:
        return Phase1CChecklistItem("skill_stub_output", "FAIL", "SKILL_STUB_MISMATCH")
    return Phase1CChecklistItem("skill_stub_output", "PASS", "SKILL_STUB_READY")


def _check_benchmark(
    contract: Phase1CReadinessContract,
    benchmark: Phase1BBaselineBenchmarkResult | None,
) -> Phase1CChecklistItem:
    if benchmark is None:
        return Phase1CChecklistItem("mechanics_benchmark", "FAIL", "BENCHMARK_MISSING")
    if benchmark.benchmark_id != contract.benchmark_id:
        return Phase1CChecklistItem("mechanics_benchmark", "FAIL", "BENCHMARK_ID_MISMATCH")
    if benchmark.evaluation_allowed or benchmark.gate_claim_allowed:
        return Phase1CChecklistItem(
            "mechanics_benchmark", "FAIL", "BENCHMARK_CLAIM_FLAGS_NOT_ALLOWED"
        )
    if tuple(benchmark.no_claim_labels) != PHASE1B_BASELINE_NO_CLAIM_LABELS:
        return Phase1CChecklistItem(
            "mechanics_benchmark", "FAIL", "BENCHMARK_NO_CLAIM_LABEL_MISMATCH"
        )
    return Phase1CChecklistItem("mechanics_benchmark", "PASS", "BENCHMARK_READY")


def _validate_surface(surface: Phase1BBaselineSurface) -> None:
    if surface.surface_id != PHASE1B_BASELINE_SURFACE_ID:
        raise ValueError("Phase 1C requires the Phase 1B baseline surface")
    if surface.evaluation_allowed or surface.gate_claim_allowed:
        raise ValueError("Phase 1C requires no-claim Phase 1B surface flags")
    if PHASE1A_VALIDATION_LABEL not in surface.denied_split_labels:
        raise ValueError("Phase 1C requires validation split to remain denied")
    if PHASE1A_HOLDOUT_LABEL not in surface.denied_split_labels:
        raise ValueError("Phase 1C requires holdout split to remain denied")


def _nonblank_str_sequence(values: Sequence[str]) -> tuple[str, ...]:
    if not all(isinstance(value, str) and value.strip() for value in values):
        raise ValueError("Phase 1C request values must be nonblank strings")
    return tuple(values)
