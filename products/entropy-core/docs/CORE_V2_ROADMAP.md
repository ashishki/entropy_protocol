# Entropy Core V2 Roadmap

Status: Active bounded roadmap
Date: 2026-05-29
Decision: `D-CORE-V2-001`
Scope: Entropy Core internal kernel only

Core V2 starts from the Core V1 internal product kernel. The V2 roadmap keeps
Core local, deterministic, Python-first, and human-gated unless a later human
decision and ADR explicitly change those boundaries.

## V2 Direction

Core V2 should make the internal artifact trust layer easier to evolve safely:

- define schema evolution and compatibility rules before breaking schema
  changes;
- add deterministic compatibility checks for versioned artifacts;
- strengthen evidence and governance records around migrations;
- improve local operator visibility without creating a hosted service;
- keep product bridges narrow and Core-owned only at the artifact contract
  boundary.

## Phase Plan

| Phase | Name | Tasks | Delivery | Gate criteria |
|-------|------|-------|----------|---------------|
| 28 | Schema Evolution Foundations | T123-T126 | V2 roadmap activation, schema evolution policy, compatibility primitives, and phase review. | Version policy and compatibility checks exist without changing public/service/live boundaries. |
| 29 | Evidence Query Hardening | T127-T130 | Local evidence lookup and packet inspection improvements. | Operators can inspect local evidence deterministically without runtime RAG or hosted search. |
| 30 | Product Bridge Adoption Readiness | T131-T134 | More precise product-profile adoption checks and synthetic fixtures. | Core improves product-shaped validation without editing product workspaces or owning product reports. |
| 31 | V2 Internal Kernel Review | T135-T138 | Review V2 foundations and decide whether any further scope needs human approval. | No P0/P1 findings remain and restricted surfaces stay blocked. |

Phase 31 is opened by T134 after completing Phases 28-30. Later phase task
contracts remain directional and must be written before execution.

## Phase 28 Scope

Allowed:

- documentation and tests for schema evolution policy;
- deterministic Python compatibility helpers;
- synthetic fixtures for compatible and incompatible artifact versions;
- local CLI/library behavior that only validates or reports compatibility;
- evidence index and audit updates for local proof.

Blocked:

- holdout read or unlock;
- OOS/performance conclusions;
- live feeds by default;
- live broker/exchange execution;
- order placement or order blocking;
- live capital;
- production credentials;
- production or capital-ready labels;
- investment advice;
- public SDK;
- hosted service, SaaS, auth, SSO, RBAC, or tenant isolation;
- external compliance certification or enterprise SLA claims;
- Rust, Go, Java, native extensions, FFI, or a second runtime service.

## First Implementable Task

T124 is the first implementable Core V2 task. It defines the schema evolution
policy before any compatibility code or migration behavior changes.

T124 must leave a written policy and test coverage that state:

- version taxonomy and compatibility categories;
- required fields for future migration records;
- append-only and evidence binding expectations;
- blocked surfaces that schema evolution cannot approve;
- validation commands used to prove the policy is in place.

## Auto-Continue Rule

The loop may continue through Phase 28 while tasks stay inside the allowed
scope above. Any task that proposes a service boundary, external provider,
runtime/language escalation, holdout/OOS expansion, live execution, public SDK,
production credentials, or external compliance claim must stop for a human
decision and any required ADR before implementation.
