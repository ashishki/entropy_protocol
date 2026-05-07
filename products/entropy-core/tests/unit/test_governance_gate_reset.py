"""Reset-era human approval gate tests."""

from __future__ import annotations

from entropy.governance import (
    HumanApprovalRecord,
    ProviderActivationContract,
    authorize_holdout_access,
    build_phase_gate_report,
    evaluate_provider_activation,
)


def test_phase_gate_report_requires_human_approval_event() -> None:
    """Phase gate status is not approved without matching human evidence."""
    report = build_phase_gate_report(
        phase=2,
        phase_gate_id="phase-2-governance-integrity",
        task_results={"T04": True, "T05": True, "T06": True, "T07": True},
        approval_records=[],
    )

    assert report.status == "NOT_APPROVED"
    assert report.reason_code == "MISSING_HUMAN_PHASE_GATE_APPROVAL"

    incomplete = build_phase_gate_report(
        phase=2,
        phase_gate_id="phase-2-governance-integrity",
        task_results={"T04": True, "T05": False},
        approval_records=[
            HumanApprovalRecord(
                approval_id="approval-001",
                boundary="phase_gate",
                reference_id="phase-2-governance-integrity",
                approved=True,
                actor="human-governor",
                policy_hash="policy-sha",
            )
        ],
    )
    assert incomplete.status == "NOT_APPROVED"
    assert incomplete.reason_code == "PHASE_TASKS_INCOMPLETE"


def test_holdout_access_without_gate_is_blocked_before_read() -> None:
    """Holdout access blocks before invoking the read callback."""
    read_attempted = False

    def read_holdout(_path: str) -> None:
        nonlocal read_attempted
        read_attempted = True
        raise AssertionError("holdout data was read")

    decision = authorize_holdout_access(
        holdout_path="archive/holdout.parquet",
        approval_records=[],
        read_holdout=read_holdout,
    )

    assert decision.status == "BLOCKED"
    assert decision.reason_code == "MISSING_HUMAN_HOLDOUT_APPROVAL"
    assert read_attempted is False


def test_provider_activation_requires_contract_and_approval() -> None:
    """Provider activation is design-only until contract and human approval exist."""
    missing_contract = evaluate_provider_activation(
        provider_name="fixture-provider",
        contract=None,
        approval_records=[],
    )
    contract = ProviderActivationContract(
        provider_name="fixture-provider",
        contract_id="provider-contract-001",
        allowed_purpose="local_test_data",
    )
    missing_approval = evaluate_provider_activation(
        provider_name="fixture-provider",
        contract=contract,
        approval_records=[],
    )
    approved = evaluate_provider_activation(
        provider_name="fixture-provider",
        contract=contract,
        approval_records=[
            HumanApprovalRecord(
                approval_id="approval-001",
                boundary="provider_activation",
                reference_id="provider-contract-001",
                approved=True,
                actor="human-governor",
                policy_hash="policy-sha",
            )
        ],
    )

    assert missing_contract.status == "BLOCKED"
    assert missing_contract.reason_code == "MISSING_PROVIDER_CONTRACT"
    assert missing_approval.status == "BLOCKED"
    assert missing_approval.reason_code == "MISSING_HUMAN_PROVIDER_APPROVAL"
    assert approved.status == "APPROVED"
    assert approved.approval_id == "approval-001"
