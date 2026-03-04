# Entropy Protocol — Protocol Specification
**Classification:** Confidential — Internal Strategic Document
**Filename:** `PROTOCOL_SPEC.md` (stable; no version in filename — version tracked in header)
**Role:** Engineering specification: rules, thresholds, phase structure, exit criteria
**Version:** 1.2
**Date:** 2026-03-04
**Basis:** `CHARTER.md` v5.0 (strategic constraints) + v4 audit (authoritative corrections applied)
**Supersedes:** `entropy_protocol_master_spec_v1.md` (archived)
**Freeze period:** 6 months from issue date, or earlier if a kill criterion fires
**v1.1 change summary:** Added Growth Layer module (Section E), Growth Layer & Efficiency Metrics (Section J1), Risk Budget Escalation Protocol (Section J2). Surgical updates to Phase 0, 1, 2 monitoring requirements. Section B (Frozen Non-Negotiables), all kill criteria, all phase exit criteria, and all metric thresholds are unchanged.
**v1.2 change summary:** Added Research Discovery Layer (RDL) module (Section E). RDL is research-only, dormant until Phase 2; before Phase 2 only scaffolding (contracts/datasets/logging) is permitted — no signal generation, no OOS claims, no portfolio routing, no RBE interaction. Section B (Frozen Non-Negotiables), all kill criteria, all phase exit criteria, and all metric thresholds are unchanged.

---

## A. Executive Summary

### Classification

**Current:** Research Lab (Era 0–2)
**Conditional destination:** Capital Allocation Framework (Era 3+)
**Rationale:** Realistic mature form combines moderate trading alpha (net Sharpe 0.28–0.42 base case), regime-driven risk controls, and separately-accounted treasury yield on idle capital. A CAF is viable at this Sharpe level; a Niche Alpha Engine is not — it cannot justify operational complexity at 0.30–0.35 Sharpe.

The "Capital Allocation Framework" label is conditional, not assumed. It requires Phase 1 exit criteria to be met.

### Primary Objective

Build a systematic, multi-asset portfolio intelligence system that:
- Establishes and validates a long-only baseline (Phase 1) before adding any extension
- Enforces ≤20% maximum drawdown through structural rules, not passive design
- Maintains strict four-stream P&L separation throughout all phases
- Generates enough OOS evidence to make a well-powered kill-or-continue decision

### In-Scope Now
- Phase 0: Evaluation engine + SimBroker construction
- Hypothesis Acceleration Track (AT): paper-only, parallel with Phase 0
- Phase 1: Long-only baseline, 4H–1D, ~20 assets, 5–6 base skills

### In-Scope Conditionally (sequence-gated)
- Phase 2: 1W regime overlay (after Phase 1 exit criteria)
- Phase 3: Equity short positions, paper-first (after Phase 2)
- Phase 4: Crypto perpetual shorts (after Phase 3; base plan = bypassed)
- Phase 5: Treasury activation (after Phase 1 exit + 3mo live capital)
- Research Discovery Layer (RDL): scaffolding only in Phase 0–1 (contracts, dataset collection, logging); operational (signal generation, Trial Registry routing) from Phase 2+

### Out of Scope Until Explicitly Unlocked
- CCA as live portfolio influencer (deferred to Era 4 minimum)
- Three-axis source scoring (deferred until ≥50 calls/source)
- Era 5 distillation/collective evolution
- Any capital deployment without Phase 1 exit criteria fully met

### Performance Context (heuristic ranges; not point estimates)

| Scenario | Net Sharpe | Annual return at $100k |
|---|---|---|
| Pessimistic | 0.10–0.25 | 1–4% |
| Base | 0.28–0.42 | 5–9% |
| Optimistic | 0.50–0.70 | 10–16% |

Uncertainty on the 20–32% (18-month CAF probability) estimate is itself ±8–12 pp. These ranges are reference points, not forecasts.

---

## B. Frozen Non-Negotiables (Core)

The following cannot be modified without a full charter-level review and a written justification document. Inline edits to these rules are not permitted.

### NN-1: Gross Leverage ≤ 1.0 (hard rule, not a risk limit)

|long positions| + |short positions| ≤ 100% NAV at all times.

Short positions substitute for long positions. They do not supplement them.
- Example (compliant): 70% long + 30% short = gross 1.0
- Example (prohibited): 80% long + 30% short = gross 1.1

### NN-2: Four-Stream P&L Attribution (permanent)

Every performance report must decompose into exactly four streams. These streams are **never blended** in primary metrics.

| Stream | Content |
|---|---|
| **(a) Long P&L** | Entries and exits from long-side signals |
| **(b) Short P&L** | Entries and exits from short-side signals |
| **(c) Borrow/Funding P&L** | Equity borrow cost + crypto perpetual funding cost (separate from (b)) |
| **(d) Treasury P&L** | Yield on idle capital (permanently separate from trading book) |

**Net Sharpe = streams (a)+(b)+(c) only.** Stream (d) is never included in the primary metric.
Total portfolio return including (d) is a secondary figure, explicitly labeled "blended."

### NN-3: Evaluation Engine First

No signal receives an "OOS" label without passing through the walk-forward harness with proper OOS separation. Phase 0 is a prerequisite, not an enhancement. A partial Phase 0 is not Phase 0.

### NN-4: Sequential Rollout

Long-only baseline (4H/1D) → 1W overlay → equity shorts → crypto perp shorts → treasury.
No phase begins before the prior phase meets documented exit criteria. No parallel capital deployment across phases.

The Acceleration Track runs in parallel with Phase 0 only. It is paper-only and does not bypass phase sequencing.

### NN-5: Trial Registry + Multiplicity Correction

Every signal specification tested must be pre-registered before any data from the evaluation window is examined. Harvey-Liu deflation is mandatory when net Sharpe < 0.40. Deflated Sharpe is reported alongside raw Sharpe. Trial count is visible in the evaluation log at all times.

### NN-6: Asset-Class-Specific Stop-Loss Parameters

| Asset class | Daily vol range | Hard stop | Expected holds/month/position |
|---|---|---|---|
| Equity shorts | 0.8–1.5%/day | 4–6% from entry | 0.5–2 |
| Crypto perpetual shorts | 2–4%/day | 12–18% from entry OR 3× 5-day realized ATR (wider) | 1.5–3 |

A uniform 4% stop on crypto shorts produces 10–15 stop events/month per position — turnover alone eliminates any expected short-side value. These parameters are fixed for the current era. Modifications require a pre-registered stop-loss hypothesis evaluated through the Acceleration Track.

---

## C. Definitions

### "Net Sharpe"
```
Net Sharpe = mean(annual returns, active trading book) / stdev(annual returns, active trading book)
```
- Active trading book = streams (a) + (b) + (c). Stream (d) excluded.
- Costs included: transaction fees, borrow costs, crypto funding costs, stop-loss turnover costs
- Costs excluded: infrastructure costs, LLM/API costs, developer time (tracked separately for K2)
- Annualization: 252 trading days regardless of timeframe; 4H bars use 6 bars/day
- Always include 68% confidence interval. At 15 months OOS, CI ≈ ±0.15–0.20 for a ~0.30-Sharpe system.

### "OOS (Out-of-Sample)"
Chronologically after the last training/calibration window, with strict enforcement:
- Walk-forward test windows do not overlap calibration windows for any parameter
- Regime labels, feature normalization, and portfolio weights computed using only information available at start of each test window
- **AT results are never OOS.** They are labeled "AT-[ID]" and tracked separately.

### "Paper Trading"
Live signal generation on real-time or near-real-time data, no capital at risk, fills logged at SimBroker-estimated execution prices. Always labeled "Paper" — never combined with walk-forward OOS results.

### "Regime"
A market state classification produced by the authoritative signal hierarchy (Section D). A regime instance requires ≥8 consecutive weeks to count toward OOS spanning requirements. Fragments < 8 weeks are excluded from spanning calculations.

### "Net Sharpe Delta (from an extension)"
The improvement in net Sharpe (streams a+b+c) computed on matched observations against a pre-defined baseline. Never computed by comparing different evaluation windows.

### Cost Model Components (explicit)

| Component | Base rate | Stress rate | Notes |
|---|---|---|---|
| Equity commissions | 0.08%/leg | same | Per-leg |
| Crypto spot/perp taker fee | 0.05%/leg | same | Per-leg |
| Equity borrow | 1.5% annualized | flag >5% | Position-size weighted |
| Crypto perp funding (neutral) | 0.02%/8hr (~22% ann.) | — | Base case |
| Crypto perp funding (trending-bull) | 0.05%–0.15%/8hr (55–165% ann.) | — | Not a tail; routine in bull phases |
| Market impact | 0.02%/fill | — | Liquid assets at target sizes |
| Slippage buffer | 0.02%/fill | — | Additional buffer |

---

## D. Regime Signal Governance

Four regime-adjacent signals operate on incompatible time horizons and require explicit conflict resolution. The v2 "single authoritative signal" principle is preserved through strict precedence ordering.

### Precedence Hierarchy (P1 highest, P4 lowest)

| Priority | Signal | Trigger condition | Action | Recovery condition |
|---|---|---|---|---|
| **P1** | Hard DD circuit breaker | Realized DD from HWM ≥ 12% | Reduce all positions to 50%; suspend new additions 5 business days | HWM gap < 8% AND ≥5 days elapsed |
| **P2** | Funding exit (crypto perps only) | Crypto perp funding > 0.05%/8hr for ≥3 consecutive windows | Exit all crypto short positions | Funding < 0.03%/8hr for ≥5 consecutive windows |
| **P3** | Daily correlation trigger | 20-day rolling avg pairwise ρ > 0.55 | Reduce gross exposure 35–50% over 3 business days | 20-day ρ < 0.45 (hysteresis band = 0.10; recovery threshold ≠ trigger threshold) |
| **P4** | Weekly regime overlay | 1W signal state (trending / mean-reverting / stress) | Adjust skill routing and allocation targets within current exposure budget | Weekly close; no recovery period |

### Conflict Resolution Rules

1. Higher-priority signal always wins. P1 active + P4 says "add allocation" → P1 wins; no new additions.
2. Signals do not combine multiplicatively. P3 fires (reduce 35–50%) → P4 routing applies within the reduced book, not against original sizing.
3. Recovery conditions are defined above per signal. A signal does not clear just because the trigger condition is no longer met — the hysteresis window must close.

### Regime Label Immutability

Regime labels applied to historical OOS windows are frozen at evaluation time. A recalibration of the 1W signal in Phase 2 does not retroactively update Phase 1 regime labels. Performance reports reference the signal version active at evaluation time.

---

## E. System Map (Module View)

### Core Modules (always active after Phase 0)

| Module | Purpose | Key inputs | Key outputs | Gating |
|---|---|---|---|---|
| Data Pipeline | OHLCV ingestion, cleaning, Parquet storage | Raw exchange/market feeds | Clean feature store | Phase 0 prerequisite |
| SimBroker | Execution simulation with realistic costs | Order signals, market data | Fill records, cost estimates | Phase 0 exit criterion: within 15% of market bid/ask on ≥100 verified fills |
| Walk-Forward Harness | Leakage-resistant OOS evaluation | Feature store, skill parameters, trial registry | OOS performance records, CI estimates | Phase 0 prerequisite for any OOS claims |
| Trial Registry | Pre-registration log for all specifications | Hypothesis specs (pre-data) | Locked spec records, Harvey-Liu trial count | Active from Phase 0 onward |
| Portfolio Layer | Vol targeting, correlation control, regime routing, weight allocation | Skill signals, regime state (P1–P4), covariance estimates | Position targets | Active from Phase 1 |
| Skills (5–6 base) | Signal generation (trend, reversion, vol-regime) | OHLCV features, asset universe | Raw signal scores | Phase 1 (long-only); extensions gated to Phase 3+ |
| P&L Attribution Engine | Four-stream decomposition on every report | Trade log, cost log | Stream (a)/(b)/(c)/(d) P&L | Active from Phase 1; (b)/(c) active from Phase 3 |

### Pluggable Modules (sequence-gated)

**1W Regime Overlay (Phase 2)**
- Purpose: Reduce false-trigger deleveraging events from P3 correlation trigger; improve regime routing accuracy
- Inputs: Weekly OHLCV, P4 signal specification (pre-registered)
- Outputs: Modified P4 state label (trending / mean-reverting / stress)
- Key risk: Higher IC correlation with 4H/1D signals than expected → N_eff improvement below maintenance justification threshold
- Gating: Phase 1 exit criteria met; empirical ρ(4H,1W) < 0.60 computed; 6-month paper comparison; P2K1/P2K2 not triggered
- Scope constraint: Limited to ≤2 skill instances with 1W-informed sizing; no full third skill tier

**Equity Shorts (Phase 3)**
- Purpose: Substitute short positions for long positions where downward edge is signaled; improve net Sharpe via FLAM breadth addition
- Inputs: Long-side skill signals (repurposed/mirrored for short direction), equity borrow quotes, asset universe
- Outputs: Short-side position targets; streams (b) and (c, equity borrow component)
- Key risk: IC_short < IC_long on liquid assets; turnover from stop-loss events at wider crypto stops is large but bounded; borrow cost model drift
- Expected net Sharpe delta: +0.01–0.05 (corrected FLAM; IC_short = 0.02–0.03 assumed; uncertainty is high at this range)
- Gating: Phase 2 exit; ≥12 months paper / ≥90 trades; t-stat ≥ 0.5; SimBroker borrow within 20%; gross ≤ 1.0 maintained
- **IC_short > 0.04 in walk-forward results → treat as suspect (possible overfitting); apply 0.015 haircut before reporting**

**Crypto Perpetual Shorts (Phase 4)**
- Purpose: Extend short book to crypto perps if funding drag is empirically manageable
- Inputs: Crypto perp OHLCV, funding rate at 8-hour resolution, basis (perp–spot spread)
- Outputs: Crypto short position targets; stream (c, funding drag component)
- Key risk: **Funding drag (2.25% NAV/year at 15% avg annualized funding, 30% short book, 50% in perps) exceeds expected gross benefit (~0.55% additional return) under realistic bull-market funding assumptions. Net EV may be negative.** Base plan = Phase 4 bypassed.
- Gating: Phase 3 exit; Phase 4 entry decision requires explicit funding rate analysis at time of decision; P4K1/P4K2 not triggered

**Exit Overlays (Acceleration Track → Phase 1+ if promoted)**
- Purpose: Test whether rule-based TP levels improve per-trade expectancy vs baseline exit
- Categories: (1) Price-history levels (monthly H/L, weekly H/L, daily H/L) — no optimization; (2) Vol-adjusted (ATR-multiples, VWAP, MA bands); (3) Derived combinations — deferred
- Key risk: Overfitting surface; max 3 overlays in active evaluation simultaneously per quarter
- Gating: Pre-registration in AT; promotion to Phase 1 requires matched baseline paper-trade comparison; Phase 1 baseline computed before overlay result evaluated
- Expected contribution if level effect exists: +0.01–0.05 Sharpe units after multiplicity correction

**Treasury Layer (Phase 5)**
- Purpose: Yield on idle capital (typically 50% avg utilization); mechanically improves total return by ~1.5–2.5% at $100k / 3–5% yield
- Instruments: T-Bill equivalents or Tier-1 PoS staking (ETH, SOL) only. No exchange lending. No high-yield protocols.
- Key risk: Masks weak trading alpha; creates incentive to not fix alpha problems when blended total returns look acceptable; K5 trigger
- Gating: Phase 1 exit criteria met AND ≥3 months live capital data with net Sharpe ≥ 0.28
- Permanent rule: Stream (d) never in primary net Sharpe metric

**Insight Layer / Chief Context Agent (research-only, no live influence)**
- Purpose: Hypothesis generation from text ingestion (Twitter, Discord, Telegram, manual); 3–7 dominant market theses; source scoring via Brier score (1-axis until ≥50 calls/source)
- Key risk: CCA route into live portfolio → systematic regime misclassification amplified across all skill routing (failure mode worse than absence)
- Gating: Era 4 minimum; requires ≥300 resolved InsightHypothesis objects with verified outcomes before any live portfolio influence; currently dashboard/research only

**Research Discovery Layer (RDL) — Dormant Until Phase 2**

- **Status: Research-only. Dormant until Phase 2.** Before Phase 2, only scaffolding is permitted: schema/contract definitions, dataset collection setup, and object logging infrastructure. No signal generation, no OOS claims, no portfolio routing, and no RBE interaction are permitted before Phase 2. This constraint is non-negotiable and is enforced by the audit pipeline (any Phase 0–1 RDL routing or OOS claim is automatically P0).
- **Purpose:** Structured research pipeline for generating, labeling, and feature-engineering candidate hypotheses. Before Phase 2, outputs are scaffolding artifacts (schemas, logged objects) only. After Phase 2 activation, RDL outputs feed the Trial Registry as pre-registered candidates; they do not bypass preregistration or multiplicity controls.
- **Governance:** All RDL hypotheses must be pre-registered in the Trial Registry before any evaluation window data is examined. Namespace: `RDL-*`. RDL hypothesis IDs are counted in the Harvey-Liu trial budget from the moment they are submitted to the Trial Registry — not from the moment they are promoted to Phase evaluation. RDL does not create an exemption from Rule GE-3 (Section J1). Feature modifications generated by RDL submodules are subject to preregistration in full.
- **Gating:** Phase 2 exit criteria met before any RDL output influences portfolio routing, skill signal selection, or exposure sizing.
- **RBE interaction:** RDL outputs must never feed into RBE step activation or stop-condition evaluation. The RBE is governed by realized P&L and structural metrics only (Section J2).

*Submodule RDL-1 — Hypothesis Generator*
- Purpose: Structure candidate hypotheses as `CandidateHypothesis` objects with pre-specified entry condition, metric, threshold, and minimum sample. Output is a pre-registration record ready for Trial Registry submission.
- Inputs: Text ingestion feeds (manual or structured), AT promotion candidates, open questions from external review (Section I).
- Outputs: `CandidateHypothesis` objects. Before Phase 2: objects logged to the scaffolding store only; no evaluation window access permitted.

*Submodule RDL-2 — Market State Labeler*
- Purpose: Produce structured `RegimeTag` objects for defined market states. Supports P4 signal specification development and Phase 2+ regime routing research.
- Inputs: OHLCV feature store; P4 signal pre-registration spec (when defined per F-4 resolution).
- Outputs: `RegimeTag` objects. Before Phase 2: schema validation and logging only; no OOS label generation; no interaction with the walk-forward harness.

*Submodule RDL-3 — Feature Library*
- Purpose: Maintain versioned `FeatureSpec` definitions available for pre-registered hypothesis testing. Each `FeatureSpec` is version-locked at registration time; modifications require a new version with a new Trial Registry entry (GE-3 applies).
- Inputs: OHLCV feature store; feature transformation specs.
- Outputs: `FeatureSpec` definitions. Before Phase 2: schema definition and dataset collection scaffolding only; no evaluation window access.

*Submodule RDL-4 — Event Label Builder*
- Purpose: Generate structured `EventLabel` objects tagging named market events (earnings releases, funding rate spikes, macro announcements) for use in hypothesis conditioning and influencer-derived hypothesis (AT-INF) base rate computation.
- Inputs: Calendar data, funding rate history (8-hour resolution), text event markers.
- Outputs: `EventLabel` objects. Before Phase 2: dataset collection and logging only; no signal conditioning active.

**Growth Layer (Locked by Default)**
- **Status:** Locked. All outputs are monitoring-only. No Growth Layer output influences portfolio decisions or triggers automatic actions until an RBE step is formally activated via charter-level review and preregistration in the trial registry.
- **Purpose:** Monitor execution efficiency, diversification quality, and capital utilization as structural performance levers. Enable the RBE protocol as a gated escalation path after empirical stability is demonstrated.

*Submodule 1 — Cost & Execution Monitor*
- Purpose: Detect slippage drift and cost drag before they accumulate to Sharpe-significant levels.
- Inputs: Fill log (SimBroker and paper), trade log, gross P&L streams (a)+(b)+(c), rolling 30-day window.
- Outputs: Slippage drift indicator (30d rolling deviation from SimBroker estimate); Cost Drag (% NAV/year, annualized); Turnover per skill (round-trips/month); CRR = total friction / gross P&L (rolling 30d).
- Monitoring cadence: Weekly update; monthly report.
- Policy (not tunable): CRR > 0.35 for 2 consecutive months → mandatory cost review before any phase transition is assessed. This is a review trigger, not a kill criterion.
- Tunable: Rolling window length (20–60 days); reporting frequency.

*Submodule 2 — Diversification Controller*
- Purpose: Optimize N_eff as a diversification quality metric via allocation adjustments only. Signal entry/exit modifications are not permitted under this submodule.
- Inputs: Skill P&L streams, rolling pairwise correlation matrix (20-day default), cluster detection output, N_eff estimate.
- Outputs: Cluster membership assignments; allocation cap per correlated cluster; N_eff trend (weekly series).
- Monitoring cadence: Daily correlation update; weekly allocation review.
- Policy (not tunable): N_eff optimization target ≥ 3.0 (aligned with Phase 1 K3 threshold). Maximum gross exposure per correlated cluster = 40% of total gross. Allocation adjustments that increase N_eff without modifying signals are permitted without preregistration, subject to Rule GE-2 (Section J1). Signal modifications require preregistration per Rule GE-3 regardless of stated rationale.
- Tunable: Cluster detection method (hierarchical or k-means); correlation window (15–30 days); cluster cap (35–50%, within documented bounds).

*Submodule 3 — Capital Utilization Monitor*
- Purpose: Track idle capital to inform treasury activation eligibility and identify structural underdeployment.
- Inputs: Daily position log (gross exposure as % NAV), cash balance.
- Outputs: Idle capital % (daily); Average utilization (rolling 90-day); Utilization band compliance flag.
- Monitoring cadence: Daily update; monthly report.
- Policy (not tunable): Target utilization band = 40–70% gross exposure (Phase 1 long-only baseline). Below 40% for ≥30 consecutive days → flag for review. Phase 5 treasury eligibility check uses the 90-day average. Above 70% is constrained by existing position-sizing rules; not a Growth Layer alert condition.
- Tunable: Utilization band thresholds adjustable ±5 percentage points with logged rationale; no preregistration required if adjustment stays within ±5 pp of policy band.

*Submodule 4 — Risk Budget Escalator (RBE)*
- **Status: Locked.** All RBE step activations require charter-level review and preregistration as a policy experiment in the trial registry.
- Purpose: Define and govern a gated, reversible escalation path for risk expansion after structural stability is empirically demonstrated.
- Inputs: Rolling 12-month net Sharpe; rolling 12-month max DD; N_eff trend (Submodule 2); Cost Drag trend (Submodule 1); RBE activation log.
- Outputs: Current RBE step (0–4); activation and rollback event log; preregistration confirmation per step.
- Monitoring cadence: Quarterly RBE step review; continuous stop-condition monitoring when Step 2+ is active.
- Policy (not tunable): Step 0 is always active. Steps cannot be skipped. Rollback is automatic when stop conditions trigger. Step 4 is prohibited during the current freeze period (see Section J2).
- Tunable: None. RBE is fully policy-governed.

---

## F. Main Track Phases (0 → 5)

### Phase 0: Evaluation Engine + SimBroker

**Objective:** Build measurement infrastructure. No signal receives an OOS label before this phase is complete.

**Frozen:** WFO harness architecture, leakage audit checklist, trial registry schema, SimBroker cost model structure
**Can change:** Technology stack choices, data provider (if quality equivalent)

**What NOT to do in this phase:**
- Do not run any signal evaluation and label results "OOS"
- Do not begin paper trading the Acceleration Track until the trial registry is operational
- Do not tune cost model parameters to match a specific desired output
- Do not defer the leakage audit — it must pass before Phase 1 can claim OOS results

**Growth Layer build requirements (Phase 0 addition):**
- Implement Cost & Execution Monitor (Submodule 1) as part of SimBroker instrumentation. The fill log schema must support CRR computation from day one: every fill records estimated slippage, actual slippage, and cost component breakdown.
- Implement Capital Utilization Monitor (Submodule 3) before Phase 1 begins. Target utilization band (40–70%) is established as policy before any Phase 1 trading commences.
- Implement Diversification Controller (Submodule 2) with daily correlation update before Phase 1 begins. N_eff baseline computed over the first 30 days of Phase 1 paper trading.
- These are build requirements verified by the leakage audit. They do not add exit criteria to Phase 0; they add instrumentation requirements that must be operationally confirmed before Phase 1 is declared started.

**Exit criteria (all required):**
- [ ] Walk-forward harness passes leakage audit: zero forward-looking features verified by temporal shuffling test
- [ ] SimBroker fills within 15% of market bid/ask data on ≥100 manually verified fills across representative assets
- [ ] Trial registry operational: every test run logged with parameters, data hash, date, result
- [ ] Data pipeline stable: zero unexplained gaps in target universe over ≥90 continuous days of feed monitoring
- [ ] P4 (weekly regime signal) produces historically labeled regime series covering ≥3 years of 1D data on ≥15 of 20 target assets
- [ ] DD circuit breaker (P1) logic implemented, tested with synthetic data, and verified

**No kill criteria in Phase 0.** If infrastructure cannot be built, Phase 1 does not start.

**Estimated duration:** 8–16 weeks at 20–40 hrs/week

---

### Phase 1: Long-Only Baseline (4H–1D)

**Objective:** Establish a net Sharpe baseline for 5–6 base skills. This is the control benchmark all subsequent phases must beat.

**Frozen:** Skill count (max 6; expansion requires OOS marginal Sharpe contribution > 0.05); evaluation methodology; cost model; trial registry discipline
**Can change:** Individual skill parameters within pre-registered bounds; portfolio construction weights within portfolio layer framework; allocation-based diversification adjustments via Growth Layer Submodule 2 (N_eff optimization without signal modification) do not require preregistration and are permitted. Any modification to signal entry conditions, exit conditions, feature definitions, or look-back parameters — regardless of stated rationale — requires preregistration (Rule GE-3, Section J1).

**What NOT to do in this phase:**
- Do not add skills beyond 6 without demonstrated OOS marginal contribution > 0.05
- Do not begin 1W overlay or short positions
- Do not report AT results as OOS
- Do not optimize regime thresholds (P1–P4) for Sharpe — they are policy parameters, not tunable knobs
- Do not modify signal entry/exit conditions, feature definitions, or look-back parameters under the label of "efficiency improvement" — such modifications require preregistration as AT experiments regardless of framing (Rule GE-3)
- Do not deploy capital

**Required sample:**
- ≥15 months WFO OOS spanning ≥2 distinct regime instances (≥8 weeks each)
- ≥250 completed trades for MAE/MFE analysis

**Metrics and thresholds:**

| Metric | Target | Kill / Flag |
|---|---|---|
| Net Sharpe (streams a+c) | ≥ 0.28 point estimate | K1: < 0.28 after 15mo/2 regimes |
| Calmar ratio | ≥ 0.25 | Flag if < 0.15 for 2 consecutive quarters |
| Maximum DD | < 20% any calendar quarter | Kill if breached |
| Factor N_eff | ≥ 3 after DR + correlation clustering | K3: N_eff ≤ 2 for 2 consecutive months |
| Harvey-Liu deflated Sharpe | Reported alongside raw; haircut < 0.05 | Flag if haircut > 0.08 |
| SimBroker cost accuracy | Within 15% of paper fills | Flag if > 15% for 2 consecutive months |
| CRR (Cost-to-Return Ratio) | < 0.35 (rolling 30d) | Flag if > 0.35 for 1 month; mandatory cost review if > 0.35 for 2 consecutive months |
| CER (Capital Efficiency Ratio) | Reported quarterly; trend tracked | Flag if declining for 2 consecutive quarters with stable or rising Sharpe |
| Capital Utilization % | 40–70% (90d average) | Flag if < 40% for ≥30 consecutive days |
| N_eff trend | Stable or improving (weekly) | Flag if declining ≥ 0.5 units over 60 days without a logged allocation change |

Note: At 15 months OOS, CI on net Sharpe ≈ ±0.15–0.20 (68%). The point estimate is informative, not final.

**Kill criteria:**
- **K1:** Net OOS Sharpe < 0.28 (point estimate) after 15 months spanning ≥2 regimes → project kill review
- **K2:** Infrastructure + LLM costs > 50% of simulated monthly gross return at target AUM for 2 consecutive quarters → cost review; likely kill
- **K3:** N_eff ≤ 2 after 3+ months of DR monitoring + correlation clustering → factor collapse; kill or radical universe reduction

**Pivot criterion (not a kill):** Net Sharpe 0.22–0.28 but improving monotonically across sequential 6-month windows. Continuation requires written causal theory + testable correction hypothesis registered before next evaluation window.

**Phase 1 exit criteria (all required):**
- [ ] 15 months OOS spanning ≥2 regimes completed
- [ ] Net Sharpe point estimate ≥ 0.28
- [ ] Max DD not breached in OOS period
- [ ] SimBroker cost accuracy confirmed within 15%
- [ ] Harvey-Liu haircut < 0.05 Sharpe units
- [ ] K1, K2, K3 not triggered

---

### Phase 2: 1W Regime Overlay

**Objective:** Test whether the 1W regime signal as overlay-only improves net Sharpe vs Phase 1 baseline. Primary hypothesis: reduces false-trigger deleveraging events.

**Frozen:** Phase 1 skill set; Phase 1 cost model; P1–P3 signal hierarchy; four-stream P&L
**Can change:** P4 weekly overlay parameters within pre-registered bounds

**What NOT to do in this phase:**
- Do not build a full third skill tier for 1W
- Do not adjust more than 2 skill instances with 1W-informed sizing
- Do not begin equity shorts
- Do not use uncalibrated ρ(4H,1W) — compute empirically first

**Pre-Phase 2 requirement:** Compute empirical IC correlations across signal types at 4H, 1D, 1W on target universe for ≥3 years. If realized ρ(4H,1W) > 0.65, the N_eff improvement from 1W is below the justification threshold for the maintenance overhead — do not proceed with Phase 2.

**Required sample:**
- ≥6 months paper comparison vs Phase 1 benchmark (same entry signals; parallel baseline and overlay)
- ≥80 comparable trade pairs (same entry signal, different overlay state)
- Note: at 80 pairs, CI on Sharpe delta ≈ ±0.12. Phase 2 screens for plausibility, not confirmation.

**Metrics and thresholds:**

| Metric | Target | Kill / Flag |
|---|---|---|
| Net Sharpe delta (matched comparison) | ≥ 0 (non-negative) | Kill: negative delta |
| False-trigger reduction | ≥ 20% reduction in P3 events reversed within 5 business days | Flag if < 10% |
| Turnover impact | Phase 2 RT/month ≤ Phase 1 RT/month | Kill if turnover increases |
| Empirical ρ(4H,1W) | < 0.60 | Do not advance Phase 2 if > 0.65 |
| CER | ≥ Phase 1 CER baseline | Flag if Phase 2 CER < Phase 1 CER for 2 consecutive months; overlay adds overhead without capital efficiency gain |
| CRR | ≤ Phase 1 CRR baseline | Flag if 1W overlay increases cost-to-return ratio; investigate turnover interaction |

**Kill criteria:**
- **P2K1:** Turnover increases with 1W overlay → retire overlay; return to Phase 1 baseline
- **P2K2:** False-trigger reduction < 10% after 6 months without registered causal explanation → retire overlay

**Phase 2 exit criteria (all required):**
- [ ] 6 months paper comparison; ≥80 matched trade pairs
- [ ] Empirical ρ(4H,1W) computed and < 0.60
- [ ] Net Sharpe delta ≥ 0 in matched comparison
- [ ] Phase 1 exit criteria remain satisfied during Phase 2 period
- [ ] P2K1 and P2K2 not triggered

---

### Phase 3: Equity Shorts (Paper First; Gross ≤ 1)

**Objective:** Test whether equity short positions, substituted for long positions, improve portfolio-level net Sharpe at gross ≤ 1.0.

**Frozen:** gross ≤ 1.0; four-stream P&L; Phase 1–2 baseline as control; equity stop model (4–6%); no crypto shorts in Phase 3
**Can change:** Short signal specifications within pre-registered bounds; short book allocation (0–30% of gross); equity borrow estimates as live market quotes become available

**What NOT to do in this phase:**
- Do not use a 4% stop for crypto assets (Phase 4 only; crypto not in Phase 3)
- Do not use IC_short = IC_long = 0.04 as a default — IC_short = 0.02–0.03 is the working prior
- Do not treat a positive but non-significant t-statistic as confirmation of edge
- Do not begin crypto perp shorts

**Required sample:**
- ≥12 months paper; ≥90 completed short-side trades
- K4 evaluated at 18 months if 90 trades not reached by 12 months
- Note: at 90 trades, IC_short = 0.025 produces expected t ≈ 0.24. K4 is a screening threshold, not a significance test.

**Metrics and thresholds:**

| Metric | Target | Kill / Flag |
|---|---|---|
| Short-side t-statistic | ≥ 0.5 after 18mo/90 trades | K4: < 0.5 → retire shorts |
| Net Sharpe delta (streams a+b+c vs Phase 2 baseline) | ≥ 0 point estimate | Flag if negative 2 consecutive quarters |
| Gross leverage (paper record) | Never > 1.0 | Hard fail if any breach |
| SimBroker borrow cost accuracy | Within 20% of market quotes | K6: > 20% for 2 consecutive months |
| Harvey-Liu haircut (short-side trial count) | All short specs logged | Flag if haircut > 0.08 |

**Kill criteria:**
- **K4 (fixed from v4 audit):** Short-side t-statistic < 0.5 after 18 months AND ≥90 short-side trades → retire short positions; revert to Phase 2. Known limitation: at IC_short = 0.025, P(false kill at t < 0.5) ≈ 60%. Accepted as screening threshold, not statistical test.
- **K6:** SimBroker short-cost model diverges > 20% from paper-fill costs for 2 consecutive months → halt; recalibrate

**Phase 3 exit criteria (all required):**
- [ ] ≥12 months paper; ≥90 completed short-side trades
- [ ] Short-side t-statistic ≥ 0.5
- [ ] Net Sharpe delta ≥ 0 vs Phase 2 baseline
- [ ] SimBroker borrow accuracy < 20% deviation
- [ ] Gross ≤ 1.0 maintained throughout paper record
- [ ] K4 and K6 not triggered

---

### Phase 4: Crypto Perpetual Shorts (Optional — Phase 3 Required)

**Objective:** Test whether crypto perp shorts add portfolio-level net Sharpe, net of funding drag.
**Base planning assumption: Phase 4 is bypassed.** The expected value of crypto perp shorts may be negative in sustained bull markets.

**Key risk (quantified):** At 30% short book, 50% in crypto perps, 15% avg annualized funding (conservative for any bullish crypto period):
```
Funding drag = 0.30 × 0.50 × 15% = 2.25% NAV/year
Expected gross benefit (FLAM, IC=0.025): ~0.55% additional return at 12% portfolio vol
Net expected value: negative under this scenario
```
Phase 4 is only empirically justified if realized funding rates are materially below this base-case.

**Additional risk:** Crypto perp basis risk — perp prices can deviate materially from spot during stress. This P&L variance does not appear in spot OHLCV backtests. Perp-vs-spot basis must be tracked daily.

**Required sample:** ≥12 months paper; ≥60 completed crypto short-side trades; funding cost logged at 8-hour resolution

**Kill criteria:**
- **P4K1:** Trailing 3-month funding drag (stream c, crypto component) > 2.5% NAV annualized → pause crypto shorts
- **P4K2:** Combined short book (equity + crypto) Sharpe delta vs Phase 2 baseline < 0 for 2 consecutive 6-month rolling windows → retire crypto shorts; equity shorts continue per Phase 3 rules
- **K6:** Same 20% deviation threshold as Phase 3

**Phase 4 exit criteria (all required):**
- [ ] ≥12 months paper; ≥60 crypto short trades
- [ ] Net Sharpe delta (vs Phase 3 baseline) ≥ 0, accounting for full funding cost
- [ ] Average realized funding cost ≤ 2.0% NAV annualized over evaluation period
- [ ] Perp-vs-spot basis tracked and < 1.0% persistent deviation
- [ ] K4, K6, P4K1, P4K2 not triggered

---

### Phase 5: Treasury Activation

**Objective:** Activate yield on idle capital after trading alpha is independently validated.

**Prerequisites:** Phase 1 exit criteria met AND ≥3 months live capital data with net Sharpe ≥ 0.28

**Instruments:** T-Bill equivalents or Tier-1 PoS staking (ETH, SOL) only.
Prohibited: exchange lending programs, high-yield protocols, any instrument where tail risk is opaque.

**Permanent rules:**
- Stream (d) never included in primary net Sharpe
- Total portfolio return including stream (d) reported separately, explicitly labeled
- **K5:** Treasury yield > 60% of total return in any 12-month period → strategic review; evaluate treasury-only allocation as alternative

---

## G. Hypothesis Acceleration Track

### Purpose and Strict Separation

The Acceleration Track (AT) exists because Phase 1 requires ≥15 months before actionable OOS results. Paper trading during Phase 0 can generate early signals on scoped hypotheses without contaminating the main evaluation path.

**Critical separation rules:**
- AT results DO NOT substitute for Phase 1 OOS evaluation
- AT results CANNOT be combined with walk-forward OOS data
- AT results are labeled "AT-[ID]" in all reports — never "OOS"
- The AT runs in parallel with Phase 0 only. It is paper-only.

### What Can Be Concluded in 2–3 Months

**Validatable:**
| Question | Min sample | Inference quality |
|---|---|---|
| Does exit overlay at a key level improve per-trade P&L vs baseline? | 40+ matched pairs | Suggestive; CI on mean difference ≈ ±0.3R |
| MAE/MFE distribution per skill type | 60+ trades | Descriptive; informs stop/TP calibration |
| How often does a stop variant trigger? | 40+ stop events | Rate estimate ±15–20 pp |
| SimBroker fill model vs paper fills | Continuous | Bias correction if systematic deviation > 5% |
| Does an influencer setup type have systematic signal? | 40+ instances | Highly provisional; screening only |

**Cannot be concluded in 2–3 months (explicitly stated):**
| Claim | Why not |
|---|---|
| Net Sharpe estimate with tight CI | CI at 3 months ≈ ±0.30–0.50 — statistically inert |
| Multi-regime robustness | 3 months cannot span 2 regime instances by construction |
| Factor independence | Requires longer period and larger cross-section |
| Any kill criterion evaluation | All kill criteria are 12–18 month windows |
| "The system is working" | 3 months of paper results is screening, not validation |

### Decisions That Can Be Made at 2–3 Months

**Can decide:**
- Which exit overlay variants are worth advancing to Phase 1 evaluation (plausibility screen)
- Whether a stop variant fires so frequently it is disqualified by turnover alone
- Whether SimBroker cost model needs recalibration before Phase 1
- Whether an influencer-derived setup has a base rate sufficient for systematic testing
- Which key levels appear in MAE/MFE profiles (informs Phase 1 pre-registration)

**Cannot decide:**
- Whether any skill has positive net Sharpe
- Whether the portfolio is viable
- Whether any kill criterion is met or not
- Whether to deploy capital

### Pre-Registration Protocol (One-Page Spec)

Required fields before any data from the evaluation window is examined:

1. **AT-ID:** Sequential (AT-001, AT-002, ...)
2. **Hypothesis statement:** Specific, falsifiable, testable on paper trades
3. **Entry condition:** Locked; cannot change after registration
4. **Exit condition being tested:** The hypothesis variable
5. **Baseline exit:** The control (must be paper-traded in parallel)
6. **Pre-specified metric:** Computable from trade log
7. **Pre-specified threshold:** What value classifies as "promising" (not "validated")
8. **Minimum sample:** Trades required before evaluation
9. **Expiry:** Evaluation at this date OR sample target, whichever is later
10. **Origin tag:** AT-IND (internal) or AT-INF-[source type] (influencer-derived)

### Influencer-Derived Hypothesis Safeguards

**Safeguard 1: Rule-first, chart-second**
Systematic rule written in precise terms before examining recent price data. "Buy when weekly close > 52-week high" is testable. "Buy when price looks ready to break" is not.

**Safeguard 2: Historical base rate pre-check**
Before registration, compute the historical base rate of the setup condition on target assets over ≥3 years. Prevents testing setups that occurred once in the sample.

**Safeguard 3: 60-day embargo on recent history**
Entry condition must be defined on data older than 60 days relative to registration date. Prevents fitting to the market move that motivated the influencer's post.

**Safeguard 4: Separate tracking**
AT-INF hypotheses tracked separately from AT-IND. If AT-INF promotion rate is systematically higher than AT-IND (adjusted for sample), flag as potential reverse-engineering bias.

### Promotion to Main Track

An AT hypothesis may be promoted to Phase 1 evaluation only if:
1. Pre-registered threshold was met on the pre-specified metric
2. A matching Phase 1 comparison test is pre-registered before any Main Track data for that dimension is examined
3. Harvey-Liu trial count includes all AT hypotheses tested for the same dimension
4. Phase 1 baseline (no-overlay) P&L is computed first, before the overlay result is evaluated

"Promising AT result" ≠ "AT validated" ≠ "deploy." Main Track evaluation is mandatory.

### Exit Overlay Taxonomy (First AT Batch)

**Category 1 (no-optimization):** AT-001 (monthly H/L), AT-002 (weekly H/L), AT-003 (daily H/L)

**Category 2 (vol-adjusted):** ATR-multiples (1×/1.5×/2×), VWAP, MA bands — after Category 1 completes

**Category 3 (derived combinations):** Deferred until Categories 1 and 2 complete

**Hard rules for all exit overlay testing:**
- Max 3 exit overlay hypotheses in active evaluation simultaneously per quarter
- Entry signal version-controlled and locked before any exit overlay hypothesis is registered
- One dimension at a time (level type OR ATR multiple; not both simultaneously)
- Baseline exit paper-traded in parallel for every test
- TP level computed deterministically at entry time; no mid-trade adjustment

---

## H. Known Weak Points and Failure Modes

### 1. Factor Collapse / N_eff Risk
At k=6 skills with average pairwise correlation ρ=0.30: N_eff ≈ 2.4. At ρ=0.50: N_eff ≈ 1.7. Having many skills does not prevent factor collapse. K3 triggers at N_eff ≤ 2 for 2 consecutive months. P(N_eff ≤ 2 despite controls) ≈ 35% (literature-anchored estimate with wide uncertainty). This is a known, unsolved structural risk.

### 2. Cost Model Risk
A 1%/year unmodeled friction on a 12%-vol portfolio reduces net Sharpe by ~0.08 units. This alone can move the system from above-K1 to below-K1. Crypto funding drag in bull markets (routine 0.05%–0.15%/8hr = 55–165% annualized) is not a tail scenario. It is the base case in sustained uptrends, and the system's cost model must treat it as such.

### 3. Solo Execution Maintenance Burden
Estimated steady-state maintenance: 15–40 hrs/month (Phase 1–2); 25–58 hrs/month (Phase 3–4, adding 10–18 hrs for short-side management). At 80 hrs/month total availability (part-time), maintenance can consume 31–73% of available time, directly competing with research and forward development. This is the primary mechanism by which ambitious solo systems stall.

### 4. Multiplicity / Overfitting Surface
Net Sharpe < 0.40 is where Harvey-Liu haircuts are largest — often >50% of the raw estimate. The system operates near this threshold by design. Every untested variant, parameter sweep, or signal modification that is later discarded is an implicit trial that accrues against the multiplicity budget even if not formally logged.

### 5. Paper Success ≠ OOS Validation
AT paper results, 2–3 month paper comparison periods, and short paper-trading windows cannot confirm multi-regime robustness, net Sharpe viability, or any kill criterion (in either direction). The tendency to anchor on early favorable paper results before Phase 1 OOS is complete is a documented failure mode in solo research systems.

### 6. Regime Classifier Circularity
Regime routing is mostly descriptive (current-conditions classification), not predictive. Optimizing regime thresholds on historical data creates a feedback loop: the regime labels affect the portfolio, which affects the performance, which was used to calibrate the threshold. Regime signal parameters (P1–P4 thresholds) must be treated as policy parameters, fixed before evaluation, not tuned for Sharpe.

### 7. Basis Risk in Crypto Perps (Phase 4)
Perpetual contract prices can deviate materially from spot during stress events. This P&L variance does not appear in spot OHLCV backtests. SimBroker must track perp-vs-spot basis daily before any crypto short evaluation is credible.

---

## I. Open Questions for External Review

The following questions are open and appropriate for external review. A definitive answer to any materially affects architecture or phase planning.

1. **IC_short bounds:** What is the empirical range of short-side IC for the top-4-per-sector universe in 4H–1D systematic strategies? Is 0.02–0.03 the right prior, or should it be lower given market microstructure post-2020?

2. **FLAM applicability:** Is the marginal FLAM formula (`IC × [sqrt(BR_long + BR_short) − sqrt(BR_long)]`) appropriate for a system where long and short signals are correlated (derived from the same skill set)? If IC_long and IC_short are correlated, the breadth addition from the short sleeve is overstated.

3. **N_eff under regime-switching:** What is the empirically observed N_eff trajectory for a 20-asset cross-asset portfolio (equities + crypto + commodities) during the 2020–2025 period, using the standard `k / (1 + (k-1)×ρ_avg)` approximation? Does adding the short sleeve genuinely increase N_eff, or are short P&Ls correlated with long P&Ls at the skill level?

4. **Walk-forward window design:** Is 4-year training / 1-year validation / 1-year test / annual roll appropriate for 4H–1D systems, or does autocorrelation in 4H bars require a different purge/embargo structure? What is the minimum embargo length for 4H bars given typical holding periods of 3–15 days?

5. **Regime signal lead time:** Can any observable (breadth, funding rate trend, macro factor) provide >3-day forward warning of a ρ-spike or DD acceleration? If yes, what is the empirical lead time distribution? This would change the P1 circuit-breaker trigger design.

6. **Crypto funding regime forecast:** Is there empirical evidence that crypto perpetual funding rates can be forecast 1–3 days ahead with IC > 0.03? If yes, this changes the Phase 4 EV calculation. If no, the LS-4 exit trigger (reactive, not predictive) is the right design.

7. **1W IC correlation with 4H/1D:** What is the empirical ρ(signal IC at 4H, signal IC at 1W) for trend-following and reversion signal types on the target universe? If this exceeds 0.65, Phase 2 should not proceed.

8. **Exit overlay effect size:** Does the literature support a non-zero exit-level effect for systematic trend-following at 4H–1D timeframes? Or are level-based TPs primarily a feature of discretionary trading where the "community reference" self-fulfillment requires human participants?

9. **K4 power problem:** With expected t-stat ≈ 0.24 at 90 short-side trades (IC=0.025), K4 cannot distinguish a genuinely flat short book from a genuinely marginal positive one. Is there an alternative stopping rule (sequential probability ratio test, Bayesian posterior) that provides better power at this sample size?

10. **Solo feasibility at 25–58 hrs/month:** Has the reviewer seen solo-executed systematic trading systems with comparable complexity achieve Phase 1 exit criteria (15mo OOS) at part-time commitment (≤30 hrs/week)? What are the common failure modes and how long did they typically take to surface?

11. **CCA statistical power:** At what minimum resolved-InsightHypothesis sample size would a Brier-score-based source evaluation have sufficient power (80%) to detect a Sharpe delta of 0.05 from CCA-influenced routing? Is 300 the right number, too low, or too high?

12. **Treasury instruments:** Are there T-Bill equivalent on-chain instruments that genuinely carry near-zero counterparty risk (comparable to direct T-bill ownership), and if so, which current ones meet that bar? This affects whether stream (d) can be modeled as truly risk-free for kill criterion K5.

13. **Data quality on 4H bars from free sources:** What is the empirical bias in OHLCV data from free crypto sources (CoinGecko, Binance public API) vs professional data (Kaiko, CCData) for the 2020–2025 period? Is the 0.05–0.15 Sharpe degradation estimate (v2) consistent with observed discrepancies?

14. **Hysteresis band calibration:** Is the P3 recovery threshold (ρ < 0.45) appropriate for the target universe? The 0.10 hysteresis band was chosen heuristically. What is the empirical distribution of ρ persistence once it crosses 0.55?

15. **Stress analog calibration:** Which historical stress analogs (2020 COVID, 2022 rate shock, 2021 crypto deleveraging) are most relevant for calibrating the Phase 0 stress test requirement? Should the stress analog set be expanded to include cross-asset regime shifts not present in recent history?

---

## J. Kill Criteria Consolidated Reference

| ID | Trigger | Action | Phase |
|---|---|---|---|
| **K1** | Net OOS Sharpe < 0.28 (point estimate) after 15mo spanning ≥2 regimes | Project kill review | Phase 1+ |
| **K2** | Infrastructure + LLM costs > 50% of simulated monthly gross (target AUM) for 2 consecutive quarters | Cost review; likely kill | Phase 1+ |
| **K3** | N_eff ≤ 2 after 3+ months DR monitoring + correlation clustering | Factor collapse; kill or radical universe reduction | Phase 1+ |
| **K4** | Short-side t-statistic < 0.5 after 18mo AND ≥90 short-side trades | Retire shorts; revert to Phase 2 | Phase 3 |
| **K5** | Treasury yield > 60% of total return in any 12-month period | Strategic review; evaluate treasury-only alternative | Phase 5 |
| **K6** | SimBroker short-cost model diverges > 20% from paper-fill costs for 2 consecutive months | Halt short development; recalibrate | Phase 3–4 |
| **P2K1** | Turnover increases with 1W overlay active | Retire overlay; revert to Phase 1 | Phase 2 |
| **P2K2** | False-trigger reduction < 10% after 6mo without registered causal explanation | Retire overlay | Phase 2 |
| **P4K1** | Trailing 3-month funding drag (crypto stream c) > 2.5% NAV annualized | Pause crypto shorts; regime review | Phase 4 |
| **P4K2** | Combined short book Sharpe delta vs Phase 2 baseline < 0 for 2 consecutive 6-month rolling windows | Retire crypto shorts; equity shorts continue per Phase 3 | Phase 4 |

---

## J1. Growth Layer & Efficiency Metrics

### Metric Definitions

| Metric | Definition | Unit | Cadence |
|---|---|---|---|
| **Cost Drag** | Total friction (commissions + slippage + borrow cost + funding cost) / NAV, annualized | % NAV/year | Monthly |
| **Turnover per skill** | Completed round-trips per month per active skill instance | RT/skill/month | Monthly |
| **CRR (Cost-to-Return Ratio)** | Total friction (rolling 30d) / Gross P&L (rolling 30d, streams a+b+c) | Dimensionless | Monthly |
| **CER (Capital Efficiency Ratio)** | Realized net return (streams a+b+c) / Allocated capital (avg gross exposure × NAV, quarterly) | % return / % capital | Quarterly |
| **Capital Utilization %** | Average gross exposure as % NAV over rolling 90 days | % | Monthly |
| **N_eff** | Effective number of independent factors: k / (1 + (k−1) × ρ_avg), where k = active skill count, ρ_avg = mean pairwise skill P&L correlation | Count | Weekly |

### Interpretation Rules

**Rule GE-1: Suspicious Improvement**
A reported Sharpe improvement accompanied by simultaneously rising Cost Drag AND rising Turnover per skill must be flagged before acceptance. The improvement may reflect cost misaccounting rather than alpha. Mandatory action: decompose P&L via four-stream attribution and verify CRR is not deteriorating before attributing the improvement to skill.

**Rule GE-2: Allocation-Based Diversification Permitted Without Preregistration**
Adjustments to allocation weights that improve N_eff are permitted without preregistration, provided:
- Signal entry/exit logic is unchanged for all skills
- Gross leverage remains ≤ 1.0 (NN-1)
- The allocation change is logged with N_eff before/after values and the date

**Rule GE-3: Signal Modification Always Requires Preregistration**
Any modification to signal entry conditions, exit conditions, feature definitions, or look-back parameters — regardless of whether it is framed as a "diversification improvement," "efficiency fix," or "parameter correction" — requires preregistration in the trial registry as a full AT experiment or Phase experiment before any related data is examined. The Growth Layer does not create an exemption from multiplicity controls.

**Rule GE-4: CRR Thresholds**

| CRR Range | Status | Required Action |
|---|---|---|
| < 0.20 | Healthy | No action |
| 0.20–0.35 | Monitor | Review cost model at next monthly report |
| > 0.35 for 1 month | Warning | Cost review mandatory before next phase transition assessment |
| > 0.35 for 2 consecutive months | Flag | Potential K2 input; compare against infrastructure cost threshold; log in RBE transition log |

**Rule GE-5: N_eff as Allocation Optimization Target**
N_eff optimization via allocation rebalancing is allowed and is the primary use case of Submodule 2. N_eff improvement via signal proliferation (adding skills beyond the Phase 1 cap of 6 without OOS marginal Sharpe > 0.05) is prohibited. The distinction is structural: allocation changes the weight of existing signals; signal addition changes the signal set and requires full OOS justification.

**Rule GE-6: CER Trend Interpretation**
CER declining while net Sharpe is stable or rising indicates capital is being increasingly tied up without proportional return. This may reflect rising idle capital, concentration in lower-return allocations, or inefficient position sizing. A declining CER trend for 2 consecutive quarters with stable Sharpe is a mandatory review trigger, not a kill criterion.

---

## J2. Risk Budget Escalation Protocol (RBE — Locked)

### Status and Governance

This protocol is **locked by default**. During the current freeze period (until 2026-09-02), no RBE step transition above Step 0 may occur without charter-level review. All RBE step activations above Step 0 are policy experiments and must be preregistered in the trial registry before activation.

Rollback is automatic and non-negotiable when stop conditions trigger. A rolled-back step cannot be re-activated for a minimum of 3 calendar months from the rollback date, regardless of subsequent metric recovery.

---

### Step 0 — Base Regime (Always Active)

**Definition:** The operating state for all phases without RBE activation. Permanent floor; cannot be exited.

| Parameter | Value |
|---|---|
| Gross leverage | ≤ 1.0 (NN-1; not an RBE parameter) |
| Maximum drawdown target | ≤ 20% |
| Volatility target | As calibrated in Phase 1 baseline |
| Capital utilization target | 40–70% gross (monitored, not enforced by circuit breaker) |

**Entry conditions:** Automatic from Phase 0 onward.
**Monitoring cadence:** Continuous.
**Stop/rollback:** N/A — Step 0 cannot be exited. Extensions via higher steps are additive.
**Documentation required:** None beyond standard P&L reporting.

---

### Step 1 — Efficiency Expansion (No Risk Increase)

**Definition:** Structural improvements that reduce friction or improve diversification quality without increasing gross volatility or position sizing.

**Permitted actions under Step 1:**
- Cost compression: renegotiate execution routes, reduce turnover through better exit timing, consolidate redundant fills
- Diversification optimization: allocation rebalancing via Submodule 2 per Rule GE-2
- Capital utilization improvement: reduce idle capital toward target band (40–70%) without gross exceeding 70%
- Exit refinement: via AT promotion only (pre-registered, matched baseline required)

**Prohibited under Step 1:**
- Any increase in gross volatility target
- Any increase in position sizing beyond current Phase 1 calibration
- Any signal modification without preregistration

**Entry conditions:** Step 0 active; no active kill criteria (K1–K6 and phase-specific kill criteria all clear). Available from Phase 1 onward.
**Monitoring cadence:** Monthly CRR + N_eff review.
**Stop/rollback:** If CRR increases ≥ 0.05 from the pre-activation baseline within 60 days of Step 1 activation → revert Step 1 changes; document failure cause in RBE transition log.
**Documentation required:** Log each efficiency action with before/after CRR and N_eff values. Entry into RBE transition log mandatory.

---

### Step 2 — Volatility Expansion (No Leverage)

**Definition:** Increase portfolio volatility target within the ≤20% DD constraint and ≤1.0 gross leverage constraint, using allocation adjustment only. No new leverage is introduced.

**Entry conditions (all required before preregistration):**
- [ ] Phase 1 exit criteria fully met
- [ ] Rolling 12-month Net Sharpe ≥ 0.35
- [ ] Rolling 12-month Max DD < 12% (significant headroom below 20% ceiling)
- [ ] N_eff ≥ 3.0 for ≥3 consecutive months (stable)
- [ ] CRR < 0.25 for ≥3 consecutive months (cost regime stable)
- [ ] Preregistration in trial registry: step activation logged as policy experiment before any vol target change is made

**Implementation rules:**
- Vol target increase: +1 percentage point per activation increment (e.g., 10% → 11%)
- Minimum evaluation interval between increments: 60 trading days
- Vol target ceiling under Step 2: constrained by DD ≤ 20% hard limit at all realized volatility levels

**Automatic rollback trigger:** Rolling 30-day realized DD accelerates by ≥ 3 percentage points within any single 30-day window → immediately revert vol target to Step 0 baseline.
**Monitoring cadence:** Weekly DD and realized vol measurement; formal evaluation at each 60-day interval.
**Stop/rollback moratorium:** ≥ 3 calendar months from rollback date before re-activation attempt.
**Documentation required:** Pre-activation snapshot of all entry condition metrics; weekly log during active Step 2 period.

---

### Step 3 — DD Constraint Micro-Adjustment (Optional)

**Definition:** A minor upward adjustment to the maximum drawdown policy target (20% → up to 22%). This does not affect NN-1 (leverage) and does not override the P1 hard circuit breaker logic. The P1 trigger (≥ 12% from HWM) is not a function of the DD policy target and is not adjusted here.

**Scope constraint:** Maximum adjustment = +2 percentage points (20% → 22%). Any larger adjustment requires a full charter revision and is outside the scope of this protocol.

**Entry conditions (all required):**
- [ ] Step 2 active and stable for ≥ 6 months
- [ ] Rolling 18-month Net Sharpe ≥ 0.38
- [ ] Zero DD breaches of the 20% target during the entire Step 2 period
- [ ] N_eff ≥ 3.5 for ≥ 6 consecutive months
- [ ] Formal written review document produced, covering: current regime state, cost state, N_eff trend, rationale for adjustment, and explicit rollback conditions
- [ ] Preregistration in trial registry with rollback conditions specified before any adjustment is applied

**Rollback conditions:**
- Realized DD exceeds 20% at any point during Step 3 → immediately rollback to 20% target; 6-month moratorium on Step 3 re-activation
- Rolling 12-month Net Sharpe falls below 0.30 → mandatory review; rollback to 20% target if Sharpe falls below 0.28

**Monitoring cadence:** Weekly.
**Documentation required:** Written review document at activation; weekly log during Step 3 period; formal post-period review report.

---

### Step 4 — Leverage (Future Era Only — Explicitly Prohibited During Freeze)

**Status: NOT PERMITTED during the current freeze period (through 2026-09-02).**

Step 4 exists in this protocol for structural completeness only. Its presence does not constitute approval, intent, or planning authorization. The following constraints are in force until explicitly superseded by a new charter:

- Step 4 cannot override NN-1 (Gross Leverage ≤ 1.0) during the freeze period or current era
- Step 4 requires Era 3 minimum before eligibility review
- Step 4 requires a charter-level written review with a documented risk model for levered operation
- Step 4 cannot be preregistered as a policy experiment during the current era

Any discussion of Step 4 activation must occur at a scheduled charter review. Inline or informal escalation to Step 4 is not permitted.

---

### RBE Transition Log (Permanent Record)

Every RBE step transition — activation or rollback — must be logged immediately with:

1. Date and RBE step before and after transition
2. All entry condition metric values at the moment of activation
3. Trial registry preregistration ID (activation only; not required for automatic rollbacks)
4. Expected monitoring horizon and next evaluation date
5. Rollback trigger conditions (explicitly restated per step rules)
6. Actual trigger condition if a rollback event (with date and metric value)

The RBE transition log is a permanent project record. Retroactive modification is not permitted.

---

## K. Versioning and Freeze Policy

### Freeze Period
This document is frozen for **6 months** from issue date (until 2026-09-02), or until a kill criterion fires (whichever is earlier).

### What "Frozen" Means
- Non-Negotiables (Section B) cannot be modified under any circumstances during the freeze period
- Phase exit criteria, kill criteria, and metric thresholds cannot be adjusted
- New modules cannot be added without charter-level review and written justification
- The kill criterion thresholds and statistical framework cannot be recalibrated to accommodate poor results

**v1.1 controlled evolution note:** The Growth Layer module (Section E), Growth Layer & Efficiency Metrics (Section J1), and Risk Budget Escalation Protocol (Section J2) were added via charter-level review constituting this v1.1 update. These additions are monitoring infrastructure and a locked escalation protocol. They do not modify any Frozen Non-Negotiable, kill criterion, phase exit criterion, or metric threshold. The Growth Layer's internal monitoring thresholds (CRR warning band, utilization band, N_eff target) are tunable within their specified bounds per the module's own policy/tunable classification. They are not freeze-governed parameters.

### Change Control Rules
During the freeze period, permitted changes:
- Technology stack choices within Phase 0 (explicitly listed as changeable)
- Skill parameter values within pre-registered bounds
- Cost model updates based on new market data (logged, not retroactive)
- New AT hypotheses (pre-registered in trial registry)

Changes requiring a charter-level review and written justification:
- Any Non-Negotiable (Section B)
- Kill criterion thresholds
- Phase exit criteria
- Addition of new phases or modules
- Changes to the four-stream P&L definition

After a kill criterion fires: evaluation, not automatic restart. The project may be killed, restructured, or continued with a documented corrective hypothesis.

### Next Scheduled Review
End of Phase 0 (evaluation engine and SimBroker complete).

---

## L. Next Actions (1–2 Weeks)

### Phase 0 Track
- [ ] Finalize walk-forward harness architecture (training/validation/test window lengths, roll frequency, purge/embargo design)
- [ ] Define trial registry schema (fields, version locking, hash computation method)
- [ ] Define leakage audit checklist: enumerate all potential forward-looking features; design temporal shuffling test procedure
- [ ] Select data provider(s) for target universe; document quality assessment criteria
- [ ] Begin SimBroker cost model implementation using cost table in Section C

### Acceleration Track
- [ ] Register AT-001 (Monthly H/L TP hypothesis) in trial registry — one-page spec, all 10 required fields
- [ ] Register AT-002 (Weekly H/L TP hypothesis)
- [ ] Register AT-003 (ATR-multiple TP hypothesis, 1× baseline)
- [ ] Define baseline exit condition to be paper-traded in parallel with all Category 1 overlays
- [ ] Confirm that trial registry is operational before any paper trading begins

### External Review Preparation
- [ ] Share this document with intended reviewers (trader, CTO); share accompanying targeted documents
- [ ] Collect answers to open questions in Section I; log as tagged notes in project docs
- [ ] Schedule a structured review session focused on Sections H (weak points) and I (open questions)

---

*Document Version: 1.2 | Base: 2026-03-02 | v1.1 update: 2026-03-02 | v1.2 update: 2026-03-04*
*Supersedes: Strategic Architecture Review v2, v3, v4; Strategic Charter v5 (all replaced by this document as reader entry point)*
*Classification: Confidential — Internal Strategic Document*
*Freeze expires: 2026-09-02 or at first kill criterion event*
*v1.1 additions: Growth Layer (E), Growth Metrics (J1), RBE Protocol (J2), Phase 0/1/2 monitoring updates. Section B unchanged.*
