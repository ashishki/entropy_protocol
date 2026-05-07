from __future__ import annotations

import json

from entropy.baseline.long_only import build_phase1b_long_only_baseline_surface
from entropy.baseline.readiness import (
    PHASE1C_HOLDOUT_CLAIM_GUARD_ID,
    PHASE1C_PREFLIGHT_CHECKLIST_ID,
    PHASE1C_READINESS_CONTRACT_ID,
    PHASE1C_READINESS_PAYLOAD_ID,
    Phase1CPreflightRequest,
    Phase1CReadinessArtifacts,
    build_phase1c_readiness_contract,
    phase1c_readiness_payload,
    phase1c_readiness_payload_hash,
    run_phase1c_preflight_checklist,
    validate_phase1c_preflight_request,
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


def test_readiness_contract_records_required_artifacts_without_claims(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    contract = build_phase1c_readiness_contract(surface)

    assert contract.contract_id == PHASE1C_READINESS_CONTRACT_ID
    assert contract.surface_id == surface.surface_id
    assert contract.baseline_spec_hash == surface.baseline_spec_hash
    assert contract.allowed_split_labels == (PHASE1A_FORMATION_LABEL,)
    assert contract.denied_split_labels == (PHASE1A_VALIDATION_LABEL, PHASE1A_HOLDOUT_LABEL)
    assert "phase1_evaluation_approval" in contract.required_human_gates
    assert contract.evaluation_allowed is False
    assert contract.gate_claim_allowed is False
    assert contract.phase_gate_evidence is False


def test_readiness_guard_rejects_validation_holdout_and_claim_fields(tmp_path) -> None:
    contract = build_phase1c_readiness_contract(_build_surface(tmp_path))

    validation = validate_phase1c_preflight_request(
        contract,
        Phase1CPreflightRequest(split_label=PHASE1A_VALIDATION_LABEL),
    )
    holdout = validate_phase1c_preflight_request(
        contract,
        Phase1CPreflightRequest(split_label=PHASE1A_HOLDOUT_LABEL),
    )
    claim = validate_phase1c_preflight_request(
        contract,
        Phase1CPreflightRequest(requested_fields=("sharpe",)),
    )

    assert validation.allowed is False
    assert validation.reason_code == "SPLIT_LABEL_DENIED"
    assert holdout.allowed is False
    assert holdout.reason_code == "SPLIT_LABEL_DENIED"
    assert claim.allowed is False
    assert claim.reason_code == "FORBIDDEN_REQUEST_FIELD"


def test_readiness_guard_rejects_labels_live_broker_growth_runtime_and_eval(tmp_path) -> None:
    contract = build_phase1c_readiness_contract(_build_surface(tmp_path))

    cases = [
        (Phase1CPreflightRequest(requested_labels=("capital_ready",)), "FORBIDDEN_REQUEST_LABEL"),
        (Phase1CPreflightRequest(live_feed_requested=True), "LIVE_FEED_NOT_ALLOWED"),
        (Phase1CPreflightRequest(broker_requested=True), "BROKER_NOT_ALLOWED"),
        (Phase1CPreflightRequest(growth_rdl_rbe_requested=True), "GROWTH_RDL_RBE_NOT_ALLOWED"),
        (
            Phase1CPreflightRequest(runtime_escalation_requested=True),
            "RUNTIME_ESCALATION_NOT_ALLOWED",
        ),
        (
            Phase1CPreflightRequest(phase1_evaluation_requested=True),
            "PHASE1_EVALUATION_NOT_ALLOWED",
        ),
        (Phase1CPreflightRequest(holdout_unlock_requested=True), "HOLDOUT_UNLOCK_NOT_ALLOWED"),
    ]

    for request, reason_code in cases:
        decision = validate_phase1c_preflight_request(contract, request)
        assert decision.allowed is False
        assert decision.reason_code == reason_code


def test_readiness_guard_allows_formation_metadata_preflight_only(tmp_path) -> None:
    contract = build_phase1c_readiness_contract(_build_surface(tmp_path))

    decision = validate_phase1c_preflight_request(
        contract,
        Phase1CPreflightRequest(
            split_label=PHASE1A_FORMATION_LABEL,
            requested_fields=("surface_id", "baseline_spec_hash"),
        ),
    )

    assert decision.allowed is True
    assert decision.reason_code == "PREFLIGHT_REQUEST_ALLOWED"


def test_preflight_checklist_ready_for_human_review_when_metadata_matches(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    contract = build_phase1c_readiness_contract(surface)
    artifacts = Phase1CReadinessArtifacts(
        surface=surface,
        benchmark=run_phase1b_baseline_surface_benchmark(surface, row_count=10),
    )

    result = run_phase1c_preflight_checklist(contract, artifacts)

    assert result.checklist_id == PHASE1C_PREFLIGHT_CHECKLIST_ID
    assert result.status == "READY_FOR_HUMAN_REVIEW"
    assert {item.status for item in result.items} == {"PASS"}
    assert result.evaluation_allowed is False
    assert result.gate_claim_allowed is False
    assert result.phase_gate_evidence is False


def test_preflight_checklist_blocks_missing_or_mismatched_artifacts(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    contract = build_phase1c_readiness_contract(surface)

    result = run_phase1c_preflight_checklist(
        contract,
        Phase1CReadinessArtifacts(
            surface=surface,
            benchmark=None,
            feature_contract_id="wrong",
        ),
    )

    assert result.status == "BLOCKED"
    assert ("feature_contract", "FAIL", "FEATURE_CONTRACT_MISMATCH") in {
        (item.item_id, item.status, item.reason_code) for item in result.items
    }
    assert ("mechanics_benchmark", "FAIL", "BENCHMARK_MISSING") in {
        (item.item_id, item.status, item.reason_code) for item in result.items
    }


def test_preflight_checklist_blocks_forbidden_request(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    contract = build_phase1c_readiness_contract(surface)
    artifacts = Phase1CReadinessArtifacts(
        surface=surface,
        benchmark=run_phase1b_baseline_surface_benchmark(surface, row_count=10),
    )

    result = run_phase1c_preflight_checklist(
        contract,
        artifacts,
        Phase1CPreflightRequest(requested_labels=("performance",)),
    )

    assert result.status == "BLOCKED"
    assert ("preflight_request_guard", "FAIL", "FORBIDDEN_REQUEST_LABEL") in {
        (item.item_id, item.status, item.reason_code) for item in result.items
    }


def test_no_claim_readiness_payload_and_hash_are_deterministic(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    contract = build_phase1c_readiness_contract(surface)
    artifacts = Phase1CReadinessArtifacts(
        surface=surface,
        benchmark=run_phase1b_baseline_surface_benchmark(surface, row_count=10),
    )
    checklist = run_phase1c_preflight_checklist(contract, artifacts)

    payload = phase1c_readiness_payload(contract, checklist)

    assert payload["payload_id"] == PHASE1C_READINESS_PAYLOAD_ID
    assert payload["evaluation_allowed"] is False
    assert payload["gate_claim_allowed"] is False
    assert payload["phase_gate_evidence"] is False
    no_claim_labels = payload["no_claim_labels"]
    assert isinstance(no_claim_labels, list)
    assert "not_phase_gate_evidence" in no_claim_labels
    assert "performance_metric" not in payload
    assert phase1c_readiness_payload_hash(contract, checklist) == phase1c_readiness_payload_hash(
        contract,
        checklist,
    )


def test_guard_id_is_stable() -> None:
    assert PHASE1C_HOLDOUT_CLAIM_GUARD_ID == "PHASE1C-HOLDOUT-CLAIM-GUARD-v1"


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
