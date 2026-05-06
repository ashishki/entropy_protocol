# ARCH_MODEL — D-K Deep Review

**Audit cycle:** Cycle 5 — Phase 1D-K archive-only baseline deep review
**Date:** 2026-05-06
**Prior artifact:** `META_ANALYSIS.md`
**Status:** Draft — pending Spec Owner acceptance

## Component Model

| Component | File | Role | Boundary |
|---|---|---|---|
| P1D contract | `entropy/baseline/implementation.py` | Declares permitted formation-only implementation surface | No evaluation, portfolio, runtime escalation, or claims |
| P1E bounded baseline | `entropy/baseline/bounded.py` | Emits deterministic formation observations for registered skill families | No score, rank, weight, return, PnL, performance, or gate columns |
| P1F registration | `entropy/baseline/registration.py` | Binds code/policy/input/dataset/output hashes and prepares `TrialSpec` | No registry write and no evaluation execution |
| P1G evaluation config | `entropy/baseline/evaluation.py` | Defines split, window, leakage, SimBroker, stats, and gate requirements | Evaluation run needs explicit approval; holdout/live/broker/claims denied |
| P1H governed run | `entropy/baseline/governed.py` | Executes archive-only walk-forward mechanics and emits `RunRecord` metadata | No strategy performance computation or holdout |
| P1I report packet | `entropy/baseline/report.py` | Assembles deterministic report metadata and no-claim labels | No phase-gate evidence or capital-ready label |
| P1J/P1K packets | `entropy/baseline/decision.py` | Records no-holdout research decision and D-K closure packet | Deep review required before next workflow step |

## Data Flow

1. Phase 1A archive boundary and scaffold manifest define admissible formation
   data and holdout lock state.
2. Phase 1B/1C surfaces define the baseline schema and readiness checks.
3. P1D permits only formation-safe deterministic transforms.
4. P1E transforms formation input into per-family observation payloads.
5. P1F hashes source files, policy payload, input contract, dataset hashes, and
   P1E outputs into preregistration metadata.
6. P1G converts preregistration metadata into a governed evaluation config.
7. P1H runs walk-forward mechanics with approved metadata and leakage checklist.
8. P1I packages hashes, leakage status, run metadata, and report labels.
9. P1J/P1K close the archive-only block without opening holdout.

## Phase Dependencies

| Dependency | Verdict |
|---|---|
| P1E requires P1D approval | PASS |
| P1F requires complete P1E outputs | PASS |
| P1G requires no-claim preregistration | PASS |
| P1H requires `phase1g_evaluation_run_approval` | PASS |
| P1I requires matching trial and dataset hashes | PASS |
| P1J rejects reports with holdout/performance/gate evidence | PASS |
| P1K requires holdout gate closed for no-holdout closure | PASS |

## Integration Assumptions

- The P1H run is a mechanics run: it records IS/OOS bar counts and leakage
  status through the walk-forward runner, not tradable strategy returns.
- The P1I `stat_fields` value is currently an inventory inherited from P1G, not
  a set of computed statistics.
- P1F code hashing is intended to identify source contents independent of the
  caller's workspace path.

## Architecture Findings

### F-DK-001 — Source Path Identity Leaks Into Code Hash

Severity: P1

Initial review found that `_hash_source_files()` included `path.as_posix()`
directly in the hashed payload. If one caller passed
`entropy/baseline/bounded.py` and another passed the same file as an absolute
path, the same code contents produced different code hashes. DK-FIX-001 now
normalizes repository-local source identity before hashing.

Acceptance criterion: equivalent repository-local absolute and relative source
paths produce the same Phase 1F code hash, while missing files still fail.
Status: fixed, pending Spec Owner acceptance.

### F-DK-002 — Report Statistics Inventory Is Ambiguous

Severity: P2

Initial review found that P1G defined required statistic field names and P1I
recorded them as `stat_fields`. Because P1H intentionally avoids strategy
performance calculation, those fields are not computed statistics. DK-FIX-002
now records deterministic per-field no-computation status.

Acceptance criterion: P1I exposes deterministic per-field status metadata that
states the fields are not computed and not phase-gate evidence.
Status: fixed, pending Spec Owner acceptance.
