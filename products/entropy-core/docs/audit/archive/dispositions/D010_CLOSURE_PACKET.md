# D010 Closure Packet - Protocol P0 Blockers Before T15

Date: 2026-05-03
Status: Applied to canonical docs - D-016 focused audit passed for F-1/F-2/F-4/F-5
Scope: D-010 formula blockers for T15 plus future real-evidence gates

---

## Executive Decision

Do not implement T15 SimBroker Cost Model yet.

D-013 denies a T15-specific waiver. D-014 applies canonical mitigations and
evidence contracts. D-015 narrows the T15 blocker scope: the only compliant path
to T15 is focused audit verification of F-1, F-2, F-4, and F-5 mitigations.

F-30 and F-31 are not closed. They are future hard gates for real RDL promotion
telemetry, K-report epoch coverage, phase-exit evidence, and any code path that
emits those artifacts. They must not be closed with synthetic evidence or text-only
assertion.

This packet is not closure evidence by itself. It has been applied to canonical
protocol docs, and `products/entropy-core/docs/audit/D010_FOCUSED_AUDIT_F1_F2_F4_F5.md` records the
focused audit pass that permits T15 under D-016.

---

## Why T15 Stays Blocked

T15 would encode executable cost arithmetic. In this protocol, cost arithmetic is
not local to fills: it feeds net Sharpe, Harvey-Liu haircut decisions, phase exit
evidence, CRR, SimBroker drift, and later K-report windows.

The expected workload is high, so small optimistic errors compound:

- A 1%/year unmodeled friction on a 12%-vol portfolio reduces net Sharpe by about
  0.08 units per `PROTOCOL_SPEC.md` Cost Model Risk.
- Crypto funding at 0.05%-0.15% per 8h is routine in bull phases, not a tail case.
- High turnover makes a few basis points per fill large enough to flip K1-adjacent
  conclusions.
- If multiplicity, CI width, and P4 labels remain ambiguous, a correct-looking
  SimBroker implementation can make invalid downstream reports look precise.
  Separate RDL/K-report telemetry remains a future evidence gate under D-015.

Therefore the architecture posture is conservative: resolve formula semantics
first, then implement deterministic formulas.

---

## Closure Principles

1. Deterministic and independently reproducible.
2. Conservative when evidence is missing.
3. No phase-gate pass from unstated formulas or missing telemetry.
4. Every formula-bearing report must include method ID, input fields, policy hash,
   code hash, and a worked example.
5. Retrieval files (`DECISION_LOG.md`, `EVIDENCE_INDEX.md`) can point to evidence;
   they cannot close findings by assertion.
6. F-30 and F-31 require real generated runtime/audit evidence. Text-only
   clarification and synthetic closure artifacts are not enough to close them.

---

## Summary Matrix

| Finding | Current blocker | Recommended decision | Closure status after this packet |
|---|---|---|---|
| F-1 | Harvey-Liu variant and aggregation not fully specified | Lock `HL-HB-v1` as Holm-Bonferroni gate control; define p-value workflow, trial family, and Sharpe-equivalent haircut | Closed by D-016 focused audit |
| F-2 | Sharpe CI precision claim was wrong and power is weak | Replace narrow CI claims with `CI-SR-ACF-v1` derivation; treat K1 as policy screen, not powered statistical proof | Closed by D-016 focused audit |
| F-4 | P4 labels required but algorithm undefined | Adopt rule-based `P4-RBL-v1`, no fitted parameters, vintage-locked labels | Closed by D-016 focused audit |
| F-5 | `IC_long` and `BR_long` overstate confidence | Correct BR arithmetic; add correlation-adjusted `BR_eff`; add `IC_long` suspect and low-edge controls | Closed by D-016 focused audit |
| F-30 | RDL queue policy lacks telemetry evidence | Define promotion-log schema and audit queries for FIFO, monthly cap, and shock-control | Future real-evidence gate; not a T15 blocker under D-015 |
| F-31 | K-report epoch tags lack coverage evidence | Define K1-K6 report schema and mixed-epoch audit query | Future real-evidence gate; not a T15 blocker under D-015 |

---

## D-015 Scope Rule

D-015 does not close F-30 or F-31. It reclassifies them out of the T15 blocker set
because they cannot honestly be closed before real RDL promotion and K-report
events exist, and because they are not SimBroker cost-model formula blockers.

For T15, this packet now supports a focused audit question:

- Are the canonical mitigations for F-1, F-2, F-4, and F-5 sufficient to let
  SimBroker cost formulas be implemented without encoding unresolved protocol
  arithmetic?

For future governance, F-30 and F-31 remain hard gates before:

- RDL promotion telemetry is emitted or used as phase evidence.
- K1-K6 reports are generated from mixed evaluation epochs.
- Phase-exit evidence depends on RDL queue behavior or K-report epoch coverage.
- Any implementation path claims those artifacts are audit-complete.

No synthetic evidence may close F-30 or F-31.

---

## F-1 - Harvey-Liu Multiplicity Correction

### Finding

The protocol mandates Harvey-Liu deflation but does not provide a complete formula
variant, parameter set, or cross-phase aggregation rule. `GLOSSARY.md` names
`HL-HB-v1`, but the current text is not enough for a second reviewer to reproduce
the haircut.

### Recommended Decision

Use `HL-HB-v1` as a Holm-Bonferroni family-wise error-rate control for phase-gate
decisions. DSR-style or BHY/FDR-style values may be reported as secondary research
diagnostics only, but cannot decide a gate unless separately approved.

### Proposed Canonical Specification

Inputs per trial:

- `trial_id`
- `family_tag`
- `raw_sharpe_annual`
- `se_sharpe_annual` from `CI-SR-ACF-v1`
- `sample_length`
- `return_frequency`
- `M_total`
- `method_id = HL-HB-v1`
- `code_hash`
- `policy_hash`

Family scope:

- Main Track, AT, and `RDL-*` trials all count.
- Trials count at Trial Registry submission time, not promotion time.
- The family is `family_tag` unless the Spec Owner explicitly declares a broader
  gate family before evaluation.
- Partial or failed runs still count once registered if they inspected evaluation
  data or produced a reportable result.

Computation:

1. Compute `z_i = raw_sharpe_annual_i / se_sharpe_annual_i`.
2. Compute one-sided positive-edge p-value `p_i = 1 - Phi(z_i)`.
3. Sort p-values in ascending order inside the declared family.
4. For sorted rank `j`, compute Holm adjusted value:
   `p_holm_j = max_{k<=j} min(1, (M_total - k + 1) * p_(k))`.
5. Map back to a Sharpe-equivalent value:
   `z_deflated_j = Phi^{-1}(1 - p_holm_j)`.
6. `deflated_sharpe_j = z_deflated_j * se_sharpe_annual_j`.
7. `haircut_units_j = raw_sharpe_annual_j - deflated_sharpe_j`.

Reporting rules:

- Do not floor `deflated_sharpe` at zero.
- If any required trial p-value in the family is unavailable, the phase gate cannot
  claim a valid Harvey-Liu haircut.
- Every phase report must show `M_total`, family membership, raw p-value, adjusted
  p-value, raw Sharpe, deflated Sharpe, and haircut units.

### Required Evidence To Close

- `PROTOCOL_SPEC.md` NN-5 and metric sections contain the full workflow above.
- `GLOSSARY.md` defines `HL-HB-v1` with the same fields and formula.
- A worked example with at least three trials shows raw p-values, sorted ranks,
  adjusted p-values, deflated Sharpe, and haircut units.
- Audit rerun confirms a second reviewer can reproduce the worked example.

---

## F-2 - Sharpe CI Correction

### Finding

The old CI claim was materially too narrow. Audit evidence derived about +/-0.89
to +/-0.91 at 15 months for a 0.30 Sharpe system, not +/-0.15 to +/-0.20.

### Recommended Decision

Keep `CI-SR-ACF-v1` as the canonical uncertainty disclosure method, but make the
wide uncertainty explicit. K1 remains a frozen policy screen unless the Spec Owner
opens a separate charter-level threshold change.

### Proposed Canonical Specification

Base approximation:

`SE(SR_annual) = sqrt((1 + SR_annual^2 / 2) / T_eff_years)`

Autocorrelation adjustment:

1. Compute bar-level return autocorrelations through preregistered lag `L`.
2. Use Bartlett weights `w_l = 1 - l/(L+1)`.
3. Estimate effective sample size:
   `n_eff = n / (1 + 2 * sum_{l=1..L}(w_l * rho_l))`.
4. Convert to effective years:
   `T_eff_years = n_eff / annualization_factor`.
5. `CI_68 = raw_sharpe_annual +/- SE(SR_annual)`.

Minimum reporting fields:

- return frequency
- annualization factor
- `n`
- `L`
- autocorrelation vector or hash of it
- `n_eff`
- `T_eff_years`
- `raw_sharpe_annual`
- `se_sharpe_annual`
- CI lower and upper
- method ID and policy hash

Interpretation rule:

- CI is mandatory uncertainty disclosure.
- K1 at 15 months is a policy screen, not a powered statistical proof.
- Any text implying that 15 months gives tight Sharpe precision must be removed.
- The pivot band `0.22-0.28` may support a written continuation hypothesis, but it
  must not be described as statistically separable from K1 at 15 months.

### Required Evidence To Close

- `CHARTER.md`, `PROTOCOL_SPEC.md`, and `GLOSSARY.md` remove the narrow CI claim.
- A derivation example reproduces the 15-month `SR=0.30` half-width near 0.91 when
  autocorrelation is zero.
- A second example shows nonzero autocorrelation widening or otherwise changing
  `T_eff_years`.
- Audit rerun confirms all downstream wording treats K1 as a policy screen.

---

## F-4 - P4 Weekly Regime Algorithm

### Finding

P4 labels are required for Phase 0 exit, Phase 1 regime spanning, and Phase 2
overlay evaluation, but the label algorithm is undefined.

### Recommended Decision

Adopt `P4-RBL-v1`: a deterministic, rule-based weekly labeler with no fitted
parameters. P4 thresholds are policy constants, not Sharpe-optimized knobs.

### Proposed Canonical Specification

Input data:

- UTC daily OHLCV bars.
- Weekly bars are built from complete calendar-profile weeks using locked
  `p4_weekly_resample_v1`: `weekday` datasets use ISO Monday-Friday bars and
  `continuous` datasets use ISO Monday-Sunday bars.
- A label at week `t` may use only data with timestamp `<= weekly_close_t`.

Features at week `t`:

- `r_4w = log(close_t / close_{t-4})`
- `r_13w = log(close_t / close_{t-13})`
- `dd_26w = close_t / max(close_{t-25..t}) - 1`
- `vol_13w = sample_stdev(weekly_log_returns_{t-12..t}, ddof=1) * sqrt(52)`
- `vol_pct_156w = weak_percentile_rank(current vol_13w over computable trailing
  values from completed weeks t-155..t)`.
- `eff_13w = abs(r_13w) / sum(abs(weekly_log_returns_{t-12..t}))`; if the
  denominator is zero, `eff_13w = 0`.

Warmup:

- No P4 label is valid until 156 completed weekly bars exist.
- Warmup windows are `UNLABELED` and do not count toward regime-spanning evidence.

Priority assignment:

1. `stress` if any condition is true:
   - `r_4w <= -0.08`
   - `dd_26w <= -0.15`
   - `vol_pct_156w >= 0.80 and r_4w < -0.03`
2. `trending` if not stress and both are true:
   - `abs(r_13w) >= 0.08`
   - `eff_13w >= 0.35`
3. `mean_reverting` otherwise.

Versioning:

- Method ID: `P4-RBL-v1`.
- The parameter set above is hashed as `p4_param_hash`.
- `calibration_end_ts = null` because no fitting is performed.
- Every label stores `{symbol, week_close_ts, p4_state, p4_version, p4_param_hash,
  label_generation_ts, dataset_hash}`.

### Required Evidence To Close

- `PROTOCOL_SPEC.md` contains the full algorithm, warmup rule, and vintage artifact.
- `GLOSSARY.md` defines P4 labels by method ID.
- A deterministic reproduction fixture over at least two symbols shows identical
  labels from the same raw data.
- Audit rerun confirms Phase 0 P4 exit evidence is third-party reproducible.

---

## F-5 - IC_long, BR_long, And Correlation-Adjusted Breadth

### Finding

The current documents use `BR_long ~= 240` while also stating `5 skills x 2
timeframes x 12 months`, which equals 120. The IC_long prior is load-bearing,
unvalidated, and lacks the suspect controls already applied to IC_short.

### Recommended Decision

Treat IC_long as a planning prior only. Correct the BR arithmetic and require
correlation-adjusted breadth for any FLAM-derived planning or explanation.

### Proposed Canonical Specification

Definitions:

- `K_signal = count(active skill-timeframe streams)`.
- `BR_raw_long = count(completed independent long-side bets per year)`.
- Pre-observation planning default:
  `BR_raw_long_prior = skill_count * timeframe_count * 12`.
- With 5 skills and 2 timeframes, the default is `120`, not `240`.

Correlation adjustment:

- `N_eff_signal` is computed from the canonical K3 estimator once available.
- `BR_eff_long = BR_raw_long * min(1, N_eff_signal / K_signal)`.
- If `N_eff_signal` is unavailable, FLAM planning must use the conservative
  placeholder `BR_eff_long = 0.40 * BR_raw_long` and mark the result as provisional.

IC_long controls:

- Prior range `0.03-0.05` is not evidence and cannot be used to pass a gate.
- If observed WFO `IC_long < 0.03`, report `LOW_EDGE_FLAG`.
- If observed WFO `IC_long > 0.05`, report `HIGH_IC_SUSPECT_FLAG`.
- While `HIGH_IC_SUSPECT_FLAG` is active, reports must include a haircuted IC:
  `IC_long_haircuted = IC_long_observed - 0.015`.
- Phase-gate evidence must show both observed and haircuted FLAM calculations when
  the suspect flag is active.

FLAM reporting:

`IR_long_planning = IC_long_used * sqrt(BR_eff_long)`

Reporting rules:

- Raw and adjusted BR must both be shown.
- `BR_long = 240` must be removed unless an empirical trade-count derivation proves it.
- Reports must state whether IC/BR values are prior, paper, WFO OOS, or live.

### Required Evidence To Close

- `CHARTER.md`, `PROTOCOL_SPEC.md`, and `GLOSSARY.md` correct the BR arithmetic.
- `IC_long` suspect and low-edge controls are added beside `IC_short` controls.
- A worked example shows 5 skills, 2 timeframes, `BR_raw=120`, `N_eff/K=0.4`, and
  the resulting `BR_eff=48`.
- Audit rerun confirms FLAM-derived claims cannot use unadjusted 240-breadth planning.

---

## F-30 - RDL Queue Runtime Telemetry

### Finding

The RDL queue policy now exists in text, but closure requires telemetry evidence
that FIFO, monthly cap, and shock-control behavior are actually demonstrated.

### Recommended Decision

Do not mark F-30 closed with documentation alone. Define the telemetry contract now;
close only after generated evidence exists.

### Required Evidence Contract

Every RDL promotion event must log:

- `promotion_event_id`
- `rdl_trial_id`
- `family_tag`
- `trial_registry_submission_ts`
- `promotion_ts`
- `promotion_month`
- `queue_rank_before_promotion`
- `selected_rank`
- `fifo_exception_id` or null
- `M_total_before`
- `M_total_after`
- `rolling_30d_M_total_delta`
- `shock_control_state`
- `haircut_impact_note_hash` or null
- `actor`
- `policy_hash`

Required audit checks:

- `rdl_fifo_check`: no promoted item has a newer submission timestamp than an
  unpromoted eligible item in the same queue, unless `fifo_exception_id` is present.
- `rdl_monthly_cap_check`: count of new `RDL-*` active-evaluation promotions per
  calendar month is `<= 3`, excluding explicitly rejected attempts.
- `rdl_shock_control_check`: if `rolling_30d_M_total_delta > 10`, promotion is
  paused until `haircut_impact_note_hash` is present.

### Required Evidence To Close

- Schema or artifact contract is canonical.
- Real generated telemetry evidence demonstrates FIFO, cap, and shock-control
  checks.
- A review report cites the artifact and marks F-30 closed.

---

## F-31 - K-Report Epoch Coverage

### Finding

The freeze-safe `evaluation_epoch_id` rule exists, but closure requires evidence
that every K1-K6 report includes epoch tags and mixed windows show per-epoch slices.

### Recommended Decision

Do not mark F-31 closed with documentation alone. Define the K-report evidence
contract now; close only after generated evidence exists.

### Required Evidence Contract

Every K1-K6 report must include:

- `report_id`
- `kill_id`
- `window_start_ts`
- `window_end_ts`
- `evaluation_epoch_ids`
- `aggregate_metric`
- `aggregate_sample_count`
- `per_epoch_slices`
- `policy_hash`
- `code_hash`
- `dataset_hash`
- `generated_at`

Every `per_epoch_slices` entry must include:

- `evaluation_epoch_id`
- `slice_start_ts`
- `slice_end_ts`
- `metric_value`
- `sample_count`
- `policy_hash`

Required audit checks:

- `k_report_epoch_presence_check`: every K1-K6 report has at least one
  `evaluation_epoch_id`.
- `mixed_epoch_slice_check`: every report spanning more than one epoch includes
  per-epoch slices before the aggregate metric.
- `no_epoch_reset_check`: epoch transitions do not reset, pause, or alter frozen
  kill-window thresholds.

### Required Evidence To Close

- Schema or artifact contract is canonical.
- Real generated K-report evidence demonstrates per-epoch slices when a mixed
  epoch report exists.
- A review report cites the artifact and marks F-31 closed.

---

## T15 Entry Rule Under D-015

T15 may start only when all of the following are true:

1. D-015 is recorded in `products/entropy-core/docs/DECISION_LOG.md`.
2. A focused audit review verifies the canonical mitigations for F-1, F-2, F-4,
   and F-5, or explicitly rejects them and keeps T15 blocked.
3. The same review records that F-30 and F-31 remain In Progress future
   real-evidence gates and are not closed for T15.
4. `products/entropy-core/docs/CODEX_PROMPT.md` is updated to name T15 as next task only after F-1,
   F-2, F-4, and F-5 pass the focused audit.

These conditions were satisfied by D-016 on 2026-05-03. T15 may proceed within
the cost-model scope guard recorded in `products/entropy-core/docs/CODEX_PROMPT.md`.

---

## T15 Cost-Model Constraints Once Unblocked

When T15 becomes legal to implement, the cost model should use these additional
engineering constraints:

- Pessimistic defaults: use explicit cost floors rather than optimistic zeros.
- Every cost component is separately returned and logged.
- Parameters are versioned in `CostModelConfig` with `method_id`, `policy_hash`, and
  `simbroker_version`.
- Funding, borrow, slippage, and impact are never silently omitted; unavailable
  inputs must produce explicit zero-with-reason or missing-input status.
- Tests include high-turnover sensitivity examples, not only one small fill.
- Any vectorization or performance work stays in Python until D-012 profiling gates
  justify language escalation.

These constraints are not substitutes for D-010 closure; they are implementation
guardrails after closure.
