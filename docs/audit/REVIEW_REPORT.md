# Entropy Protocol — Consolidated Review Report

**Classification:** Confidential — Internal Audit Document
**Filename:** `docs/audit/REVIEW_REPORT.md`
**Audit Cycle:** Phase 0 Baseline (Cycle 0)
**Pipeline Version:** v1.0
**Date:** 2026-03-04
**Status:** Draft — Awaiting Spec Owner Acceptance
**Source:** Baseline consolidation from `docs/AUDIT_v1.md` v1.0
**Note:** This is a pre-pipeline baseline. Steps 1–5 of the formal audit pipeline have not yet been executed. This report consolidates findings from the external audit document only. Steps 1–5 artifacts (META_ANALYSIS, ARCH_MODEL, INVARIANTS, DRIFT_ASSERTIONS, DRIFT_REPORT, ADVERSARIAL_REVIEW) are pending the first formal pipeline run.

---

## Executive Summary

**Dominant risk theme:** The evaluation system's evidentiary backbone — the Sharpe confidence interval, the Harvey-Liu multiplicity correction, and the P4 regime classifier — are each underspecified or miscalculated in ways that will produce invalid performance claims or unverifiable phase gate decisions without the failure being detectable at Phase 1 exit.

**Total findings: 21**
- P0 (CRITICAL, block phase gating): 5
- P1 (HIGH, required before next phase): 6
- P2 (MEDIUM/LOW, time-bounded): 10

**All 21 findings are Open.** The source audit (AUDIT_v1.md) status is "Awaiting author responses to Open Questions." No finding has been acknowledged, mitigated, or closed by any document in the repository as of 2026-03-04.

**Consequence of current state:** Phase 1 cannot begin until all P0 findings are resolved and the REVIEW_REPORT is accepted by the Spec Owner. Phase 0 development may proceed but must not produce OOS performance claims until P0 findings F-1, F-2, F-3, F-4, and F-5 are addressed.

**Open questions requiring author response:** Q1–Q10 (enumerated in source audit). Each is directly traceable to a P0 or P1 finding.

---

## Finding Inventory by Severity

### P0 — CRITICAL (Block Phase Gating)

---

#### F-1 — Harvey-Liu Formula Variant Not Specified

**Task:** TASK-AF-001
**Status:** Open
**Confidence:** High (formula gap confirmed across all five source documents; Q12 in ARCHITECT_BRIEF.md directly confirms the gap)

**Location:** CHARTER.md NN-5; PROTOCOL_SPEC.md NN-5, Section J, Phase 1 metrics; GLOSSARY.md ("Deflated Sharpe (Harvey-Liu)")

**Evidence:**
- CHARTER.md NN-5: "Harvey-Liu deflation is mandatory when net Sharpe < 0.40."
- GLOSSARY.md: "Deflated Sharpe (Harvey-Liu): Net Sharpe with a haircut applied to account for the number of strategies tested in the trial registry."
- PROTOCOL_SPEC.md Phase 1 metrics: "Harvey-Liu deflated Sharpe | Reported alongside raw; haircut < 0.05 | Flag if haircut > 0.08."
- No document contains a formula or parameter specification.
- ARCHITECT_BRIEF.md Q12: "How would you implement trial count aggregation in a way that is robust to partial registry entries?" — listed as open and unresolved, directly confirming the gap.

**Impact:** The Harvey-Liu haircut flag threshold (<0.05 Sharpe units, flag if >0.08) is a Phase 1 exit criterion gating condition. If the formula is implemented incorrectly — wrong variant, wrong trial count, or wrong cross-phase aggregation — the declared haircut is meaningless, and the Phase 1 exit criterion is unverifiable. The correction provides false rigor rather than actual protection.

**Impact categories:** (A) Invalid performance claims; Phase 1 exit criterion unverifiable.

**Next action:** Author must answer Q1 from source audit. Spec addition required in PROTOCOL_SPEC.md NN-5 and GLOSSARY.md.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-001.

---

#### F-2 — Sharpe Confidence Interval Claim Is Materially Wrong

**Task:** TASK-AF-002
**Status:** Open
**Confidence:** High (arithmetic derivation shown in source audit; no alternative framework provided in any document)

**Location:** CHARTER.md Section C; PROTOCOL_SPEC.md Sections C, F, H; GLOSSARY.md ("Net Sharpe")

**Evidence:**
- All three documents state: "At 15 months OOS, CI ≈ ±0.15–0.20 for a ~0.30-Sharpe system (68%)."
- Standard asymptotic formula: `SE(SR_annual) = sqrt((1 + SR²/2) / T)` at T=1.25 years yields SE ≈ 0.914.
- The stated ±0.15–0.20 would require approximately 34 years of annual observations.
- Phase 1 CI (annualized Sharpe) and Phase 2 CI (per-trade P&L difference) are computed on incommensurable scales.
- No derivation exists in any of the five documents.

**Impact:** (1) K1 false-kill and missed-kill rates are uncalibrated — a failing system has ~44% chance of not triggering K1. (2) The pivot criterion (0.22–0.28) is statistically indistinguishable from the kill threshold (0.28) under the true CI. (3) All CI-referenced evaluation reports will overstate precision by 4–6×.

**Impact categories:** (A) Invalid performance claims; (B) Incorrect kill decisions.

**Next action:** Author must answer Q2 from source audit. If no derivation exists, replace CI with ±0.89 and cascade to all dependent decision thresholds.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-002.

---

#### F-3 — P3 Correlation Trigger Population Undefined

**Task:** TASK-AF-003
**Status:** Open
**Confidence:** High (all five documents use identical language with no population specification)

**Location:** CHARTER.md Section D; PROTOCOL_SPEC.md Section D; GLOSSARY.md ("Regime Signal Hierarchy"); ARCHITECT_BRIEF.md Section C

**Evidence:**
- All documents: "20-day rolling avg pairwise ρ > 0.55 | Reduce gross exposure 35–50% over 3 business days."
- Population candidates (each producing materially different trigger frequencies): all 20 assets (price correlation), active long positions, active positions including shorts (Phase 3+), skill-level P&L correlations, cluster-level P&L correlations.
- PROTOCOL_SPEC.md Section I, Q14: "Is the P3 recovery threshold (ρ < 0.45) appropriate for the target universe?" — does not acknowledge the population definition gap.

**Impact:** (C) Undetected state corruption. P3 can be triggered inconsistently across evaluation periods — firing on one definition during Phase 1 and a different definition (with shorts added) during Phase 3. This corrupts the regime signal hierarchy state in ways not detectable from the output signal alone.

**Next action:** Author must answer Q3 from source audit. Definition must be locked before Phase 0 P3 implementation begins.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-003.

---

#### F-4 — P4 Signal Algorithm Undefined

**Task:** TASK-AF-004
**Status:** Open
**Confidence:** High (PROTOCOL_SPEC.md Section E refers to "P4 signal specification (pre-registered)" that does not exist in any of the five documents)

**Location:** CHARTER.md Section D; PROTOCOL_SPEC.md Sections D, E, F; ARCHITECT_BRIEF.md Section C

**Evidence:**
- PROTOCOL_SPEC.md Section E ("1W Regime Overlay"): "Inputs: Weekly OHLCV, P4 signal specification (pre-registered)" — refers to a specification that does not exist.
- Phase 0 exit criterion: "P4 produces historically labeled regime series covering ≥3 years" — labeled by what rule?
- Phase 1 OOS spanning requirement uses P4 labels ("≥2 distinct regime instances").
- Phase 2 IC correlation requirement (ρ(4H,1W)) cannot be computed without a defined P4.
- ARCHITECT_BRIEF.md Q4 asks how to architect regime signal versioning — presupposes algorithm will be defined but does not state it currently is not.

**Impact:** (A)(B)(C) All three primary failure modes. Phase 0 exit criterion is unverifiable by a third party. Phase 1 OOS spanning is indeterminate without a defined algorithm. Regime label immutability is meaningless without a versioned algorithm.

**Next action:** Author must answer Q4 and Q5 from source audit. P4 spec must be pre-registered before Phase 0 historical labeling begins.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-004.

---

#### F-5 — IC_long Assumption Load-Bearing and Unvalidated; No Suspect Threshold

**Task:** TASK-AF-005
**Status:** Open
**Confidence:** High (asymmetric treatment vs. IC_short is documented; FLAM arithmetic is verifiable from spec's own N_eff figure)

**Location:** GLOSSARY.md ("IC"); PROTOCOL_SPEC.md Section I, Q1; CHARTER.md Correction 1

**Evidence:**
- GLOSSARY.md: "IC_long: 0.03–0.05 assumed for long-side skills (moderate; not verified until Phase 1)."
- IC_short has explicit suspect threshold (>0.04), haircut rule, and correction in EVOLUTION.md Section 6. IC_long has none.
- PROTOCOL_SPEC.md H1: N_eff ≈ 2.4 at ρ_avg=0.30 → BR_eff ≈ 96 (not 240); reduces FLAM gross Sharpe by 1.58×.
- At ρ_avg=0.40: BR_eff ≈ 71, FLAM gross ≈ 0.25 — below K1=0.28.
- FLAM BR_long formulation "5 × 2 × 12 ≈ 240" is dimensionally ambiguous (5×2×12=120, not 240).
- No literature citation supports 0.03–0.05 as the prior for this universe.

**Impact:** (A)(B) If IC_long is below assumed range, the system will fail K1 at Phase 1 exit with no prior diagnostic signal, having consumed 15+ months. Absence of an IC_long suspect threshold means high in-sample IC_long values will not be flagged as potential overfitting, producing false-positive Phase 1 exit certifications.

**Next action:** Define IC_long suspect threshold, FLAM BR_eff correction, and literature citation. Update CHARTER.md and GLOSSARY.md.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-005.

---

### P1 — HIGH (Required Before Next Phase)

---

#### F-6 — K4 Missed-Kill Probability Unspecified

**Task:** TASK-AF-006
**Status:** Open
**Confidence:** High (missed-kill rate calculable from t-distribution at stated threshold)

**Location:** CHARTER.md Correction 2, Kill Criteria Appendix; PROTOCOL_SPEC.md Phase 3, Section J; EVOLUTION.md Section 7

**Evidence:**
- CHARTER.md Correction 2: "P(false kill at t < 0.5 threshold) ≈ 60%. This is still too high for a definitive kill. The criterion is accepted as a screening threshold." — no statement of missed-kill rate.
- Derivation: For genuinely dead short book (IC=0), P(K4 does NOT fire) = P(t(89) > 0.5) ≈ 31%. A dead short book survives K4 with 31% probability.
- K4 also requires ≥90 trades AND 18 months elapsed — if 90 trades not reached, K4 is never evaluated regardless of performance.

**Impact:** (B) A dead short book surviving K4 (31% probability) proceeds to Phase 3 exit consideration, where net Sharpe delta criterion might be marginally satisfied by sampling variance. K4 is miscalibrated in both directions simultaneously.

**Next action:** Document both false-kill and missed-kill rates. Record decision on whether threshold is accepted or adjusted. Update EVOLUTION.md with rationale.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-006.

---

#### F-7 — Regime Label Vintage Contamination

**Task:** TASK-AF-007
**Status:** Open
**Confidence:** High (structural overlap between P4 calibration window and Phase 1 WFO IS windows is a direct consequence of Phase 0 exit criterion timeline)

**Location:** CHARTER.md Phase 0 exit criteria, Section D; PROTOCOL_SPEC.md Phase 0 exit criteria, Phase 1 OOS spanning; ARCHITECT_BRIEF.md Section D

**Evidence:**
- Phase 0 exit: P4 calibrates on ≥3 years historical data.
- Phase 1 WFO: 4-year IS window with annual roll.
- If P4 involves parameter fitting, calibration window overlaps with Phase 1 IS windows → labels for those windows are in-sample, not contemporaneous.
- "Regime label immutability" (CHARTER.md Section D) addresses Phase 2 recalibration risk but not Phase 0 vintage contamination.
- ARCHITECT_BRIEF.md Section D addresses Phase 2 only. "Known Gap" section confirms nested recovery gap but not vintage contamination.

**Impact:** (A)(C) If Phase 1 OOS spanning is certified using P4 labels produced with in-sample information, the spanning requirement is satisfied on invalid grounds. Propagates to all subsequent phase gate decisions.

**Next action:** Author must answer Q5 from source audit. If P4 involves parameter fitting, calibration procedure must specify how overlapping IS windows are excluded from OOS spanning counts.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-007.

---

#### F-8 — FLAM Phase 3 Justification Rests on Unresolved Assumption

**Task:** TASK-AF-008
**Status:** Open (DOCUMENTED — PROTOCOL_SPEC.md Section I, Q2 explicitly lists this as an open external question)

**Confidence:** High (arithmetic derivation shown; independence assumption directly contradicted by spec language "repurposed/mirrored")

**Location:** CHARTER.md Correction 1, Phase 3; PROTOCOL_SPEC.md Section E, Section I Q2; EVOLUTION.md Section 6

**Evidence:**
- PROTOCOL_SPEC.md I, Q2: "Is the marginal FLAM formula appropriate for a system where long and short signals are correlated (derived from the same skill set)?" — listed as open.
- PROTOCOL_SPEC.md Section E: "Inputs: Long-side skill signals (repurposed/mirrored for short direction)."
- At ρ_IC=0.8 (mirrored skill): BR_eff=21.6; net delta after costs approaches zero or negative.
- Published range +0.01–0.05 achievable only if IC_long and IC_short are uncorrelated — directly contradicted by the mirroring statement.

**Impact:** (A) Phase 3 expected net Sharpe delta may be zero or negative if signal correlation is moderate-to-high, making the stated Phase 3 development justification non-viable.

**Next action:** Resolve Q2. Either (a) compute adjusted FLAM with ρ_IC assumption stated, or (b) reclassify Phase 3 as exploratory with no positive-EV claim.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-008.

---

#### F-9 — No SimBroker Drift Kill Criterion in Phase 1

**Task:** TASK-AF-009
**Status:** Open
**Confidence:** High (monitoring flag exists; no kill action specified; gap between K6 active phase and Phase 1 is explicit)

**Location:** CHARTER.md Kill Criteria Appendix, Phase 1 metrics; PROTOCOL_SPEC.md Sections F, J; ARCHITECT_BRIEF.md Section E

**Evidence:**
- CHARTER.md Phase 1 metrics: "SimBroker cost accuracy | Within 15% of paper fills | Flag if > 15% for 2 consecutive months" — no kill action.
- CHARTER.md Kill Criteria: K6 active from Phase 3–4 only.
- ARCHITECT_BRIEF.md Q5: "If SimBroker has a systematic bias, all kill criteria will be miscalibrated in the same direction." — listed as open.
- A system passing K1 with point estimate 0.30 may have true net Sharpe 0.22 if costs understated ~25%.

**Impact:** (B) Systematic SimBroker cost underestimation in Phase 1 produces a false-positive Phase 1 exit certification. All subsequent phases begin from a contaminated baseline.

**Next action:** Define a Phase 1 SimBroker cost kill criterion (K6-Phase1 or equivalent). Update CHARTER.md and PROTOCOL_SPEC.md Sections F and J.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-009.

---

#### F-10 — P1+P3 Concurrent Activation and Sequential Recovery Undefined

**Task:** TASK-AF-010
**Status:** Open (DOCUMENTED — ARCHITECT_BRIEF.md Section C explicitly acknowledges as known gap)

**Confidence:** High (gap acknowledged by prior architect review; four specific unresolved states enumerated)

**Location:** CHARTER.md Section D; PROTOCOL_SPEC.md Section D; ARCHITECT_BRIEF.md Section C

**Evidence:**
- CHARTER.md conflict rule 1: "Higher-priority signal always takes precedence." Defines simultaneous firing priority only.
- ARCHITECT_BRIEF.md Section C "What Is Not Addressed (Known Gap)": "The recovery from P3 that occurs while P1 recovery criteria are also pending should be explicitly handled in the harness implementation. The current spec is silent on nested recovery sequencing."
- Four unresolved states: (A) P1 recovers while P3 still active — target gross?, (B) P3 triggers during P1 5-day suspension window, (C) P3 ramp interrupted mid-execution by P1, (D) P4 state change during P1 active period.

**Impact:** (C) In a stress scenario (≥12% DD coinciding with correlation spike), P1 and P3 will fire simultaneously or in rapid succession. Undefined recovery sequencing means harness and paper trading implementations may default to different developer judgments, producing systematic evaluation-vs-execution mismatch.

**Next action:** Author must answer Q7 from source audit. Four states must be specified with deterministic rules before Phase 0 P1/P3 implementation begins.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-010.

---

#### F-11 — N_eff Approximation Inaccurate for Heterogeneous Portfolios

**Task:** TASK-AF-011
**Status:** Open
**Confidence:** High (arithmetic example shown; same data gives N_eff=2.07 vs 3.0 depending on formula — straddles K3 threshold)

**Location:** PROTOCOL_SPEC.md Sections H, J1; GLOSSARY.md ("N_eff"); ARCHITECT_BRIEF.md Section E

**Evidence:**
- Formula used: `k / (1 + (k−1) × ρ_avg)` — valid only for equicorrelation model.
- For heterogeneous 3-cluster portfolio (trend/reversion/vol-regime): equicorrelation gives N_eff=2.07 (K3 triggers); eigenvalue-based gives N_eff≈3.0 (K3 does not trigger).
- ARCHITECT_BRIEF.md R1: "N_eff=2.4 at ρ_avg=0.3 — barely above K3 threshold" — proximity acknowledged; formula accuracy not questioned.

**Impact:** (B) K3 fires at N_eff ≤ 2 for 2 consecutive months. Given spec's own estimate N_eff≈2.4 in normal conditions, formula accuracy at this margin is directly consequential.

**Next action:** Author must answer Q6 from source audit. Specify formula for K3 purposes; if equicorrelation retained, cite evidence of adequacy at N_eff≈2.0–2.5.

**Acceptance criterion:** See `docs/tasks.md` TASK-AF-011.

---

### P2 — MEDIUM/LOW (Time-Bounded Remediation)

---

#### F-12 — Purge/Embargo Duration Not Specified

**Task:** TASK-AF-012 | **Status:** Open | **Confidence:** High (confirmed unresolved by PROTOCOL_SPEC.md I, Q4)

**Location:** ARCHITECT_BRIEF.md Section B; PROTOCOL_SPEC.md Phase 0 exit criteria, I Q4

**Evidence:** "Proportional to maximum holding period" is not a formula. Q4 listed as open external question.

**Impact:** (A) Inadequate embargo allows training labels to overlap with validation-window prices, inflating Sharpe. A Phase 0 that passes the leakage audit without a defined embargo may certify a harness with systematic label leakage.

---

#### F-13 — P3 Reduction Range Has No Selection Protocol

**Task:** TASK-AF-013 | **Status:** Open | **Confidence:** High

**Location:** CHARTER.md Section D; PROTOCOL_SPEC.md Section D; ARCHITECT_BRIEF.md Section C

**Evidence:** "Reduce gross exposure 35–50% over 3 business days" — no selection rule within the range.

**Impact:** (C) If harness uses 40% and paper trading uses 50%, P3 creates a 15-percentage-point gross exposure mismatch — unreproducible evaluation results.

---

#### F-14 — Temporal Shuffling Insufficient for Full Leakage Detection

**Task:** TASK-AF-014 | **Status:** Open (DOCUMENTED — ARCHITECT_BRIEF.md Q1 explicitly asks whether temporal shuffling is sufficient)

**Location:** CHARTER.md Phase 0 exit criteria; PROTOCOL_SPEC.md Phase 0 exit criteria; ARCHITECT_BRIEF.md Section B, Q1

**Evidence:** Four undetected leakage classes: (a) feature normalization leakage, (b) regime label look-ahead, (c) universe selection bias, (d) within-window optimization.

**Impact:** (A) If Phase 0 leakage audit passes with temporal shuffling alone, classes (a)–(d) remain undetected throughout all phases.

---

#### F-15 — K4 T-Statistic Formula Not Specified

**Task:** TASK-AF-015 | **Status:** Open | **Confidence:** High (formula (a) implied by "expected t ≈ 0.24" but never stated)

**Location:** CHARTER.md Correction 2, Kill Criteria Appendix; PROTOCOL_SPEC.md Phase 3, Section J

**Evidence:** Three candidate formulas give materially different values. Formula (a) per-trade t-statistic is implied but not documented.

**Impact:** (B) K4 decision is formula-sensitive; undocumented formula choice introduces implementation ambiguity.

---

#### F-16 — Phase 2 Matched Pair Criteria Undefined

**Task:** TASK-AF-016 | **Status:** Open | **Confidence:** High

**Location:** CHARTER.md Phase 2; PROTOCOL_SPEC.md Phase 2

**Evidence:** "≥80 comparable trade pairs (same entry signal, different overlay state)" — matching rule, time-proximity bound, overlay state classification, and regime confounding treatment all undefined.

**Impact:** (A)(D) Undefined matching in solo-developer context will be operationalized at reporting time — undetectable after the fact. Potential behavioral integrity gap.

---

#### F-17 — Timestamp Convention Leakage Not in Phase 0 Exit Criteria

**Task:** TASK-AF-017 | **Status:** Open (DOCUMENTED — ARCHITECT_BRIEF.md Section F acknowledges as advisory)

**Location:** ARCHITECT_BRIEF.md Section F; PROTOCOL_SPEC.md Phase 0 exit criteria

**Evidence:** ARCHITECT_BRIEF.md: "This should be a checklist item in the Phase 0 leakage audit." Phase 0 exit criteria contain no such item.

**Impact:** (A) A one-bar timestamp misalignment produces entry fills at the wrong price for 100% of trades — structural bias throughout all phases.

---

#### F-18 — GE-2/GE-3 Boundary Not Bright-Line

**Task:** TASK-AF-018 | **Status:** Open | **Confidence:** High

**Location:** PROTOCOL_SPEC.md Sections J1, F

**Evidence:** Zero-weight allocation (functionally = skill removal) could be framed as GE-2 (preregistration-exempt). No rule for this case. GE-2 framing erodes Harvey-Liu trial count, leaving multiplicity correction understated.

**Impact:** (A)(D) Harvey-Liu trial count understatement; behavioral integrity gap.

---

#### F-19 — HWM and Purge/Embargo Absent from GLOSSARY

**Task:** TASK-AF-019 | **Status:** Open | **Confidence:** High

**Location:** GLOSSARY.md; CHARTER.md Section D; ARCHITECT_BRIEF.md Section B

**Evidence:** GLOSSARY.md states all terms used in PROTOCOL_SPEC.md and CHARTER.md are defined. HWM, purge/embargo, walk-forward window parameters are absent.

**Impact:** (D) Implementation ambiguity for HWM reset timing and embargo duration.

---

#### F-20 — K5 Measurement Period Not Specified

**Task:** TASK-AF-020 | **Status:** Open | **Confidence:** High

**Location:** CHARTER.md Phase 5, Kill Criteria Appendix; PROTOCOL_SPEC.md Section F (Phase 5), Section J

**Evidence:** "Any 12-month period" — rolling vs. calendar year vs. fixed windows unspecified.

**Impact:** (B) K5 may fire or not fire for the same data depending on measurement period choice.

---

#### F-21 — P1 Circuit Breaker Verification Criterion Untestable

**Task:** TASK-AF-021 | **Status:** Open | **Confidence:** High

**Location:** CHARTER.md Phase 0 exit criteria; PROTOCOL_SPEC.md Phase 0 exit criteria

**Evidence:** "Tested with synthetic data and verified" — no minimum test suite specified. A single test case satisfies the criterion as written.

**Impact:** (C) Developer self-certifies against an undefined protocol. Undertested P1 may fail in stress scenarios.

---

## Converted Backlog Items

All 21 findings have been converted to `docs/tasks.md` entries:

| Finding ID | Task ID | Severity | Status |
|---|---|---|---|
| F-1 | TASK-AF-001 | P0 | Open |
| F-2 | TASK-AF-002 | P0 | Open |
| F-3 | TASK-AF-003 | P0 | Open |
| F-4 | TASK-AF-004 | P0 | Open |
| F-5 | TASK-AF-005 | P0 | Open |
| F-6 | TASK-AF-006 | P1 | Open |
| F-7 | TASK-AF-007 | P1 | Open |
| F-8 | TASK-AF-008 | P1 | Open |
| F-9 | TASK-AF-009 | P1 | Open |
| F-10 | TASK-AF-010 | P1 | Open |
| F-11 | TASK-AF-011 | P1 | Open |
| F-12 | TASK-AF-012 | P2 | Open |
| F-13 | TASK-AF-013 | P2 | Open |
| F-14 | TASK-AF-014 | P2 | Open |
| F-15 | TASK-AF-015 | P2 | Open |
| F-16 | TASK-AF-016 | P2 | Open |
| F-17 | TASK-AF-017 | P2 | Open |
| F-18 | TASK-AF-018 | P2 | Open |
| F-19 | TASK-AF-019 | P2 | Open |
| F-20 | TASK-AF-020 | P2 | Open |
| F-21 | TASK-AF-021 | P2 | Open |

---

## Missing Evidence / Ambiguous Items

The following items were observed in the source audit but require clarification before closing:

1. **ASSUMPTION: All findings treated as Open.** The source audit status is "Awaiting author responses to Open Questions." No document in the repository acknowledges, mitigates, or closes any finding. This is treated as Open. **If any finding was orally acknowledged or resolved off-document, it must be formally recorded before status can change.**

2. **ASSUMPTION: AUDIT_v1.md is the only completed audit.** No prior audit documents exist in the repository. This report has no predecessor to diff against.

3. **AMBIGUOUS: F-8 impact on Phase 3 decision.** The source audit notes that PROTOCOL_SPEC.md I, Q2 documents this as an open question, meaning the specification acknowledges the unresolved assumption and Phase 3 planning proceeds anyway. The Phase 3 positive-EV claim is presented as tentative ("uncertainty is high at this range") but not retracted. It is recorded here as P1 rather than P0 because Phase 3 is not the current development phase and cannot be gated yet. When Phase 2 exit is being evaluated, this finding must be re-evaluated as P0 if still Open.

4. **AMBIGUOUS: F-5 FLAM BR_long derivation.** "5 skills × 2 timeframes × 12 months ≈ 240" is dimensionally ambiguous (5×2×12=120, not 240). The source audit flags this but does not resolve the correct interpretation. The impact is included in F-5; the derivation itself is not independently verified in this baseline.

---

## Next Actions

1. **Spec Owner:** Review and accept or reject this REVIEW_REPORT (changes status from Draft to Accepted).
2. **Author:** Respond to Open Questions Q1–Q10 from `docs/AUDIT_v1.md`. Each response constitutes a spec addition that must be committed to the appropriate document (not answered informally).
3. **Development:** No Phase 1 activity — no OOS signal testing, no performance evaluation claims — until P0 findings F-1 through F-5 are Mitigated and verified by a partial pipeline re-run (Step 3 + Step 5 minimum).
4. **Governance:** Run the full audit pipeline (Steps 1–6) before the Phase 0 → Phase 1 gate. This baseline (Steps 1–5 missing) is insufficient for a gate decision.

---

## Scope Exclusions

Per `docs/AUDIT_v1.md` "Findings Not In Scope" section, the following were reviewed and explicitly excluded:

- Technology stack choices (Parquet, PostgreSQL, data providers)
- Individual asset selection (top-4 per sector, universe composition)
- Era roadmap feasibility (18-month timeline, solo hours estimates)
- Cost model base rates (commission and fee rates; these are subject to K6 mechanism)
- Leverage (x1 only; no evaluation integrity risk at current scope)
- CCA and InsightHypothesis schema (deferred to Era 4)

---

*Audit Cycle: Phase 0 Baseline | Pipeline: v1.0 | Date: 2026-03-04*
*Source: `docs/AUDIT_v1.md` v1.0 | Status: Draft*
*See also: `docs/tasks.md` (task backlog), `docs/audit/AUDIT_INDEX.md` (artifact registry)*
