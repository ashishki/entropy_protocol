# Decision Log - Trader Risk Audit

Version: 1.3
Last updated: 2026-05-15

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
| D-007 | 2026-05-07 | Active | Phase 6 prioritizes demo artifacts, pilot intake, local workspace conventions, and validation evidence before more product expansion. | The startup pressure test found that market validation, not more core engineering, is now the binding risk. | `STARTUP_PRESSURE_TEST_RU.md` and `docs/tasks.md#t21-demo-audit-pack` | none |
| D-008 | 2026-05-07 | Active | Telegram may be explored only as pilot intake/delivery after an ADR; it must not become signal analytics, broker integration, order blocking, or advice. | Telegram is a useful trader workflow surface, but unconstrained Telegram scope would contaminate the current audit wedge. | `docs/tasks.md#t24-telegram-intake-adr` | none |
| D-009 | 2026-05-09 | Active | Read-only exchange import may be planned as a local post-trade ingestion path under accepted ADR-002, starting with Binance/Bybit historical fills only. | Reduces user friction while preserving no-trading, no-withdrawal, no-transfer, no-live-control boundaries. | `docs/adr/ADR-002-read-only-exchange-import.md` and `docs/EXCHANGE_API_IMPORT_PLAN_RU.md` | Narrows D-006: exchange read-only import is allowed, exchange control remains forbidden. |
| D-010 | 2026-05-14 | Active | Automate the pilot validation loop locally before building hosted SaaS: intake profiler, structured rule builder, one-click runner, preview/CTA, and evidence dashboard. Real read-only fetching remains conditional on CSV friction evidence. | Phase 16 proved artifact quality but not repeated customer validation. The next bottleneck is reducing manual setup labor and measuring hypothesis evidence without adding hosted scope too early. | `docs/AUTOMATED_PILOT_ROADMAP.md` and `docs/tasks.md#automated-pilot-priority` | Extends D-007 and narrows D-009 routing: import remains allowed, but real fetching waits for T93/T94. |
| D-011 | 2026-05-15 | Active | After T93 defer, active work moves to an open-source audit case bank, multi-case report-quality loop, and private-pilot readiness. Core is paused. | The operator wants more real/open-source data and validated report artifacts before going to warm prospects. This reduces cherry-pick risk and avoids spending on Core/SaaS before report validity is proven. | `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md` and `docs/tasks.md#open-source-audit-validation-priority` | Extends D-010; keeps D-009 real fetching blocked until new evidence reopens T93/T94. |
| D-012 | 2026-05-15 | Active | Phase 23 case selection must include positive, limitation/reject, and edge/schema coverage where available, and must label public/open-source packs as artifact-quality evidence only. | Prevents a case bank made only from flattering reports and keeps demo/report validity evidence separate from paid-pilot, PMF, and customer evidence. | `docs/OPEN_SOURCE_CASE_BANK.md` | Implements D-011 source-selection discipline. |

## Retrieval Notes

- Read this file before revisiting architecture, runtime tier, capability profiles, rule semantics, P&L attribution, Telegram behavior, live integration boundaries, or pilot automation routing.
- If a task has `Context-Refs`, prefer those entries over scanning this file top-to-bottom.
