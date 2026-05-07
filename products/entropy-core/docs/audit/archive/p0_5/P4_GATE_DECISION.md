# P4_GATE_DECISION
_Date: 2026-05-05 · Scope: P0.5-005 P4 labeler gate decision_

## Decision

Decision: `IMPLEMENT_AND_EVIDENCE_P4_BEFORE_PHASE1`.

Do not revise the Phase 0 exit criterion yet. The deterministic `P4-RBL-v1`
algorithm is already specified in the canonical docs, so the correct next path
is to implement the labeler and produce the required historical label evidence.

Phase 0 remains `NOT_APPROVED` until P4 evidence covers >=3 years of 1D data on
>=15 of 20 target assets, or until a later charter-level review explicitly
changes that criterion.

## Reviewed Artifacts

| Artifact | Role |
|----------|------|
| `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Deterministic P4 Protocol | Canonical `P4-RBL-v1` algorithm |
| `products/entropy-core/docs/core/CHARTER.md` Phase 0 exit criteria / P4 | Gate requirement and governance role |
| `products/entropy-core/docs/core/GLOSSARY.md` Regime Signal Hierarchy | P4 semantics and state names |
| `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` EC-05 | Current P4 gate gap |
| `products/entropy-core/docs/audit/FORMULA_EVIDENCE_DEBT.md` FD-01 | P4 ranked as direct gate blocker |

## Current State

| Item | State |
|------|-------|
| P4 algorithm text | Specified as `P4-RBL-v1` |
| Runtime labeler | Missing |
| Label-vintage artifact writer | Missing |
| Target universe snapshot | Missing |
| >=3-year 1D data coverage | Missing |
| >=15-of-20 asset evidence | Missing |
| Phase 0 gate status | `NOT_APPROVED` |

## Why Not Revise The Criterion Now

The criterion is demanding, but it is not incoherent:

- P4 labels are required before Phase 1 because Phase 1 OOS needs regime
  spanning and later overlays depend on label immutability.
- The algorithm is deterministic and has no fitted parameters, reducing the
  risk of optimization leakage.
- The missing work is implementation and evidence, not conceptual impossibility.
- Revising the criterion now would weaken the "evaluation engine first" posture
  before testing whether the specified deterministic labeler is feasible.

Charter-level revision remains available only if implementation/evidence work
shows the criterion is infeasible or harmful.

## Required Implementation Scope

A future P4 implementation task should include:

- weekly resampling rule `p4_weekly_resample_v1`;
- support for `weekday` and `continuous` calendar profiles;
- completed-week validation;
- 156-week warmup behavior with `UNLABELED` outputs;
- feature calculation for `r_4w`, `r_13w`, `dd_26w`, `vol_13w`,
  `vol_pct_156w`, and `eff_13w`;
- priority assignment: `stress`, then `trending`, then `mean_reverting`;
- deterministic `p4_param_hash`;
- label-vintage artifact fields:
  `{symbol, calendar_profile, week_close_ts, p4_state, p4_version,
  p4_param_hash, label_generation_ts, dataset_hash,
  p4_weekly_resample_version}`;
- tests for no look-ahead, warmup, incomplete weeks, zero efficiency denominator,
  percentile rank, and deterministic replay.

## Required Evidence Scope

P4 gate evidence must include:

- declared 20-asset target universe snapshot;
- dataset hashes for each input series;
- coverage table for all 20 assets;
- pass/fail marker for >=3 years of 1D data per asset;
- label artifact path per passing asset;
- aggregate proof that >=15 assets satisfy coverage;
- reproduction command or procedure;
- no OOS/performance interpretation of the labels.

## Blockers Before Closure

| Blocker | Required closure |
|---------|------------------|
| No runtime labeler | Implement and test `P4-RBL-v1` |
| No label artifacts | Generate vintage-locked label outputs |
| No target universe | Approve target 20-asset universe snapshot |
| No historical data coverage | Produce >=3-year 1D coverage for >=15 assets |
| No reproduction packet | Add deterministic reproduction command/procedure |

## Allowed / Prohibited

Allowed:

- implement deterministic P4 labeler;
- generate historical labels for evidence;
- use local approved datasets or explicitly approved provider data;
- record P4 labels as gate evidence only.

Prohibited:

- optimize P4 thresholds for Sharpe;
- treat P4 labels as OOS performance evidence;
- use P4 labels to route capital before Phase 1 approval;
- close the Phase 0 gate with algorithm text alone;
- revise the Phase 0 criterion without charter-level review.

## Decision Boundary

This decision selects the implementation/evidence path. It does not implement
P4, does not approve Phase 0, does not start Phase 1, and does not authorize any
performance claim.
