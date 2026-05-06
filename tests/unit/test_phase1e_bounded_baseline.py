from __future__ import annotations

import json

import polars as pl
import pytest

from entropy.baseline.bounded import (
    PHASE1E_BOUNDED_BASELINE_LOGIC_ID,
    PHASE1E_BOUNDED_BASELINE_OUTPUT_ID,
    PHASE1E_NO_CLAIM_LABELS,
    PHASE1E_REQUIRED_OUTPUT_COLUMNS,
    build_phase1e_all_bounded_baseline_outputs,
    build_phase1e_bounded_baseline_output,
)
from entropy.baseline.formation import prepare_phase1b_formation_input
from entropy.baseline.implementation import build_phase1d_implementation_contract
from entropy.baseline.long_only import (
    PHASE1B_FORBIDDEN_OUTPUT_COLUMNS,
    build_phase1b_long_only_baseline_surface,
)
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


def test_phase1e_bounded_output_builds_formation_observations_without_claims(tmp_path) -> None:
    surface, contract = _build_surface_and_contract(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    output = build_phase1e_bounded_baseline_output(
        surface,
        formation,
        contract,
        skill_family="trend_following",
    )

    assert output.output_id == PHASE1E_BOUNDED_BASELINE_OUTPUT_ID
    assert output.logic_id == PHASE1E_BOUNDED_BASELINE_LOGIC_ID
    assert output.skill_family == "trend_following"
    assert output.row_count == formation.row_count
    assert output.columns == PHASE1E_REQUIRED_OUTPUT_COLUMNS
    assert output.no_claim_labels == PHASE1E_NO_CLAIM_LABELS
    assert output.evaluation_allowed is False
    assert output.gate_claim_allowed is False
    assert output.phase_gate_evidence is False
    assert not set(output.columns).intersection(PHASE1B_FORBIDDEN_OUTPUT_COLUMNS)
    assert set(output.frame.get_column("no_claim_label").unique().to_list()) == {
        "formation_only_observation"
    }


def test_phase1e_outputs_cover_every_registered_skill_family(tmp_path) -> None:
    surface, contract = _build_surface_and_contract(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    outputs = build_phase1e_all_bounded_baseline_outputs(surface, formation, contract)

    assert len(outputs) == 6
    assert {output.skill_family for output in outputs} == {
        skill.family for skill in surface.skill_interfaces
    }
    assert sum(output.row_count for output in outputs) == formation.row_count * 6


def test_phase1e_output_hash_is_deterministic_across_replay(tmp_path) -> None:
    surface, contract = _build_surface_and_contract(tmp_path)
    rows = _formation_rows()
    formation = prepare_phase1b_formation_input(surface, rows)
    replay = prepare_phase1b_formation_input(surface, rows.sort("timestamp_utc", descending=True))

    output = build_phase1e_bounded_baseline_output(
        surface,
        formation,
        contract,
        skill_family="breakout",
    )
    replay_output = build_phase1e_bounded_baseline_output(
        surface,
        replay,
        contract,
        skill_family="breakout",
    )

    assert output.output_hash == replay_output.output_hash


def test_phase1e_observations_are_prefix_stable_without_future_rows(tmp_path) -> None:
    surface, contract = _build_surface_and_contract(tmp_path)
    full = prepare_phase1b_formation_input(surface, _formation_rows())
    prefix = prepare_phase1b_formation_input(surface, _formation_rows().head(4))

    full_output = build_phase1e_bounded_baseline_output(
        surface,
        full,
        contract,
        skill_family="mean_reversion",
    )
    prefix_output = build_phase1e_bounded_baseline_output(
        surface,
        prefix,
        contract,
        skill_family="mean_reversion",
    )

    full_prefix = full_output.frame.head(prefix_output.row_count)
    assert full_prefix.to_dicts() == prefix_output.frame.to_dicts()


def test_phase1e_requires_p1e_approval_before_replacing_schema_stubs(tmp_path) -> None:
    surface, contract = _build_surface_and_contract(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    with pytest.raises(ValueError, match="IMPLEMENTATION_APPROVAL_REQUIRED"):
        build_phase1e_bounded_baseline_output(
            surface,
            formation,
            contract,
            skill_family="trend_following",
            approval_gate_id="phase1d_contract_approval",
        )


def test_phase1e_rejects_unknown_skill_family(tmp_path) -> None:
    surface, contract = _build_surface_and_contract(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    with pytest.raises(ValueError, match="registered skill family"):
        build_phase1e_bounded_baseline_output(
            surface,
            formation,
            contract,
            skill_family="unknown",
        )


def test_phase1e_keeps_validation_and_holdout_blocked(tmp_path) -> None:
    surface, _ = _build_surface_and_contract(tmp_path)

    with pytest.raises(ValueError, match="only accepts formation"):
        prepare_phase1b_formation_input(
            surface,
            _formation_rows(),
            split_label=PHASE1A_VALIDATION_LABEL,
        )
    with pytest.raises(ValueError, match="only accepts formation"):
        prepare_phase1b_formation_input(
            surface,
            _formation_rows(),
            split_label=PHASE1A_HOLDOUT_LABEL,
        )


def _build_surface_and_contract(tmp_path):
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
    return surface, build_phase1d_implementation_contract(readiness_contract, checklist)


def _formation_rows() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "symbol": ["BTCUSDT", "BTCUSDT", "BTCUSDT", "BTCUSDT", "BTCUSDT", "ETHUSDT"],
            "timestamp_utc": [
                "2021-01-01T00:00:00Z",
                "2021-01-02T00:00:00Z",
                "2021-01-03T00:00:00Z",
                "2021-01-04T00:00:00Z",
                "2021-01-05T00:00:00Z",
                "2021-01-01T00:00:00Z",
            ],
            "open": [100.0, 101.0, 102.0, 103.0, 104.0, 200.0],
            "high": [101.0, 102.0, 103.0, 104.0, 105.0, 202.0],
            "low": [99.0, 100.0, 101.0, 102.0, 103.0, 198.0],
            "close": [100.5, 101.5, 102.5, 103.5, 104.5, 201.0],
            "volume": [10.0, 11.0, 12.0, 13.0, 14.0, 20.0],
            "dataset_hash": [
                "btc_hash",
                "btc_hash",
                "btc_hash",
                "btc_hash",
                "btc_hash",
                "eth_hash",
            ],
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
