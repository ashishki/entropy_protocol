from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import pytest

from entropy.baseline.bounded import build_phase1e_all_bounded_baseline_outputs
from entropy.baseline.decision import (
    PHASE1J_RESEARCH_DECISION_ID,
    PHASE1K_RESEARCH_CLOSURE_PACKET_ID,
    build_phase1j_research_decision,
    build_phase1k_closure_packet,
    phase1j_decision_hash,
    phase1k_closure_hash,
)
from entropy.baseline.evaluation import build_phase1g_evaluation_config
from entropy.baseline.formation import prepare_phase1b_formation_input
from entropy.baseline.governed import Phase1HBar, run_phase1h_governed_evaluation
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
from entropy.baseline.report import (
    PHASE1I_EVALUATION_REPORT_ID,
    PHASE1I_STAT_FIELD_STATUS,
    build_phase1i_evaluation_report,
    phase1i_evaluation_report_payload,
)
from entropy.baseline.skills import run_phase1b_baseline_surface_benchmark
from entropy.evidence.phase1a_baseline import build_phase1a_baseline_registration_manifest
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
)
from entropy.evidence.phase1a_scaffold import load_phase1a_baseline_scaffold

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase1i_report_assembles_hashes_run_record_and_claim_boundaries(tmp_path) -> None:
    preregistration, config, evaluation = _build_report_inputs(tmp_path)

    report = build_phase1i_evaluation_report(config, preregistration, evaluation)

    assert report.report_id == PHASE1I_EVALUATION_REPORT_ID
    assert report.trial_id == evaluation.run_record.trial_id
    assert report.run_id == evaluation.run_record.run_id
    assert report.leakage_status == "PASS"
    assert report.holdout_used is False
    assert report.performance_conclusion is False
    assert report.phase_gate_evidence is False
    assert report.production_label is False
    assert report.capital_ready_label is False
    assert report.stat_field_statuses == tuple(
        (field, PHASE1I_STAT_FIELD_STATUS) for field in report.stat_fields
    )
    assert len(report.report_hash) == 64


def test_phase1i_report_payload_marks_stats_as_not_computed(tmp_path) -> None:
    preregistration, config, evaluation = _build_report_inputs(tmp_path)

    report = build_phase1i_evaluation_report(config, preregistration, evaluation)
    payload = phase1i_evaluation_report_payload(report)

    assert payload["stat_field_statuses"] == [
        {"field": field, "status": PHASE1I_STAT_FIELD_STATUS} for field in config.stat_report_fields
    ]


def test_phase1i_report_payload_is_deterministic(tmp_path) -> None:
    preregistration, config, evaluation = _build_report_inputs(tmp_path)

    first = build_phase1i_evaluation_report(config, preregistration, evaluation)
    second = build_phase1i_evaluation_report(config, preregistration, evaluation)

    assert phase1i_evaluation_report_payload(first) == phase1i_evaluation_report_payload(second)


def test_phase1i_report_rejects_trial_mismatch(tmp_path) -> None:
    preregistration, config, evaluation = _build_report_inputs(tmp_path)
    bad_evaluation = evaluation.__class__(
        evaluation_id=evaluation.evaluation_id,
        run_record=evaluation.run_record.model_copy(update={"trial_id": "wrong"}),
        is_bar_count=evaluation.is_bar_count,
        oos_bar_count=evaluation.oos_bar_count,
        leakage_status=evaluation.leakage_status,
        no_claim_labels=evaluation.no_claim_labels,
    )

    with pytest.raises(ValueError, match="trial_id mismatch"):
        build_phase1i_evaluation_report(config, preregistration, bad_evaluation)


def test_phase1j_decision_keeps_holdout_closed_without_performance_conclusion(tmp_path) -> None:
    preregistration, config, evaluation = _build_report_inputs(tmp_path)
    report = build_phase1i_evaluation_report(config, preregistration, evaluation)

    decision = build_phase1j_research_decision(report)

    assert decision.decision_id == PHASE1J_RESEARCH_DECISION_ID
    assert decision.holdout_gate_opened is False
    assert decision.reason_code == "NO_PERFORMANCE_CONCLUSION_FOR_HOLDOUT"
    assert decision.production_label is False
    assert decision.capital_ready_label is False
    assert len(phase1j_decision_hash(decision)) == 64


def test_phase1k_closure_packet_requires_holdout_gate_closed(tmp_path) -> None:
    preregistration, config, evaluation = _build_report_inputs(tmp_path)
    report = build_phase1i_evaluation_report(config, preregistration, evaluation)
    decision = build_phase1j_research_decision(report)

    packet = build_phase1k_closure_packet(decision)

    assert packet.packet_id == PHASE1K_RESEARCH_CLOSURE_PACKET_ID
    assert packet.deep_review_required_next is True
    assert packet.holdout_executed is False
    assert packet.production_label is False
    assert packet.capital_ready_label is False
    assert len(phase1k_closure_hash(packet)) == 64


def _build_report_inputs(tmp_path):
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
            PROJECT_ROOT / "entropy" / "baseline" / "bounded.py",
            PROJECT_ROOT / "entropy" / "baseline" / "implementation.py",
        ),
    )
    preregistration = build_phase1f_preregistration_surface(
        binding,
        registered_at=_dt(2026, 5, 6),
    )
    config = build_phase1g_evaluation_config(
        preregistration,
        formation_start=_dt(2021, 1, 1),
        formation_end=_dt(2021, 1, 3),
        validation_start=_dt(2021, 1, 5),
        validation_end=_dt(2021, 1, 8),
        embargo_bars=1,
    )
    evaluation = run_phase1h_governed_evaluation(config, _bars())
    return preregistration, config, evaluation


def _bars() -> tuple[Phase1HBar, ...]:
    return tuple(
        Phase1HBar(
            timestamp=_dt(2021, 1, day),
            open=100.0 + day,
            high=101.0 + day,
            low=99.0 + day,
            close=100.5 + day,
            volume=1_000.0 + day,
        )
        for day in range(1, 9)
    )


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


def _dt(year: int, month: int, day: int):
    return datetime(year, month, day, tzinfo=timezone.utc)


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
