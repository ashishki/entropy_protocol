from __future__ import annotations

import json

import polars as pl
import pytest

from entropy.baseline.features import (
    PHASE1B_FEATURE_CONTRACT_ID,
    PHASE1B_REQUIRED_INPUT_COLUMNS,
    phase1b_feature_contract_hash,
    phase1b_feature_contract_payload,
    validate_phase1b_feature_columns,
)
from entropy.baseline.formation import (
    PHASE1B_FORMATION_INPUT_ADAPTER_ID,
    prepare_phase1b_formation_input,
)
from entropy.baseline.long_only import (
    PHASE1B_FORBIDDEN_OUTPUT_COLUMNS,
    PHASE1B_REQUIRED_OUTPUT_COLUMNS,
    build_phase1b_long_only_baseline_surface,
)
from entropy.baseline.skills import (
    PHASE1B_BASELINE_BENCHMARK_ID,
    PHASE1B_SKILL_STUB_OUTPUT_ID,
    build_phase1b_all_skill_stub_outputs,
    build_phase1b_skill_stub_output,
    run_phase1b_baseline_surface_benchmark,
)
from entropy.evidence.phase1a_baseline import build_phase1a_baseline_registration_manifest
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
)
from entropy.evidence.phase1a_scaffold import load_phase1a_baseline_scaffold


def test_feature_contract_allows_only_formation_ohlcv_columns() -> None:
    decision = validate_phase1b_feature_columns(PHASE1B_REQUIRED_INPUT_COLUMNS)
    forbidden = validate_phase1b_feature_columns(PHASE1B_REQUIRED_INPUT_COLUMNS + ("alpha_score",))
    unknown = validate_phase1b_feature_columns(PHASE1B_REQUIRED_INPUT_COLUMNS + ("custom_feature",))

    assert decision.allowed is True
    assert decision.reason_code == "FEATURE_COLUMNS_ALLOWED"
    assert forbidden.allowed is False
    assert forbidden.reason_code == "FORBIDDEN_FEATURE_COLUMN"
    assert unknown.allowed is False
    assert unknown.reason_code == "UNKNOWN_FEATURE_COLUMN"


def test_feature_contract_payload_and_hash_are_stable() -> None:
    payload = phase1b_feature_contract_payload()

    assert payload["contract_id"] == PHASE1B_FEATURE_CONTRACT_ID
    assert payload["lookahead_allowed"] is False
    assert payload["performance_fields_allowed"] is False
    assert phase1b_feature_contract_hash() == phase1b_feature_contract_hash()


def test_formation_adapter_sorts_and_hashes_formation_rows(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    rows = _formation_rows()

    prepared = prepare_phase1b_formation_input(surface, rows)
    replay = prepare_phase1b_formation_input(surface, rows.sort("timestamp_utc", descending=True))

    assert prepared.adapter_id == PHASE1B_FORMATION_INPUT_ADAPTER_ID
    assert prepared.split_label == PHASE1A_FORMATION_LABEL
    assert prepared.row_count == 3
    assert prepared.symbol_count == 2
    assert prepared.evaluation_allowed is False
    assert prepared.gate_claim_allowed is False
    assert prepared.input_hash == replay.input_hash
    assert prepared.frame.columns == list(PHASE1B_REQUIRED_INPUT_COLUMNS)


def test_formation_adapter_rejects_holdout_and_forbidden_columns(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    with pytest.raises(ValueError, match="only accepts formation"):
        prepare_phase1b_formation_input(surface, _formation_rows(), split_label=PHASE1A_HOLDOUT_LABEL)
    with pytest.raises(ValueError, match="FORBIDDEN_FEATURE_COLUMN"):
        prepare_phase1b_formation_input(
            surface,
            _formation_rows().with_columns(pl.lit(0.1).alias("future_return")),
        )


def test_formation_adapter_rejects_bad_ohlcv_values(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    with pytest.raises(ValueError, match="OHLCV sanity"):
        prepare_phase1b_formation_input(
            surface,
            _formation_rows().with_columns(pl.lit(-1.0).alias("close")),
        )


def test_skill_stub_outputs_required_no_claim_schema(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    output = build_phase1b_skill_stub_output(surface, formation, skill_family="trend_following")

    assert output.output_id == PHASE1B_SKILL_STUB_OUTPUT_ID
    assert output.evaluation_allowed is False
    assert output.gate_claim_allowed is False
    assert output.row_count == formation.row_count
    assert set(output.columns) == set(PHASE1B_REQUIRED_OUTPUT_COLUMNS)
    assert not set(output.columns).intersection(PHASE1B_FORBIDDEN_OUTPUT_COLUMNS)
    assert set(output.frame.get_column("no_claim_label").unique().to_list()) == {"not_alpha_logic"}


def test_all_skill_stubs_cover_registered_families(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    outputs = build_phase1b_all_skill_stub_outputs(surface, formation)

    assert len(outputs) == 6
    assert {output.skill_family for output in outputs} == {
        skill.family for skill in surface.skill_interfaces
    }
    assert sum(output.row_count for output in outputs) == formation.row_count * 6


def test_skill_stub_rejects_unknown_family(tmp_path) -> None:
    surface = _build_surface(tmp_path)
    formation = prepare_phase1b_formation_input(surface, _formation_rows())

    with pytest.raises(ValueError, match="registered skill family"):
        build_phase1b_skill_stub_output(surface, formation, skill_family="unknown")


def test_phase1b_mechanics_benchmark_is_no_claim(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    result = run_phase1b_baseline_surface_benchmark(surface, row_count=25)

    assert result.benchmark_id == PHASE1B_BASELINE_BENCHMARK_ID
    assert result.row_count == 25
    assert result.skill_family_count == 6
    assert result.output_row_count == 150
    assert result.wall_clock_seconds >= 0
    assert result.peak_memory_bytes >= 0
    assert result.evaluation_allowed is False
    assert result.gate_claim_allowed is False


def _build_surface(tmp_path):
    boundary_path = _write_boundary_manifest(tmp_path)
    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )
    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=result.manifest_path)
    return build_phase1b_long_only_baseline_surface(scaffold)


def _formation_rows() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "symbol": ["ETHUSDT", "BTCUSDT", "BTCUSDT"],
            "timestamp_utc": [
                "2021-01-03T00:00:00Z",
                "2021-01-01T00:00:00Z",
                "2021-01-02T00:00:00Z",
            ],
            "open": [101.0, 100.0, 100.5],
            "high": [102.0, 101.0, 101.5],
            "low": [100.0, 99.0, 99.5],
            "close": [101.5, 100.5, 101.0],
            "volume": [10.0, 11.0, 12.0],
            "dataset_hash": ["eth_hash", "btc_hash", "btc_hash"],
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
