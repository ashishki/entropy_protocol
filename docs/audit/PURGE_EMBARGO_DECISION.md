# PURGE_EMBARGO_DECISION
_Date: 2026-05-05 · Scope: P0.5-004 purge/embargo design decision_

## Decision

Decision: `METHODOLOGY_IMPLEMENTED_PACKET_REQUIRED`.

The current T18 splitter behavior remains acceptable for deterministic Phase 0
implementation tests: `embargo_bars = N consecutive bars immediately preceding
the first OOS bar`.

P0.6-003 implements method `PE-MAX-HORIZON-v1`, which binds the embargo length
to the strategy's feature lookback, label horizon, holding period, bar duration,
and execution lag. Phase 1 OOS claims remain blocked until registered leakage
and gate packets use this methodology with real trial parameters.

## Reviewed Artifacts

| Artifact | Role |
|----------|------|
| `entropy/walkforward/splitter.py` | Current split and embargo implementation |
| `tests/integration/test_walk_forward.py` | Current boundary and runner tests |
| `docs/spec.md` Walk-Forward Harness | Implementation-facing Phase 0 behavior |
| `docs/ARCHITECTURE.md` Phase 0 Run Path | Evaluation run path and leakage boundary |
| `docs/core/PROTOCOL_SPEC.md` Phase 0 / research questions | Canonical leakage and walk-forward context |
| `docs/audit/PHASE0_EXIT_GAP_REGISTER.md` EC-01 | Gate gap tied to registered leakage evidence |
| `docs/audit/FORMULA_EVIDENCE_DEBT.md` FD-07 | Purge/embargo debt ranking |

## Current Implementation

The splitter:

- requires UTC timestamps;
- requires strictly increasing bars;
- identifies the first OOS bar by `timestamp >= oos_start`;
- excludes exactly `embargo_bars` bars immediately before OOS from both IS and
  OOS;
- returns `is_window`, `embargo_window`, and `oos_window`;
- blocks IS feature leakage when `feature_computed_through >= is_cutoff`;
- records `embargo_bars` in walk-forward RunRecord metadata.

This is a clear and testable splitter. The derivation now lives in
`entropy/walkforward/embargo.py`.

## Why It Cannot Be Fully Accepted Yet

The current `N`-bar assumption does not answer:

- whether `N` covers the maximum feature lookback;
- whether `N` covers label horizon or target construction leakage;
- whether `N` covers typical holding period and order-lifecycle overlap;
- whether `N` differs for 1H, 4H, 1D, and weekly-derived features;
- whether irregular bars, missing bars, or mixed market calendars require a
  time-duration embargo instead of a pure bar-count embargo;
- whether multiple folds/rolling WFO should purge before and after test windows.

The protocol explicitly asks whether 4-year training / 1-year validation /
1-year test / annual roll and 4H-bar embargo assumptions are appropriate given
typical holding periods of 3-15 days. That open question cannot be closed by the
current implementation tests.

## Disposition Matrix

| Use case | Disposition | Rationale |
|----------|-------------|-----------|
| Unit/integration scaffold tests | Accepted | Current behavior is deterministic and covered by tests |
| Phase 0 implementation baseline | Accepted with label | T18 can remain complete as implementation foundation |
| Phase 0 gate leakage packet | Blocked pending packet design | Registered temporal-shuffling evidence must state why the embargo is sufficient |
| Phase 1 OOS performance claims | Blocked | No accepted derivation ties embargo length to strategy horizons |
| Phase 1 task planning | Allowed only with explicit blocker | Plans may reference current scaffold but must not call it final methodology |
| Production rolling WFO | Blocked | Single-split Phase 0 behavior is not a complete rolling WFO design |

## Required Design Inputs

Before this blocker can close, the project needs a purge/embargo design packet
with:

- bar frequency;
- maximum feature lookback;
- label horizon;
- expected holding-period range;
- order/fill latency assumption;
- calendar profile and missing-bar policy;
- whether embargo is counted in bars, time duration, or both;
- formula for minimum embargo length;
- per-trial preregistration of embargo parameters;
- examples for 4H and 1D data;
- leakage tests proving no OOS-derived feature, label, universe selection, or
  optimization state reaches IS.

## Implemented Closure Rule

P0.6-003 implements:

`embargo_duration = max(feature_lookback_duration, label_horizon_duration, max_expected_holding_period, execution_settlement_lag)`

Then convert to bars using the dataset calendar profile and require:

`embargo_bars = ceil(embargo_duration / bar_duration)`

Method ID: `PE-MAX-HORIZON-v1`.

This closes the methodology implementation gap. It does not close the Phase 0
gate by itself because registered leakage evidence still has to use concrete
trial parameters and produce a gate packet.

## Required Follow-Up

| Item | Required artifact |
|------|-------------------|
| Final purge/embargo formula | Future implementation/review task before Phase 1 OOS claims |
| Registered leakage packet | P0.5-009 gate packet must state the accepted embargo disposition |
| Architecture/spec reality sync | P0.5-008 must keep the temporary T18 assumption visible |
| Task graph | Future Phase 1 tasks must explicitly carry this blocker until closed |

## Decision Boundary

This decision does not require immediate code edits. It preserves the existing
splitter as a deterministic scaffold while blocking its use as final OOS
methodology. Phase 0 remains `NOT_APPROVED`, and Phase 1 remains stop-shipped.
