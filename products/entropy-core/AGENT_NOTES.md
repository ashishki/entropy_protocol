# Agent Notes - Entropy Core

Date: 2026-05-31

This file keeps only restart-relevant notes. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`, and
`docs/tasks.md`.

## Active State

- Phase: 31 V2 Internal Kernel Review
- Active task: none - human gate required for next bounded Core V2 phase
- Baseline: `625 passed, 20 skipped`
- Primary roadmap: `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
- AI loop rules: `docs/AI_LOOP_OPERATING_MODEL.md`
- Phase 15 status: complete through T74; Core remains hidden/internal
- Phase 16 status: complete through T78
- Phase 17 status: complete through T82
- Phase 18 status: complete through T86
- Phase 19 status: complete through T90
- Phase 20 status: complete through T94
- Phase 21 status: complete through T98
- Phase 22 status: complete through T102
- Phase 23 status: complete through T106
- Phase 24 status: complete through T110
- Phase 25 status: complete through T114
- Phase 26 status: complete through T118
- Phase 27 status: complete through T122
- Phase 28 status: complete through T126
- Phase 29 status: complete through T130
- Phase 30 status: complete through T134
- Phase 31 status: complete through T138

## Current Decision

Core is the long-lived internal protocol kernel. Trader Risk Audit and Signal
Analytics Sandbox remain separate products. Core may validate product-shaped
artifacts but must not absorb product report logic.

T75-T118 added executable artifact validation, local append-only registry,
compare-only reproducibility classification, evidence packets, local evidence
CLI, evidence-index automation, product bridge profiles, profile-aware CLI
validation, synthetic profile fixtures, artifact governance state mechanics,
local governance transition CLI, approval-event binding, research artifact
schemas/adapters/fixtures, storage/audit backend foundations, internal API/job
boundary, CAF artifact vocabulary, allocation decision primitives, synthetic
CAF fixtures, audit bundle schemas, lineage graph builder, data classification,
reviewer-role metadata, Phase 26 review, Core V1 surface freeze, runbook,
examples, docs alignment, and Core V1 productization review. On 2026-05-29 the
operator approved starting Core V2 and instructed the loop to select T123 as
the next task before continuing. T123 defined `docs/CORE_V2_ROADMAP.md`; T124
defined `docs/core/SCHEMA_EVOLUTION_POLICY.md`; T125 added library-only schema
compatibility primitives; T126 reviewed Phase 28; T127-T130 completed local
evidence query hardening; T131 defined product bridge adoption policy; T132
added Core-side product bridge readiness checks; T133 added synthetic adoption
fixtures; T134 reviewed Phase 30 and opened bounded Phase 31; T135 inventoried
Core V2 foundations; T136 added restricted-surface regression checks; T137
summarized V2 evidence coverage and gaps; T138 reviewed Phase 31 and stopped
automatic Core V2 expansion at a human gate.

## Deferred

- T66-T68 local replay continuation;
- live/broker/exchange execution;
- holdout/OOS expansion;
- public Core productization.
- any human-gated item listed in `docs/AI_LOOP_OPERATING_MODEL.md`.
- external compliance certification, enterprise SLA, auth/RBAC, SSO, hosted
  service, or tenant isolation.
- Product workspace edits, product report ownership, external delivery approval,
  public SDK, hosted service, runtime RAG, live, holdout, compliance, production
  credential, or capital scope in Phase 31.

## Guardrails

- Holdout remains locked.
- Live capital and broker/exchange execution are not approved.
- Production credentials are not approved.
- OOS/performance claims are not approved.

## Key Links

- `docs/CODEX_PROMPT.md`
- `docs/tasks.md`
- `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
- `docs/AI_LOOP_OPERATING_MODEL.md`
- `docs/audit/ARTIFACT_SUPPORT_REVIEW.md`
- `docs/audit/EXECUTABLE_ARTIFACT_VALIDATION_REVIEW.md`
- `docs/audit/ARTIFACT_REGISTRY_REVIEW.md`
- `docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md`
- `docs/audit/EVIDENCE_PIPELINE_REVIEW.md`
- `docs/audit/PRODUCT_BRIDGE_PROFILE_REVIEW.md`
- `docs/audit/ARTIFACT_GOVERNANCE_STATE_MACHINE_REVIEW.md`
- `docs/audit/RESEARCH_ARTIFACT_INTEGRATION_REVIEW.md`
- `docs/audit/STORAGE_AND_AUDIT_BACKEND_REVIEW.md`
- `docs/audit/INTERNAL_API_JOB_BOUNDARY_REVIEW.md`
- `docs/audit/CAF_DECISION_PRIMITIVES_REVIEW.md`
- `docs/audit/ENTERPRISE_AUDIT_READINESS_REVIEW.md`
- `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
