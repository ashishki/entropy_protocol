# Core V2 Evidence Completeness Matrix

Status: Active Phase 31 evidence matrix
Date: 2026-05-31
Scope: T123-T136 internal Core V2 evidence only

This matrix summarizes Core V2 evidence coverage. It records internal evidence
gaps as follow-ups only. It does not claim product readiness, hosted service
readiness, live execution readiness, holdout readiness, external compliance
readiness, production readiness, capital readiness, investment advice, or
OOS/performance confirmation.

## Task Evidence

| Task | Evidence artifacts | Validation |
|------|--------------------|------------|
| T123 Core V2 Roadmap Activation | `docs/CORE_V2_ROADMAP.md`; `docs/tasks.md`; `docs/CODEX_PROMPT.md`; `docs/EVIDENCE_INDEX.md` | manual docs review; `git diff --check` |
| T124 Schema Evolution Policy Contract | `docs/core/SCHEMA_EVOLUTION_POLICY.md`; `tests/reset/test_core_v2_schema_evolution_policy.py` | `.venv/bin/python -m pytest -q tests/reset/test_core_v2_schema_evolution_policy.py` |
| T125 Schema Compatibility Primitives | `src/entropy/artifacts/schema_compatibility.py`; `tests/unit/test_schema_compatibility.py` | `.venv/bin/python -m pytest -q tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` |
| T126 Schema Evolution Foundations Review | `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md`; `docs/audit/AUDIT_INDEX.md` | manual review PASS; Stop-Ship 0, P0 0, P1 0 |
| T127 Evidence Lookup Policy Contract | `docs/core/EVIDENCE_LOOKUP_POLICY.md`; `tests/reset/test_evidence_lookup_policy.py` | `.venv/bin/python -m pytest -q tests/reset/test_evidence_lookup_policy.py tests/reset/test_core_v2_schema_evolution_policy.py tests/unit/test_schema_compatibility.py` |
| T128 Local Evidence Lookup Primitives | `src/entropy/artifacts/evidence_lookup.py`; `tests/unit/test_evidence_lookup.py` | `.venv/bin/python -m pytest -q tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` |
| T129 Evidence Inspect Alignment | `src/entropy/artifacts/evidence_lookup.py`; `tests/unit/test_evidence_lookup.py` | `.venv/bin/python -m pytest -q tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` |
| T130 Evidence Query Hardening Review | `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md`; `docs/audit/AUDIT_INDEX.md` | manual review PASS; Stop-Ship 0, P0 0, P1 0 |
| T131 Product Bridge Adoption Policy | `docs/core/PRODUCT_BRIDGE_ADOPTION_POLICY.md`; `tests/reset/test_product_bridge_adoption_policy.py` | `.venv/bin/python -m pytest -q tests/reset/test_product_bridge_adoption_policy.py tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` |
| T132 Product Bridge Readiness Checks | `src/entropy/artifacts/product_bridge_adoption.py`; `tests/unit/test_product_bridge_adoption.py` | `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_adoption.py tests/reset/test_product_bridge_adoption_policy.py tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` |
| T133 Product Bridge Adoption Fixtures | `tests/fixtures/artifacts/adoption/`; `tests/unit/test_product_bridge_adoption.py` | `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_adoption.py tests/reset/test_product_bridge_adoption_policy.py tests/unit/test_evidence_lookup.py tests/reset/test_evidence_lookup_policy.py tests/unit/test_schema_compatibility.py tests/reset/test_core_v2_schema_evolution_policy.py` |
| T134 Product Bridge Adoption Readiness Review | `docs/audit/PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md`; `docs/audit/AUDIT_INDEX.md` | manual review PASS; Stop-Ship 0, P0 0, P1 0 |
| T135 V2 Kernel Foundation Inventory | `docs/core/V2_KERNEL_FOUNDATION_INVENTORY.md`; `tests/reset/test_v2_kernel_review_inventory.py` | `.venv/bin/python -m pytest -q tests/reset/test_v2_kernel_review_inventory.py tests/unit/test_product_bridge_adoption.py tests/reset/test_product_bridge_adoption_policy.py tests/reset/test_reset_smoke.py tests/reset/test_no_claim_roadmap_sweep.py tests/reset/test_live_feed_boundary_contract.py tests/reset/test_broker_sandbox_boundary_contract.py` |
| T136 Restricted Surface Regression Sweep V2 | `tests/reset/test_v2_restricted_surface_sweep.py` | `.venv/bin/python -m pytest -q tests/reset/test_v2_restricted_surface_sweep.py tests/reset/test_v2_kernel_review_inventory.py tests/reset/test_no_claim_roadmap_sweep.py tests/reset/test_live_feed_boundary_contract.py tests/reset/test_broker_sandbox_boundary_contract.py` |

## Phase Evidence

| Phase | Review artifact | Evidence index rows |
|-------|-----------------|---------------------|
| 28 Schema Evolution Foundations | `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md` | T123, T124, T125, T126 |
| 29 Evidence Query Hardening | `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md` | T127, T128, T129-T130 |
| 30 Product Bridge Adoption Readiness | `docs/audit/PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md` | T131, T132, T133, T134 |
| 31 V2 Internal Kernel Review | `docs/audit/V2_INTERNAL_KERNEL_REVIEW.md` planned for T138 | T135, T136, T137, T138 planned |

## Evidence Gaps

| Gap | Classification | Follow-up |
|-----|----------------|-----------|
| Phase 31 final review is not complete yet | internal review follow-up, not product readiness | T138 must review the Phase 31 inventory, restricted-surface sweep, and this matrix. |
| Full-suite validation has not been rerun after every V2 task | internal validation follow-up, not hosted service readiness | T138 should decide whether full pytest/ruff/format/pyright coverage is needed before next phase. |
| V2 evidence is local-doc/test evidence only | internal evidence limitation, not live/holdout/capital readiness | Future scope expansion still requires explicit human approval and any required ADR. |

## Blocked Interpretation

The matrix rows above are evidence of internal Core kernel work. They are not
evidence for public SDK availability, hosted service readiness, runtime RAG,
product runtime ownership, product report authorship, external delivery
approval, live execution, holdout access, broker/exchange execution, production
credential use, external compliance certification, production readiness,
capital readiness, investment advice, or OOS/performance confirmation.
