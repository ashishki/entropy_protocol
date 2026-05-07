from __future__ import annotations

import json

import pytest

from entropy.evidence.phase1a_baseline import build_phase1a_baseline_registration_manifest
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
    Phase1AReadRequest,
    authorize_phase1a_archive_read,
)
from entropy.evidence.phase1a_scaffold import (
    PHASE1A_BASELINE_SCAFFOLD_ID,
    PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY,
    Phase1AScaffoldPortfolioRequest,
    authorize_phase1a_scaffold_read,
    load_phase1a_baseline_scaffold,
    validate_phase1a_scaffold_constraints,
)


def test_load_phase1a_baseline_scaffold_exposes_non_trading_placeholders(tmp_path) -> None:
    boundary_path, registration_path = _build_registration(tmp_path)

    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=registration_path)

    assert boundary_path.exists()
    assert scaffold.scaffold_id == PHASE1A_BASELINE_SCAFFOLD_ID
    assert scaffold.archive_only is True
    assert scaffold.gate_claim_allowed is False
    assert scaffold.direction == "long_only"
    assert scaffold.workload_boundary == PHASE1A_SCAFFOLD_WORKLOAD_BOUNDARY
    assert len(scaffold.skill_placeholders) == 6
    assert scaffold.skill_placeholders[0].placeholder_id == "P1A-SKILL-01-trend_following"
    assert {placeholder.runtime_status for placeholder in scaffold.skill_placeholders} == {
        "placeholder_non_trading"
    }
    assert {placeholder.output_status for placeholder in scaffold.skill_placeholders} == {
        "no_signal_no_score_no_weight"
    }


def test_phase1a_scaffold_constraints_enforce_long_only_no_leverage(tmp_path) -> None:
    _, registration_path = _build_registration(tmp_path)
    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=registration_path)

    allowed = validate_phase1a_scaffold_constraints(
        scaffold,
        Phase1AScaffoldPortfolioRequest(gross_exposure=0.75),
    )
    short_denied = validate_phase1a_scaffold_constraints(
        scaffold,
        Phase1AScaffoldPortfolioRequest(gross_exposure=0.75, short_exposure=0.01),
    )
    leverage_denied = validate_phase1a_scaffold_constraints(
        scaffold,
        Phase1AScaffoldPortfolioRequest(gross_exposure=0.75, leverage="2x"),
    )
    gross_denied = validate_phase1a_scaffold_constraints(
        scaffold,
        Phase1AScaffoldPortfolioRequest(gross_exposure=1.01),
    )

    assert allowed.allowed is True
    assert allowed.reason_code == "CONSTRAINTS_ALLOWED"
    assert short_denied.allowed is False
    assert short_denied.reason_code == "SHORT_EXPOSURE_NOT_ALLOWED"
    assert leverage_denied.allowed is False
    assert leverage_denied.reason_code == "LEVERAGE_NOT_ALLOWED"
    assert gross_denied.allowed is False
    assert gross_denied.reason_code == "GROSS_EXPOSURE_ABOVE_MAX"


def test_phase1a_scaffold_authorizes_formation_and_registered_validation(tmp_path) -> None:
    boundary_path, registration_path = _build_registration(tmp_path)
    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=registration_path)

    formation = authorize_phase1a_scaffold_read(
        scaffold=scaffold,
        boundary_manifest_path=boundary_path,
        symbol="BTCUSDT",
        split_label=PHASE1A_FORMATION_LABEL,
    )
    missing_validation_metadata = authorize_phase1a_archive_read(
        boundary_manifest_path=boundary_path,
        request=Phase1AReadRequest(
            symbol="BTCUSDT",
            split_label=PHASE1A_VALIDATION_LABEL,
            read_purpose="registered_validation",
        ),
    )
    registered_validation = authorize_phase1a_scaffold_read(
        scaffold=scaffold,
        boundary_manifest_path=boundary_path,
        symbol="BTCUSDT",
        split_label=PHASE1A_VALIDATION_LABEL,
    )

    assert formation.allowed is True
    assert formation.window_start == "2020-01-01"
    assert formation.window_end == "2022-12-31"
    assert missing_validation_metadata.allowed is False
    assert missing_validation_metadata.reason_code == "MISSING_REQUIRED_REGISTRATION_FIELDS"
    assert registered_validation.allowed is True
    assert registered_validation.window_start == "2023-01-01"
    assert registered_validation.window_end == "2024-12-31"


def test_phase1a_scaffold_keeps_holdout_locked(tmp_path) -> None:
    boundary_path, registration_path = _build_registration(tmp_path)
    scaffold = load_phase1a_baseline_scaffold(registration_manifest_path=registration_path)

    authorization = authorize_phase1a_scaffold_read(
        scaffold=scaffold,
        boundary_manifest_path=boundary_path,
        symbol="BTCUSDT",
        split_label=PHASE1A_HOLDOUT_LABEL,
    )

    assert authorization.allowed is False
    assert authorization.reason_code == "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION"


def test_load_phase1a_baseline_scaffold_rejects_mutated_spec_hash(tmp_path) -> None:
    _, registration_path = _build_registration(tmp_path)
    payload = json.loads(registration_path.read_text(encoding="utf-8"))
    payload["baseline_spec"]["version"] = "v2"
    registration_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="spec hash mismatch"):
        load_phase1a_baseline_scaffold(registration_manifest_path=registration_path)


def test_load_phase1a_baseline_scaffold_rejects_executable_signal_status(tmp_path) -> None:
    _, registration_path = _build_registration(tmp_path)
    payload = json.loads(registration_path.read_text(encoding="utf-8"))
    payload["baseline_spec"]["signal_runtime_status"] = "implemented"
    registration_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="must not load executable signal logic"):
        load_phase1a_baseline_scaffold(registration_manifest_path=registration_path)


def _build_registration(tmp_path):
    boundary_path = _write_boundary_manifest(tmp_path)
    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )
    return boundary_path, result.manifest_path


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
