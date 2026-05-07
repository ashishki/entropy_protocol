# Decision Log - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-07

This file is a retrieval surface for important decisions. It is not the source of truth. If a row conflicts with a canonical document, the canonical document wins and this file must be corrected.

---

## Rules

- Keep entries short and link to the authoritative document or section.
- Record why a decision was made and what it replaced.
- Update this file when architecture, runtime, governance, profiles, or major implementation direction changes.
- Mark superseded decisions explicitly instead of deleting them.

## Decision Index

| ID | Date | Status | Decision | Why it matters | Canonical source | Supersedes |
|----|------|--------|----------|----------------|------------------|------------|
| D-001 | 2026-05-07 | Active | Use workflow orchestration with deterministic subsystems for v1. | Captures the local audit sequence and human gates without adding runtime agency. | `docs/ARCHITECTURE.md#solution-shape` | none |
| D-002 | 2026-05-07 | Active | CI is part of Phase 1 and must run ruff check, ruff format check, and pytest. | Prevents implementation from starting without an executable quality gate. | `docs/ARCHITECTURE.md#tech-stack` and `.github/workflows/ci.yml` | none |
| D-003 | 2026-05-07 | Active | Trade imports start with supported local CSV fixtures and deterministic normalization. | Avoids live broker scope and keeps first pilots local and reproducible. | `docs/ARCHITECTURE.md#data-flow-primary-audit-path` | none |
| D-004 | 2026-05-07 | Active | Capability profiles are OFF for RAG, Tool-Use, Agentic, Planning, and Compliance. | Keeps v1 profile governance proportional; turning any profile on later requires ADR. | `docs/ARCHITECTURE.md#capability-profiles` | none |
| D-005 | 2026-05-07 | Active | Violation P&L attribution uses heavy-task evidence. | Incorrect attribution is the highest trust risk; golden fixtures and evidence indexing are required. | `docs/tasks.md#t12-violation-pl-attribution` | none |
| D-006 | 2026-05-07 | Active | No live broker APIs, order blocking, or capital-control path in v1. | Protects the product wedge and keeps runtime tier at T0. | `docs/ARCHITECTURE.md#non-goals-v1` and `docs/IMPLEMENTATION_CONTRACT.md#forbidden-actions` | none |

## Retrieval Notes

- Read this file before revisiting architecture, runtime tier, capability profiles, rule semantics, P&L attribution, or live integration boundaries.
- If a task has `Context-Refs`, prefer those entries over scanning this file top-to-bottom.
