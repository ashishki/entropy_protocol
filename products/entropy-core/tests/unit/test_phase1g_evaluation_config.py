from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import pytest

from entropy.baseline.bounded import build_phase1e_all_bounded_baseline_outputs
from entropy.baseline.evaluation import (
    PHASE1G_EVALUATION_APPROVAL_GUARD_ID,
    PHASE1G_EVALUATION_CONFIG_CONTRACT_ID,
    PHASE1G_REQUIRED_LEAKAGE_CHECKS,
    PHASE1G_REQUIRED_STAT_FIELDS,
    Phase1GEvaluationRequest,
    build_phase1g_evaluation_config,
    phase1g_evaluation_config_hash,
    phase1g_evaluation_config_payload,
    validate_phase1g_evaluation_request,
)
from entropy.baseline.formation import prepare_phase1b_formation_input
from entropy.baseline.implementation import build_phase1d_implementation_contract
from entropy.baseline.long_only import build_phase1b_long_only_baseline_surface
from entropy.baseline.readiness import (
    Phase1CReadinessArtifacts,
    build_phase1c_readiness_contract,
    run_phase1c_preflight_checklist,
)
from entropy.baseline.registration import (
    build_phase1f_baseline_hash_binding,
    build_phase1f_preregistration_surface,
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase1g_config_records_required_governed_evaluation_fields(tmp_path) -> None:
    config = _build_config(tmp_path)

    assert config.contract_id == PHASE1G_EVALUATION_CONFIG_CONTRACT_ID
    assert config.allowed_split_labels == (PHASE1A_FORMATION_LABEL, PHASE1A_VALIDATION_LABEL)
    assert config.denied_split_labels == (PHASE1A_HOLDOUT_LABEL,)
    assert config.leakage_checks_required == PHASE1G_REQUIRED_LEAKAGE_CHECKS
    assert config.stat_report_fields == PHASE1G_REQUIRED_STAT_FIELDS
    assert "phase1g_evaluation_run_approval" in config.required_human_gates
    assert config.evaluation_execution_allowed is False
    assert config.holdout_allowed is False
    assert config.gate_claim_allowed is False
    assert config.phase_gate_evidence is False


def test_phase1g_config_payload_and_hash_are_deterministic(tmp_path) -> None:
    config = _build_config(tmp_path)

    payload = phase1g_evaluation_config_payload(config)

    assert payload["contract_id"] == PHASE1G_EVALUATION_CONFIG_CONTRACT_ID
    no_claim_labels = payload["no_claim_labels"]
    assert isinstance(no_claim_labels, list)
    assert "not_phase_gate_evidence" in no_claim_labels
    assert phase1g_evaluation_config_hash(config) == phase1g_evaluation_config_hash(config)


def test_phase1g_config_rejects_bad_windows(tmp_path) -> None:
    preregistration = _build_preregistration(tmp_path)

    with pytest.raises(ValueError, match="validation_start must be after formation_end"):
        build_phase1g_evaluation_config(
            preregistration,
            formation_start=_dt(2020, 1, 1),
            formation_end=_dt(2022, 12, 31),
            validation_start=_dt(2022, 12, 31),
            validation_end=_dt(2024, 12, 31),
            embargo_bars=5,
        )


def test_phase1g_guard_rejects_holdout_live_broker_claims_and_labels(tmp_path) -> None:
    config = _build_config(tmp_path)

    cases = [
        (Phase1GEvaluationRequest(split_label=PHASE1A_HOLDOUT_LABEL), "HOLDOUT_NOT_ALLOWED"),
        (Phase1GEvaluationRequest(holdout_requested=True), "HOLDOUT_NOT_ALLOWED"),
        (Phase1GEvaluationRequest(live_feed_requested=True), "LIVE_FEED_NOT_ALLOWED"),
        (Phase1GEvaluationRequest(broker_requested=True), "BROKER_NOT_ALLOWED"),
        (
            Phase1GEvaluationRequest(performance_conclusion_requested=True),
            "PERFORMANCE_CONCLUSION_NOT_ALLOWED",
        ),
        (Phase1GEvaluationRequest(phase_gate_claim_requested=True), "PHASE_GATE_CLAIM_NOT_ALLOWED"),
        (Phase1GEvaluationRequest(production_label_requested=True), "PRODUCTION_LABEL_NOT_ALLOWED"),
        (
            Phase1GEvaluationRequest(capital_ready_label_requested=True),
            "CAPITAL_READY_LABEL_NOT_ALLOWED",
        ),
    ]

    for request, reason_code in cases:
        decision = validate_phase1g_evaluation_request(config, request)
        assert decision.allowed is False
        assert decision.reason_code == reason_code


def test_phase1g_guard_requires_approval_before_evaluation_run(tmp_path) -> None:
    config = _build_config(tmp_path)

    denied = validate_phase1g_evaluation_request(
        config,
        Phase1GEvaluationRequest(evaluation_run_requested=True),
    )
    allowed = validate_phase1g_evaluation_request(
        config,
        Phase1GEvaluationRequest(
            evaluation_run_requested=True,
            approval_gate_id="phase1g_evaluation_run_approval",
        ),
    )

    assert denied.allowed is False
    assert denied.reason_code == "EVALUATION_APPROVAL_REQUIRED"
    assert allowed.allowed is True
    assert allowed.reason_code == "EVALUATION_CONFIG_REQUEST_ALLOWED"


def test_phase1g_approval_guard_id_is_stable() -> None:
    assert PHASE1G_EVALUATION_APPROVAL_GUARD_ID == "PHASE1G-EVALUATION-APPROVAL-GUARD-v1"


def _build_config(tmp_path):
    return build_phase1g_evaluation_config(
        _build_preregistration(tmp_path),
        formation_start=_dt(2020, 1, 1),
        formation_end=_dt(2022, 12, 31),
        validation_start=_dt(2023, 1, 1),
        validation_end=_dt(2024, 12, 31),
        embargo_bars=5,
    )


def _build_preregistration(tmp_path):
    boundary_path = _write_boundary_manifest(tmp_path)
    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )
    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=result.manifest_path)
    surface = build_phase1b_long_only_baseline_surface(scaffold)
    readiness_contract = build_phase1c_readiness_contract(surface)
    checklist = run_phase1c_preflight_checklist(
        readiness_contract,
        Phase1CReadinessArtifacts(
            surface=surface,
            benchmark=run_phase1b_baseline_surface_benchmark(surface, row_count=10),
        ),
    )
    contract = build_phase1d_implementation_contract(readiness_contract, checklist)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())
    outputs = build_phase1e_all_bounded_baseline_outputs(surface, formation, contract)
    binding = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        outputs,
        source_paths=(
            PROJECT_ROOT / "src" / "entropy" / "baseline" / "bounded.py",
            PROJECT_ROOT / "src" / "entropy" / "baseline" / "implementation.py",
        ),
    )
    return build_phase1f_preregistration_surface(binding, registered_at=_dt(2026, 5, 6))


def _dt(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, tzinfo=timezone.utc)


def _formation_rows() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "symbol": ["BTCUSDT", "BTCUSDT", "BTCUSDT", "BTCUSDT"],
            "timestamp_utc": [
                "2021-01-01T00:00:00Z",
                "2021-01-02T00:00:00Z",
                "2021-01-03T00:00:00Z",
                "2021-01-04T00:00:00Z",
            ],
            "open": [100.0, 101.0, 102.0, 103.0],
            "high": [101.0, 102.0, 103.0, 104.0],
            "low": [99.0, 100.0, 101.0, 102.0],
            "close": [100.5, 101.5, 102.5, 103.5],
            "volume": [10.0, 11.0, 12.0, 13.0],
            "dataset_hash": ["btc_hash", "btc_hash", "btc_hash", "btc_hash"],
        }
    )


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
