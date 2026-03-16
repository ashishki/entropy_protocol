# Entropy Protocol — Quantitative Research Integrity Audit

**Classification:** Confidential — Internal Review Document
**Filename:** `AUDIT_v1.md`
**Version:** 1.0
**Date:** 2026-03-04
**Auditor role:** Staff-Level Quantitative Research Systems Architect
**Documents reviewed:** CHARTER.md v5.0, PROTOCOL_SPEC.md v1.1, GLOSSARY.md v1.0, EVOLUTION.md v1.0, ARCHITECT_BRIEF.md v1.0
**Status:** Awaiting author responses to Open Questions

---

## FINDINGS SUMMARY

**Dominant risk theme:** The evaluation system's evidentiary backbone — the Sharpe confidence interval, the Harvey-Liu correction, and the P4 regime classifier — are each underspecified or miscalculated in ways that will produce invalid performance claims without the failure being detectable at Phase 1 exit.

**Finding count:**
- CRITICAL: 5
- HIGH: 6
- MEDIUM: 7
- LOW: 3
- **Total: 21**

---

## FINDINGS

---

### [CRITICAL] F-1: Harvey-Liu Formula Variant Not Specified

**LOCATION:** CHARTER.md NN-5; PROTOCOL_SPEC.md NN-5, Section J (Kill Criteria), Phase 1 metrics table; GLOSSARY.md ("Deflated Sharpe (Harvey-Liu)")

**OBSERVED:** The specification mandates Harvey-Liu deflation when net Sharpe < 0.40, requires the deflated Sharpe to be reported alongside raw Sharpe in all evaluation outputs, and requires the trial count to be visible at all times. No formula is provided.

**PROBLEM:** "Harvey-Liu" refers to a family of correction methods from Harvey and Liu (2015) ("Backtesting"). The paper presents multiple variants: a Bonferroni correction, a Holm-Bonferroni correction, and the authors' preferred BHY approach. Each produces a materially different haircut for the same trial count. Furthermore, the "Deflated Sharpe Ratio" cited in GLOSSARY.md is a distinct construction from López de Prado (2018) that requires additional parameters: T (length of the backtest in years), ρ (mean correlation between test statistics), and the full distribution of SR estimates across trials. None of these parameters are specified. The formula for δ (mean pairwise correlation between test returns across trials) is particularly problematic: it requires data that may not be logged at the trial level.

Without specifying: (a) which Harvey-Liu variant, (b) the formula and its inputs, (c) the aggregation rule for cross-phase trial counts, and (d) whether AT trials count toward the same budget as Phase 1 trials for the same signal dimension — the mandated correction cannot be correctly implemented, verified, or audited.

**EVIDENCE:**
- CHARTER.md NN-5: "Harvey-Liu deflation is mandatory when net Sharpe < 0.40. Deflated Sharpe is reported alongside raw Sharpe in all evaluation reports."
- GLOSSARY.md: "Deflated Sharpe (Harvey-Liu): Net Sharpe with a haircut applied to account for the number of strategies tested in the trial registry. Mandatory when net Sharpe < 0.40."
- PROTOCOL_SPEC.md Phase 1 metrics: "Harvey-Liu deflated Sharpe | Reported alongside raw; haircut < 0.05 | Flag if haircut > 0.08."
- No document contains a formula or parameter specification.
- ARCHITECT_BRIEF.md Q12: "How would you implement trial count aggregation in a way that is robust to partial registry entries?" — this question is listed as open and unresolved, directly confirming the gap.

**IMPACT:** (A) Invalid performance claims. The Harvey-Liu haircut flag threshold (<0.05 Sharpe units, flag if >0.08) is used as a Phase 1 exit criterion gating condition. If the formula is implemented incorrectly — using the wrong variant, the wrong trial count, or the wrong cross-phase aggregation — the declared haircut is meaningless, the Phase 1 exit criterion becomes unverifiable, and the multiplicity correction provides a false sense of rigor rather than actual protection.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED] The formula gap is not acknowledged in any document. ARCHITECT_BRIEF Q12 approaches but does not state it.

---

### [CRITICAL] F-2: Sharpe Confidence Interval Claim Is Materially Wrong

**LOCATION:** CHARTER.md Section C ("Net Sharpe" definition); PROTOCOL_SPEC.md Sections C, F (Phase 1), H; GLOSSARY.md ("Net Sharpe")

**OBSERVED:** All three documents state: "At 15 months OOS, CI ≈ ±0.15–0.20 for a ~0.30-Sharpe system (68%)." This figure is cited as the basis for the "pivot criterion" (0.22–0.28 range interpretable as distinct from kill threshold) and for framing Phase 2's ±0.12 comparison.

**PROBLEM:** The standard asymptotic formula for the standard error of the annualized Sharpe ratio is:

```
SE(SR_annual) = sqrt((1 + SR²/2) / T)
```

where T is the number of years of OOS data.

**Computation for 15 months OOS, SR = 0.30:**

```
T = 15/12 = 1.25 years
SE = sqrt((1 + 0.30²/2) / 1.25)
   = sqrt((1 + 0.045) / 1.25)
   = sqrt(1.045 / 1.25)
   = sqrt(0.836)
   = 0.914
```

The 68% CI at 15 months OOS is approximately **±0.91**, not ±0.15–0.20.

Cross-check using daily returns (T = 15/12 × 252 = 315 trading days):

```
SR_daily = 0.30 / sqrt(252) ≈ 0.019
SE_daily = sqrt((1 + 0.019²/2) / 315) ≈ sqrt(0.003175) ≈ 0.0563
SE_annual = 0.0563 × sqrt(252) ≈ 0.894
```

Result: ±0.89. The stated ±0.15–0.20 would require approximately T = (1 + SR²/2) / (0.175²) ≈ 1.045 / 0.0306 ≈ **34 years** of annual observations to achieve — not 15 months. The stated CI is 4–6× too small by any standard treatment.

The comparison Phase 2 CI of ±0.12 at "80 trade pairs" is plausibly computed as SE ≈ sqrt(1/80) ≈ 0.112, treating trade pairs as independent observations. This is not the CI on the annual Sharpe ratio — it is the CI on the mean per-trade P&L difference in trade-return units. The Phase 1 CI (±0.15–0.20 stated for the annual Sharpe) and the Phase 2 CI (±0.12 stated for the "Sharpe delta" over matched pairs) are computed on incommensurable scales.

**EVIDENCE:**
- CHARTER.md: "at 15 months, CI on net Sharpe ≈ ±0.15–0.20 (68%). The point estimate is informative, not final."
- PROTOCOL_SPEC.md Phase 1: "At 15 months OOS, CI on net Sharpe ≈ ±0.15–0.20 (68%). The point estimate is informative, not final."
- GLOSSARY.md: "Always reported with 68% confidence interval. At 15 months OOS, CI ≈ ±0.15–0.20 for a 0.30-Sharpe system."
- Stated derivation: none across all five documents.

**IMPACT:** (A) (B) Invalid performance claims and incorrect kill decisions. The consequences are threefold:

1. **K1 false-kill and missed-kill rates are uncalibrated.** With true CI ≈ ±0.91, a system at true Sharpe 0.15 has P(point estimate ≥ 0.28) ≈ P(Z ≥ (0.28–0.15)/0.91) ≈ P(Z ≥ 0.14) ≈ 0.44. A failing system has a 44% chance of NOT triggering K1. Conversely, a viable system at true Sharpe 0.40 has P(point estimate < 0.28) ≈ P(Z < (0.28–0.40)/0.91) ≈ P(Z < –0.13) ≈ 0.45. K1 is effectively a coin flip at the relevant effect sizes given the actual sample.

2. **The pivot criterion (0.22–0.28) is statistically indistinguishable from the kill threshold (0.28)** when the true CI is ±0.91. The 0.06 gap between pivot and kill is 7% of the CI width — not a meaningful distinction.

3. **All CI-referenced evaluation reports will overstate precision by a factor of 4–6×**, creating systematically overconfident performance claims.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED] No document acknowledges any uncertainty about this CI calculation, and no derivation is provided.

---

### [CRITICAL] F-3: P3 Correlation Trigger Population Undefined

**LOCATION:** CHARTER.md Section D; PROTOCOL_SPEC.md Section D; GLOSSARY.md ("Regime Signal Hierarchy (P1–P4)"); ARCHITECT_BRIEF.md Section C

**OBSERVED:** P3 trigger condition across all documents: "20-day rolling avg pairwise ρ > 0.55."

**PROBLEM:** The population over which pairwise ρ is computed is never specified. Candidate definitions — each producing materially different trigger frequencies — include:

- All 20 assets in the target universe (asset price correlations)
- All currently active long positions (subset of universe)
- All active positions including shorts (after Phase 3)
- Skill-level P&L pairwise correlations (5–6 skills × 2 timeframes)
- Cluster-level P&L correlations (post-clustering output from Submodule 2)

The choice is not trivial. A cross-asset universe including crypto majors and equities in 2022 would have pairwise ρ_avg well above 0.55 by asset price correlations for extended periods, triggering P3 continuously. The same portfolio measured by skill P&L correlation might sit at 0.30–0.40. These are distinct objects: P3 would operate at fundamentally different frequencies depending on the definition.

Additionally: after Phase 3 introduces short positions, the inclusion/exclusion of short position correlations with long positions in the pairwise calculation further alters P3's trigger behavior. The specification is silent on this.

**EVIDENCE:**
- CHARTER.md Section D: "20-day rolling avg pairwise ρ > 0.55 | Reduce gross exposure 35–50% over 3 business days"
- PROTOCOL_SPEC.md Section D: identical language
- ARCHITECT_BRIEF.md C: identical language, no population specification
- PROTOCOL_SPEC.md Section I, Q14: "Is the P3 recovery threshold (ρ < 0.45) appropriate for the target universe?" — listed as an open external question but does not acknowledge the population definition gap

**IMPACT:** (C) Undetected state corruption. Without a defined population, P3 can be triggered inconsistently across evaluation periods — firing on one definition during Phase 1 and a different definition (with shorts added) during Phase 3. This corrupts the regime signal hierarchy state in ways that are not detectable from the output signal alone.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [CRITICAL] F-4: P4 Signal Algorithm Undefined

**LOCATION:** CHARTER.md Section D; PROTOCOL_SPEC.md Sections D, E ("Pluggable Modules"), F (Phase 0 and Phase 2); ARCHITECT_BRIEF.md Section C

**OBSERVED:** P4 is described as producing states "trending / mean-reverting / stress" from a "1W signal." Phase 0 exit criterion: "P4 produces historically labeled regime series covering ≥3 years of 1D data on ≥15 of 20 target assets." Phase 2 includes detailed pre-requirements for P4 recalibration.

**PROBLEM:** No document specifies the algorithm that produces the P4 state classification. No inputs (which indicators? which features?), no parameters (lookback periods? thresholds?), no model class (rule-based? HMM? ML?), and no update rule are provided. The three output states ("trending / mean-reverting / stress") cannot be reproduced from the specification alone.

This gap is load-bearing in four ways:

1. **Phase 0 exit criterion is unverifiable by a third party.** "P4 produces historically labeled regime series" — labeled by what rule? An auditor cannot confirm this criterion is met without knowing the algorithm.

2. **Phase 1 OOS spanning requirement depends on P4.** "≥2 distinct regime instances (≥8 weeks each)" uses P4 labels. Without a defined algorithm, two developers starting Phase 1 simultaneously would produce different regime spanning counts from the same data.

3. **Phase 2 re-calibration cannot be designed.** The pre-Phase 2 requirement to compute ρ(4H,1W) relies on an empirically defined IC correlation between signal types — but if the P4 signal algorithm is undefined, the 1W IC cannot be computed from it.

4. **Regime label immutability is meaningless without a versioned algorithm.** "Regime labels frozen at evaluation time" requires a specific version of the signal to be version-locked. Without specifying the algorithm, no meaningful versioning is possible.

**EVIDENCE:**
- CHARTER.md Section D: "P4 | Weekly regime overlay | 1W signal state (trending / mean-reverting / stress)"
- PROTOCOL_SPEC.md Phase 0 exit criteria: "P4 (weekly regime signal) produces historically labeled regime series covering ≥3 years of 1D data on ≥15 of 20 target assets"
- PROTOCOL_SPEC.md Section E ("1W Regime Overlay"): "Inputs: Weekly OHLCV, P4 signal specification (pre-registered)" — refers to a specification that does not exist in any of the five documents
- ARCHITECT_BRIEF.md Q4: "How would you architect the regime signal versioning so that a Phase 2 recalibration cannot corrupt Phase 1 regime label records?" — open question that presupposes the algorithm will be defined but does not state that it is not yet defined
- PROTOCOL_SPEC.md I, Q7: "What is the empirical ρ(signal IC at 4H, signal IC at 1W)?" — requires a defined P4 to be answerable; listed as an open external question

**IMPACT:** (A) (B) (C) All three primary failure modes. Invalid OOS spanning claims (Phase 1 regime spanning cannot be verified), incorrect kill decisions (K1 regime spanning requirement cannot be certified), and undetected state corruption (P4 state is undefined so any state inconsistency is undetectable).

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [CRITICAL] F-5: IC_long Assumption Is Load-Bearing and Unvalidated — No Suspect Threshold Defined

**LOCATION:** GLOSSARY.md ("IC"); PROTOCOL_SPEC.md Section I, Q1; CHARTER.md Correction 1

**OBSERVED:** GLOSSARY.md: "IC_long: 0.03–0.05 assumed for long-side skills (moderate; not verified until Phase 1)."

**PROBLEM:** The IC_long assumption is the primary driver of the entire Sharpe feasibility case. Via FLAM:

```
IR_long = IC_long × sqrt(BR_long) = [0.03, 0.05] × sqrt(240) ≈ [0.46, 0.78] gross
```

After costs (targeting net Sharpe 0.28–0.42), the cost burden must be approximately 0.18–0.50 Sharpe units — a range that is internally consistent only if IC_long ≥ 0.03. If IC_long = 0.015 (half the stated lower bound), FLAM gross ≈ 0.23, and net Sharpe collapses well below K1 = 0.28 with no early warning signal.

The asymmetry with IC_short is stark: IC_short has explicit suspect controls (IC_short > 0.04 → apply 0.015 haircut before reporting; never default to IC_long), documented reasoning in EVOLUTION.md Section 6, and an explicit correction from v4. IC_long has none of these:

- No suspect threshold is defined for IC_long
- No haircut rule applies if walk-forward results yield IC_long > 0.05
- No literature citation supports 0.03–0.05 as the prior for this universe
- EVOLUTION.md does not document an audit or challenge of IC_long comparable to the v4 IC_short correction

The FLAM formula for BR_long compounds this: "5 skills × 2 timeframes × 12 months, approximate = 240." This formulation is dimensionally ambiguous (5 × 2 × 12 = 120, not 240; the derivation is unclear) and does not account for skill correlation. The spec's own N_eff ≈ 2.4 at ρ_avg = 0.30 implies effective independent bets BR_eff ≈ 240 × (2.4/6) ≈ 96, which reduces FLAM gross Sharpe by sqrt(240/96) ≈ 1.58×, cutting the lower bound from 0.46 to approximately 0.30 — barely above K1. At ρ_avg = 0.40, BR_eff ≈ 71, and FLAM gross ≈ 0.25. The system would be expected to fail K1 even if IC_long achieves the assumed range.

**EVIDENCE:**
- GLOSSARY.md: "IC_long: 0.03–0.05 assumed for long-side skills (moderate; not verified until Phase 1)"
- CHARTER.md Correction 1 (FLAM fix): IC_short correction derived explicitly; IC_long correction not proposed
- CHARTER.md Phase 3: "IC_short > 0.04 in walk-forward results → treat as suspect; apply 0.015 haircut" — no equivalent rule for IC_long
- PROTOCOL_SPEC.md H1: "At k=6 skills with average pairwise correlation ρ=0.30: N_eff ≈ 2.4" — implies BR_eff materially below BR_long = 240
- PROTOCOL_SPEC.md I, Q1: "What is the empirical range of short-side IC for the top-4-per-sector universe?" — long-side IC not even raised as an open question

**IMPACT:** (A) (B) Invalid performance claims and missed kill decisions. If IC_long is below the assumed range, the system will fail K1 at Phase 1 exit with no prior diagnostic signal, having consumed 15+ months of development time. The absence of an IC_long suspect threshold means high in-sample IC_long values will not be flagged as potential overfitting, producing false positive Phase 1 exit certifications.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED] The IC_long assumption is presented as a calibrated prior; its unvalidated status is noted in GLOSSARY.md ("not verified until Phase 1") but the asymmetric treatment relative to IC_short is not acknowledged.

---

### [HIGH] F-6: K4 Missed-Kill Probability Unspecified

**LOCATION:** CHARTER.md Correction 2, Appendix Kill Criteria; PROTOCOL_SPEC.md Section F (Phase 3), Section J; EVOLUTION.md Section 7

**OBSERVED:** CHARTER.md Correction 2: "P(false kill at t < 0.5 threshold) ≈ 60%. This is still too high for a definitive kill. The criterion is accepted as a screening threshold."

**PROBLEM:** The specification acknowledges and accepts the false-kill probability (P(K4 fires | IC_short = 0.025) ≈ 60%). It does not state the missed-kill probability.

**Derivation:**
K4 fires when t < 0.5 after ≥90 trades. For a genuinely dead short book (IC_short = 0):
```
E[t | IC = 0] = 0
P(K4 fires | IC = 0) = P(t(89) < 0.5) ≈ P(Z < 0.5) ≈ 0.69
P(K4 does NOT fire | IC = 0) ≈ 0.31
```

A dead short book has a 31% chance of surviving K4 at 90 trades. The criterion also requires 18 months elapsed AND ≥90 trades — if 90 trades are not reached at 18 months, K4 is never evaluated regardless of performance.

The specification frames K4 as calibrated toward "erring toward rejection" (EVOLUTION.md Section 7: "The asymmetry favors erring toward rejection"). However, a 31% missed-kill rate on a dead strategy is not a conservative posture. Combined with the acknowledged 60% false-kill rate, K4 is miscalibrated in both directions simultaneously.

**EVIDENCE:**
- CHARTER.md Correction 2: "At IC_short = 0.025, 90 trades, expected t ≈ 0.24. P(false kill at t < 0.5 threshold) ≈ 60%."
- PROTOCOL_SPEC.md Phase 3: "at 90 trades, IC_short = 0.025 produces expected t ≈ 0.24. K4 is a screening threshold, not a significance test."
- EVOLUTION.md Section 7: "P(false kill | IC=0.025) ≈ 60%" — no statement of missed-kill rate
- [REVIEWER KNOWLEDGE] For t(89) distribution: P(t > 0.5 | null) = P(t(89) > 0.5) ≈ 0.31

**IMPACT:** (B) Incorrect kill decisions. A dead short book that survives K4 (31% probability) would proceed to Phase 3 exit consideration, where the net Sharpe delta criterion (≥0) might be marginally satisfied by sampling variance over 12 months, advancing a valueless extension to capital deployment.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED] The missed-kill rate is not mentioned in any document.

---

### [HIGH] F-7: Regime Label Vintage Problem — Phase 1 OOS Labels Potentially Contaminated by P4 Calibration

**LOCATION:** CHARTER.md Sections D (Regime Label Immutability), Phase 0 exit criteria; PROTOCOL_SPEC.md Phase 0 exit criteria, Phase 1 OOS spanning requirement; ARCHITECT_BRIEF.md Section D ("Regime signal versioning")

**OBSERVED:** Phase 0 exit criterion: "P4 (weekly regime signal) produces historically labeled regime series covering ≥3 years of 1D data on ≥15 of 20 target assets." Phase 1 OOS spanning: "≥2 distinct regime instances (≥8 weeks each)" counted using these labels.

**PROBLEM:** The P4 signal is calibrated in Phase 0 on ≥3 years of historical data. If the P4 signal involves any parameter optimization fitted to the historical period, the resulting regime labels for that historical period are in-sample labels — they were produced using information that spans the calibration window, including windows that will become Phase 1 IS data.

The walk-forward harness has a 4-year training window with annual roll. The Phase 0 historical labeling covers ≥3 years. The overlap between the P4 calibration window and the Phase 1 walk-forward IS windows creates a structural vintage problem: regime labels in Phase 1 IS windows were produced by a signal that "saw" those IS windows during calibration. The labels are not contemporaneous estimates from information available at the start of each test window — they are retrospective classifications using the full calibration sample.

The regime label immutability rule ("labels frozen at evaluation time") addresses the Phase 2 recalibration risk but does not address the Phase 0 vintage contamination. Once frozen, labels remain contaminated.

**EVIDENCE:**
- CHARTER.md Phase 0: "P4 (weekly regime signal) produces historically labeled regime series covering ≥3 years of 1D data"
- CHARTER.md Section D: "Regime labels applied to historical OOS windows are frozen at evaluation time."
- ARCHITECT_BRIEF.md Section D: addresses Phase 2 recalibration risk only; does not address Phase 0 vintage contamination
- ARCHITECT_BRIEF.md "What Is Not Addressed (Known Gap)": confirms nested recovery gap; does not address vintage problem

**IMPACT:** (A) (C) Invalid OOS spanning claims and undetected state corruption. If Phase 1 OOS spanning is certified using P4 labels produced with in-sample information, the spanning requirement is satisfied on invalid grounds. This propagates to all subsequent phase gate decisions.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [HIGH] F-8: FLAM Phase 3 Justification Rests on Acknowledged Unresolved Assumption

**LOCATION:** CHARTER.md Correction 1, Phase 3; PROTOCOL_SPEC.md Section E ("Equity Shorts"), Section I, Q2; EVOLUTION.md Section 6

**OBSERVED:** Phase 3 expected net Sharpe delta: "+0.01–0.05 (corrected FLAM; IC_short = 0.02–0.03 assumed; uncertainty is high at this range)."

**PROBLEM:** The FLAM marginal contribution formula:
```
Delta_IR = IC_short × [sqrt(BR_long + BR_short) - sqrt(BR_long)]
```
assumes long and short bets are independent (uncorrelated). Phase 3 short signals are derived by "repurposing/mirroring" long-side skills. If IC_long and IC_short are correlated at level ρ_IC, the effective breadth addition is:

```
BR_effective = BR_short × (1 - ρ_IC²)
```

At ρ_IC = 0.5 (moderate correlation from shared skill basis):
```
BR_effective = 60 × (1 - 0.25) = 45
Delta_IR = 0.025 × [sqrt(240 + 45) - sqrt(240)]
         = 0.025 × [16.88 - 15.49]
         = 0.025 × 1.39 ≈ 0.035 gross
```

At ρ_IC = 0.8 (high correlation, same skill mirrored):
```
BR_effective = 60 × (1 - 0.64) = 21.6
Delta_IR = 0.025 × [sqrt(261.6) - sqrt(240)] = 0.025 × 0.68 ≈ 0.017 gross
```

After costs (funding drag, borrow, stop turnover), net delta at ρ_IC = 0.8 approaches zero or goes negative. The published range +0.01–0.05 is achievable only if IC_long and IC_short are uncorrelated — a condition directly contradicted by the specification's statement that shorts are derived from mirrored long skills.

**EVIDENCE:**
- PROTOCOL_SPEC.md I, Q2: "Is the marginal FLAM formula appropriate for a system where long and short signals are correlated (derived from the same skill set)? If IC_long and IC_short are correlated, the breadth addition from the short sleeve is overstated." — **listed as an open external question, meaning the specification acknowledges the unresolved assumption**
- PROTOCOL_SPEC.md Section E: "Inputs: Long-side skill signals (repurposed/mirrored for short direction)"
- CHARTER.md Correction 1: Delta_IR derivation assumes independent bets (no correlation adjustment)

**IMPACT:** (A) Invalid performance claims. The Phase 3 expected net Sharpe delta may be zero or negative if signal correlation is moderate-to-high, making the stated Phase 3 development justification non-viable before evaluation begins.

**ASSUMPTION FLAG:** [DOCUMENTED] PROTOCOL_SPEC.md Section I explicitly lists this as an open question. The finding is that Phase 3 planning proceeds despite the unresolved status.

---

### [HIGH] F-9: No SimBroker Drift Kill Criterion in Phase 1

**LOCATION:** CHARTER.md Kill Criteria Appendix; PROTOCOL_SPEC.md Sections F (Phase 1), J; ARCHITECT_BRIEF.md Section E (R3, R5)

**OBSERVED:** K6 ("SimBroker short-cost model diverges > 20% from paper-fill costs for 2 consecutive months") is listed as Active From: Phase 3–4. Phase 1 monitoring table includes "SimBroker cost accuracy: within 15% of paper fills → Flag if > 15% for 2 consecutive months."

**PROBLEM:** Phase 1 has a monitoring flag for SimBroker cost deviation but no kill criterion. All Phase 1 kill criteria — K1 (net Sharpe), K2 (infrastructure cost ratio), K3 (N_eff) — are computed against SimBroker outputs. If SimBroker systematically underestimates long-side transaction costs in Phase 1, the net Sharpe is overstated by the same magnitude. A system passing K1 with point estimate 0.30 may have a true net Sharpe of 0.22 if costs are understated by ~25%.

The "Flag if > 15% deviation" monitoring action is not a kill or hold. There is no specified consequence — no required remediation before Phase 1 exit, and no mechanism to retroactively recompute Phase 1 OOS Sharpe if post-hoc SimBroker recalibration reveals systematic bias.

ARCHITECT_BRIEF.md Section D: "SimBroker calibration drift: Market microstructure evolves. A cost model calibrated in Phase 0 will drift by Phase 3 without quarterly recalibration." This drift begins accumulating during Phase 1 with no trip wire.

**EVIDENCE:**
- CHARTER.md Phase 1 metrics: "SimBroker cost accuracy | Within 15% of paper fills | Flag if > 15% for 2 consecutive months" — no kill action
- CHARTER.md Kill Criteria: K6 listed as "Phase 3–4" only
- ARCHITECT_BRIEF.md Q5: "If SimBroker has a systematic bias, all kill criteria will be miscalibrated in the same direction." — listed as open architecture question
- ARCHITECT_BRIEF.md R3: cost model risk acknowledged; no Phase 1 kill resolution

**IMPACT:** (B) Incorrect kill decisions. SimBroker cost underestimation in Phase 1 produces a false-positive Phase 1 exit certification. All subsequent phases begin from a contaminated baseline.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED] The gap between Phase 0 SimBroker validation and Phase 3 K6 activation is not acknowledged as a Phase 1 risk.

---

### [HIGH] F-10: P1+P3 Concurrent Activation and Sequential Recovery Undefined

**LOCATION:** CHARTER.md Section D ("Conflict Resolution Rules"); PROTOCOL_SPEC.md Section D; ARCHITECT_BRIEF.md Section C ("What Is Not Addressed — Known Gap")

**OBSERVED:** CHARTER.md conflict resolution rule 1: "Higher-priority signal always takes precedence." P3 recovery: "20-day ρ < 0.45 (hysteresis band = 0.10)." P1 recovery: "HWM gap < 8% AND ≥5 business days elapsed."

**PROBLEM:** The specification defines conflict resolution for simultaneous firing (P1 wins over P3) but does not define the recovery sequencing when P1 fires, partially recovers, and P3 fires or remains active during P1's recovery window. Four specific unresolved states:

**State A:** P1 fires (reduce to 50%). P3 fires simultaneously. P1's 50% constraint is binding. P1 then recovers. At P1 recovery: what is the target gross? Should P3 reduction (35–50%) now apply to the original full gross? Or has P3's clearing elapsed?

**State B:** P1 fires. During the 5-business-day suspension window, P3 triggers. P1 recovers after 5 days. P3 has been triggered but not yet cleared (requires 20-day average below 0.45). Who enforces P3 reduction during the P1 recovery period, and at what ramp rate?

**State C:** P3 fires. Reduction over 3 business days begins. On day 2, P1 fires ("reduce all to 50% immediately"). The 3-day P3 ramp is interrupted. Does P3 reduction restart from 50% when P1 recovers?

**State D:** P4 state changes during P1 active (suppressed per conflict rules). Does the new P4 state apply when P1 recovers, or the P4 state at the time of P1 trigger?

**EVIDENCE:**
- CHARTER.md Section D conflict rules 1–3: defines simultaneous firing priority; no nested recovery sequencing
- ARCHITECT_BRIEF.md Section C "What Is Not Addressed (Known Gap)": "The recovery from P3 that occurs while P1 recovery criteria are also pending should be explicitly handled in the harness implementation. The current spec is silent on nested recovery sequencing."

**IMPACT:** (C) Undetected state corruption. In a stress scenario (≥12% DD coinciding with correlation spike), P1 and P3 will fire simultaneously or in rapid succession. Undefined recovery sequencing means the harness and paper trading implementations may default to different developer judgments, producing a systematic evaluation-vs-execution mismatch.

**ASSUMPTION FLAG:** [DOCUMENTED] Explicitly acknowledged as a known gap in ARCHITECT_BRIEF.md but unresolved across all five documents.

---

### [HIGH] F-11: N_eff Approximation Assumes Homogeneous Correlation; Inaccurate for Heterogeneous Portfolios

**LOCATION:** PROTOCOL_SPEC.md Sections H, J1; GLOSSARY.md ("N_eff"); ARCHITECT_BRIEF.md Section E (R1)

**OBSERVED:** N_eff formula used throughout: `k / (1 + (k−1) × ρ_avg)`, where ρ_avg is mean pairwise skill P&L correlation.

**PROBLEM:** This formula is valid only when all pairwise correlations are equal (equicorrelation model). For a portfolio of 5–6 skills spanning trend, reversion, and vol-regime clusters — three conceptually distinct types — pairwise correlations will be systematically heterogeneous: high within cluster, low across clusters.

**Illustrative example:** 3 trend skills correlated at ρ=0.70, 2 reversion skills at ρ=0.60, 1 vol-regime skill correlated at ρ=0.10 with all others. ρ_avg ≈ 0.38.

```
Equicorrelation formula: N_eff = 6 / (1 + 5 × 0.38) = 6 / 2.9 ≈ 2.07  → K3 triggers
Precise participation ratio (eigenvalue-based): ~3.0               → K3 does not trigger
```

The same data can produce N_eff of 2.07 (K3 triggers, project killed) or 3.0 (K3 does not trigger) depending on the formula used.

**EVIDENCE:**
- GLOSSARY.md: "N_eff: k / (1 + (k−1) × ρ_avg)"
- PROTOCOL_SPEC.md H1: "At k=6 skills with average pairwise correlation ρ=0.30: N_eff ≈ 2.4" — using the equicorrelation formula
- ARCHITECT_BRIEF.md R1: "At k=6 skills, ρ_avg=0.3 → N_eff=2.4; barely above K3 threshold in normal conditions" — proximity to K3 acknowledged, formula accuracy not questioned

**IMPACT:** (B) Incorrect kill decisions. K3 triggers at N_eff ≤ 2 for 2 consecutive months. Given the spec's own estimate of N_eff ≈ 2.4 in normal conditions — barely above threshold — formula accuracy at this margin is directly consequential for K3 fire/no-fire decisions.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [MEDIUM] F-12: Purge/Embargo Duration Not Specified

**LOCATION:** ARCHITECT_BRIEF.md Section B ("Walk-Forward Harness Design"); PROTOCOL_SPEC.md Phase 0 exit criteria, Section I, Q4

**OBSERVED:** ARCHITECT_BRIEF.md: "Purge/embargo applied to training-validation boundary proportional to maximum holding period to prevent label leakage from overlapping trade horizons."

**PROBLEM:** "Proportional to maximum holding period" is not a formula or a value. Maximum holding period for 4H signals is 3–15 days per the cost model; for 1D signals, longer. The embargo length has no specified formula, no computed value, and no acceptance criterion in the Phase 0 exit criteria. The Phase 0 leakage audit checklist is described but not published in any of the five documents. PROTOCOL_SPEC.md Q4 asks: "What is the minimum embargo length for 4H bars given typical holding periods of 3–15 days?" — confirming this is unresolved.

**EVIDENCE:**
- ARCHITECT_BRIEF.md: "Purge/embargo applied to training-validation boundary proportional to maximum holding period"
- PROTOCOL_SPEC.md Phase 0 exit: no mention of embargo length
- PROTOCOL_SPEC.md I, Q4: listed as open external question

**IMPACT:** (A) Invalid performance claims. An inadequate embargo allows training labels to overlap with validation-window prices, inflating validation Sharpe and biasing parameter selection. A Phase 0 that passes the leakage audit without a defined embargo may certify a harness that has systematic label leakage at the training-validation boundary.

**ASSUMPTION FLAG:** [DOCUMENTED]

---

### [MEDIUM] F-13: P3 Reduction Range Has No Selection Protocol

**LOCATION:** CHARTER.md Section D; PROTOCOL_SPEC.md Section D; ARCHITECT_BRIEF.md Section C

**OBSERVED:** P3 trigger action across all documents: "Reduce gross exposure 35–50% over 3 business days."

**PROBLEM:** The P3 action is a range (35–50% reduction), not a value. No rule, formula, or protocol exists for selecting the reduction magnitude within this range. If the harness uses 40% and paper trading uses 50%, P3 actions create a 15-percentage-point gross exposure mismatch — a systematic evaluation-vs-execution divergence. In a solo-developer context, the choice will be made once at implementation time and may never be revisited.

**EVIDENCE:**
- CHARTER.md Section D: "Reduce gross exposure 35–50% over 3 business days" — no selection rule
- PROTOCOL_SPEC.md Section D: identical
- No document specifies a selection rule within the range

**IMPACT:** (C) Undetected state corruption. Portfolio state after P3 fires is indeterminate within a 15-percentage-point range, creating unreproducible evaluation results.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [MEDIUM] F-14: Temporal Shuffling Detects Only One Class of Leakage

**LOCATION:** CHARTER.md Phase 0 exit criteria; PROTOCOL_SPEC.md Phase 0 exit criteria; ARCHITECT_BRIEF.md Section B, Q1

**OBSERVED:** Phase 0 exit criterion: "Walk-forward harness passes leakage audit: zero forward-looking features verified by temporal shuffling test."

**PROBLEM:** The temporal shuffling test detects leakage from features that depend on future prices. It cannot detect:

**(a) Feature normalization leakage:** Rolling Z-scores using mean/std computed over the full dataset (including OOS) rather than only up to the training window end. Temporal shuffling tests feature-return correlation, not parameter source.

**(b) Regime label look-ahead:** If P4 labels are produced using any smoothing incorporating future bars, labels contain future information. Shuffling tests do not verify the information set used to produce labels.

**(c) Universe selection bias:** If the ~20 target assets are selected using post-evaluation data, historical backtests contain survivorship/selection bias. Shuffling does not detect this.

**(d) Walk-forward within-window optimization:** If calibration steps implicitly access test-window data during iteration, per-feature shuffling does not catch this.

ARCHITECT_BRIEF.md Q1: "Is temporal shuffling sufficient, or are there classes of leakage it cannot detect?" — listed as an open external question, confirming the gap.

**EVIDENCE:**
- Phase 0 exit criteria in both CHARTER.md and PROTOCOL_SPEC.md treat temporal shuffling as the primary leakage detection mechanism
- ARCHITECT_BRIEF.md Q1 explicitly asks whether it is sufficient
- No document lists additional audit procedures for normalization leakage, label leakage, or selection bias

**IMPACT:** (A) Invalid performance claims. If the Phase 0 leakage audit passes with temporal shuffling alone, classes (a)–(d) of leakage remain undetected.

**ASSUMPTION FLAG:** [DOCUMENTED] ARCHITECT_BRIEF Q1 acknowledges this as an open question.

---

### [MEDIUM] F-15: K4 T-Statistic Formula Not Specified

**LOCATION:** CHARTER.md Correction 2, Kill Criteria Appendix; PROTOCOL_SPEC.md Phase 3, Section J

**OBSERVED:** K4: "Short-side t-statistic < 0.5 after 18 months AND ≥90 completed short-side trades."

**PROBLEM:** "Short-side t-statistic" is not defined. Three candidate formulas produce materially different values:

**(a) Per-trade t-statistic:** `t = mean(trade P&L) / (std(trade P&L) / sqrt(n_trades))`
At IC_short = 0.025, n=90: expected t ≈ 0.025 × sqrt(90) ≈ 0.24. This matches the spec's stated value, confirming this is the implied formula.

**(b) Time-series Sharpe-based:** `t = SR_monthly × sqrt(n_months)` at n=18 months.
At SR ≈ 0.081 monthly: t ≈ 0.081 × sqrt(18) ≈ 0.34. Different value; different threshold probability.

**(c) Regression t-statistic** from regressing short P&L on a constant: numerically similar to (a) but distributional assumptions differ for autocorrelated trade P&L.

The K4 decision is formula-sensitive. An undocumented formula choice introduces implementation ambiguity that could produce materially different kill criterion behavior.

**EVIDENCE:**
- CHARTER.md Correction 2: "expected t ≈ 0.24" — implies formula (a)
- PROTOCOL_SPEC.md Phase 3: "expected t ≈ 0.24" — same
- No document states the formula

**IMPACT:** (B) Incorrect kill decisions.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [MEDIUM] F-16: Phase 2 Matched Comparison Matching Criteria Undefined

**LOCATION:** CHARTER.md Phase 2; PROTOCOL_SPEC.md Phase 2

**OBSERVED:** Phase 2 requires: "≥80 comparable trade pairs (same entry signal, different overlay state)."

**PROBLEM:** "Matched pair" criteria are undefined across critical dimensions:

- **Matching on entry signal type vs. instance:** Same skill on same asset on same timeframe? Or same skill category (trend-following)?
- **Time proximity:** If two trades have the same entry signal but occur 6 weeks apart in different market conditions, is the pair valid?
- **Overlay state classification:** For a pair to be valid, one trade must have overlay "active" and one "inactive." If overlay state is a continuous sizing variable, the binary classification rule is undefined.
- **Confound by regime:** If all overlay-active periods coincide with trending regimes and overlay-inactive periods with mean-reverting regimes (by P4 construction), the comparison is regime-confounded. The Phase 2 comparison is the primary evidence basis for advancing or killing the 1W overlay. Undefined matching criteria allow ex-post pair construction to favor a desired outcome.

**EVIDENCE:**
- CHARTER.md Phase 2: "≥80 comparable trade pairs (same entry signal, different overlay state)"
- PROTOCOL_SPEC.md Phase 2: identical; no matching methodology
- No document specifies matching methodology

**IMPACT:** (A) (D) Invalid performance claims and behavioral integrity gap. Undefined matching in a solo-developer context will be operationalized at reporting time — undetectable after the fact.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [MEDIUM] F-17: Timestamp Convention Leakage Not in Phase 0 Exit Criteria

**LOCATION:** ARCHITECT_BRIEF.md Section F ("Reproducibility Risk"); PROTOCOL_SPEC.md Phase 0 exit criteria

**OBSERVED:** ARCHITECT_BRIEF.md: "At 4H resolution, bar data from different sources can differ in timestamp convention (UTC vs exchange local, bar-open vs bar-close alignment). If the evaluation engine and paper trading use different timestamp conventions, fills may occur on different bars, creating a systematic evaluation-vs-execution mismatch that is invisible in backtests. **This should be a checklist item in the Phase 0 leakage audit.**"

**PROBLEM:** "Should be" is not "must be." This recognized risk appears in ARCHITECT_BRIEF as an advisory note but is not codified in the Phase 0 exit criteria or any required verification step. For a 4H bar strategy, a one-bar timestamp misalignment produces entry fills at the wrong price for 100% of trades — a structural bias that inflates or deflates every strategy's Sharpe by a fixed amount throughout all phases.

**EVIDENCE:**
- ARCHITECT_BRIEF.md Section F: advisory note only
- Phase 0 exit criteria in CHARTER.md and PROTOCOL_SPEC.md: no mention of timestamp convention verification

**IMPACT:** (A) Invalid performance claims. A timestamp convention mismatch not caught in Phase 0 produces systematic WFO-vs-paper mismatch throughout all subsequent phases.

**ASSUMPTION FLAG:** [DOCUMENTED] Acknowledged in ARCHITECT_BRIEF.md but not elevated to required exit criterion.

---

### [MEDIUM] F-18: GE-2 / GE-3 Boundary Between Allocation and Signal Modification Is Not Bright-Line

**LOCATION:** PROTOCOL_SPEC.md Sections J1 (Rules GE-2, GE-3), F (Phase 1 "Can change" section)

**OBSERVED:** Rule GE-2: "Adjustments to allocation weights that improve N_eff are permitted without preregistration." Rule GE-3: "Any modification to signal entry conditions, exit conditions, feature definitions, or look-back parameters — regardless of framing — requires preregistration."

**PROBLEM:** The boundary between an "allocation adjustment" (GE-2, preregistration-exempt) and a "signal modification" (GE-3, preregistration-required) is not defined for ambiguous cases:

- **Reducing a skill's allocation to 0%:** Functionally equivalent to removing the skill. GE-2 or GE-3?
- **Differentially weighting skill instances by timeframe:** Changes effective signal contribution without modifying the algorithm. GE-2 or GE-3?
- **Cluster-cap changes that effectively exclude a skill:** A cluster cap reduction that forces a skill to near-zero allocation. GE-2 or GE-3?

In a solo-developer context, the distinction will be made unilaterally. GE-2 exceptions erode the multiplicity protection by providing a framing escape from preregistration, leaving the Harvey-Liu trial count understated.

**EVIDENCE:**
- PROTOCOL_SPEC.md J1 Rules GE-2 and GE-3: no bright-line rule for edge cases
- PROTOCOL_SPEC.md Phase 1: "allocation-based diversification adjustments... do not require preregistration"
- No document defines the allocation/signal modification boundary for zero-weight or near-zero-weight cases

**IMPACT:** (A) (D) Invalid performance claims through Harvey-Liu trial count understatement; behavioral integrity gap.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [LOW] F-19: HWM and Purge/Embargo Absent from GLOSSARY

**LOCATION:** GLOSSARY.md; CHARTER.md Section D; ARCHITECT_BRIEF.md Section B

**OBSERVED:** GLOSSARY.md states: "Purpose: Reference definitions for developers and AI models. All terms used in PROTOCOL_SPEC.md and CHARTER.md are defined here."

**PROBLEM:** The following terms are used in specification documents but absent from GLOSSARY.md:
- **HWM (High Water Mark):** Used in P1 trigger and recovery. Whether HWM resets at phase boundaries, resets annually, or is permanent since inception is unspecified.
- **Purge/Embargo:** Core leakage prevention mechanism in ARCHITECT_BRIEF. No glossary definition.
- **Walk-Forward Window parameters (4yr/1yr/1yr/annual roll):** Appear only in ARCHITECT_BRIEF, not in PROTOCOL_SPEC or GLOSSARY.

**EVIDENCE:**
- GLOSSARY.md: HWM, purge/embargo not included despite the stated coverage claim
- CHARTER.md Section D: "Realized DD from HWM ≥ 12%"; "HWM gap < 8%"

**IMPACT:** (D) Implementation ambiguity for HWM reset timing and embargo duration.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [LOW] F-20: K5 Measurement Period Not Specified

**LOCATION:** CHARTER.md Phase 5, Kill Criteria Appendix; PROTOCOL_SPEC.md Section F (Phase 5), Section J

**OBSERVED:** K5: "Treasury yield > 60% of total return in any 12-month period."

**PROBLEM:** "Any 12-month period" is ambiguous: rolling (evaluated monthly or continuously), calendar year (January–December), or fixed windows from treasury activation date. The difference matters in a scenario where treasury yield is high for 11 months but trading alpha recovers in month 12. Under rolling evaluation, K5 may fire. Under calendar-year evaluation, it may not. The rolling vs. calendar choice is unspecified.

**EVIDENCE:**
- CHARTER.md Phase 5: "Treasury yield > 60% of total return in any 12-month period"
- PROTOCOL_SPEC.md Section J: identical
- No document specifies rolling vs. calendar

**IMPACT:** (B) Incorrect kill decisions (specifically missed K5 triggers from boundary selection).

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

### [LOW] F-21: Phase 0 P1 Circuit Breaker Verification Criterion Is Untestable as Stated

**LOCATION:** CHARTER.md Phase 0 exit criteria; PROTOCOL_SPEC.md Phase 0 exit criteria

**OBSERVED:** Phase 0 exit criterion: "DD circuit breaker (P1) logic implemented, tested with synthetic data, and verified."

**PROBLEM:** "Tested with synthetic data and verified" has no acceptance criterion. No minimum test suite specification exists. A minimalist implementation could run P1 logic against a single test case and certify the criterion as met. Without specifying which scenarios must pass (e.g., simultaneous P1+P3 firing, P1 recovery with P3 still active, restart mid-suspension, partial position reduction), this exit criterion cannot be verified by a third party and creates a behavioral integrity gap where the developer self-certifies against an undefined protocol.

**EVIDENCE:**
- CHARTER.md Phase 0: "DD circuit breaker (P1) logic implemented, tested with synthetic data, and verified"
- PROTOCOL_SPEC.md Phase 0: identical
- No test specification in any of the five documents

**IMPACT:** (C) Undetected state corruption. An undertested P1 implementation may fail to correctly reduce positions, enforce the 5-day suspension, or enforce recovery conditions in edge cases.

**ASSUMPTION FLAG:** [UNACKNOWLEDGED]

---

## OPEN QUESTIONS REQUIRING AUTHOR RESPONSE

The following questions must be answered to resolve material specification ambiguities. Each is answerable with a concrete specification addition.

**Q1 (resolves F-1):** Which variant of the Harvey-Liu correction is mandated? Provide the complete formula with all parameters and state where the parameter values are obtained (T in years, ρ_avg between test statistics, number of independent tests per dimension). How are cross-phase trials aggregated — specifically, do AT trials for hypothesis dimension X count in the Harvey-Liu denominator for the same dimension X in Phase 1?

**Q2 (resolves F-2):** What formula and sample unit was used to derive "CI ≈ ±0.15–0.20 at 15 months OOS"? Provide the derivation. If the answer is inconsistent with the standard asymptotic formula SE = sqrt((1 + SR²/2) / T) at T = 1.25 annual periods (which yields SE ≈ 0.91), identify the alternative framework and document it as authoritative. If no derivation exists, replace the stated CI with the correct value and cascade the correction to all documents and decision thresholds that depend on it.

**Q3 (resolves F-3):** Define the exact population for P3's pairwise ρ calculation: (a) asset-level price correlation or skill-level P&L correlation; (b) whether short positions are included after Phase 3; (c) whether the universe is all 20 assets or only active positions; (d) whether correlation is computed on daily returns, 4H bar returns, or another interval. This definition must be locked before Phase 0 P3 implementation begins.

**Q4 (resolves F-4):** Specify the P4 signal algorithm completely: input data, features, thresholds or model class, calibration method (if any), and the rule for assigning "trending / mean-reverting / stress" labels. The specification must be sufficient for a second developer to independently reproduce the historical label series from the same raw data.

**Q5 (resolves F-7):** Does P4 involve any parameter fitting on historical data during Phase 0 calibration? If yes: specify the calibration procedure and describe the mechanism by which Phase 1 walk-forward IS windows overlapping with the P4 calibration window are treated as having in-sample regime labels (and therefore excluded from OOS spanning counts). If no: specify the purely rule-based algorithm (resolves F-4 simultaneously).

**Q6 (resolves F-11):** Which formula is used for N_eff computation for K3 purposes: the equicorrelation approximation `k / (1 + (k−1) × ρ_avg)` or the precise eigenvalue-based participation ratio? If the equicorrelation formula is retained, provide evidence or a reference demonstrating its adequacy for a heterogeneous three-cluster portfolio of 5–6 skills at the K3 trigger boundary (N_eff ≈ 2.0–2.5).

**Q7 (resolves F-10):** For P1+P3 simultaneous or sequentially nested firing: specify the gross exposure target at the moment P1 recovers if P3 is still active. Specify whether P3's 3-business-day reduction ramp restarts or continues from current gross when P1 triggers during the ramp. Specify what P4 routing state applies when P1 recovers. This closes the acknowledged "known gap" in ARCHITECT_BRIEF.md Section C.

**Q8 (resolves F-15):** Specify the K4 t-statistic formula precisely: numerator, denominator, degrees of freedom, and handling of autocorrelated trade-level P&L. Confirm whether the formula is consistent with the derivation "expected t ≈ 0.24 at IC = 0.025, n = 90."

**Q9 (resolves F-16):** Define the matched pair criteria for Phase 2 comparison: what constitutes a valid pair (same entry signal instance? same entry signal type? same asset?), the time-proximity requirement, the classification rule for overlay-active vs. overlay-inactive, and how regime state confounding between P4-active and P4-inactive periods is addressed.

**Q10 (resolves F-12):** Specify the purge/embargo length as a formula or specific value (in bars or days) for 4H signals and 1D signals separately. Add this to GLOSSARY.md and to the Phase 0 leakage audit checklist as a required parameter.

---

## FINDINGS NOT IN SCOPE

The following were observed but excluded per the audit scope definition:

- **Technology stack choices** (Parquet + PostgreSQL, data provider selection): explicitly variable per Phase 0 "Can change" rules; not an architectural integrity question
- **Individual asset selection** (top-4 per sector, universe composition): excluded per audit mandate
- **Era roadmap feasibility** (18-month timeline, solo hours estimates): operational planning; not an evaluation integrity question
- **Cost model base rates** (0.08%/leg equity commission, 0.05% crypto taker fee): market-specific parameters; their accuracy is the subject of K6 (an in-scope mechanism) — the rates themselves are excluded
- **Step 4 (leverage)**: explicitly prohibited during the current era; no evaluation integrity risk at current scope
- **CCA and InsightHypothesis schema**: explicitly deferred to Era 4; no current evaluation integrity risk

---

*Document Version: 1.0 | Date: 2026-03-04*
*Auditor: Quantitative Research Integrity Auditor (Staff-Level QRS Architect)*
*Status: Awaiting author responses to Q1–Q10*
*Next action: Author to respond to Open Questions; findings to be resolved or accepted with documented rationale*
