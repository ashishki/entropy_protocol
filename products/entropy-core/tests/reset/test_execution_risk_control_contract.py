"""Execution risk control contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "protocols" / "EXECUTION_RISK_CONTROL_CONTRACT.md"
MANIFEST = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_FIXTURE_MANIFEST.md"


def test_execution_risk_contract_records_controls() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "Status: EXECUTION_RISK_CONTROL_CONTRACT_SANDBOX_ONLY" in text
    assert "`docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md`" in text
    assert MANIFEST.is_file()
    for field in (
        "`order_id`",
        "`scenario_id`",
        "`sandbox_venue_class`",
        "`instrument_id`",
        "`side`",
        "`order_type`",
        "`quantity`",
        "`limit_price`",
        "`time_in_force`",
        "`risk_policy_version`",
        "`risk_policy_hash`",
        "`account_fingerprint`",
        "`replay_timestamp_utc`",
    ):
        assert field in text
    for control in (
        "sandbox mode: required",
        "fixture scenario class: required",
        "order message schema validation: required",
        "execution report schema validation: required",
        "instrument allowlist validation: required",
        "side validation: required",
        "order type validation: required",
        "quantity validation: required",
        "price band validation: required",
        "time-in-force validation: required",
        "session state validation: required",
        "duplicate client order id validation: required",
        "missing risk approval rejection: required",
    ):
        assert control in text
    for limit in (
        "max notional per order: enforced",
        "max quantity per order: enforced",
        "max open sandbox orders: enforced",
        "max rejected order burst: enforced",
        "price band basis: deterministic fixture midpoint",
        "session state basis: deterministic fixture clock",
        "risk policy mutation allowed: false",
        "limit override without audit event: rejected",
    ):
        assert limit in text


def test_execution_risk_contract_rejects_live_effects() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for rejected in (
        "live order placement: rejected",
        "live broker/exchange execution: rejected",
        "production credential reference: rejected",
        "raw secret material: rejected",
        "real account identifier: rejected",
        "live capital action: rejected",
        "production label: rejected",
        "capital-ready label: rejected",
        "broker/exchange activation: rejected",
        "holdout read: rejected",
        "holdout unlock: rejected",
    ):
        assert rejected in text
    for false_state in (
        "live orders sent: false",
        "live capital active: false",
        "production credentials deployed: false",
        "broker/exchange connection opened: false",
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
    ):
        assert false_state in text


def test_execution_risk_contract_records_audit_boundaries() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for field in (
        "`risk_decision`",
        "`risk_state`",
        "`rejection_code`",
        "`rejection_reason`",
        "`triggered_control_id`",
        "`policy_hash_at_decision`",
        "`fixture_hash_at_decision`",
        "`deterministic_decision_hash`",
    ):
        assert field in text
    for decision in (
        "sandbox_accept",
        "reject_price_band",
        "reject_size_limit",
        "reject_session_state",
        "reject_missing_risk_approval",
        "reject_duplicate_order_id",
        "reject_kill_switch_active",
    ):
        assert decision in text
    for boundary in (
        "audit mode: local deterministic sandbox audit",
        "audit event required for every decision: true",
        "decision hash required: true",
        "fixture hash required: true",
        "policy hash required: true",
        "replay timestamp required: true",
        "account fingerprint only: true",
        "raw account identifier allowed: false",
        "external order telemetry emitted: false",
        "sandbox orders emitted from code: false",
        "no-capital mode required: true",
    ):
        assert boundary in text
