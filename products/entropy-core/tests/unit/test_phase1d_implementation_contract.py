from __future__ import annotations

import json

from entropy.baseline.implementation import (
    PHASE1D_IMPLEMENTATION_APPROVAL_GUARD_ID,
    PHASE1D_IMPLEMENTATION_CONTRACT_ID,
    PHASE1D_IMPLEMENTATION_CONTRACT_PAYLOAD_ID,
    Phase1DImplementationRequest,
    build_phase1d_implementation_contract,
    phase1d_implementation_contract_hash,
    phase1d_implementation_contract_payload,
    validate_phase1d_implementation_request,
)
from entropy.baseline.long_only import build_phase1b_long_only_baseline_surface
from entropy.baseline.readiness import (
    Phase1CReadinessArtifacts,
    build_phase1c_readiness_contract,
    run_phase1c_preflight_checklist,
)
from entropy.baseline.skills import run_phase1b_baseline_surface_benchmark
from entropy.evidence.phase1a_baseline import build_phase1a_baseline_registration_manifest
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
)
from entropy.evidence.phase1a_scaffold import load_phase1a_baseline_scaffold


def test_phase1d_contract_binds_ready_phase1c_without_claims(tmp_path) -> None:
    contract = _build_phase1d_contract(tmp_path)

    assert contract.contract_id == PHASE1D_IMPLEMENTATION_CONTRACT_ID
    assert contract.allowed_split_labels == (PHASE1A_FORMATION_LABEL,)
    assert contract.denied_split_labels == (PHASE1A_VALIDATION_LABEL, PHASE1A_HOLDOUT_LABEL)
    assert "phase1e_bounded_implementation_approval" in contract.required_approval_gates
    assert "deterministic_rolling_ohlcv_transform" in contract.allowed_transform_families
    assert "target_weight" in contract.forbidden_output_columns
    assert contract.executable_logic_approved is False
    assert contract.evaluation_allowed is False
    assert contract.gate_claim_allowed is False
    assert contract.phase_gate_evidence is False


def test_phase1d_guard_allows_formation_contract_check_only(tmp_path) -> None:
    contract = _build_phase1d_contract(tmp_path)

    decision = validate_phase1d_implementation_request(
        contract,
        Phase1DImplementationRequest(
            transform_families=("formation_schema_binding",),
            requested_output_columns=("symbol", "timestamp_utc", "skill_family"),
        ),
    )

    assert decision.allowed is True
    assert decision.reason_code == "IMPLEMENTATION_CONTRACT_REQUEST_ALLOWED"


def test_phase1d_guard_rejects_validation_holdout_claims_and_unknown_transform(tmp_path) -> None:
    contract = _build_phase1d_contract(tmp_path)

    cases = [
        (Phase1DImplementationRequest(split_label=PHASE1A_VALIDATION_LABEL), "SPLIT_LABEL_DENIED"),
        (Phase1DImplementationRequest(split_label=PHASE1A_HOLDOUT_LABEL), "SPLIT_LABEL_DENIED"),
        (
            Phase1DImplementationRequest(requested_output_columns=("alpha_score",)),
            "FORBIDDEN_OUTPUT_COLUMN",
        ),
        (Phase1DImplementationRequest(requested_labels=("ready_for_trading",)), "FORBIDDEN_LABEL"),
        (
            Phase1DImplementationRequest(transform_families=("cross_sectional_alpha_rank",)),
            "TRANSFORM_FAMILY_NOT_ALLOWED",
        ),
    ]

    for request, reason_code in cases:
        decision = validate_phase1d_implementation_request(contract, request)
        assert decision.allowed is False
        assert decision.reason_code == reason_code


def test_phase1d_guard_requires_approval_before_replacing_schema_stubs(tmp_path) -> None:
    contract = _build_phase1d_contract(tmp_path)

    denied = validate_phase1d_implementation_request(
        contract,
        Phase1DImplementationRequest(replace_schema_only_stubs=True),
    )
    allowed = validate_phase1d_implementation_request(
        contract,
        Phase1DImplementationRequest(
            replace_schema_only_stubs=True,
            approval_gate_id="phase1e_bounded_implementation_approval",
        ),
    )

    assert denied.allowed is False
    assert denied.reason_code == "IMPLEMENTATION_APPROVAL_REQUIRED"
    assert allowed.allowed is True
    assert allowed.reason_code == "IMPLEMENTATION_CONTRACT_REQUEST_ALLOWED"


def test_phase1d_guard_rejects_evaluation_portfolio_live_and_runtime_requests(tmp_path) -> None:
    contract = _build_phase1d_contract(tmp_path)

    cases = [
        (
            Phase1DImplementationRequest(validation_read_requested=True),
            "VALIDATION_READ_NOT_ALLOWED",
        ),
        (Phase1DImplementationRequest(holdout_read_requested=True), "HOLDOUT_READ_NOT_ALLOWED"),
        (Phase1DImplementationRequest(evaluation_requested=True), "EVALUATION_NOT_ALLOWED"),
        (Phase1DImplementationRequest(portfolio_requested=True), "PORTFOLIO_NOT_ALLOWED"),
        (
            Phase1DImplementationRequest(performance_metrics_requested=True),
            "PERFORMANCE_METRICS_NOT_ALLOWED",
        ),
        (Phase1DImplementationRequest(live_feed_requested=True), "LIVE_FEED_NOT_ALLOWED"),
        (Phase1DImplementationRequest(broker_requested=True), "BROKER_NOT_ALLOWED"),
        (
            Phase1DImplementationRequest(runtime_escalation_requested=True),
            "RUNTIME_ESCALATION_NOT_ALLOWED",
        ),
    ]

    for request, reason_code in cases:
        decision = validate_phase1d_implementation_request(contract, request)
        assert decision.allowed is False
        assert decision.reason_code == reason_code


def test_phase1d_contract_payload_and_hash_are_deterministic(tmp_path) -> None:
    contract = _build_phase1d_contract(tmp_path)

    payload = phase1d_implementation_contract_payload(contract)

    assert payload["payload_id"] == PHASE1D_IMPLEMENTATION_CONTRACT_PAYLOAD_ID
    assert payload["evaluation_allowed"] is False
    assert payload["gate_claim_allowed"] is False
    assert payload["phase_gate_evidence"] is False
    forbidden_output_columns = payload["forbidden_output_columns"]
    assert isinstance(forbidden_output_columns, list)
    assert "performance_metric" in forbidden_output_columns
    assert phase1d_implementation_contract_hash(contract) == phase1d_implementation_contract_hash(
        contract,
    )


def test_phase1d_guard_id_is_stable() -> None:
    assert PHASE1D_IMPLEMENTATION_APPROVAL_GUARD_ID == "PHASE1D-IMPLEMENTATION-APPROVAL-GUARD-v1"


def _build_phase1d_contract(tmp_path):
    surface = _build_surface(tmp_path)
    readiness_contract = build_phase1c_readiness_contract(surface)
    checklist = run_phase1c_preflight_checklist(
        readiness_contract,
        Phase1CReadinessArtifacts(
            surface=surface,
            benchmark=run_phase1b_baseline_surface_benchmark(surface, row_count=10),
        ),
    )
    return build_phase1d_implementation_contract(readiness_contract, checklist)


def _build_surface(tmp_path):
    boundary_path = _write_boundary_manifest(tmp_path)
    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )
    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=result.manifest_path)
    return build_phase1b_long_only_baseline_surface(scaffold)


def _write_boundary_manifest(tmp_path):
    boundary_path = tmp_path / "boundary.json"
    boundary_path.write_text(
        json.dumps(
            {
                "boundary_id": PHASE1A_REGISTRATION_BOUNDARY_ID,
                "freeze_id": "PHASE1A-ARCHIVE-FREEZE-v1",
                "freeze_manifest_hash": "f" * 64,
                "archive_only": True,
                "gate_claim_allowed": False,
                "status": "READ_GATE_ACTIVE_HOLDOUT_LOCKED",
                "boundary": "registration_read_gate_no_strategy_no_portfolio_no_performance_claim",
                "datasets": [
                    {
                        "symbol": "BTCUSDT",
                        "timeframe": "1d",
                        "calendar_profile": "continuous",
                        "dataset_hash": "btc_dataset_hash",
                        "parquet_path": "/tmp/BTCUSDT.parquet",
                    }
                ],
                "split_rules": [
                    {
                        "split_label": PHASE1A_FORMATION_LABEL,
                        "window_start": "2020-01-01",
                        "window_end": "2022-12-31",
                        "default_access": "ALLOW",
                        "allowed_purposes": ["instrumentation"],
                        "required_fields": [],
                        "locked_reason": None,
                    },
                    {
                        "split_label": PHASE1A_HOLDOUT_LABEL,
                        "window_start": "2025-01-01",
                        "window_end": "2025-12-31",
                        "default_access": "LOCKED",
                        "allowed_purposes": ["final_holdout_audit"],
                        "required_fields": ["holdout_unlock_id"],
                        "locked_reason": "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return boundary_path
