# Kill-Switch Audit Log Contract

Status: KILL_SWITCH_AUDIT_LOG_CONTRACT_SANDBOX_ONLY
Task: T54 Kill-Switch Audit Log Contract
Last updated: 2026-05-09

This contract defines sandbox kill-switch audit requirements for Phase 12
broker sandbox execution risk work. It records deterministic trigger, state,
actor, timestamp, and fail-closed evidence fields for checked-in fixture
scenarios only. It does not emit live order telemetry, connect to broker or
exchange systems, load production credentials, activate live capital, or alter
holdout status.

## Required Source Contract

- execution risk control contract: `docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md`

## Required Audit Fields

- `kill_switch_event_id`
- `trigger_id`
- `trigger_source`
- `trigger_reason`
- `previous_risk_state`
- `new_risk_state`
- `actor_type`
- `actor_fingerprint`
- `replay_timestamp_utc`
- `fixture_id`
- `fixture_hash`
- `risk_policy_hash`
- `decision_hash`
- `audit_sequence`
- `append_only_log_hash`

## Trigger Classes

- manual_sandbox_operator_trigger
- deterministic_limit_breach_trigger
- rejected_order_burst_trigger
- fixture_integrity_failure_trigger
- missing_risk_policy_hash_trigger
- audit_log_integrity_failure_trigger

Allowed trigger classes must be deterministic, fixture-bound, and reproducible
without broker, exchange, network, credential, account, capital, or holdout
access.

## Kill-Switch State Contract

- kill switch default state: disabled_before_trigger
- trigger evaluation mode: local deterministic sandbox audit
- state transition on trigger: enabled_fail_closed
- order acceptance after trigger: blocked
- new sandbox order validation after trigger: rejected
- existing sandbox scenario replay after trigger: audit_only
- reset path: human-reviewed local contract only
- automatic reset: rejected

## Fail-Closed Behavior

- fail closed when trigger is malformed: true
- fail closed when fixture hash is stale: true
- fail closed when risk policy hash is missing: true
- fail closed when audit sequence is non-monotonic: true
- fail closed when actor fingerprint is missing: true
- fail closed when decision hash is missing: true
- order/capital activation after fail-closed state: blocked
- live order path after fail-closed state: blocked
- broker/exchange activation after fail-closed state: blocked

## Rejected Sensitive Surfaces

- raw secret material: rejected
- production credential reference: rejected
- raw account identifier: rejected
- live broker endpoint: rejected
- live exchange endpoint: rejected
- external order telemetry payload: rejected
- holdout path: rejected
- holdout read: rejected
- holdout unlock: rejected
- production label: rejected
- capital-ready label: rejected

## Current Boundary State

- phase: 12 sandbox-only broker/exchange execution risk audit
- live orders sent: false
- sandbox orders emitted from code: false
- live capital active: false
- production credentials deployed: false
- broker/exchange connection opened: false
- external order telemetry emitted: false
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false
