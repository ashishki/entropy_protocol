# ARCH_REPORT — Phase 7 Boundary Review
_Date: 2026-05-03 · Scope: Phase 6/7 implementation surfaces_

## Architecture Summary

Phase 6 adds the SimBroker surface:

- deterministic cost model
- fill engine constrained to current-bar high/low
- bid/ask provider abstraction with no live integration

Phase 7 adds the walk-forward surface:

- strict time-based IS/OOS splitter
- machine-checkable leakage checklist
- walk-forward runner with RunRecord persistence

## Architecture Findings

### P0

_None open._

### P1

_None open._

### P2

_None open._

## Remediated Review Finding

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| WF-P1-01 | P1 | T19's checklist could return PASS with omitted detector callbacks, allowing T20 to pass a leakage gate without detector-backed checks. | Missing detector callbacks now FAIL; T20 tests use explicit clean detector callbacks and verify failed checks block OOS. |

## Boundary Checks

| Boundary | Assessment |
|----------|------------|
| SimBroker live systems | No live broker API, order routing, or partial-fill simulation introduced. |
| Cost arithmetic | T15 formulas isolated in `entropy/simbroker/costs.py`; T16/T17 did not alter arithmetic. |
| Fill no-lookahead | T16 uses current bar timestamp/high/low only; tests guard against future access. |
| IS/OOS separation | T18 splitter enforces timestamp ordering, embargo exclusion, and feature cutoff checks. |
| Leakage gate | T19 now requires explicit detector evidence for PASS; T20 blocks OOS before `run_oos()` when missing/non-PASS. |
| Persistence | T20 writes complete `RunRecord` metadata to `runs` with ORM INSERT-only behavior. |

## Architecture Decision

Phase 7 architecture is acceptable for the next governance step. Direct Phase 8
implementation remains blocked by formula-governance scope, not by a discovered
Phase 7 architecture defect.
