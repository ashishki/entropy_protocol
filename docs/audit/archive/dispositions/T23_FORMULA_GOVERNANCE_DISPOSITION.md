# T23_FORMULA_GOVERNANCE_DISPOSITION
_Date: 2026-05-05 · Decision ID: D-019_

## Verdict

T23 may proceed under a narrow, task-specific formula-governance disposition.
This is not a global D-010 closure.

## Rationale

T23 is formula-bearing because it introduces statistical helper surfaces for
Sharpe confidence intervals, Harvey-Liu deflation, and N_eff/K3. At this point
the project is still establishing Phase 0 foundation. The implementation should
make these surfaces explicit and testable without treating them as final
research evidence or phase-exit authority.

The acceptable foundation posture is therefore: implement provisional helpers
with method IDs, worked examples, and clear stub status, while preserving the
remaining research/audit debt for the post-T24 analysis pass.

## Allowed T23 Scope

T23 may implement only:

- `compute_sharpe_ci()` with method ID `CI-SR-ACF-v1`, analytical base logic,
  and a deterministic bootstrap stub path;
- `compute_harvey_liu_deflation()` as an `HL-HB-v1` formula skeleton with clear
  stub status and worked-example tests;
- `compute_n_eff()` using the documented K3 formula
  `k / (1 + (k - 1) * rho_avg)`;
- simple return types that expose method IDs, reason codes, and input metadata;
- tests that verify bounds, determinism, worked examples, and explicit stub
  documentation.

## Prohibited T23 Scope

T23 must not implement:

- phase-exit pass/fail decisions;
- K-report generation or epoch coverage evidence;
- RDL promotion telemetry or any closure claim for F-30/F-31;
- OOS performance claims;
- P4 label generation;
- IC/BR or FLAM calculations;
- any claim that Harvey-Liu or Sharpe CI formulas are independently validated
  beyond the T23 provisional helper tests.

## D-010 Finding Disposition for T23

| Finding | T23 disposition |
|---------|-----------------|
| F-1 Harvey-Liu | Implement a skeleton helper only; mark as pending independent reproducibility verification. |
| F-2 Sharpe CI | Implement provisional `CI-SR-ACF-v1` helper with explicit method ID; do not use it for phase-gate proof. |
| F-4 P4 reproducibility | Out of T23 scope; no P4 labeler. |
| F-5 IC_long / FLAM | Out of T23 scope; no IC/BR/FLAM code. |
| F-30 RDL telemetry | Future real-evidence gate; no RDL telemetry emitted by T23. |
| F-31 K-report epoch coverage | Future real-evidence gate; no K-report artifact emitted by T23. |

## Required T23 Review Focus

The T23 implementation review must verify:

1. Statistical helpers expose method IDs and explicit stub reason codes.
2. Sharpe CI returns bounds around the point estimate for a worked example.
3. Bootstrap path is deterministic and documented as stub output.
4. Harvey-Liu helper docstring contains the required stub warning.
5. N_eff/K3 matches the worked example `6 / (1 + 5 * 0.30) = 2.4`.
6. T23 does not emit phase-exit, K-report, RDL, OOS-claim, P4, IC/BR, or FLAM
   artifacts.

## Decision

Record as D-019. T23 implementation may begin under these constraints.
