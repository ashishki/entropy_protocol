# INVARIANTS — D-K Deep Review

**Audit cycle:** Cycle 5 — Phase 1D-K archive-only baseline deep review
**Date:** 2026-05-06
**Prior artifact:** `ARCH_MODEL.md`
**Status:** Draft — pending Spec Owner acceptance

## Stable Invariants

| INV-ID | Invariant | Active scope | Verdict |
|---|---|---|---|
| DK-INV-001 | D-K does not unlock Phase 1 trading, live feeds, broker integration, holdout, production, capital-ready status, or live capital | All D-K phases | PASS |
| DK-INV-002 | P1D permits only formation-only implementation contract checks until P1E approval | P1D/P1E | PASS |
| DK-INV-003 | P1E outputs cannot include score, rank, weight, position, return, PnL, performance, or gate fields | P1E+ | PASS |
| DK-INV-004 | P1F requires all registered skill families and all no-claim outputs before hash binding | P1F+ | PASS |
| DK-INV-005 | P1F code hash must be reproducible for the same repository source contents | P1F+ | PASS |
| DK-INV-006 | P1F preregistration surface cannot write to Trial Registry or permit evaluation/gate claims | P1F+ | PASS |
| DK-INV-007 | P1G denies holdout, live feed, broker, performance conclusion, phase-gate, production, and capital-ready requests | P1G+ | PASS |
| DK-INV-008 | P1H requires explicit evaluation-run approval and remains archive-only | P1H+ | PASS |
| DK-INV-009 | P1H emits metadata and leakage status, not performance conclusions | P1H+ | PASS |
| DK-INV-010 | P1I report fields must distinguish required-stat inventory from computed statistics | P1I+ | PASS |
| DK-INV-011 | P1J/P1K cannot open holdout without explicit holdout gate approval | P1J/P1K | PASS |
| DK-INV-012 | Audit prompts must identify the current review cycle and work state | Audit pipeline | PASS |

## Core Spec Invariants Still Preserved

| Core invariant | D-K interaction | Verdict |
|---|---|---|
| NN-1 gross leverage <= 1.0 | No positions or weights are emitted | PASS |
| NN-2 four-stream P&L separation | No P&L stream is computed or blended | PASS |
| NN-3 evaluation engine first | P1H uses walk-forward mechanics and no OOS claim label | PASS |
| NN-4 sequential rollout | Holdout/production/capital phases remain blocked | PASS |
| NN-5 Trial Registry + multiplicity | P1F prepares `TrialSpec`; P1G records family accounting | PASS |
| NN-6 stop-loss parameters | No short-side or stop-loss logic is introduced | PASS |

## Formula And Boundary Flags

| INV-ID | Flag | Reason |
|---|---|---|
| DK-INV-005 | FIXED | P1F source identity is normalized before hash payload construction |
| DK-INV-010 | FIXED | Report packet lists deterministic per-field no-computation status |
| DK-INV-012 | FIXED | Prompt headers identify Cycle 5 D-K context |
