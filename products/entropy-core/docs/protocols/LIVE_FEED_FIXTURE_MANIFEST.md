# Live-Feed Fixture Manifest

Status: LIVE_FEED_FIXTURE_MANIFEST_LOCAL_ONLY
Task: T47 Live-Feed Fixture Manifest
Last updated: 2026-05-09

This manifest defines deterministic local market-data fixture requirements for
Phase 11 live-feed dry-run readiness. It does not fetch live market data, load
provider credentials, open network connections, place orders, connect to
broker/exchange execution, activate live capital, or alter holdout status.

## Required Fixture Fields

- `fixture_id`
- `fixture_version`
- `source_class`
- `instrument_universe`
- `time_range_utc`
- `schema_version`
- `content_hash`
- `schema_hash`
- `replay_clock_policy`
- `normalization_policy`
- `failure_fixture_class`

## Source Classes

- checked_in_synthetic_market_data
- checked_in_historical_sample_fixture
- generated_failure_state_fixture

Allowed source classes must be checked in, deterministic, and reproducible
without external provider access.

## Hash And Schema Binding

- content hash required: true
- schema hash required: true
- normalization policy hash required: true
- replay clock policy hash required: true
- fixture mutation allowed: false
- unversioned fixture allowed: false

## Replay Constraints

- replay mode: local deterministic dry run
- replay clock: fixed fixture timestamp clock
- network access during replay: blocked
- live provider lookup during replay: blocked
- order path during replay: blocked
- broker/exchange path during replay: blocked
- external telemetry during replay: blocked

## Rejected Live Effects

- live credential reference: rejected
- raw secret material: rejected
- live network pull: rejected
- live feed connection: rejected
- provider activation: rejected
- order placement: rejected
- broker/exchange execution: rejected
- live capital action: rejected
- production label: rejected
- capital-ready label: rejected
- holdout read: rejected
- holdout unlock: rejected

## Local Scope Binding

- boundary contract: `docs/protocols/LIVE_FEED_DRY_RUN_BOUNDARY.md`
- phase: 11 local-only live-feed dry-run readiness
- holdout path opened: false
- holdout read executed: false
- holdout unlock requested: false
- orders sent: false
- broker/exchange connection opened: false
- live feed connection opened: false
- credentials deployed: false
- live capital active: false
