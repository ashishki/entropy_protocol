# Core V1 Surface Freeze

Status: Internal surface freeze
Date: 2026-05-14
Scope: Entropy Core V1 internal product kernel

## Stable Internal CLI Commands

The Core V1 CLI surface is local-operator only:

- `entropy version`
- `entropy health`
- `entropy artifact validate <path> [--profile generic|trader-risk-audit|signal-analytics-sandbox]`
- `entropy artifact register <path> [--profile generic|trader-risk-audit|signal-analytics-sandbox]`
- `entropy artifact show <artifact_id>`
- `entropy artifact list`
- `entropy artifact history <artifact_id>`
- `entropy artifact compare <artifact_id> --against <path>`
- `entropy artifact reproduce <artifact_id>`
- `entropy evidence build <artifact_id>`
- `entropy evidence inspect <path>`
- `entropy governance transition <artifact_id> <next_state> [--approval-event-ref <ref>] [--reason <text>]`
- `entropy governance history <artifact_id>`

`artifact reproduce` remains a fail-closed command: direct rerun execution is
not approved in Core V1.

## Stable Schema Versions

- Base artifact contract: `entropy-core-artifact/v1`
- Artifact registry: `entropy-artifact-registry/v1`
- Reproducibility manifest: `entropy-reproducibility-manifest/v1`
- Artifact evidence packet: `entropy-artifact-evidence/v1`
- Research artifact: `entropy-research-artifact/v1`
- CAF artifact: `entropy-caf-artifact/v1`
- Audit bundle: `entropy-audit-bundle/v1`
- Governance transition event: `entropy-artifact-governance-event/v1`

## Stable State Vocabularies

Artifact governance states:

- `draft`
- `validated_internal`
- `blocked`
- `needs_manual_review`
- `approved_for_controlled_external_pilot`
- `rejected`
- `superseded`

Registry validation statuses:

- `validated`
- `rejected`

Registry governance states:

- `registered_internal`
- `needs_manual_review`
- `blocked`
- `superseded`

Reproducibility statuses:

- `exact`
- `materially_equivalent`
- `partial`
- `declared_non_reproducible`
- `failed`

Evidence approval states:

- `not_approved`
- `internal_only`

## Storage Boundaries

- Artifact registry records and event history are local append-only JSONL files
  by default.
- Durable metadata tables are available through explicit PostgreSQL migrations;
  application code does not run privileged DDL.
- Filesystem artifact storage is content-addressed and local.
- Object-store behavior is represented as an internal protocol boundary only;
  Core V1 does not add an external object-store runtime dependency.
- Core V1 remains single-tenant and local-operator oriented.

## Internal API Boundary

The internal Python facade and in-process job registry are stable for local
library use by approved Core callers. They are not a public SDK, HTTP API,
hosted service, SaaS surface, or external SLA.

No route, auth, SSO, RBAC, tenant isolation, public package contract, or hosted
deployment contract is frozen by this document.

## Unsupported Surfaces

Core V1 does not approve:

- holdout read or unlock;
- OOS/performance conclusions without a future explicit gate;
- live feeds by default;
- live order placement or order blocking;
- broker/exchange execution;
- live capital;
- production credentials;
- production or capital-ready labels;
- investment advice;
- public SDK;
- hosted Core service;
- multi-tenant SaaS;
- SOC 2, regulatory certification, investment-advice compliance, enterprise
  readiness, or enterprise SLA claims;
- Rust, Go, Java, native extensions, FFI, or a second runtime service.

## Migration Notes

No schema-version migration is required before the internal V1 checkpoint for
the schemas listed above. Operators using PostgreSQL metadata must apply
`migrations/versions/0002_artifact_metadata_tables.py` before relying on the
metadata repository.

Future schema/version migrations must preserve deterministic validation,
append-only history, no-claim boundaries, and explicit unsupported-surface
labels.
