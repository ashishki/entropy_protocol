# Entropy Protocol — Adversarial Review

**Classification:** Confidential — Internal Audit Document  
**Filename:** `docs/audit/ADVERSARIAL_REVIEW.md`  
**Audit Cycle:** Cycle 1 — Phase 0 (Pre-Development)  
**Pipeline Step:** Step 5 — Adversarial Review  
**Pipeline Version:** v1.0  
**Date:** 2026-03-04  
**Status:** Draft — Awaiting Spec Owner Acceptance

---

## Executive Summary

Total challenge groups assessed: **6 (A-F)**  
CRITICAL findings: **9**  
Severity split: **P0: 9, P1: 10, P2: 7**

Dominant silent-failure theme: the spec can produce internally consistent-looking results that are statistically non-discriminative (K1), structurally non-reproducible (P4), or governance-fragile (RBE/RDL boundaries) without any explicit rule being broken.

---

## A. Formula Derivation Challenges

### A1 — Sharpe CI at 15 months OOS

Given in prompt:
- `SE(SR_annual) = sqrt((1 + SR^2/2) / T)`
- `SR = 0.30`, `T = 1.25 years`

Derivation:
- `SR^2/2 = 0.09/2 = 0.045`
- `(1 + SR^2/2) = 1.045`
- `1.045 / 1.25 = 0.836`
- `SE = sqrt(0.836) = 0.914`
- 68% CI half-width approximately `+-0.914`

Comparison:
- Spec claim: `+-0.15` to `+-0.20`
- Error factor vs derived CI: `0.914/0.20 = 4.57x` to `0.914/0.15 = 6.09x`
- Verdict: **CRITICAL (wrong by ~4.6x-6.1x)**

Required T for target CI widths:
- For `+-0.20`: `T = 1.045 / 0.20^2 = 26.125 years`
- For `+-0.15`: `T = 1.045 / 0.15^2 = 46.44 years`

K1 distinguishability cascade:
- Threshold 0.28 is not statistically separable from 0.22-0.30 at 15 months under derived SE.
- Power-style checks (one-sided kill, normal approximation):
  - `P(kill | SR_true=0) = P(SR_hat < 0.28)` with `SE~0.894` = `Phi(0.313) = 0.623`
  - `P(kill | SR_true=0.15)` with `SE~0.899` = `Phi(0.145) = 0.558`
- Conclusion: K1 has weak discrimination between dead and marginal systems at the stated horizon.

### A2 — FLAM gross Sharpe with N_eff correction

Spec inconsistency:
- `5 x 2 x 12 = 120`, but text states `~240`.

Using registry-consistent assumption from prior audit context:
- `BR_eff = N_eff x 40` (implied by `N_eff=2.4 -> BR_eff~96`)

Case 1: equicorrelation at `rho_avg=0.30`, `N_eff~2.4`
- `BR_eff = 2.4 x 40 = 96`
- `sqrt(BR_eff) = 9.798`
- If `IC_long=0.03`, `IR_gross ~ 0.03 x 9.798 = 0.294`

Case 2: equicorrelation at `rho_avg=0.40`, `N_eff~1.8`
- `BR_eff = 1.8 x 40 = 72`
- `sqrt(BR_eff) = 8.485`
- `IR_gross(IC=0.03) ~ 0.255` (< K1 0.28)

Case 3: eigenvalue-style `N_eff~3.0`
- `BR_eff = 3.0 x 40 = 120`
- `sqrt(120)=10.954`
- `IR_gross(IC=0.03) ~ 0.329`

Conclusion:
- Formula choice and BR interpretation can flip K1-adjacent conclusions.
- Verdict: **CRITICAL** at phase-gate level.

### A3 — K4 t-stat calibration

Candidate formulas:
- (a) `t = mean(r) / (sd(r)/sqrt(N))`
- (b) `t = IC_short x sqrt(BR_short)`
- (c) `t = SR_short_annual x sqrt(T)`

Given spec statement: expected `t~0.24` at `N~90` with short-edge assumptions.
- Formula (b) yields `0.025 x sqrt(90) = 0.237` (matches), so implied family is IC-root-N style.

Dead short book (`IC=0`, df~89):
- `P(t < 0.5) ~ 0.69`
- Missed-kill `P(t >= 0.5) ~ 0.31`

Borderline (`IC=0.01`, mean t~0.095, normal approx):
- `P(t > 0.5) ~ 0.34` (false-persist)

Compared to spec text:
- `P(false kill)~60%` for marginal positive book is directionally consistent with current threshold regime.

Conclusion:
- K4 is a screening rule, not a statistical kill test.
- Verdict: **P1 critical calibration weakness**.

### A4 — Harvey-Liu haircut with RDL trial inflation

Scenario count:
- Base skills/timeframes: `10-12`
- AT overlays: `3`
- RDL submissions: `10`
- Total trial count `M ~ 23-25`

Adversarial implication by correction family (raw Sharpe 0.35):
- Bonferroni/Holm-class strict corrections at `M~24` would imply very severe effective thresholds (haircuts likely far above 0.08 Sharpe units).
- BHY/FDR-class would still produce material haircut at this `M`.
- DSR-style penalties are model-dependent but non-trivial at this multiplicity.

Key result:
- Without a locked formula, the same raw Sharpe can map to "acceptable" or "disqualifying" depending on variant.
- Spec thresholds (`<0.05` and `>0.08`) are uninterpretable without the variant definition.
- Verdict: **CRITICAL (F-1 remains blocking)**.

### A5 — N_eff formula comparison at K3 boundary

Given portfolio:
- 3 clusters, 2 assets each (k=6)
- Within-cluster rho=0.60
- Between-cluster rho=0.20

Weighted average rho:
- Total pairs `C(6,2)=15`
- Within pairs: `3 x 0.60 = 1.8`
- Between pairs: `12 x 0.20 = 2.4`
- `rho_avg = (1.8+2.4)/15 = 0.28`

Equicorrelation N_eff:
- `N_eff = 6 / (1 + 5x0.28) = 6/2.4 = 2.50`

Eigenvalue participation-ratio N_eff:
- Block-structured matrix eigenvalues: `[2.4, 1.2, 1.2, 0.4, 0.4, 0.4]`
- `N_eff = (sum lambda)^2 / sum(lambda^2) = 36 / 9.12 = 3.95`

Conclusion:
- Same portfolio yields `N_eff=2.5` vs `3.95` depending on formula.
- K3 boundary decision can diverge materially.
- Verdict: **CRITICAL for deterministic K3 governance**.

---

## B. State Machine Stress Tests

### B1 — P1/P3 concurrent states (A-D)

State A: P1 clears while P3 still active
- Deterministic outcome in spec: **No**
- Plausible implementations:
  1. Resume to P3-reduced target immediately
  2. Resume to post-P1 baseline then apply fresh P3 reduction
- Worst-case mismatch: exposure and trade count divergence during recovery windows.

State B: P3 triggers during P1 5-day suspension
- Deterministic outcome in spec: **No**
- Plausible implementations:
  1. Apply P3 on already-halved book (`50% x (0.5..0.65)`)
  2. Queue P3 until P1 clears
- Worst-case mismatch: 17.5-25 gross-point difference during stress.

State C: P1 fires mid P3 ramp
- Deterministic outcome in spec: **No**
- Plausible implementations:
  1. Hard reset to P1 state, discard ramp progress
  2. Preserve ramp state machine and continue after suspension
- Worst-case mismatch: different realized DD and turnover profiles.

State D: P4 state changes during active P1
- Deterministic outcome in spec: **No**
- Plausible implementations:
  1. Track-only during P1 freeze
  2. Apply P4 routing internally to constrained 50% book
- Worst-case mismatch: non-comparable attribution across eval vs paper.

### B2 — RBE activation during K1 evaluation period
- Explicit rule preventing overlap: **Not found**.
- Window reset/extension rule for K1 under RBE changes: **Not found**.
- Can RBE alter measured K1 outcome? **Yes**, through changed volatility/allocations without formal window governance.
- Verdict: **P1 interaction gap (RS-15)**.

### B3 — RDL promotion at Phase 2 activation
- Immediate eligibility of scaffolded hypotheses: **Ambiguous**.
- Promotion queue requirement: **Not specified**.
- Haircut impact if all promoted together: multiplicity shock at phase boundary; could spike deflation abruptly.
- Verdict: **P0 governance ambiguity with multiplicity side effects**.

### B4 — Phase 2 P4 recalibration + vintage contamination
- Overlap of Phase-0 P4 calibration with Phase-1 IS windows: structurally likely for any fitted P4 model.
- New vs old label coexistence across Phase 1 and Phase 2 comparisons: ambiguity persists.
- Developer could claim technically compliant but semantically mismatched comparisons.
- Verdict: **P0 certification contamination risk (F-7)**.

---

## C. Kill Criterion Calibration Audit

| Kill ID | Threshold | False-kill rate derivation | Missed-kill rate derivation | >30%? | Power adequate? |
|---|---|---|---|---|---|
| K1 | SR_hat < 0.28 at 15mo | `P(SR_hat<0.28|SR_true=0.30)` ~49% using derived SE | `P(SR_hat>=0.28|SR_true=0/0.15)` ~38-44% range | Yes | No |
| K2 | Cost ratio >50% for 2Q | `p_fp^2` (noise model unspecified) | `1-p_tp^2` | Unknown (likely high under noisy cost estimates) | Unknown |
| K3 | N_eff<=2 with temporal rule | Depends on N_eff estimator variance + formula | Same | Unknown / potentially high near boundary | No (formula not locked) |
| K4 | t<0.5 at 18mo and n>=90 | ~60% (spec-stated marginal-case false kill) | ~31% missed kill for dead book | Yes | No |
| K5 | Treasury >60% in 12mo | Depends on windowing/attribution noise | Depends on same | Unknown | Unknown |
| K6 | Cost deviation >20% for 2 months | `p_fp^2` (estimator protocol missing) | `1-p_tp^2` | Unknown | Unknown |
| P2K1 | Turnover increase | Sign test undefined | Sign test undefined | Unknown | Low |
| P2K2 | False-trigger reduction <10% | Metric definition unclear | Metric definition unclear | Unknown | Low |
| P4K1 | Funding drag >2.5% annualized, trailing 3mo | Estimator variance unspecified | Same | Unknown | Medium |
| P4K2 | Delta<0 for 2x6mo windows | `q^2` with unknown q | `1-r^2` with unknown r | Unknown | Low-Medium |

Special focus results:
- **K1** and **K4** explicitly exceed 30% error rates under plausible/derived assumptions.
- **K3** remains non-deterministic until formula is locked.

---

## D. Evaluation-vs-Execution Divergence Points

### D1 — P3 reduction range (35-50%)
- Baseline gross: 90%
- 35% reduction target: `90 x (1-0.35)=58.5`
- 50% reduction target: `90 x (1-0.50)=45.0`
- Mismatch: **13.5 gross points** per trigger episode.
- If P3 fires ~3 times/year, exposure and turnover statistics can diverge materially across implementations.

### D2 — Purge/embargo range from "proportional" wording
- 4H max-hold 5d -> plausible embargo range `5-15 days`
- 1D max-hold 20d -> plausible embargo range `20-60 days`
- Short embargo implementation can inflate apparent OOS by leakage bleed; long embargo reduces sample and power.

### D3 — HWM reset timing
- Interpretation A: phase-boundary reset
- Interpretation B: annual reset
- Interpretation C: inception-to-date HWM
- Same P&L path can generate different P1 trigger counts by definition choice alone.

### D4 — Phase 2 matched-pair definition
- Pairing by signal type vs calendar proximity yields different sample composition.
- Without locked pair rule, overlay delta can shift materially while staying "compliant".

---

## E. Behavioral Integrity Gaps

### E1 — GE-2 vs GE-3 classification for zero-weight skills
- Decision point: classify de-facto skill removal as allocation-only (`GE-2`) or signal-modification (`GE-3`).
- Impact: undercounted trials by the number of unregistered removals (example: 3 removals).
- Worst-case: lower reported deflation and false pass of haircut thresholds.
- Closing rule: "Any sustained zero-weight >= one rebalance cycle for a previously active skill is GE-3 and trial-counted."

### E2 — IC_long lacks suspect threshold
- Decision point: report high IC_long as overfitting risk vs strong edge.
- Impact: optimistic interpretation bias in phase-go/no-go narrative.
- Closing rule: add IC_long suspect threshold and mandatory haircut/flag protocol, symmetric to IC_short governance.

### E3 — Solo "charter-level review"
- Decision point: same actor proposes, approves, and activates RBE.
- Impact: governance collapses into self-authorization; auditability degrades.
- Closing rule: require explicit review artifact with external sign-off requirement (or predefined independent check template with locked evidence fields).

### E4 — K5 window choice
- Decision point: rolling 12-month vs calendar-year interpretation.
- Impact: calendar-year choice can suppress trigger incidence when treasury spikes straddle year boundaries.
- Closing rule: canonical rolling-window definition with fixed evaluation cadence.

---

## F. Open Question Resolution Review (Q1-Q10)

| Q-ID | Question summary | Addressed in spec? | Completeness | Phase gate blocked? |
|---|---|---|---|---|
| Q1 | HL variant + cross-phase trial aggregation | No | None | Yes (Phase 1 gating) |
| Q2 | CI derivation for ±0.15-0.20 claim | No | None | Yes (Phase 1 gating) |
| Q3 | P3 population/interval definition | No | None | Yes (Phase 0->1 implementation validity) |
| Q4 | Full P4 algorithm specification | No | None | Yes (Phase 0->1, Phase 1->2) |
| Q5 | P4 fitting + vintage handling | No | None | Yes (Phase 1 regime-span validity) |
| Q6 | N_eff formula for K3 | Partial | Incomplete | Yes (Phase 1 kill determinism) |
| Q7 | P1+P3 nested state rules | No | None | Yes (execution determinism in Phase 1+) |
| Q8 | K4 t-stat formula details | No | None | Yes (Phase 3 certification validity) |
| Q9 | Phase 2 matched-pair definition | No | None | Yes (Phase 2 exit validity) |
| Q10 | Purge/embargo formula by timeframe | No | None | Yes (Phase 0 leakage audit integrity) |

Conclusion: **All Q1-Q10 remain unresolved at formula/spec level.**

---

## Phase Gate Impact

### Findings that must be resolved before Phase 0 exit can be certified

1. **F-4 / Q4-Q5 (P4 algorithm + vintage protocol)**
- Certification mechanism required: reproducible P4 specification + versioned labeling procedure; independent reproduction test over historical sample.

2. **F-3 / Q3 (P3 population definition)**
- Certification mechanism required: one canonical population/interval definition in PROTOCOL_SPEC + test harness assertions.

3. **F-12 / Q10 (purge/embargo formula)**
- Certification mechanism required: explicit formula by timeframe in glossary/spec + leakage checklist parameter lock.

4. **F-2 / Q2 (Sharpe CI correction)**
- Certification mechanism required: corrected CI method and updated decision interpretation notes; explicit method section for reporting.

5. **F-1 / Q1 (Harvey-Liu formula + aggregation scope)**
- Certification mechanism required: locked formula variant, trial-count policy, and deterministic computation procedure.

### Findings required before Phase 1 exit certification

- **F-11 / Q6**: lock N_eff formula for K3.
- **F-10 / Q7**: close concurrent state-machine transition gaps.
- **F-9**: add Phase-1 cost-kill policy or formally justify omission.

Without these closures, a Phase 0 or Phase 1 gate decision can appear compliant while remaining non-reproducible or statistically invalid.

