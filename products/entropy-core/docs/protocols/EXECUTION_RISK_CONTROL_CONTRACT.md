# Execution Risk Control Contract

Status: EXECUTION_RISK_CONTROL_CONTRACT_SANDBOX_ONLY
Task: T53 Execution Risk Control Contract
Last updated: 2026-05-09

This contract defines sandbox-only execution risk controls for Phase 12 broker
sandbox audit work. It validates checked-in fixture scenarios, records
deterministic risk decisions, and rejects unsafe execution surfaces. It does
not place live orders, connect to broker or exchange systems, load production
credentials, activate live capital, create production labels, or alter holdout
status.

## Required Control Inputs

- fixture manifest: `docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md`
- `order_id`
- `scenario_id`
- `sandbox_venue_class`
- `instrument_id`
- `side`
- `order_type`
- `quantity`
- `limit_price`
- `time_in_force`
- `risk_policy_version`
- `risk_policy_hash`
- `account_fingerprint`
- `replay_timestamp_utc`

## Sandbox Order Validation Controls

- sandbox mode: required
- fixture scenario class: required
- order message schema validation: required
- execution report schema validation: required
- instrument allowlist validation: required
- side validation: required
- order type validation: required
- quantity validation: required
- price band validation: required
- time-in-force validation: required
- session state validation: required
- duplicate client order id validation: required
- missing risk approval rejection: required

## Execution Risk Limits

- max notional per order: enforced
- max quantity per order: enforced
- max open sandbox orders: enforced
- max rejected order burst: enforced
- price band basis: deterministic fixture midpoint
- session state basis: deterministic fixture clock
- risk policy mutation allowed: false
- limit override without audit event: rejected

## Rejection And Risk State Fields

- `risk_decision`
- `risk_state`
- `rejection_code`
- `rejection_reason`
- `triggered_control_id`
- `policy_hash_at_decision`
- `fixture_hash_at_decision`
- `deterministic_decision_hash`

Valid risk decisions:

- sandbox_accept
- reject_price_band
- reject_size_limit
- reject_session_state
- reject_missing_risk_approval
- reject_duplicate_order_id
- reject_kill_switch_active

## Deterministic Audit Boundary

- audit mode: local deterministic sandbox audit
- audit event required for every decision: true
- decision hash required: true
- fixture hash required: true
- policy hash required: true
- replay timestamp required: true
- account fingerprint only: true
- raw account identifier allowed: false
- external order telemetry emitted: false
- sandbox orders emitted from code: false

## Rejected Live Effects

- live order placement: rejected
- live broker/exchange execution: rejected
- production credential reference: rejected
- raw secret material: rejected
- real account identifier: rejected
- live capital action: rejected
- production label: rejected
- capital-ready label: rejected
- broker/exchange activation: rejected
- holdout read: rejected
- holdout unlock: rejected

## No-Capital Boundary

- phase: 12 sandbox-only broker/exchange execution risk audit
- no-capital mode required: true
- live orders sent: false
- live capital active: false
- production credentials deployed: false
- broker/exchange connection opened: false
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false
