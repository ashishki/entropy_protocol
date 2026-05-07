# Core Legacy Summary

Version: 1.0
Date: 2026-05-07
Status: retrieval summary for the governance reset

This summary preserves durable context from the pre-reset Entropy Core workflow. It is not authority. Canonical authority after the reset is `docs/ARCHITECTURE.md`, `docs/spec.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/IMPLEMENTATION_CONTRACT.md`, ADRs, code, tests, and audit reports.

## Current Baseline Before Reset

- Last recorded verification: `277 passed, 20 skipped`.
- Last recorded lint/type state: ruff passed; pyright 0 errors.
- Current code package: `src/entropy/`.
- Current tests: `tests/`.
- Current migrations: `migrations/`.
- Python runtime intent: Python 3.12.

## Durable Product Direction

Entropy Core is the governed systematic research engine and deterministic audit primitive layer for the Entropy Protocol product portfolio. It must continue into a usable local research MVP without weakening preregistration, leakage controls, append-only evidence, human phase gates, or no-live-capital boundaries.

## Durable Boundaries

- Holdout remains locked unless an explicit human gate opens it.
- No live broker or exchange integration in v1.
- No live feeds by default.
- No live capital, order blocking, production labels, or capital-ready labels.
- No OOS or performance claim unless protocol gates and leakage evidence explicitly authorize it.
- No autonomous AI trading or AI-generated strategies entering evaluation without human registration.
- Runtime application logic remains deterministic; AI is development/review assistance only.
- Any Rust, Go, C/C++, native extension, FFI, or second runtime service requires benchmark evidence, ADR, CI/toolchain plan, rollback plan, and human approval.

## Durable Decisions To Preserve

| ID | Summary | Source before reset |
|----|---------|---------------------|
| D-027 | Evidence mode was archive-only; live/streaming claims and OOS/performance claims were not authorized. | old `docs/DECISION_LOG.md` |
| D-050 | Phase 1 D-K roadmap was recorded but was not blanket approval for future phases. | old `docs/DECISION_LOG.md` |
| D-051 | P1D implementation contract completed and light-reviewed. | old `docs/DECISION_LOG.md` |
| D-052 | P1E bounded formation-only baseline logic completed. | old `docs/DECISION_LOG.md` |
| D-053 | P1F baseline hash binding and preregistration surface completed. | old `docs/DECISION_LOG.md` |
| D-054 | P1G/P1H governed config and archive-only run metadata completed. | old `docs/DECISION_LOG.md` |
| D-055 | P1I/P1J/P1K report, decision, and no-holdout closure completed. | old `docs/DECISION_LOG.md` |
| D-056 | D-K deep review and fix closure completed; no holdout, production, live, broker, Growth/RDL/RBE, or performance claim was approved. | old `docs/DECISION_LOG.md` |
| D-057 | Product direction split into Entropy Core, Trader Risk Audit, and Signal Analytics Sandbox. | root portfolio docs |
| D-058 | Entropy Core implementation was isolated into `products/entropy-core/`. | old `docs/DECISION_LOG.md` |

## Active Code Surfaces

- `src/entropy/registry/`: Trial Registry and readiness/admission surfaces.
- `src/entropy/simbroker/`: deterministic execution simulation surfaces.
- `src/entropy/walkforward/`: IS/OOS split, embargo, leakage, and walk-forward orchestration surfaces.
- `src/entropy/attribution/`: P&L stream and attribution surfaces.
- `src/entropy/governance/`: governance state machine surfaces.
- `src/entropy/evidence/`: evidence/report surfaces.
- `src/entropy/baseline/`: D-K archive-only baseline surfaces.
- `migrations/`: Alembic schema history.

## Historical Context Location

Old active workflow files were moved to `docs/legacy/old-workflow/2026-05-07/`. Existing archival evidence under `docs/archive/` and `docs/audit/archive/` remains in place and should be read only when a task explicitly needs historical proof.
