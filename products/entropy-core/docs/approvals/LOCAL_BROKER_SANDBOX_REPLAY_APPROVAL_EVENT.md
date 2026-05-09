# Local Broker Sandbox Replay Approval Event

Status: LOCAL_BROKER_SANDBOX_REPLAY_APPROVED_NO_EFFECT
Task: T63 Local Broker Sandbox Replay Approval Event
Last updated: 2026-05-09

This event records the operator approval to proceed with the local broker
sandbox no-capital replay extension. It authorizes only deterministic local
fixture replay through Entropy Core SimBroker primitives. It does not authorize
sandbox order emission from code, live orders, broker or exchange connections,
production credential loading, live capital, holdout access, OOS/performance
claims, production labels, or capital-ready labels.

## Approval Source

- operator approval source: explicit_user_message_2026-05-09
- operator decision text summary: "I authorize, proceed"
- approved scope: local_broker_sandbox_no_capital_replay
- maximum allowed effect: local_no_effect_only
- approval expiry: same-session-only
- revocation mode: operator message or follow-up patch

## Allowed Actions

- create local replay contract docs
- run deterministic in-process SimBroker replay over local fixture scenarios
- compute replay hash from local inputs and fill logs
- record replay result packet
- update state docs, task graph, evidence index, and tests

## Blocked Actions

- sandbox order emission from code: blocked
- live order placement: blocked
- live broker/exchange execution: blocked
- broker/exchange network connection: blocked
- production credential loading: blocked
- live capital action: blocked
- holdout read: blocked
- holdout unlock: blocked
- OOS/performance conclusion: blocked
- production label: blocked
- capital-ready label: blocked

## Evidence Boundary

- product hypothesis confirmation status before replay: not_confirmed
- product hypothesis rejection status before replay: not_rejected
- permitted evidence delta: local_evidence_strengthened_not_confirmed
- restricted validation execution: not_approved
- external side effect execution: not_approved

