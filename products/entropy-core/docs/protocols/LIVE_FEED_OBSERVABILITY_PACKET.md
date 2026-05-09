# Live-Feed Observability Packet

Status: LIVE_FEED_OBSERVABILITY_PACKET_LOCAL_ONLY
Task: T49 Live-Feed Observability Packet
Last updated: 2026-05-09

This packet defines local observability evidence for Phase 11 live-feed dry-run
readiness. It covers local logs, counters, and failure states only. It does not
emit live telemetry, expose credentials, place orders, activate capital, or
read holdout data.

## Required Observability Fields

- `dry_run_id`
- `fixture_id`
- `fixture_content_hash`
- `adapter_contract`
- `parser_message_count`
- `normalized_message_count`
- `parse_failure_count`
- `normalization_failure_count`
- `clock_skew_failure_count`
- `replay_order_failure_count`
- `idempotence_failure_count`
- `dropped_message_count`
- `redaction_policy_hash`
- `timestamp_utc`

## Failure Counters

- parse failures counted: true
- normalization failures counted: true
- clock skew failures counted: true
- replay order failures counted: true
- idempotence failures counted: true
- dropped messages counted: true
- external effect attempts counted: true

## Sensitive And External Effect Boundary

- credential values logged: false
- raw secrets logged: false
- raw API keys logged: false
- provider tokens logged: false
- raw holdout path logged: false
- holdout data logged: false
- orders emitted: false
- capital action emitted: false
- broker/exchange telemetry emitted: false
- live feed telemetry emitted: false
- external telemetry emission: blocked

## Local Evidence Binding

- adapter contract: `docs/protocols/LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md`
- observability mode: local dry run
- log destination: local artifact only
- metrics destination: local artifact only
- source data: checked-in deterministic fixtures
- network sockets opened: false
- live feed connection opened: false
- orders sent: false
- live capital active: false
- holdout read executed: false

## Readiness Limitations

- live-feed readiness: local dry-run only
- production readiness: rejected
- capital-ready conclusion: rejected
- broker/exchange readiness: rejected
- OOS/performance conclusion: rejected
- credentialed deployment readiness: rejected
- holdout access: rejected
