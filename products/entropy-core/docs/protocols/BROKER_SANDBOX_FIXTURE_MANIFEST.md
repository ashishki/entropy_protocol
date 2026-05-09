# Broker Sandbox Fixture Manifest

Status: BROKER_SANDBOX_FIXTURE_MANIFEST_SANDBOX_ONLY
Task: T52 Broker Sandbox Fixture Manifest
Last updated: 2026-05-09

This manifest defines deterministic sandbox fixture requirements for Phase 12
broker/exchange execution risk tests. It does not connect to live broker or
exchange systems, load production credentials, place live orders, activate live
capital, create production labels, or alter holdout status.

## Required Fixture Fields

- `fixture_id`
- `fixture_version`
- `sandbox_venue_class`
- `order_scenario_class`
- `instrument_universe`
- `order_message_schema_version`
- `execution_report_schema_version`
- `content_hash`
- `schema_hash`
- `risk_policy_hash`
- `replay_clock_policy`
- `expected_rejection_state`
- `expected_audit_event_class`

## Order Scenario Classes

- accepted_sandbox_limit_order
- rejected_price_band_order
- rejected_size_limit_order
- rejected_session_state_order
- rejected_missing_risk_approval_order
- kill_switch_trigger_fixture

Allowed scenario classes must be checked in, deterministic, and reproducible
without broker, exchange, network, credential, or capital access.

## Hash And Schema Binding

- content hash required: true
- schema hash required: true
- risk policy hash required: true
- replay clock policy hash required: true
- order scenario class required: true
- expected rejection state required: true
- fixture mutation allowed: false
- unversioned fixture allowed: false

## Replay Constraints

- replay mode: local sandbox deterministic risk audit
- replay clock: fixed fixture timestamp clock
- network access during replay: blocked
- broker/exchange session during replay: blocked
- production credential lookup during replay: blocked
- live order path during replay: blocked
- live capital path during replay: blocked
- external order telemetry during replay: blocked
- holdout path during replay: blocked

## Rejected Live Effects

- production credential reference: rejected
- raw secret material: rejected
- real account identifier: rejected
- live broker endpoint: rejected
- live exchange endpoint: rejected
- network socket: rejected
- live order placement: rejected
- live broker/exchange execution: rejected
- live capital action: rejected
- production label: rejected
- capital-ready label: rejected
- holdout read: rejected
- holdout unlock: rejected

## Sandbox Scope Binding

- boundary contract: `docs/protocols/BROKER_SANDBOX_BOUNDARY.md`
- phase: 12 sandbox-only broker/exchange execution risk audit
- sandbox mode required: true
- risk-audit boundary required: true
- no-capital dry run required: true
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false
- live orders sent: false
- sandbox orders emitted from code: false
- broker/exchange connection opened: false
- production credentials deployed: false
- live capital active: false
