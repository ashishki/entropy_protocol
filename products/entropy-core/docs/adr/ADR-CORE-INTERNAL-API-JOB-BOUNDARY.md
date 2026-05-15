# ADR: Core Internal API And Job Boundary

Status: Accepted
Date: 2026-05-14

## Context

Entropy Core now has stable local operations for artifact validation, registry,
reproducibility comparison, evidence packets, governance transitions, metadata
storage, and local artifact storage. Phase 24 must decide whether these should
remain CLI/local-library operations or expand into an internal service/job
runtime.

Security boundaries in `docs/ARCHITECTURE.md` state that v1 has no HTTP API,
external auth provider, or multi-tenant storage. `docs/AI_LOOP_OPERATING_MODEL.md`
also blocks public SDK and hosted Core service scope unless explicitly approved.

## Options Considered

| Option | Summary | Benefit | Cost / Risk | Decision |
|---|---|---|---|---|
| CLI-only | Keep only command-line workflows. | Lowest surface area. | Repeats orchestration code for product-local callers. | Rejected as too narrow for internal reuse. |
| Internal Python API | Add typed in-process facade over stable Core operations. | Reduces duplicate local orchestration while preserving local-only scope. | Requires careful boundary tests to avoid public SDK claims. | Accepted. |
| FastAPI internal service | Add HTTP service for Core operations. | Could support future process isolation. | Opens auth, routing, deployment, and service lifecycle questions. | Deferred. |
| Background job runtime | Add worker queue/runtime for async operations. | Could support long-running validation later. | Adds runtime dependency and worker operational surface. | Deferred; model in-process jobs only. |

## Decision

Accepted for this roadmap segment:

- build an internal Python API facade in Core;
- build an idempotent in-process job model for local validation/evidence
  operations.

Deferred or rejected for this roadmap segment:

- no FastAPI or HTTP service;
- no public SDK;
- no hosted Core service;
- no external auth provider;
- no tenant model;
- no external SLA;
- no Celery, Redis, Temporal, Kafka, or service-container worker runtime.

## Boundary Requirements

- The facade is an internal library surface, not a public SDK.
- Jobs execute in-process unless a future ADR explicitly approves a worker
  runtime.
- Product workspaces may call approved Core primitives, but Core does not own
  product runtime behavior or report generation.
- No holdout/OOS/live/broker/production/capital-ready scope is opened by this
  ADR.
- No public API, hosted service, auth, tenant, or external SLA claim is created.

## Consequences

- T108 should implement `src/entropy/artifacts/api.py` as a typed internal
  facade.
- T109 should implement `src/entropy/artifacts/jobs.py` as an idempotent
  in-process job model only.
- Any future HTTP service, hosted worker, public SDK, external auth, or
  multi-tenant behavior requires a new ADR and human approval before code.

## Rollback Plan

If the internal facade or job model expands scope, remove those modules and keep
CLI/local module calls as the only supported operator path. Existing artifact
schemas, validation, registry, evidence, governance, and storage modules remain
valid without the facade.

## Related Documents

- `docs/ARCHITECTURE.md#security-boundaries`
- `docs/AI_LOOP_OPERATING_MODEL.md`
- `docs/tasks.md` Phase 24, T107-T110
- `docs/audit/STORAGE_AND_AUDIT_BACKEND_REVIEW.md`
