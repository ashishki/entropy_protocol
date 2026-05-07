# Strategic Architecture Review v4 — Independent Quant Audit of V3
**Classification:** Confidential — Internal Strategic Document
**Auditor role:** Independent Quant Auditor / Red-Team Reviewer
**Date:** 2026-03-02
**Version:** 4.0 (Audit Pass)
**Basis:** Strategic Architecture Review v3.0 (2026-03-02)
**Scope:** Adversarial stress-test of v3 claims — Sharpe deltas, DD probabilities, 1W timeframe claims, short implementation assumptions, structural integrity

**Operating mode:** Adversarial. No optimism bias. No architectural expansion. No defense of prior conclusions.

---

## SECTION 1 — SHARPE & IC CLAIMS

---

### 1.1 Sharpe Delta from Turnover Reduction: +0.03–0.08

**Rating: Weakly Supported**

Claim (A3): 1W integration reduces turnover by 25–40%, saving 0.03–0.08 Sharpe units.

**Problem 1 — Source of 25–40% is asserted, not derived.**
The turnover reduction estimate is presented as if self-evident. The actual reduction depends on regime stability of the 1W signal, which is itself the variable being estimated. If the weekly regime signal flips 8 times per year instead of 4, the turnover reduction collapses toward zero. No sensitivity analysis is provided.

**Problem 2 — Inconsistency between B1 and A3.**
Section B1: "30% turnover reduction saves approximately 0.05–0.08 Sharpe units."
Section A3: "Cost drag reduces by approximately 0.03–0.08 Sharpe units."
Lower bound shifts from 0.03 to 0.05 between sections without explanation. These numbers are inconsistent and neither is derived from a formula.

**What minimum model would justify this claim:** Define regime flip frequency distribution, compute expected turnover as a function of flip frequency, then propagate to Sharpe via `saved_cost% / portfolio_vol`. At round-trip cost 0.25% and 30% turnover reduction from 18 to 12.6 round trips/year at average 5% position weight: saved cost ≈ 5.4 trips × 5% × 0.25% = 0.068% NAV per asset × 20 assets = 1.35% NAV saved annually. At 12% portfolio vol: 0.11 Sharpe — higher than stated. The conservatism in the stated range is unexplained but not itself the primary problem. The primary problem is that 25–40% turnover reduction is circular: it depends on regime stability, which is the unvalidated input.

---

### 1.2 Clarke et al. Application: +15–30% Sharpe from Removing Long-Only Constraint

**Rating: Not Defensible under the gross ≤ 1 constraint**

Claim (A3): "Clarke et al. document +15–30% Sharpe improvement from removing the long-only constraint in well-calibrated systems. Applied to a base of 0.35: this implies +0.05–0.10 Sharpe delta."

**Critical problem:** Clarke et al. study unconstrained long-short portfolios where gross leverage is not bounded at 1.0. Removing the long-only constraint in their framework means you can take full short positions on top of full long positions (gross > 1). The architecture in v3 caps gross at exactly 1.0 — meaning shorts substitute for longs, not supplement them. This is a categorically different constraint regime.

Under gross ≤ 1 with a 30% short book, the system is effectively 70% long + 30% short. The information gain from the short side is therefore bounded by: at most 30% additional directional bets relative to a 100% long portfolio. This is not the same as the unconstrained Clarke et al. setup.

**The correct reasoning for gross ≤ 1:** The incremental Sharpe from shorts in the gross-constrained case is proportional to the IC uplift from being able to express short views versus holding cash. This is smaller than Clarke et al. by a factor reflecting the gross cap. A conservative estimate under gross ≤ 1 would be +8–15% relative improvement (not +15–30%), implying +0.03–0.05 Sharpe units at base 0.35 — half the claimed range.

The document partially acknowledges this ("With gross ≤ 1, short positions substitute for zero-exposure positions") but then uses the unconstrained Clarke et al. estimate anyway. This is a logical inconsistency.

---

### 1.3 FLAM Application: IC × sqrt(Breadth) in Section C1

**Rating: Not Defensible — mathematical error**

Claim (C1): "Net expected gain ≈ IC_short × breadth_short × vol_short. At IC = 0.04 and breadth of ~5 short positions per month: Sharpe delta ≈ 0.04 × √(60) × 1 ≈ +0.31 gross, before costs."

**This is a misapplication of the Fundamental Law of Active Management.**

The expression `IR = IC × sqrt(BR)` gives the total information ratio of a portfolio, not the incremental contribution from adding a new strategy sleeve to an existing portfolio. Applying this to "5 short positions/month × 12 months = 60 breadth" yields the Sharpe of a portfolio that only holds those 60 short bets, evaluated in isolation.

The correct calculation for the incremental Sharpe from adding the short sleeve to an existing long system with breadth BR_long is:

```
IR_total = IC × sqrt(BR_long + BR_short)
IR_long  = IC × sqrt(BR_long)
Delta_IR = IC × [sqrt(BR_long + BR_short) - sqrt(BR_long)]
```

If the long system has BR_long ≈ 240 bets/year (5 signals × 4 timeframes × 12 months, rough):

```
Delta = 0.04 × [sqrt(300) - sqrt(240)] = 0.04 × [17.32 - 15.49] = 0.04 × 1.83 ≈ +0.07 gross
```

The document's claim of +0.31 gross is inflated by a factor of ~4.4x relative to a correct marginal FLAM calculation. The final answer (+0.04–0.10 net) happens to be in a reasonable range, but the derivation is wrong. The intermediate step "0.31 gross before costs" is not defensible and will cause confusion when used as a reference point.

**Additionally:** The calculation assumes IC_short = IC_long = 0.04. This is a hidden assumption that is not validated. Short-side IC for liquid assets (especially crypto) is likely 0.02–0.03, not 0.04, due to short-squeeze noise in signal-to-P&L mapping. This is never tested or bounded in the document.

---

### 1.4 Combined Sharpe Delta: +0.04–0.10 from Both Extensions

**Rating: Not Defensible as presented — dimensional inconsistency**

The document derives:
- 1W turnover reduction: +0.03–0.08 Sharpe
- Long/short extension: +0.04–0.10 Sharpe (after costs, C1)
- Combined: +0.04–0.10 Sharpe (A3)

**Simple arithmetic:** 0.03 + 0.04 = 0.07 lower bound, 0.08 + 0.10 = 0.18 upper bound.

The combined estimate of +0.04–0.10 is less than the sum of the parts. No interaction term is stated. No explanation is provided for why the combination yields a figure lower than what the components individually imply and identical to the short-side estimate alone.

This is either: (a) an unstated negative correlation penalty between 1W and L/S benefits, (b) a conservative combined estimate with the justification omitted, or (c) an arithmetic error. All three interpretations are problems. If (a), the interaction needs to be specified. If (b), the omission should be filled. If (c), it should be corrected.

---

## SECTION 2 — DRAWDOWN & PROBABILITY CLAIMS

---

### 2.1 DD Probability Table (F4)

**Rating: Quantitatively Loose — False Precision**

| DD Threshold | V2 | V3 |
|---|---|---|
| P(DD > 20%, normal regime, annual) | ~10% | ~7% |
| P(DD > 20%, high-correlation regime, annual) | ~35% | ~25–28% |
| P(DD > 20%, crypto squeeze scenario) | ~20% | ~22–25% |
| P(DD > 20%, 2020-style sudden onset) | ~40% | ~32–35% |

**None of these numbers are model-backed.**

The improvement from 35% to 25–28% in the high-correlation regime is presented as a quantified result of adding L/S and 1W controls. The 7–10 pp improvement is within any reasonable uncertainty band for heuristic estimation. The actual uncertainty range on "P(DD > 20% in a high-correlation regime)" for a 20-asset system with mixed equity/crypto is approximately ±15 pp given the model error alone. A point estimate of 25–28% vs 35% is indistinguishable from noise at this level of uncertainty.

**What minimum modeling would justify these numbers:**
- Parametric: specify a process for portfolio vol and drawdown (e.g., Ornstein-Uhlenbeck or GBM with drift), calibrate to asset vol and correlation assumptions, compute DD exceedance probabilities analytically or via closed-form approximation.
- Simulation: Monte Carlo over calibrated joint return distributions with regime-switching, at minimum 10,000 paths.
- Historical: use empirical DD distributions from similar strategy types in comparable universes.

None of these approaches are present. The numbers are derived from intuition adjustment over prior intuition estimates. The cascade of heuristic adjustments is not a model.

---

### 2.2 Factor Collapse Correlation Claim

**Rating: Not Defensible as stated**

Claim (D5): "20 liquid assets in a macro risk-off event will correlate above 0.65 regardless of timeframe or directionality."

This is stated as a structural fact without empirical citation.

**Counterevidence:** In March 2020 (COVID crash), pairwise correlations spiked across equities, but commodity/equity and crypto/equity correlations were not uniformly above 0.65. Bitcoin initially sold off with equities (positive correlation), then partially decoupled. Gold briefly fell with equities before inverting. Across a universe mixing sector equities, commodities, and crypto, the proportion of pairs with ρ > 0.65 in a crisis is likely 40–70%, not 100%.

The claim overstates the correlation collapse and therefore overstates the intractability of the effective-N problem — which paradoxically overstates the benefit of short positions by making the baseline look worse than it is.

---

### 2.3 Probability Model (Section H)

**Rating: Weakly Supported**

H1 claim: 18-month P(net Sharpe ≥ 0.35) revised from 20–32% to 19–31%.

The revision: +3–7% (positive) minus −4–8% (negative) = net −1% to +3%. Document calls this "structurally unchanged."

**Problem:** The positive and negative adjustments are themselves estimated with ±5–10% uncertainty each. The difference of two estimates each with ±5–10% uncertainty has combined uncertainty of ±7–14%. The resulting adjustment of "−1 to +3%" is entirely within the noise band. The calculation is arithmetically correct but statistically meaningless.

H3 claim: P(N_eff ≥ 4) revised from 35–40% to 40–52%.

A 10–17 pp improvement attributed to "+10–15% from L/S factors, −5–8% from stress/gross constraint." This is additive adjustment of probability estimates — an informal technique appropriate for rough estimation but not for presenting as a revised probability model. The 52% upper bound is not derivable from first principles.

---

## SECTION 3 — 1W TIMEFRAME CLAIMS

---

### 3.1 "1W Reduces False Triggers" — Circular Claim

**Rating: Weakly Supported**

The benefit of 1W regime signals is quantified as: "2–3 false deleveraging triggers per year avoidable, each costing 0.3–0.8%." This produces the "+0.05–0.17 Sharpe" regime-routing estimate in E2.

**The circular dependency:** The false-trigger rate (2–3/year) is an assumed input, not a measured value. The benefit calculation propagates this assumption forward as if it were data. In practice:
- In 2021 (crypto bull market), daily correlation spikes between crypto assets could trigger the ρ > 0.55 rule multiple times per month.
- In 2023–2024 (equity bull market), correlation across liquid equities was persistently elevated, potentially triggering sustained deleveraging rather than false spikes.
- The 2–3/year assumption may be appropriate for "normal" mixed-regime periods but is not bounded for extended trending or correlation regimes.

The +0.05–0.17 range is too wide to be actionable. A factor of 3.4x between lower and upper bound reflects the assumption sensitivity, not empirical confidence.

---

### 3.2 Inconsistency in False-Trigger Reduction Estimates

**Confirmed inconsistency:**

- Section B5: "avoids 60–70% of false deleveraging events"
- Section E2: "Estimated reduction in false-trigger deleveraging events: 50–65%"

Upper bounds differ by 5 percentage points. Lower bounds differ by 10 percentage points. These are not the same claim. The document uses both without noting the inconsistency or reconciling them into a single estimate.

---

### 3.3 Time-Scale Correlation Estimates

**Rating: Uncited — sensitivity not analyzed**

The document provides:
- ρ(4H, 1D) = 0.55–0.75
- ρ(1D, 1W) = 0.40–0.65
- ρ(4H, 1W) = 0.25–0.50

No empirical source. No citation. These are plausible priors but nothing more.

**Sensitivity problem:** The N_eff calculation uses average ρ ≈ 0.50 to get N_eff = 1.5 for 3 timeframes. If actual ρ = 0.60 (within stated range), N_eff = 3/(1 + 2×0.60) = 1.36. If ρ = 0.40, N_eff = 1.67. The sensitivity of the N_eff calculation to the assumed correlation is not discussed, despite the correlation range spanning 0.25–0.75 across the stated pairs.

**Required empirical validation method:** Compute realized IC correlations across the same signal type at 4H, 1D, 1W on the target universe, using at least 3 years of historical data. Until this is done, the N_eff improvement from 1W is unverified.

---

### 3.4 1W Crisis Lag Acknowledgment

**Valid — correctly stated.**

Section B5 correctly identifies that 1W regime signals lag sudden-onset crises by 1–2 weeks and quantifies the DD cost: "at 12% annual portfolio vol, 2 weeks unhedged exposure contributes 1.2–2.4% additional DD." This is a correct and properly reasoned calculation. The cost-benefit framing for this tradeoff is the best quantitative reasoning in the document. No flag.

---

### 3.5 Vol-Trigger vs. Correlation-Trigger Conflation

**Rating: Weakly Supported**

Section B5 and E2 derive false-trigger reduction benefits from 1W smoothing. The analysis conflates two distinct trigger types:
- Vol-spike false triggers (single-session vol events that resolve within a week)
- Correlation-spike false triggers (pairwise ρ events that may persist for multiple weeks)

The 1W smoothing benefit applies primarily to vol-spike triggers, whose half-life is typically under a week. Correlation spikes in risk-off events often persist for 2–6 weeks, meaning 1W smoothing does not prevent them — it delays their detection by 1 week. The 50–70% reduction claim may hold for vol triggers but is overstated for correlation-based deleveraging triggers.

---

## SECTION 4 — SHORT IMPLEMENTATION ASSUMPTIONS

---

### 4.1 Short-Side IC Assumption

**Rating: Hidden assumption — Not Defensible**

IC = 0.04 is assumed for the short side without justification. This is the same IC assumed for long-side signals, but short-side IC is structurally lower on liquid assets:
- Short interest in top-4-per-sector liquid assets is typically low, reducing information asymmetry available to short sellers
- Short signals in crypto face squeeze risk that creates idiosyncratic noise uncorrelated with fundamental signal quality
- Post-decline mean reversion in liquid assets is faster than post-rally momentum, reducing the persistence of short signals

An IC of 0.02–0.03 on the short side would halve the short-side FLAM contribution before accounting for the formula error in 1.3.

---

### 4.2 Crypto Perpetual Funding Rate Model

**Rating: Not Defensible — material understatement**

Claim: "short-side implementation costs... add 0.5–2.0% annual drag on short positions."
Claim in C2: "funding rates in bull markets can run 0.1–0.5% per 8-hour period (73–365% annualized)."

**Inconsistency:** The base case cost model uses 0.5–2.0% annual. The tail risk section acknowledges 73–365% annualized scenarios. The LS-4 exit trigger fires at 0.05%/8hr ≈ 220% annualized. But in the regime before reaching 220% — say, 10–50% annualized funding (not unusual in 2020–2021 crypto bull markets) — the system accumulates funding costs without triggering the exit rule.

If 50% of the short book is in crypto perpetuals with average funding of 8% annualized (conservative for any period with sustained bullish crypto sentiment), and 30% of the portfolio is short: funding drag = 0.15 × 8% = 1.2% NAV annually from crypto alone, before equity borrow costs. Total cost drag reaches 1.5–2.5% NAV, implying a Sharpe cost of 0.12–0.21 units at 12% vol. This exceeds the entire expected Sharpe benefit from short positions (+0.04–0.10).

**The net expected value of crypto perpetual shorts under realistic funding scenarios may be negative.** This is not analyzed.

---

### 4.3 Stop-Loss Design vs. Crypto Volatility

**Rating: Not Defensible — order-of-magnitude error in turnover estimate**

Claim (LS-3): "Short positions: maximum 4% adverse move from entry before stop-loss."
Claim (C4): "Estimated additional turnover from short positions: 0.3–0.8 round trips per asset per month."

**The 4% stop-loss combined with crypto asset daily volatility is incompatible with the turnover estimate.**

Top-4 liquid crypto assets have daily volatility of 2–4%. A random walk with 3% daily vol will touch a 4% threshold within 2 days on average via first-passage time: E[τ] ≈ (4/3)² ≈ 1.78 days. This implies approximately 10–15 stop-loss triggers per month per actively-held short position.

At 5 average active short positions: 50–75 stop events per month × round-trip cost 0.25% × average 5% position = 0.625–0.94% NAV/month in stop-loss-triggered turnover costs alone. Annualized: 7.5–11.3% NAV. This would completely eliminate any positive Sharpe contribution from short positions.

The 0.3–0.8 RT/month estimate is off by a factor of 10–30 for any crypto short position held with a 4% hard stop in an asset with 3% daily vol.

Either the stop-loss needs to be wider (10–15%) for crypto shorts, or the turnover estimate needs to be revised by an order of magnitude, or crypto shorts require separate treatment with a distinct stop-loss model. The document proposes none of these.

---

### 4.4 Short-Side Complexity: Equity vs. Crypto

**Partially addressed — basis risk omitted**

The document correctly identifies that equity borrow and crypto perpetual funding are different implementation problems and sequences them appropriately. However, it does not address basis risk in crypto perpetuals: the perpetual contract price can deviate materially from spot price during stress events, creating additional P&L variance not captured in OHLCV backtests. This is a silent cost that does not appear in the cost model or DD analysis.

---

## SECTION 5 — STRUCTURAL INTEGRITY

---

### 5.1 Regime Signal Proliferation — Violation of Single Authoritative Regime Principle

**Rating: Structural Fragility**

The v2 architecture established a "single authoritative regime signal" requirement to prevent definitional drift across layers. V3 introduces:
- 1W regime overlay (weekly update, regime state)
- Daily correlation trigger (ρ > 0.55, deleveraging)
- Hard 12% DD circuit breaker (daily)
- LS-4 funding rate exit (per 8-hour funding window)

This is four regime-adjacent signals operating on four different time frequencies with no specified conflict resolution protocol. During a volatile week where the 1W regime says "trending, maintain allocation," the daily ρ trigger fires, the 12% circuit breaker is not yet triggered, and LS-4 is not triggered — the document does not specify what the portfolio layer does.

The "single authoritative regime signal" architectural principle from v2 is functionally abandoned in v3. This is not acknowledged.

---

### 5.2 Multiplicity Overfitting Surface

**Rating: Underdefined**

The document requires Harvey-Liu haircut, trial count logging, and Deflated Sharpe for the main skill evaluation. Short signals are a new dimension not previously in the evaluation matrix. If the developer tests 15 short-signal specifications before selecting 5 for inclusion, the effective trial count for multiplicity correction expands to include all 15 trials. The document specifies how to handle multiplicity for the long-side skill library but is silent on the short-side development search space.

---

### 5.3 Kill Criterion K4 — Insufficient Statistical Power

**Rating: Not Defensible as a kill criterion**

Kill K4: "Short-side P&L is negative in aggregate after 12 months of short positions being active."

With ~5 short positions per month, 12 months gives approximately 60 short-side trades. The expected t-statistic for a strategy with IC = 0.04 on 60 observations: t = IC × sqrt(60) ≈ 0.31. The threshold for rejecting zero IC at p < 0.10 (one-tailed) is t ≈ 1.30. We cannot reject the null.

For a marginally positive short strategy (IC = 0.02, Sharpe ≈ 0.15), P(aggregate P&L < 0 over 12 months) ≈ 44%. This means a genuinely positive short strategy triggers K4 prematurely with near-coin-flip probability.

K4 as written requires either: (a) a minimum t-statistic threshold instead of a sign-based threshold, (b) a longer evaluation window (24 months), or (c) a Bayesian posterior probability threshold.

---

### 5.4 Maintenance Burden Arithmetic

**Inconsistency confirmed:**

Section G1 table: V2 base maintenance = 9–17 hrs/month.
Section G1 narrative: "Combined with v2's existing maintenance estimate of 15–40 hours/month."

9–17 + 7.5–13.5 = 16.5–30.5. The narrative then states 24–71 hrs/month. The 71-hour upper bound is not derivable from the numbers in the table. Either the table is incomplete or the narrative uses a different v2 baseline. The inconsistency is material: 30.5 hrs/month vs. 71 hrs/month is the difference between "manageable with full-time work" and "impossible even at full-time." If the 71-hour figure is correct, it must be derived explicitly. The current state allows the reader to accept either number as authoritative.

---

### 5.5 SimBroker Circular Bootstrap Problem

**Rating: Structural gap — not addressed**

Kill K6 requires SimBroker short-cost model to be validated against paper trading within 20% of realized costs. But paper trading requires running the live system, which requires a validated SimBroker to verify signals are being generated correctly.

The document says "validate against paper trading" without specifying the bootstrap sequence. During Era 1, before any paper trading data exists, the SimBroker cost model cannot be validated against realized costs. The document does not address how to handle this gap.

---

## SECTION 6 — FINAL AUDIT VERDICT

---

### Classification

**Mildly Overconfident + Quantitatively Loose**

The structural architecture is sound. The sequencing logic is correct. The non-negotiables (four-stream P&L, gross ≤ 1, sequential implementation) are appropriate. The quantitative supporting layer contains a formula error, circular estimates, an incompatible stop-loss design, and a kill criterion with insufficient statistical power. The document is suitable as an architectural guideline but not as a quantitative reference for evaluating expected value of the extensions.

---

### 5 Strongest Components

1. **Non-negotiable 3 — Four-stream P&L attribution.** Requiring separate accounting for long P&L, short P&L, borrow/funding cost P&L, and treasury P&L is the single most important structural control in the document. It prevents alpha laundering through treasury yield blending.

2. **Sequential implementation (Non-negotiable 1).** Long-only baseline → 1W validation → equity shorts → crypto perpetual shorts is logically correct and represents the minimum viable attribution chain.

3. **1W as regime overlay only (B3, B6).** Restricting 1W to regime routing and avoiding a third full skill tier is correct scope discipline. This decision prevents ~20 additional skill instances from entering the evaluation matrix prematurely.

4. **1W crisis-lag tradeoff (B5).** The acknowledgment that 1W regime signals lag sudden-onset crises by 1–2 weeks, combined with explicit preservation of the daily 12% circuit breaker, is honest and correctly reasoned. The dual-layer design (slow weekly regime + fast daily stop) is the best quantitative reasoning in the document.

5. **Cut C3 — equity shorts before crypto shorts (G3).** Staging the short implementation by asset class is the correct risk management response to the heterogeneity between equity borrow and crypto perpetual mechanics.

---

### 5 Weakest Components

1. **FLAM application (C1).** The +0.31 gross Sharpe delta claim from short positions results from applying the Fundamental Law to the short sleeve in isolation rather than computing the marginal contribution to the existing long portfolio. The correct marginal calculation yields approximately +0.07 gross. The error inflates the perceived theoretical headroom for the short extension by ~4.4×.

2. **Combined Sharpe delta arithmetic (A3).** +0.04–0.10 combined from two extensions whose individual estimates sum to +0.07–0.18 has no derivation. An unexplained 40–60% discount is applied without justification or interaction term.

3. **Stop-loss design vs. crypto vol (LS-3 + C4).** The 4% hard stop combined with 2–4% daily crypto vol implies turnover of 10–15 stop events per month per crypto short, not 0.3–0.8 RT/month. The turnover estimate is wrong by one order of magnitude. This error propagates through the cost model and net Sharpe delta.

4. **DD probability table (F4).** Claiming P(DD > 20%) shifts from 35% to 25–28% as a result of these extensions is false precision over an unmodeled baseline. Uncertainty on these numbers is ±10–15 pp, making the 7–10 pp claimed improvement statistically indistinguishable from noise.

5. **Kill K4 statistical power.** Negative aggregate short-P&L after 12 months as a kill criterion has a ~44% probability of triggering prematurely on a marginally positive strategy. This criterion kills a working short book approximately as often as it kills a non-working one.

---

### 3 Mandatory Corrections

**Correction 1: Restate the FLAM derivation (C1) or remove it.**
Either derive the incremental Sharpe from short positions using the marginal FLAM formula — `IC × [sqrt(BR_long + BR_short) − sqrt(BR_long)]` with explicitly stated IC_short and BR assumptions — or remove the +0.31 gross figure entirely and state the net delta (+0.04–0.10) as a calibrated estimate without the intermediate step. The current intermediate step is a formula error that will cascade into wrong intuitions downstream.

**Correction 2: Redesign Kill K4 around a t-statistic threshold.**
Replace "negative aggregate P&L after 12 months" with: "t-statistic of short-side Sharpe < 0.5 after 18 months (minimum 90 short-side trades)" or equivalent Bayesian posterior below a defined threshold. The current sign-based criterion has a ~44% false-kill rate on marginally positive strategies.

**Correction 3: Replace the 4% short stop-loss for crypto with asset-class-specific stops.**
For equities with daily vol 0.8–1.5%, a 4% stop implies 3–5 trading days expected holding — reasonable. For crypto assets with daily vol 2–4%, the same 4% stop implies 1–2 days expected holding, generating stop-driven turnover that eliminates the expected value of the position. Crypto short positions require either a wider stop (10–15% to allow multi-week holding), vol-scaled trailing stops, or an explicit acknowledgment that crypto short positions are high-turnover instruments with a correspondingly revised cost model. The current LS-3 control as written is internally inconsistent with the universe composition.

---

### 3 Optional Refinements

**Refinement 1: Specify conflict resolution protocol for the four regime-adjacent signals.**
Define a strict precedence hierarchy: which signal overrides which when they conflict. This restores the "single authoritative regime signal" principle in a multi-layer system. Proposed hierarchy: hard DD circuit breaker > LS-4 funding exit > daily correlation trigger > weekly regime state. Any deviation from this precedence order must be explicitly justified.

**Refinement 2: Provide empirical bounds on time-scale IC correlations.**
The cross-timeframe correlation estimates (ρ(4H,1D) = 0.55–0.75, etc.) drive N_eff calculations throughout the document. Before implementing 1W, compute these correlations empirically on a representative subset of the target universe using available historical data. This is a one-time calculation that transforms the most sensitive uncited assumption into a measured parameter.

**Refinement 3: Resolve the maintenance burden arithmetic.**
Derive the 71-hour upper bound explicitly from component estimates, or revise it downward to 30.5 hours (derivable from the G1 table). The discrepancy changes the conclusion about solo feasibility and must not be left ambiguous. At 30.5 hrs/month the conclusion is "manageable at full-time"; at 71 hrs/month the conclusion is "exceeds part-time capacity." These have different implications for the era timeline.

---

### Go / Conditional Go / No-Go

**Conditional Go — with conditions on the mandatory corrections, not just the implementation sequence.**

The architecture is conceptually sound and the sequencing is correct. The extensions are appropriate in scope. The non-negotiable constraints are the right constraints.

However, the document cannot serve as a credible quantitative reference until:
1. The FLAM error is corrected or the intermediate step removed
2. The stop-loss design is reconciled with crypto asset volatility, with a revised cost model
3. K4 is redesigned with statistical power sufficient to distinguish signal from noise

Proceeding under the current v3 quantitative layer means building a short-position cost model that is underestimated by 1–3× and implementing a kill criterion that terminates the short extension prematurely with near-coin-flip probability.

**The structural architecture: Conditional Go.**
**The quantitative supporting layer as written: Not ready.**

---

*Document Version: 4.0 | Audit Date: 2026-03-02 | Audits: Strategic Architecture Review v3.0*
*Next action: Apply mandatory corrections to v3 quantitative claims before v3 extensions enter active scope*
