from __future__ import annotations

import json

import pytest

from entropy.evidence.phase1a_baseline import (
    PHASE1A_BASELINE_REGISTRATION_ID,
    Phase1ABaselineSpec,
    Phase1APortfolioConstraints,
    build_phase1a_baseline_registration_manifest,
)
from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
    Phase1AReadRequest,
    authorize_phase1a_archive_read,
)


def test_build_phase1a_baseline_registration_manifest_writes_hashes(tmp_path) -> None:
    boundary_path = _write_boundary_manifest(tmp_path)

    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )

    assert result.registration_id == PHASE1A_BASELINE_REGISTRATION_ID
    assert result.archive_only is True
    assert result.gate_claim_allowed is False
    assert len(result.manifest_hash) == 64
    assert len(result.baseline_spec_hash) == 64
    assert len(result.validation_registration_hash) == 64
    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert payload["validation_access"]["baseline_spec_hash"] == result.baseline_spec_hash
    assert payload["holdout_access"]["access"] == "locked"
    assert payload["baseline_spec"]["signal_runtime_status"] == "not_implemented"
    summary = result.summary_path.read_text(encoding="utf-8")
    assert "non-executable baseline specification" in summary
    assert "does not implement strategies" in summary


def test_registered_baseline_metadata_authorizes_validation_read(tmp_path) -> None:
    boundary_path = _write_boundary_manifest(tmp_path)
    result = build_phase1a_baseline_registration_manifest(
        boundary_manifest_path=boundary_path,
        output_dir=tmp_path / "registration",
    )
    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    validation_access = payload["validation_access"]

    authorization = authorize_phase1a_archive_read(
        boundary_manifest_path=boundary_path,
        request=Phase1AReadRequest(
            symbol="BTCUSDT",
            split_label=PHASE1A_VALIDATION_LABEL,
            read_purpose="registered_validation",
            baseline_registration_id=validation_access["baseline_registration_id"],
            baseline_spec_hash=validation_access["baseline_spec_hash"],
            validation_registration_hash=validation_access["validation_registration_hash"],
        ),
    )

    assert authorization.allowed is True
    assert authorization.window_start == "2023-01-01"
    assert authorization.window_end == "2024-12-31"


def test_build_phase1a_baseline_registration_rejects_holdout_allowed(tmp_path) -> None:
    boundary_path = _write_boundary_manifest(tmp_path)
    spec = Phase1ABaselineSpec(
        allowed_split_labels=(
            PHASE1A_FORMATION_LABEL,
            PHASE1A_VALIDATION_LABEL,
            PHASE1A_HOLDOUT_LABEL,
        ),
        forbidden_split_labels=(),
    )

    with pytest.raises(ValueError, match="holdout split"):
        build_phase1a_baseline_registration_manifest(
            boundary_manifest_path=boundary_path,
            output_dir=tmp_path / "registration",
            baseline_spec=spec,
        )


def test_build_phase1a_baseline_registration_rejects_executable_signal_status(tmp_path) -> None:
    boundary_path = _write_boundary_manifest(tmp_path)
    spec = Phase1ABaselineSpec(signal_runtime_status="implemented")

    with pytest.raises(ValueError, match="must not implement signals"):
        build_phase1a_baseline_registration_manifest(
            boundary_manifest_path=boundary_path,
            output_dir=tmp_path / "registration",
            baseline_spec=spec,
        )


def test_build_phase1a_baseline_registration_rejects_leverage(tmp_path) -> None:
    boundary_path = _write_boundary_manifest(tmp_path)
    spec = Phase1ABaselineSpec(portfolio_constraints=Phase1APortfolioConstraints(leverage="2x"))

    with pytest.raises(ValueError, match="leverage"):
        build_phase1a_baseline_registration_manifest(
            boundary_manifest_path=boundary_path,
            output_dir=tmp_path / "registration",
            baseline_spec=spec,
        )


def test_build_phase1a_baseline_registration_rejects_boundary_hash_mismatch(tmp_path) -> None:
    boundary_path = _write_boundary_manifest(tmp_path)

    with pytest.raises(ValueError, match="boundary manifest hash"):
        build_phase1a_baseline_registration_manifest(
            boundary_manifest_path=boundary_path,
            output_dir=tmp_path / "registration",
            expected_boundary_manifest_hash="0" * 64,
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
                        "allowed_purposes": ["baseline_spec_drafting"],
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
                        "required_fields": ["holdout_unlock_id"],
                        "locked_reason": "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return boundary_path
