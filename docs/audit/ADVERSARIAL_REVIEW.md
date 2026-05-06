# ADVERSARIAL_REVIEW — D-K Deep Review

**Audit cycle:** Cycle 5 — Phase 1D-K archive-only baseline deep review
**Date:** 2026-05-06
**Prior artifacts:** `ARCH_MODEL.md`, `INVARIANTS.md`, `DRIFT_REPORT.md`
**Status:** Draft — pending Spec Owner acceptance

## Executive Summary

Challenges assessed: 6 categories. Critical findings: 0. P1 findings: 1. P2
findings: 2.

The D-K implementation preserves the archive-only/no-claim boundary. The
adversarial concerns were narrower than prior formula-level Phase 0 reviews:
hash reproducibility, report-field semantics, and stale prompt metadata. All
three are fixed in the current working tree. None of these findings permits
performance claims or opens holdout.

## A — Formula Derivation Challenges

The prompt asks for full derivations for Sharpe CI, FLAM breadth, K4,
Harvey-Liu, and K3. Current core docs already carry the corrected formula
surface:

- `PROTOCOL_SPEC.md` and `GLOSSARY.md` state `CI-SR-ACF-v1` and explicitly note
  that at 15 months a 0.30 Sharpe has 68% CI half-width near 0.91, not
  0.15-0.20.
- `CHARTER.md` and `GLOSSARY.md` state long raw breadth as 120/year, not 240.
- `GLOSSARY.md` defines `HL-HB-v1` Holm-Bonferroni reporting inputs and outputs.

D-K does not change these formulas or create gate-level formula claims.

## B — State Machine Stress Tests

D-K does not implement P1/P3/P4 exposure transitions, Growth RBE activation, RDL
promotion, or P4 recalibration. The tested D-K state machine is:

| Transition | Deterministic? | Verdict |
|---|---|---|
| P1D contract to P1E implementation | Yes, requires P1E approval | PASS |
| P1F preregistration to P1G config | Yes, requires no-claim preregistration | PASS |
| P1G config to P1H run | Yes, requires `phase1g_evaluation_run_approval` | PASS |
| P1I report to P1J decision | Yes, rejects holdout/performance/gate evidence | PASS |
| P1J decision to P1K no-holdout closure | Yes, requires holdout gate closed | PASS |

## C — Kill Criterion Calibration Audit

D-K does not evaluate kill criteria. It emits no net Sharpe, drawdown, Calmar,
K3, K4, K5, or SimBroker drift verdict. Any consumer treating P1H/P1I metadata
as kill evidence would violate the report labels and no-claim flags.

## D — Evaluation vs Execution Divergence

The main divergence point was not execution logic but reproducibility metadata.
P1F could produce different code hashes for the same file contents if called
with absolute versus relative source paths. DK-FIX-001 closes this with
repo-local source identity normalization. Finding: F-DK-001.

## E — Behavioral Integrity Gaps

The report packet previously depended on readers understanding that
`stat_fields` was an inventory, not results. DK-FIX-002 now records explicit
per-field `not_computed_no_performance_conclusion` status. Finding: F-DK-002.

## F — Open Question Resolution Review

| Q-ID | Question summary | Addressed in spec/code? | Completeness | Phase gate blocked? |
|---|---|---|---|---|
| DK-Q1 | Does D-K open holdout? | Yes, P1J/P1K keep it closed | Complete | No; holdout remains blocked |
| DK-Q2 | Is P1H performance evidence? | Yes, flags say no | Complete | No |
| DK-Q3 | Are report statistics computed? | Yes; explicit no-computation status | Complete | No |
| DK-Q4 | Is code hash path-stable? | Yes | Complete | No |
| DK-Q5 | Are audit prompts current? | Yes | Complete | No |

## Phase Gate Impact

D-K remains archive-only and not phase-gate evidence. F-DK-001, F-DK-002, and
F-DK-003 are fixed in the current working tree, pending Spec Owner acceptance of
the review and fix closure.
