# Entropy Protocol — Invariant Registry

**Classification:** Confidential — Internal Audit Document  
**Filename:** `docs/audit/INVARIANTS.md`  
**Audit Cycle:** Cycle 1 — Phase 0 (Pre-Development)  
**Pipeline Step:** Step 3 — Invariant Extraction  
**Pipeline Version:** v1.0  
**Date:** 2026-03-04  
**Status:** Draft — Awaiting Spec Owner Acceptance  
**Prior step input acknowledged:** `docs/audit/ARCH_MODEL.md` (2026-03-04, Cycle 1)  
**Full run / Partial run:** Full run: Yes / Partial run: No

---

## Category A — Frozen Non-Negotiables (NN-1..NN-6)

| Invariant ID | Verbatim invariant (spec) | Applies from | Third-party check mechanism | Known audit gap |
|---|---|---|---|---|
| INV-A-01 (NN-1) | Gross leverage <= 1.0 at all times (`|long| + |short| <= 100% NAV`) | Phase 1 runtime onward (policy active immediately) | Recompute gross from position ledger at each timestamp | RS-14 (`INTERACTION_RISK` with RBE) |
| INV-A-02 (NN-2) | Four-stream P&L required; net Sharpe uses streams (a)+(b)+(c) only; (d) excluded | Phase 1+ (reporting policy active immediately) | Validate P&L schema, report templates, and Sharpe numerator inputs | RS-14 |
| INV-A-03 (NN-3) | No signal can be labeled OOS without passing walk-forward harness | Phase 0 onward | Check evaluation labels vs harness run IDs and timestamps | RS-13 (`COVERAGE_GAP` for RDL boundary attestations) |
| INV-A-04 (NN-4) | Sequential rollout only (Phase 1 -> 2 -> 3 -> 4 -> 5); no parallel capital deployment | Phase 0 onward | Verify phase transition approvals and capital-at-risk logs | RS-14 |
| INV-A-05 (NN-5) | Trial preregistration mandatory; Harvey-Liu deflation mandatory when net Sharpe < 0.40 | Phase 0 onward | Confirm prereg IDs before any eval-window reads; verify deflation field present | RS-01/RS-12 (`FORMULA_MISSING`) |
| INV-A-06 (NN-6) | Asset-class-specific stops: equities 4-6%, crypto perps 12-18% or 3x ATR wider | Phase 3 (equity), Phase 4 (crypto) | Validate stop configs and executed stop events by asset class | RS-14 |

Flags:
- `FORMULA_MISSING`: INV-A-05 (deflation formula unspecified).
- `INTERACTION_RISK`: INV-A-01, INV-A-02, INV-A-04 with RBE step changes (RS-15).

---

## Category B — Kill Criteria Invariants

Method note for false-kill / missed-kill: where stochastic model is unspecified in the spec, rates are presented as symbolic expressions and marked `FORMULA_MISSING`.

| Kill ID | Condition / threshold | Measurement period | Active from | Action | Recovery condition | Formula complete? | Open finding |
|---|---|---|---|---|---|---|---|
| INV-B-K1 | Net OOS Sharpe < 0.28 after 15 months and >=2 regimes | 15-month OOS window | Phase 1+ | Project kill review | None specified | Partial | F-2 / TASK-AF-002 |
| INV-B-K2 | Infra+LLM costs > 50% of simulated monthly gross for 2 consecutive quarters | Quarterly, 2 consecutive | Phase 1+ | Cost review; likely kill | None specified | Partial | F-9 context |
| INV-B-K3 | N_eff <= 2 after >=3 months DR monitoring + correlation clustering | Monthly (after 3+ month precondition) | Phase 1+ | Factor-collapse kill / radical reduction | None specified | Partial | F-11 / TASK-AF-011 |
| INV-B-K4 | Short-side t-stat < 0.5 after 18 months and >=90 short trades | 18-month / >=90 trade gate | Phase 3 | Retire shorts; revert to Phase 2 | Re-enter only via phase sequence | Partial | F-6 / TASK-AF-006; F-15 / TASK-AF-015 |
| INV-B-K5 | Treasury yield > 60% of total return in any 12-month period | 12-month period | Phase 5 | Strategic review | None specified | Partial | F-16 / TASK-AF-016 |
| INV-B-K6 | SimBroker short-cost deviation > 20% for 2 consecutive months | Monthly, 2 consecutive | Phase 3-4 | Halt short development; recalibrate | Clear deviation condition post-recalibration (not formalized) | Partial | F-9 / TASK-AF-009 |
| INV-B-P2K1 | Turnover increases with 1W overlay active | 6-month Phase 2 comparison context | Phase 2 | Retire overlay | Return to Phase 1 baseline | Partial | F-14 / TASK-AF-014 |
| INV-B-P2K2 | False-trigger reduction < 10% after 6 months | 6-month Phase 2 window | Phase 2 | Retire overlay | None specified | Partial | F-14 / TASK-AF-014 |
| INV-B-P4K1 | Trailing 3-month crypto funding drag > 2.5% NAV annualized | Rolling trailing 3 months | Phase 4 | Pause crypto shorts | Regime review (threshold for restart not fixed) | Partial | F-19 / TASK-AF-019 |
| INV-B-P4K2 | Combined short-book Sharpe delta < 0 for 2 consecutive 6-month windows | 2 consecutive 6-month windows | Phase 4 | Retire crypto shorts; keep equity shorts per Phase 3 | None specified | Partial | F-20 / TASK-AF-020 |

### Kill-rate derivations (approximate)

1. `INV-B-K1` (numeric scenario from stated CI framework inconsistency):
- Spec states CI ~ +/-0.15-0.20 but review derives SE ~0.914 for T=1.25 years.
- False-kill example (true SR=0.30): `P(SR_hat < 0.28) = Phi((0.28-0.30)/0.914) ~ 49%`.
- Missed-kill example (true SR=0.20): `P(SR_hat >= 0.28) ~ 47%`.
- Both exceed 30% -> `AMBIGUOUS` + `FORMULA_MISSING` on CI methodology.

2. `INV-B-K2` (symbolic due missing noise model):
- Let quarterly observed cost ratio be `R_t` with unknown estimation noise distribution.
- False-kill = `P(R_t>0.5 and R_{t+1}>0.5 | true ratio<=0.5) = p_fp^2` (independence assumption).
- Missed-kill = `1 - p_tp^2`, where `p_tp=P(R_t>0.5 | true ratio>0.5)`.
- Numeric rates not derivable from spec -> `FORMULA_MISSING`.

3. `INV-B-K3` (symbolic):
- Trigger requires estimator `N_eff_hat <= 2` after precondition.
- False-kill = `P(N_eff_hat<=2 for required months | true N_eff>2)` depends on estimator variance and formula choice (equicorrelation vs eigenvalue).
- Missed-kill analogous for true `N_eff<=2`.
- No estimator spec -> `FORMULA_MISSING` + `AMBIGUOUS`.

4. `INV-B-K4` (numeric from charter/review):
- False-kill for marginally positive short edge (IC_short=0.025, n~90) documented ~60%.
- Missed-kill for dead strategy (IC=0): `P(t>0.5)` with df~89 ~31%.
- Both >30% -> threshold is screening, not calibrated statistical test.

5. `INV-B-K5` (symbolic):
- Deterministic ratio threshold with no uncertainty model.
- False/missed rates depend on return attribution estimation noise and window convention (rolling vs calendar ambiguity in docs).
- Numeric rates not derivable -> `FORMULA_MISSING`.

6. `INV-B-K6` (symbolic):
- Depends on deviation estimator `D_t = |model_cost - realized_cost| / realized_cost`.
- False-kill = `P(D_t>0.2 and D_{t+1}>0.2 | true model acceptable)`.
- Missed-kill analogous; no measurement protocol variance specified -> `FORMULA_MISSING`.

7. `INV-B-P2K1` (symbolic):
- Requires turnover comparison statistic and baseline definition.
- Without test rule, false/missed rates cannot be computed numerically.

8. `INV-B-P2K2` (symbolic):
- Requires precise "false-trigger" label definition and counting algorithm.
- Missing -> no numeric false/missed rates.

9. `INV-B-P4K1` (symbolic):
- Requires funding-drag estimator variance and annualization method stability.
- Missing -> no numeric false/missed rates.

10. `INV-B-P4K2` (scenario approximation):
- If each 6-month Sharpe-delta estimate has SE unknown, criterion needs two consecutive negatives.
- With illustrative `P(delta_hat<0 | true delta=+eps)=q`, false-kill=`q^2`; missed-kill=`1-(1-r)^2` where `r=P(delta_hat<0 | true delta<0)`.
- Numeric rates not spec-derivable -> `FORMULA_MISSING`.

Flags:
- `FORMULA_MISSING`: All kill criteria except partial numeric K1/K4 scenarios.
- `AMBIGUOUS`: K1 CI framework; K3 estimator choice; P2K2 event definition; K5 windowing.
- `COVERAGE_GAP`: K6 absent in Phase 1 despite cost-bias risk (F-9).

---

## Category C — Phase Exit Criteria Invariants

| Invariant ID | Phase Gate | Condition | Verifiable by third party? | Open blocker |
|---|---|---|---|---|
| INV-C-01 | 0 -> 1 | WFO harness leakage audit passes (zero forward-looking features under temporal shuffling test) | Yes (if audit logs + test artifacts retained) | None direct |
| INV-C-02 | 0 -> 1 | SimBroker fills within 15% of bid/ask on >=100 verified fills | Yes | F-9 (Phase-1 coverage gap follow-on) |
| INV-C-03 | 0 -> 1 | Trial registry operational; each test run logged (params, hash, date, result) | Yes | F-1 (haircut formula unresolved) |
| INV-C-04 | 0 -> 1 | Data pipeline stable: zero unexplained gaps over >=90 days | Yes | None direct |
| INV-C-05 | 0 -> 1 | P4 produces historically labeled regime series >=3 years over >=15/20 assets | **No (algorithm undefined)** | F-4 / TASK-AF-004 |
| INV-C-06 | 0 -> 1 | P1 circuit breaker logic implemented and synthetic-tested | Partial (test-suite spec not fully enumerated) | F-10 concurrency interaction |
| INV-C-07 | 1 -> 2 | >=15 months OOS and >=2 regimes | Partial (depends on valid P4 labels) | F-4, F-7 |
| INV-C-08 | 1 -> 2 | Net Sharpe point estimate >=0.28 | Partial (CI/statistical calibration issue) | F-2 |
| INV-C-09 | 1 -> 2 | Max DD not breached; SimBroker <=15% drift; HL haircut <0.05; K1/K2/K3 not triggered | Partial (HL formula + N_eff formula unresolved) | F-1, F-11 |
| INV-C-10 | 2 -> 3 | Phase 2 sample/metrics met; rho(4H,1W)<0.60; P2K1/P2K2 not triggered | Partial (P4 model and false-trigger definition incomplete) | F-4, F-14 |
| INV-C-11 | 3 -> 4 | >=12 months short paper, >=90 trades, t-stat>=0.5, delta>=0, borrow drift<20%, gross<=1.0 | Partial (K4 t-stat formula unresolved) | F-6, F-15 |
| INV-C-12 | 4 -> 5 | Not defined as direct gate in spec; Phase 5 prerequisites reference Phase 1 exit + live capital data, not Phase 4 completion | No (gate topology inconsistent) | `COVERAGE_GAP` |
| INV-C-13 | Phase 5 entry prerequisite | Phase 1 exit met + >=3 months live capital with net Sharpe>=0.28 | Partial (live-capital measurement protocol not formalized) | F-16 context |

Phase-0 mandatory specifics covered:
- WFO + leakage: INV-C-01
- SimBroker 15%/100 fills: INV-C-02
- P4 historical labeling: INV-C-05 (`FORMULA_MISSING`)
- P1 circuit-breaker tests: INV-C-06
- Regime hierarchy implementation: implicitly INV-C-05 + Category D invariants

Flags:
- `FORMULA_MISSING`: INV-C-05.
- `COVERAGE_GAP`: INV-C-12 (4->5 gate not explicit in phase chain).
- `INTERACTION_RISK`: INV-C-07 with P4 vintage contamination (F-7).

---

## Category D — Regime Signal Governance Invariants

| Invariant ID | Trigger | Action | Recovery | Precedence/Hysteresis | Flag(s) |
|---|---|---|---|---|---|
| INV-D-P1 | DD from HWM >=12% | Reduce all to 50%; suspend adds 5 business days | HWM gap <8% and >=5 days elapsed | Highest priority (overrides P2-P4) | `AMBIGUOUS` (HWM convention not fully defined) |
| INV-D-P2 | Funding >0.05%/8h for >=3 windows | Exit crypto short positions | Funding <0.03%/8h for >=5 windows | Priority above P3/P4; hysteresis explicit | Formula mostly complete |
| INV-D-P3 | 20-day rolling avg pairwise rho >0.55 | Reduce gross 35-50% over 3 business days | rho <0.45 | Priority above P4; 0.10 hysteresis band | `AMBIGUOUS` (population undefined, reduction-selection undefined; RS-04/RS-18) |
| INV-D-P4 | Weekly regime state (trending/mean-reverting/stress) | Routing/allocation adjustments within budget | Weekly close update | Lowest priority; no recovery lag | `FORMULA_MISSING` (algorithm undefined; RS-03) |
| INV-D-CR-01 | Higher priority always wins | Suppress lower-priority conflicting action | N/A | Global conflict rule | Partial |
| INV-D-CR-02 | No multiplicative stacking of signals | Apply P4 inside reduced book when P3 active | N/A | Global composition rule | Partial |
| INV-D-CR-03 | Label immutability: historical regime labels frozen at evaluation-time version | No retroactive relabeling after recalibration | N/A | Versioning rule | `INTERACTION_RISK` (vintage contamination unresolved, F-7) |

Concurrent-firing undefined behaviors:
- `INV-D-U1` (`AMBIGUOUS`, RS-06): P1 recovers while P3 still active.
- `INV-D-U2` (`AMBIGUOUS`, RS-06): P3 triggers during P1 suspension window.
- `INV-D-U3` (`AMBIGUOUS`, RS-06): P3 reduction ramp interrupted by P1 trigger.
- `INV-D-U4` (`AMBIGUOUS`, RS-06): P4 state change during P1 active hold.

---

## Category E — Metric and Formula Invariants

| Invariant ID | Metric | Spec formula | Inputs / conventions | Implementable? | Flag(s) |
|---|---|---|---|---|---|
| INV-E-01 | Net Sharpe | mean(annual returns active-book)/stdev(annual returns active-book) | Active-book=(a)+(b)+(c); 252-day annualization; 4H=6 bars/day | Partial | `AMBIGUOUS` (`streams a+c` appears in some Phase-1 tables vs NN-2/Glossary include b+c) |
| INV-E-02 | Net Sharpe CI | Stated as +/-0.15-0.20 at 15mo for SR~0.30 | 68% interval required, but no exact CI estimator defined | No | `FORMULA_MISSING`, F-2 |
| INV-E-03 | Harvey-Liu deflated Sharpe | Mandatory when raw<0.40; haircut thresholds (<0.05 flag >0.08) | Trial count visible; AT and RDL counts feed budget | No | `FORMULA_MISSING`, F-1 |
| INV-E-04 | IC_long prior | 0.03-0.05 assumed (unvalidated) | Long-skill prediction vs realized returns | Partial | `AMBIGUOUS` (no suspect threshold, F-5) |
| INV-E-05 | IC_short prior | 0.02-0.03; if >0.04 suspect -> apply 0.015 haircut | Short-skill prediction vs realized returns | Partial | Formula-like rule complete but empirical basis incomplete |
| INV-E-06 | N_eff | In J1: `k / (1 + (k-1)*rho_avg)`; elsewhere described as DR+clustering without fixed estimator | Skill count + average pairwise skill P&L correlation | Partial | `AMBIGUOUS`, F-11 |
| INV-E-07 | FLAM marginal short contribution | `Delta_IR = IC_short * (sqrt(BR_long+BR_short)-sqrt(BR_long))` | IC_short, BR_long, BR_short | Partial | `AMBIGUOUS` (BR_long arithmetic inconsistency and correlation-adjustment gap, F-8) |
| INV-E-08 | K4 t-stat | Threshold provided (<0.5) but exact t-stat computation not specified | Short trade outcomes, n>=90 | No | `FORMULA_MISSING`, F-15 |
| INV-E-09 | P3 rho metric | 20-day rolling average pairwise rho | Return interval and population unspecified | No | `FORMULA_MISSING`, F-3 |
| INV-E-10 | K5 treasury dominance metric | Treasury >60% total return in 12-month period | Windowing and denominator treatment lack full protocol | Partial | `AMBIGUOUS`, F-16 |
| INV-E-11 | Funding drag metric (P4K1) | Trailing 3-month funding drag annualized >2.5% NAV | 8h funding logs, annualization method | Partial | `AMBIGUOUS` |
| INV-E-12 | Sharpe delta metric (P4K2/P2) | Delta vs matched baseline over rolling windows | No explicit SE estimator for window-level deltas | No | `FORMULA_MISSING` |

---

## Category F — Governance and Preregistration Invariants

| Invariant ID | Governance invariant | Status |
|---|---|---|
| INV-F-01 | Trial Registry preregistration required before any evaluation-window data inspection | Active |
| INV-F-02 | GE-1: Sharpe improvements with rising cost drag and turnover must be flagged and decomposed before acceptance | Active |
| INV-F-03 | GE-2: Allocation reweighting for diversification allowed without preregistration only if no signal logic change and gross<=1.0 | Active |
| INV-F-04 | GE-3: Any signal entry/exit/feature/lookback modification requires preregistration | Active |
| INV-F-05 | GE-4: CRR threshold banding and mandatory review triggers | Active |
| INV-F-06 | GE-5: N_eff improvement by allocation permitted; skill proliferation without OOS marginal gain prohibited | Active |
| INV-F-07 | GE-6: Declining CER with stable/rising Sharpe triggers mandatory review | Active |
| INV-F-08 | RDL dormancy invariant: pre-Phase-2 only scaffolding; no signal generation, OOS claims, routing, or RBE interaction | Active |
| INV-F-09 | Growth Layer lock invariant: monitoring-only unless RBE activation is preregistered and charter-reviewed | Active |
| INV-F-10 | RDL trial counting starts at submission (`RDL-*` counted immediately) | Active |
| INV-F-11 | RDL outputs must never feed RBE activation or stop-condition evaluation | Active |
| INV-F-12 | Four-stream P&L separation is permanent; blended returns secondary only | Active |
| INV-F-13 | RBE transition log is permanent; retroactive modification prohibited | Active |
| INV-F-14 | Findings remain draft until Spec Owner acceptance; closure requires formal pipeline confirmation | Active via prompt/pipeline governance |

Flags:
- `AMBIGUOUS`: INV-F-03 boundary at near-zero weights and cluster-cap edge cases (F-18 context).
- `COVERAGE_GAP`: INV-F-08 has no explicit machine-check artifact proving dormancy (RS-13).
- `INTERACTION_RISK`: INV-F-03/04 with RBE Step 1 "efficiency" actions.

---

## Category G — New Module Invariants (v1.1/v1.2)

### Growth Layer invariants

| Invariant ID | Invariant | Flag(s) |
|---|---|---|
| INV-G-GL-01 | Growth Layer locked by default; monitoring-only outputs cannot directly change portfolio decisions | `COVERAGE_GAP` (enforcement artifact unspecified) |
| INV-G-GL-02 | RBE Step >0 requires charter-level review + preregistration before activation | `AMBIGUOUS` ("charter-level review" process undefined) |
| INV-G-GL-03 | Step 4 prohibited during freeze (through 2026-09-02) | Complete |
| INV-G-GL-04 | Step transitions cannot be skipped; rollback automatic on stop triggers; reactivation moratorium applies | Partial (`stop trigger` specificity varies by step) |
| INV-G-GL-05 | RBE Step 1: no risk increase; efficiency expansion only | `INTERACTION_RISK` with GE-2/GE-3 boundary |
| INV-G-GL-06 | RBE Step 2 entry conditions: Sharpe/DD/N_eff/CRR prerequisites + prereg ID | Partial (metric estimation formulas incomplete) |
| INV-G-GL-07 | RBE Step 3 allows max DD target micro-adjustment (20->22) only under strict criteria | `INTERACTION_RISK` with kill criteria comparability |
| INV-G-GL-08 | RBE actions cannot override NN-1 during freeze/current era | Complete |

### RDL invariants

| Invariant ID | Invariant | Flag(s) |
|---|---|---|
| INV-G-RDL-01 | RDL dormant until Phase 2; pre-Phase-2 scope restricted to schema/contracts/datasets/logging | `COVERAGE_GAP` (no explicit compliance attestation mechanism) |
| INV-G-RDL-02 | RDL hypotheses (`RDL-*`) counted in Harvey-Liu budget from submission, not promotion | `INTERACTION_RISK` with undefined HL formula (F-1) |
| INV-G-RDL-03 | RDL outputs cannot influence routing/sizing until Phase 2 exit criteria met | Partial (depends on phase-boundary enforcement) |
| INV-G-RDL-04 | RDL outputs must not feed RBE activation or stop-condition evaluation | Partial (runtime segregation mechanism unspecified) |
| INV-G-RDL-05 | RDL-2 depends on P4 prereg spec; before Phase 2 no OOS label generation | `FORMULA_MISSING` (P4 undefined) |
| INV-G-RDL-06 | RDL-3 feature modifications require new version + new registry entry (GE-3) | Complete |
| INV-G-RDL-07 | RDL-4 event labels pre-Phase-2 are logging-only, no active conditioning | `AMBIGUOUS` (timestamp normalization standard missing) |

---

## Flag Register

- `FORMULA_MISSING`:
  - Harvey-Liu formula and aggregation method (INV-A-05, INV-E-03, INV-G-RDL-02 interaction).
  - P4 algorithm (INV-D-P4, INV-C-05, INV-G-RDL-05).
  - P3 population/metric protocol (INV-D-P3, INV-E-09).
  - K4 t-stat formula exact definition (INV-E-08).
  - CI estimator methodology (INV-E-02).

- `AMBIGUOUS`:
  - K3 estimator choice and K5 windowing.
  - Stream composition wording inconsistencies (`a+c` vs `a+b+c`).
  - GE-2/GE-3 edge boundaries.
  - RBE review authority and operational artifact requirements.

- `COVERAGE_GAP`:
  - No explicit Phase-1 analog to K6 kill action.
  - RDL dormancy and Growth-lock enforcement lack machine-checkable attestation.
  - Direct 4->5 phase gate not explicitly defined though phase dependency skips it.

- `INTERACTION_RISK`:
  - RBE step changes vs frozen NNs and kill-criteria comparability.
  - RDL submission-time trial counting vs undefined HL haircut.
  - Label immutability vs vintage contamination.

---

## Summary Counts

Total invariants extracted: **81**

By category:
- Category A: 6
- Category B: 10
- Category C: 13
- Category D: 11
- Category E: 12
- Category F: 14
- Category G: 15

By flag type (non-exclusive counts):
- `FORMULA_MISSING`: 16
- `AMBIGUOUS`: 19
- `COVERAGE_GAP`: 9
- `INTERACTION_RISK`: 13

Prepared for Step 4 input (`docs/audit/PROMPT_3_DRIFT_GUARD.md`).
