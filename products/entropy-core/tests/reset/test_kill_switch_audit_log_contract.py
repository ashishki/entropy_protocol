"""Kill-switch audit log contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "protocols" / "KILL_SWITCH_AUDIT_LOG_CONTRACT.md"
RISK_CONTRACT = PROJECT_ROOT / "docs" / "protocols" / "EXECUTION_RISK_CONTROL_CONTRACT.md"


def test_kill_switch_contract_records_required_fields() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "Status: KILL_SWITCH_AUDIT_LOG_CONTRACT_SANDBOX_ONLY" in text
    assert "`docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md`" in text
    assert RISK_CONTRACT.is_file()
    for field in (
        "`kill_switch_event_id`",
        "`trigger_id`",
        "`trigger_source`",
        "`trigger_reason`",
        "`previous_risk_state`",
        "`new_risk_state`",
        "`actor_type`",
        "`actor_fingerprint`",
        "`replay_timestamp_utc`",
        "`fixture_id`",
        "`fixture_hash`",
        "`risk_policy_hash`",
        "`decision_hash`",
        "`audit_sequence`",
        "`append_only_log_hash`",
    ):
        assert field in text
    for trigger_class in (
        "manual_sandbox_operator_trigger",
        "deterministic_limit_breach_trigger",
        "rejected_order_burst_trigger",
        "fixture_integrity_failure_trigger",
        "missing_risk_policy_hash_trigger",
        "audit_log_integrity_failure_trigger",
    ):
        assert trigger_class in text


def test_kill_switch_contract_records_fail_closed_behavior() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for state in (
        "kill switch default state: disabled_before_trigger",
        "trigger evaluation mode: local deterministic sandbox audit",
        "state transition on trigger: enabled_fail_closed",
        "order acceptance after trigger: blocked",
        "new sandbox order validation after trigger: rejected",
        "existing sandbox scenario replay after trigger: audit_only",
        "reset path: human-reviewed local contract only",
        "automatic reset: rejected",
    ):
        assert state in text
    for fail_closed in (
        "fail closed when trigger is malformed: true",
        "fail closed when fixture hash is stale: true",
        "fail closed when risk policy hash is missing: true",
        "fail closed when audit sequence is non-monotonic: true",
        "fail closed when actor fingerprint is missing: true",
        "fail closed when decision hash is missing: true",
        "order/capital activation after fail-closed state: blocked",
        "live order path after fail-closed state: blocked",
        "broker/exchange activation after fail-closed state: blocked",
    ):
        assert fail_closed in text
    for false_state in (
        "live orders sent: false",
        "sandbox orders emitted from code: false",
        "live capital active: false",
        "production credentials deployed: false",
        "broker/exchange connection opened: false",
        "external order telemetry emitted: false",
    ):
        assert false_state in text


def test_kill_switch_contract_rejects_sensitive_surfaces() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for rejected in (
        "raw secret material: rejected",
        "production credential reference: rejected",
        "raw account identifier: rejected",
        "live broker endpoint: rejected",
        "live exchange endpoint: rejected",
        "external order telemetry payload: rejected",
        "holdout path: rejected",
        "holdout read: rejected",
        "holdout unlock: rejected",
        "production label: rejected",
        "capital-ready label: rejected",
    ):
        assert rejected in text
    for false_state in (
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
    ):
        assert false_state in text
