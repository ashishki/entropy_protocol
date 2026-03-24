# Entropy Protocol — Glossary

**Version:** 1.2
**Last updated:** 2026-03-04
**Purpose:** Reference definitions for developers and AI models. All terms used in PROTOCOL_SPEC.md and CHARTER.md are defined here.

---

## Core Metrics

**Net Sharpe**
```
Net Sharpe = mean(annual returns, active trading book) / stdev(annual returns, active trading book)
```
Active trading book = streams (a) + (b) + (c) only. Treasury stream (d) excluded.
Annualized using 252 trading days. 4H bars: 6 bars/day.
Always reported with 68% confidence interval using canonical method `CI-SR-ACF-v1` (autocorrelation-consistent). CI is mandatory uncertainty disclosure and does not override frozen kill thresholds.

**Deflated Sharpe (Harvey-Liu)**
Net Sharpe with a haircut applied to account for the number of strategies tested in the trial registry. Mandatory when net Sharpe < 0.40. Reported alongside raw Sharpe in all evaluation outputs.
- Canonical method ID: `HL-HB-v1`.
- Trial-count scope (`M_total`): cross-namespace `Main + AT + RDL-*`, counted at submission time in Trial Registry.

**Calmar Ratio**
```
Calmar = Net Sharpe / Maximum Drawdown
```
Target ≥ 0.25. Flag if < 0.15 for 2 consecutive quarters.

**IC (Information Coefficient)**
Rank correlation between a signal's predictions and subsequent realized returns. Used to estimate strategy edge.
- IC_long: 0.03–0.05 assumed for long-side skills (moderate; not verified until Phase 1)
- IC_short: 0.02–0.03 working prior for equity shorts (conservative; never default to IC_long)
- IC_short > 0.04: treat as suspect; apply 0.015 haircut before reporting

**BR (Breadth)**
Number of independent bets per year.
- BR_long ≈ 240/year (5 skills × 2 timeframes × 12 months, approximate)
- BR_short ≈ 60/year (5 short positions/month × 12 months)

**FLAM (Fundamental Law of Active Management)**
```
IR ≈ IC × sqrt(BR)
```
For marginal contribution of short positions to an existing long portfolio:
```
Delta_IR = IC_short × [sqrt(BR_long + BR_short) - sqrt(BR_long)]
```
With IC_short = 0.025, BR_long = 240, BR_short = 60:
Delta_IR ≈ +0.046 gross. After costs: net delta +0.01–0.05.
Do NOT use the isolated short-only formula for marginal contribution calculations.

**N_eff (Effective Factor Count)**
Effective number of independent risk factors in the portfolio. Computed via dimensionality reduction (DR) + correlation clustering.
- Target: ≥ 3 after controls
- K3 kill criterion timing: after >=3 months DR monitoring precondition, N_eff <= 2 for 2 consecutive monthly checkpoints.

---

## IS / OOS Framework

**IS (In-Sample)**
Data used for model training, calibration, or parameter selection. Any result computed on IS data is NOT a performance claim.

**OOS (Out-of-Sample)**
Chronologically after the last training/calibration window. Strict enforcement:
- Walk-forward test windows do not overlap calibration windows for any parameter
- Regime labels, feature normalization, and portfolio weights use only information available at the start of each test window
- OOS accumulation begins after Phase 0 exit criteria are met

**Walk-Forward Evaluation**
Sequential evaluation where models are trained on a rolling IS window and tested on the subsequent OOS window. The harness advances forward in time; never backward.

**Paper Trading**
Live signal generation on real-time or near-real-time data, no capital at risk. Fills logged at SimBroker-estimated execution prices.
- NOT equivalent to OOS — paper results labeled "Paper" in all reports
- AT paper results labeled "AT-[ID]" — never combined with walk-forward OOS results

**AT (Acceleration Track)**
Hypothesis Acceleration Track. Runs in parallel with Phase 0 only. Paper-only. Results are labeled AT-[hypothesis ID] and cannot substitute for Phase 1 OOS evaluation.

---

## System Components

**SimBroker**
Simulation broker: models transaction fees, borrow costs, crypto perpetual funding, market impact, and slippage. Must be calibrated against real market bid/ask data before Phase 1. Accuracy target: fills within 15% of market data on ≥100 verified fills.

**Skill**
A signal-generating strategy component. Produces raw signal scores; does not determine position sizes.
- Base skill count: 5–6 maximum
- Expansion requires OOS marginal Sharpe contribution > 0.05

**Regime Signal**
A market state classifier. Four layers in the P1–P4 hierarchy (see below). Higher priority always overrides lower.

**Trial Registry**
Log of every strategy specification tested, including parameters, data hash, date, and result. Pre-registration required before any data is examined. Supports Harvey-Liu multiplicity correction.

**CCA (Chief Context Agent)**
Research dashboard only. Aggregates InsightHypothesis objects and narrative context. No live portfolio influence until Era 4 minimum + ≥300 resolved InsightHypothesis objects.

**InsightHypothesis**
A structured hypothesis object in the Insight Layer. Tracks: source, claim, resolution, Brier score. Schema must be locked before ingestion begins (deferred to Era 4).

**Research Portfolio Monitor (RPM)**
A read-only governance dashboard in the Governance Layer. Displays the factual state of the research portfolio by hypothesis family. Has no write access to the Trial Registry. Produces no admissible evidence, no priority rankings, no composite scores, and no recommendations. All RPM outputs are factual state observations of the form "The state of [X] is [Y]." Governed by three permitted signal extensions (ATT, DM, SC) and two additional forbidden output classes (F-6, F-7). Full specification: `docs/governance/research_portfolio_monitor.md`.

**Attention Signal (ATT)**
A permitted RPM output class. Fires when a human-preregistered condition is mechanically satisfied by current registry data. The condition is defined entirely by the human before any session in which it is active. The system evaluates the condition and reports the factual state; it adds no inference, no action prescription, and no severity framing. Both triggered (`[MET]`) and untriggered conditions are always displayed with equal visual weight, in alphabetical order. Forbidden condition fields include composite scores, cross-family comparisons, trend-derived values, and AI-generated assessments.

**Derived Metric (DM)**
A permitted RPM output class. A mechanical transformation of raw registry data that shows all inputs necessary for interpretation. The denominator is always visible — percentages without visible denominators are prohibited (F-7). Cross-family comparisons and composite aggregations are prohibited. Permitted forms: X of Y resolution counts (DM-1), mean resolution time with basis count (DM-2), outcome triplet counts (DM-3), budget headroom as remaining capacity (DM-4), consecutive outcome count as raw integer (DM-5), mean days per submission interval with basis count (DM-6).

**Session Comparison (SC)**
A permitted RPM output class, invoked on manual trigger only. Displays a point-in-time diff between the current registry state and a single human-named, timestamped snapshot. One snapshot is retained at a time; saving a new snapshot overwrites the prior one, preventing time-series construction from accumulated diffs. The delta is a signed integer; both prior and current values are shown. No directional arrows, directional language, or percentage change are permitted. Applies to State (A) and Pace (B) signals only.

---

## Regime Signal Hierarchy (P1–P4)

| Priority | Name | Trigger | Action |
|---|---|---|---|
| P1 | DD circuit breaker | Realized DD from HWM ≥ 12% | Reduce all to 50%; suspend new additions 5 days |
| P2 | Funding exit (crypto perps) | Crypto perp funding > 0.05%/8hr × ≥3 consecutive windows | Exit all crypto short positions |
| P3 | Correlation trigger | 20-day rolling avg pairwise ρ > 0.55 | Reduce gross 35–50% over 3 business days |
| P4 | Weekly regime overlay | 1W signal state (trending / mean-reverting / stress) | Adjust skill routing and allocation targets |

Recovery thresholds (hysteresis):
- P1: HWM gap < 8% AND ≥5 business days
- P2: funding < 0.03%/8hr × ≥5 consecutive windows
- P3: 20-day ρ < 0.45 (not 0.55 — 0.10 hysteresis band)
- P4: updates at weekly close

Deterministic P3 protocol:
- Population: active Phase universe assets with valid returns at decision timestamp.
- Returns: daily close-to-close log returns.
- Estimator: Pearson correlation over 20-day window (minimum 15 valid observations).
- Aggregation: mean of upper-triangle pairwise correlations.
- Mapping: `0.55 < rho_avg <= 0.65` => 35% reduction; `rho_avg > 0.65` => 50% reduction.
- Ramp: linear over 3 business days.

Concurrent transition semantics:
- P1 activation during P3 ramp pauses ramp.
- P1 clear while P3 active resumes paused ramp.
- P4 updates while P1 active are track-only.

---

## Phase Labels

| Phase | Name | Prerequisite |
|---|---|---|
| Phase 0 | Evaluation engine + SimBroker | None — start immediately |
| AT | Hypothesis Acceleration Track | Runs parallel with Phase 0; paper-only |
| Phase 1 | Long-only baseline (4H/1D) | Phase 0 exit criteria met |
| Phase 2 | 1W regime overlay | Phase 1 exit criteria met |
| Phase 3 | Equity shorts, paper first | Phase 2 exit criteria met |
| Phase 4 | Crypto perpetual shorts | Phase 3 exit; base plan = bypassed |
| Phase 5 | Treasury activation | Phase 1 exit + ≥3mo live capital |

---

## Kill Criteria

| ID | Trigger | Action | Active From |
|---|---|---|---|
| K1 | Net OOS Sharpe < 0.28 (point estimate) after 15mo/≥2 regimes | Project kill review | Phase 1 |
| K2 | Infrastructure + LLM costs > 50% simulated monthly gross for 2 consecutive quarters | Cost review; likely kill | Phase 1 |
| K3 | N_eff ≤ 2 after 3+ months DR + correlation clustering | Factor collapse kill | Phase 1 |
| K4 | Short t-statistic < 0.5 after 18mo AND ≥90 short trades | Retire short positions; revert to Phase 2 | Phase 3 |
| K5 | Treasury yield > 60% total return in any 12-month period | Strategic review | Phase 5 |
| K6 | SimBroker short-cost model > 20% deviation for 2 consecutive months | Halt; recalibrate | Phase 3–4 |
| P2K1 | Turnover increases with 1W overlay active | Retire 1W overlay | Phase 2 |
| P2K2 | False-trigger reduction < 10% after 6mo | Retire 1W overlay | Phase 2 |
| P4K1 | Trailing 3-month funding drag > 2.5% NAV annualized | Pause crypto shorts | Phase 4 |
| P4K2 | Combined short Sharpe delta < 0 for 2 consecutive 6-month windows | Retire crypto shorts | Phase 4 |

---

## RDL Governance Terms

**RDL Boundary Matrix**
- Phase 0-1: scaffolding only.
- Phase 2 start: preregistered RDL hypothesis generation + Trial Registry submission + harness evaluation allowed.
- Before Phase 2 exit: portfolio/routing influence prohibited.
- After Phase 2 exit: routing influence only via explicit phase-gated policy path.

**RDL Submission-Time Counting**
`RDL-*` hypotheses are included in Harvey-Liu multiplicity budget at submission time, not promotion time.

**RDL -> RBE Non-Interaction**
RDL outputs must never be used for RBE activation or stop-condition evaluation.

**RDL Dormancy Attestation**
Runtime mode flag `RDL_MODE` must be one of:
- `scaffold_only`
- `eval_enabled`
- `portfolio_disabled`
- `portfolio_enabled`
Pre-Phase-2 certification query `pre_phase2_rdl_portfolio_reads` must return empty.

**RDL Promotion Queue Policy**
- Default ordering: FIFO by Trial Registry submission timestamp.
- Rate limit: max 3 new `RDL-*` promotions/month into active evaluation.
- Shock-control pause: if `M_total` grows by >10 in rolling 30 days, pause new promotions until haircut-impact note is logged.

**Evaluation Epoch ID (Reporting-Only)**
Tag used in K1-K6 reports to preserve comparability across RBE transitions:
`evaluation_epoch_id = {phase_id, rbe_step, policy_hash}`.
This tag does not change frozen kill-window logic or thresholds.

---

## P&L Attribution (Four-Stream — NON-NEGOTIABLE)

| Stream | Content | Included in Net Sharpe? |
|---|---|---|
| (a) Long P&L | Entries and exits from long-side signals | Yes |
| (b) Short P&L | Entries and exits from short-side signals | Yes |
| (c) Borrow/Funding P&L | Equity borrow + crypto perpetual funding costs | Yes |
| (d) Treasury P&L | Yield on idle capital | No (secondary metric only) |

Net Sharpe = f(a + b + c). Stream (d) is reported separately in total portfolio return with explicit labeling.

---

## Cost Model

| Component | Base rate | Notes |
|---|---|---|
| Equity commissions | 0.08%/leg | Per-leg |
| Crypto spot/perp taker fee | 0.05%/leg | Per-leg |
| Equity borrow | 1.5% annualized | Flag if > 5% |
| Crypto perp funding (neutral) | 0.02%/8hr (~22% annual) | Base case |
| Crypto perp funding (trending-bull) | 0.05–0.15%/8hr (55–165% annual) | NOT a tail; routine |
| Market impact | 0.02%/fill | Liquid assets at target sizes |
| Slippage buffer | 0.02%/fill | Additional buffer |

Stop-loss cost model (asset-class specific):
- Equity shorts: hard stop 4–6% from entry; expected 0.5–2 stops/month/position
- Crypto perpetual shorts: hard stop 12–18% from entry OR 3× 5-day realized ATR (wider); expected 1.5–3 stops/month/position

---

## Classification Terms

**Research Lab**
Current state (Era 0–2). Building evaluation infrastructure, validating baseline skills.

**CAF (Capital Allocation Framework)**
Conditional destination (Era 3+). Combines moderate trading alpha with regime-driven risk controls and separately-accounted treasury yield. Viable at net Sharpe 0.28–0.42 + 3–5% treasury yield.

**Niche Alpha Engine**
NOT the target classification. Would require confirmed OOS net Sharpe ≥ 0.50, which the system does not assume or target.

**Regime**
A market state classification produced by the P1–P4 hierarchy. A regime instance requires ≥8 consecutive weeks to count for OOS spanning requirements.
