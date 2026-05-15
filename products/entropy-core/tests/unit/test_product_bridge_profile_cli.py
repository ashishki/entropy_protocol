"""Unit tests for profile-aware artifact CLI validation."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli

runner = CliRunner()
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "artifacts"


def test_trader_profile_validation_applies_boundaries(tmp_path: Path) -> None:
    artifact_path = write_artifact(
        tmp_path,
        "trader.json",
        extra_boundaries=(
            "not_order_blocking",
            "not_live_trading",
            "not_broker_exchange_execution",
            "not_core_phase_gate_approval",
        ),
    )

    result = runner.invoke(
        cli.app,
        ["artifact", "validate", str(artifact_path), "--profile", "trader-risk-audit"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert "profile" not in payload["artifact"]

    missing_result = runner.invoke(
        cli.app,
        ["artifact", "validate", str(FIXTURES / "valid_artifact.json"), "--profile", "trader-risk-audit"],
    )
    assert missing_result.exit_code == 1
    missing_payload = json.loads(missing_result.stdout)
    assert missing_payload["errors"][0]["code"] == "artifact.profile_violation"
    assert "missing required no-claim boundaries" in missing_payload["errors"][0]["message"]


def test_signal_profile_validation_applies_boundaries(tmp_path: Path) -> None:
    artifact_path = write_artifact(
        tmp_path,
        "signal.json",
        extra_boundaries=(
            "not_trading_advice",
            "not_investment_recommendation",
            "not_future_performance_prediction",
            "not_automated_signal_execution",
            "not_core_phase_gate_approval",
        ),
    )

    result = runner.invoke(
        cli.app,
        ["artifact", "validate", str(artifact_path), "--profile", "signal-analytics-sandbox"],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["ok"] is True

    unsafe_path = write_artifact(
        tmp_path,
        "signal-unsafe.json",
        extra_boundaries=(
            "not_trading_advice",
            "not_investment_recommendation",
            "not_future_performance_prediction",
            "not_automated_signal_execution",
            "not_core_phase_gate_approval",
            "automated_signal_execution",
        ),
    )
    unsafe_result = runner.invoke(
        cli.app,
        ["artifact", "validate", str(unsafe_path), "--profile", "signal-analytics-sandbox"],
    )

    assert unsafe_result.exit_code == 1
    unsafe_payload = json.loads(unsafe_result.stdout)
    assert unsafe_payload["errors"][0]["code"] == "artifact.profile_violation"
    assert "forbidden no-claim labels" in unsafe_payload["errors"][0]["message"]


def test_profile_validation_does_not_absorb_product_schema(tmp_path: Path) -> None:
    artifact_path = write_artifact(
        tmp_path,
        "trader-extra-field.json",
        extra_boundaries=(
            "not_order_blocking",
            "not_live_trading",
            "not_broker_exchange_execution",
            "not_core_phase_gate_approval",
        ),
        extra_fields={"trader_risk_audit_details": {"product_owned": True}},
    )

    result = runner.invoke(
        cli.app,
        ["artifact", "validate", str(artifact_path), "--profile", "trader-risk-audit"],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert {
        "path": "$.trader_risk_audit_details",
        "code": "artifact.extra_field",
        "severity": "P1",
        "message": "Unknown artifact field is not allowed.",
    } in payload["errors"]


def write_artifact(
    tmp_path: Path,
    filename: str,
    *,
    extra_boundaries: tuple[str, ...],
    extra_fields: dict[str, object] | None = None,
) -> Path:
    payload = json.loads((FIXTURES / "valid_artifact.json").read_text(encoding="utf-8"))
    payload["no_claim_boundary"] = [*payload["no_claim_boundary"], *extra_boundaries]
    payload.update(extra_fields or {})
    artifact_path = tmp_path / filename
    artifact_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return artifact_path
