"""Human approval gate helpers."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal


ApprovalBoundary = Literal[
    "phase_gate",
    "holdout_access",
    "provider_activation",
    "product_bridge_activation",
    "research_object_registration",
    "evaluation_execution",
]


@dataclass(frozen=True)
class HumanApprovalRecord:
    """Human approval evidence for one governed boundary."""

    approval_id: str
    boundary: ApprovalBoundary
    reference_id: str
    approved: bool
    actor: str
    policy_hash: str


@dataclass(frozen=True)
class PhaseGateReport:
    """Phase-gate report status derived from task results and approval evidence."""

    phase: int
    phase_gate_id: str
    status: Literal["APPROVED", "NOT_APPROVED"]
    task_results: Mapping[str, bool]
    reason_code: str


@dataclass(frozen=True)
class HoldoutAccessDecision:
    """Holdout access decision that can block before any read callback."""

    status: Literal["ALLOWED", "BLOCKED"]
    reason_code: str
    holdout_path: str
    approval_id: str | None = None


@dataclass(frozen=True)
class ProviderActivationContract:
    """Declared provider contract required before activation."""

    provider_name: str
    contract_id: str
    allowed_purpose: str
    external_egress: bool = False


@dataclass(frozen=True)
class ProviderActivationDecision:
    """Provider activation decision."""

    status: Literal["APPROVED", "BLOCKED"]
    provider_name: str
    reason_code: str
    contract_id: str | None = None
    approval_id: str | None = None


def build_phase_gate_report(
    *,
    phase: int,
    phase_gate_id: str,
    task_results: Mapping[str, bool],
    approval_records: Iterable[HumanApprovalRecord] = (),
) -> PhaseGateReport:
    """Return NOT_APPROVED unless matching human approval evidence exists."""
    if not task_results or not all(task_results.values()):
        return PhaseGateReport(
            phase=phase,
            phase_gate_id=phase_gate_id,
            status="NOT_APPROVED",
            task_results=dict(task_results),
            reason_code="PHASE_TASKS_INCOMPLETE",
        )
    approval = _matching_approval(approval_records, "phase_gate", phase_gate_id)
    if approval is None:
        return PhaseGateReport(
            phase=phase,
            phase_gate_id=phase_gate_id,
            status="NOT_APPROVED",
            task_results=dict(task_results),
            reason_code="MISSING_HUMAN_PHASE_GATE_APPROVAL",
        )
    return PhaseGateReport(
        phase=phase,
        phase_gate_id=phase_gate_id,
        status="APPROVED",
        task_results=dict(task_results),
        reason_code="HUMAN_PHASE_GATE_APPROVAL_RECORDED",
    )


def authorize_holdout_access(
    *,
    holdout_path: str,
    approval_records: Iterable[HumanApprovalRecord] = (),
    read_holdout: Callable[[str], Any] | None = None,
) -> HoldoutAccessDecision:
    """Block holdout access before any read when approval is absent."""
    approval = _matching_approval(approval_records, "holdout_access", holdout_path)
    if approval is None:
        return HoldoutAccessDecision(
            status="BLOCKED",
            reason_code="MISSING_HUMAN_HOLDOUT_APPROVAL",
            holdout_path=holdout_path,
        )
    if read_holdout is not None:
        read_holdout(holdout_path)
    return HoldoutAccessDecision(
        status="ALLOWED",
        reason_code="HUMAN_HOLDOUT_APPROVAL_RECORDED",
        holdout_path=holdout_path,
        approval_id=approval.approval_id,
    )


def evaluate_provider_activation(
    *,
    provider_name: str,
    contract: ProviderActivationContract | None,
    approval_records: Iterable[HumanApprovalRecord] = (),
) -> ProviderActivationDecision:
    """Require a declared provider contract and human approval before activation."""
    if contract is None or contract.provider_name != provider_name:
        return ProviderActivationDecision(
            status="BLOCKED",
            provider_name=provider_name,
            reason_code="MISSING_PROVIDER_CONTRACT",
        )
    approval = _matching_approval(
        approval_records,
        "provider_activation",
        contract.contract_id,
    )
    if approval is None:
        return ProviderActivationDecision(
            status="BLOCKED",
            provider_name=provider_name,
            reason_code="MISSING_HUMAN_PROVIDER_APPROVAL",
            contract_id=contract.contract_id,
        )
    return ProviderActivationDecision(
        status="APPROVED",
        provider_name=provider_name,
        reason_code="HUMAN_PROVIDER_APPROVAL_RECORDED",
        contract_id=contract.contract_id,
        approval_id=approval.approval_id,
    )


def _matching_approval(
    approval_records: Iterable[HumanApprovalRecord],
    boundary: ApprovalBoundary,
    reference_id: str,
) -> HumanApprovalRecord | None:
    for record in approval_records:
        if record.boundary == boundary and record.reference_id == reference_id and record.approved:
            return record
    return None
