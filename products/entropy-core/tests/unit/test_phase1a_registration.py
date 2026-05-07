from __future__ import annotations

import json

import pytest

from entropy.evidence.phase1a_registration import (
    PHASE1A_FORMATION_LABEL,
    PHASE1A_HOLDOUT_LABEL,
    PHASE1A_REGISTRATION_BOUNDARY_ID,
    PHASE1A_VALIDATION_LABEL,
    Phase1AReadRequest,
    authorize_phase1a_archive_read,
    build_phase1a_registration_boundary_manifest,
)


def test_build_phase1a_registration_boundary_locks_holdout(tmp_path) -> None:
    freeze_path = _write_freeze_manifest(tmp_path)

    result = build_phase1a_registration_boundary_manifest(
        freeze_manifest_path=freeze_path,
        output_dir=tmp_path / "boundary",
    )

    assert result.boundary_id == PHASE1A_REGISTRATION_BOUNDARY_ID
    assert result.archive_only is True
    assert result.gate_claim_allowed is False
    assert result.dataset_count == 2
    assert result.split_count == 3
    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    holdout_rule = _rule(payload, PHASE1A_HOLDOUT_LABEL)
    assert holdout_rule["default_access"] == "LOCKED"
    assert holdout_rule["locked_reason"] == "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION"
    assert "does not implement strategies" in result.summary_path.read_text(encoding="utf-8")


def test_authorize_phase1a_archive_read_allows_formation_only(tmp_path) -> None:
    freeze_path = _write_freeze_manifest(tmp_path)
    result = build_phase1a_registration_boundary_manifest(
        freeze_manifest_path=freeze_path,
        output_dir=tmp_path / "boundary",
    )

    authorization = authorize_phase1a_archive_read(
        boundary_manifest_path=result.manifest_path,
        request=Phase1AReadRequest(
            symbol="BTCUSDT",
            split_label=PHASE1A_FORMATION_LABEL,
            read_purpose="feature_design",
        ),
    )

    assert authorization.allowed is True
    assert authorization.reason_code == "READ_ALLOWED"
    assert authorization.window_start == "2020-01-01"
    assert authorization.window_end == "2022-12-31"
    assert authorization.dataset_hash == "btc_dataset_hash"
    assert authorization.parquet_path == "/tmp/BTCUSDT.parquet"
    assert authorization.gate_claim_allowed is False


def test_authorize_phase1a_archive_read_requires_validation_registration(tmp_path) -> None:
    freeze_path = _write_freeze_manifest(tmp_path)
    result = build_phase1a_registration_boundary_manifest(
        freeze_manifest_path=freeze_path,
        output_dir=tmp_path / "boundary",
    )

    denied = authorize_phase1a_archive_read(
        boundary_manifest_path=result.manifest_path,
        request=Phase1AReadRequest(
            symbol="BTCUSDT",
            split_label=PHASE1A_VALIDATION_LABEL,
            read_purpose="registered_validation",
        ),
    )
    allowed = authorize_phase1a_archive_read(
        boundary_manifest_path=result.manifest_path,
        request=Phase1AReadRequest(
            symbol="BTCUSDT",
            split_label=PHASE1A_VALIDATION_LABEL,
            read_purpose="registered_validation",
            baseline_registration_id="P1A-BASELINE-001",
            baseline_spec_hash="a" * 64,
            validation_registration_hash="b" * 64,
        ),
    )

    assert denied.allowed is False
    assert denied.reason_code == "MISSING_REQUIRED_REGISTRATION_FIELDS"
    assert allowed.allowed is True
    assert allowed.window_start == "2023-01-01"
    assert allowed.window_end == "2024-12-31"


def test_authorize_phase1a_archive_read_rejects_locked_holdout(tmp_path) -> None:
    freeze_path = _write_freeze_manifest(tmp_path)
    result = build_phase1a_registration_boundary_manifest(
        freeze_manifest_path=freeze_path,
        output_dir=tmp_path / "boundary",
    )

    authorization = authorize_phase1a_archive_read(
        boundary_manifest_path=result.manifest_path,
        request=Phase1AReadRequest(
            symbol="BTCUSDT",
            split_label=PHASE1A_HOLDOUT_LABEL,
            read_purpose="final_holdout_audit",
            baseline_registration_id="P1A-BASELINE-001",
            baseline_spec_hash="a" * 64,
            validation_registration_hash="b" * 64,
            holdout_unlock_id="P1A-HOLDOUT-UNLOCK-001",
        ),
    )

    assert authorization.allowed is False
    assert authorization.reason_code == "HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION"


def test_build_phase1a_registration_boundary_rejects_freeze_hash_mismatch(tmp_path) -> None:
    freeze_path = _write_freeze_manifest(tmp_path)

    with pytest.raises(ValueError, match="freeze manifest hash"):
        build_phase1a_registration_boundary_manifest(
            freeze_manifest_path=freeze_path,
            output_dir=tmp_path / "boundary",
            expected_freeze_manifest_hash="0" * 64,
        )


def _write_freeze_manifest(tmp_path):
    freeze_path = tmp_path / "freeze.json"
    freeze_path.write_text(
        json.dumps(
            {
                "freeze_id": "PHASE1A-ARCHIVE-FREEZE-v1",
                "archive_only": True,
                "gate_claim_allowed": False,
                "boundary": "manifest_only_no_strategy_no_portfolio_no_performance_claim",
                "dataset_count": 2,
                "allowed_report_labels": ["archive-only", "not_phase_gate_approval"],
                "forbidden_report_labels": ["live", "OOS performance"],
                "split_policy": {
                    "archive_formation": {
                        "label": PHASE1A_FORMATION_LABEL,
                        "window_start": "2020-01-01",
                        "window_end": "2022-12-31",
                    },
                    "archive_validation": {
                        "label": PHASE1A_VALIDATION_LABEL,
                        "window_start": "2023-01-01",
                        "window_end": "2024-12-31",
                    },
                    "archive_holdout": {
                        "label": PHASE1A_HOLDOUT_LABEL,
                        "window_start": "2025-01-01",
                        "window_end": "2025-12-31",
                    },
                },
                "datasets": [
                    {
                        "symbol": "BTCUSDT",
                        "timeframe": "1d",
                        "calendar_profile": "continuous",
                        "dataset_hash": "btc_dataset_hash",
                        "parquet_path": "/tmp/BTCUSDT.parquet",
                    },
                    {
                        "symbol": "ETHUSDT",
                        "timeframe": "1d",
                        "calendar_profile": "continuous",
                        "dataset_hash": "eth_dataset_hash",
                        "parquet_path": "/tmp/ETHUSDT.parquet",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return freeze_path


def _rule(payload: dict[str, object], split_label: str):
    rules = payload["split_rules"]
    assert isinstance(rules, list)
    for rule in rules:
        assert isinstance(rule, dict)
        if rule["split_label"] == split_label:
            return rule
    raise AssertionError(f"missing rule {split_label}")
