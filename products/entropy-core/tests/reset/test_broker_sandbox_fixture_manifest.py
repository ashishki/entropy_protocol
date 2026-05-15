"""Broker sandbox fixture manifest contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_FIXTURE_MANIFEST.md"
BOUNDARY = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_BOUNDARY.md"


def test_broker_sandbox_fixture_manifest_records_required_fields() -> None:
    text = MANIFEST.read_text(encoding="utf-8")

    assert "Status: BROKER_SANDBOX_FIXTURE_MANIFEST_SANDBOX_ONLY" in text
    for field in (
        "`fixture_id`",
        "`fixture_version`",
        "`sandbox_venue_class`",
        "`order_scenario_class`",
        "`instrument_universe`",
        "`order_message_schema_version`",
        "`execution_report_schema_version`",
        "`content_hash`",
        "`schema_hash`",
        "`risk_policy_hash`",
        "`replay_clock_policy`",
        "`expected_rejection_state`",
        "`expected_audit_event_class`",
    ):
        assert field in text
    for scenario_class in (
        "accepted_sandbox_limit_order",
        "rejected_price_band_order",
        "rejected_size_limit_order",
        "rejected_session_state_order",
        "rejected_missing_risk_approval_order",
        "kill_switch_trigger_fixture",
    ):
        assert scenario_class in text
    for binding in (
        "content hash required: true",
        "schema hash required: true",
        "risk policy hash required: true",
        "replay clock policy hash required: true",
        "order scenario class required: true",
        "expected rejection state required: true",
        "fixture mutation allowed: false",
        "unversioned fixture allowed: false",
    ):
        assert binding in text


def test_broker_sandbox_fixture_manifest_rejects_live_effects() -> None:
    text = MANIFEST.read_text(encoding="utf-8")

    for rejected in (
        "production credential reference: rejected",
        "raw secret material: rejected",
        "real account identifier: rejected",
        "live broker endpoint: rejected",
        "live exchange endpoint: rejected",
        "network socket: rejected",
        "live order placement: rejected",
        "live broker/exchange execution: rejected",
        "live capital action: rejected",
        "production label: rejected",
        "capital-ready label: rejected",
        "holdout read: rejected",
        "holdout unlock: rejected",
    ):
        assert rejected in text
    for blocked in (
        "network access during replay: blocked",
        "broker/exchange session during replay: blocked",
        "production credential lookup during replay: blocked",
        "live order path during replay: blocked",
        "live capital path during replay: blocked",
        "external order telemetry during replay: blocked",
        "holdout path during replay: blocked",
    ):
        assert blocked in text


def test_broker_sandbox_fixture_manifest_binds_scope() -> None:
    text = MANIFEST.read_text(encoding="utf-8")

    assert "`docs/protocols/BROKER_SANDBOX_BOUNDARY.md`" in text
    assert BOUNDARY.is_file()
    assert "phase: 12 sandbox-only broker/exchange execution risk audit" in text
    for scope in (
        "sandbox mode required: true",
        "risk-audit boundary required: true",
        "no-capital dry run required: true",
    ):
        assert scope in text
    for false_state in (
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
        "live orders sent: false",
        "sandbox orders emitted from code: false",
        "broker/exchange connection opened: false",
        "production credentials deployed: false",
        "live capital active: false",
    ):
        assert false_state in text
