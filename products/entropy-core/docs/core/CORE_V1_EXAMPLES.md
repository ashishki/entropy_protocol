# Core V1 Examples

Status: Internal examples
Date: 2026-05-14

All examples use synthetic fixtures under `tests/fixtures/artifacts/`.

## Generic Contract Fixture

- Fixture: `tests/fixtures/artifacts/valid_artifact.json`
- Validator: `entropy artifact validate tests/fixtures/artifacts/valid_artifact.json`
- Expected result: success with `entropy-core-artifact/v1`.

## Product Profile Fixtures

- Trader profile fixture: `tests/fixtures/artifacts/profiles/trader_valid.json`
- Signal profile fixture: `tests/fixtures/artifacts/profiles/signal_valid.json`
- Unsafe variants:
  - `tests/fixtures/artifacts/profiles/trader_unsafe_claim.json`
  - `tests/fixtures/artifacts/profiles/signal_unsafe_claim.json`

Use `--profile trader-risk-audit` or `--profile signal-analytics-sandbox` for
profile-specific validation overlays.

## Research Fixture

- Fixture: `tests/fixtures/artifacts/research/valid_research_artifact.json`
- Schema: `entropy-research-artifact/v1`
- Conversion path: `ResearchArtifact.to_artifact_contract()`
- Base validator target: generated local JSON under `/tmp/`.

Unsafe research variants:

- `tests/fixtures/artifacts/research/unsafe_holdout_claim.json`
- `tests/fixtures/artifacts/research/unsafe_oos_performance.json`

## CAF Fixture

- Fixture: `tests/fixtures/artifacts/caf/valid_allocation_decision.json`
- Schema: `entropy-caf-artifact/v1`
- Conversion path: `AllocationDecisionArtifact.to_artifact_contract()`
- Base validator target: generated local JSON under `/tmp/`.

Unsafe CAF variants:

- `tests/fixtures/artifacts/caf/unsafe_live_allocation.json`
- `tests/fixtures/artifacts/caf/unsafe_investment_advice.json`
- `tests/fixtures/artifacts/caf/unsafe_capital_ready.json`

## Audit Bundle Example Shape

Use `AuditBundle` with:

- `lineage_graph` from `build_artifact_lineage_graph()`;
- `evidence_packet_refs` pointing to generated evidence JSON;
- `validation_events` and `governance_events` as event refs;
- `reviewer_notes` as internal review refs;
- `content_hashes` with `sha256:` prefixes;
- `claim_boundary` labels that explicitly negate certification, enterprise SLA,
  investment-advice compliance, and production readiness.

## Boundary Examples

Allowed examples are synthetic, local, and internal. Examples must not contain:

- raw customer payloads;
- credentials or tokens;
- production account identifiers;
- live broker/exchange order refs;
- holdout data paths;
- public SDK or hosted service claims;
- SOC 2, regulatory certification, investment-advice compliance, or enterprise
  SLA claims.
