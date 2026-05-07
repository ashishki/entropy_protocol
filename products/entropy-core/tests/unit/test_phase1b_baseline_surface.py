from __future__ import annotations

import json
from dataclasses import replace

import pytest

from entropy.baseline.long_only import (
    PHASE1B_BASELINE_NO_CLAIM_LABELS,
    PHASE1B_BASELINE_SURFACE_ID,
    PHASE1B_FORBIDDEN_OUTPUT_COLUMNS,
    PHASE1B_REQUIRED_OUTPUT_COLUMNS,
    Phase1BBaselineSurfaceRequest,
    build_phase1b_long_only_baseline_surface,
    phase1b_surface_schema_hash,
    phase1b_surface_schema_payload,
    validate_phase1b_baseline_surface_request,
)
from entropy.evidence.phase1a_baseline import build_phase1a_baseline_registration_manifest
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
)
from entropy.evidence.phase1a_scaffold import load_phase1a_baseline_scaffold


def test_phase1b_surface_builds_from_phase1a_scaffold_without_claims(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    assert surface.surface_id == PHASE1B_BASELINE_SURFACE_ID
    assert surface.archive_only is True
    assert surface.evaluation_allowed is False
    assert surface.gate_claim_allowed is False
    assert surface.allowed_split_labels == (PHASE1A_FORMATION_LABEL,)
    assert PHASE1A_VALIDATION_LABEL in surface.denied_split_labels
    assert PHASE1A_HOLDOUT_LABEL in surface.denied_split_labels
    assert len(surface.skill_interfaces) == 6
    assert {skill.implementation_status for skill in surface.skill_interfaces} == {
        "interface_only_no_alpha_logic"
    }
    assert surface.no_claim_labels == PHASE1B_BASELINE_NO_CLAIM_LABELS


def test_phase1b_surface_allows_formation_schema_only_request(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    decision = validate_phase1b_baseline_surface_request(
        surface,
        Phase1BBaselineSurfaceRequest(
            split_label=PHASE1A_FORMATION_LABEL,
            requested_skill_families=("trend_following", "breakout"),
            output_columns=PHASE1B_REQUIRED_OUTPUT_COLUMNS,
        ),
    )

    assert decision.allowed is True
    assert decision.reason_code == "SURFACE_REQUEST_ALLOWED"


def test_phase1b_surface_denies_validation_and_holdout(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    validation = validate_phase1b_baseline_surface_request(
        surface,
        Phase1BBaselineSurfaceRequest(
            split_label=PHASE1A_VALIDATION_LABEL,
            requested_skill_families=("trend_following",),
            output_columns=PHASE1B_REQUIRED_OUTPUT_COLUMNS,
        ),
    )
    holdout = validate_phase1b_baseline_surface_request(
        surface,
        Phase1BBaselineSurfaceRequest(
            split_label=PHASE1A_HOLDOUT_LABEL,
            requested_skill_families=("trend_following",),
            output_columns=PHASE1B_REQUIRED_OUTPUT_COLUMNS,
        ),
    )

    assert validation.allowed is False
    assert validation.reason_code == "SPLIT_LABEL_DENIED"
    assert holdout.allowed is False
    assert holdout.reason_code == "SPLIT_LABEL_DENIED"


def test_phase1b_surface_rejects_forbidden_output_columns(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    decision = validate_phase1b_baseline_surface_request(
        surface,
        Phase1BBaselineSurfaceRequest(
            split_label=PHASE1A_FORMATION_LABEL,
            requested_skill_families=("trend_following",),
            output_columns=PHASE1B_REQUIRED_OUTPUT_COLUMNS + ("alpha_score", "target_weight"),
        ),
    )

    assert decision.allowed is False
    assert decision.reason_code == "FORBIDDEN_OUTPUT_COLUMN"


def test_phase1b_surface_rejects_unknown_family_and_missing_columns(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    unknown_family = validate_phase1b_baseline_surface_request(
        surface,
        Phase1BBaselineSurfaceRequest(
            split_label=PHASE1A_FORMATION_LABEL,
            requested_skill_families=("unknown_family",),
            output_columns=PHASE1B_REQUIRED_OUTPUT_COLUMNS,
        ),
    )
    missing_column = validate_phase1b_baseline_surface_request(
        surface,
        Phase1BBaselineSurfaceRequest(
            split_label=PHASE1A_FORMATION_LABEL,
            requested_skill_families=("trend_following",),
            output_columns=tuple(
                column for column in PHASE1B_REQUIRED_OUTPUT_COLUMNS if column != "surface_id"
            ),
        ),
    )

    assert unknown_family.allowed is False
    assert unknown_family.reason_code == "UNKNOWN_SKILL_FAMILY"
    assert missing_column.allowed is False
    assert missing_column.reason_code == "MISSING_REQUIRED_OUTPUT_COLUMN"


def test_phase1b_surface_schema_hash_is_stable_and_no_claim(tmp_path) -> None:
    surface = _build_surface(tmp_path)

    payload = phase1b_surface_schema_payload(surface)
    first_hash = phase1b_surface_schema_hash(surface)
    second_hash = phase1b_surface_schema_hash(surface)

    assert first_hash == second_hash
    assert payload["evaluation_allowed"] is False
    assert payload["gate_claim_allowed"] is False
    forbidden_columns = payload["forbidden_output_columns"]
    assert isinstance(forbidden_columns, list)
    assert set(forbidden_columns) == set(PHASE1B_FORBIDDEN_OUTPUT_COLUMNS)


def test_phase1b_surface_rejects_gate_claim_scaffold(tmp_path) -> None:
    scaffold = _build_scaffold(tmp_path)

    with pytest.raises(ValueError, match="must not allow gate claims"):
        build_phase1b_long_only_baseline_surface(replace(scaffold, gate_claim_allowed=True))


def _build_surface(tmp_path):
    return build_phase1b_long_only_baseline_surface(_build_scaffold(tmp_path))


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
