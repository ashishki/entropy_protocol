# Live-Feed Adapter Dry-Run Contract

Status: LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT_LOCAL_ONLY
Task: T48 Live-Feed Adapter Dry-Run Contract
Last updated: 2026-05-09

This contract defines local adapter dry-run checks for Phase 11 live-feed
readiness. It exercises checked-in fixture parsing, normalization, clock, and
replay boundaries only. It does not open network sockets, load credentials,
connect to live feeds, place orders, connect to broker/exchange execution,
activate live capital, or create production claims.

## Required Local Checks

- fixture manifest: `docs/protocols/LIVE_FEED_FIXTURE_MANIFEST.md`
- parser input contract: checked-in fixture messages only
- parser output contract: deterministic normalized message objects
- normalization check: schema-bound field normalization
- timestamp check: fixed replay clock only
- replay ordering check: deterministic fixture order
- failure-state check: malformed local fixture handling
- idempotence check: repeated replay produces identical normalized output

## Adapter Dry-Run Boundary

- adapter mode: local dry run
- source data: checked-in deterministic fixtures
- network sockets opened: false
- live feed connection opened: false
- credential loading: blocked
- provider activation: blocked
- order placement: blocked
- broker/exchange execution: blocked
- external telemetry emission: blocked

## Rejected External Paths

- live provider endpoint: rejected
- raw API key: rejected
- credential environment variable: rejected
- network socket: rejected
- websocket stream: rejected
- REST polling: rejected
- order router: rejected
- broker/exchange session: rejected
- live capital action: rejected
- holdout read: rejected
- holdout unlock: rejected

## Claim Boundary

- production readiness: rejected
- capital-ready conclusion: rejected
- OOS/performance conclusion: rejected
- live-feed activation: rejected
- broker/exchange activation: rejected
- orders sent: false
- live capital active: false
- current holdout approval event: absent
