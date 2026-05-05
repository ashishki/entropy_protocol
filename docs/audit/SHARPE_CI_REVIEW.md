# SHARPE_CI_REVIEW
_Date: 2026-05-05 · Scope: P0.5-003 review of `CI-SR-ACF-v1`_

## Verdict

Decision: `IMPLEMENTATION_REVISED_PACKET_REQUIRED`.

P0.6-004 revised the `compute_sharpe_ci()` helper to expose canonical report
fields and autocorrelation-adjusted effective years. It is now acceptable as
statistical helper tooling, but it still does not approve Phase 0 or authorize
OOS/performance claims without registered report/gate packet integration.

## Reviewed Artifacts

| Artifact | Role |
|----------|------|
| `docs/core/PROTOCOL_SPEC.md` Net Sharpe / `CI-SR-ACF-v1` | Canonical formula and report-field contract |
| `docs/core/GLOSSARY.md` Net Sharpe | Canonical interpretation rule |
| `docs/audit/D010_CLOSURE_PACKET.md` F-2 | Audit closure rationale and required evidence |
| `docs/audit/T23_FORMULA_GOVERNANCE_DISPOSITION.md` | Narrow permission for provisional helper |
| `entropy/stats/analysis.py` | Current implementation |
| `tests/unit/test_stats.py` | Current implementation tests |

## Canonical Requirements

`CI-SR-ACF-v1` requires:

- annualized Sharpe standard error;
- preregistered autocorrelation lag `L`;
- Bartlett-weighted serial-correlation adjustment;
- `n_eff`;
- `T_eff_years`;
- 68% CI lower/upper;
- report fields: return frequency, annualization factor, `n`, `L`,
  autocorrelation vector or hash, `n_eff`, `T_eff_years`, raw Sharpe, Sharpe SE,
  CI bounds, method ID, and policy hash.

Interpretation rule: CI is mandatory uncertainty disclosure. It does not
override frozen kill thresholds. At 15 months OOS, a 0.30 Sharpe system has a
zero-autocorrelation 68% CI half-width near 0.91, not 0.15-0.20.

## Current Helper Assessment

| Check | Result | Notes |
|-------|--------|-------|
| Method ID exposed | Pass | `CI-SR-ACF-v1` is exposed through `CI_METHOD_ID` |
| Explicit provisional reason code | Pass | Result includes `stub_pending_formula_verification` |
| Point estimate contained in bounds | Pass | Unit test covers this basic property |
| Deterministic bootstrap stub | Pass for scaffold | Unit test verifies deterministic seeded output |
| Autocorrelation lag `L` input | Pass | P0.6-004 adds `lag` |
| Autocorrelation vector/hash | Pass | P0.6-004 reports vector and SHA-256 hash |
| Bartlett adjustment | Pass | P0.6-004 computes Bartlett-adjusted `n_eff` |
| Required report-field object | Pass | P0.6-004 result includes `n`, `lag`, `n_eff`, `T_eff_years`, Sharpe SE, frequency, policy hash |
| Gate/report acceptance | Packet-required | Helper is revised, but gate/report integration remains required |

## Worked Example Review

Zero-autocorrelation 15-month example:

- `raw_sharpe_annual = 0.30`
- `T_eff_years = 1.25`
- `SE = sqrt((1 + 0.30^2 / 2) / 1.25)`
- `SE = sqrt(1.045 / 1.25) = sqrt(0.836) ~= 0.914`
- 68% CI ~= `0.30 +/- 0.914`, or `[-0.614, 1.214]`

This confirms the core protocol warning: 15 months does not give tight Sharpe
precision.

The current helper can approximate the zero-autocorrelation base path when the
return count and annualization factor imply the desired effective years, but it
does not expose enough metadata to prove the canonical report contract.

## Failure Cases Required Before Acceptance

P0.6-004 covers:

- missing or negative effective sample size;
- invalid or omitted autocorrelation lag;
- autocorrelation vector length mismatch;
- autocorrelation adjustment that produces materially different `T_eff_years`;
- policy hash missing in a report context;
- report attempting to use provisional CI for phase-gate proof.

The final two report-context checks remain packet/report integration concerns.

## Required Revision

P0.6-004 added:

1. A result object containing all canonical report fields.
2. Autocorrelation inputs or a separate auditable autocorrelation computation
   artifact.
3. Bartlett-weighted `n_eff` and `T_eff_years`.
4. Worked examples for zero and nonzero autocorrelation.

Remaining before gate/report use:

1. Integrate the revised result into report artifacts.
2. Prevent provisional or missing-policy CI output from being used as phase-exit
   proof.

## Decision Boundary

This review now records P0.6-004 implementation closure for the helper. It does
not approve Phase 0, does not validate any performance claim, and does not
replace registered gate-packet evidence.
