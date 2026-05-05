# Phase 1A Baseline Specification Registration Packet

Date: 2026-05-05
Task: P1A-004
Status: `COMPLETE`
Registration ID: `PHASE1A-BASELINE-SPEC-REGISTRATION-v1`
Registration instance ID: `P1A-BASELINE-REG-001`

## Decision

P1A-004 is approved as the first machine-readable archive baseline
specification registration for Phase 1A.

The registration records a non-executable long-only baseline specification
shape against the P1A-003 read-gate boundary. It hashes the baseline spec,
records validation-access metadata, preserves the no-claim boundary, and keeps
holdout locked. It does not implement executable strategy logic, run portfolio
or archive evaluation, activate Growth/RDL/RBE, activate live feeds, unlock
holdout, or make OOS/performance claims.

## Registration Scope

| Field | Value |
|---|---|
| Boundary manifest hash | `2759fad18037361412f504384f22b411b4283b00e7764150f8c660f4375620df` |
| Baseline spec hash | `a94c0441e0ff5b38bd0bafe83e445fe2041eb19e936dac19526ef417c39d3646` |
| Validation registration hash | `7a23273630350704809be291da57c06e23e15537a16eaf3950d5e0da599816b4` |
| Registration manifest hash | `1b968c53607729fd3a67a9a3a4264f93e9f0a1ad60044e5614baa596a8a0ba01` |
| Archive only | `true` |
| Gate claim allowed | `false` |
| Runtime signal status | `not_implemented` |

## Baseline Shape

Registered skill families:

- `trend_following`
- `breakout`
- `mean_reversion`
- `volatility_filter`
- `regime_state_filter`
- `cost_aware_risk_filter`

Portfolio constraints:

| Constraint | Value |
|---|---|
| Direction | `long_only` |
| Gross exposure | `0.0 <= gross <= 1.0` |
| Short exposure | `0.0` |
| Leverage | `none` |
| Rebalance policy | `deterministic_preregistered_before_validation` |
| Treasury stream | `report_only_excluded_from_net_sharpe` |

## Split Access State

| Split | State |
|---|---|
| `ARCHIVE_FORMATION` | Allowed for baseline specification drafting |
| `ARCHIVE_VALIDATION` | Allowed only with the recorded registration metadata |
| `ARCHIVE_HOLDOUT` | Locked; no unlock produced |

## Artifacts

| Artifact | Path |
|---|---|
| Baseline registration implementation | `entropy/evidence/phase1a_baseline.py` |
| Unit tests | `tests/unit/test_phase1a_baseline.py` |
| Package export | `entropy/evidence/__init__.py` |
| Registration manifest | `artifacts/evidence/phase1a_baseline_registration/registration_001/PHASE1A_BASELINE_SPEC_REGISTRATION_MANIFEST.json` |
| Registration summary | `artifacts/evidence/phase1a_baseline_registration/registration_001/PHASE1A_BASELINE_SPEC_REGISTRATION_SUMMARY.md` |
| Boundary manifest | `artifacts/evidence/phase1a_registration_boundary/boundary_001/PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_MANIFEST.json` |

## Next Task

Proceed to P1A-005: Phase 1A Fix Closure Review.

P1A-005 should decide whether the P1A-001 through P1A-004 fix chain is
sufficient to start a narrow executable baseline scaffold, or whether another
registration/contract fix is required first.
