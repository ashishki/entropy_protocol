# Implementation Journal - Entropy Core

Version: 1.0
Last updated: 2026-05-29
Status: append-only

This file records handoff context. It is not authority.

## Journal Entry Template

```markdown
### YYYY-MM-DD - TNN - Short Title

- Scope: files, directories, or task ids
- Why this work happened: reason or trigger
- Decisions applied: Decision Log or ADR refs, or "none"
- Evidence collected: tests, evals, review reports, or manual checks
- Follow-ups: next task, open risk, or "none"
- Notes for next agent: only context worth carrying forward
```

## Entries

### 2026-05-29 - T123 Selected - Core V2 Roadmap Activation

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: operator approved starting Core V2 and requested that T123 be explicitly selected as the next task before the loop continues
- Decisions applied: `docs/DECISION_LOG.md#D-CORE-V2-001`; `docs/audit/CORE_V1_PRODUCTIZATION_REVIEW.md`
- Evidence collected: manual state-doc update; validation pending T123 execution
- Follow-ups: execute T123 Core V2 Roadmap Activation
- Notes for next agent: T123 is active but not complete. Do not open T124+ implementation tasks until T123 defines the bounded Core V2 roadmap contract. Core V2 approval does not approve public SaaS, public SDK, hosted service, external compliance certification, holdout access, live feeds by default, broker/exchange execution, production credentials, live capital, or unsupported OOS/performance claims.

### 2026-05-29 - T123 - Core V2 Roadmap Activation

- Scope: `docs/CORE_V2_ROADMAP.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: complete the selected Core V2 activation task by defining the bounded roadmap contract and first implementable task
- Decisions applied: `docs/DECISION_LOG.md#D-CORE-V2-001`; `docs/audit/CORE_V1_PRODUCTIZATION_REVIEW.md`; `docs/core/CORE_V1_SURFACE_FREEZE.md`
- Evidence collected: manual docs review pending final validation; `git diff --check` pending final validation
- Follow-ups: execute T124 Schema Evolution Policy Contract
- Notes for next agent: Phase 28 is limited to schema evolution foundations. T124 must define policy before T125 adds compatibility primitives. Public SDK, hosted service, external compliance, holdout, live, broker/exchange, production credential, capital, and unsupported OOS/performance surfaces remain blocked.

### 2026-05-29 - T124 - Schema Evolution Policy Contract

- Scope: `docs/core/SCHEMA_EVOLUTION_POLICY.md`, `tests/reset/test_core_v2_schema_evolution_policy.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: define Core V2 schema evolution policy before compatibility code or migration behavior changes
- Decisions applied: `docs/DECISION_LOG.md#D-CORE-V2-001`; `docs/CORE_V2_ROADMAP.md`; `docs/core/CORE_V1_SURFACE_FREEZE.md`; `docs/IMPLEMENTATION_CONTRACT.md#registry-append-only`; `docs/IMPLEMENTATION_CONTRACT.md#hash-and-run-reproducibility`
- Evidence collected: `.venv/bin/python -m pytest -q tests/reset/test_core_v2_schema_evolution_policy.py` reported `3 passed`
- Follow-ups: execute T125 Schema Compatibility Primitives
- Notes for next agent: T125 may add deterministic library-only compatibility primitives. Do not add CLI, migration execution, service behavior, or registry mutation in T125.

### 2026-05-29 - T125 - Schema Compatibility Primitives

- Scope: `src/entropy/artifacts/schema_compatibility.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_schema_compatibility.py`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: add deterministic library-only schema compatibility classification primitives according to the Core V2 schema evolution policy
- Decisions applied: `docs/core/SCHEMA_EVOLUTION_POLICY.md`; `docs/CORE_V2_ROADMAP.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` reported `6 passed`
- Follow-ups: execute T126 Schema Evolution Foundations Review
- Notes for next agent: T125 added no CLI, migration execution, service behavior, or registry mutation. Compatibility results remain `not_approved` for restricted surfaces.

### 2026-05-29 - T126 - Schema Evolution Foundations Review

- Scope: `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: close Phase 28 and open the next bounded Core V2 phase without triggering a human gate
- Decisions applied: `docs/DECISION_LOG.md#D-CORE-V2-001`; `docs/CORE_V2_ROADMAP.md`; `docs/core/SCHEMA_EVOLUTION_POLICY.md`
- Evidence collected: Phase 28 review PASS; prior T124/T125 tests `6 passed`; no P0/P1 findings
- Follow-ups: execute T127 Evidence Lookup Policy Contract
- Notes for next agent: Phase 29 is local deterministic evidence lookup hardening only. Do not add runtime RAG, embeddings, hosted search, public API, service behavior, public SDK, live, holdout, external compliance, production credential, or capital scope.

### 2026-05-29 - T127 - Evidence Lookup Policy Contract

- Scope: `docs/core/EVIDENCE_LOOKUP_POLICY.md`, `tests/reset/test_evidence_lookup_policy.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: define local deterministic evidence lookup policy before lookup primitive implementation
- Decisions applied: `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md`; `docs/CORE_V2_ROADMAP.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/reset/test_evidence_lookup_policy.py tests/reset/test_core_v2_schema_evolution_policy.py tests/unit/test_schema_compatibility.py` reported `9 passed`
- Follow-ups: execute T128 Local Evidence Lookup Primitives
- Notes for next agent: T128 may parse local `docs/EVIDENCE_INDEX.md` rows only. Do not add runtime RAG, embeddings, hosted search, public API, CLI, external dependencies, or service behavior.

### 2026-05-29 - T128 - Local Evidence Lookup Primitives

- Scope: `src/entropy/artifacts/evidence_lookup.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_evidence_lookup.py`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: add deterministic file-local evidence-index lookup primitives according to the evidence lookup policy
- Decisions applied: `docs/core/EVIDENCE_LOOKUP_POLICY.md`; `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` reported `12 passed`
- Follow-ups: execute T129 Evidence Inspect Alignment
- Notes for next agent: T128 added no runtime RAG, embeddings, hosted search, public API, CLI, external dependencies, or service behavior. Results remain `not_approved` for restricted surfaces.

### 2026-05-29 - T129-T130 - Evidence Inspect Alignment And Review

- Scope: `src/entropy/artifacts/evidence_lookup.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_evidence_lookup.py`, `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: align packet evidence refs with local lookup metadata, close Phase 29, and open the next bounded Core V2 phase
- Decisions applied: `docs/core/EVIDENCE_LOOKUP_POLICY.md`; `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md`; `docs/CORE_V2_ROADMAP.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` reported `15 passed`; Phase 29 review PASS
- Follow-ups: execute T131 Product Bridge Adoption Policy
- Notes for next agent: Phase 30 must stay inside Core-owned product-profile validation and synthetic fixtures. Do not edit product workspaces, own product report logic, approve external delivery, or open public SDK, hosted service, live, holdout, compliance, production credential, or capital scope.

### 2026-05-29 - T131 - Product Bridge Adoption Policy

- Scope: `docs/core/PRODUCT_BRIDGE_ADOPTION_POLICY.md`, `tests/reset/test_product_bridge_adoption_policy.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: define Core-owned product bridge adoption policy before adding readiness checks or synthetic adoption fixtures
- Decisions applied: `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md`; `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`; `docs/CORE_V2_ROADMAP.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/reset/test_product_bridge_adoption_policy.py tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` reported `18 passed`
- Follow-ups: execute T132 Product Bridge Readiness Checks
- Notes for next agent: T132 may add Core-side readiness checks only. Do not edit product workspaces, own product report logic, approve external delivery, or open public SDK, hosted service, live, holdout, compliance, production credential, or capital scope.

### 2026-05-29 - T132 - Product Bridge Readiness Checks

- Scope: `src/entropy/artifacts/product_bridge_adoption.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_product_bridge_adoption.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: add deterministic Core-side readiness checks for product bridge adoption metadata before adding synthetic adoption fixtures
- Decisions applied: `docs/core/PRODUCT_BRIDGE_ADOPTION_POLICY.md`; `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_adoption.py tests/reset/test_product_bridge_adoption_policy.py tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` reported `21 passed`; changed Python ruff slice clean
- Follow-ups: execute T133 Product Bridge Adoption Fixtures
- Notes for next agent: T133 may add synthetic/redacted fixtures only. Do not use real customer, product, private research, holdout, credential, or live data; do not edit product workspaces, own product report logic, approve external delivery, or open public SDK, hosted service, live, holdout, compliance, production credential, or capital scope.

### 2026-05-29 - T133 - Product Bridge Adoption Fixtures

- Scope: `tests/fixtures/artifacts/adoption/`, `tests/unit/test_product_bridge_adoption.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: add synthetic adoption fixtures that exercise the Core-side readiness checks for valid and unsafe product bridge adoption metadata
- Decisions applied: `docs/core/PRODUCT_BRIDGE_ADOPTION_POLICY.md`; `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_adoption.py tests/reset/test_product_bridge_adoption_policy.py tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` reported `24 passed`
- Follow-ups: execute T134 Product Bridge Adoption Readiness Review
- Notes for next agent: T134 should review Phase 30 evidence and either open the next bounded V2 phase or stop for a human gate if scope expansion would be required. Product workspace edits, product report ownership, external delivery approval, public SDK, hosted service, live, holdout, compliance, production credential, and capital scope remain blocked.

### 2026-05-29 - T134 - Product Bridge Adoption Readiness Review

- Scope: `docs/audit/PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: close Phase 30 and open the next bounded Core V2 internal review phase without triggering a human gate
- Decisions applied: `docs/core/PRODUCT_BRIDGE_ADOPTION_POLICY.md`; `docs/CORE_V2_ROADMAP.md`; `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md`
- Evidence collected: Phase 30 review PASS; prior T133 test slice `24 passed`; no Stop-Ship/P0/P1 findings
- Follow-ups: execute T135 V2 Kernel Foundation Inventory
- Notes for next agent: Phase 31 is internal kernel review only. Do not add public SDK, hosted service, runtime RAG, embeddings, product runtime ownership, product report authorship, external delivery approval, live, holdout, compliance, production credential, or capital scope.

### 2026-05-29 - T135 - V2 Kernel Foundation Inventory

- Scope: `docs/core/V2_KERNEL_FOUNDATION_INVENTORY.md`, `tests/reset/test_v2_kernel_review_inventory.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: inventory Core V2 foundations and preserve the internal kernel boundary before adding restricted-surface regression checks
- Decisions applied: `docs/audit/PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md`; `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md`; `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/reset/test_v2_kernel_review_inventory.py tests/unit/test_product_bridge_adoption.py tests/reset/test_product_bridge_adoption_policy.py tests/reset/test_reset_smoke.py tests/reset/test_no_claim_roadmap_sweep.py tests/reset/test_live_feed_boundary_contract.py tests/reset/test_broker_sandbox_boundary_contract.py` reported `26 passed`
- Follow-ups: execute T136 Restricted Surface Regression Sweep V2
- Notes for next agent: T136 may add regression tests only. It must not implement public SDK, hosted service, runtime RAG, live, holdout, compliance, production credential, product runtime ownership, product report authorship, external delivery approval, or capital scope.

### 2026-05-31 - T136 - Restricted Surface Regression Sweep V2

- Scope: `tests/reset/test_v2_restricted_surface_sweep.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: add V2 regression checks proving the current Core V2 docs and reviews keep restricted surfaces blocked
- Decisions applied: `docs/core/V2_KERNEL_FOUNDATION_INVENTORY.md`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/reset/test_v2_restricted_surface_sweep.py tests/reset/test_v2_kernel_review_inventory.py tests/reset/test_no_claim_roadmap_sweep.py tests/reset/test_live_feed_boundary_contract.py tests/reset/test_broker_sandbox_boundary_contract.py` reported `15 passed`
- Follow-ups: execute T137 V2 Evidence Completeness Matrix
- Notes for next agent: T137 should summarize evidence coverage and gaps only. It must not convert gaps into product, hosted, live, holdout, compliance, production credential, or capital readiness claims.

### 2026-05-31 - T137 - V2 Evidence Completeness Matrix

- Scope: `docs/core/V2_EVIDENCE_COMPLETENESS_MATRIX.md`, `tests/reset/test_v2_evidence_completeness_matrix.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: summarize V2 evidence coverage and remaining internal gaps before the Phase 31 review
- Decisions applied: `docs/core/V2_KERNEL_FOUNDATION_INVENTORY.md`; `docs/audit/PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: `.venv/bin/python -m pytest -q tests/reset/test_v2_evidence_completeness_matrix.py tests/reset/test_v2_restricted_surface_sweep.py tests/reset/test_v2_kernel_review_inventory.py tests/reset/test_no_claim_roadmap_sweep.py tests/reset/test_live_feed_boundary_contract.py tests/reset/test_broker_sandbox_boundary_contract.py` reported `18 passed`
- Follow-ups: execute T138 V2 Internal Kernel Review
- Notes for next agent: T138 should review V2 foundations, regression coverage, evidence completeness, limitations, and open findings. It must stop for a human gate if the next desired work needs public SDK, hosted service, product runtime ownership, external compliance, holdout, live, production credential, or capital scope.

### 2026-05-31 - T138 - V2 Internal Kernel Review

- Scope: `docs/audit/V2_INTERNAL_KERNEL_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`
- Why this work happened: close Phase 31 and decide whether Core V2 can continue without a new human gate
- Decisions applied: `docs/core/V2_EVIDENCE_COMPLETENESS_MATRIX.md`; `docs/core/V2_KERNEL_FOUNDATION_INVENTORY.md`; `docs/CORE_V2_ROADMAP.md`
- Evidence collected: Phase 31 review PASS; `.venv/bin/python -m pytest -q tests/reset/test_v2_evidence_completeness_matrix.py tests/reset/test_v2_restricted_surface_sweep.py tests/reset/test_v2_kernel_review_inventory.py tests/reset/test_no_claim_roadmap_sweep.py tests/reset/test_live_feed_boundary_contract.py tests/reset/test_broker_sandbox_boundary_contract.py tests/reset/test_reset_smoke.py` reported `23 passed`
- Follow-ups: wait for a human decision opening the next bounded Core V2 phase
- Notes for next agent: No active next task is approved. Do not continue beyond T138 until a human opens a new bounded Core V2 phase. Public SDK, hosted service, runtime RAG, embeddings, product runtime/report ownership, external delivery approval, live, holdout, compliance, production credential, and capital scope remain blocked.

### 2026-05-14 - T122 - Core V1 Productization Review

- Scope: `docs/audit/CORE_V1_PRODUCTIZATION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `README.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: close Phase 27 and checkpoint Core V1 as a documented, tested internal product kernel
- Decisions applied: `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: full pytest `625 passed, 20 skipped`; ruff clean; scoped artifact/db pyright `0 errors`; `git diff --check` clean
- Follow-ups: stop automatic roadmap expansion until a human approves a Core V2 roadmap
- Notes for next agent: Core V1 is internal only. Do not continue beyond T122 or invent a V2 roadmap without human approval.

### 2026-05-14 - T121 - Documentation And Test Alignment Sweep

- Scope: `docs/ARCHITECTURE.md`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `README.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: align active architecture, evidence, README, and task state with the final Core V1 internal surface
- Decisions applied: `docs/core/CORE_V1_SURFACE_FREEZE.md`; `docs/IMPLEMENTATION_CONTRACT.md`
- Evidence collected: manual docs review pending final Phase 27 validation
- Follow-ups: start T122 Core V1 Productization Review
- Notes for next agent: `docs/IMPLEMENTATION_CONTRACT.md` was reviewed as immutable authority and was not changed because no ADR-approved contract change was required.

### 2026-05-14 - T120 - Operator Runbook And Examples

- Scope: `RUNBOOK.md`, `docs/core/CORE_V1_EXAMPLES.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: document local operator command sequences and synthetic examples for generic, research-shaped, product-shaped, CAF-shaped, evidence, governance, and failure-handling workflows
- Decisions applied: `docs/AI_LOOP_OPERATING_MODEL.md`; `docs/core/CORE_V1_SURFACE_FREEZE.md`
- Evidence collected: manual document review pending final Phase 27 validation
- Follow-ups: start T121 Documentation And Test Alignment Sweep
- Notes for next agent: Examples reference only synthetic fixtures and local `/tmp` outputs. No real customer, product, private research, holdout, live, broker/exchange, capital, hosted service, public SDK, or compliance claim was introduced.

### 2026-05-14 - T119 - Core V1 Surface Freeze

- Scope: `docs/core/CORE_V1_SURFACE_FREEZE.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: freeze the internal Core V1 surface across CLI commands, schema versions, state vocabularies, storage boundaries, unsupported surfaces, and migration notes
- Decisions applied: `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: manual document review pending final Phase 27 validation
- Follow-ups: start T120 Operator Runbook And Examples
- Notes for next agent: The freeze is internal-only. It explicitly does not approve public SDK, hosted service, SaaS, external compliance, live, broker/exchange, holdout, or capital scope.

### 2026-05-14 - T115-T118 - Enterprise Audit Readiness

- Scope: `src/entropy/artifacts/audit_bundle.py`, `src/entropy/artifacts/lineage.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_audit_bundle.py`, `tests/unit/test_lineage_graph.py`, `tests/unit/test_audit_data_classification.py`, `docs/audit/ENTERPRISE_AUDIT_READINESS_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 26 by adding exportable audit bundle, lineage, data classification, reviewer role metadata, and review evidence without external certification or service claims
- Decisions applied: `docs/ARCHITECTURE.md#security-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#authorization`; `docs/EVIDENCE_INDEX.md`; `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
- Evidence collected: audit bundle tests `7 passed`; bundle/lineage tests `10 passed`; bundle/lineage/classification tests `13 passed`; full pytest `625 passed, 20 skipped`; scoped source pyright `0 errors`; scoped ruff clean
- Follow-ups: start T119 Core V1 Surface Freeze
- Notes for next agent: Audit readiness remains internal packaging metadata. No SOC 2, regulatory compliance, investment-advice compliance, enterprise SLA, hosted service, auth/RBAC, SSO, tenant isolation, public SDK, holdout, live, broker/exchange, or capital scope was introduced.

### 2026-05-14 - T111-T114 - CAF Decision Primitives

- Scope: `src/entropy/artifacts/caf.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_caf_artifact_vocabulary.py`, `tests/unit/test_allocation_decision_artifact.py`, `tests/unit/test_caf_artifact_fixtures.py`, `tests/fixtures/artifacts/caf/`, `docs/audit/CAF_DECISION_PRIMITIVES_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 25 by adding CAF artifact vocabulary, governed allocation decision primitives, synthetic fixtures, and review evidence without opening execution or advice scope
- Decisions applied: `docs/core/CHARTER.md#b-non-negotiables`; `docs/core/PROTOCOL_SPEC.md`; `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: CAF scoped tests `12 passed`; reset suite `150 passed`; full pytest `612 passed, 20 skipped`; ruff clean; scoped artifact/db pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T115 Audit Bundle Schema
- Notes for next agent: CAF artifacts are evidence contracts only. No capital movement, investment advice, live allocation, broker/exchange execution, production label, public SDK, hosted service, holdout, or OOS scope was introduced.

### 2026-05-14 - T107-T110 - Internal API And Job Boundary

- Scope: `docs/adr/ADR-CORE-INTERNAL-API-JOB-BOUNDARY.md`, `src/entropy/artifacts/api.py`, `src/entropy/artifacts/jobs.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_internal_api_facade.py`, `tests/unit/test_internal_job_model.py`, `docs/audit/INTERNAL_API_JOB_BOUNDARY_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 24 by deciding and implementing an internal-only Python facade and in-process job model without opening service scope
- Decisions applied: `docs/adr/ADR-CORE-INTERNAL-API-JOB-BOUNDARY.md`; `docs/ARCHITECTURE.md#security-boundaries`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: facade tests `3 passed`; facade/job tests `6 passed`; full pytest `600 passed, 20 skipped`; ruff clean; scoped artifact/db pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T111 CAF Artifact Vocabulary
- Notes for next agent: API/job work remains internal-library and in-process only. No public SDK, hosted service, HTTP API, auth, tenant model, external SLA, or worker runtime dependency was introduced.

### 2026-05-14 - T103-T106 - Storage And Audit Backend

- Scope: `migrations/versions/0002_artifact_metadata_tables.py`, `src/entropy/db/models.py`, `src/entropy/artifacts/store.py`, `src/entropy/artifacts/repository.py`, `src/entropy/artifacts/__init__.py`, `tests/integration/test_artifact_metadata_migration.py`, `tests/unit/test_artifact_store.py`, `tests/unit/test_artifact_metadata_repository.py`, `tests/integration/test_artifact_metadata_repository.py`, `docs/audit/STORAGE_AND_AUDIT_BACKEND_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 23 by adding durable artifact metadata schema, local content-addressed storage, insert-only repository behavior, and storage review evidence
- Decisions applied: `docs/ARCHITECTURE.md#runtime-and-isolation-model`; `docs/IMPLEMENTATION_CONTRACT.md#registry-append-only`; `docs/IMPLEMENTATION_CONTRACT.md#sql-safety`
- Evidence collected: migration scoped tests `4 passed`; store/migration tests `6 passed`; repository scoped tests `4 passed`; full pytest `594 passed, 20 skipped`; ruff clean; scoped artifact/db pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T107 Internal API Boundary ADR
- Notes for next agent: Storage remains local/internal. No multi-tenant SaaS, auth, hosted storage, public API, public SDK, or external object-store runtime dependency was introduced.

### 2026-05-14 - T99-T102 - Research Artifact Integration

- Scope: `src/entropy/artifacts/research.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_research_artifact_schemas.py`, `tests/unit/test_research_artifact_adapter.py`, `tests/unit/test_research_artifact_fixtures.py`, `tests/fixtures/artifacts/research/`, `docs/audit/RESEARCH_ARTIFACT_INTEGRATION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 22 by representing archive-only research outputs as governed artifact-compatible schemas and adapters without opening holdout/OOS claims
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary`; `docs/IMPLEMENTATION_CONTRACT.md#pii-policy`
- Evidence collected: research schema tests `3 passed`; schema/adapter tests `6 passed`; research fixture scoped tests `9 passed`; full pytest `584 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T103 Artifact Metadata Migration
- Notes for next agent: Research artifacts preserve archive-only no-claim semantics. No holdout read/unlock, OOS/performance label, live execution, broker/exchange, production, capital-ready, public SDK, or hosted service scope was opened.

### 2026-05-14 - T95-T98 - Artifact Governance State Machine

- Scope: `src/entropy/artifacts/governance.py`, `src/entropy/artifacts/__init__.py`, `src/entropy/cli.py`, `tests/unit/test_artifact_governance_state.py`, `tests/unit/test_artifact_governance_cli.py`, `tests/unit/test_artifact_approval_binding.py`, `docs/audit/ARTIFACT_GOVERNANCE_STATE_MACHINE_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 21 by adding deterministic artifact governance states, local append-only transition CLI, approval-event binding, and governance review evidence
- Decisions applied: `docs/IMPLEMENTATION_CONTRACT.md#deterministic-runtime-truth`; `docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: governance state tests `3 passed`; governance state/CLI tests `6 passed`; approval binding scoped tests `9 passed`; full pytest `575 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T99 Research Artifact Schemas
- Notes for next agent: Governance state mechanics do not approve external delivery, live execution, holdout access, broker/exchange execution, production, capital-ready status, or OOS/performance claims.

### 2026-05-14 - T91-T94 - Product Bridge Profiles

- Scope: `src/entropy/artifacts/profiles.py`, `src/entropy/artifacts/__init__.py`, `src/entropy/cli.py`, `tests/unit/test_product_bridge_profiles.py`, `tests/unit/test_product_bridge_profile_cli.py`, `tests/unit/test_product_bridge_profile_fixtures.py`, `tests/fixtures/artifacts/profiles/`, `docs/audit/PRODUCT_BRIDGE_PROFILE_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 20 by adding Core-only product bridge profile overlays, profile-aware CLI validation, synthetic product-shaped fixtures, and a profile review
- Decisions applied: `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`; `docs/IMPLEMENTATION_CONTRACT.md#pii-policy`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: profile model tests `3 passed`; profile CLI scoped tests `15 passed`; fixture/profile scoped tests `9 passed`; full pytest `566 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T95 Artifact Governance State Model
- Notes for next agent: Profile ids are Core validation overlays only. Product runtime behavior, report generation, source ingestion, delivery approval, and product-local error registers remain outside Core.

### 2026-05-14 - T89-T90 - Evidence Index Automation And Pipeline Review

- Scope: `src/entropy/artifacts/evidence_index.py`, `src/entropy/artifacts/__init__.py`, `tests/unit/test_artifact_evidence_index.py`, `docs/audit/EVIDENCE_PIPELINE_REVIEW.md`, `docs/audit/generated/evidence/artifact-bf2e9ce008e7c16d.json`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 19 by adding safe evidence-index automation and reviewing the evidence packet pipeline before product bridge profile hardening
- Decisions applied: `docs/EVIDENCE_INDEX.md`; `docs/AI_LOOP_OPERATING_MODEL.md`; `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`
- Evidence collected: evidence-index plus evidence packet/CLI tests `9 passed`; full pytest `557 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T91 Product Bridge Profile Model
- Notes for next agent: Phase 20 profile work may add Core validation overlays for product-shaped artifacts, but must not edit Trader Risk Audit or Signal Analytics Sandbox workspaces or absorb product report logic into Core.

### 2026-05-14 - T75-T78 - Executable Artifact Validation

- Scope: `src/entropy/artifacts/`, `src/entropy/cli.py`, `tests/unit/test_artifact_contract_v1.py`, `tests/unit/test_artifact_validation.py`, `tests/unit/test_artifact_cli.py`, `tests/fixtures/artifacts/`, `.gitignore`, repository root `.gitignore`, `docs/audit/EXECUTABLE_ARTIFACT_VALIDATION_REVIEW.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/CODEX_PROMPT.md`
- Why this work happened: continue Phase 16 by turning the frozen Phase 15 artifact contract into executable Core validators, fixtures, and local CLI behavior
- Decisions applied: `docs/core/ARTIFACT_CONTRACT.md`; `docs/core/REPORT_VALIDITY_CHECKLIST.md`; `docs/AI_LOOP_OPERATING_MODEL.md`
- Evidence collected: pre-task full pytest baseline `23 failed, 487 passed, 20 skipped`; T75-T77 scoped artifact tests `15 passed`; artifact plus existing CLI tests `18 passed`; reset suite `150 passed`; full pytest `525 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T79 Artifact Registry Model
- Notes for next agent: Phase 16 closed and Phase 17 opened. The implementation did not touch Trader Risk Audit or Signal Analytics Sandbox and did not add public SDK, hosted service, holdout/OOS, live, broker/exchange, capital, or new runtime scope.

### 2026-05-14 - T79-T82 - Artifact Registry

- Scope: `src/entropy/artifacts/registry.py`, `src/entropy/cli.py`, `tests/unit/test_artifact_registry.py`, `tests/unit/test_artifact_registry_cli.py`, `docs/audit/ARTIFACT_REGISTRY_REVIEW.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: continue Phase 17 by adding governed local artifact registry records and safe local operator registry commands on top of executable artifact validation
- Decisions applied: `docs/IMPLEMENTATION_CONTRACT.md#registry-append-only`; `docs/AI_LOOP_OPERATING_MODEL.md`; `docs/core/ARTIFACT_CONTRACT.md`
- Evidence collected: registry model and CLI tests `15 passed`; full pytest `534 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T83 Reproducibility Manifest Schema
- Notes for next agent: registry storage is local JSONL until Phase 23. No database persistence, public SDK, hosted service, holdout/OOS, live, broker/exchange, capital, production, or product workspace scope was opened.

### 2026-05-14 - T83-T86 - Reproducibility Runner

- Scope: `src/entropy/artifacts/reproducibility.py`, `src/entropy/cli.py`, `tests/unit/test_reproducibility_manifest.py`, `tests/unit/test_reproducibility_runner.py`, `tests/unit/test_reproducibility_cli.py`, `docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: continue Phase 18 by adding local reproducibility manifests, deterministic hash comparison, safe diff metadata, and compare-only CLI behavior
- Decisions applied: `docs/core/REPRODUCIBILITY_CHECKLIST.md`; `docs/IMPLEMENTATION_CONTRACT.md#hash-and-run-reproducibility`
- Evidence collected: manifest and runner tests `11 passed`; reproducibility CLI scoped tests `17 passed`; full pytest `548 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T87 Evidence Packet Schema
- Notes for next agent: direct rerun command execution remains blocked. Reproducibility status is local/internal evidence support only and is not performance, external pilot, production, capital-ready, holdout/OOS, live, or broker/exchange approval.

### 2026-05-14 - T87-T88 - Evidence Packet Schema And CLI

- Scope: `src/entropy/artifacts/evidence.py`, `src/entropy/cli.py`, `tests/unit/test_artifact_evidence_packet.py`, `tests/unit/test_artifact_evidence_cli.py`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: continue Phase 19 by adding deterministic evidence packets and local build/inspect commands for validated and registered artifacts
- Decisions applied: `docs/core/REPORT_VALIDITY_CHECKLIST.md`; `docs/EVIDENCE_INDEX.md`
- Evidence collected: evidence packet tests `3 passed`; evidence CLI scoped tests `9 passed`; full pytest `554 passed, 20 skipped`; ruff clean; scoped artifact pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T89 Evidence Index Automation
- Notes for next agent: evidence packets explain status and boundaries; they do not grant external delivery, production, capital-ready, holdout/OOS, live, broker/exchange, or investment-advice approval.

### 2026-05-12 - ROADMAP - Core Executable Roadmap And AI Loop Setup

- Scope: `docs/CORE_12_MONTH_EXECUTION_ROADMAP.md`, `docs/AI_LOOP_OPERATING_MODEL.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: operator clarified that Entropy Core is the long-lived protocol kernel, while Trader Risk Audit and Signal Analytics Sandbox remain separate commercial product workspaces; Core needs a full AI-loop roadmap rather than another manual checkpoint
- Decisions applied: Core remains internal; adjacent product artifacts may be used as shape examples only; AI agents may auto-continue through T75-T122 unless a human gate is triggered
- Evidence collected: roadmap and AI loop documents created; detailed task graph added for Phases 16-27; `git diff --check` clean
- Follow-ups: start T75 Artifact Contract V1 Schema
- Notes for next agent: the next executable proof point is `ArtifactContractV1` plus validation tests. Do not edit neighboring product workspaces from Core tasks.

### 2026-05-12 - T74 - Core Artifact Support Review And Platformization Gate

- Scope: `docs/audit/ARTIFACT_SUPPORT_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: close Phase 15 artifact-support mode and decide whether Core should remain internal, expose an internal SDK surface, or remain frozen until product report artifacts validate
- Decisions applied: `docs/core/ARTIFACT_CONTRACT.md`; `docs/core/REPORT_VALIDITY_CHECKLIST.md`; `docs/core/REPRODUCIBILITY_CHECKLIST.md`; `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`; `docs/templates/`
- Evidence collected: T74 manual review PASS; Stop-Ship 0, P0 0, P1 0, P2 0; `git diff --check` clean
- Follow-ups: wait for product-local adoption evidence from Trader Risk Audit or Signal Analytics Sandbox, or an explicit human-scoped Core support task
- Notes for next agent: Phase 15 keeps Core hidden/internal. No public SDK, hosted service, live execution, holdout/OOS workflow, production/capital-ready path, or product-specific report logic ownership is approved.

### 2026-05-12 - T73 - Internal Review Packet Templates

- Scope: `docs/templates/ARTIFACT_SCOPE_NOTE.md`, `docs/templates/MANUAL_VALIDATION_NOTES.md`, `docs/templates/ERROR_REGISTER.md`, `docs/templates/EXTERNAL_DELIVERY_DECISION.md`, `docs/ARTIFACT_SUPPORT_ROADMAP.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: provide short product-neutral templates for real input scope, manual validation, error tracking, external delivery decisions, redaction approval, and pilot feedback
- Decisions applied: `docs/core/ARTIFACT_CONTRACT.md`; `docs/core/REPORT_VALIDITY_CHECKLIST.md`
- Evidence collected: manual docs review; `git diff --check` clean
- Follow-ups: start T74 Core Artifact Support Review And Platformization Gate
- Notes for next agent: templates are copy sources owned by product workspaces and explicitly warn against raw private/customer data, secrets, credentials, private keys, or unredacted confidential payloads.

### 2026-05-12 - T72 - Product Bridge Support Notes

- Scope: `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`, `docs/ARTIFACT_SUPPORT_ROADMAP.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: document narrow Core support boundaries for Trader and Signal artifact validation while keeping product-specific report logic product-local
- Decisions applied: `docs/core/ARTIFACT_CONTRACT.md`; `docs/bridges/trader-risk-audit.md`
- Evidence collected: manual docs review; `git diff --check` clean
- Follow-ups: start T73 Internal Review Packet Templates
- Notes for next agent: bridge notes explicitly forbid Core-driven product rewrites and preserve Trader no-order/no-live/no-production boundaries plus Signal no-advice/no-future-performance boundaries.

### 2026-05-12 - T71 - Reproducibility Checklist

- Scope: `docs/core/REPRODUCIBILITY_CHECKLIST.md`, `docs/ARTIFACT_SUPPORT_ROADMAP.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: define shared rerun, hash comparison, and accepted-nondeterminism guidance for product report artifacts
- Decisions applied: `docs/core/ARTIFACT_CONTRACT.md`; `docs/core/REPORT_VALIDITY_CHECKLIST.md`
- Evidence collected: manual docs review; `git diff --check` clean
- Follow-ups: start T72 Product Bridge Support Notes
- Notes for next agent: Trader guidance focuses on same real audit inputs producing the same material findings; Signal guidance distinguishes hash-reproducible source packs from source availability and manual-review dependencies.

### 2026-05-12 - T70 - Report Validity Checklist

- Scope: `docs/core/REPORT_VALIDITY_CHECKLIST.md`, `docs/ARTIFACT_SUPPORT_ROADMAP.md`, `docs/tasks.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: define a shared manual checklist for moving Trader or Signal report artifacts from internal review to controlled external pilot readiness
- Decisions applied: `docs/core/ARTIFACT_CONTRACT.md`; `docs/ARTIFACT_SUPPORT_ROADMAP.md`
- Evidence collected: manual docs review; `git diff --check` clean
- Follow-ups: start T71 Reproducibility Checklist
- Notes for next agent: checklist separates internal demo readiness from controlled external pilot readiness and treats P0/P1 issues, delivery approval mismatches, and unapproved claim surfaces as blockers.

### 2026-05-12 - T69 - Shared Artifact Contract Freeze

- Scope: `docs/core/ARTIFACT_CONTRACT.md`, `docs/ARTIFACT_SUPPORT_ROADMAP.md`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`
- Why this work happened: define a minimal shared artifact contract that Trader Risk Audit and Signal Analytics Sandbox can attach to real reports without moving product-specific report logic into Core
- Decisions applied: `docs/ARTIFACT_SUPPORT_ROADMAP.md`; `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
- Evidence collected: manual docs review; `git diff --check` clean
- Follow-ups: start T70 Report Validity Checklist
- Notes for next agent: Core owns only shared artifact validity vocabulary, no-claim language, and product-neutral validation expectations. Trader and Signal keep their report logic, data handling, delivery decisions, and error registers product-local.

### 2026-05-09 - T68 - Local Replay Extension Review

- Scope: `docs/audit/LOCAL_REPLAY_EXTENSION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `tests/reset/test_local_replay_extension_review.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: close Phase 14 with a local replay extension review, validation record, limitations, findings, product hypothesis status, and next decision point
- Decisions applied: `docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md`; `tests/reset/test_replay_evidence_non_approval_regression.py`
- Evidence collected: T68 acceptance tests passed (`3 passed`); full reset baseline `510 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: checkpoint for human decision before any further validation execution phase
- Notes for next agent: Phase 14 is closed. Product hypothesis status is `local_evidence_strengthened_not_confirmed`; no restricted validation, holdout/OOS, broker/exchange execution, production credential, live capital, production, or capital-ready path is approved.

### 2026-05-09 - T67 - Replay Evidence Non-Approval Regression

- Scope: `tests/reset/test_replay_evidence_non_approval_regression.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: prove replay approval, replay results, and local evidence delta packets remain non-approval sources for restricted execution and product claim labels
- Decisions applied: `docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md`; `docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md`
- Evidence collected: T67 acceptance tests passed (`3 passed`); full reset baseline `507 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T68 Local Replay Extension Review
- Notes for next agent: Phase 14 is ready for local review. Restricted execution and claim surfaces remain blocked.

### 2026-05-09 - T66 - Local Replay Evidence Delta Decision

- Scope: `docs/approvals/LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md`, `tests/reset/test_local_replay_evidence_delta_decision.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: decide how the deterministic local no-effect replay evidence changes the product hypothesis posture without creating restricted execution or claim approvals
- Decisions applied: `docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md`; `docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md`
- Evidence collected: T66 acceptance tests passed (`3 passed`); full reset baseline `504 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T67 Replay Evidence Non-Approval Regression
- Notes for next agent: product hypothesis remains not confirmed and not rejected. T66 only selects the next local test option, `replay_evidence_non_approval_regression`, and keeps all restricted actions blocked.

### 2026-05-09 - T65 - Broker Sandbox Replay Evidence Packet

- Scope: `docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT.md`, `docs/protocols/BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md`, `tests/reset/test_broker_sandbox_no_capital_replay_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record the approved local replay contract and evidence packet after adding the deterministic no-capital replay primitive
- Decisions applied: `docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md`; `src/entropy/simbroker/replay.py`
- Evidence collected: T65 acceptance tests passed (`4 passed`); full reset baseline `501 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T66 Local Replay Evidence Delta Decision
- Notes for next agent: replay hash is `9b3681de22bf73160baadb022cc4b8af289b144449ca421ffa0f6457910c4c7e`; product hypothesis delta is `local_evidence_strengthened_not_confirmed`, not a confirmation claim.

### 2026-05-09 - T64 - Broker Sandbox No-Capital Replay Primitive

- Scope: `src/entropy/simbroker/replay.py`, `src/entropy/simbroker/__init__.py`, `tests/unit/test_simbroker_replay.py`
- Why this work happened: execute the approved local broker sandbox no-capital replay extension using deterministic in-process SimBroker primitives
- Decisions applied: `docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md`; `docs/protocols/SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md`
- Evidence collected: T64 acceptance tests passed (`5 passed`); full reset baseline `497 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T65 Broker Sandbox Replay Evidence Packet
- Notes for next agent: replay rejects invalid scopes, empty scenarios, duplicate scenario ids, and live broker/exchange imports. It does not implement order emission.

### 2026-05-09 - T63 - Local Broker Sandbox Replay Approval Event

- Scope: `docs/approvals/LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md`, `tests/reset/test_local_broker_sandbox_replay_approval_event.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: operator approved proceeding with the local broker sandbox no-capital replay extension after Phase 13
- Decisions applied: operator approval message on 2026-05-09; `docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md`
- Evidence collected: T63 acceptance tests passed (`3 passed`); full reset baseline `492 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T64 Broker Sandbox No-Capital Replay Primitive
- Notes for next agent: approval scope is `local_broker_sandbox_no_capital_replay` with `local_no_effect_only` maximum effect. It does not approve external side effects or claims.

### 2026-05-09 - T62 - Product Hypothesis Confirmation Decision Review

- Scope: `docs/audit/PRODUCT_HYPOTHESIS_CONFIRMATION_DECISION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `tests/reset/test_product_hypothesis_confirmation_decision_review.py`
- Why this work happened: close Phase 13 local-only product hypothesis confirmation decision work and record the next human decision point
- Decisions applied: `docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md`
- Evidence collected: T62 acceptance tests passed (`3 passed`); full reset baseline `489 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: human decision required before any future validation execution
- Notes for next agent: product hypothesis status is `unconfirmed_pending_future_validation`. The recommended next safe approval is a future local broker sandbox no-capital replay extension task. No next validation execution is approved.

### 2026-05-09 - T61 - Local Next Validation Plan Packet

- Scope: `docs/approvals/LOCAL_NEXT_VALIDATION_PLAN_PACKET.md`, `tests/reset/test_local_next_validation_plan_packet.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: assemble a human-reviewable local next-validation plan before Phase 13 review
- Decisions applied: `docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md`
- Evidence collected: T61 acceptance tests passed (`3 passed`); full reset baseline `486 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T62 Product Hypothesis Confirmation Decision Review
- Notes for next agent: recommended next step is a local broker sandbox no-capital replay extension plan only. The plan is not executed and does not confirm/reject the product hypothesis.

### 2026-05-09 - T60 - Production Capital Non-Approval Regression

- Scope: `tests/reset/test_production_capital_non_approval_regression.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: prove Phase 13 local-only artifacts remain non-approval sources before assembling the next validation plan
- Decisions applied: `docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md`
- Evidence collected: T60 acceptance tests passed (`3 passed`); full reset baseline `483 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T61 Local Next Validation Plan Packet
- Notes for next agent: roadmap rows, reviews, tests, protocol docs, readiness artifacts, generated scaffolds, local dry-run packets, and Phase 13 packets are not approval sources. Restricted actions remain blocked.

### 2026-05-09 - T59 - Product Hypothesis Validation Path Decision

- Scope: `docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md`, `tests/reset/test_product_hypothesis_validation_path_decision.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record the safest current validation path toward product hypothesis confirmation after approval intake rejected current missing approval state
- Decisions applied: `docs/approvals/PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md`
- Evidence collected: T59 acceptance tests passed (`3 passed`); full reset baseline `480 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T60 Production Capital Non-Approval Regression
- Notes for next agent: selected path is local planning only; product hypothesis is not confirmed; holdout/OOS, live execution, capital deployment, production labels, and capital-ready labels remain blocked.

### 2026-05-09 - T58 - Product Validation Approval Intake Contract

- Scope: `docs/approvals/PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md`, `tests/reset/test_product_validation_approval_intake_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define local-only intake requirements for any future validation approval before choosing a validation path
- Decisions applied: `docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md`
- Evidence collected: T58 acceptance tests passed (`3 passed`); full reset baseline `477 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T59 Product Hypothesis Validation Path Decision
- Notes for next agent: T58 creates no approval event. Missing, generated, inferred, stale, revoked, incomplete, and overbroad approvals are rejected; restricted actions remain blocked.

### 2026-05-09 - T57 - Product Hypothesis Confirmation Request Packet

- Scope: `docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md`, `tests/reset/test_product_hypothesis_confirmation_request.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: operator approved rewriting Phase 13 as local-only approval decision work to define the safest next validation step toward product hypothesis confirmation
- Decisions applied: `docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md`; operator approval on 2026-05-09
- Evidence collected: T57 acceptance tests passed (`3 passed`); full reset baseline `474 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T58 Product Validation Approval Intake Contract
- Notes for next agent: T57 does not confirm the product hypothesis and does not approve live orders, broker/exchange execution, production credentials, live capital, production labels, capital-ready labels, or holdout access.

### 2026-05-09 - T56 - Broker Sandbox Readiness Review

- Scope: `docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `tests/reset/test_broker_sandbox_readiness_review.py`
- Why this work happened: close Phase 12 broker sandbox and execution risk audit, then evaluate the production/capital gate roadmap boundary
- Decisions applied: `docs/protocols/SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md`
- Evidence collected: T56 acceptance tests passed (`3 passed`); full reset baseline `471 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: checkpoint before Phase 13 Production and Capital Gate
- Notes for next agent: Phase 13 production/capital work is blocked pending explicit human approval and a local-only task rewrite. Do not open production, capital, live order, broker/exchange execution, production credential, or holdout access work without operator direction.

### 2026-05-09 - T55 - Sandbox Execution No-Capital Dry Run

- Scope: `docs/protocols/SANDBOX_EXECUTION_NO_CAPITAL_DRY_RUN.md`, `tests/reset/test_sandbox_execution_no_capital_dry_run.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: assemble Phase 12 sandbox execution risk artifacts into a local no-capital dry-run packet before readiness review
- Decisions applied: `docs/protocols/KILL_SWITCH_AUDIT_LOG_CONTRACT.md`
- Evidence collected: T55 acceptance tests passed (`3 passed`); full reset baseline `468 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T56 Broker Sandbox Readiness Review
- Notes for next agent: T55 assembles sandbox boundary, fixture manifest, execution risk control, and kill-switch artifacts into a local no-capital packet. No sandbox or live orders were emitted from code; live broker/exchange execution, production credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T54 - Kill-Switch Audit Log Contract

- Scope: `docs/protocols/KILL_SWITCH_AUDIT_LOG_CONTRACT.md`, `tests/reset/test_kill_switch_audit_log_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define sandbox kill-switch audit requirements before the no-capital dry run
- Decisions applied: `docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md`
- Evidence collected: T54 acceptance tests passed (`3 passed`); full reset baseline `465 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T55 Sandbox Execution No-Capital Dry Run
- Notes for next agent: T54 records deterministic trigger, state transition, actor fingerprint, append-only log hash, and fail-closed behavior. Live order telemetry, live broker/exchange execution, production credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T53 - Execution Risk Control Contract

- Scope: `docs/protocols/EXECUTION_RISK_CONTROL_CONTRACT.md`, `tests/reset/test_execution_risk_control_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define sandbox execution risk controls before kill-switch audit contract work
- Decisions applied: `docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md`
- Evidence collected: T53 acceptance tests passed (`3 passed`); full reset baseline `462 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T54 Kill-Switch Audit Log Contract
- Notes for next agent: T53 records sandbox order validation, risk limits, rejection states, deterministic decision audit fields, and no-capital boundaries. Live orders, live broker/exchange execution, production credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T52 - Broker Sandbox Fixture Manifest

- Scope: `docs/protocols/BROKER_SANDBOX_FIXTURE_MANIFEST.md`, `tests/reset/test_broker_sandbox_fixture_manifest.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define deterministic sandbox fixture requirements before execution risk-control contract work
- Decisions applied: `docs/protocols/BROKER_SANDBOX_BOUNDARY.md`
- Evidence collected: T52 acceptance tests passed (`3 passed`); full reset baseline `459 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T53 Execution Risk Control Contract
- Notes for next agent: T52 binds broker sandbox fixtures to checked-in deterministic order scenarios, hashes, schema, replay constraints, rejected live effects, and no-capital scope. Live orders, live broker/exchange execution, production credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T51 - Broker Sandbox Boundary Contract

- Scope: `docs/protocols/BROKER_SANDBOX_BOUNDARY.md`, `tests/reset/test_broker_sandbox_boundary_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define Phase 12 sandbox-only broker/exchange boundaries before fixture and risk-control work
- Decisions applied: `docs/audit/LIVE_FEED_READINESS_REVIEW.md`
- Evidence collected: T51 acceptance tests passed (`3 passed`); full reset baseline `456 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T52 Broker Sandbox Fixture Manifest
- Notes for next agent: T51 permits only local sandbox scenario review, fixture design, risk-control design, kill-switch audit design, and no-capital dry-run packet assembly. Live orders, live broker/exchange execution, production credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T50 - Live-Feed Dry Run Readiness Review

- Scope: `docs/audit/LIVE_FEED_READINESS_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 11 live-feed dry-run readiness and evaluate the next roadmap phase without enabling broker execution or capital
- Decisions applied: `docs/protocols/LIVE_FEED_OBSERVABILITY_PACKET.md`
- Evidence collected: T50 acceptance tests passed (`3 passed`); full reset baseline `453 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T51 Broker Sandbox Boundary Contract
- Notes for next agent: T50 opens Phase 12 as sandbox-only broker/exchange execution risk audit work. Live orders, live broker/exchange execution, production credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T49 - Live-Feed Observability Packet

- Scope: `docs/protocols/LIVE_FEED_OBSERVABILITY_PACKET.md`, `tests/reset/test_live_feed_observability_packet.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define local dry-run observability evidence before Phase 11 review
- Decisions applied: `docs/protocols/LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md`
- Evidence collected: T49 acceptance tests passed (`3 passed`); full reset baseline `450 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T50 Live-Feed Dry Run Readiness Review
- Notes for next agent: T49 records local observability fields, failure counters, redaction boundaries, and readiness limitations. Secrets, orders, capital actions, external telemetry, production labels, and holdout access remain blocked.

### 2026-05-09 - T48 - Live-Feed Adapter Dry-Run Contract

- Scope: `docs/protocols/LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md`, `tests/reset/test_live_feed_adapter_dry_run_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define local adapter dry-run checks before observability packet work
- Decisions applied: `docs/protocols/LIVE_FEED_FIXTURE_MANIFEST.md`
- Evidence collected: T48 acceptance tests passed (`3 passed`); full reset baseline `447 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T49 Live-Feed Observability Packet
- Notes for next agent: T48 covers local parser, normalization, clock, replay, failure-state, and idempotence checks. Network sockets, credentials, live feed connectivity, orders, broker/exchange execution, capital actions, production labels, and holdout access remain blocked.

### 2026-05-09 - T47 - Live-Feed Fixture Manifest

- Scope: `docs/protocols/LIVE_FEED_FIXTURE_MANIFEST.md`, `tests/reset/test_live_feed_fixture_manifest.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define deterministic local market-data fixture requirements before adapter dry-run work
- Decisions applied: `docs/protocols/LIVE_FEED_DRY_RUN_BOUNDARY.md`
- Evidence collected: T47 acceptance tests passed (`3 passed`); full reset baseline `444 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T48 Live-Feed Adapter Dry-Run Contract
- Notes for next agent: T47 binds fixtures to checked-in deterministic sources, hashes, schema, and replay constraints. Live pulls, credentials, broker/exchange execution, capital actions, production labels, and holdout access remain blocked.

### 2026-05-09 - T46 - Live-Feed Boundary Contract

- Scope: `docs/protocols/LIVE_FEED_DRY_RUN_BOUNDARY.md`, `tests/reset/test_live_feed_boundary_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define Phase 11 live-feed dry-run scope before fixture or adapter work
- Decisions applied: `docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md`; `docs/ARCHITECTURE.md`
- Evidence collected: T46 acceptance tests passed (`3 passed`); full reset baseline `441 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T47 Live-Feed Fixture Manifest
- Notes for next agent: T46 allows only local fixture review, replay, parsing, normalization, clock validation, logging, and failure-state design. Live feed connections, orders, broker/exchange execution, credentials, live capital, production labels, and holdout access remain blocked.

### 2026-05-09 - T45 - Holdout Approval Decision Review

- Scope: `docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 10 approval decision work and evaluate the next roadmap phase without opening holdout
- Decisions applied: `docs/approvals/HOLDOUT_DECISION_DRY_RUN.md`; `docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md`
- Evidence collected: T45 acceptance tests passed (`3 passed`); full reset baseline `438 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T46 Live-Feed Boundary Contract
- Notes for next agent: T45 blocks future approved holdout evaluation and opens Phase 11 as local-only live-feed readiness. No order placement, broker/exchange execution, credentials, live capital, production labels, or holdout access are approved.

### 2026-05-09 - T44 - Holdout Decision No-Read Dry Run

- Scope: `docs/approvals/HOLDOUT_DECISION_DRY_RUN.md`, `tests/reset/test_holdout_decision_no_read_dry_run.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: assemble protocol and denial evidence into a local no-read decision dry run without opening holdout data
- Decisions applied: `docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md`; `docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md`
- Evidence collected: T44 acceptance tests passed (`3 passed`); full reset baseline `435 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T45 Holdout Approval Decision Review
- Notes for next agent: T44 records a denied local no-read decision assembly. No approval event exists, no holdout path was opened, and no read/unlock/OOS approval flag is present.

### 2026-05-09 - T43 - Holdout Non-Approval Source Regression

- Scope: `tests/reset/test_holdout_non_approval_source_regression.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: prevent roadmap phases, reviews, tests, readiness packets, protocol docs, or generated scaffolds from being treated as approval
- Decisions applied: `docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md`; `docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md`
- Evidence collected: T43 acceptance tests passed (`3 passed`); full reset baseline `432 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T44 Holdout Decision No-Read Dry Run
- Notes for next agent: T43 is regression-only and confirms no approval event exists, holdout read/unlock remain blocked, and common artifact classes are non-approval sources.

### 2026-05-09 - T42 - Holdout Approval Absence Denial

- Scope: `docs/approvals/HOLDOUT_APPROVAL_ABSENCE_DENIAL.md`, `tests/reset/test_holdout_approval_absence_denial.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record deterministic denial evidence for the current missing-approval state without opening holdout data
- Decisions applied: `docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md`; `docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md`
- Evidence collected: T42 acceptance tests passed (`3 passed`); full reset baseline `429 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T43 Holdout Non-Approval Source Regression
- Notes for next agent: T42 denies holdout approval because explicit human approval and phase-gate approval are missing, the intake has no accepted event, and the leakage guard remains incomplete. No approval event currently exists.

### 2026-05-09 - T41 - Holdout Approval Evidence Intake

- Scope: `docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md`, `tests/reset/test_holdout_approval_intake_contract.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define no-read intake checks for future explicit holdout approval evidence
- Decisions applied: `docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md`; `docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md`
- Evidence collected: T41 acceptance tests passed (`3 passed`); full reset baseline `426 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T42 Holdout Approval Absence Denial Packet
- Notes for next agent: T41 rejects absent, generated, inferred, expired, revoked, stale, scope-mismatched, and incomplete approval evidence. No approval event currently exists.

### 2026-05-09 - T40 - Holdout Approval Request Packet

- Scope: `docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md`, `tests/reset/test_holdout_approval_request_packet.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: scaffold no-read approval request evidence for Phase 10 without creating approval
- Decisions applied: `docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md`; `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`; `docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md`; `docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md`; `docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md`
- Evidence collected: T40 acceptance tests passed (`3 passed`); full reset baseline `423 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T41 Holdout Approval Evidence Intake Contract
- Notes for next agent: T40 is a request packet scaffold only. No approval event currently exists, and holdout read/unlock remains blocked.

### 2026-05-09 - T39 - Holdout Access Protocol Review

- Scope: `docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `tests/reset/test_holdout_access_protocol_review.py`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 9 with protocol review and roadmap evaluation before opening the next autonomous phase
- Decisions applied: `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`; `docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md`; `docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md`; `docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md`; `D-ROADMAP-001`
- Evidence collected: T39 acceptance tests passed (`3 passed`); full reset baseline `420 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T40 Holdout Approval Request Packet Scaffold
- Notes for next agent: Phase 10 is no-read approval decision work. No approval event currently exists, and holdout read/unlock remain blocked.

### 2026-05-09 - T38 - Holdout Leakage Guard Protocol

- Scope: `docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md`, `tests/reset/test_holdout_leakage_guard_protocol.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define local leakage guard inputs and fail-closed fixtures required before any future holdout read could be considered
- Decisions applied: `src/entropy/walkforward/leakage.py`; `src/entropy/data/holdout.py`; `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`; `D-ROADMAP-001`
- Evidence collected: T38 acceptance tests passed (`3 passed`); full reset baseline `417 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T39 Holdout Access Protocol Review
- Notes for next agent: T38 is fixture/protocol only. Guard status remains incomplete, no approval event exists, and holdout read/unlock remains blocked.

### 2026-05-09 - T37 - Holdout Access Audit Logging

- Scope: `docs/protocols/HOLDOUT_AUDIT_LOGGING_CONTRACT.md`, `tests/reset/test_holdout_audit_logging_contract.py`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define audit logging requirements for denied and future approved holdout access attempts while preserving no-read behavior
- Decisions applied: `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`; `docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md`; `D-ROADMAP-001`
- Evidence collected: T37 acceptance tests passed (`3 passed`); full reset baseline `414 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T38 Holdout Leakage Guard Protocol Fixture
- Notes for next agent: T37 records path fingerprints only, rejects raw holdout path/content in logs, and treats denied attempts as audit events without opening holdout data.

### 2026-05-09 - T36 - Holdout Approval Event Schema

- Scope: `docs/protocols/HOLDOUT_APPROVAL_EVENT_SCHEMA.md`, `tests/reset/test_holdout_approval_event_schema.py`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define the local explicit human holdout approval event schema without creating any approval event
- Decisions applied: `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`; `docs/governance/`; `D-ROADMAP-001`
- Evidence collected: T36 acceptance tests passed (`3 passed`); full reset baseline `411 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T37 Holdout Access Audit Logging Contract
- Notes for next agent: T36 records required approval fields and invalid fixture classes. No approval event currently exists, and holdout read/unlock remains blocked.

### 2026-05-09 - T35 - Holdout Access Protocol

- Scope: `docs/protocols/HOLDOUT_ACCESS_PROTOCOL.md`, `tests/reset/test_holdout_access_protocol.py`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: define a local denied-by-default holdout access protocol before any future approval schema or holdout access discussion
- Decisions applied: `docs/audit/PHASE_GATE_READINESS_REVIEW.md`; `docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md`; `docs/readiness/PHASE_GATE_READINESS_PACKET.md`; `D-ROADMAP-001`
- Evidence collected: T35 acceptance tests passed (`3 passed`); full reset baseline `408 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T36 Holdout Approval Event Schema Contract
- Notes for next agent: T35 is protocol scaffold only. It records denied-by-default, rejects roadmap/review/test/readiness artifacts as approval, and preserves that no approval event currently exists.

### 2026-05-09 - T34 - Phase-Gate Readiness Review

- Scope: `docs/audit/PHASE_GATE_READINESS_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `tests/reset/test_phase_gate_readiness_review.py`, `docs/tasks.md`, `docs/EVIDENCE_INDEX.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: close Phase 8 with a readiness review and roadmap evaluation before opening the next autonomous phase
- Decisions applied: `docs/readiness/PHASE_GATE_GAP_MATRIX.md`; `docs/readiness/PHASE_GATE_READINESS_PACKET.md`; `docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md`; `D-ROADMAP-001`
- Evidence collected: T34 acceptance tests passed (`3 passed`); full reset baseline `405 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T35 Holdout Access Protocol Deny-By-Default Contract
- Notes for next agent: Phase 9 is protocol-only. It may define denied-by-default controls, approval schemas, audit logs, and leakage guards, but must not read or unlock holdout data or create OOS/performance claims.

### 2026-05-09 - T33 - Readiness No-Holdout Dry Run

- Scope: `docs/readiness/PHASE_GATE_READINESS_PACKET.md`, `tests/reset/test_readiness_no_holdout_dry_run.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: prove readiness review can assemble archive evidence without reading or unlocking holdout data
- Decisions applied: `docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md`; `docs/readiness/PHASE_GATE_READINESS_PACKET.md`; `D-ROADMAP-001`
- Evidence collected: T33 acceptance tests passed (`3 passed`); full reset baseline `402 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T34 Phase-Gate Readiness Review
- Notes for next agent: readiness dry-run section uses archive-only artifacts, records holdout path/read/unlock as false, rejects restricted approval flags, and lists missing human approvals/protocols instead of claim conclusions.

### 2026-05-09 - T32 - Approval Boundary Checklist

- Scope: `docs/readiness/APPROVAL_BOUNDARY_CHECKLIST.md`, `tests/reset/test_approval_boundary_checklist.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record explicit human approval boundaries, blocked status, evidence prerequisites, and non-approval sources before no-holdout dry-run validation
- Decisions applied: `docs/ARCHITECTURE.md#human-approval-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions`; `D-ROADMAP-001`
- Evidence collected: T32 acceptance tests passed (`3 passed`); full reset baseline `399 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T33 Readiness No-Holdout Dry Run
- Notes for next agent: checklist confirms roadmap phases, readiness docs, archive evidence, passing tests, and review recommendations are not approval sources. Prompt and handoff must keep external side effects, holdout reads, live capital, live broker/exchange execution, and credentialed production deployment blocked.

### 2026-05-09 - T31 - Phase-Gate Readiness Packet Scaffold

- Scope: `docs/readiness/PHASE_GATE_READINESS_PACKET.md`, `tests/reset/test_phase_gate_readiness_packet.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: scaffold a phase-gate readiness packet that assembles evidence, missing controls, limitations, and approval prerequisites without granting approval
- Decisions applied: `D-ROADMAP-001`; `docs/readiness/PHASE_GATE_GAP_MATRIX.md`; `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`
- Evidence collected: T31 acceptance tests passed (`3 passed`); full reset baseline `396 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T32 Approval Boundary Checklist
- Notes for next agent: readiness packet references the Phase 8 gap matrix and Phase 7 review, lists missing controls, and explicitly records all restricted approval flags as false or blocked.

### 2026-05-08 - T30 - Archive Evidence Sufficiency Gap Matrix

- Scope: `docs/readiness/PHASE_GATE_GAP_MATRIX.md`, `docs/EVIDENCE_INDEX.md`, `tests/reset/test_phase_gate_readiness_gap_matrix.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: map current archive evidence to readiness controls and missing prerequisites before any future human phase-gate discussion
- Decisions applied: `D-ROADMAP-001`; `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`; `docs/research/REPRODUCIBILITY_MATRIX.md`
- Evidence collected: T30 acceptance tests passed (`3 passed`); full reset baseline `393 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T31 Phase-Gate Readiness Packet Scaffold
- Notes for next agent: T30 records complete, partial, and blocked readiness controls. Holdout, OOS/performance, live feed, broker/exchange, production, capital-ready, and phase-gate approvals remain blocked.

### 2026-05-08 - T29 - Archive Reproducibility Hardening Review

- Scope: `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `tests/reset/test_archive_reproducibility_review.py`
- Why this work happened: close Phase 7 with deep review, audit archive entry, roadmap evaluation, and next active phase opening
- Decisions applied: `D-ROADMAP-001`; `docs/research/REPRODUCIBILITY_MATRIX.md`; `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`
- Evidence collected: T29 acceptance tests passed (`3 passed`); full reset baseline `390 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T30 Archive Evidence Sufficiency Gap Matrix
- Notes for next agent: Phase 8 is readiness analysis only. It may identify evidence gaps before any future phase-gate discussion, but it must not read holdout data or approve OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate claim surfaces.

### 2026-05-08 - T28 - No-Claim Surface Regression Sweep

- Scope: `tests/reset/test_no_claim_roadmap_sweep.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `docs/EVIDENCE_INDEX.md`, `AGENT_NOTES.md`
- Why this work happened: prove active archive evidence, bridge, phase plan, prompt, and handoff surfaces do not silently open restricted claim paths before Phase 7 review
- Decisions applied: `D-ROADMAP-001`; `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`; `docs/bridges/hypothesis-backtest.md`
- Evidence collected: T28 acceptance tests passed (`3 passed`); full reset baseline `387 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T29 Archive Reproducibility Hardening Review
- Notes for next agent: no-claim sweep scans active docs and replayed packets for concrete approval flags, confirms phases 8 through 13 remain planned roadmap direction, and preserves prompt/handoff boundary language.

### 2026-05-08 - T27 - Evidence Hash Reproducibility Matrix

- Scope: `docs/research/REPRODUCIBILITY_MATRIX.md`, `docs/EVIDENCE_INDEX.md`, `tests/reset/test_reproducibility_matrix.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: record concrete hash categories across existing archive-only evidence packets and prove the matrix rejects missing, unresolved, invalid, or duplicate rows
- Decisions applied: `D-ROADMAP-001`; T26 archive packet replay contract
- Evidence collected: T27 acceptance tests passed (`3 passed`); full reset baseline `384 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T28 No-Claim Surface Regression Sweep
- Notes for next agent: the matrix is evidence bookkeeping only. It records candidate, dataset, code, policy, parameter, evidence artifact, and replay JSON hashes for the first and second archive packets without ranking hypotheses or opening holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approvals.

### 2026-05-08 - T26 - Archive Packet Replay Contract

- Scope: `src/entropy/evidence/archive_replay.py`, `src/entropy/evidence/__init__.py`, `tests/integration/test_archive_replay.py`, `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`
- Why this work happened: prove first and second archive-only evidence packets can be deterministically replayed from current fixtures and checked against stored packet/manifest artifacts
- Decisions applied: `D-ROADMAP-001`; T25 roadmap governance contract
- Evidence collected: T26 acceptance tests passed (`4 passed`); full reset baseline `381 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T27 Evidence Hash Reproducibility Matrix
- Notes for next agent: replay checks compare stable packet ids, candidate ids, no-claim labels, artifact references, deterministic packet hashes, and required manifest boundaries. They fail missing packet artifacts, dataset manifests, artifact references, or unresolved hash bindings without opening holdout, OOS/performance, live, broker/exchange, production, capital-ready, or phase-gate approvals.

### 2026-05-08 - T25 - Roadmap Governance Contract Opened

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, `docs/DECISION_LOG.md`
- Why this work happened: record the forward roadmap requested after T24, open the first active roadmap phase, and make phase boundaries autonomous rollover points
- Decisions applied: `D-ROADMAP-001`; `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`
- Evidence collected: T25 acceptance tests passed (`3 passed`); full reset baseline `377 passed, 20 skipped`; ruff check clean; ruff format clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: continue Phase 7 with T26 replay checks
- Notes for next agent: phases 8 through 13 are planned direction and may be promoted or rewritten by roadmap evaluation. After every active phase, deep-review, fix findings, validate, evaluate the roadmap, rewrite future phases/tasks if useful, open the next logical active phase, and continue automatically.

### 2026-05-07 - T24 - Archive Evidence Expansion Review

- Scope: `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `tests/reset/test_archive_evidence_expansion_review.py`
- Why this work happened: close the archive evidence expansion block with a review artifact, audit index row, validation record, limitations, and next human decision point
- Decisions applied: `docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md`; `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`
- Evidence collected: T24 acceptance tests passed (`3 passed`); full reset baseline `374 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: stop for human decision unless explicitly instructed to open a new research block or gate discussion
- Notes for next agent: archive evidence expansion is complete; holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved.

### 2026-05-07 - T23 - Second Research Evidence Packet

- Scope: `src/entropy/evidence/first_research_packet.py`, `docs/research/second-packet/RESEARCH_EVIDENCE_PACKET.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_second_research_packet.py`
- Why this work happened: generate a second deterministic archive-only research evidence packet from the second candidate, manifest, and evaluation outputs
- Decisions applied: `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`; `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`; T22 archive evaluation harness proof
- Evidence collected: T23 acceptance tests passed (`20 passed`); full reset baseline `371 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T24 Archive Evidence Expansion Review
- Notes for next agent: T23 parameterized packet id for the second packet and remains no-claim; no holdout, live, broker/exchange, production, capital-ready, phase-gate, or OOS/performance approval was introduced.

### 2026-05-07 - T22 - Second Archive Evaluation Harness Wiring

- Scope: `tests/integration/test_second_research_packet.py`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: prove repeat use of the archive-only evaluation harness on the second candidate without opening claim surfaces
- Decisions applied: `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`; `docs/audit/PHASE3_REVIEW.md`; T17 archive evaluation harness contract; T20-T21 second packet contracts
- Evidence collected: T22 acceptance tests passed (`17 passed`); full reset baseline `368 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T23 Second Research Evidence Packet
- Notes for next agent: T22 is heavy evidence; the second evaluation remains archive-only, refuses missing hashes, emits separated attribution streams, and does not produce OOS/performance, holdout, phase-gate, production, or capital-ready approval.

### 2026-05-07 - T21 - Second Archive Dataset Manifest and Hash Binding

- Scope: `docs/research/second-packet/DATASET_MANIFEST.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_second_research_packet.py`
- Why this work happened: bind the second research candidate to an archive-only dataset manifest with deterministic aggregate hashes and explicit holdout exclusion
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary`; T16 manifest binding contract; T20 second candidate packet contract
- Evidence collected: T21 acceptance tests passed (`14 passed`); full reset baseline `365 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T22 Second Archive Evaluation Harness Wiring
- Notes for next agent: T21 reused the archive manifest boundary for ETH fixture paths; holdout paths remain rejected and T20 candidate fields remain unchanged by dataset binding.

### 2026-05-07 - T20 - Second Research Candidate Registration Packet

- Scope: `src/entropy/research/candidate.py`, `src/entropy/research/__init__.py`, `docs/research/second-packet/CANDIDATE_PACKET.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_second_research_packet.py`
- Why this work happened: human approval after T19 requested more evidence, so Phase 6 opens archive-only expansion with a second distinct candidate
- Decisions applied: `docs/governance/research_firewall.md`; `docs/governance/experiment_readiness_gate.md`; `docs/governance/hypothesis_families.md`; `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`
- Evidence collected: T20 acceptance tests passed (`11 passed`); full reset baseline `362 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T21 Second Archive Dataset Manifest and Hash Binding
- Notes for next agent: T20 is candidate-only and not registered or evaluated; it uses Structure Levels, distinct from the first Volatility Compression candidate, and preserves all no-claim/no-live/no-holdout boundaries.

### 2026-05-07 - T19 - First Research Packet Review

- Scope: `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `tests/reset/test_first_research_packet_review.py`
- Why this work happened: close the first research evidence packet block with a review artifact, audit index row, validation record, limitations, and next human decision point
- Decisions applied: `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`; `docs/audit/RESET_REVIEW.md`
- Evidence collected: T19 acceptance tests passed (`3 passed`); full reset baseline `351 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: stop for human decision unless explicitly instructed to open a new research block or gate discussion
- Notes for next agent: first packet block is complete; holdout, live feeds, broker/exchange, production, capital-ready, phase-gate, and OOS/performance remain unapproved.

### 2026-05-07 - T18 - First Research Evidence Packet

- Scope: `src/entropy/evidence/first_research_packet.py`, `src/entropy/evidence/__init__.py`, `docs/research/first-packet/RESEARCH_EVIDENCE_PACKET.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: generate the first deterministic archive-only research evidence packet from the candidate, manifest, and archive evaluation outputs
- Decisions applied: `docs/audit/RESET_REVIEW.md`; `docs/EVIDENCE_INDEX.md`; T11 phase-gate packet boundary; T17 archive evaluation harness
- Evidence collected: T18 acceptance tests passed (`20 passed`); full reset baseline `348 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T19 First Research Packet Review
- Notes for next agent: T18 creates a concrete packet artifact but remains no-claim; it fails missing referenced artifacts or unresolved hashes and preserves blocked holdout, OOS/performance, phase-gate, production, capital-ready, live-feed, and broker/exchange approvals.

### 2026-05-07 - T17 - Archive Evaluation Harness Wiring

- Scope: `src/entropy/research/evaluation.py`, `src/entropy/research/__init__.py`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: wire the first candidate and archive dataset manifest through a deterministic archive-only evaluation surface that records leakage, SimBroker, attribution, and no-claim evidence
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/audit/PHASE3_REVIEW.md`; T09 SimBroker evidence; T10 attribution boundary evidence; T15-T16 first packet contracts
- Evidence collected: T17 acceptance tests passed (`17 passed`); full reset baseline `345 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T18 First Research Evidence Packet
- Notes for next agent: T17 is heavy evidence and remains archive-only; the harness refuses unresolved dataset/code/policy/parameter hashes, does not create an OOS label, and emits separated attribution streams with no performance conclusion.

### 2026-05-07 - T16 - Archive Dataset Manifest and Hash Binding

- Scope: `src/entropy/research/manifest.py`, `src/entropy/research/__init__.py`, `docs/research/first-packet/DATASET_MANIFEST.md`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: bind the first research candidate to an archive-only dataset manifest with deterministic aggregate hashes and explicit holdout exclusion
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#leakage-and-holdout-boundary`; T08 dataset/hash and holdout guard evidence; T15 candidate packet contract
- Evidence collected: T16 acceptance tests passed (`14 passed`); full reset baseline `342 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T17 Archive Evaluation Harness Wiring
- Notes for next agent: T16 added manifest binding only; it excludes holdout paths and preserves the T15 hypothesis text, family, and frozen parameters when replacing the candidate dataset hash placeholder with the aggregate archive dataset hash.

### 2026-05-07 - T15 - First Research Candidate Registration Packet

- Scope: `src/entropy/research/`, `docs/research/first-packet/CANDIDATE_PACKET.md`, `tests/integration/test_first_research_packet.py`
- Why this work happened: create the first narrow archive-only preregistration candidate for the Phase 5 research evidence packet block
- Decisions applied: `docs/governance/research_firewall.md`; `docs/governance/experiment_readiness_gate.md`; `docs/governance/hypothesis_families.md`; `docs/bridges/hypothesis-backtest.md`
- Evidence collected: T15 acceptance tests passed (`11 passed`); full reset baseline `339 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T16 Archive Dataset Manifest and Hash Binding
- Notes for next agent: T15 is candidate-only and not registered or evaluated; hash placeholders are present for dataset, code, policy, and parameter binding, and no holdout, live feed, broker/exchange, production, capital-ready, or OOS/performance surface is approved.

### 2026-05-07 - PHASE5 - First Research Evidence Packet Block Opened

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: human decision after T14 opened a new block focused on a concrete research result rather than a faster product MVP
- Decisions applied: `docs/audit/RESET_REVIEW.md`; `docs/core/PROTOCOL_SPEC.md`; `docs/governance/research_firewall.md`
- Evidence collected: documentation contract update; validation pending for first implementation task T15
- Follow-ups: start T15 First Research Candidate Registration Packet
- Notes for next agent: Phase 5 target is one registered, hash-bound, archive-only, leakage-checked research evidence packet; it must remain no-claim and cannot approve holdout, live feeds, broker integration, production, capital-ready, or OOS/performance labels.

### 2026-05-07 - T14 - Reset Strategy Closure Review

- Scope: `docs/audit/RESET_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `tests/reset/test_reset_closure.py`
- Why this work happened: close the reset implementation block with a strategy review, audit index update, and next-block recommendation grounded in current evidence
- Decisions applied: `docs/EVIDENCE_INDEX.md`; `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence collected: T14 acceptance tests passed (`3 passed`); full reset baseline `328 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: reset implementation awaits human decision after T14
- Notes for next agent: no open findings remain; no holdout, live feed, broker, production, capital-ready, or OOS/performance claim surface is approved by this closure.

### 2026-05-07 - T13 - Hypothesis Backtest Bridge Design

- Scope: `docs/bridges/hypothesis-backtest.md`, `tests/integration/test_hypothesis_bridge_design.py`
- Why this work happened: define a design-only bridge from research-assist hypothesis drafts to registered, hash-bound, leakage-safe evaluation objects without enabling autonomous strategy execution
- Decisions applied: `docs/governance/research_firewall.md`; `docs/core/CHARTER.md`
- Evidence collected: T13 acceptance tests passed (`3 passed`); full reset baseline `325 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T14 Reset Strategy Closure Review
- Notes for next agent: T13 is documentation-only; drafts remain research-only until human registration, hash binding, readiness, leakage, holdout, and no-claim boundaries are satisfied.

### 2026-05-07 - T12 - Trader Risk Audit Bridge Contracts

- Scope: `docs/bridges/trader-risk-audit.md`, `src/entropy/bridges/`, `tests/integration/test_trader_risk_bridge_contract.py`
- Why this work happened: define deterministic Core-side bridge contracts for Trader Risk Audit without opening live trading, order-blocking, or unsupported research-claim surfaces
- Decisions applied: `docs/ARCHITECTURE.md#human-approval-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#product-bridge-boundary`
- Evidence collected: T12 acceptance tests passed (`8 passed`); full reset baseline `322 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T13 Hypothesis Backtest Bridge Design
- Notes for next agent: T12 adds schemas and guard functions only; it does not integrate with product runtime code, broker APIs, holdout reads, or Core registry/gate writes.

### 2026-05-07 - PHASE3 - Evaluation Safety Boundary

- Scope: T08-T11, `docs/audit/PHASE3_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`
- Why this work happened: Phase 3 tasks completed and the reset loop required a phase-boundary review, archive/index update, and handoff checkpoint
- Decisions applied: `D-RESET-001`, `D-RESET-004`, `D-RESET-005`; `docs/ARCHITECTURE.md#minimum-viable-control-surface`
- Evidence collected: Phase 3 boundary review PASS; full reset baseline `314 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T12 Trader Risk Audit Bridge Contracts
- Notes for next agent: no phase-boundary findings were opened; Phase 4 begins with product bridge contracts and must preserve no-live/no-claim boundaries.

### 2026-05-07 - T11 - Phase-Gate Evidence Packet

- Scope: `src/entropy/evidence/`, `docs/EVIDENCE_INDEX.md`, `tests/integration/test_phase_gate_packet_reset.py`
- Why this work happened: produce a reset-era phase-gate packet that binds baseline, required approvals, blocked claims, and canonical evidence rows without using old workflow state as authority
- Decisions applied: `docs/ARCHITECTURE.md#minimum-viable-control-surface`
- Evidence collected: T11 acceptance tests passed (`3 passed`); focused phase-gate/evidence slice `9 passed`; full reset baseline `314 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: run Phase 3 boundary review before starting T12
- Notes for next agent: T11 added `build_phase_gate_evidence_packet`, which verifies evidence-index artifact/test references and renders all claim surfaces blocked unless gate evidence exists.

### 2026-05-07 - T10 - Attribution Stream Boundary Audit

- Scope: `src/entropy/attribution/`, `tests/unit/test_attribution_reset.py`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: verify P&L stream separation and prevent archive-only attribution output from implying unsupported performance conclusions
- Decisions applied: `docs/core/PROTOCOL_SPEC.md#nn-2-four-stream-pl-attribution-permanent`
- Evidence collected: T10 acceptance tests passed (`3 passed`); full reset baseline `311 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T11 Phase-Gate Evidence Packet
- Notes for next agent: T10 added an archive-only attribution payload helper that serializes streams a/b/c/d separately and omits performance/OOS/phase-gate claim fields.

### 2026-05-07 - T09 - SimBroker and Cost Surface Regression

- Scope: `src/entropy/simbroker/`, `tests/unit/test_simbroker_reset.py`
- Why this work happened: verify deterministic SimBroker fill logs, separated cost fields, and no live broker/exchange imports after reset
- Decisions applied: `docs/ARCHITECTURE.md#non-goals-v1`
- Evidence collected: T09 acceptance tests passed (`3 passed`); focused SimBroker slice `28 passed`; full reset baseline `308 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T10 Attribution Stream Boundary Audit
- Notes for next agent: T09 changed tests only; existing SimBroker runtime behavior already satisfied the reset contract.

### 2026-05-07 - T08 - Data and Leakage Gate Verification

- Scope: `src/entropy/data/`, `src/entropy/walkforward/`, `src/entropy/hashing/`, `tests/unit/test_data_leakage_reset.py`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: heavy Evaluation Safety task to verify deterministic dataset hashing, leakage-gated OOS labels, and holdout lock checks before read access
- Decisions applied: `docs/core/PROTOCOL_SPEC.md`; `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions`
- Evidence collected: T08 acceptance tests passed (`3 passed`); focused data/leakage/walk-forward slice `17 passed, 2 skipped`; full reset baseline `305 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T09 SimBroker and Cost Surface Regression
- Notes for next agent: T08 added explicit OOS label creation only from passing leakage reports and holdout read authorization that checks lock status before invoking a reader.

### 2026-05-07 - PHASE2 - Governance Integrity Boundary

- Scope: T04-T07, `docs/audit/PHASE2_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`
- Why this work happened: Phase 2 tasks completed and the reset loop required a phase-boundary review, archive/index update, and handoff checkpoint
- Decisions applied: `D-RESET-001`, `D-RESET-004`, `D-RESET-005`
- Evidence collected: Phase 2 boundary review PASS; full reset baseline `302 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T08 Data and Leakage Gate Verification
- Notes for next agent: no phase-boundary findings were opened.

### 2026-05-07 - T07 - Governance Approval Gate Audit

- Scope: `src/entropy/governance/`, `src/entropy/evidence/`, `tests/unit/test_governance_gate_reset.py`
- Why this work happened: verify human approval gates for phase gates, holdout access, and provider activation
- Decisions applied: `docs/ARCHITECTURE.md#human-approval-boundaries`; `docs/governance/governor.md`
- Evidence collected: T07 acceptance tests passed (`3 passed`); full reset baseline `302 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: run Phase 2 boundary review and start T08
- Notes for next agent: T07 added deterministic approval-gate helpers only; provider activation remains design-only unless future tasks approve a concrete provider.

### 2026-05-07 - T06 - No-Claim Report Boundary

- Scope: `src/entropy/evidence/`, `src/entropy/baseline/report.py`, `src/entropy/baseline/decision.py`, `tests/unit/test_no_claim_report_boundary.py`
- Why this work happened: verify report and decision surfaces remain archive-only/no-claim after reset and reject unsupported production, capital-ready, or OOS claim flags
- Decisions applied: `D-RESET-001`; `docs/legacy/CORE_LEGACY_SUMMARY.md#durable-boundaries`; `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions`
- Evidence collected: T06 acceptance tests passed (`5 passed`); full reset baseline `299 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T07 Governance Approval Gate Audit
- Notes for next agent: T06 added an `oos_label` boolean guard to report payloads and rejects it before any no-claim research decision can be built.

### 2026-05-07 - T05 - Evidence Index and Journal Sync

- Scope: `docs/EVIDENCE_INDEX.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/tasks.md`, `tests/reset/test_evidence_index_contract.py`
- Why this work happened: make reset-era evidence and handoff records executable and scoped so future work can retrieve proof without reading old workflow logs by default
- Decisions applied: `D-RESET-001`, `D-RESET-005`
- Evidence collected: T05 acceptance tests passed (`3 passed`); full reset baseline `294 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T06 No-Claim Report Boundary
- Notes for next agent: T05 removed legacy summary from active `Files:` task scope and enforces legacy references only through scoped `Context-Refs`.

### 2026-05-07 - T04 - Registry Append-Only Audit

- Scope: `src/entropy/registry/`, `migrations/`, `tests/unit/test_registry_append_only_reset.py`, `tests/integration/test_registry_append_only_reset.py`
- Why this work happened: verify reset-era append-only behavior for Trial Registry and governance event surfaces
- Decisions applied: `D-RESET-001`; `docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules`; `docs/core/PROTOCOL_SPEC.md`
- Evidence collected: T04 acceptance tests passed (`3 passed`); full reset baseline `291 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T05 Evidence Index and Journal Sync
- Notes for next agent: T04 added static mutation-path checks, missing-hash-before-DB guard coverage, and migration append-only checks. Runtime code already satisfied the tested contracts.

### 2026-05-07 - PHASE1 - Reset Foundation Boundary

- Scope: T01-T03, `docs/audit/PHASE1_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`
- Why this work happened: Phase 1 tasks completed and the reset loop required a phase-boundary deep review, archive/index update, and handoff checkpoint
- Decisions applied: `D-RESET-001`, `D-RESET-002`, `D-RESET-004`, `D-RESET-005`
- Evidence collected: Phase 1 boundary review PASS; full reset baseline `288 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean
- Follow-ups: start T04 Registry Append-Only Audit
- Notes for next agent: no phase-boundary findings were opened.

### 2026-05-07 - T03 - Reset Baseline Smoke Tests

- Scope: `src/entropy/tracing.py`, `src/entropy/metrics.py`, `docs/CODEX_PROMPT.md`, `tests/reset/test_reset_smoke.py`
- Why this work happened: close Phase 1 with smoke coverage for tracing, metrics stubs, CLI health, reset baseline documentation, and legacy context scoping
- Decisions applied: `D-RESET-001`, `D-RESET-005`
- Evidence collected: `tests/reset/test_reset_smoke.py` passed (`5 passed`); full reset baseline `288 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean
- Follow-ups: run Phase 1 boundary review and archive update, then start T04
- Notes for next agent: the reset smoke tests scan source AST for tracing-boundary drift and active tasks for old workflow archive references.

### 2026-05-07 - T02 - Product-Local CI Setup

- Scope: `.github/workflows/ci.yml`, `tests/reset/test_ci_contract.py`
- Why this work happened: verify the product-local GitHub Actions workflow under the reset task graph
- Decisions applied: `D-RESET-002`, `D-RESET-004`
- Evidence collected: `tests/reset/test_ci_contract.py` passed (`3 passed`); full reset baseline `283 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `git diff --check` clean
- Follow-ups: start T03 Reset Baseline Smoke Tests
- Notes for next agent: the CI workflow was already structurally aligned; this task added reset contract tests for the workflow.

### 2026-05-07 - T01 - Existing Project Baseline Skeleton

- Scope: `pyproject.toml`, `src/entropy/__init__.py`, `src/entropy/cli.py`, `tests/reset/test_reset_tooling.py`, `tests/reset/test_reset_skeleton.py`
- Why this work happened: complete the first reset foundation task by verifying Python 3.12 tooling, package import/version surface, and CLI help surface against current files
- Decisions applied: `D-RESET-001`, `D-RESET-002`
- Evidence collected: `tests/reset/test_reset_tooling.py tests/reset/test_reset_skeleton.py` passed (`3 passed`); full reset baseline `280 passed, 20 skipped`; ruff check clean; ruff format check clean; pyright `0 errors`; `entropy --help` exited 0; `git diff --check` clean
- Follow-ups: start T02 Product-Local CI Setup
- Notes for next agent: T01 required no product-code patch in this segment; current files already satisfied the reset contract.

### 2026-05-07 - RESET - Governance Reset Bootstrap

- Scope: `docs/`, `.github/workflows/ci.yml`, `.claude/commands/orchestrate.md`, `pyproject.toml`
- Why this work happened: rebuild the AI Workflow Playbook loop over existing Entropy Core code
- Decisions applied: `D-RESET-001`, `D-RESET-002`, `D-RESET-003`, `D-RESET-004`, `D-RESET-005`, `D-RESET-006`
- Evidence collected: structural sanity checks pending; Phase 1 audit pending
- Follow-ups: run `/orchestrate` to execute Phase 1 validation, then start T01 if validation passes
- Notes for next agent: old active workflow files are in `docs/legacy/old-workflow/2026-05-07/`; do not read them by default.
