# Entropy Protocol — Research Question Pool

**Classification:** Confidential — Internal Governance Document
**Filename:** `docs/audit/QUESTION_POOL.md`
**Cycle:** 1 (Phase 0, Pre-Development)
**Date:** 2026-03-04
**Owner:** Spec Owner / Staff-Level Systems Architect
**Purpose:** Structured research questions for deep investigation during audit pipeline execution and spec development. Questions are organized by priority and mapped to risk surfaces, open findings, and recommended investigation methods.

---

## Top Priority Research Questions (Q-001 through Q-025)

These questions must be answered before Phase 0 exit can be evaluated. Most correspond directly to P0/P1 open findings.

---

### Q-001 — Harvey-Liu: Which Variant and How Are Cross-Phase Trials Counted?

**Precise question:** Which Harvey-Liu variant (Bonferroni, Holm-Bonferroni, BHY/Benjamini-Hochberg-Yekutieli, or DSR) is specified for the Entropy Protocol? How are cross-phase trials (Phase 1 signals + AT signals + RDL-* signals) aggregated into a single trial count? Does each additional Phase introduce a new trial budget or extend the existing one?

**Why it matters:** The Harvey-Liu haircut is a Phase 1 exit criterion gating condition. If the variant is wrong or the trial count is undercounted (e.g., excluding AT or RDL trials), the computed haircut is meaningless. With PROTOCOL_SPEC.md v1.2 adding RDL trial counting "from submission," the budget is now larger and more complex than at v1.0 audit time. (Finding F-1; RS-01)

**Missing evidence:** No variant specified in any document. No formula. No cross-phase aggregation rule. No statement on whether AT-INF trials count toward the same budget.

**Recommended files:** `docs/PROTOCOL_SPEC.md` NN-5, Phase 1 metrics, Section E (RDL governance); `docs/CHARTER.md` NN-5; `docs/GLOSSARY.md` ("Deflated Sharpe"); `docs/AUDIT_v1.md` Q1; `docs/audience/ARCHITECT_BRIEF.md` Q12

**Method:** Literature check on Harvey-Liu variants; invariant proof sketch comparing each variant's behavior at expected trial counts (10–30 strategies); threat model for understated trial count scenarios

**Expected deliverable:** ADR candidate specifying variant + formula + trial aggregation rule; update to PROTOCOL_SPEC.md NN-5 and GLOSSARY.md

**Confidence:** High (gap confirmed across all documents)

---

### Q-002 — Sharpe CI: What Is the Correct Value and How Do Cascading Thresholds Change?

**Precise question:** Using the standard asymptotic formula `SE(SR_annual) = sqrt((1 + SR²/2) / T)` at T=1.25 years and SR≈0.30, what is the correct 68% CI? What minimum OOS duration is required to achieve the spec's claimed ±0.15–0.20? Given the correct CI, are K1=0.28, the pivot zone (0.22–0.28), and the Phase 1 exit criterion (≥0.28) statistically distinguishable? What is the power of K1 to detect a dead system?

**Why it matters:** The CI is cited in CHARTER.md, PROTOCOL_SPEC.md, and GLOSSARY.md. It underlies K1 calibration and the Phase 1 exit decision. The arithmetic error means K1 is effectively uncalibrated. (Finding F-2; RS-02)

**Missing evidence:** No derivation exists in any document. The actual SE formula using 15 months of data implies SE ≈ 0.91, not ≈ 0.17.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section C definition of Net Sharpe, Phase 1 exit criteria; `docs/CHARTER.md` Section C; `docs/GLOSSARY.md` Net Sharpe; `docs/AUDIT_v1.md` Q2

**Method:** First-principles derivation; power analysis for K1 at SR_true=0 and SR_true=0.15; design comparison (alternative: bootstrapped CI, block bootstrap, Newey-West adjusted)

**Expected deliverable:** ADR candidate correcting CI to ≈±0.89; cascade analysis of all downstream thresholds; potentially: revised Phase 1 OOS duration recommendation

**Confidence:** High (arithmetic is unambiguous)

---

### Q-003 — P3 Population: Which Assets and Which Correlation Metric?

**Precise question:** For the P3 correlation trigger (20-day rolling avg pairwise ρ > 0.55), what is the exact population: (a) all 20 universe assets by price return, (b) active long positions only, (c) active positions including shorts (Phase 3+), (d) skill-level P&L correlations, or (e) cluster-level P&L correlations? What return interval is used (daily, 4H)? Does the population change across phases?

**Why it matters:** The five plausible populations produce materially different trigger frequencies. P3 is an active risk control — indeterminate trigger frequency makes Phase 0 implementation impossible. (Finding F-3; RS-04)

**Missing evidence:** All documents use identical language with no population specification.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section D; `docs/CHARTER.md` Section D; `docs/GLOSSARY.md` ("Regime Signal Hierarchy"); `docs/audience/ARCHITECT_BRIEF.md` Section C; `docs/AUDIT_v1.md` Q3

**Method:** Threat model (quantify trigger frequency for each population candidate under historical data); design comparison (asset-price vs. P&L correlation has fundamentally different properties)

**Expected deliverable:** Spec update to PROTOCOL_SPEC.md Section D with locked population definition; GLOSSARY.md entry for "P3 correlation population"

**Confidence:** High

---

### Q-004 — P4 Algorithm: What Is the Complete Specification?

**Precise question:** What are the complete inputs, features, thresholds (or model class), calibration method, and assignment rule for P4's three states (trending / mean-reverting / stress)? Can a second developer independently reproduce the historical label series from the same raw data without reference to any judgment or undocumented parameter?

**Why it matters:** Phase 0 exit criterion requires P4 to produce a labeled regime series covering ≥3 years. Phase 1 OOS spanning requires ≥2 distinct regime instances. Both are unverifiable without a defined algorithm. RDL-2 (Market State Labeler) depends on this specification to generate meaningful `RegimeTag` objects. (Finding F-4; RS-03)

**Missing evidence:** PROTOCOL_SPEC.md Section E references "P4 signal specification (pre-registered)" that does not exist.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Sections D, E; `docs/CHARTER.md` Section D; `docs/audience/ARCHITECT_BRIEF.md` Q4, Q5; `docs/AUDIT_v1.md` Q4, Q5

**Method:** Design comparison (parametric classification vs. rule-based vs. HMM; what is the minimum-specification approach that is pre-registerable and reproducible?); threat model for P4 vintage contamination under each design

**Expected deliverable:** Pre-registered P4 specification in PROTOCOL_SPEC.md Section E (or referenced annex); resolves RS-03 and RS-07 partially

**Confidence:** High

---

### Q-005 — IC_long: What Is the Suspect Threshold and What Is the FLAM BR_eff Correction?

**Precise question:** What is the suspect threshold for IC_long analogous to IC_short's >0.04 rule? What haircut applies if walk-forward IC_long exceeds the threshold? What is the correct BR_eff formula for the long book, accounting for skill correlation via N_eff? Is the "5 × 2 × 12 ≈ 240" derivation correct (5×2×12=120, not 240)?

**Why it matters:** At ρ_avg=0.40, FLAM gross ≈ 0.25 — below K1. Without an IC_long suspect threshold, a high walk-forward IC_long (possible overfitting) would not be flagged, producing a false-positive Phase 1 exit. (Finding F-5; RS-05)

**Missing evidence:** No IC_long suspect threshold. FLAM derivation is dimensionally ambiguous. No literature citation for IC_long 0.03–0.05 range.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section E (Equity Shorts, IC_short rule), Section H, Section I Q1; `docs/CHARTER.md` Correction 1; `docs/GLOSSARY.md` IC; `docs/AUDIT_v1.md` F-5

**Method:** Literature check (Harvey-Liu-Zhu on IC priors for multi-factor systems; Grinold-Kahn BR formulation); invariant proof sketch for IC_long threshold analogous to IC_short at >0.04; first-principles derivation of BR_eff with N_eff correction

**Expected deliverable:** ADR specifying IC_long suspect threshold, FLAM BR_eff correction, and FLAM "5×2×12" clarification; updates to CHARTER.md Correction 1 and GLOSSARY.md

**Confidence:** High

---

### Q-006 — N_eff Formula: Which One Is Used for K3?

**Precise question:** For K3 purposes, which N_eff formula is specified: (a) equicorrelation `k/(1+(k-1)×ρ_avg)` or (b) eigenvalue-based `(Σλ_i)² / Σ(λ_i²)`? For a representative 3-cluster portfolio (trend/reversion/vol-regime, within-cluster ρ=0.60, between-cluster ρ=0.20), what does each formula give? Does the formula choice affect whether K3 would fire?

**Why it matters:** The two formulas give N_eff=2.07 vs. 3.0 for a plausible portfolio — this straddles the K3 threshold of 2.0. With N_eff≈2.4 in normal conditions (per spec), formula accuracy at this margin is directly consequential. (Finding F-11; RS-09)

**Missing evidence:** Formula not specified in PROTOCOL_SPEC.md Section H, J, or GLOSSARY.md. ARCH_MODEL.md may resolve this when produced.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Sections H, J1; `docs/GLOSSARY.md` N_eff; `docs/audience/ARCHITECT_BRIEF.md` Section E; `docs/AUDIT_v1.md` Q6

**Method:** First-principles derivation for both formulas on example portfolio; design comparison (equicorrelation adequate for equicorrelated clusters; eigenvalue better for heterogeneous)

**Expected deliverable:** Spec update specifying N_eff formula for K3 purposes; if equicorrelation: evidence of adequacy near K3 boundary

**Confidence:** High

---

### Q-007 — P1+P3 Concurrent States: What Are the Deterministic Rules for All Four States?

**Precise question:** For each of the four concurrent-firing states identified in F-10:
- State A: P1 recovers while P3 still active → what is gross exposure target?
- State B: P3 fires during P1 5-day suspension window → is reduction applied to P1-reduced book or original book?
- State C: P3 mid-ramp interrupted by P1 → what is exposure target on the day P1 fires?
- State D: P4 state change during P1 active period → what allocation target applies?

**Why it matters:** In a stress scenario (≥12% DD + correlation spike, which co-occur historically), P1 and P3 fire simultaneously. Undefined recovery sequencing means the harness and paper trading implementations will default to different developer choices — producing systematic evaluation-vs-execution mismatch. (Finding F-10; RS-06)

**Missing evidence:** Gap acknowledged in ARCHITECT_BRIEF.md as "known gap" but unresolved in all five documents.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section D; `docs/CHARTER.md` Section D; `docs/audience/ARCHITECT_BRIEF.md` Section C; `docs/AUDIT_v1.md` Q7

**Method:** Threat model for each state; design comparison (two approaches: deterministic formula, or priority-override-complete)

**Expected deliverable:** ADR + spec update to PROTOCOL_SPEC.md Section D with deterministic rules for all four states; prerequisite for TASK-DEV-003

**Confidence:** High

---

### Q-008 — SimBroker Phase 1 Kill Criterion: What Triggers a Phase 1 Cost Kill?

**Precise question:** Should there be a Phase 1 SimBroker cost kill criterion (K6-Phase1 or equivalent)? If SimBroker cost deviation exceeds X% for Y consecutive months during Phase 1, what is the appropriate action? Should it block Phase 1 exit or trigger recalibration?

**Why it matters:** K6 is active Phase 3–4 only. Phase 1 has a 15% deviation flag but no kill action. A systematic SimBroker cost underestimation in Phase 1 would produce a false-positive Phase 1 exit certification that contaminates all subsequent phases. (Finding F-9; RS-08)

**Missing evidence:** No Phase 1 kill action defined anywhere.

**Recommended files:** `docs/CHARTER.md` Kill Criteria Appendix, Phase 1 metrics; `docs/PROTOCOL_SPEC.md` Sections F, J; `docs/audience/ARCHITECT_BRIEF.md` Q5; `docs/AUDIT_v1.md` F-9

**Method:** Threat model for false-positive Phase 1 exit under different cost underestimation magnitudes; design comparison for Phase 1 kill vs. hard block vs. recalibration requirement

**Expected deliverable:** ADR + CHARTER.md and PROTOCOL_SPEC.md update defining Phase 1 SimBroker cost kill criterion

**Confidence:** High

---

### Q-009 — Vintage Contamination: Does P4 Involve Parameter Fitting?

**Precise question:** Does the P4 algorithm (once specified per Q-004) involve parameter fitting on historical data? If yes, what fraction of Phase 1 IS windows overlap with the P4 calibration window (given P4 calibrates on ≥3 years and Phase 1 IS window = 4 years)? How should the spanning requirement exclude in-sample labeled windows?

**Why it matters:** If P4 is parameter-fitted, Phase 1 OOS spanning may be certified using labels that are in-sample — making the spanning requirement satisfied on invalid grounds. This propagates to all subsequent phase gate decisions. (Finding F-7; RS-07)

**Missing evidence:** Dependent on Q-004 resolution (P4 algorithm). If P4 is rule-based (no parameters), this issue may resolve automatically.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Phase 0 exit criteria, Phase 1 OOS spanning; `docs/audience/ARCHITECT_BRIEF.md` Section D; `docs/AUDIT_v1.md` Q5

**Method:** Design comparison (rule-based P4 avoids vintage contamination entirely; parametric P4 requires explicit window exclusion); threat model for spanning count contamination

**Expected deliverable:** Resolved as part of Q-004 ADR or separate ADR specifying window exclusion procedure

**Confidence:** High (dependent on Q-004)

---

### Q-010 — Growth Layer RBE: What Are the Complete Activation Prerequisites?

**Precise question:** What conditions must be met for an RBE step to be initiated? What does "charter-level review" mean operationally for a solo developer? What format does the review output take, where is it recorded, and what is the review period? What specific kill criteria interact with RBE activation, and does activation reset any measurement windows?

**Why it matters:** The Growth Layer is the only pathway from monitoring-only to active portfolio influence outside the normal phase gate sequence. If the activation prerequisites are undefined, a solo developer can trigger portfolio influence changes with no formal governance constraint. (RS-11, RS-15; no prior finding ID — this is Cycle 1 new surface)

**Missing evidence:** PROTOCOL_SPEC.md Section J2 defines RBE steps but does not specify the charter-level review format or the interaction with kill criteria.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section E (Growth Layer), J1, J2; `docs/CHARTER.md` (kill criteria appendix); `docs/workflow_ai_development.md`

**Method:** Threat model for unauthorized Growth Layer activation; design comparison for governance mechanisms (external review requirement, audit pipeline trigger, dedicated ADR format)

**Expected deliverable:** ADR + spec update defining RBE activation governance; cross-reference to kill criteria that RBE cannot override

**Confidence:** High

---

### Q-011 — RDL Trial Budget: How Large Will It Be at Phase 2 Activation?

**Precise question:** Under realistic Phase 0–1 activity (scaffolding and hypothesis logging), how many RDL-* hypothesis IDs will be in the Trial Registry at Phase 2 activation? With those counts added to the Harvey-Liu budget, what haircut does each variant produce on a raw Phase 1 Sharpe of 0.35? Does the resulting deflated Sharpe still exceed the Phase 1 exit criterion?

**Why it matters:** RDL trials count from submission (not promotion). During Phase 0–1, RDL-1 could log hypotheses that are never evaluated. These still inflate the trial count. With F-1 unresolved (no Harvey-Liu formula), this risk is doubly unverifiable. (RS-12; related to F-1)

**Missing evidence:** No trial count scenario analysis exists. No Harvey-Liu formula to compute the haircut.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section E (RDL governance, RDL-1); `docs/CHARTER.md` NN-5; `docs/GLOSSARY.md`; `docs/audit/REVIEW_REPORT.md` F-1

**Method:** Scenario analysis: assume 10, 20, 50 RDL submissions by Phase 2; apply each Harvey-Liu variant; compute haircut sensitivity

**Expected deliverable:** Scenario analysis table; highlights dependency on Q-001 resolution; may lead to an RDL submission rate governance rule

**Confidence:** High

---

### Q-012 — RDL Phase Boundary: What Is the Enforcement Mechanism?

**Precise question:** How would a neutral third-party auditor verify that RDL submodules (RDL-2, RDL-3) are operating in scaffolding-only mode and not accessing evaluation window data during Phase 0–1? What physical artifact, log file, or state flag distinguishes scaffolding mode from operational mode?

**Why it matters:** The constraint "dormant until Phase 2" exists in policy but has no verification mechanism. The audit pipeline's auto-P0 classification rule depends on detecting a violation after the fact — not preventing it. (RS-13)

**Missing evidence:** No enforcement artifact defined in any document.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section E (RDL); `docs/workflow_ai_development.md` Section 6; `docs/audit/review_pipeline.md`

**Method:** Design comparison (compile-time gating vs. runtime state flag vs. audit log check); threat model for undetected Phase boundary violation

**Expected deliverable:** ADR specifying RDL mode enforcement mechanism; addition to Phase 0 exit criteria checklist

**Confidence:** High

---

### Q-013 — Growth Layer vs. NN-1 through NN-6: Is There a Potential Conflict?

**Precise question:** Can a Growth Layer RBE step activation, even a formally approved one, change portfolio parameters in ways that conflict with any of the six frozen non-negotiables? Specifically: (a) can RBE escalation push gross leverage toward the NN-1 limit? (b) can it change P&L attribution streams in ways that violate NN-2? (c) can it create an "OOS" claim that bypasses NN-3?

**Why it matters:** The Growth Layer was added without a formal audit. Frozen non-negotiables are the highest-level invariants. If RBE activation can interact with them, the Growth Layer is a potential non-negotiable bypass mechanism. (RS-14)

**Missing evidence:** No document reviews Growth Layer against NN-1 through NN-6.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section B (NN-1 through NN-6), Section E (Growth Layer), J1, J2; `docs/CHARTER.md` Section B

**Method:** Invariant proof sketch — for each NN, derive whether a plausible RBE step could violate it

**Expected deliverable:** ADR confirming or correcting Growth Layer/NN interaction; update to Section J2 if gap found

**Confidence:** Medium (depends on RBE step definition, which is not fully specified)

---

### Q-014 — K4 Formula: Which t-Statistic Formula Is Implied?

**Precise question:** Three formulas are candidates for K4: (a) `t = mean(r_short)/(std(r_short)/sqrt(N))`, (b) `t = IC_short * sqrt(BR_short)`, (c) `t = SR_short_annual * sqrt(T_years)`. The spec states "expected t ≈ 0.24" — which formula produces this value at IC_short=0.02, N=90 trades? Once identified, what are the false-kill and missed-kill rates?

**Why it matters:** K4 decision is formula-sensitive. Three formulas produce materially different values. The missed-kill rate derivation in Q-003 depends on using the correct formula. K4 combined with F-6 (both error rates undocumented) is miscalibrated in both directions simultaneously. (Finding F-15; related to F-6)

**Missing evidence:** Formula not explicitly stated anywhere.

**Recommended files:** `docs/CHARTER.md` Correction 2, Kill Criteria Appendix; `docs/PROTOCOL_SPEC.md` Phase 3, Section J; `docs/AUDIT_v1.md` F-6, F-15

**Method:** First-principles derivation to identify which formula produces the stated "expected t ≈ 0.24"; then derive false-kill and missed-kill rates using t-distribution

**Expected deliverable:** ADR specifying K4 formula; update to PROTOCOL_SPEC.md Phase 3 and CHARTER.md Kill Criteria Appendix

**Confidence:** High

---

### Q-015 — Phase 2 Matched Pairs: What Is the Complete Matching Protocol?

**Precise question:** For the Phase 2 matched pairs requirement (≥80 comparable trade pairs), what are: (a) the matching rule (entry signal instance vs. type), (b) the time-proximity bound (±N days), (c) the binary classification rule for "overlay state" (active/inactive based on what threshold?), and (d) the treatment of regime-confounded pairs?

**Why it matters:** Undefined matching will be operationalized at reporting time — creating a behavioral integrity gap where the developer can choose the matching rule that produces the most favorable comparison. (Finding F-16)

**Missing evidence:** All four sub-questions are undefined in the spec.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Phase 2; `docs/CHARTER.md` Phase 2; `docs/AUDIT_v1.md` F-16

**Method:** Design comparison (instance vs. type matching has very different statistical properties); threat model for cherry-picking via matching rule choice

**Expected deliverable:** ADR + pre-registration template for Phase 2 matched pair evaluation; addition to PROTOCOL_SPEC.md Phase 2 section

**Confidence:** High

---

### Q-016 — Purge/Embargo: What Is the Formula for 4H and 1D Signals?

**Precise question:** For 4H signals with a maximum holding period of X bars, and for 1D signals with a maximum holding period of Y bars, what is the purge/embargo length in days? What is "proportional to maximum holding period" as a precise formula? Does it apply per-feature, per-signal, or per-walk-forward window boundary?

**Why it matters:** Prerequisite for Phase 0 evaluation engine passing the leakage audit. RDL-3 FeatureSpec versioning (v1.2 addition) may require a per-feature embargo for new feature versions introduced mid-walk-forward. (Finding F-12; RS-16)

**Missing evidence:** Only "proportional to maximum holding period" stated. No formula, no values, no per-feature specification.

**Recommended files:** `docs/audience/ARCHITECT_BRIEF.md` Section B; `docs/PROTOCOL_SPEC.md` Phase 0 exit criteria, Section I Q4; `docs/AUDIT_v1.md` Q4, F-12

**Method:** Literature check (Roberts & Symmonds embargo formula for walk-forward; Prado's purged cross-validation); design comparison (single window vs. per-sample embargo)

**Expected deliverable:** GLOSSARY.md entry for "purge/embargo" with formula and values; update to Phase 0 exit criteria checklist

**Confidence:** High

---

### Q-017 — Timestamp Conventions: What Is the Complete Verification Checklist?

**Precise question:** For each data source (equity OHLCV, crypto OHLCV, funding rates, event calendar), what is the UTC offset? Is OHLCV data bar-open or bar-close aligned? Does the SimBroker use bar-open or bar-close for fill price? What is the 4H bar boundary convention (00:00/04:00 or exchange-specific)? For RDL-4 EventLabel objects, what timestamp convention applies to calendar events vs. funding spikes?

**Why it matters:** A one-bar timestamp misalignment produces entry fills at wrong prices for 100% of trades. ARCHITECT_BRIEF.md recognizes this as advisory but it is not in Phase 0 exit criteria. RDL-4 adds new event data sources with potentially different timestamp conventions. (Finding F-17; RS-17)

**Missing evidence:** Not in Phase 0 exit criteria. No explicit timestamp verification protocol anywhere.

**Recommended files:** `docs/audience/ARCHITECT_BRIEF.md` Section F; `docs/PROTOCOL_SPEC.md` Phase 0 exit criteria; `docs/AUDIT_v1.md` F-17

**Method:** Checklist design; threat model for each data source type

**Expected deliverable:** Timestamp convention checklist added to Phase 0 exit criteria in PROTOCOL_SPEC.md; GLOSSARY.md entry

**Confidence:** High

---

### Q-018 — GE-2/GE-3 Boundary: What Are the Bright-Line Rules?

**Precise question:** Specifically for: (a) zero-weight skill allocation, (b) skill allocation reduced to near-zero (<1% NAV) by cluster-cap enforcement, (c) differential weighting between 4H and 1D timeframes within a skill — which require GE-3 preregistration and which qualify for GE-2 exemption?

**Why it matters:** Zero-weight framing as GE-2 erodes the Harvey-Liu trial count, leaving multiplicity correction understated. Over a 15-month Phase 1 with multiple skill retirements, this creates a systematically understated haircut. Also creates a behavioral integrity gap. (Finding F-18)

**Missing evidence:** No bright-line rules for edge cases in PROTOCOL_SPEC.md Section J1 or GLOSSARY.md.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section J1; `docs/AUDIT_v1.md` F-18

**Method:** Invariant proof sketch (is zero-weight removal functionally equivalent to signal removal? if yes, GE-3 is logically required); threat model for trial count understatement over 15 months

**Expected deliverable:** ADR + spec update to PROTOCOL_SPEC.md Section J1 with bright-line rules

**Confidence:** High

---

### Q-019 — K5 Measurement Window: Rolling or Calendar Year?

**Precise question:** For K5 ("treasury > 60% total return in any 12-month period"), is the measurement window: (a) rolling monthly (evaluated at each month-end), (b) calendar year with fixed January cutoff, or (c) 12-month window from treasury activation date? For a portfolio where treasury yield exceeds 60% in months 7–18 but not in any fixed calendar year, does K5 fire?

**Why it matters:** K5 may fire or not fire for the same data depending on measurement period choice. The measurement window defines whether treasury masking is detected. (Finding F-20)

**Missing evidence:** "Any 12-month period" is stated without qualification.

**Recommended files:** `docs/CHARTER.md` Phase 5, Kill Criteria Appendix; `docs/PROTOCOL_SPEC.md` Section F (Phase 5), Section J; `docs/AUDIT_v1.md` F-20

**Method:** Scenario analysis: same data under three window definitions; design comparison for detection sensitivity

**Expected deliverable:** Spec update to CHARTER.md and PROTOCOL_SPEC.md Section J specifying rolling measurement

**Confidence:** High

---

### Q-020 — Phase 0 P1 Circuit Breaker Tests: What Is the Minimum Test Suite?

**Precise question:** What are the minimum required test scenarios for the Phase 0 P1 circuit breaker verification? At minimum: (a) simultaneous P1+P3 firing from 100% gross, (b) P1 recovery with P3 still active (State A from F-10), (c) restart mid-suspension, (d) partial position reduction interrupted mid-execution. Are there additional required scenarios for P4 state change during P1 active (State D)?

**Why it matters:** Phase 0 exit criterion says "tested with synthetic data and verified" — a single test case satisfies this as written. A developer can self-certify against an undefined protocol. (Finding F-21)

**Missing evidence:** No minimum test suite specified anywhere.

**Recommended files:** `docs/CHARTER.md` Phase 0 exit criteria; `docs/PROTOCOL_SPEC.md` Phase 0 exit criteria; `docs/audience/ARCHITECT_BRIEF.md` Section C; `docs/AUDIT_v1.md` F-21

**Method:** Checklist design; threat model for undertested P1 behavior in stress scenarios

**Expected deliverable:** Minimum test scenario list added to Phase 0 exit criteria in CHARTER.md and PROTOCOL_SPEC.md

**Confidence:** High

---

### Q-021 — FLAM Phase 3: What Is the Adjusted Formula for Mirrored Signals?

**Precise question:** If Phase 3 short signals are derived by mirroring Phase 1 long signals (ρ_IC between long and short = 0.6–0.9), what is the BR_eff for the combined book? What is the expected net Sharpe delta after applying this correlation? Does the result justify the Phase 3 positive-EV claim, or should Phase 3 be reclassified as exploratory?

**Why it matters:** At ρ_IC=0.8 (mirrored signals), BR_eff falls dramatically and net delta approaches zero. The Phase 3 development justification may be non-viable. This needs to be resolved before Phase 2 exit is evaluated (when F-8 must be re-evaluated as P0 if still Open). (Finding F-8; RS-05 related)

**Missing evidence:** PROTOCOL_SPEC.md I, Q2 documents this as open. No resolution in any document.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section E (Equity Shorts), Section I Q2; `docs/CHARTER.md` Correction 1, Phase 3; `docs/EVOLUTION.md` Section 6; `docs/AUDIT_v1.md` F-8

**Method:** First-principles derivation of adjusted FLAM at ρ_IC = 0.3, 0.6, 0.8; design comparison (mirrored vs. independent short signals)

**Expected deliverable:** ADR specifying assumed ρ_IC and adjusted BR_eff; either revised Phase 3 EV estimate or reclassification to exploratory

**Confidence:** High

---

### Q-022 — HWM Definition: When Does HWM Reset?

**Precise question:** At what events does the HWM (high-water mark) reset: (a) never (inception-to-date), (b) at each phase boundary, (c) annually, (d) when P1 circuit breaker completes recovery? For the P1 circuit breaker trigger ("DD from HWM ≥ 12%"), if the portfolio experiences a 10% drawdown followed by a 3% recovery followed by a further 5% drawdown, does P1 fire?

**Why it matters:** HWM reset timing directly affects P1 circuit breaker trigger frequency. With no reset: HWM grows over time, making new P1 triggers harder to reach after a prolonged recovery. With phase-boundary reset: allows a fresh drawdown budget each phase. Undefined HWM is an implementation ambiguity. (Finding F-19)

**Missing evidence:** HWM absent from GLOSSARY.md despite stated coverage claim.

**Recommended files:** `docs/CHARTER.md` Section D (P1 circuit breaker); `docs/PROTOCOL_SPEC.md` Section D; `docs/GLOSSARY.md`; `docs/AUDIT_v1.md` F-19

**Method:** Scenario analysis for each reset convention; design comparison

**Expected deliverable:** GLOSSARY.md entry for HWM with reset timing rule; update to PROTOCOL_SPEC.md Section D

**Confidence:** High

---

### Q-023 — Leakage Classes: What Is the Full Audit Checklist?

**Precise question:** Beyond temporal shuffling (which detects future price features only), the Phase 0 leakage audit must also check: (a) feature normalization leakage (normalization statistics computed on full dataset), (b) regime label look-ahead (P4 labels depend on future bars), (c) universe selection bias (assets selected post-hoc based on performance), (d) within-window optimization (parameters tuned within the walk-forward IS window). What is the exact verification step for each?

**Why it matters:** If Phase 0 leakage audit passes with temporal shuffling alone, classes (a)–(d) remain undetected through all phases. The addition of RDL-3 FeatureSpec versioning and RDL-4 EventLabel construction adds new potential leakage surfaces. (Finding F-14)

**Missing evidence:** ARCHITECT_BRIEF.md Q1 lists the undetected classes but no verification protocol.

**Recommended files:** `docs/CHARTER.md` Phase 0 exit criteria; `docs/PROTOCOL_SPEC.md` Phase 0 exit criteria; `docs/audience/ARCHITECT_BRIEF.md` Section B, Q1; `docs/AUDIT_v1.md` F-14

**Method:** Checklist design; threat model for each leakage class; design comparison for detection methods

**Expected deliverable:** Extended Phase 0 leakage audit checklist added to PROTOCOL_SPEC.md Phase 0 exit criteria

**Confidence:** High

---

### Q-024 — RDL-3 FeatureSpec Versioning vs. Purge/Embargo Interaction

**Precise question:** When a new FeatureSpec version is introduced mid-walk-forward (e.g., between IS window 3 and IS window 4), does the purge/embargo rule apply to the new feature version? If yes, what is the embargo duration (same as for the base signal, or feature-specific)? If a feature is used across multiple skills, is the embargo applied per-skill or per-feature?

**Why it matters:** New FeatureSpec versions introduced mid-walk-forward without per-version embargo could introduce a subtle leakage channel: the new feature was implicitly selected using information from prior IS windows. (RS-16; related to F-12)

**Missing evidence:** No interaction between FeatureSpec versioning and embargo rules defined anywhere.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section E (RDL-3); `docs/AUDIT_v1.md` F-12; `docs/audience/ARCHITECT_BRIEF.md` Section B

**Method:** Invariant proof sketch for leakage via feature versioning; design comparison for per-feature vs. per-signal embargo

**Expected deliverable:** ADR specifying FeatureSpec versioning embargo rule; addition to GLOSSARY.md

**Confidence:** Medium

---

### Q-025 — RBE + Kill Criteria: Which Kill Criteria Apply During RBE Activation?

**Precise question:** If an RBE step is formally activated (via charter-level review and preregistration), which kill criteria remain active during the RBE-altered portfolio state? Specifically: does K1 apply during an RBE transition period? Can an RBE step change the active skill set in a way that resets the K3 (N_eff) measurement window? Can it change the short book composition in a way that resets the K4 (t-stat) measurement window?

**Why it matters:** Kill criteria are designed as objective stopping rules. If RBE activation can implicitly reset measurement windows or change what is being measured, the kill criteria become gameable. (RS-15)

**Missing evidence:** No document addresses kill criteria behavior during RBE activation.

**Recommended files:** `docs/PROTOCOL_SPEC.md` Section J, J2; `docs/CHARTER.md` Kill Criteria Appendix; relevant: F-6, F-9

**Method:** Threat model for each kill criterion under an RBE activation scenario; invariant proof sketch for kill criterion independence from RBE

**Expected deliverable:** ADR specifying kill criteria behavior during RBE steps; update to PROTOCOL_SPEC.md Section J2

**Confidence:** Medium

---

## Secondary Research Questions (Q-026 through Q-050)

These questions are important but less immediately blocking. Address after Top Priority questions are resolved.

---

### Q-026 — What Is the Phase 2 IC Correlation Threshold for ρ(4H,1W)?

**Q:** The gating condition for Phase 2 states "empirical ρ(4H,1W) < 0.60 computed." What is the measurement period, population, and return interval? Is 0.60 derived or arbitrary?
**Matters:** If 4H and 1W signals are highly correlated, the 1W overlay adds no diversification benefit and fails P2K2.
**Method:** Literature check; design comparison
**Files:** `docs/PROTOCOL_SPEC.md` Section E (1W Overlay), Phase 2; `docs/GLOSSARY.md` IC
**Deliverable:** Measurement protocol + derivation of 0.60 threshold
**Confidence:** Medium

### Q-027 — What Does "Net Sharpe Delta on Matched Observations" Mean?

**Q:** "Net Sharpe Delta (from an extension) = improvement in net Sharpe computed on matched observations against pre-defined baseline." What is the baseline definition for Phase 2 1W overlay evaluation vs. Phase 3 equity shorts?
**Matters:** Different baseline definitions produce different deltas. Behavioral integrity gap.
**Files:** `docs/PROTOCOL_SPEC.md` Section C definition; Phase 2, Phase 3
**Method:** Design comparison; threat model for cherry-picked baseline
**Deliverable:** Spec update to definition with baseline construction protocol
**Confidence:** High

### Q-028 — Are AT-INF Hypotheses Counted in the Harvey-Liu Budget?

**Q:** The spec discusses AT-INF (influencer-derived) hypotheses with a 60-day embargo and historical base rate pre-check. Do AT-INF registrations count toward the Harvey-Liu trial budget? If 20 AT-INF hypotheses are pre-registered over Phase 0–1, what is the haircut impact?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Exit Overlays), NN-5; `docs/CHARTER.md` Hypothesis Acceleration Track
**Method:** Scenario analysis at 5, 10, 20 AT-INF trials with each Harvey-Liu variant
**Deliverable:** Clarification in PROTOCOL_SPEC.md NN-5 on AT-INF trial counting
**Confidence:** Medium

### Q-029 — Walk-Forward Window Parameters: What Defines a Valid OOS Window?

**Q:** Phase 1 uses "4-year IS window with annual roll." What is the minimum OOS window length? How many OOS windows are required for the 15-month OOS requirement to be satisfied (one 15-month window or three 5-month annual rolls)?
**Files:** `docs/PROTOCOL_SPEC.md` Phase 1 exit criteria, Section F; `docs/GLOSSARY.md`; `docs/AUDIT_v1.md` F-19
**Method:** Design comparison; implications for K1 statistical power
**Deliverable:** GLOSSARY.md entry for walk-forward window parameters
**Confidence:** High

### Q-030 — Universe Selection: How Are the ~20 Assets Chosen and Frozen?

**Q:** "Top 4 per sector/cluster" — what is the selection criterion (market cap? liquidity? volume?)? When is the universe frozen for Phase 1? Can assets be replaced if a selected asset delists? Does universe change count as a GE-3 event?
**Files:** `docs/PROTOCOL_SPEC.md` Section E; `docs/CHARTER.md`
**Method:** Design comparison; threat model for universe selection bias (F-14 class c)
**Deliverable:** Universe selection and lock protocol; GE-3 classification for universe changes
**Confidence:** Medium

### Q-031 — What Is the Minimum Data History Required Before Phase 0 Can Begin?

**Q:** Phase 0 exit requires "P4 historical label series covering ≥3 years." Is 3 years of clean data a prerequisite for starting Phase 0, or can Phase 0 begin with shorter history and extend as data accumulates?
**Files:** `docs/PROTOCOL_SPEC.md` Phase 0 exit criteria
**Deliverable:** Clarification in Phase 0 prerequisites
**Confidence:** Medium

### Q-032 — P2 Funding Exit Recovery: What Counts as ≥5 Consecutive Windows?

**Q:** P2 recovery condition: "funding < 0.03%/8hr for ≥5 consecutive 8-hour windows." Are weekend/low-activity windows counted? What if funding is exactly 0.03% (boundary condition)?
**Files:** `docs/PROTOCOL_SPEC.md` Section D; `docs/CHARTER.md` Section D
**Method:** Boundary condition analysis; threat model for delayed P2 recovery
**Deliverable:** Clarification in PROTOCOL_SPEC.md Section D
**Confidence:** Medium

### Q-033 — Does the 8-Week Minimum Regime Instance Requirement Interact with Phase 1 Exit Timing?

**Q:** "A regime instance requires ≥8 consecutive weeks to count toward OOS spanning requirements. Fragments < 8 weeks are excluded." If a market transition occurs in the last 8 weeks of Phase 1 OOS, and the new regime has not yet accumulated 8 weeks, does the Phase 1 OOS spanning requirement (≥2 distinct regime instances) potentially fail even with 15 months of OOS data?
**Files:** `docs/PROTOCOL_SPEC.md` Section C definition of "Regime"; Phase 1 exit criteria
**Method:** Scenario analysis; boundary condition
**Deliverable:** Clarification in Phase 1 exit criteria
**Confidence:** High

### Q-034 — Is There a Paper Trading Duration Requirement Separate from Walk-Forward OOS?

**Q:** The spec says "always labeled 'Paper' — never combined with walk-forward OOS results." For Phase 2 entry, it requires "6-month paper comparison." Is this 6 months of live paper trading or can it use simulated paper trading from historical data? What is the difference in evidentiary weight?
**Files:** `docs/PROTOCOL_SPEC.md` Phase 2 entry criteria; definition of "Paper Trading" in Section C
**Method:** Threat model for simulated vs. live paper trade distinction
**Deliverable:** Clarification in Phase 2 entry criteria
**Confidence:** Medium

### Q-035 — How Are Skill Timeframes Weighted in the Portfolio Layer?

**Q:** Each skill operates at 4H and 1D. In the Portfolio Layer, when both 4H and 1D versions of the same skill signal in the same direction, how are their position targets combined? Is one timeframe given priority? Is there a blending formula?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Portfolio Layer); `docs/GLOSSARY.md`
**Method:** Design comparison; threat model for double-counting factor exposure
**Deliverable:** GLOSSARY.md entry; PROTOCOL_SPEC.md Section E clarification
**Confidence:** Medium

### Q-036 — What Triggers the "Pre-Registration Required" for AT-002 (Weekly H/L) Exit Overlays?

**Q:** AT-002 and AT-003 are Category 1 (no-optimization) exit overlays. The spec says they require pre-registration. At what granularity must the pre-registration specify the exit rule: (a) "use weekly high as TP for any long position" or (b) a more specific rule including asset class, position size threshold, and holding period?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Exit Overlays); `docs/CHARTER.md` Hypothesis Acceleration Track
**Method:** Design comparison; threat model for over-specified vs. under-specified pre-registration
**Deliverable:** Pre-registration template for Category 1 exit overlays
**Confidence:** Medium

### Q-037 — What Is the RDL-1 Hypothesis Object Format and Required Fields?

**Q:** RDL-1 produces `CandidateHypothesis` objects "with pre-specified entry condition, metric, threshold, and minimum sample." Is there a complete schema? Are there required fields beyond these four? What happens if a submitted object is missing a field?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (RDL-1)
**Method:** Schema design; threat model for incomplete pre-registration
**Deliverable:** Complete `CandidateHypothesis` schema definition
**Confidence:** Medium

### Q-038 — How Does the Vol Targeting Mechanism Interact with P1 Exposure Reduction?

**Q:** The Portfolio Layer includes "vol targeting." If P1 fires and reduces all positions to 50%, does the vol targeting mechanism then immediately signal to increase positions back toward the vol target? Is there a rule governing vol targeting behavior during P1/P3 active periods?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Portfolio Layer); Section D (Regime Signal Governance)
**Method:** State machine analysis; threat model for vol targeting fighting regime signal reduction
**Deliverable:** Clarification in PROTOCOL_SPEC.md Section D or E
**Confidence:** Medium

### Q-039 — What Is the Brier Score Measurement Protocol for Source Scoring?

**Q:** The spec uses Brier score for source scoring (1-axis until ≥50 calls/source). What is the resolution period for each "call"? What constitutes a "call" (any market prediction, or only predictions meeting a specificity threshold)?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Insight Layer); `docs/GLOSSARY.md`
**Deliverable:** Brier score measurement protocol; "call" definition
**Confidence:** Low (deferred to Era 4; lower immediate relevance)

### Q-040 — What Is the Cost Model for Tier-1 PoS Staking in the Treasury Layer?

**Q:** The treasury uses "T-Bill equivalents or Tier-1 PoS staking (ETH/SOL) only." What is the cost model for staking (slashing risk, lock-up, unstaking period)? How is stream (d) measured for PoS staking?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Treasury Layer); `docs/CHARTER.md` Phase 5
**Deliverable:** Treasury cost model for PoS staking; stream (d) measurement protocol for staking
**Confidence:** Low (Phase 5 deferred; lower immediate relevance)

### Q-041 — How Are Cluster-Level and Asset-Level Exposure Caps Enforced Together?

**Q:** The spec references "cluster-level P&L correlations" and "cluster cap." Are cluster caps defined as a maximum fraction of NAV per cluster? If so, what is the cap? If a cluster cap forces a skill to near-zero weight, does this trigger a GE-3 event?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Portfolio Layer); `docs/AUDIT_v1.md` F-18
**Method:** Invariant proof sketch
**Deliverable:** Cluster cap definition; GE-3 interaction rule
**Confidence:** Medium

### Q-042 — What Happens to the Trial Registry When a Phase Gate Fails (Kill)?

**Q:** If K1 fires (project kill), the trial registry has accumulated many entries. If the project is restarted with a modified approach, are prior trial entries carried forward (increasing the Harvey-Liu budget from day one) or is the registry reset?
**Files:** `docs/PROTOCOL_SPEC.md` NN-5; `docs/CHARTER.md` NN-5; `docs/GLOSSARY.md`
**Deliverable:** Trial registry continuation/reset rule on kill decision
**Confidence:** Low (hypothetical scenario; lower immediate relevance)

### Q-043 — Does the 20-Asset Universe Constraint Bind During Phase 3+?

**Q:** With shorts added in Phase 3, "top 4 per sector/cluster" for long positions may not map cleanly to the same 20 assets for short positions. Are shorts limited to the same 20-asset universe? Can a short be entered on an asset not in the long universe?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Equity Shorts); `docs/CHARTER.md`
**Deliverable:** Short universe definition; whether it must equal long universe
**Confidence:** Medium

### Q-044 — What Are the Specific Features Used by Each of the 5–6 Base Skills?

**Q:** The spec names skill categories (trend, reversion, vol-regime) but not the specific feature inputs for each. Are these features pre-registered for Phase 1, or defined during Phase 0 development?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (Skills); `docs/CHARTER.md`
**Deliverable:** Feature specification template for base skills; pre-registration requirement
**Confidence:** Low (implementation detail; Phase 0 deliverable; not a spec gap)

### Q-045 — Is There a Maximum Number of RDL Hypothesis Submissions Per Cycle?

**Q:** No rate limit on RDL-1 hypothesis submission is stated. If a developer submits 100 CandidateHypothesis objects in a single day, all are counted in the Harvey-Liu trial budget from that moment. Is there a governance rule limiting the rate or total count of RDL submissions before Phase 2?
**Files:** `docs/PROTOCOL_SPEC.md` Section E (RDL-1, RDL governance)
**Method:** Threat model for Harvey-Liu budget inflation via RDL
**Deliverable:** Rate governance rule for RDL submissions (or explicit statement that no rate limit applies)
**Confidence:** Medium

### Q-046 — Does P4K2 ("Combined Short Book Sharpe Delta") Use the Same Matched-Pair Definition as Phase 2?

**Q:** P4K2 fires if "combined short book Sharpe delta < 0 for 2 consecutive 6-month windows." What is the baseline for this delta? The same matched-pair definition as Phase 2 (Q-015), or a different one?
**Files:** `docs/PROTOCOL_SPEC.md` Section J; `docs/CHARTER.md` Kill Criteria Appendix
**Deliverable:** P4K2 measurement baseline definition
**Confidence:** Medium

### Q-047 — Are the ARCHITECT_BRIEF.md Open Questions (Q1–Q14) Now All Closed?

**Q:** ARCHITECT_BRIEF.md lists 14 open questions (Q1–Q14). How many of these are answered in PROTOCOL_SPEC.md v1.2? Which remain open? Do any of the v1.2 additions (RDL, Growth Layer) implicitly address any questions?
**Files:** `docs/audience/ARCHITECT_BRIEF.md`; `docs/PROTOCOL_SPEC.md` v1.2
**Method:** Systematic cross-reference
**Deliverable:** Updated Q status table in ADVERSARIAL_REVIEW.md
**Confidence:** High

### Q-048 — Does the Growth Layer "Efficiency Metrics" Section (J1) Introduce New Kill Criteria?

**Q:** Section J1 adds Growth Layer & Efficiency Metrics. Does any metric in J1 define a new kill condition or trigger a kill criterion evaluation? Or are all J1 metrics monitoring-only until RBE activation?
**Files:** `docs/PROTOCOL_SPEC.md` Section J1; `docs/CHARTER.md` Kill Criteria Appendix
**Method:** Systematic check of all J1 metrics against kill criteria list
**Deliverable:** Clarification that J1 is monitoring-only; or identification of implicit new kill conditions
**Confidence:** Medium

### Q-049 — Can a Phase 1 Walk-Forward Run Satisfy Phase 2 Paper Trading Requirement Simultaneously?

**Q:** Phase 1 is walk-forward OOS. Phase 2 entry requires "6-month paper comparison." If Phase 1 includes live paper trading for the last 6 months (on top of walk-forward), does that paper period simultaneously satisfy the Phase 2 paper requirement?
**Files:** `docs/PROTOCOL_SPEC.md` Phase 1 exit criteria, Phase 2 entry criteria; definition of "Paper Trading"
**Method:** Boundary condition analysis
**Deliverable:** Clarification in phase sequencing rules
**Confidence:** Medium

### Q-050 — What Is the Expected Turnover and Its Effect on Cost Budget (K2)?

**Q:** K2 fires if "costs > 50% gross simulated return for 2 consecutive quarters." What is the expected annual turnover for the 5–6 base skills at 4H/1D? At the spec's base rates (0.08% equity commissions + 0.02% impact + 0.02% slippage = 0.12%/leg × 2 legs), what is the break-even gross Sharpe required for K2 not to fire?
**Files:** `docs/PROTOCOL_SPEC.md` Section C (cost model), Section J (K2); `docs/CHARTER.md` Kill Criteria Appendix
**Method:** First-principles turnover estimate from holding period assumptions; K2 break-even derivation
**Deliverable:** K2 break-even analysis as a spec annex or GLOSSARY entry
**Confidence:** High

---

*Cycle: 1 | Date: 2026-03-04 | Pipeline: v1.0*
*Top priority questions: Q-001 through Q-025 (25 questions; all Phase 0 relevant)*
*Secondary questions: Q-026 through Q-050 (25 questions; Phase 0–2 relevant)*
*See also: docs/audit/REVIEW_REPORT.md (findings), docs/tasks.md (task backlog), docs/audit/PROMPT_0_META.md (risk surface register)*
