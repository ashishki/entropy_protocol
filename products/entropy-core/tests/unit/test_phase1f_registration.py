from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import pytest

from entropy.baseline.bounded import build_phase1e_all_bounded_baseline_outputs
from entropy.baseline.formation import prepare_phase1b_formation_input
from entropy.baseline.implementation import build_phase1d_implementation_contract
from entropy.baseline.long_only import build_phase1b_long_only_baseline_surface
from entropy.baseline.readiness import (
    Phase1CReadinessArtifacts,
    build_phase1c_readiness_contract,
    run_phase1c_preflight_checklist,
)
from entropy.baseline.registration import (
    PHASE1F_BASELINE_HASH_BINDING_ID,
    PHASE1F_FAMILY_TAG,
    PHASE1F_TRIAL_ID,
    PHASE1F_TRIAL_PREREGISTRATION_SURFACE_ID,
    build_phase1f_baseline_hash_binding,
    build_phase1f_preregistration_surface,
    phase1f_hash_binding_hash,
    phase1f_hash_binding_payload,
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


def test_phase1f_hash_binding_records_code_policy_input_and_dataset_hashes(tmp_path) -> None:
    surface, formation, contract, outputs = _build_registration_inputs(tmp_path)

    binding = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        outputs,
        source_paths=_source_paths(),
    )

    assert binding.binding_id == PHASE1F_BASELINE_HASH_BINDING_ID
    assert binding.trial_id == PHASE1F_TRIAL_ID
    assert binding.family_tag == PHASE1F_FAMILY_TAG
    assert len(binding.code_hash) == 64
    assert len(binding.policy_hash) == 64
    assert len(binding.input_contract_hash) == 64
    assert len(binding.dataset_hash) == 64
    assert len(binding.output_hashes) == 6
    assert binding.registry_write_allowed is False
    assert binding.evaluation_allowed is False
    assert binding.gate_claim_allowed is False
    assert binding.phase_gate_evidence is False


def test_phase1f_hash_binding_payload_and_hash_are_deterministic(tmp_path) -> None:
    surface, formation, contract, outputs = _build_registration_inputs(tmp_path)

    first = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        outputs,
        source_paths=_source_paths(),
    )
    second = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        tuple(reversed(outputs)),
        source_paths=tuple(reversed(_source_paths())),
    )

    assert phase1f_hash_binding_payload(first) == phase1f_hash_binding_payload(second)
    assert phase1f_hash_binding_hash(first) == phase1f_hash_binding_hash(second)


def test_phase1f_code_hash_is_stable_for_absolute_and_relative_paths(tmp_path) -> None:
    surface, formation, contract, outputs = _build_registration_inputs(tmp_path)
    relative_paths = tuple(path.relative_to(PROJECT_ROOT) for path in _source_paths())

    absolute = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        outputs,
        source_paths=_source_paths(),
    )
    relative = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        outputs,
        source_paths=relative_paths,
    )

    assert absolute.code_hash == relative.code_hash
    assert phase1f_hash_binding_hash(absolute) == phase1f_hash_binding_hash(relative)


def test_phase1f_hash_binding_requires_all_registered_outputs(tmp_path) -> None:
    surface, formation, contract, outputs = _build_registration_inputs(tmp_path)

    with pytest.raises(ValueError, match="all registered skill families"):
        build_phase1f_baseline_hash_binding(
            surface,
            formation,
            contract,
            outputs[:-1],
            source_paths=_source_paths(),
        )


def test_phase1f_hash_binding_rejects_missing_source_path(tmp_path) -> None:
    surface, formation, contract, outputs = _build_registration_inputs(tmp_path)

    with pytest.raises(ValueError, match="source does not exist"):
        build_phase1f_baseline_hash_binding(
            surface,
            formation,
            contract,
            outputs,
            source_paths=(PROJECT_ROOT / "missing.py",),
        )


def test_phase1f_preregistration_surface_builds_trial_spec_without_registry_write(tmp_path) -> None:
    surface, formation, contract, outputs = _build_registration_inputs(tmp_path)
    binding = build_phase1f_baseline_hash_binding(
        surface,
        formation,
        contract,
        outputs,
        source_paths=_source_paths(),
    )

    preregistration = build_phase1f_preregistration_surface(
        binding,
        registered_at=datetime(2026, 5, 6, 0, 0, tzinfo=timezone.utc),
    )

    assert preregistration.surface_id == PHASE1F_TRIAL_PREREGISTRATION_SURFACE_ID
    assert preregistration.registry_write_allowed is False
    assert preregistration.evaluation_allowed is False
    assert preregistration.gate_claim_allowed is False
    assert preregistration.phase_gate_evidence is False
    assert preregistration.trial_spec.trial_id == PHASE1F_TRIAL_ID
    assert preregistration.trial_spec.dataset_hash == binding.dataset_hash
    assert preregistration.trial_spec.code_hash == binding.code_hash
    assert preregistration.trial_spec.policy_hash == binding.policy_hash
    assert preregistration.trial_spec.parameter_lock["registry_write_allowed"] is False


def _build_registration_inputs(tmp_path):
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
    return surface, formation, contract, outputs


def _source_paths() -> tuple[Path, ...]:
    return (
        PROJECT_ROOT / "src" / "entropy" / "baseline" / "bounded.py",
        PROJECT_ROOT / "src" / "entropy" / "baseline" / "implementation.py",
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
