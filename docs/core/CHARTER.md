# Entropy Protocol — Project Charter
**Classification:** Confidential — Internal Strategic Document
**Filename:** `CHARTER.md` (stable; no version in filename — version tracked in header)
**Version:** 5.3
**Date:** 2026-05-03
**Basis:** v2.0 findings, v3.0 extensions, v4.0 audit (authoritative corrections applied)
**Supersedes:** `strategic_charter_v5.md` (archived)
**Next review:** End of Phase 0 (evaluation engine complete)

**v5.2 change summary:** Applied D-010 closure-packet mitigations for formula-bearing implementation blockers: corrected long-side breadth arithmetic, clarified `CI-SR-ACF-v1` interpretation, locked `HL-HB-v1` as the multiplicity control for gates, added IC_long controls, and summarized deterministic `P4-RBL-v1`. No kill threshold or phase-exit threshold was changed.
**v5.3 change summary:** Clarified deterministic `P4-RBL-v1` computational conventions for weekly resampling, volatility, percentile rank, efficiency-ratio zero handling, and label artifacts. No P4 threshold, kill threshold, phase-exit threshold, or cost-model rule was changed.

---

## PREAMBLE: V4 MANDATORY CORRECTIONS (Applied Before v5 Scope Adds)

v4 identified 3 mandatory corrections. All are resolved here. v5 is built on the corrected foundation. No new scope is added until these are closed.

---

### Correction 1: FLAM Derivation (v4 Section 1.3 — Fixed)

**What v3 did:** Applied `IR = IC × sqrt(BR_short)` to the short sleeve in isolation, yielding +0.31 gross. This is wrong — it computes the Sharpe of a short-only portfolio, not the marginal contribution to an existing long portfolio.

**Correct formula:**
```
Delta_IR = IC_short × [sqrt(BR_long + BR_short) - sqrt(BR_long)]
```

**With explicit inputs:**
- BR_long raw prior = 120 bets/year (5 skills × 2 timeframes × 12 months)
- BR_short ≈ 60 bets/year (5 short positions/month × 12 months)
- IC_short = 0.02–0.03 (conservative; liquid assets with squeeze noise; v4 Section 4.1 — NOT 0.04 which was the unsupported v3 assumption)

```
Delta_IR = 0.025 × [sqrt(180) - sqrt(120)] = 0.025 × 2.46 ≈ +0.062 gross
```

After costs (funding drag, borrow, stop-loss turnover at corrected stop model):

**Corrected net Sharpe delta from short positions: +0.01–0.05**

The v3 lower bound of +0.04 is revised to +0.01. The +0.31 intermediate step is voided. All downstream planning that assumed +0.04 as a floor must be updated. Any FLAM planning must show raw breadth and correlation-adjusted breadth; unadjusted `BR_long = 240` is void unless later empirical trade-count evidence proves it.

---

### Correction 2: Kill K4 Redesigned (v4 Section 5.3 — Fixed)

**What v3 did:** K4 triggered if short-side P&L is negative in aggregate after 12 months. At IC_short = 0.025, 60 trades, expected t ≈ 0.19 — well below any significance threshold. P(false kill on a marginally positive IC=0.025 strategy) ≈ 44%. This is a coin flip, not a kill criterion.

**Replacement K4:**
> Kill K4: Short-side t-statistic < 0.5 after 18 months AND ≥90 completed short-side trades → retire short positions; revert to long-only + 1W overlay.

**Known limitation acknowledged:** At IC_short = 0.025 on 90 trades, expected t ≈ 0.24. P(false kill at t < 0.5 threshold) ≈ 60%. This is still too high for a definitive kill. The criterion is accepted as a **screening threshold** (too underpowered to be probative at this sample), not a statistical test. Its function is to terminate a non-working short book early enough to redirect development capacity. The alternative — waiting for a 90% powered test — requires ~1000 short trades and is incompatible with a solo development timeline. Accepted as a deliberate tradeoff.

---

### Correction 3: Stop-Loss Asset-Class Specific (v4 Section 4.3 — Fixed)

**What v3 did:** LS-3 specified a 4% hard stop for all short positions. For crypto assets (daily vol 2–4%), the 4% stop implies E[τ] ≈ (4/3)² ≈ 1.8 days before first passage. Result: ~10–15 stop events/month per crypto short position. Turnover cost alone at 5 positions × 12 stop events × 0.05% fee × 4% avg weight ≈ 1.2% NAV/month = 14.4% NAV/year. This eliminates all expected short-side value before alpha is even computed. The v3 turnover estimate of 0.3–0.8 RT/month was wrong by an order of magnitude.

**Replacement LS-3:**

| Asset class | Daily vol | Hard stop | Expected hold | Expected stops/month/position |
|---|---|---|---|---|
| Equity shorts | 0.8–1.5% | 4–6% from entry | 3–8 days | 0.5–2 |
| Crypto perpetual shorts | 2–4% | 12–18% from entry OR 3× 5-day ATR (wider) | 5–15 days | 1.5–3 |

**Revised cost model for crypto shorts (corrected):**
With 12–18% stop: 5 active positions × 2 stop events/month × 0.05% fee × 4% avg weight = 0.020% NAV/month = 0.24% NAV/year from stop turnover alone. Manageable, but funding drag is still the primary cost driver (see Phase 4).

Any reference to a 4% stop on crypto assets in v3 is voided.

---

## DELIVERABLE 1: STRATEGIC CHARTER v5

### A) Classification

**Primary:** Research Lab (Era 0–2)
**Conditional destination:** Capital Allocation Framework (Era 3+)
**CONFIRMED. No change from v3.**

Rationale for CAF (not reclassified):
The system's realistic mature form combines moderate trading alpha (net Sharpe 0.28–0.42 base case), regime-driven risk controls, and treasury yield on idle capital (stream d, separately accounted). This is a Capital Allocation Framework. A CAF is viable at trading Sharpe 0.25–0.35 combined with 3–5% treasury yield if risk controls genuinely enforce the ≤20% DD target. A Niche Alpha Engine at the same Sharpe is not viable — it cannot justify its operational complexity.

The Hypothesis Acceleration Track does not change the classification. It is an internal research methodology within the Research Lab phase.

**Probability estimates (heuristic ranges; not point estimates):**

| Outcome | 18 months | 30 months | Primary driver |
|---|---|---|---|
| Research Lab (baseline) | 85–90% | 95% | Solo execution continuity |
| Capital Allocation Framework | 20–32% | 40–55% | Portfolio layer + treasury accounting discipline |
| Niche Alpha Engine | 12–20% | 25–35% | Net Sharpe ≥ 0.50 confirmed OOS |
| Statistically Fragile (unverifiable) | 35–45% | 20–28% | Evaluation engine rigor |

These ranges are unchanged from v3 because v4's audit of intermediate Sharpe calculations does not materially move the terminal probability distribution. The uncertainty on the 20–32% range itself is ±8–12 pp.

---

### B) Non-Negotiables

The following cannot be modified without a full charter-level review. Changes to non-negotiables require a written justification document, not inline edits.

**NN-1: Gross leverage ≤ 1.0 at all times**
|long| + |short| ≤ 100% NAV. Hard structural rule, not a risk limit. Short positions substitute for long positions; they do not supplement them. A portfolio that is 70% long + 30% short has gross = 1.0. A portfolio that is 80% long + 30% short has gross = 1.1 — prohibited.

**NN-2: Four-stream P&L attribution (permanent, from v2/v3)**
Every performance report must decompose P&L into exactly four streams. These streams are NEVER blended in primary metrics:
- **(a)** Long position P&L (entries and exits from long signals)
- **(b)** Short position P&L (entries and exits from short signals)
- **(c)** Borrow/funding cost P&L (equity borrow + crypto perpetual funding — separate line from (b))
- **(d)** Treasury yield P&L (idle capital; separate from trading book entirely)

The primary performance metric (net Sharpe) is computed on streams (a)+(b)+(c) only. "Total portfolio return" including stream (d) is a secondary figure, labeled explicitly. K5 triggers if (d) > 60% of total in any 12-month period.

**NN-3: Evaluation engine first**
No signal is evaluated as "working" without passing through the walk-forward harness with proper OOS separation. The evaluation engine is a prerequisite for any edge claim, not a future enhancement. Phase 0 is non-negotiable.

**NN-4: Sequential rollout (unchanged from v3)**
Implementation sequence: long-only baseline (4H/1D) → 1W overlay → equity shorts → crypto perp shorts → treasury. No phase begins before the prior phase meets exit criteria. No parallel execution of phases with capital at risk.

The Acceleration Track runs in parallel with Phase 0 only. It is paper-only and does not bypass phase sequencing for the main evaluation path.

**NNN-5: Trial registry + multiplicity correction**
Every signal specification tested must be pre-registered before any data is examined. Harvey-Liu deflation is mandatory when net Sharpe < 0.40. Deflated Sharpe is reported alongside raw Sharpe in all evaluation reports. Trial count is visible in the evaluation log at all times.

**NN-6: Asset-class-specific stop-loss parameters (NEW — from v4 Correction 3)**
- Equity shorts: hard stop 4–6% from entry
- Crypto shorts: hard stop 12–18% from entry OR 3× 5-day realized ATR, whichever is wider

These parameters are fixed for the current era. Modifications require a pre-registered stop-loss hypothesis, evaluated through the Acceleration Track before Main Track adoption.

---

### C) Definitions

**"Net Sharpe":**
```
Net Sharpe = mean(annual returns of active trading book) / stdev(annual returns of active trading book)
```
Where:
- *Active trading book* = streams (a) + (b) + (c). Stream (d) excluded.
- *Costs included*: transaction fees, borrow costs, crypto funding costs, stop-loss turnover costs
- *Costs excluded*: infrastructure costs, LLM/API costs, developer time (tracked separately for K2)
- *Annualization*: 252 trading days regardless of timeframe. 4H bars use 6 bars/day.
- *Reporting*: always include 68% confidence interval using canonical method `CI-SR-ACF-v1` (autocorrelation-consistent). CI is mandatory uncertainty disclosure and does not override frozen kill thresholds.
- *CI interpretation*: at 15 months OOS, a 0.30-Sharpe system has a zero-autocorrelation 68% CI half-width near 0.91, not 0.15–0.20. K1 is a policy screen, not a powered statistical proof at this horizon.

**"Harvey-Liu deflation":**
Canonical method ID is `HL-HB-v1`, a Holm-Bonferroni family-wise error-rate workflow for phase-gate decisions. Main Track, Acceleration Track, and `RDL-*` trials count in the same family budget at Trial Registry submission time. Reports must include `M_total`, family membership, raw p-value, adjusted p-value, raw Sharpe, deflated Sharpe, and haircut units. DSR-style or BHY/FDR-style values may be reported as secondary diagnostics only.

**"IC_long and breadth controls":**
IC_long = 0.03–0.05 is a planning prior only, not gate evidence. Observed WFO `IC_long < 0.03` raises `LOW_EDGE_FLAG`; observed WFO `IC_long > 0.05` raises `HIGH_IC_SUSPECT_FLAG` and requires a 0.015 IC haircut view. Planning default `BR_raw_long = skill_count × timeframe_count × 12`, so 5 skills × 2 timeframes × 12 = 120. FLAM reports must also show `BR_eff_long = BR_raw_long × min(1, N_eff_signal / K_signal)` once the K3 estimator is audit-locked; until then they must use conservative placeholder `BR_eff_long = 0.40 × BR_raw_long`.

**"OOS (Out-of-Sample)":**
Chronologically after the last training/calibration window, with strict enforcement:
- Walk-forward test windows do not overlap calibration windows for any parameter
- Regime labels, feature normalization, and portfolio weights computed using only information available at the start of each test window
- OOS data begins accumulating after Phase 0 exit criteria are met
- **Paper trading results from the Acceleration Track are NOT OOS.** They are labeled "AT-[ID]" and tracked separately.

**"Paper trading":**
Live signal generation on real-time or near-real-time data, no capital at risk, fills logged at SimBroker-estimated execution prices. Paper results labeled "Paper" in all reports, never combined with walk-forward OOS results.

**"Regime":**
A market state classification produced by the authoritative signal hierarchy (Section D). A regime instance requires ≥8 consecutive weeks to count for OOS spanning requirements. Fragments < 8 weeks are excluded from spanning calculations.

**"Cost model components" (explicit):**
| Component | Base rate | Stress rate | Notes |
|---|---|---|---|
| Equity commissions | 0.08%/leg | same | Per-leg basis |
| Crypto spot/perp taker fee | 0.05%/leg | same | Per-leg basis |
| Equity borrow | 1.5% annualized | flag > 5% | Position-size weighted |
| Crypto perp funding (neutral) | 0.02%/8hr (~22% ann.) | — | Base case |
| Crypto perp funding (trending-bull) | 0.05%–0.15%/8hr (55–165% ann.) | — | NOT a tail; routine in bull phases |
| Market impact | 0.02%/fill | — | Liquid assets at target sizes |
| Slippage buffer | 0.02%/fill | — | Additional buffer |

**Excluded from cost model** (separate tracking only): infrastructure, API/LLM costs, developer time.

---

### D) Regime Signal Governance (Resolves v4 Section 5.1)

**Problem from v4:** v3 introduced four regime-adjacent signals (1W overlay, daily ρ trigger, 12% DD breaker, LS-4 funding exit) with no conflict resolution protocol. This de facto abandoned the v2 "single authoritative regime signal" principle without acknowledging it.

**Resolution:** The v2 single-signal principle is replaced with a **layered precedence hierarchy**. The v2 goal (preventing definitional drift) is preserved through the explicit ordering. The practical multi-layer design is preserved because these signals operate on incompatible time horizons and cannot sensibly be collapsed into one.

**Strict precedence order (highest = P1, lowest = P4):**

| Priority | Signal | Trigger condition | Action taken | Overrides |
|---|---|---|---|---|
| **P1** | Hard DD circuit breaker | Realized DD from HWM ≥ 12% | Reduce all positions to 50% immediately; suspend new additions for 5 business days | All lower |
| **P2** | Funding exit (crypto perps) | Crypto perp funding > 0.05%/8hr for ≥3 consecutive windows | Exit all crypto short positions | P3, P4 |
| **P3** | Daily correlation trigger | 20-day rolling avg pairwise ρ > 0.55 | Reduce gross exposure 35–50% over 3 business days | P4 |
| **P4** | Weekly regime overlay | 1W signal state (trending / mean-reverting / stress) | Adjust skill routing and allocation targets | Nothing |

**Conflict resolution rules (explicit):**
1. Higher-priority signal always takes precedence. P1 active + P4 says "maintain trending allocation" → P1 wins. P3 active + P4 says "add long" → P3 wins; no new longs added at pre-reduction size.
2. Signals do not combine multiplicatively. P3 fires (reduce 35–50%) → the P3-reduced book is what P4 routing applies to. P4 routing applies within the reduced book.
3. Recovery from a higher-priority signal requires the trigger condition to clear for a defined window:
   - P1 recovery: HWM gap < 8% AND ≥5 business days elapsed
   - P2 recovery: funding < 0.03%/8hr for ≥5 consecutive windows (hysteresis: re-entry threshold is 0.03%, not 0.05%)
   - P3 recovery: 20-day ρ < 0.45 (hysteresis band = 0.10; not the same as trigger threshold)
   - P4 state: changes on weekly close; no recovery period

**Deterministic P3 protocol (normative):**
- Correlation population: active Phase universe assets with valid returns at decision timestamp.
- Return interval: daily close-to-close log returns.
- Estimator: Pearson correlation on 20-day window; minimum 15 valid observations.
- Aggregation: simple mean of upper-triangle pairwise correlations.
- Action mapping:
  - if `0.55 < rho_avg <= 0.65` -> gross reduction 35%;
  - if `rho_avg > 0.65` -> gross reduction 50%.
- Ramp rule: linear over 3 business days; ramp progress logged each day.

**Concurrent transition semantics (P1/P3/P4):**
- If P1 activates during a P3 ramp, pause the ramp and freeze progress.
- If P1 clears while P3 is still active, resume paused P3 ramp from frozen progress.
- While P1 is active, P4 updates are track-only (logged) and do not alter effective exposure.
- Transition logs must include prior state, next state, reason code, and policy hash.

**Regime label immutability:**
Regime labels applied to historical OOS windows are frozen at evaluation time. A recalibration of the 1W signal in Phase 2 does not retroactively update Phase 1 regime labels. Performance reports reference the signal version active at evaluation time.
For each reported window, store label vintage artifact:
`{p4_version, p4_param_hash, calibration_end_ts, label_generation_ts, dataset_hash}`.

**Deterministic P4 protocol:**
Canonical P4 method ID is `P4-RBL-v1`: a rule-based weekly labeler with no fitted parameters. Labels are assigned from UTC daily OHLCV resampled to locked weekly bars, using only data available at or before the weekly close. No label is valid until 156 completed weekly bars exist; warmup windows are `UNLABELED` and do not count toward regime-spanning evidence. The three labels are assigned by priority:
1. `stress` if 4-week return <= -8%, 26-week drawdown <= -15%, or trailing 13-week volatility percentile >= 80% with 4-week return < -3%.
2. `trending` if not stress and abs(13-week return) >= 8% and 13-week efficiency ratio >= 0.35.
3. `mean_reverting` otherwise.
Weekly resampling uses `p4_weekly_resample_v1`: `weekday` datasets use complete ISO Monday-Friday weeks; `continuous` datasets use complete ISO Monday-Sunday weeks. Weekly bars use first open, max high, min low, last close, and sum volume. `vol_13w` uses sample standard deviation with `ddof=1`; volatility percentile uses weak percentile rank `count(x <= current) / count(x)` over computable trailing values in completed weeks `t-155..t`; zero efficiency-ratio denominators map to `eff_13w = 0`.
The parameter set is hashed as `p4_param_hash`; `calibration_end_ts = null` because no fitting is performed. Every label artifact includes the calendar profile and `p4_weekly_resample_version`.

---

## DELIVERABLE 2: PROJECT STAGES v5 (Main Track)

---

### Phase 0: Integrity & Evaluation Engine

**Primary objective:** Build the measurement infrastructure before any signal is tested. No signal receives an "OOS" evaluation label before Phase 0 exit criteria are met.

**Frozen:** walk-forward harness architecture, leakage audit checklist, trial registry schema, SimBroker cost model structure
**Can change:** technology stack choices, data provider (if quality equivalent)

**Exit criteria (all required):**
- [ ] Walk-forward harness passes leakage audit: zero forward-looking features verified by temporal shuffling test
- [ ] SimBroker fills within 15% of market bid/ask data on ≥100 manually verified fills across representative assets
- [ ] Trial registry operational: every test run logged with parameters, data hash, date, result
- [ ] Data pipeline stable: zero unexplained gaps in target universe over ≥90 continuous days of feed monitoring
- [ ] P4 (weekly regime signal) produces historically labeled regime series covering ≥3 years of 1D data on ≥15 of 20 target assets
- [ ] DD circuit breaker (P1) logic implemented, tested with synthetic data, and verified

**No kill criteria in Phase 0.** If infrastructure cannot be built, Phase 1 does not start. There is no partial Phase 0.

**Realistic duration:** 8–16 weeks at 20–40 hrs/week.

---

### Phase 1: Long-Only Baseline (4H–1D)

**Primary objective:** Establish a net Sharpe baseline for the 5–6 base skill set. This becomes the control benchmark that every subsequent extension must beat.

**Frozen:** skill count (max 6; expansion only with OOS Sharpe marginal contribution > 0.05); evaluation methodology; cost model; trial registry discipline
**Can change:** individual skill parameters within pre-registered bounds; portfolio construction weights within the portfolio layer framework

**Required sample size:**
- Primary: ≥15 months walk-forward OOS spanning ≥2 distinct regime instances (≥8 weeks each)
- Secondary: ≥250 completed trades through the evaluation engine for per-trade MAE/MFE analysis
- Context: at 15 months, report 68% CI via `CI-SR-ACF-v1`. Point estimate remains informative, not final; K1 is a policy screen and is not statistically well-powered at this horizon.

**Metrics and thresholds:**

| Metric | Target | Kill / Flag |
|---|---|---|
| Net Sharpe (streams a+b+c) | ≥ 0.28 point estimate | K1: < 0.28 after 15 mo / 2 regimes |
| Calmar ratio (Sharpe / max DD) | ≥ 0.25 | Flag if < 0.15 for 2 consecutive quarters |
| Maximum DD | < 20% in any calendar quarter | Kill if breached |
| Factor N_eff | ≥ 3 after DR + correlation clustering | K3: N_eff ≤ 2 after 3+ months DR precondition and 2 consecutive monthly checkpoints |
| Harvey-Liu deflated Sharpe | Reported alongside raw; haircut < 0.05 | Flag if haircut > 0.08 |
| SimBroker cost accuracy | Within 15% of paper fills | Flag if > 15% for 2 consecutive months |

**Kill criteria:**
- **K1:** Net OOS Sharpe < 0.28 (point estimate) after 15 months spanning ≥2 regimes → project kill review
- **K2:** Infrastructure + LLM costs > 50% of simulated monthly gross return (at target AUM) for 2 consecutive quarters → cost structure review; likely kill
- **K3:** N_eff ≤ 2 after 3+ months of DR monitoring + correlation clustering → factor collapse; kill or radical universe reduction

**Pivot criterion (not a kill):** Net Sharpe is 0.22–0.28 but improving monotonically across sequential 6-month windows. Continuation requires a written causal theory for the improvement and a testable correction hypothesis registered before the next evaluation window.

**Phase 1 exit criteria (all required):**
- [ ] 15 months OOS spanning ≥2 regimes completed
- [ ] Net Sharpe point estimate ≥ 0.28
- [ ] Max DD not breached in OOS period
- [ ] SimBroker cost accuracy confirmed within 15%
- [ ] Harvey-Liu haircut < 0.05 Sharpe units
- [ ] K1, K2, K3 not triggered

---

### Phase 2: 1W Regime Overlay

**Primary objective:** Test whether the 1W regime signal, applied as overlay only, improves net Sharpe vs Phase 1 baseline. Primary hypothesis: fewer false-trigger deleveraging events.

**Frozen:** Phase 1 skill set; Phase 1 cost model; P1–P3 signal hierarchy; four-stream P&L
**Can change:** P4 weekly overlay parameters within pre-registered bounds

**Scope constraint:** 1W overlay limited to ≤2 skill instances with 1W-informed position sizing. No new full skill tier for 1W.

**Pre-Phase 2 requirement:** Compute empirical IC correlations across signal types at 4H, 1D, 1W on target universe for ≥3 years. This replaces the uncited ρ(4H,1W) = 0.25–0.50 from v3. If realized IC correlation ρ(4H,1W) > 0.65, the N_eff improvement from 1W is below the justification threshold for the maintenance overhead.

**Required sample size:**
- ≥6 months paper comparison vs Phase 1 benchmark (same entry signals; Phase 1 exits vs Phase 2 exits with overlay active)
- ≥80 comparable trade pairs (same entry signal, different overlay state)
- Context: at 80 pairs, CI on Sharpe delta ≈ ±0.12. The 1W overlay cannot be definitively validated at 6 months. Phase 2 screens for plausibility, not confirmation.

**Metrics and thresholds:**

| Metric | Target | Kill / Flag |
|---|---|---|
| Net Sharpe delta (Phase 2 vs Phase 1, matched) | ≥ 0.01 (non-negative) | Kill: negative delta in matched comparison |
| False-trigger reduction | ≥ 20% reduction in P3 events reversed within 5 business days | Flag if < 10% |
| Turnover impact | Phase 2 RT/month ≤ Phase 1 RT/month | Kill if turnover increases |
| Empirical IC correlation ρ(4H,1W) | < 0.60 | Do not advance Phase 2 if > 0.65 |

**Kill criteria (Phase 2-specific):**
- **P2K1:** Turnover increases with 1W overlay active → retire overlay; return to Phase 1 baseline
- **P2K2:** False-trigger reduction < 10% after 6 months without a registered causal explanation → retire overlay

**Phase 2 exit criteria (all required):**
- [ ] 6 months paper comparison completed; ≥80 matched trade pairs
- [ ] Empirical ρ(4H,1W) computed and < 0.60
- [ ] Net Sharpe delta ≥ 0 in matched comparison
- [ ] Phase 1 exit criteria remain satisfied during Phase 2 period
- [ ] P2K1 and P2K2 not triggered

---

### Phase 3: Equity Shorts (Paper First; Gross ≤ 1)

**Primary objective:** Test whether equity short positions, substituted for long positions, improve portfolio-level net Sharpe at gross ≤ 1.0. Paper trading required before any capital at risk.

**Frozen:** gross ≤ 1.0; four-stream P&L; Phase 1–2 baseline as control; equity stop model (4–6%); no crypto shorts in Phase 3
**Can change:** short signal specifications within pre-registered bounds; short book allocation (0–30% of gross); equity borrow estimates as live market quotes become available

**Short-side IC assumption (explicit):**
IC_short = 0.02–0.03 is the working prior for liquid equity shorts. If walk-forward evaluation produces IC_short > 0.04, treat as suspect (possible overfitting); apply a 0.015 haircut before reporting. Do not use IC_short = IC_long as a default.

**Required sample size:**
- Primary: ≥12 months paper trading, ≥90 completed short-side trades
- K4 is evaluated at 18 months if 90 trades not reached at 12 months
- Context: at 90 trades, IC_short = 0.025 produces expected t ≈ 0.24. This is a screening threshold, not a significance test.

**Metrics and thresholds:**

| Metric | Target | Kill / Flag |
|---|---|---|
| Short-side t-statistic | ≥ 0.5 after 18mo / 90 trades | K4: < 0.5 → retire shorts |
| Net Sharpe delta (streams a+b+c vs Phase 2 baseline) | ≥ 0 point estimate | Flag if negative for 2 consecutive quarters |
| Gross leverage (paper record) | Never > 1.0 | Hard fail if any breach recorded |
| SimBroker borrow cost accuracy | Within 20% of market quotes | K6: > 20% for 2 consecutive months |
| Harvey-Liu haircut (short-side trial count) | All short specs logged; haircut reported | Flag if haircut > 0.08 |

**Kill criteria:**
- **K4 (fixed):** Short-side t-statistic < 0.5 after 18 months AND ≥90 short-side trades → retire short positions; revert to Phase 2 (long-only + 1W overlay)
- **K6:** SimBroker short-cost model diverges > 20% from realized paper-fill costs for 2 consecutive months → halt; recalibrate before resuming

**Phase 3 exit criteria (all required):**
- [ ] ≥12 months paper; ≥90 completed short-side trades
- [ ] Short-side t-statistic ≥ 0.5
- [ ] Net Sharpe delta (3-stream) ≥ 0 vs Phase 2 baseline
- [ ] SimBroker borrow accuracy confirmed (< 20% deviation)
- [ ] Gross ≤ 1.0 maintained throughout paper record
- [ ] K4 and K6 not triggered

---

### Phase 4: Crypto Perpetual Shorts (Optional — Phase 3 Required)

**Primary objective:** Test whether crypto perp shorts add portfolio-level net Sharpe, net of funding drag. **Base planning assumption: Phase 4 is bypassed.** The expected value of crypto perp shorts may be negative in sustained bull markets.

**Prerequisite:** Phase 3 exit criteria fully met. Crypto shorts are a distinct asset class with qualitatively different cost structure from equity shorts.

**Frozen:** all Phase 1–3 baselines; four-stream P&L; gross ≤ 1.0; crypto-specific stop model (12–18% or 3× ATR)
**Can change:** LS-4 funding exit threshold (currently 0.05%/8hr; may be tightened to 0.03%/8hr if Phase 4 evaluation shows funding costs dominating)

**Funding drag analysis (explicit — v4 Section 4.2 corrected):**
Assume 30% short book, 50% in crypto perps, average funding 15% annualized (conservative for any period with sustained bullish crypto sentiment; not a tail scenario):
```
Funding drag = 0.30 × 0.50 × 15% = 2.25% NAV/year
```
Corrected FLAM marginal contribution at IC_short = 0.025: +0.046 gross Sharpe ≈ +0.55% additional return at 12% portfolio vol.
**Funding drag (2.25%) > expected gross benefit (0.55%). The net expected value is negative under this scenario.** This is the primary risk of Phase 4 and must be tracked explicitly from day 1.

Phase 4 is only justified empirically if realized funding rates are materially below this base-case assumption.

**Basis risk note (v4 Section 4.4 — not addressed in v3):** Crypto perpetual prices can deviate materially from spot during stress events. This creates P&L variance that does not appear in spot OHLCV backtests and is not captured in the standard cost model. The evaluation engine must track perp-vs-spot basis daily.

**Required sample size:**
- ≥12 months paper; ≥60 completed crypto short-side trades
- Funding cost logged at 8-hour resolution throughout

**Kill criteria (Phase 4-specific):**
- **P4K1:** Trailing 3-month funding drag (stream c, crypto component) > 2.5% NAV annualized rate → pause crypto shorts; evaluate whether market regime warrants suspension
- **P4K2:** Combined short book (equity + crypto) net Sharpe delta vs Phase 2 baseline < 0 over rolling 6-month window for 2 consecutive windows → retire crypto shorts; equity shorts continue per Phase 3 rules
- **K6:** applies here with the same 20% deviation threshold

**Phase 4 exit criteria (all required):**
- [ ] ≥12 months paper; ≥60 crypto short trades
- [ ] Net Sharpe delta (vs Phase 3 baseline) ≥ 0 at point estimate, accounting for full funding cost
- [ ] Average realized funding cost ≤ 2.0% NAV annualized over evaluation period
- [ ] Perp-vs-spot basis tracked and non-disqualifying (< 1.0% persistent deviation)
- [ ] K4, K6, P4K1, P4K2 not triggered

---

### Phase 5: Treasury Activation

**Primary objective:** Activate treasury yield on idle capital after trading alpha is independently validated. Never blend.

**Prerequisites:** Phase 1 exit criteria met AND ≥3 months of live capital trading data with net Sharpe ≥ 0.28.

**Instruments:** T-Bill equivalents or Tier-1 PoS staking (ETH, SOL) only. No exchange lending programs. No high-yield protocols.

**Permanent rules:**
- Treasury P&L (stream d) is never included in the primary net Sharpe metric
- Treasury is reported in total portfolio return only, with explicit labeling
- K5: treasury yield > 60% of total return in any 12-month period → strategic review; evaluate treasury-only allocation as alternative

---

## DELIVERABLE 3: HYPOTHESIS ACCELERATION TRACK (2–3 Months)

### Purpose and Separation

**Why it exists:** Phase 1 requires ≥15 months OOS before actionable results. Waiting with no feedback loop is both demotivating and wasteful — paper trading can generate early signals if the hypotheses are properly scoped and separated.

**Critical separation from Main Track:**
- AT results do NOT substitute for Phase 1 OOS evaluation
- AT results CANNOT be combined with walk-forward OOS data
- AT results are labeled "AT-[hypothesis ID]" in all reports — never "OOS"
- Promotion of an AT hypothesis to the main skill set requires passing the full Phase 1 evaluation protocol

**The Acceleration Track runs in parallel with Phase 0 only.** It is paper-only and does not bypass phase sequencing.

---

### What Can Be Validated in 2–3 Months

**Validatable (per-trade, measurable):**

| Question | Measurable? | Minimum sample | Inference quality |
|---|---|---|---|
| Does exit overlay at key level improve per-trade P&L vs baseline exit? | Yes | 40+ matched trade pairs | Suggestive at 40 pairs (CI ≈ ±0.3 R on mean difference) |
| What is the MAE/MFE distribution for each skill type? | Yes | 60+ trades | Descriptive; informs stop/TP calibration |
| How often does each stop variant trigger? | Yes | 40+ stop events | Rate estimate ±15–20 pp |
| Does SimBroker fill model match paper fills? | Yes | Continuous | Bias correction if systematic deviation > 5% |
| Does an influencer's setup type have systematic signal? | Yes (if pre-registered) | 40+ setup instances | Highly provisional; screening only |

**Cannot be validated in 2–3 months (explicitly stated):**

| Claim | Why not validatable |
|---|---|
| Net Sharpe estimate with tight CI | CI at 3 months ≈ ±0.30–0.50 — statistically inert |
| Multi-regime robustness | 3 months cannot span 2 regime instances by construction |
| Factor independence claims | Correlation structure requires longer period and larger cross-section |
| Any kill criterion evaluation | All kill criteria are 12–18 month windows |
| "The system is working" | 3 months of paper results is hypothesis screening, not validation |

**Minimum viable sample targets (heuristics, not guarantees):**
- 100–150 paper trades: early inference bands on per-trade expectancy (CI ≈ ±0.5 R at 80% confidence)
- 40+ matched trade pairs: exit overlay comparison (CI on mean P&L difference ≈ ±0.3 R)
- 30+ stop events: stop-trigger frequency estimate (rate CI ≈ ±15–20 pp)

State these as heuristic minimums in all reports, not confidence thresholds.

---

### Decisions That Can Be Made at 2–3 Months vs Cannot

**Decisions that can be made at 2–3 months:**
- Which exit overlay variants are worth advancing to Phase 1 evaluation (plausibility screen)
- Whether a specific stop variant fires so frequently it is disqualified by turnover alone
- Whether SimBroker cost model needs recalibration before Phase 1 begins
- Whether an influencer-derived setup has a base rate sufficient to be worth systematic testing
- Which key levels appear most frequently in the MAE/MFE profiles (informing pre-registration for Phase 1)

**Decisions that cannot be made at 2–3 months:**
- Whether any skill has positive net Sharpe
- Whether the portfolio is viable
- Whether any regime detection approach is working
- Whether the system meets any kill criterion (in either direction — cannot be confirmed or denied)
- Whether to deploy capital (this requires Phase 1 exit criteria)

---

### Hypothesis Pre-Registration Protocol

Each AT hypothesis requires a one-page spec before any data from the evaluation window is examined. The spec is filed in the trial registry and is version-locked.

**Required fields:**
1. **AT-ID:** Sequential (AT-001, AT-002, ...)
2. **Hypothesis statement:** Specific, falsifiable, testable on paper trades
3. **Entry condition:** Locked; cannot change after registration
4. **Exit condition being tested:** The hypothesis variable
5. **Baseline exit:** The control condition (must be paper-traded in parallel)
6. **Pre-specified metric:** Computable from trade log
7. **Pre-specified threshold:** What value must be observed to classify as "promising" (not "validated")
8. **Minimum sample:** Trades required before evaluation is performed
9. **Expiry:** Evaluation at this date OR sample target, whichever is later
10. **Origin tag:** Internal hypothesis (AT-IND) or influencer-derived (AT-INF-[source type])

---

### Influencer-Derived Hypothesis Safeguards

External sources are legitimate hypothesis generators but high-bias sources. Mandatory controls:

**Safeguard 1: Rule-first, chart-second**
The systematic rule must be written in precise terms before any recent price data is examined. "Buy when weekly close > 52-week high" is systematic. "Buy when price looks ready to break" is not testable.

**Safeguard 2: Historical base rate pre-check**
Before registration, compute the historical base rate of the stated setup condition on target assets over ≥3 years. This prevents testing setups that occurred once in the sample period and cannot generate ≥40 instances.

**Safeguard 3: 60-day embargo on recent history**
The entry condition must be defined on data older than 60 days relative to the registration date. This prevents fitting the hypothesis to the market move that motivated the influencer's post.

**Safeguard 4: Separate tracking**
AT-INF hypotheses tracked separately from AT-IND. If AT-INF promotion rate is systematically higher than AT-IND (adjusted for sample), flag as potential reverse-engineering bias.

**What influencer strategies may inform:** hypothesis generation, identification of common reference levels (e.g., "community uses weekly H/L as TP"), narrative context for regime identification.

**What they must not do:** determine the evaluation window, determine which data to look at before hypothesis formation, or bypass the pre-registration requirement.

---

### How Acceleration Track Results Feed Main Track

An AT hypothesis may be promoted to Main Track evaluation if and only if:
1. Pre-registered threshold was met on the pre-specified metric
2. A matching Phase 1 comparison test is pre-registered before any Main Track data for that dimension is examined
3. The Harvey-Liu trial count includes all AT hypotheses tested for the same signal dimension
4. The Phase 1 baseline (no-overlay) P&L is computed first, before the overlay result is evaluated

"Promising AT result → Phase 1 entry" is NOT "AT validated → deploy." The Main Track evaluation protocol is mandatory.

---

## DELIVERABLE 4: LEVEL-BASED TAKE-PROFIT INTEGRATION

### Classification: Exit Overlays, Not Strategy Change

Level-based TPs modify only when an existing position exits. They do not change:
- The entry condition (generated by Phase 1 skills)
- The position sizing (governed by portfolio layer)
- The regime state (governed by P1–P4 hierarchy)

They are parameters within the exit component of the skill framework. They are tested as AT hypotheses, not as new strategies.

---

### Taxonomy of Exit Level Types

**Category 1: Price-History Levels (static within window, no optimization)**

| Level | Definition | Update frequency | Testable hypothesis |
|---|---|---|---|
| Monthly High/Low (prior month) | Last business day of prior month | Monthly | AT-001: TP at monthly H/L improves per-trade expectancy vs N-bar exit |
| Weekly High/Low (prior week) | At weekly close | Weekly | AT-002: TP at weekly H/L improves per-trade expectancy |
| Daily High/Low (prior day) | At daily close | Daily | AT-003: TP at prior-day H/L improves per-trade expectancy |

Rationale: these are non-optimized, derived from a rule applied at entry time. Their potential value comes from self-fulfilling liquidity (many participants use the same reference). This is an empirical claim, not an assumption.

**Category 2: Volatility-Adjusted Levels (dynamic; no fixed-pip bias)**

| Level | Definition | Notes |
|---|---|---|
| ATR-multiple (1×, 1.5×, 2× ATR) | N× realized ATR at entry | Most defensible: adapts to asset vol |
| VWAP (session/daily) | Standard VWAP calculation | Commonly used institutional reference |
| MA proximity bands (20MA, 50MA, 200MA ± 1%) | Moving average at entry | Common institutional reference level |

ATR-multiple targets are the highest-priority Category 2 test. They generalize across assets without per-asset calibration.

**Category 3: Derived Combinations (deferred)**

- VWAP ± 1× ATR bands
- Volume-profile S/R zones

Category 3 is not entered until Category 1 and 2 hypotheses complete AT evaluation. More parameters = more overfitting surface.

---

### Anti-Overfitting Rules (Hard Constraints)

**Rule 1: Max 3 exit overlay hypotheses in active evaluation simultaneously per quarter.**
More than 3 creates a search problem requiring full combinatorial multiplicity correction. The trial count accrues against the Harvey-Liu budget.

**Rule 2: Fixed entry during exit testing.**
Entry signal is version-controlled and locked before any exit overlay hypothesis is registered. If entry signal changes, all active exit overlay tests are invalidated and must be re-registered.

**Rule 3: One dimension at a time.**
A hypothesis tests either the level type (monthly H/L vs weekly H/L) OR the ATR multiple (1× vs 1.5×), never both simultaneously. Combined parameter searches require full combinatorial correction.

**Rule 4: Baseline must run in parallel.**
The baseline exit (e.g., N-bar holding period or signal reversal) is paper-traded in parallel during every exit overlay test. The overlay must exceed the baseline by the pre-registered threshold on the pre-registered metric. No cherry-picking evaluation windows.

**Rule 5: No level adjustment during trade.**
The TP level is computed deterministically at entry time from historical data. Mid-trade adjustment based on new price information makes the exit discretionary and unstatistical.

---

### Expected Incremental Value

The expected incremental Sharpe from exit overlays is small and uncertain:
- Literature range for exit optimization in systematic trend-following: +0.03–0.10 Sharpe units gross
- After multiplicity correction for N=3 simultaneously tested variants: effective range ≈ +0.01–0.05
- Realistic expected net contribution if a level effect exists: **+0.01–0.05 Sharpe units**

This is worth testing because the cost is low (pre-registered paper trading) and the benefit is permanent once validated. It is not a primary alpha driver.

---

## DELIVERABLE 5: FINAL DECISIONS

### Verdict: Conditional Proceed

The architecture is sound. The sequencing is correct. The non-negotiables are the right constraints. The Acceleration Track provides a credible path to early learning without contaminating the main evaluation path. The extensions (1W, shorts) are properly scoped and sequenced.

**Proceed immediately on:**
- Phase 0 (start now; this is the highest-leverage activity in the project)
- Hypothesis Acceleration Track (run in parallel with Phase 0; paper-only)
- Exit overlay hypothesis registration: AT-001 (monthly H/L), AT-002 (weekly H/L), AT-003 (ATR-multiple) — first quarter batch

**Proceed conditionally on (sequence-gated):**
- Phase 1: after Phase 0 exit criteria met
- Phase 2: after Phase 1 exit criteria met
- Phase 3: after Phase 2 exit criteria met
- Phase 4: after Phase 3 exit criteria met AND funding drag analysis is non-disqualifying at time of entry decision
- Phase 5 (treasury): after Phase 1 exit criteria met AND ≥3 months live capital data

---

### 3 Mandatory Corrections (Apply Before Any Phase Begins)

**Mandatory 1: FLAM corrected (from v4 Correction 1)**
Delete any planning reference to "+0.04–0.10 net Sharpe delta from shorts" as a floor. The corrected lower bound is +0.01. The corrected gross intermediate step is +0.046 (not +0.31). Internal documents, spreadsheets, and feasibility models must be updated before Phase 3 scoping begins. Proceeding with the wrong floor creates a systematically overoptimistic case for investing development time in the short extension.

**Mandatory 2: Kill K4 redesigned (from v4 Correction 2)**
Replace "negative aggregate short P&L after 12 months" with "t-statistic < 0.5 after 18 months AND ≥90 short-side trades." Log the known limitation (60% false-kill probability at IC=0.025) explicitly in the kill criterion documentation. The criterion is accepted as a screening threshold, not a statistical test.

**Mandatory 3: Asset-class-specific stops implemented before Phase 3 (from v4 Correction 3)**
The SimBroker must implement separate stop models for equity vs crypto shorts before any short-side paper trading begins in Phase 3. Running Phase 3 paper trading with a uniform 4% stop produces systematically understated turnover costs, which contaminates the Phase 3 cost evaluation.

---

### 3 Things Explicitly Deferred

**Deferred 1: Phase 4 (Crypto perp shorts)**
Not on the active roadmap. Available conditionally after Phase 3 validation. The base planning assumption is Phase 4 is bypassed. The expected value of crypto perp shorts in any sustained bull crypto environment is negative to neutral. Do not schedule Phase 4. Keep it as a documented option, not a committed phase.

**Deferred 2: CCA as live portfolio influencer**
Chief Context Agent remains a dashboard research tool. No live portfolio influence until Phase 1–3 validated AND ≥300 resolved InsightHypothesis objects with outcome tracking. That is a multi-year data accumulation requirement. Do not scope CCA integration during Era 1–3 development.

**Deferred 3: Three-axis source scoring (reduce to one axis)**
The full Predictive Skill / Tradability Skill / Regime Timing Skill scoring framework (3-axis) is deferred until source sample sizes reach 50+ resolved calls per source. Until then, one axis only: directional accuracy with Brier score. Adding axis complexity before sufficient data exists is overhead with no return.

---

## DELTA SUMMARY: V4 → V5

| Topic | V4 state | V5 resolution | Action required |
|---|---|---|---|
| FLAM derivation (C1) | Formula error; +0.31 gross claimed; lower bound floor +0.04 | Fixed: +0.046 gross marginal; net lower bound +0.01 | Update all planning documents; remove +0.31 |
| Kill K4 | Sign-based; ~44% false-kill on IC=0.025 | t-stat < 0.5 after 18mo/90 trades; 60% false-kill acknowledged | Replace K4 definition in evaluation engine |
| Stop-loss for crypto | 4% hard stop; turnover underestimated 10–30× | Equity 4–6%, Crypto 12–18% or 3× ATR; revised cost model | SimBroker must implement before Phase 3 |
| Regime signal conflicts | 4 signals, no precedence; v2 principle abandoned | Explicit P1–P4 hierarchy with triggers, hysteresis, recovery rules | Document in evaluation engine spec |
| Crypto funding drag | 0.5–2.0% annual stated; understates realistic bull-phase scenario | Modeled at 15% avg annualized for bull phases; Phase 4 EV may be negative | Flag in Phase 4 entry decision |
| DD probability tables | Point estimates with ±15pp uncertainty stated as results | Heuristic ranges with explicit uncertainty bands; no false precision | Remove point estimates from v3 table; report as ranges |
| Combined Sharpe delta arithmetic | +0.04–0.10 combined without derivation of interaction term | Not provided as a combined estimate; components stated separately with explicit IC/BR assumptions | No combined estimate in planning until Phase 2–3 empirical data |
| Hypothesis validation | Not addressed | Acceleration Track: 2–3 month paper, pre-registration, bias safeguards, explicit scope limits | New process to implement in parallel with Phase 0 |
| Level-based TPs | Not addressed | Classified as exit overlays; taxonomy + anti-overfitting rules; AT-001–003 as first batch | Register AT hypotheses in trial registry |
| Short-side IC assumption | IC_short = IC_long = 0.04 (hidden, unsupported) | IC_short = 0.02–0.03 as explicit working prior; > 0.04 treated as suspect | Update FLAM calculations and cost model |
| Maintenance burden arithmetic | 9–17 vs 71 hrs/month inconsistency (v4 Section 5.4) | Resolved: v2 base 15–40 hrs/month; Phase 3–4 adds 10–18 hrs → total 25–58 hrs/month | Solo feasibility threshold: 25 hrs/month viable; 58 hrs/month requires near-full-time |
| SimBroker bootstrap gap | Circular: validate against paper trading before paper trading exists | Acknowledged: Phase 0 validates SimBroker against market bid/ask data directly; paper trading validation supplements but does not bootstrap | Phase 0 exit criterion updated accordingly |

---

## APPENDIX: KILL CRITERIA CONSOLIDATED REFERENCE

| ID | Trigger | Action | Phase active |
|---|---|---|---|
| **K1** | Net OOS Sharpe < 0.28 (point estimate) after 15 months spanning ≥2 regimes | Project kill review | Phase 1+ |
| **K2** | Infrastructure + LLM costs > 50% of simulated monthly gross (target AUM) for 2 consecutive quarters | Cost review; likely kill | Phase 1+ |
| **K3** | N_eff ≤ 2 after 3+ months of DR monitoring + correlation clustering | Factor collapse; kill or radical universe reduction | Phase 1+ |
| **K4** | Short-side t-statistic < 0.5 after 18 months AND ≥90 short-side trades | Retire short positions; revert to Phase 2 | Phase 3 |
| **K5** | Treasury yield > 60% of total return in any 12-month period | Strategic review; evaluate treasury-only alternative | Phase 5 |
| **K6** | SimBroker short-cost model diverges > 20% from realized paper-fill costs for 2 consecutive months | Halt short development; recalibrate | Phase 3–4 |
| **P2K1** | Turnover increases with 1W overlay active | Retire 1W overlay; revert to Phase 1 | Phase 2 |
| **P2K2** | False-trigger reduction < 10% after 6 months, no registered causal explanation | Retire 1W overlay | Phase 2 |
| **P4K1** | Trailing 3-month funding drag (crypto stream c) > 2.5% NAV annualized | Pause crypto shorts; regime review | Phase 4 |
| **P4K2** | Combined short book Sharpe delta vs Phase 2 baseline < 0 for 2 consecutive 6-month rolling windows | Retire crypto shorts; continue equity shorts per Phase 3 | Phase 4 |

---

*Document Version: 5.3 | Date: 2026-05-03 | Supersedes: v3.0 (extensions), v4.0 (audit findings incorporated); v5.2 applies D-010 formula-bearing implementation mitigations; v5.3 applies deterministic P4 computational conventions*
*Next scheduled review: End of Phase 0 (evaluation engine complete)*
*Classification: Confidential — Internal Strategic Document*
