# T21_FORMULA_GOVERNANCE_DISPOSITION
_Date: 2026-05-03 · Decision ID: D-017_

## Verdict

T21 may proceed under a narrow, task-specific formula-governance disposition.
This is not a global D-010 closure.

## Rationale

T21 is formula-bearing because it implements four-stream P&L attribution, a raw
Net Sharpe boundary, drawdown worked examples, and `PerformanceMetrics`
construction. The Phase 7 review correctly stopped direct implementation until
this disposition existed.

The formula risk is containable because T21 can be limited to deterministic
attribution arithmetic and worked examples. The unresolved statistical package
surfaces remain outside T21 and are still assigned to T23.

## Allowed T21 Scope

T21 may implement only:

- four-stream attribution into streams (a), (b), (c), and (d);
- explicit enforcement that Net Sharpe uses streams (a)+(b)+(c) only;
- raw Net Sharpe point-estimate arithmetic over explicitly supplied return
  observations;
- drawdown record generation from a deterministic cumulative equity sequence;
- `PerformanceMetrics` assembly with `n_eff=None` and
  `harvey_liu_deflated_sharpe=None` plus explicit reason code
  `stub_pending_formula_verification`;
- worked-example tests for the above.

## Prohibited T21 Scope

T21 must not implement:

- Harvey-Liu deflation or adjusted p-value logic;
- standalone Sharpe CI calculation, bootstrap CI, or T23 statistical helpers;
- N_eff / K3 estimator logic;
- IC/BR, P4, P1/P3 governance state machine, phase-exit logic, K-report, RDL
  promotion, or OOS performance-claim artifacts;
- any inclusion of stream (d) in Net Sharpe.

If a `NetSharpe` object is constructed in T21, the confidence interval must be
provided explicitly by the caller or test fixture. T21 must not derive the CI
internally; T23 owns that statistical calculation.

## D-010 Finding Disposition for T21

| Finding | T21 disposition |
|---------|-----------------|
| F-1 Harvey-Liu | Not implemented in T21. T21 may only return explicit stub fields. T23 owns implementation. |
| F-2 Sharpe CI | Not implemented in T21. T21 may preserve caller-provided CI metadata only. T23 owns CI helpers. |
| F-4 P4 reproducibility | Out of T21 scope; no P4 code allowed. |
| F-5 IC_long / FLAM | Out of T21 scope; no IC/BR/FLAM code allowed. |
| F-30 RDL telemetry | Future real-evidence gate; no RDL telemetry artifact emitted by T21. |
| F-31 K-report epoch coverage | Future real-evidence gate; no K-report artifact emitted by T21. |

## Related P1 Closure

TASK-AF-022 / F-22 is closed for current canonical implementation scope:
current source-of-truth implementation docs define Net Sharpe as streams
(a)+(b)+(c), excluding stream (d). Historical audit artifacts that describe the
old drift are retained as history and are not treated as current protocol
definitions.

## Required T21 Review Focus

The T21 implementation review must verify:

1. Stream (d) cannot enter Net Sharpe through the public API.
2. `compute_net_sharpe()` cannot accept stream (d) directly.
3. T21 does not compute Sharpe CI, Harvey-Liu, or N_eff.
4. Drawdown worked examples are deterministic and manually reproducible.
5. `PerformanceMetrics` reason code explicitly marks unresolved statistical
   fields as stubs.

## Decision

Record as D-017. T21 implementation may begin under these constraints.
