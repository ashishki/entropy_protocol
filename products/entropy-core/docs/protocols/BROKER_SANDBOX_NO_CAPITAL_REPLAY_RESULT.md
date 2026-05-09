# Broker Sandbox No-Capital Replay Result

Status: BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT_LOCAL_ONLY
Task: T65 Broker Sandbox Replay Evidence Packet
Last updated: 2026-05-09

This result packet records the local replay evidence produced after the
operator approved the broker sandbox no-capital replay extension. The replay
used only in-process SimBroker primitives and local fixture scenarios. It did
not emit sandbox orders from code, place live orders, connect to broker or
exchange systems, load production credentials, activate capital, access holdout
data, or create OOS/performance claims.

## Inputs

- approval event: `docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md`
- replay contract: `docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT.md`
- code primitive: `src/entropy/simbroker/replay.py`
- unit test: `tests/unit/test_simbroker_replay.py`
- approval scope: local_broker_sandbox_no_capital_replay

## Replay Scenario Set

| Scenario | Symbol | Side | Quantity | Proposed Price | Expected Mode |
|---|---:|---:|---:|---:|---|
| accepted-buy-fixture-fill | BTC-USD | BUY | 1.25 | 101.25 | fixture_fill_only |
| constrained-sell-fixture-fill | BTC-USD | SELL | 0.75 | 98.0 | fixture_fill_only |

## Replay Result

- replay_id: broker-sandbox-no-capital-replay-v1
- scenario_count: 2
- replay_hash: 9b3681de22bf73160baadb022cc4b8af289b144449ca421ffa0f6457910c4c7e
- deterministic replay: true
- no_order_emission: true
- no_broker_exchange_connection: true
- no_credential_loading: true
- no_capital_activation: true
- no_holdout_access: true
- product_hypothesis_delta: local_evidence_strengthened_not_confirmed

## Fill Log Summary

| Scenario | Fill Price | Total Cost | Constrained |
|---|---:|---:|---:|
| accepted-buy-fixture-fill | 101.25 | 0.503125 | false |
| constrained-sell-fixture-fill | 99.0 | 0.39849999999999997 | true |

## Interpretation

- product hypothesis confirmation status: not_confirmed
- product hypothesis rejection status: not_rejected
- local evidence status: strengthened_by_no_effect_replay
- production/capital readiness status: not_claimed
- OOS/performance conclusion status: not_claimed

## Blocked Effects

- sandbox order emission from code: false
- live orders sent: false
- broker/exchange connection opened: false
- production credentials loaded: false
- live capital active: false
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false

