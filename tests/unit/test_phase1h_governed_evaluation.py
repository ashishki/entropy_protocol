from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import pytest

from entropy.baseline.bounded import build_phase1e_all_bounded_baseline_outputs
from entropy.baseline.evaluation import build_phase1g_evaluation_config
from entropy.baseline.formation import prepare_phase1b_formation_input
from entropy.baseline.governed import (
    PHASE1H_GOVERNED_EVALUATION_RUN_ID,
    Phase1HBar,
    run_phase1h_governed_evaluation,
)
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
)
from entropy.evidence.phase1a_scaffold import load_phase1a_baseline_scaffold
from entropy.models.registry import LeakageStatus

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase1h_governed_evaluation_emits_run_record_without_claims(tmp_path) -> None:
    config = _build_config(tmp_path)

    result = run_phase1h_governed_evaluation(config, _bars())

    assert result.evaluation_id == PHASE1H_GOVERNED_EVALUATION_RUN_ID
    assert result.run_record.trial_id == config.trial_id
    assert result.run_record.dataset_hash == config.dataset_hash
    assert result.run_record.code_hash == config.code_hash
    assert result.run_record.policy_hash == config.policy_hash
    assert result.leakage_status is LeakageStatus.PASS
    assert result.is_bar_count == 3
    assert result.oos_bar_count == 4
    assert result.holdout_used is False
    assert result.performance_conclusion is False
    assert result.phase_gate_evidence is False
    assert result.production_label is False
    assert result.capital_ready_label is False


def test_phase1h_governed_evaluation_requires_p1g_approval(tmp_path) -> None:
    config = _build_config(tmp_path)

    with pytest.raises(ValueError, match="EVALUATION_APPROVAL_REQUIRED"):
        run_phase1h_governed_evaluation(
            config,
            _bars(),
            approval_gate_id="phase1d_contract_approval",
        )


def test_phase1h_run_id_is_deterministic_for_same_hashes(tmp_path) -> None:
    config = _build_config(tmp_path)

    first = run_phase1h_governed_evaluation(config, _bars())
    second = run_phase1h_governed_evaluation(config, _bars())

    assert first.run_record.run_id == second.run_record.run_id


def test_phase1h_rejects_leaky_is_features(tmp_path) -> None:
    config = _build_config(tmp_path)
    bars = list(_bars())
    bars[0] = Phase1HBar(
        timestamp=bars[0].timestamp,
        open=bars[0].open,
        high=bars[0].high,
        low=bars[0].low,
        close=bars[0].close,
        volume=bars[0].volume,
        feature_computed_through=_dt(2021, 1, 5),
    )

    with pytest.raises(ValueError, match="computed using data"):
        run_phase1h_governed_evaluation(config, tuple(bars))


def _build_config(tmp_path):
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
    return build_phase1g_evaluation_config(
        preregistration,
        formation_start=_dt(2021, 1, 1),
        formation_end=_dt(2021, 1, 3),
        validation_start=_dt(2021, 1, 5),
        validation_end=_dt(2021, 1, 8),
        embargo_bars=1,
    )


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


def _dt(year: int, month: int, day: int) -> datetime:
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
