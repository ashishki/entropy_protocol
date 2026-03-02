# Strategic Architecture Review v3 — Evolution Pass: 1W Timeframe + Short Positions
**Classification:** Confidential — Internal Strategic Document
**Reviewer:** Staff-Level Quant Architect / Spec Owner
**Date:** 2026-03-02
**Version:** 3.0 (Minor Evolution Pass)
**Basis:** v2.0 findings + deep-research-report.md + proposed scope extensions
**Scope:** Timeframe extension to 1W; short positions at x1 gross leverage only

---

**Governing Constraints Extracted from deep-research-report.md and v2.0**

Before any section, the following are binding:

- **Net Sharpe base case:** 0.28–0.42. Literature anchor: gross 0.35–0.70, net 0.15–0.45, median ~0.30–0.35.
- **Factor collapse:** Effective N ≈ 3–5 after controls. P(N_eff ≤ 2 despite controls) ≈ 35%.
- **DD enforcement:** ≤20% DD requires four structural rules — dynamic vol target, correlation-triggered deleveraging at ρ > 0.55, hard 12% DD circuit breaker, stress analog calibration. None are optional.
- **Treasury accounting:** Trading P&L and treasury P&L permanently separate. Treasury activates no earlier than Era 3 Phase 1. Only Tier-1 instruments.
- **Kill threshold:** Net OOS Sharpe < 0.28 after 15 months spanning ≥2 regimes.
- **Classification:** Capital Allocation Framework. Probability: ~55% at 30 months.
- **Skill count:** 5–6 base skills maximum. Expansion only on demonstrated marginal OOS contribution > 0.05 Sharpe.
- **Multiplicity correction:** Mandatory at net Sharpe < 0.40. Deflated Sharpe / Harvey-Liu haircut apply. Trial count must be logged.

**Gross leverage interpretation (disambiguated):**
The constraint "x1, no margin amplification" is interpreted as **gross leverage ≤ 1.0**:
|long positions| + |short positions| ≤ 100% of NAV.
This means short positions substitute for long positions, not supplement them.
A 30% short allocation reduces maximum long allocation to 70%.
This constraint is load-bearing for all analysis below.

---

## Section A — Validation of V2 Baseline

### A1. V2 Classification Restated

The v2 document classifies this system as a **Research Lab** in current state, with a conditional path to a **Capital Allocation Framework** as its most probable mature form — not a Niche Alpha Engine. The distinction is substantive: a Capital Allocation Framework is viable at net Sharpe 0.30–0.40 when combined with regime-aware risk controls and separately-accounted treasury yield. A Niche Alpha Engine requires net Sharpe ≥ 0.50 to justify its complexity overhead. The deep research report confirms this classification at ~55% probability for Capital Allocation Framework versus ~30% for Niche Alpha Engine.

### A2. Is Capital Allocation Framework Still the Most Probable Mature State?

**Yes, and it is reinforced by the proposed extensions.**

Adding 1W signals and short positions increases the system's architectural coherence as an allocation engine rather than a pure signal engine. Both extensions expand the portfolio layer's decision space (regime routing via slower signals; directional flexibility via shorts) without fundamentally increasing signal alpha potential. The extensions strengthen the portfolio layer's risk management capability more than they strengthen raw return generation. This is the definition of a Capital Allocation Framework, not a Niche Alpha Engine.

The probability that the extensions push the system into Niche Alpha Engine territory is low: ~5–10%. The extensions do not materially expand the gross alpha surface. They redistribute existing alpha more efficiently across market states.

### A3. Sharpe Re-Evaluation Under 1W + Long/Short Symmetry

**Base case net Sharpe revised to 0.30–0.45 from 0.28–0.42.**

The revision is modest and directional, not transformative. The mechanisms:

- 1W signals reduce turnover. At 4H–1D, estimated 1–2 round trips/asset/month; at 1W-included systems, estimated 0.7–1.4 round trips/asset/month. Cost drag reduces by approximately 0.03–0.08 Sharpe units. This is the primary quantifiable benefit.
- Long/short at x1 gross removes the long-only constraint premium: unconstrained mean-variance portfolios theoretically dominate long-only under the same signal quality. Clarke et al. document +15–30% Sharpe improvement from removing the long-only constraint in well-calibrated systems. Applied to a base of 0.35: this implies +0.05–0.10 Sharpe delta under favorable conditions.
- Offset: short-side implementation costs (borrow costs, potential funding rates on crypto perpetuals) add 0.5–2.0% annual drag on short positions. At a 25–35% average short allocation, effective drag is 0.1–0.7% of total portfolio — reducing the cost benefit by approximately 0.01–0.06 Sharpe units.

Net expected Sharpe delta from both extensions combined: +0.04 to +0.10 Sharpe.

**Revised scenario table:**

| Scenario | Conditions | Net Sharpe | Annual Return ($100k) |
|---|---|---|---|
| Pessimistic | Alpha decay; data quality issues; short-side costs materialize | 0.12–0.28 | 1–4% |
| Base | Competent execution; moderate cost control; 1W regime overlay working | 0.30–0.45 | 5–10% |
| Optimistic | Portfolio layer functioning; short signals additive; regime routing effective | 0.50–0.72 | 10–18% |

The pessimistic floor is unchanged from v2. The optimistic ceiling rises by ~0.02–0.05 due to directional symmetry. The base case shifts upward by ~0.03.

### A4. Does 1W Meaningfully Expand the Alpha Surface?

**Marginally. Not materially.**

The weekly timeframe captures a regime of intermediate-term price dynamics that is not fully represented in 4H or 1D signals. Specifically:
- Weekly momentum (12–52 week lookback range, Moskowitz et al. framework) has different IC structure than daily. It is more autocorrelated and slower to decay.
- Weekly mean-reversion signals operate at a different amplitude than daily — they capture multi-week overshoots, not daily noise.

However, the incremental alpha from 1W signals, after accounting for their high correlation with 1D signals (ρ ≈ 0.45–0.65 for trend signals across adjacent timeframes), is limited. The marginal contribution is:
- **Additional signal diversity:** real but partial. Cross-timeframe correlation of ~0.5 implies approximately 0.33 additional effective bets per incremental timeframe added (not 1.0).
- **Regime detection improvement:** more substantial. Weekly regime signals are meaningfully more stable than daily. This is where 1W earns its keep.

**Classification of 1W contribution:** 70% regime overlay value, 30% incremental signal alpha. This has direct architectural implications (see Section B).

### A5. Does Shorting Increase or Decrease Factor Collapse Risk?

**Decreases it, modestly. Not substantially.**

In a long-only system, all strategies share a common constraint: they can only express negative views by reducing exposure to zero. They cannot profit from assets that decline. This creates a structural bias: all long-only strategies load positively on broad market beta, and in bearish regimes, their diversity collapses because they all go to cash simultaneously.

Short positions eliminate this structural bias. A strategy that shorts falling assets in a bearish regime produces positive returns when all long-only strategies are at zero or small loss. This is a genuinely orthogonal return stream in regime-conditioned analysis.

**However**, the orthogonality is not as large as it appears because:
1. Gross leverage cap (≤1) means shorts come at the cost of longs. A portfolio that is 30% short in a bear regime is necessarily only 70% long — it is partially already in the long-only "go to reduced exposure" mode.
2. In a universe of 20 liquid assets, short signals tend to cluster on the same assets (weakest assets in bearish regimes). Correlated shorts reduce effective N of short-side positions.
3. Short squeezes (especially in crypto) create positively correlated losses across short positions during covering events — the opposite of diversification.

**Quantified factor collapse impact:** P(N_eff ≤ 2 despite controls) revised from 35% to 25–30%. This is directionally positive but not transformative. The system with long/short remains at risk of effective N collapse during macro stress events, where both long and short sides can experience correlated errors (longs fall, shorts get squeezed, simultaneously).

---

## Section B — Timeframe Extension (4H–1D–1W)

### B1. Statistical Implications of Adding Weekly Timeframe

**Signal stability:** Higher on 1W than 1D. Weekly bars average out 5 days of microstructure noise. False breakout rate lower. Signal half-life longer. IC (information coefficient) per bar lower, but IC per unit of information higher. For trend signals: weekly is more robust but slower.

**Turnover impact:** Significant and positive. A system where 1W signals gate or weight the 4H/1D allocations rather than run independently reduces gross turnover by an estimated 25–40%. At an estimated round-trip cost of 0.20–0.40%, a 30% turnover reduction saves approximately 0.05–0.08 Sharpe units. This is the single largest quantifiable benefit of 1W integration.

**Correlation across timeframes:** 4H–1D–1W signals for the same strategy class (e.g., trend following) are correlated at approximately:
- ρ(4H, 1D): 0.55–0.75 (high; both capture short-term momentum)
- ρ(1D, 1W): 0.40–0.65 (moderate; weekly captures intermediate-term dynamics)
- ρ(4H, 1W): 0.25–0.50 (lower; greatest time-scale separation)

None of these correlations are zero. The three timeframes do not constitute three independent signal layers.

### B2. Does 1W Meaningfully Increase Effective N?

**Yes, but by less than one full effective bet.**

Using the standard effective-N formula with k=3 timeframes and average pairwise ρ ≈ 0.50: N_eff ≈ 3 / (1 + 2×0.50) = 1.5. This is almost no increase over 2 timeframes (which gives ≈ 1.33). The N_eff increase from adding 1W to (4H, 1D) is approximately 0.1–0.3 effective bets — small.

This calculation applies to signal-level N_eff. At the strategy level (combining signal + portfolio construction), the benefit of 1W is primarily through the portfolio layer (regime routing stability) rather than signal diversity.

### B3. Is 1W Additive Alpha or Redundant Smoothing?

**Primarily redundant smoothing with genuine regime-routing value.**

For signal alpha: 1W is largely a smoothed version of the 1D signal with longer decay. It adds ~30% genuinely new alpha surface (regime-specific intermediate-term dynamics). It is ~70% correlated noise with 1D.

For regime routing: 1W is materially valuable. The portfolio layer's regime detector, operating on weekly bars, produces regime calls that are 5× more stable than daily calls. The whipsaw cost of daily regime misclassification (estimated 0.03–0.06 Sharpe units annually from the deep research report's analysis of turnover amplification from frequent weight updates) is substantially reduced by a weekly regime signal.

**Architectural implication:** 1W should be integrated as a **regime signal and portfolio layer input**, not as a full third signal tier requiring its own walk-forward evaluation and skill instances. Running a full skill library at 1W creates unnecessary complexity. Using 1W bars for regime state detection and signal confirmation/gating is the correct use.

### B4. Minimum Historical Depth for 1W Walk-Forward

The deep research report specifies: IS = 4 years, validation = 1 year, OOS = 1 year, rolled annually. For 1W bars:
- IS period: 4 years × 52 = 208 weekly bars. This is adequate but not generous. Parameter estimation on 208 observations with any volatility clustering will have material estimation error.
- 3 full OOS windows (minimum for regime diversity): 4+1+1 + 2×(1+1) = 10 years total data required.
- For crypto assets: 10 years of weekly data is unavailable (Bitcoin has 15 years; most altcoins have 4–8 years). **Weekly walk-forward on crypto assets is data-constrained at the strict 10-year standard.**
- For equities and commodities: 10 years of weekly data available and sufficient.

**Practical resolution:** Apply 1W walk-forward with 6-year minimum (IS=4, val=1, OOS=1; 2 OOS windows only). Accept higher regime-diversity uncertainty on weekly signals. This is a known limitation, not a fatal constraint, provided it is explicitly stated in evaluation reports.

### B5. Does 1W Materially Improve Drawdown Control?

**Yes. This is the most robust benefit of 1W integration.**

A correlation-triggered deleveraging rule using weekly rolling correlation is 5× less prone to false triggers than the same rule on daily bars. In a choppy market (daily correlation spikes that resolve within the week), a weekly-smoothed correlation measure avoids 60–70% of false deleveraging events. Each false deleveraging event costs approximately 0.3–0.8% in missed returns (cost of reducing positions and re-establishing them). Eliminating 60–70% of these events at a daily rate of ~2–3 false triggers per year saves approximately 0.4–1.7% annually.

In a genuine market stress event (2020-style), a weekly regime signal will lag the crisis onset by 1–2 weeks. This lag is a real cost: at 12% annual portfolio volatility, 2 weeks of unhedged exposure in a crisis contributes approximately 1.2–2.4% additional DD. **The 1W regime signal is not better than daily at crisis detection — it is worse. It is better at avoiding false alarms in normal conditions.**

This tradeoff is explicit and acceptable: the daily false-alarm cost exceeds the 1W crisis-lag cost in most market environments. The exception is sudden-onset crises (pandemic-style), where 1W lag is genuinely harmful.

**Resolution:** Use 1W for routine regime state (trending/ranging/correlated); retain a daily circuit breaker (the hard 12% DD stop) that operates independently of the weekly regime signal. The daily circuit breaker catches the sudden-onset crisis case that 1W misses.

### B6. Decision: Go / Conditional Go / No-Go for 1W

**Conditional Go.**

Conditions:
1. 1W is integrated as a **regime overlay and portfolio-layer input only**, not as a third independent skill tier.
2. 1W walk-forward uses a minimum 6-year data requirement, with explicit documentation that crypto assets operate under the lower-bound data constraint.
3. The daily DD circuit breaker (12% trigger) is **not replaced or deactivated** by weekly regime signals. Both coexist as independent controls.
4. 1W signals do not add new skill instances to the walk-forward evaluation matrix. If it appears as a separate timeframe in the leaderboard, it must carry the same OOS validation requirement as 4H and 1D.

**Required structural constraints:**
- 1W regime state: updated once per week on Monday open. Not mid-week.
- Skill instances on 1W: maximum 2 (trend confirmation, correlation measurement). No new signal families.
- Minimum 1W OOS window: 52 bars (1 year). Do not evaluate 1W signals on windows shorter than this.

---

## Section C — Short Positions (x1 Gross Only)

### C1. Does Long/Short Materially Increase Sharpe Expectation?

**Yes, but the magnitude is regime-dependent and mechanically constrained by the gross-≤1 rule.**

The theoretical Sharpe benefit from removing the long-only constraint is:
- Under perfect forecasts: removing long-only constraint doubles information content exploited. Sharpe gain ~100%.
- Under realistic IC (0.03–0.06 for 4H–1D signals on liquid assets): the gain is proportional to the additional positions taken. With gross ≤ 1, short positions substitute for zero-exposure positions in the long-only case. The gain is smaller than unconstrained long-short.

Quantified estimate under gross ≤ 1 constraint:
- Long-only system in bearish regime: under-invested (cash) = wasted alpha on the short side.
- Long/short system: shorts in bearish regime generate positive P&L. Net expected gain ≈ IC_short × breadth_short × vol_short. At IC = 0.04 and breadth of ~5 short positions per month: Sharpe delta ≈ 0.04 × √(60) × 1 ≈ +0.31 gross, before costs.
- After short-side implementation costs (0.5–2% annual borrow on short notional, 0.3–0.5% additional turnover cost): net Sharpe delta ≈ +0.04 to +0.10.

**Expected Sharpe delta: +0.04 to +0.10. Base case: +0.06.**

This is real but not large. The gross ≤ 1 constraint is the binding limiter.

### C2. Does Short Selling Increase Tail Risk?

**Yes, in specific scenarios that are distinct from long-only tail risks.**

Long-only tail risk: assets fall further than expected. Maximum loss is 100% of position.
Short-side tail risk: assets rise violently against the short position. Loss is theoretically unlimited (in practice, bounded by stop-loss, but stop-loss execution in illiquid or fast-moving markets is unreliable).

Specific tail risks from short selling in this universe:
1. **Short squeeze in crypto assets:** A top-4-per-sector crypto asset (e.g., ETH, SOL) can experience 30–60% short squeezes in hours during forced liquidation cascades. At a 5% portfolio short on one asset, this produces 1.5–3.0% portfolio loss in a single session. At a 15% total short exposure, a coordinated squeeze event produces 4.5–9.0% portfolio loss — material relative to the 20% DD budget.
2. **Funding rate inversion (crypto perpetuals):** If short positions are implemented via perpetual futures rather than spot short-selling (which may not be available for crypto), funding rates in bull markets can run 0.1–0.5% per 8-hour period (73–365% annualized). This is a slow bleed that is not captured in OHLCV backtests and must be modeled in SimBroker.
3. **Recall risk (equities):** In an equity short, the prime broker can recall borrowed shares at any time, forcing premature position closure. This risk is low for top-4-per-sector liquid equities but non-zero.

**DD delta from tail risks:** +2 to +4 percentage points on maximum drawdown in stress tail scenarios (short squeeze coinciding with max drawdown period). This partially offsets the DD reduction benefit from hedging.

### C3. Does Shorting Reduce Regime Asymmetry?

**Yes. This is its most structurally valuable property.**

A long-only system is regime-asymmetric by construction: it profits in risk-on and underperforms in risk-off. The system can only "defend" in risk-off, not profit from it. This creates a structural beta to economic cycles that the portfolio layer cannot fully neutralize regardless of vol targeting.

Short positions allow the system to be **directionally symmetric across regimes**:
- Risk-on: net long, profits from rising assets
- Risk-off: net short or low-net, profits from falling assets
- Sideways: mixed long-short, captures mean reversion

This symmetry directly reduces the regime-dependency of P&L. A long/short system that correctly identifies regime state should produce more consistent per-regime Sharpe than a long-only system.

**Caution:** the symmetry benefit is conditional on having predictive short signals. A system that shorts in risk-off but selects the wrong assets to short earns less than cash — it has added complexity with negative expected value for that component. Short-side signal quality must be validated separately in the walk-forward harness.

### C4. Does Shorting Increase Turnover Costs?

**Yes. Short positions generate higher turnover than equivalent long positions.**

Reasons:
1. Stop-loss asymmetry: short positions against the trend are stopped out faster than trend-aligned long positions. Short positions against upward momentum require tighter stops to prevent large losses.
2. Funding cost accumulation: on crypto perpetuals, holding a short overnight incurs funding costs that incentivize shorter holding periods.
3. Mean-reversion of short signals: short signals on highly liquid assets tend to mean-revert faster than long signals (short-term reversion is well-documented post-sharp-decline). This causes higher entry/exit frequency.

**Estimated additional turnover from short positions:** 0.3–0.8 round trips per asset per month for active short positions. At average 25–30% portfolio in shorts: approximately 0.10–0.25 additional portfolio round-trips per month. At 0.25% round-trip cost: 0.3–0.75% additional annual cost. Sharpe impact: −0.02 to −0.06.

### C5. Implementation Complexity

**Significant. Cross-asset complexity is non-trivial.**

For a universe mixing equities and crypto:
- **Equities:** short via broker margin account (requires borrow; incurs borrow cost 0.25–2% annualized for liquid names). SimBroker must model borrow availability and cost.
- **Crypto:** short via perpetual futures (different instrument type, different cost structure, funding rate mechanics, basis risk). SimBroker must model perpetual mechanics separately from spot OHLCV.

These are **not the same implementation problem**. A SimBroker that handles equity short-selling correctly does not automatically handle crypto perpetual shorts. This is a hidden complexity multiplier.

For a solo developer, building a SimBroker that correctly handles both equity borrows and crypto perpetual funding rates in parallel adds approximately 30–50% to the SimBroker build and validation time in Era 1. This must be budgeted explicitly.

### C6. Delivery Summary: Short Positions

**Expected Sharpe delta:** +0.04 to +0.10 (base: +0.06). Partially offset by: borrow costs, funding rates, higher turnover. Net expected delta after costs: +0.02 to +0.07.

**DD delta:** −2 to −5 percentage points (hedging benefit in stress). Partially offset by: +2 to +4 percentage points (short squeeze / tail risk). Net DD delta in median stress scenario: −1 to −3 percentage points.

**Complexity delta:** High. SimBroker must be rebuilt or significantly extended to handle two distinct short-selling mechanisms (equity borrow vs crypto perpetuals). Adds ~30–50% to Era 1 build time.

**Final recommendation:** **Conditional adoption, sequenced after 1W regime integration is validated.** Short positions should not be introduced simultaneously with 1W. The correct sequence is: (1) establish long-only baseline with 1W regime overlay; (2) validate portfolio layer with 1W; (3) then introduce short positions as a strategy extension.

**The short-selling extension is worth implementing but not worth rushing.** Premature short-side implementation with an unvalidated SimBroker cost model will produce systematically optimistic backtests, which is the failure mode the architecture is designed to prevent.

---

## Section D — Factor Collapse Under Long/Short + 1W

### D1. Does Short Exposure Double Factor Space?

**No. It expands factor space, but by far less than a factor of two.**

Factor space is determined by the number of genuinely independent return drivers. Adding short positions does not create new factors — it accesses the same factors from the opposite direction. A long momentum strategy and a short mean-reversion strategy are not independent factors; they are both expressions of the same directional bias in trending regimes.

The true factor expansion from long/short:
- **New access:** negative beta exposure (market-neutral or short-biased in risk-off). This is a genuinely new positioning unavailable to long-only.
- **Partial expansion:** long-short spreads within sectors (long strong/short weak within same sector cluster). This captures the cross-sectional momentum factor more completely than long-only.
- **No expansion:** time-series factors (trend, mean-reversion) are accessed in both directions but remain the same factors.

Estimated factor space expansion: +1 to +2 genuinely independent return drivers. Not +5 to +10.

### D2. How Many Independent Clusters Are Realistic Now?

**Expected effective N range under 4H + 1D + 1W + long/short:**

Normal regime:
- Without extensions: N_eff ≈ 3–5 (v2 baseline)
- With 1W regime overlay: +0.3–0.5 (stability of factor expression, not new factors)
- With long/short: +0.5–1.5 (negative beta access, cross-sectional spread)
- Total: N_eff ≈ **4–7 in normal conditions**

Stress regime (ρ spikes to 0.7+):
- Without extensions: N_eff ≈ 2–4 (v2, citing Longin & Solnik correlation increase in bear markets)
- With 1W + long/short: correlation spike affects long-side assets. Short positions may not maintain independence if squeeze events create correlated losses.
- Total: N_eff ≈ **2–5 in stress conditions**

### D3. Is Effective N > 4 Plausible?

**Yes, in normal conditions. Probability: ~55–65%.**

Previously: P(N_eff > 4 in normal conditions) ≈ 35–40%.
Revised with 1W + long/short: P(N_eff > 4 in normal conditions) ≈ 50–60%.

This improvement is meaningful but not transformative. The stress-regime N_eff collapse remains the binding constraint on realized diversification.

### D4. Does Time-Scale Diversification Improve Independence?

**Yes, but the improvement is in IC consistency, not factor count.**

The primary benefit of multi-timeframe systems is not factor independence — it is signal consistency. A 1W trend signal and a 4H trend signal on the same asset are correlated, but they disagree at transition points. These disagreements are informative: when 1W is trending up but 4H is pulling back, the pullback is more likely to be mean-reverting than trend-reversing. This conditional information is valuable for position sizing, not for creating independent factors.

Multi-timeframe systems improve IC per unit of information. They do not materially increase the number of independent P&L drivers.

**Practical implication:** The effective-N improvement from adding 1W comes primarily via the portfolio construction pathway (better-informed position sizing), not via the signal diversity pathway (more independent signals).

### D5. Is Collapse Probability Reduced?

**Reduced, not eliminated.**

| Scenario | P(N_eff ≤ 2, normal regime) | P(N_eff ≤ 2, stress regime) |
|---|---|---|
| V2 baseline (4H+1D, long-only) | ~15% | ~40% |
| V3 (4H+1D+1W regime, long/short) | ~10% | ~30–35% |

The stress-regime collapse probability remains high because neither extension resolves the fundamental problem: 20 liquid assets in a macro risk-off event will correlate above 0.65 regardless of timeframe or directionality. Short positions on the weakest assets may themselves be squeezed. The probability reduction is real (~5–10 percentage points) but the risk is not eliminated.

---

## Section E — Portfolio Layer Impact

### E1. Does Long/Short Make Portfolio Construction More Important?

**Yes. Materially so.**

Long-only portfolio construction manages: position size, correlation, vol target. Three primary inputs.

Long/short portfolio construction manages: gross exposure, net exposure, position size, correlation (long-side and short-side independently), vol target, net beta (separate from vol target), sector neutrality (optional but relevant). Seven or more primary inputs.

The additional inputs are not interchangeable. Gross exposure and net exposure are independent constraints. A portfolio that is 80% long and 20% short has 100% gross but 60% net — different risk properties from a 60% long, 0% short portfolio with the same "net." SimBroker, evaluation engine, and portfolio layer must all track both dimensions.

**This is not a reason to avoid long/short — it is a reason to build the extended portfolio construction framework before implementing shorts, not after.**

### E2. Does 1W Enable Better Regime Routing?

**Yes. This is the clearest and most defensible structural benefit in this entire extension proposal.**

The deep research report notes that regime routing is "mostly descriptive" (lagged) rather than predictive. Weekly-smoothed descriptive signals have lower false-positive rates than daily signals. Specifically:
- A weekly realized-vol estimate requires two consecutive weeks of elevated vol before triggering deleveraging. This eliminates single-session vol spikes from triggering unnecessary position cuts.
- A weekly correlation estimate (20-week rolling window) changes more slowly. This prevents the correlation-triggered deleveraging rule from firing on transient 3-day correlation spikes.

**Estimated reduction in false-trigger deleveraging events:** 50–65%. Each false trigger costs 0.3–0.8% in missed returns. At an estimated 2–4 false triggers per year: annual savings of 0.6–2.0%. Sharpe impact: +0.05–0.17. This is real and consistent.

### E3. Can Portfolio Layer Add ≥ 0.10 Sharpe?

**Probability increased from ~45% (v2) to ~55–60% (v3).**

The improvement comes from two independent mechanisms:
1. 1W regime signals reduce false deleveraging (adds ~0.05–0.17 Sharpe, probabilistically).
2. Long/short enables positive returns in both regimes, reducing the drag from regimes where long-only is forced to sit in cash.

The ceiling for portfolio-layer improvement remains bounded by the deep research report's finding: "portfolio-layer improvements are real only under strong regularization/constraints and cost control." The probability increase is from improved regime routing, not from complexity addition.

### E4. Should Portfolio Construction Complexity Increase?

**Yes, but specifically and minimally.**

Required additions (not optional):
1. **Gross exposure tracking:** |longs| + |shorts| ≤ 100% NAV at all times. Hard constraint.
2. **Net exposure reporting:** separate metric from vol target. Net exposure is not bounded, but must be monitored and reported.
3. **Short-side correlation tracking:** pairwise correlation among short positions tracked separately. Short-side N_eff should be computed independently of long-side N_eff.
4. **Borrow cost integration:** SimBroker and portfolio layer must deduct borrow costs from short position P&L in real time.

**Not required (do not add without demonstrated need):**
- Sector-neutrality constraints (adds optimization complexity; not validated as value-adding in this universe)
- Beta-neutral constraints (conflicts with the regime-routing architecture, which intentionally takes directional views)
- Dollar-neutral constraints (an unnecessary constraint that reduces the long/short flexibility the extension is designed to provide)

---

## Section F — Drawdown Model Update

### F1. Is DD Enforcement Easier or Harder with Long/Short?

**Easier in trending environments. Harder in squeeze events.**

Long-only DD mechanics: portfolio falls when assets fall. Simple, linear.
Long/short DD mechanics: portfolio falls when longs fall AND/OR when shorts rise against the position. Two independent adverse states. In squeeze events, the adverse states can occur simultaneously (longs falling during broad market stress, shorts rising due to a squeeze).

Net assessment: DD enforcement is mechanically easier in normal trending regimes (short positions provide hedge) and more complex in stress events (simultaneous adverse long and short movement is possible). The new structural controls below address the stress regime case.

### F2. Does Shorting Reduce Crisis DD?

**In standard risk-off events: yes, by 2–5 percentage points.**
**In squeeze-dominated events: may worsen DD by 1–3 percentage points.**

Standard risk-off (2022 rate shock): assets fall uniformly, short positions in weaker assets generate gains. Estimated DD reduction: 3–6 percentage points relative to long-only. This is meaningful.

Squeeze-dominated events (crypto-specific; e.g., 2021 leveraged long unwind): cascading liquidations drive short squeezes simultaneously with falling prices elsewhere. Portfolio faces correlated losses on both long and short positions. DD worsening: 1–4 percentage points relative to long-only.

**Net statistical expectation across regime types:** DD reduction of approximately 1–3 percentage points in median adverse scenarios. This helps, but the reduction is not contractually reliable in all stress environments.

### F3. New Structural Controls Required for Long/Short

These controls are **additive** to the four existing DD enforcement rules from v2. They do not replace them.

**Control LS-1: Maximum single-asset short exposure cap**
No single asset short position exceeds 5% of portfolio NAV. This limits the maximum loss from a single short squeeze event to 5% × (theoretical max loss factor). For an asset that gaps 60% against the short: maximum single-squeeze loss ≤ 3% of portfolio. Combined with the 12% DD circuit breaker, this bounds the scenario where multiple squeezes occur simultaneously.

**Control LS-2: Total short exposure cap**
Total short positions ≤ 30% of portfolio NAV in normal regimes; ≤ 20% in high-correlation regimes (when pairwise correlation > 0.55). This prevents the scenario where a coordinated squeeze event creates >6% portfolio loss from the short book alone.

**Control LS-3: Short position stop-loss tighter than long**
Short positions: maximum 4% adverse move from entry before stop-loss. Long positions: maximum 6% adverse move. This asymmetry reflects the asymmetric risk profile: short positions have unlimited theoretical loss while long positions are bounded at 100%.

**Control LS-4: Funding rate monitoring (crypto perpetuals)**
If perpetual funding rate on any held short position exceeds 0.05% per 8 hours (equivalent to ~220% annualized), the position is exited regardless of signal. This prevents slow-bleed funding rate traps during extended bull regimes.

**Control LS-5: Gross exposure accounting at portfolio layer**
Portfolio layer must verify gross ≤ 100% NAV before every rebalance. If a prior position moved against the short (short position grew due to price rise), and gross exposure has exceeded 100%, immediate pro-rata reduction is triggered before new positions are added.

### F4. Revised DD Probability Under Extended Model

| DD Threshold | V2 (long-only, 4H+1D) | V3 (long/short, 4H+1D+1W) |
|---|---|---|
| P(DD > 20%, normal regime, annual) | ~10% | ~7% |
| P(DD > 20%, high-correlation regime, annual) | ~35% | ~25–28% |
| P(DD > 20%, crypto squeeze scenario) | ~20% | ~22–25% (slightly worse) |
| P(DD > 20%, 2020-style sudden onset) | ~40% | ~32–35% (1W lag mitigated by daily circuit breaker) |

The improvements are real. The LS-short squeeze risk introduces a new adverse scenario not present in v2. The net expected outcome is an improvement of ~5–8 percentage points in high-correlation regime DD probability — which is the most relevant scenario for the ≤20% DD target.

---

## Section G — Solo Execution Stress Test

### G1. Maintenance Burden Delta

**Quantified complexity additions from 1W + short positions:**

| Component | V2 Maintenance (hrs/month) | V3 Addition | Total |
|---|---|---|---|
| Data pipeline | 2–4 | +0.5 (1W bar aggregation, minimal) | 2.5–4.5 |
| SimBroker | 1–2 | +3–6 (short borrow mechanics, crypto perpetual funding) | 4–8 |
| Walk-forward harness | 3–5 | +1–2 (1W OOS window management) | 4–7 |
| Portfolio layer | 2–4 | +2–3 (gross/net exposure tracking, LS controls) | 4–7 |
| Performance attribution | 1–2 | +1–2 (long P&L, short P&L, borrow cost P&L separately) | 2–4 |
| **Total** | **9–17 hrs/month** | **+7.5–13.5 hrs/month** | **16.5–30.5 hrs/month** |

Combined with v2's existing maintenance estimate of 15–40 hours/month, total maintenance burden rises to **24–71 hours/month**. The upper bound of this range exceeds a part-time developer's total capacity.

**This is a significant finding.** A solo developer working 40 hours/week at the Era 2–3 maintenance level is spending 37–89% of their time on maintenance before any new development. This is the mechanism by which the project stalls.

### G2. Is Complexity Still Manageable for Solo?

**At full-time effort: barely. At part-time effort: no.**

The additions are not negligible. The SimBroker extension for short selling (equity borrow mechanics + crypto perpetual funding rates) is a 30–50% extension of the SimBroker build scope. This is not a minor addition — it is a second implementation project within the same module.

If the developer is part-time (20 hrs/week, ~80 hrs/month), post-maintenance available development bandwidth at v3 complexity is:
- V2 complexity: 80 − (15+40)/2 = 52.5 hours/month available for development
- V3 complexity: 80 − (24+71)/2 = 32.5 hours/month available for development

This 38% reduction in development bandwidth has direct implications for the era timeline: Era completion dates extend proportionally.

### G3. What Must Be Removed to Compensate?

If both extensions are adopted, the following compensatory cuts are **required**, not optional:

**Cut C1: Freeze Era 4 (Insight Layer + CCA) until Era 3 is complete and validated.**
The v2 already deferred CCA from live portfolio influence. Under v3 complexity, Era 4 scope must not begin until Era 3 "Done" criteria are met and 3 months of post-Era-3 maintenance are completed at stable bandwidth. This extends the Era 4 start from month 9–12 to month 12–18.

**Cut C2: 1W skills are limited to 2 instances maximum.**
The 1W timeframe must not expand to a full skill library tier. Maximum 2 skill types on 1W: (1) a trend confirmation filter, (2) a regime state indicator. All other 1W analysis happens at the portfolio layer, not the skill layer. This prevents 1W from adding ~20 new skill instances to the evaluation matrix.

**Cut C3: Short selling introduced to one asset class first.**
Do not implement short selling across all 20 assets simultaneously. Begin with the 5 most liquid equity assets, where borrow mechanics are simplest. Validate SimBroker accuracy for equity shorts against paper trading before extending to crypto perpetuals. Crypto shorts are Phase 2 of the short-selling implementation, not Phase 1.

---

## Section H — Updated Probability Model

### Governing Adjustment Logic

All probability updates from v2 are bounded by the following:
- The deep research report confirms: P(live net Sharpe < backtest Sharpe) ≈ 70–85%. This multiplicity degradation applies to the v3 extensions as well.
- Extensions improve alpha surface modestly (+0.04–0.10 Sharpe) but also increase implementation complexity and maintenance burden. The net expected probability improvement is partial.
- Solo execution bandwidth is more constrained under v3 than v2. This acts as a negative correction on all timeline-dependent probabilities.

### H1. Net Sharpe ≥ 0.35 at 18 Months

| Basis | Estimate |
|---|---|
| V2 estimate | 20–32% |
| Positive adjustment (1W turnover reduction + long/short alpha expansion) | +3–7% |
| Negative adjustment (increased complexity, SimBroker rebuild, solo bandwidth constraint) | −4–8% |
| **V3 revised estimate** | **19–31%** |

The adjustments nearly cancel. The 18-month probability is structurally unchanged. The extensions do not accelerate the timeline to validated profitability — they shift the composition of the edge, not its arrival time.

### H2. Net Sharpe ≥ 0.50 at 24 Months

| Basis | Estimate |
|---|---|
| Deep research report estimate | 15–30% (ranges cited for 24-month period) |
| Positive adjustment (1W + long/short expand optimistic ceiling) | +3–6% |
| Negative adjustment (complexity debt slows iteration; short-side validation required separately) | −2–5% |
| **V3 revised estimate** | **16–31%** |

Net effect: approximately unchanged from v2 estimate. The optimistic ceiling rises marginally; the base probability is similar.

### H3. Effective N ≥ 4 Achievable

| Basis | Estimate |
|---|---|
| V2 baseline (P of N_eff ≥ 4 in normal regime) | ~35–40% |
| Positive adjustment (long/short adds ~1–2 factors; 1W adds ~0.3–0.5) | +10–15% |
| Negative adjustment (stress regime squeeze risk reduces N_eff; gross ≤ 1 constraint limits LS diversification) | −5–8% |
| **V3 revised estimate** | **40–52%** |

For the first time, P(N_eff ≥ 4) has a reasonable base probability above 50%. This is the most meaningful structural improvement from the extensions.

### H4. System Becoming Capital Allocation Framework

**V3 estimate: 58–68%** (v2: ~55%)

The long/short extension makes the Capital Allocation Framework classification more stable: a long/short, multi-timeframe system with treasury yield on idle capital is the archetype of this classification. The architecture more closely matches the classification's definition.

### H5. System Becoming Niche Alpha Engine

**V3 estimate: 20–28%** (v2: ~22–30%)

The probability that the system achieves standalone alpha justification (net Sharpe ≥ 0.50 sustained for 24+ months) is slightly lower under v3 than v2, because the complexity increase under solo execution raises the probability of implementation errors masking genuine alpha. The higher ceiling (optimistic v3 Sharpe 0.50–0.72) is offset by higher probability of complexity-induced quality degradation.

### H6. Statistical Fragility Risk

**V3 estimate: 32–40%** (v2: ~35%)

The risk of the system being statistically fragile (evaluation framework untrustworthy, multiplicity uncorrected, no confirmed OOS edge) is slightly elevated under v3. The additional complexity creates more opportunities for silent errors in the walk-forward harness. The risk is mitigated only if the evaluation engine and SimBroker are fully validated before the extensions are activated.

---

## Section I — Final V3 Verdict

### Classification

**Capital Allocation Framework (maintained from v2).**

The proposed extensions do not change the fundamental classification. They improve the system's internal coherence as a Capital Allocation Framework:
- Long/short enables regime-symmetric capital deployment (core Capital Allocation Framework property).
- 1W regime signals improve stability of allocation decisions (core Capital Allocation Framework property).
- Treasury layer (from v2) provides base return floor on idle capital (core Capital Allocation Framework property).

The extensions do not push the system toward Niche Alpha Engine territory. They do not materially increase the standalone signal alpha. They improve the efficiency of existing alpha surface utilization and reduce the regime-asymmetry that was a weakness of the long-only design.

A reclassification to Niche Alpha Engine would require demonstrated net Sharpe ≥ 0.50 in OOS walk-forward spanning ≥2 regimes. The extensions improve the probability of this outcome from ~22–30% to ~20–28% — effectively unchanged, because the complexity overhead partially offsets the alpha expansion.

### Three Structural Improvements from V2

**Improvement 1: Regime-triggered deleveraging is now deterministic and not subject to whipsaw.**
1W regime signals reduce false deleveraging events by 50–65%. The hard daily circuit breaker (12% DD) coexists as the catch for sudden-onset crises. This dual-layer design — slow regime signal (1W) + fast circuit breaker (daily) — is more robust than a single-frequency signal.

**Improvement 2: Directional symmetry eliminates the "forced cash" state.**
In bearish regimes, the long-only system's optimal response is to hold cash — earning zero while missing short-side alpha. The long/short extension converts this dead-weight state into a positively contributing state. Estimated annual benefit: +0.02 to +0.07 Sharpe in bearish regime periods.

**Improvement 3: Effective N floor raised.**
P(N_eff ≥ 4 in normal regime) increases from ~35–40% to ~40–52%. This reduces the probability of the most common factor-collapse failure mode.

### Three New Risks Introduced

**Risk 1: SimBroker scope creep.**
Short-selling mechanics (equity borrow, crypto perpetual funding) require significant SimBroker extensions. If these extensions are implemented with optimistic cost assumptions, the entire OOS evaluation is compromised. The v2 "SimBroker optimism cascade" failure mode is more likely under v3, not less.

**Risk 2: Maintenance bandwidth breach.**
At v3 complexity, a part-time developer's available development bandwidth drops from ~52 hours/month to ~32 hours/month. At the lower end, this is below the threshold needed to iterate on Era 3 while maintaining Era 2 infrastructure. The risk of maintenance consuming all available capacity is elevated under v3.

**Risk 3: Short-squeeze tail event during evaluation period.**
Short selling introduces a new tail scenario absent in v2: a coordinated squeeze event during the OOS evaluation period. If this event occurs before sufficient history exists to distinguish squeeze losses from system failure, it may trigger kill criteria prematurely or, worse, be absorbed into the "normal variance" of a system that looks otherwise functional. The kill criteria require revision to handle squeeze-specific events (see below).

### Three Non-Negotiable Constraints for V3

**Non-negotiable 1: Sequential, not simultaneous, implementation of extensions.**
Sequence:
1. Integrate 1W as regime overlay. Validate DD improvement. (Era 1–2 scope)
2. Validate long-only baseline to Era 2 "Done" criteria.
3. Introduce short selling on equities only. Validate SimBroker borrow cost accuracy.
4. Extend shorts to crypto perpetuals only after equity short validation is complete.

Violating this sequence — implementing both 1W and shorts simultaneously before the long-only baseline is validated — introduces compounded sources of error that cannot be disentangled. This is not a stylistic preference; it is a logical requirement for attribution of causes.

**Non-negotiable 2: Gross exposure hard cap enforced in real-time.**
|long| + |short| ≤ 100% NAV. Verified at every rebalance event. No exceptions. If a position moves against the short (growing the gross), an immediate partial exit is triggered before new positions are added. The constraint must be a hard rule in the portfolio layer, not a monitoring alert.

**Non-negotiable 3: Long P&L, short P&L, and treasury P&L reported independently.**
Performance attribution must separate: (a) long position P&L, (b) short position P&L, (c) borrow/funding cost P&L, (d) treasury yield P&L. Any blending of these streams destroys the ability to evaluate whether the short extension is adding value. The original v2 treasury separation rule extends to: four-stream attribution, not two-stream.

### Revised Kill/Pivot Criteria for V3

**Kill K1 (revised):** Net OOS Sharpe < 0.28 after 15 months. Unchanged.
**Kill K2 (unchanged):** Cost structure dominance.
**Kill K3 (unchanged):** Effective N ≤ 2 after controls.
**Kill K4 (new in v3):** Short-side P&L is negative in aggregate after 12 months of short positions being active. A short book that generates cumulative negative P&L after borrow/funding costs over 12 months is not adding edge — it is adding risk for negative expected value. Retire short positions; revert to long-only.
**Kill K5 (unchanged):** Treasury yield > 60% of total return.
**Kill K6 (new in v3):** SimBroker short-cost model diverges from realized costs by > 20% (absolute). If the SimBroker underestimates short-side costs by more than 20% relative to paper trading validation, all short-position OOS metrics are unreliable. Halt short-position development until SimBroker is recalibrated.

---

**Final Decision:**

**Conditional Evolution Only.**

The extensions (1W + long/short) are structurally justified and modestly improve the system's expected performance envelope. They are not transformative. They do not change the classification. They do not reduce the 18-month success probability materially.

**The conditions for proceeding:**
1. Era 2 "Done" criteria from v2 must be met before any v3 extension is activated.
2. 1W regime overlay must be implemented and validated (≥ 3 months of stable regime classification, measured against daily circuit breaker outcomes) before short selling begins.
3. SimBroker must be extended and validated against paper trading reference costs before any short-position results are treated as credible.

**Do not expand until v2 is validated.** The v3 extensions are next-phase scope. They are not current-phase scope. Treating them as current-phase additions before v2 validation is a complexity failure mode, not a feature.

---

*Document Version: 3.0 | Review Date: 2026-03-02 | Supersedes: v2.0 classification on short positions, 1W integration, and factor collapse probability*
*Next Scheduled Review: End of Era 2 (portfolio layer validated) — at that point, v3 extensions become active scope*
