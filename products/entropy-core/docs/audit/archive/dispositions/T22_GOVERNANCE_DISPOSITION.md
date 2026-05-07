# T22_GOVERNANCE_DISPOSITION
_Date: 2026-05-05 · Decision ID: D-018_

## Verdict

T22 may proceed under a narrow, task-specific governance disposition.
This is not a global D-010 closure.

## Rationale

T22 is formula-bearing because it encodes P1/P3 regime thresholds and transition
semantics. The risk is containable because the canonical protocol now specifies
deterministic P1/P3 policy parameters:

- P1 trips when realized drawdown from HWM is greater than or equal to 12%.
- P1 resets only when HWM gap is less than 8% and at least 5 business days have
  elapsed.
- P3 fires when 20-day average pairwise correlation is greater than 0.55.
- P3 clears when correlation is less than 0.45 after cooldown.
- If P1 activates during a P3 ramp, P3 ramp progress is frozen; after P1 clears,
  the P3 ramp resumes from the frozen progress.

T22 can implement these deterministic policy thresholds without implementing the
unresolved statistical package, P4 labeler, K-report evidence, or RDL telemetry.

## Allowed T22 Scope

T22 may implement only:

- P1 drawdown trip/reset state transitions;
- P1 `can_open_new_position()` blocking while active;
- P3 correlation fire/clear state transitions with hysteresis and cooldown;
- P3 gross reduction tier mapping for `rho_avg`;
- P1/P3 concurrent transition semantics where P1 pauses P3 ramp progress;
- append-only `GovernanceEvent` emission for P1/P3 state transitions;
- synthetic tests for trip, reset, idempotency, boundary, cooldown, and
  concurrent behavior.

## Prohibited T22 Scope

T22 must not implement:

- IC/BR or FLAM calculations;
- N_eff/K3 estimators or statistical helper formulas;
- P4 label generation or weekly regime algorithms;
- K-report generation, epoch coverage evidence, or phase-exit evidence;
- RDL promotion telemetry or audit-complete claims for F-30/F-31;
- automated position management beyond exposing state and `can_open_new_position()`.

## D-010 Finding Disposition for T22

| Finding | T22 disposition |
|---------|-----------------|
| F-1 Harvey-Liu | Out of T22 scope; no multiplicity logic. |
| F-2 Sharpe CI | Out of T22 scope; no confidence interval logic. |
| F-4 P4 reproducibility | Out of T22 scope; no P4 labeler. |
| F-5 IC_long / FLAM | Out of T22 scope; T22 uses only supplied `rho_avg` policy input. |
| F-30 RDL telemetry | Future real-evidence gate; no RDL telemetry emitted by T22. |
| F-31 K-report epoch coverage | Future real-evidence gate; no K-report artifact emitted by T22. |

## Required T22 Review Focus

The T22 implementation review must verify:

1. P1 trips at exactly 12% and not below.
2. P1 reset requires both `gap_from_hwm < 8%` and `business_days_elapsed >= 5`.
3. P1 and P3 transition paths are idempotent.
4. Every transition emits exactly one `GovernanceEvent`.
5. Events are appended through inserts/adds only; no update/delete path is added.
6. P1 active state freezes P3 ramp progress, and P3 resumes after P1 clears.
7. T22 does not implement IC/BR, N_eff/K3, P4, RDL telemetry, K-report, or
   phase-exit evidence.

## Decision

Record as D-018. T22 implementation may begin under these constraints.
