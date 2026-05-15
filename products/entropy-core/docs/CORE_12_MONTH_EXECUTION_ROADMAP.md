# Entropy Core 12 Month Execution Roadmap

Status: Active roadmap
Date: 2026-05-12
Scope: Entropy Core only

This roadmap treats Entropy Core as the long-lived protocol kernel, not as a
short-cycle commercial mini-product. Trader Risk Audit and Signal Analytics
Sandbox remain separate products. Core may use their artifacts as external
shape examples, but must not absorb product-specific report logic.

## Target State

By the end of this roadmap, Core should be an executable trust layer that can:

- validate report, research, and allocation artifacts against versioned
  contracts;
- register artifacts and corrections through append-only metadata;
- rerun or classify reproducibility checks;
- emit machine-readable evidence packets;
- enforce no-claim, holdout, live-capital, production, and delivery boundaries;
- support product bridge profiles without becoming the product runtime;
- represent Capital Allocation Framework decision artifacts without executing
  capital movement.

Core v1 is complete when it can validate, register, reproduce, govern, and
explain artifacts that support research/product/allocation decisions without
making unsupported performance, advice, live-capital, or production claims.

## Roadmap Summary

| Phase | Name | Primary output |
|---:|---|---|
| 16 | Executable Artifact Validation | `entropy artifact validate` and `ArtifactContractV1` |
| 17 | Artifact Registry | Append-only artifact records and CLI read surface |
| 18 | Reproducibility Runner | Rerun/compare statuses and hash-drift reports |
| 19 | Evidence Pipeline | Machine-readable evidence packets |
| 20 | Product Bridge Profiles | Product-shaped validation overlays |
| 21 | Governance State Machine | Deterministic artifact state transitions |
| 22 | Research Evaluation Integration | Research/evaluation packets as governed artifacts |
| 23 | Storage And Audit Backend | Postgres metadata and artifact-store abstraction |
| 24 | Internal API And Job Boundary | Optional internal service/job interface |
| 25 | CAF Decision Primitives | Allocation/risk/decision artifact schemas |
| 26 | Enterprise Audit Readiness | Exportable lineage and audit bundles |
| 27 | Core V1 Productization | Stable internal Core product surface |

## Non-Negotiable Boundaries

The roadmap does not approve:

- holdout read or unlock;
- OOS/performance conclusions without explicit future gate;
- live feeds by default;
- broker/exchange execution;
- live capital;
- order placement or order blocking;
- production or capital-ready labels;
- investment advice;
- public SDK;
- hosted Core service;
- multi-tenant SaaS;
- Rust/Go/Java/native extensions or second runtime service.

Those require an explicit human decision, ADR where applicable, CI/toolchain
plan where applicable, and a bounded task contract.

## Stack Policy

Core remains Python-first for this roadmap:

- Python 3.12 for schemas, validators, governance, CLI, batch analytics, and
  evidence generation;
- Pydantic v2 for contract models;
- Typer/Rich for CLI;
- Polars, DuckDB, PyArrow, and Parquet for local analytical artifacts;
- PostgreSQL and Alembic for durable metadata once Phase 23 begins.

Future escalation is allowed only behind stable contracts:

- Rust for proven CPU-bound kernels, parsers, rolling-window logic, or
  simulations;
- Go for proven long-running services, collectors, workers, or operational
  control planes;
- Java only if a future enterprise data platform requires it.

No escalation is allowed without benchmark evidence, ADR, CI/toolchain plan,
rollback plan, and human approval.

## Definition Of Progress

Each phase must leave Core able to validate or explain something it could not
validate or explain before. Documentation is allowed only when it directly
supports executable behavior, task routing, or safety boundaries.

Bad progress:

- more philosophy without code;
- new product strategy text without validators;
- platformization language without repeated validated artifacts;
- stack debates without measured bottlenecks.

Good progress:

- executable schemas;
- CLI commands;
- append-only records;
- deterministic validation results;
- reproducibility classifications;
- evidence packets;
- regression fixtures;
- phase reviews with actual verification.

## Phase Exit Pattern

Every phase exits through the same pattern:

1. all task acceptance criteria are satisfied;
2. relevant tests pass;
3. `git diff --check` passes;
4. an evidence row or review artifact records the result;
5. no P0/P1 finding remains open;
6. the next phase is opened automatically unless a human gate is triggered.

