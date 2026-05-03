# D010 Focused Audit - F-1/F-2/F-4/F-5

Date: 2026-05-03
Status: PASS for T15 entry; recorded as D-016
Scope: Formula-bearing D-010 blockers that still govern T15 after D-015

---

## Verdict

T15 SimBroker Cost Model may proceed after this review is recorded in the
governance state.

This review verifies the canonical mitigations for F-1, F-2, F-4, and F-5 in:

- `docs/core/PROTOCOL_SPEC.md` v1.8
- `docs/core/CHARTER.md` v5.3
- `docs/core/GLOSSARY.md` v1.4
- `docs/audit/D010_CLOSURE_PACKET.md`

F-30 and F-31 are explicitly outside this closure verdict. They remain In
Progress future real-evidence gates under D-015 and must not be closed with
synthetic evidence.

---

## Review Matrix

| Finding | Focused audit question | Verdict | Rationale |
|---|---|---|---|
| F-1 | Is the Harvey-Liu/deflated-Sharpe workflow reproducible from specified inputs? | PASS | `HL-HB-v1` fixes method ID, family scope, M_total timing, one-sided p-value, Holm adjustment, Sharpe-equivalent mapping, output fields, and no-floor rule. |
| F-2 | Is the Sharpe CI correction explicit and downstream K1 wording no longer overclaims precision? | PASS | `CI-SR-ACF-v1` defines the base SE, autocorrelation adjustment, required report fields, and states that 15-month K1 is a policy screen, not powered proof. |
| F-4 | Is the P4 labeler deterministic and free of fitted historical calibration? | PASS | `P4-RBL-v1` is rule-based, no fitted parameters, vintage-tagged, and now fixes weekly resampling, volatility, percentile rank, and zero-denominator conventions. |
| F-5 | Is long-side IC/breadth planning corrected and conservative enough for implementation? | PASS | BR arithmetic is corrected to 120 for 5 x 2 x 12, IC_long is planning-only, high/low flags exist, and `BR_eff_long` uses N_eff or a conservative 0.40 placeholder. |

---

## F-1 Verification

Canonical inputs are sufficient:

- `trial_id`, `family_tag`, `raw_sharpe_annual`, `se_sharpe_annual`,
  `sample_length`, `M_total`, `return_frequency`, `method_id`, `code_hash`,
  `policy_hash`
- `M_total = Main + AT + RDL-*`, counted at Trial Registry submission time
- one-sided positive-edge p-value: `p_i = 1 - Phi(raw_sharpe / se_sharpe)`
- Holm adjusted p-value:
  `p_holm_j = max_{k<=j} min(1, (M_total - k + 1) * p_(k))`

Worked example with `M_total=3`, all `se_sharpe_annual=0.30`:

| Trial | Raw Sharpe | z | p_raw | p_holm | Deflated Sharpe | Haircut |
|---|---:|---:|---:|---:|---:|---:|
| A | 0.600000 | 2.000000 | 0.022750 | 0.068250 | 0.446685 | 0.153315 |
| B | 0.450000 | 1.500000 | 0.066807 | 0.133614 | 0.332840 | 0.117160 |
| C | 0.300000 | 1.000000 | 0.158655 | 0.158655 | 0.300000 | 0.000000 |

Result: a second reviewer can reproduce the haircut from the same inputs. The
implementation must still handle `p_holm=1.0` explicitly instead of silently
flooring deflated Sharpe.

---

## F-2 Verification

Canonical formula:

`SE(SR_annual) = sqrt((1 + SR_annual^2 / 2) / T_eff_years)`

Zero-autocorrelation 15-month example:

- `SR = 0.30`
- `T_eff_years = 1.25`
- `SE = sqrt((1 + 0.30^2 / 2) / 1.25) = 0.914330`
- `CI_68 = [-0.614330, 1.214330]`

Positive-autocorrelation example:

- `n = 315`, annualization factor `252`, `L = 2`
- `rho_1 = 0.20`, `rho_2 = 0.10`
- Bartlett weights: `2/3`, `1/3`
- denominator `= 1 + 2 * ((2/3)*0.20 + (1/3)*0.10) = 1.333333`
- `n_eff = 236.25`
- `T_eff_years = 0.937500`
- `SE = 1.055778`
- `CI_68 = [-0.755778, 1.355778]`

Result: the old narrow 15-month CI claim is removed, and K1 is correctly treated
as a policy screen.

---

## F-4 Verification

`P4-RBL-v1` now has fixed deterministic conventions:

- no fitted parameters; `calibration_end_ts = null`
- `weekday` calendar profile = complete ISO Monday-Friday weeks
- `continuous` calendar profile = complete ISO Monday-Sunday weeks
- weekly bar = first open, max high, min low, last close, sum volume
- `vol_13w` uses sample standard deviation with `ddof=1`
- `vol_pct_156w` uses weak percentile rank `count(x <= current) / count(x)`
- zero efficiency-ratio denominator maps to `eff_13w = 0`
- every label stores `calendar_profile` and `p4_weekly_resample_version`

Result: F-4's protocol blocker is closed for T15. A real historical label fixture
is still required before implementing or accepting TASK-DEV-003 / regime signal
runtime behavior, but that is no longer a SimBroker cost-model formula blocker.

---

## F-5 Verification

Corrected breadth example:

- `skill_count = 5`
- `timeframe_count = 2`
- monthly independent-bet prior = `12`
- `BR_raw_long = 5 * 2 * 12 = 120`
- if `N_eff_signal / K_signal = 0.40`, then `BR_eff_long = 48`

IC examples:

- `IC_long_observed = 0.060` raises `HIGH_IC_SUSPECT_FLAG`
- haircut view: `IC_long_haircuted = 0.060 - 0.015 = 0.045`
- observed provisional `IR_long_planning = 0.060 * sqrt(48) = 0.415692`
- haircuted provisional `IR_long_planning = 0.045 * sqrt(48) = 0.311769`
- mid-prior example: `0.040 * sqrt(48) = 0.277128`

Result: the previous unadjusted 240-breadth planning path is closed. Remaining
K3 estimator work affects future portfolio/risk modules, not T15 cost formulas.

---

## Closure Actions

This audit supports:

- closing TASK-AF-001, TASK-AF-002, TASK-AF-004, and TASK-AF-005 in
  `docs/audit_task_registry.md`
- updating `docs/CODEX_PROMPT.md` to name T15 as the next task
- keeping TASK-AF-030 and TASK-AF-031 In Progress under D-015

T15 must not implement P4, Harvey-Liu, Sharpe CI, IC/BR, RDL, K-report, or
phase-exit logic. T15 may implement only deterministic SimBroker cost-model code
and its worked-example tests.
