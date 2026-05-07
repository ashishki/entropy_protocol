# Strategic Architecture Review — Second Pass: Stress Test and Correction
**Classification:** Confidential — Internal Strategic Document
**Reviewer:** Staff-Level Quant Architect / Strategic Risk Analyst
**Date:** 2026-03-02
**Version:** 2.0 (Second-Pass Re-Evaluation)
**Basis:** v1.0 findings + Treasury Layer proposal + solo-team constraint re-examination

---

## 1. Executive Delta Summary

### What Has Changed

The first-pass review was structurally sound but contained three specific optimism biases that require correction:

**Bias 1 — Net Sharpe was anchored to the upper literature range.**
The 0.45 base-case net Sharpe cited in v1.0 implicitly assumed above-median signal design quality, competent portfolio construction from Era 2, and disciplined turnover control — simultaneously. For a solo team in a research lab phase, the joint probability of achieving all three is lower than the individual probabilities imply. Revised base case: 0.30–0.40 net Sharpe.

**Bias 2 — Factor collapse controls were presented as more tractable than they are.**
The four controls proposed (exposure budgeting, correlation clustering, DR monitoring, regime gating) are correct in theory but each requires the evaluation engine to already be functioning, the portfolio layer to already be stable, and the team to have bandwidth to maintain them. In solo execution, these controls compete for the same resource pool as primary development. The probability that all four are implemented and maintained correctly from the start is low. The practical mitigation is to start with fewer, simpler controls — not four complex ones.

**Bias 3 — The 18-month timeline implicitly assumed near-full-time solo execution.**
"Solo or small team" covers a wide range. If the primary developer is working on this 20–30 hours per week (common for side-project research labs), Era 2 alone is a 6–9 month undertaking. The timeline was underspecified on this assumption and must be revised.

### What Assumptions Need Revision

| Previous Assumption | Revised Position | Severity |
|---|---|---|
| Net Sharpe base case 0.45 | Revised to 0.30–0.40 | Moderate |
| Factor collapse controls are implementable as described | Revised: pick 2, not 4; implement sequentially | Moderate |
| 18-month profitability probability 30–40% | Revised to 20–30% | Significant |
| Treasury layer not discussed | Now requires explicit position | High |
| Era 1 "done" in 3 months | Realistic only at 40+ hours/week; else 4–6 months | Significant |
| Kill threshold at Sharpe < 0.35 | Revised: consider kill at < 0.30 given revised base case | Moderate |

### What Is Confirmed and Unchanged

The following v1.0 findings are reinforced, not weakened, by second-pass analysis:

- Portfolio layer is the true alpha engine. This is more true than stated in v1.0.
- Evaluation engine must be built first. Still the single most important action.
- Insight layer statistical power is insufficient for Era 1–3. Confirmed.
- The ≤20% DD target is not passive. Regime-triggered deleveraging is mandatory.
- Scope discipline is the survival skill for solo execution. More true than stated.

---

## 2. Re-Assessment of Core Alpha

### Was 0.45 Net Sharpe Realistic or Optimistic?

**It was optimistic under solo execution conditions. Realistic net Sharpe for this system design is 0.25–0.50, with the base case at the lower half of that range.**

The reasons to revise downward from 0.45:

**Reason 1: Post-2018 alpha decay on 4H–1D signals is well-documented.**
Momentum and trend-following signals at daily-and-above frequencies have experienced significant capacity compression in liquid equity and crypto markets. Cross-sectional momentum on a 20-asset universe with fixed top-4-per-sector composition has limited rebalancing degrees of freedom. Gross Sharpe expectations should anchor to 0.5–0.7, not 0.7–1.0.

**Reason 2: Free data sources introduce asymmetric quality risk.**
Professional-grade systems use clean, adjusted, point-in-time data. Free data sources (Yahoo Finance, CoinGecko, etc.) contain: gaps, split-adjustment errors, survivorship bias in historical universe construction, timezone inconsistencies on 4H bars. Each of these introduces a small negative bias to realized OOS metrics versus simulation metrics. Aggregate impact: 0.05–0.15 Sharpe units of unexplained degradation in live conditions.

**Reason 3: Solo development introduces untracked latent costs.**
Feature engineering time is also feature overfitting time. A solo developer iterating on signals without a strict pre-registration discipline will inadvertently perform multiple implicit backtests. Without Harvey-Liu correction applied rigorously, reported Sharpe is overstated by an unknown amount. This is not a criticism of intent — it is a structural property of iterative solo research.

**Reason 4: The 20-asset universe is smaller than it appears.**
"Top 4 per sector" on liquid assets in 2026 means the universe is dominated by mega-cap equities, top-5 crypto by market cap, and a handful of commodities. These assets are the most-analyzed, most-crowded in quantitative strategies globally. The available alpha surface is thinner than it would be in a broader, less-picked universe.

### Pessimistic / Base / Optimistic Scenarios

| Scenario | Conditions | Net Sharpe | Annual Return ($100k) | Max DD (normal) |
|---|---|---|---|---|
| **Pessimistic** | Alpha decay persists; data quality issues; turnover higher than modeled | 0.10–0.25 | 1–4% | 12–18% |
| **Base** | Competent execution; moderate data quality; controlled turnover | 0.28–0.42 | 5–9% | 14–20% |
| **Optimistic** | Regime detection genuinely adds value; portfolio layer well-tuned; insight layer non-negative | 0.50–0.70 | 10–16% | 10–16% |
| **Upside outlier** | All systems functioning; macro regime diversity creates strategy diversification | 0.70–0.90 | 15–22% | 8–14% |

The pessimistic scenario is not a tail case. Given solo execution, free data, and a first-generation system, it is the median outcome for the first 12 months of OOS evaluation. The base case is achievable by month 18–24 with sustained execution discipline.

### Conditions That Improve Sharpe Above 0.7

Sharpe above 0.7 net requires at minimum three of the following to be simultaneously true:

1. **Regime detection is genuinely predictive** (not just lagged momentum confirmation). This requires an ensemble regime signal with demonstrably better-than-random transition detection — a research result, not an assumption.
2. **Effective N of skill factors ≥ 4** (factor collapse successfully controlled). Currently assessed as 50% likely at best.
3. **Portfolio layer rebalancing cost < 1.5% annual turnover cost.** Requires strict turnover budget and active enforcement — not automatic.
4. **Insight layer is at least neutral** (CCA does not introduce correlated noise into portfolio routing). Currently uncertain for Era 1–3.
5. **Data quality is professional-grade or validated as equivalent.** Requires Era 1 SimBroker/data validation work to produce a confirmed result.

The probability that all five are simultaneously achieved by month 18: 10–20%. The probability that at least three are achieved: 40–55%. This is why the optimistic scenario is real but not the central case.

---

## 3. Drawdown Reality Check

### Is 20% DD Structurally Achievable?

**Yes, in normal regimes. No, as a passive property of the system design. It requires active structural enforcement.**

The v1.0 assessment was correct but understated the severity of the structural requirements. Here is the precise argument:

A 20-asset x1 portfolio with 12% annual vol target will produce a 20% DD at approximately:
- 1.67σ drawdown event in normal market conditions → probability ≈ 5% annually (once per 20 years at that magnitude in any single year).
- But 20 correlated assets during a macro stress event (ρ ≈ 0.7) behave as 3–4 effective positions → effective vol rises to ~25% annualized at normal position sizes → the 1.67σ event becomes a 0.8σ event from the portfolio's perspective → frequency ≈ 21% annually.

This means: without regime-triggered deleveraging, the 20% DD target will be breached in approximately 1 in 5 normal calendar years, and in most macro stress years. This is not a rare event risk — it is a recurring structural exposure.

### Structural Changes Required to Enforce ≤20% DD

These are not optional enhancements. They are load-bearing requirements:

**Requirement 1: Dynamic vol target, not static.**
The vol target must respond to realized vol with a lag of no more than 5 trading days. When 10-day realized vol exceeds 1.3× target, position sizes must be cut proportionally. Static vol targets calibrated on historical averages will overshoot in vol expansion regimes.

**Requirement 2: Correlation-triggered deleveraging.**
When the rolling 20-day average pairwise correlation across the portfolio exceeds 0.55, reduce gross exposure by 35–50%. This must be implemented before any capital deployment. A correlation threshold of 0.55 corresponds approximately to "late-trending" or "early-stress" regimes where DD risk accelerates nonlinearly.

**Requirement 3: Hard drawdown circuit breaker.**
At 12% realized DD from equity high-water mark, reduce all positions to 50% of normal size and suspend new position additions for 5 business days. This is not a portfolio optimization decision — it is a survival mechanism. The purpose is to prevent a 12% DD from becoming a 25% DD through continued full-size exposure during a developing adverse regime.

**Requirement 4: Cross-asset stress scenario pre-computation.**
Before any era with capital involvement, run the full portfolio through at least three historical stress analogs: 2020 COVID drawdown, 2022 rate-shock drawdown, and the most recent stress event (whatever that is at time of deployment). If any scenario produces simulated DD > 22%, the position sizing must be reduced until no scenario exceeds 22%. This must be a recurring monthly check.

**Is explicit regime-triggered de-risking mandatory?**

**Yes. Mandatory. Not a feature — a prerequisite for capital deployment.**

A system that targets ≤20% DD without regime-triggered de-risking is claiming to control a risk that its architecture does not actually control. This would be a material misrepresentation of risk properties.

---

## 4. Factor Collapse Re-Evaluation

### Can the Architecture Reduce Factor Redundancy?

**Only modestly, and with significantly more overhead than v1.0 implied.**

Re-examining the proposed controls from v1.0 under solo execution constraints:

- **Exposure budgeting:** Requires PCA factor measurement on rolling windows. Computationally tractable, but requires the evaluation engine to run factor attribution continuously. Not available until Era 2 at earliest.
- **Correlation clustering with 1-per-cluster routing:** Correct in theory. In practice, cluster membership changes across regimes, requiring dynamic re-clustering. This is a non-trivial maintenance burden: the clustering logic itself can overfit to historical correlation structures.
- **Diversification ratio monitoring:** Straightforward to implement. This is the single control worth implementing first.
- **Regime-conditioned exposure limits:** Requires a reliable regime classifier. Which is the open question the entire system is built to answer. This is circular dependency as a control.

**The honest conclusion: factor collapse controls reduce the problem by 30–50%, they do not solve it.** After all controls, expect effective N of independent factors in the range 3–5, not 6–8 as the skill count might suggest.

### Should Skill Count Be Reduced Instead of Expanded?

**Yes. The default skill count should be 6–9, not 12–18.**

The architecture document describes "12–18 skills" as though additional skills are low-cost. They are not. Each additional skill requires:
- Feature engineering and data validation
- Walk-forward calibration and OOS evaluation
- Portfolio layer integration and correlation monitoring
- Ongoing maintenance against data drift

For a solo team, the maintenance cost of each skill is approximately constant per month. Adding a skill that contributes 0.02 additional Sharpe while consuming 5 hours/month of maintenance is net-negative at any reasonable valuation of developer time.

**Recommended restructure:**

| Skill Cluster | Representative Skills | Rationale |
|---|---|---|
| Trend | Time-series momentum, breakout (1 variant each) | Core directional edge; well-documented |
| Reversion | Short-term mean reversion, range-bound oscillator | Orthogonal to trend; necessary for regime diversification |
| Volatility | Vol regime filter, ATR-normalized signal | Controls for vol-clustering; not a return-generating signal alone |
| **Total** | 5–6 base skills | Covers 85–90% of the skill diversity value at 40% of the maintenance cost |

The remaining 6–12 skills in the original design are marginal contributors that increase maintenance overhead and factor collision risk. They should be added one at a time only after OOS evidence confirms marginal Sharpe contribution > 0.05.

---

## 5. Treasury Layer Analysis

### The Proposal

Idle capital allocated to staking, passive yield, or safe lending when the trading system holds no active positions or is deleveraged due to regime conditions.

### Does Treasury Yield Improve Risk-Adjusted Returns?

**Yes, mechanically. The question is whether the improvement is real or cosmetic.**

**The mathematical case:**
On a $100k portfolio at 50% average utilization (reasonable for a stability-first x1 system), approximately $50k is idle in normal conditions. At conservative staking/lending yields of 3–5% APY on that idle capital, this generates $1,500–$2,500 annually — equivalent to 1.5–2.5% additional return on total capital. This is not trivial: it is equivalent to adding 0.06–0.12 Sharpe units to a 12%-vol portfolio.

**The risk structure:**

| Treasury Instrument | Yield Range | Risk Type | Risk Level |
|---|---|---|---|
| Staking (PoS consensus layer) | 3–7% APY | Protocol slashing risk, illiquidity during lock-up | Low–Moderate |
| Stablecoin lending (blue-chip protocols) | 3–8% APY | Smart contract risk, counterparty risk, liquidity | Moderate |
| T-Bill equivalent (on-chain wrapped) | 4–5% APY | Minimal; near risk-free in non-tail scenarios | Low |
| Exchange lending programs | 4–10% APY | Counterparty risk (exchange failure), concentration | High |

For a stability-first system, only T-Bill equivalents and established PoS staking on top-2 networks (ETH, SOL) qualify as appropriate treasury instruments. Higher-yield protocols introduce tail risks that are asymmetrically bad: they are invisible in normal conditions and catastrophic in tail events (see: Terra/Luna, Celsius, FTX historical analogs).

### Does Treasury Yield Mask Weak Alpha?

**Yes. This is the most important risk in the proposal.**

If the trading portfolio produces 2% net annually and the treasury layer produces 4% annually, the combined portfolio reports 6% — which looks acceptable. But the trading system is a net drag on capital at 2% versus a risk-free rate of 4–5%. The correct benchmark comparison is: trading contribution versus opportunity cost of that capital in the treasury layer.

Without explicit separation of:
1. **Trading P&L** (from active signal-driven positions)
2. **Treasury P&L** (from idle capital yield)
3. **Blended reported return**

...the system will systematically obscure the failure of the trading alpha. A portfolio reporting 8% total return where 5% is treasury yield and 3% is trading return is not demonstrating trading edge — it is demonstrating that stablecoin lending exists.

**This risk is not hypothetical. It is the most common failure mode for hybrid yield+trading systems: alpha weakness is hidden until the team stops believing they need to find real alpha.**

### Is Treasury a Capital Efficiency Tool or Strategic Distraction?

**At the current stage (Era 1–3): Strategic distraction. After Era 2 validation: Capital efficiency tool.**

The treasury layer is mechanically sound but architecturally premature. It should not be integrated until the trading system's alpha contribution is independently validated. Introducing treasury yield before that point:

1. Obscures the signal-to-noise ratio of the evaluation engine's outputs.
2. Creates incentive to not fix weak trading alpha (total returns look acceptable).
3. Adds operational complexity (staking lock-up periods, liquidity management for rebalancing) that conflicts with the era roadmap's development priorities.

### Should Treasury Be Introduced Before or After Validated Alpha?

**After validated alpha. Specifically: no earlier than Phase 1 capital deployment (Era 3, month 7–9) and only after the 6-criterion eligibility checklist is cleared.**

**Implementation sequence:**
1. Era 1–2: Trading alpha in simulation only. No treasury.
2. Era 3 micro deployment: Trading-only. Establish a clean baseline. Treasury yield = 0 by design.
3. Era 3–4 (after 3 months of live trading data): Activate treasury on idle capital using only T-Bill equivalents or Tier-1 staking.
4. Permanent accounting rule: trading P&L and treasury P&L reported separately in all performance reports. Never blended in primary metrics.

**The "separate reporting" rule is non-negotiable.** If these P&L streams are blended in any primary metric, the evaluation engine loses its integrity as a judge of trading alpha quality.

---

## 6. Architectural Simplification Pass

### If Forced to Cut 30% of System Complexity

**What to cut:**

1. **Cut the Chief Context Agent from the active portfolio path (preserve as dashboard only).**
The CCA is the highest-complexity, hardest-to-validate component in the architecture. Its failure mode (systematic regime misclassification amplified across all skill routing) is worse than its absence. Removing it from the live portfolio path does not eliminate its value — it converts it from a risk amplifier to a research tool.

2. **Cut 6–9 skills from the initial skill library. Reduce to 5–6 skills maximum at Era 1–2 launch.**
The marginal Sharpe contribution of skills beyond the first 5–6 is small. The marginal maintenance burden is not small. This cut preserves 85–90% of portfolio-layer diversification value at 40% of the signal-layer development cost.

3. **Cut the three-axis source scoring system to a single primary axis for Era 1–3.**
The three-axis system (Predictive Skill, Tradability Skill, Regime Timing Skill) is statistically underpowered at available sample sizes. Building all three axes, with proper calibration, for each source before sufficient data exists is overhead with no return. Implement one axis only: directional accuracy with Brier score. Add axes when sample sizes reach 50+ calls per source.

4. **Cut the Era 5 distillation/collective evolution work from the active roadmap.**
Make it explicit that Era 5 begins only if Era 3 "Done" criteria are met, and treat it as a separate project proposal requiring fresh scoping. Remove it from the current 18-month plan entirely to reduce cognitive overhead.

**What to double down on:**

1. **Double down on the evaluation engine.** The single most leveraged investment in the system. Every hour spent making walk-forward evaluation rigorous, transparent, and leakage-free pays dividends on every subsequent decision. This should receive the largest single allocation of development time in Era 1.

2. **Double down on the portfolio layer.** The v1.0 finding — "portfolio layer is the true alpha engine" — is correct and undersold. The portfolio layer with 5 skills and excellent construction will outperform 15 skills with mediocre construction. Budget disproportionately here.

3. **Double down on the SimBroker cost model.** Underestimated in most systems, disproportionately harmful when wrong. A SimBroker that produces accurate cost estimates is worth more than any individual signal.

**Architecture after 30% complexity reduction:**

```
Data Layer (unchanged — non-negotiable)
Evaluation Engine (upgraded — primary deliverable)
Skill Layer (5–6 base skills only)
Portfolio Layer (upgraded — core alpha engine)
Insight Layer (Era 4, deferred)
CCA (Era 4, dashboard only — no live portfolio influence until Era 4 validated)
Treasury Layer (Era 3+, separately accounted)
```

This reduced architecture can be built, maintained, and rigorously evaluated by a solo developer. The full architecture cannot.

---

## 7. Solo Team Feasibility

### Is 18 Months Realistic?

**18 months to stable profitability: No, for a solo developer at part-time commitment. Possibly, for a solo developer at near-full-time (35–40 hrs/week) with strong pre-existing infrastructure experience.**

The honest assessment broken down by commitment level:

| Commitment Level | Era 1 Duration | Era 2 Duration | First Viable OOS Data | Realistic 18-Month State |
|---|---|---|---|---|
| Full-time (40 hrs/wk) | 2.5–3 months | 3–4 months | Month 7–9 | End of Era 3; early capital deployment possible |
| Part-time (20 hrs/wk) | 4–6 months | 5–8 months | Month 12–15 | Mid-Era 2; no capital deployment justified |
| Side project (10 hrs/wk) | 8–12 months | Never (deferred) | Not achievable | Still in Era 1 evaluation phase |

The first-pass estimate of "25–40% probability in 18 months" was implicitly anchored to a near-full-time execution assumption. If part-time, the same outcomes require 30–36 months.

### Hidden Maintenance Burdens

These are the costs not visible in the Era roadmap but paid continuously:

**Burden 1: Data source maintenance.**
Free APIs change rate limits, response formats, and historical coverage without notice. Yahoo Finance, CoinGecko, and similar sources require active monitoring and repair. Estimate: 2–4 hours/month at steady state, 10–20 hours during a major API change.

**Burden 2: SimBroker calibration drift.**
Market microstructure evolves. A SimBroker calibrated in Era 1 will drift from reality over 12–18 months. Requires quarterly recalibration: 4–8 hours per cycle.

**Burden 3: Walk-forward window management.**
As time passes, the walk-forward harness accumulates new data windows. Skill re-evaluation across growing windows requires increasing computation time. By Era 3, a full walk-forward run may take 4–8 hours. This limits iteration speed and creates incentive to run "quick checks" that cut corners on rigor.

**Burden 4: Schema evolution.**
Every time a feature definition changes, the InsightHypothesis schema gains a field, or the evaluation framework adds a new metric, historical data migration is required. Solo developers routinely underestimate this cost. Estimate: 5–15 hours per schema change; 2–4 schema changes per era.

**Burden 5: The "it was working last week" debugging cycle.**
Stochastic failures in data pipelines, silent numerical errors in OOS calculations, and regime classifier behavioral changes between versions all consume debugging time with no productive output. Estimate: 5–10 hours/month at steady state.

**Total hidden maintenance estimate: 15–40 hours/month at steady state (Era 2+).** For a part-time developer working 80 hours/month, this is 19–50% of available time spent on maintenance rather than forward progress. This is the mechanism by which ambitious systems stall.

### Where Will Complexity Accumulate?

**Three locations where technical debt silently accumulates and eventually halts progress:**

**Location 1: The evaluation engine.**
If walk-forward logic is not perfectly clean from the start, every fix attempt risks introducing new leakage. By Era 3, a patched evaluation engine may be producing unreliable results that the team has normalized. The cost of rebuilding it at that point is enormous.

**Location 2: The regime signal.**
As regime detection is tuned and updated across eras, the historical regime labels applied to past OOS windows will change retroactively. This causes previously reported performance metrics to become inconsistent. A regime signal change in Era 3 invalidates all Era 1–2 performance claims unless the regime labels are frozen at evaluation time and never retroactively updated.

**Location 3: The insight ingestion pipeline.**
As ingestion sources multiply (Twitter, Discord, Telegram, images), the pipeline becomes a high-maintenance surface. Schema mismatches, encoding issues, rate limits, and platform API changes accumulate here faster than in any other component. This is the component most likely to be "almost working" for months without ever being clean.

---

## 8. Revised Probability of Success

### Definitions

"Success" = Net OOS Sharpe ≥ 0.35 over ≥12 consecutive months of forward data, with a SimBroker cost model validated within 15% of live execution costs, and max DD not exceeded in that period.

This is a conservative but meaningful definition. It does not require profitability above a passive baseline — that is a higher bar appropriate for capital deployment, not for project validation.

### Revised Probabilities

**At 12 months:**

| Prior estimate | 15–25% | (implied from v1.0 timeline) |
|---|---|---|
| **Revised estimate** | **10–20%** | |

Rationale for downward revision: By month 12, a solo team at realistic execution pace will have completed Era 1 (evaluation engine, SimBroker) and early Era 2 (portfolio layer with 3–5 skills). They will have approximately 3–6 months of forward OOS data — insufficient to span 2 regimes. The probability of meeting the full "Success" definition at month 12 is low not because the system is failing, but because it hasn't had time to be evaluated rigorously. A 10–20% probability represents the scenario where execution was near-full-time and markets happened to provide regime diversity in a short window.

**At 18 months:**

| Prior estimate | 30–40% | |
|---|---|---|
| **Revised estimate** | **20–32%** | |

Rationale: Revised downward by ~10 percentage points due to (a) revised net Sharpe expectation from 0.45 to 0.30–0.40 base case, (b) explicit accounting for solo maintenance burden reducing forward development velocity, and (c) tighter definition of "success" requiring SimBroker validation. The range 20–32% assumes part-time to full-time execution respectively.

**At 24–30 months:**

| Prior estimate | 50–60% | |
|---|---|---|
| **Revised estimate** | **40–55%** | |

Rationale: The extended timeline significantly helps. By month 24–30, the evaluation engine has sufficient OOS data to span multiple market regimes, the portfolio layer has been through at least one stress test, and maintenance debt is better understood. The downward revision from prior estimate reflects the revised Sharpe base case — a system with a true net Sharpe of 0.30–0.35 is harder to confirm as "successful" when the confidence interval around that estimate is ±0.15 at 24 months.

### Why These Numbers Are Not Simply Pessimistic

The probability of producing valuable research output (regime analysis, signal documentation, influencer scoring infrastructure) even in the "not successful" scenarios is 70–80%. The 20–32% figure is specifically for trading alpha validation, which is the hardest bar. The project is not a binary pass/fail — it is a research trajectory with multiple intermediate deliverables, most of which are achievable.

---

## 9. Kill / Pivot Criteria (Revised)

### Revised Kill Criteria

**Kill K1 (revised): OOS Sharpe threshold lowered.**
Previous: kill if net Sharpe < 0.35 after 12 months.
Revised: kill if net Sharpe < 0.28 after 15 months of walk-forward data spanning ≥2 regimes.
Rationale: 0.28 is two standard errors below the revised base case of 0.35. If results are below 0.28, the system is operating in a regime inconsistent with the theoretical edge framework — not merely underperforming.

**Kill K2 (unchanged): Cost structure dominance.** Monthly infrastructure + LLM costs > 50% of simulated monthly gross return at target AUM in two consecutive quarters.

**Kill K3 (revised): Factor collapse confirmed, effective N ≤ 2 after controls.**
Previous: "after all four controls."
Revised: after the two primary controls (DR monitoring + correlation clustering) are implemented and have been running for ≥3 months.
Rationale: Requiring "all four" controls before calling collapse was too lenient. If the first two controls cannot raise effective N above 2, the system fundamentally lacks diversification surface on this universe.

**Kill K4 (new): Insight layer is net negative after 300 resolved hypotheses.**
If, after 300 resolved InsightHypothesis objects with verified outcomes, CCA-influenced allocation decisions show statistically significant negative contribution (p < 0.10, one-tailed) to portfolio Sharpe versus baseline (no-CCA), the insight layer must be permanently removed from portfolio influence. 300 resolved hypotheses provides 80% power at d = 0.3 effect size.

**Kill K5 (new): Treasury yield is primary return driver.**
If treasury yield accounts for > 60% of total reported portfolio return in any 12-month period during active trading deployment, the trading system has failed to justify its complexity. Evaluate whether a simple treasury-only allocation meets risk/return objectives more efficiently.

### Evidence Required for Justified Continuation

The following are sufficient evidence to continue through a difficult period without triggering a pivot:

1. OOS Sharpe is below target (< 0.35) but improving monotonically across sequential 6-month windows.
2. Factor attribution shows effective N improving across eras (even if currently below target).
3. Regime-conditioned performance shows that at least one regime type produces Sharpe ≥ 0.5.
4. The cause of underperformance is identified, isolated, and has a testable corrective hypothesis.

The key distinction: continuing because of a credible causal theory that is being tested is rational. Continuing because "it will get better eventually" without a testable mechanism is not.

---

## 10. Final Verdict (Revised)

### Classification

**Primary: Research Lab (confirmed)**
**Conditional path to: Capital Allocation Framework (not Niche Alpha Engine)**

This classification represents a meaningful shift from v1.0.

The v1.0 classification "Research Lab → Niche Alpha Engine" implied the primary destination was alpha generation. The revised classification "Research Lab → Capital Allocation Framework" reflects that the system's most probable mature form is a **capital allocation engine** that intelligently combines:
- Moderate trading alpha (Sharpe 0.30–0.45)
- Regime-driven risk controls
- Treasury yield on idle capital
- Systematic hypothesis tracking as qualitative context

This is not a demotion. A Capital Allocation Framework is a legitimate, valuable, and coherent outcome. It is a system that manages capital intelligently across multiple return sources rather than relying on pure quantitative alpha. The distinction matters because it changes what "success" means and what architecture decisions are appropriate.

A Niche Alpha Engine implies the trading signals themselves are the primary value driver and must justify the full system cost. A Capital Allocation Framework allows the system to succeed even if individual signal Sharpe is modest (0.30–0.40) by combining it with regime-aware risk management and treasury efficiency.

**This re-classification also changes the kill criteria:** a Capital Allocation Framework is viable at Sharpe 0.25–0.35 combined with 3–5% treasury yield if the risk controls genuinely enforce the DD target. A Niche Alpha Engine at Sharpe 0.25–0.35 is not viable — it doesn't justify its complexity.

### Probability of Reaching Each Classification

| Classification | 18-Month Probability | 30-Month Probability | Key Dependency |
|---|---|---|---|
| Research Lab (baseline) | 85% | 95% | Solo execution continuity |
| Capital Allocation Framework | 25–35% | 45–58% | Portfolio layer + treasury accounting discipline |
| Niche Alpha Engine | 15–22% | 28–38% | Net Sharpe ≥ 0.50 confirmed OOS |
| Statistically Fragile System | 35–45% | 20–30% | Evaluation rigor determines this; it's a measurement failure risk |

The "Statistically Fragile" classification is not about the system being bad — it is about the system being unverifiable. The largest risk in this project is not that trading alpha doesn't exist but that the evaluation framework isn't rigorous enough to confirm it does or doesn't. Investing in evaluation engine quality is thus simultaneously the best risk mitigation for both the success outcomes and the fragile outcome.

### The Single Structural Correction from v1.0 to v2.0

The most important change in this review is the reclassification of the treasury layer from "not discussed" to "structural component that requires mandatory accounting separation." This single addition changes the viability calculation for the project at the $100k scale.

Without treasury yield: at base-case Sharpe of 0.32 net, the system produces ~$5,500/year gross on $100k. Infrastructure and LLM costs in Era 3–4 run $400–$1,100/month. The system is cost-negative at $100k AUM without external funding.

With treasury yield on idle capital (conservative 3.5% on 50% average idle capital): adds ~$1,750/year. Total: ~$7,250/year. Still below Era 4 cost ceiling but within range.

**The treasury layer, properly accounted and risk-managed, converts the project from economically inviable at $100k to marginally viable — but only if costs are controlled and only if trading P&L is reported separately.**

This is the revised verdict. Not a breakthrough. Not a kill. A recalibration toward realism with a specific structural requirement: build the accounting separation before the first dollar of treasury yield enters the system.

---

*Document Version: 2.0 | Review Date: 2026-03-02 | Supersedes: v1.0 Section findings on Sharpe, factor collapse controls, treasury layer, and classification*
*Next Scheduled Review: End of Era 1 (evaluation engine complete)*
