"""Sandbox execution no-capital dry-run tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DRY_RUN = PROJECT_ROOT / "docs" / "protocols" / "SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md"


def test_sandbox_dry_run_assembles_artifacts() -> None:
    text = DRY_RUN.read_text(encoding="utf-8")

    assert "Status: SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN_LOCAL_ONLY" in text
    for artifact in (
        "`docs/protocols/BROKER_SANDBOX_BOUNDARY.md`",
        "`docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md`",
        "`docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md`",
        "`docs/protocols/KILL_SWITCH_AUDIT_LOG_CONTRACT.md`",
    ):
        assert artifact in text
        assert (PROJECT_ROOT / artifact.strip("`")).is_file()
    for check in (
        "dry run mode: local no-capital assembly",
        "artifact existence check: required",
        "artifact status check: sandbox-only statuses required",
        "fixture hash binding check: required",
        "risk policy hash binding check: required",
        "kill-switch fail-closed check: required",
        "deterministic replay clock check: required",
        "append-only audit hash check: required",
        "no-capital boundary check: required",
        "no-holdout boundary check: required",
    ):
        assert check in text
    for scenario in (
        "accepted_sandbox_limit_order: reviewed_from_fixture_only",
        "rejected_price_band_order: reviewed_from_fixture_only",
        "rejected_size_limit_order: reviewed_from_fixture_only",
        "rejected_session_state_order: reviewed_from_fixture_only",
        "rejected_missing_risk_approval_order: reviewed_from_fixture_only",
        "kill_switch_trigger_fixture: reviewed_from_fixture_only",
    ):
        assert scenario in text


def test_sandbox_dry_run_rejects_live_effects() -> None:
    text = DRY_RUN.read_text(encoding="utf-8")

    for rejected in (
        "sandbox order emission from code: rejected",
        "live order placement: rejected",
        "live broker/exchange execution: rejected",
        "broker/exchange connection: rejected",
        "production credential reference: rejected",
        "raw secret material: rejected",
        "real account identifier: rejected",
        "live capital action: rejected",
        "production readiness: rejected",
        "production label: rejected",
        "capital-ready label: rejected",
        "external order telemetry: rejected",
        "holdout read: rejected",
        "holdout unlock: rejected",
    ):
        assert rejected in text
    for false_state in (
        "sandbox orders emitted from code: false",
        "live orders sent: false",
        "broker/exchange connection opened: false",
        "production credentials deployed: false",
        "live capital active: false",
        "external order telemetry emitted: false",
    ):
        assert false_state in text


def test_sandbox_dry_run_records_limitations() -> None:
    text = DRY_RUN.read_text(encoding="utf-8")

    for result in (
        "assembly result: complete_local_no_capital_packet",
        "execution result: not_executed_no_orders_sent",
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
    ):
        assert result in text
    for limitation in (
        "no capital-ready conclusion: true",
        "no production readiness conclusion: true",
        "no live execution approval: true",
        "no broker/exchange activation approval: true",
        "no holdout approval event: true",
        "phase 13 remains planned direction only: true",
    ):
        assert limitation in text
