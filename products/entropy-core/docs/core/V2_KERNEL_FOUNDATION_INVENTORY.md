# Core V2 Kernel Foundation Inventory

Status: Active Phase 31 inventory
Date: 2026-05-29
Scope: internal Entropy Core kernel only

This inventory records what Core V2 has added so far and what remains outside
the kernel boundary. It is an internal review artifact, not a product launch,
hosted service plan, external delivery approval, or compliance claim.

## Foundations

| Phase | Foundation | Core-owned primitives | Evidence |
|-------|------------|-----------------------|----------|
| 28 | Schema Evolution Foundations | schema evolution policy; deterministic schema compatibility classification; schema evolution review | `docs/core/SCHEMA_EVOLUTION_POLICY.md`; `src/entropy/artifacts/schema_compatibility.py`; `docs/audit/SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md` |
| 29 | Evidence Query Hardening | local deterministic evidence-index lookup; packet evidence-ref alignment; evidence query review | `docs/core/EVIDENCE_LOOKUP_POLICY.md`; `src/entropy/artifacts/evidence_lookup.py`; `docs/audit/EVIDENCE_QUERY_HARDENING_REVIEW.md` |
| 30 | Product Bridge Adoption Readiness | product bridge adoption policy; readiness metadata validation; synthetic adoption fixtures; adoption readiness review | `docs/core/PRODUCT_BRIDGE_ADOPTION_POLICY.md`; `src/entropy/artifacts/product_bridge_adoption.py`; `tests/fixtures/artifacts/adoption/`; `docs/audit/PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md` |

## Internal Kernel Boundary

Core V2 currently owns deterministic local primitives for artifact schema
evolution, local evidence lookup, packet evidence reference inspection, product
bridge profile readiness metadata, and synthetic fixture validation.

Core V2 does not own:

- public SDK delivery;
- hosted service, SaaS, auth/RBAC, SSO, or tenant isolation;
- runtime RAG, embeddings, hosted search, or public API behavior;
- product runtime execution;
- product report authorship;
- product workspace edits;
- external delivery approval;
- holdout access or holdout unlocks;
- live feeds by default;
- broker/exchange execution;
- production credentials;
- external compliance certification or enterprise SLA claims;
- live capital or capital-ready labels;
- production, investment-advice, or unsupported OOS/performance claims.

## Evidence Gaps

| Gap | Current classification | Follow-up |
|-----|------------------------|-----------|
| Cross-phase restricted-surface sweep | internal evidence gap, not a product-readiness blocker | T136 should add regression checks across V2 docs and primitives. |
| V2 evidence completeness matrix | internal evidence gap, not hosted/live/holdout/capital readiness evidence | T137 should map T123-T136 to evidence rows, review docs, and validation commands. |
| Final V2 internal kernel review | internal review gap, not public SDK or compliance readiness evidence | T138 should decide whether further V2 work can continue autonomously or requires a human gate. |

## Non-Readiness Statement

This inventory does not claim product readiness, hosted service readiness, live
execution readiness, holdout readiness, external compliance readiness,
production readiness, capital readiness, investment advice, or OOS/performance
confirmation. Any future work that needs those surfaces must stop for explicit
human approval and any required ADR before implementation.
