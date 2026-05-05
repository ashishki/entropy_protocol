# Invariants — Cycle 4 Post-Phase-1A

Date: 2026-05-05
Step: 3
Status: `COMPLETE`

## Core Invariants

| ID | Invariant | Status | Check mechanism |
|---|---|---|---|
| INV-C4-001 | No Phase 1 evaluation/trading starts without explicit gate approval | Active | Current-state docs, task graph, review report |
| INV-C4-002 | Archive holdout remains locked until a separate approved gate | Active | Registration boundary, scaffold authorization tests |
| INV-C4-003 | No OOS/performance claim without walk-forward harness and approved phase context | Active | Reports and no-claim labels |
| INV-C4-004 | Scaffold placeholders must remain non-trading and non-alpha | Active | Scaffold packet and tests |
| INV-C4-005 | Mechanics probes must not emit strategy performance metric fields | Active | Probe packet and tests |
| INV-C4-006 | Python remains Phase 0/1 control plane; non-Python requires benchmark + ADR + approval | Active | Architecture, implementation contract, P1A-006/P1A-007 |
| INV-C4-007 | Large benchmark intermediates use Parquet/Arrow-compatible data plane, not PostgreSQL bulk storage | Active | P1A-007 contract |
| INV-C4-008 | Growth/RBE remains inactive before approved activation path | Active | Protocol spec, Phase 1A entry contract |
| INV-C4-009 | RDL remains dormant/scaffolding-only through Phase 0-1 | Active | Protocol spec, glossary, Phase 1A entry contract |
| INV-C4-010 | Audit prompts must describe the current cycle and avoid stale pre-development assumptions | Active | P1A-011 refresh packet |
| INV-C4-011 | Archived audit history is not loaded by default | Active | Audit README/index and prompt context |

## Phase Gate Invariants

| Gate | Current status | Invariant |
|---|---|---|
| Live/streaming Phase 0 | Not approved | Archive-only evidence does not imply live feed readiness |
| Full Phase 1 evaluation | Not approved | Phase 1A scaffold/probe closure does not imply evaluation approval |
| Holdout unlock | Not approved | No task may read holdout without explicit gate |
| Runtime escalation | Not approved | No Rust/Go/native/second service without escalation packet |

## Invariant Finding

| ID | Severity | Finding | Impact |
|---|---|---|
| F-C4-001 | P2 | Current-state prose drift in `ARCHITECTURE.md`/`spec.md` can confuse future audit or implementation sessions. | Documentation drift only; no evidence of executable boundary violation. |

## Step Verdict

Verdict: `INVARIANTS_EXTRACTED_NO_P0_P1`.

Proceed to `PROMPT_3_DRIFT_GUARD.md`.
