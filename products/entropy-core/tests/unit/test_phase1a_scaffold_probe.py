from __future__ import annotations

import json

import polars as pl
import pytest

from entropy.evidence.phase1a_baseline import build_phase1a_baseline_registration_manifest
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
)
from entropy.evidence.phase1a_scaffold import load_phase1a_baseline_scaffold
from entropy.evidence.phase1a_scaffold_probe import (
    PHASE1A_SCAFFOLD_PROBE_ID,
    PHASE1A_SCAFFOLD_PROBE_NO_CLAIM_LABELS,
    Phase1AScaffoldProbeConfig,
    run_phase1a_scaffold_performance_probe,
)


def test_phase1a_scaffold_probe_writes_no_claim_manifest_and_artifact(tmp_path) -> None:
    scaffold = _build_scaffold(tmp_path)

    result = run_phase1a_scaffold_performance_probe(
        scaffold=scaffold,
        output_dir=tmp_path / "probe",
        config=Phase1AScaffoldProbeConfig(row_count=25, trial_shape_count=5),
    )

    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    frame = pl.read_parquet(result.artifact_path)
    assert result.benchmark_id == PHASE1A_SCAFFOLD_PROBE_ID
    assert result.row_count == 25
    assert result.artifact_size_bytes > 0
    assert len(result.replay_hash) == 64
    assert payload["no_claim_labels"] == list(PHASE1A_SCAFFOLD_PROBE_NO_CLAIM_LABELS)
    assert payload["forbidden_outputs_absent"] is True
    assert payload["rows_processed"] == 25
    assert payload["backend"] == "polars"
    assert payload["data_boundary"] == "synthetic_non_claim"
    assert frame.height == 25
    assert set(frame.columns) == {
        "row_index",
        "symbol_slot",
        "skill_slot",
        "scaffold_id",
        "baseline_spec_hash",
        "workload_id",
        "data_boundary",
    }


def test_phase1a_scaffold_probe_replay_hash_is_stable(tmp_path) -> None:
    scaffold = _build_scaffold(tmp_path)
    config = Phase1AScaffoldProbeConfig(row_count=10, symbol_count=3, trial_shape_count=2)

    first = run_phase1a_scaffold_performance_probe(
        scaffold=scaffold,
        output_dir=tmp_path / "probe_1",
        config=config,
    )
    second = run_phase1a_scaffold_performance_probe(
        scaffold=scaffold,
        output_dir=tmp_path / "probe_2",
        config=config,
    )

    assert first.replay_hash == second.replay_hash


def test_phase1a_scaffold_probe_rejects_holdout_boundary(tmp_path) -> None:
    scaffold = _build_scaffold(tmp_path)

    with pytest.raises(ValueError, match="data_boundary is not allowed"):
        run_phase1a_scaffold_performance_probe(
            scaffold=scaffold,
            output_dir=tmp_path / "probe",
            config=Phase1AScaffoldProbeConfig(data_boundary="archive_holdout"),
        )


def test_phase1a_scaffold_probe_rejects_non_polars_backend(tmp_path) -> None:
    scaffold = _build_scaffold(tmp_path)

    with pytest.raises(ValueError, match="supports only polars"):
        run_phase1a_scaffold_performance_probe(
            scaffold=scaffold,
            output_dir=tmp_path / "probe",
            config=Phase1AScaffoldProbeConfig(backend="rust"),
        )


def test_phase1a_scaffold_probe_manifest_has_no_strategy_metric_fields(tmp_path) -> None:
    scaffold = _build_scaffold(tmp_path)

    result = run_phase1a_scaffold_performance_probe(
        scaffold=scaffold,
        output_dir=tmp_path / "probe",
        config=Phase1AScaffoldProbeConfig(row_count=5),
    )

    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    forbidden_fields = {
        "sharpe",
        "drawdown",
        "return",
        "ic",
        "alpha",
        "edge",
        "pnl",
        "hit_rate",
        "trade_quality",
    }
    assert forbidden_fields.isdisjoint(set(payload))


def _build_scaffold(tmp_path):
    boundary_path = _write_boundary_manifest(tmp_path)
    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )
    return load_phase1a_baseline_scaffold(registration_manifest_path=result.manifest_path)


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
                        "allowed_purposes": [
                            "feature_design",
                            "baseline_spec_drafting",
                            "instrumentation",
                        ],
                        "required_fields": [],
                        "locked_reason": None,
                    },
                    {
                        "split_label": PHASE1A_VALIDATION_LABEL,
                        "window_start": "2023-01-01",
                        "window_end": "2024-12-31",
                        "default_access": "ALLOW_WITH_REGISTRATION",
                        "allowed_purposes": ["registered_validation"],
                        "required_fields": [
                            "baseline_registration_id",
                            "baseline_spec_hash",
                            "validation_registration_hash",
                        ],
                        "locked_reason": None,
                    },
                    {
                        "split_label": PHASE1A_HOLDOUT_LABEL,
                        "window_start": "2025-01-01",
                        "window_end": "2025-12-31",
                        "default_access": "LOCKED",
                        "allowed_purposes": ["final_holdout_audit"],
                        "required_fields": [
                            "baseline_registration_id",
                            "baseline_spec_hash",
                            "validation_registration_hash",
                            "holdout_unlock_id",
                        ],
                        "locked_reason": "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return boundary_path
