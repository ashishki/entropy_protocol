# Broker Sandbox No-Capital Replay Contract

Status: BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT_LOCAL_ONLY
Task: T64 Broker Sandbox No-Capital Replay Primitive
Last updated: 2026-05-09

This contract defines the local replay primitive used after the operator
approved the broker sandbox no-capital replay extension. The primitive runs
only against in-memory local fixture scenarios and Entropy Core SimBroker cost
logic. It does not send sandbox or live orders, open broker/exchange
connections, load production credentials, activate capital, read holdout data,
or create OOS/performance claims.

## Approval Binding

- approval event: `docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md`
- required approval scope: local_broker_sandbox_no_capital_replay
- rejected approval scopes:
  - production_capital_validation
  - broker_exchange_execution
  - live_order_placement
  - holdout_oos_evaluation
  - generated_or_inferred_approval

## Replay Inputs

- scenario model: `SandboxReplayScenario`
- scenario fields:
  - scenario_id
  - signal
  - bar
  - expected_mode: fixture_fill_only
- cost model: `CostModelConfig`
- execution primitive: `run_no_capital_sandbox_replay`

## Deterministic Result Fields

- replay_id
- approval_scope
- scenario_count
- fill_logs
- replay_hash
- no_order_emission
- no_broker_exchange_connection
- no_credential_loading
- no_capital_activation
- no_holdout_access
- product_hypothesis_delta

## Failure Conditions

- missing replay scenarios: reject
- duplicate scenario ids: reject
- approval scope outside local_broker_sandbox_no_capital_replay: reject
- non-positive fill inputs: reject through existing SimBroker validation
- live broker/exchange imports: reject by regression test

## Product Hypothesis Boundary

- allowed evidence delta: local_evidence_strengthened_not_confirmed
- product hypothesis confirmation: not_claimed
- product hypothesis rejection: not_claimed
- production/capital readiness: not_claimed
- OOS/performance conclusion: not_claimed

## Blocked Effects

- external order side effects: blocked
- broker/exchange sockets: blocked
- production credentials: blocked
- live capital: blocked
- holdout access: blocked
- external telemetry: blocked

