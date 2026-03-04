# Entropy Protocol — Design Decision History

**Version:** 1.0
**Last updated:** 2026-03-04
**Purpose:** Explain why current constraints exist. Document the sequence of design decisions from initial concept to v5 charter. Prevent re-litigation of resolved questions.

This document is the **Why** layer. It does not define current rules — `PROTOCOL_SPEC.md` does that. It explains the reasoning behind them.

---

## Reading This Document

Each section follows the same pattern:
- **Initial position** (what was assumed or proposed)
- **Challenge** (what stress-testing found)
- **Resolution** (what was adopted and why)
- **Current rule** (pointer to the authoritative location)

Sections are ordered by when the design question was resolved, not by importance.

Archive documents that contain the full reasoning are referenced as `[archive/filename]`.

---

## 1. Evaluation Engine First (v1 → v5 unchanged)

**Initial position:** Build skills and agents, add evaluation later.

**Challenge (v1 review):** Every downstream decision — which skills survive, whether the insight layer adds value, whether regime detection helps — depends on having a trustworthy evaluation harness. Without it, all results are unvalidated. The v1 review identified this as the single highest-leverage architectural decision: "Ship the walk-forward evaluation engine before any signal development."

**Resolution:** Phase 0 is a prerequisite for all other phases. No signal receives an OOS evaluation label before Phase 0 exit criteria are met. This is frozen in NN-3.

**Current rule:** `PROTOCOL_SPEC.md` NN-3, Phase 0 section.

---

## 2. Net Sharpe Target Calibration (v1 → v2 correction)

**Initial position (v1):** Net Sharpe base case of ~0.45 for the mature system.

**Challenge (v2 correction):** The 0.45 estimate implicitly assumed above-median signal design quality, competent portfolio construction from Era 2, and disciplined turnover control — simultaneously. For a solo team in a research lab phase, the joint probability of achieving all three is lower than the individual probabilities imply. The estimate was anchored to the upper literature range without accounting for execution risk.

**Resolution:** Base case revised to 0.28–0.42 net Sharpe. Kill criterion set at 0.28 (not 0.35 or 0.40). Success probability revised from 30–40% to 20–32% at 18 months.

**Why this matters:** Planning around 0.45 would have created a false floor for development decisions. At 0.28–0.42, the system is only viable as a CAF (not a Niche Alpha Engine), which changes the operational model — treasury yield becomes essential to the economic case.

**Current rule:** `PROTOCOL_SPEC.md` Section A (performance context), K1 kill criterion.

---

## 3. Factor Collapse Is the Primary Architectural Risk (v1 → v2)

**Initial position:** 12–18 skills on 20 assets creates meaningful diversification.

**Challenge (v1 review):** On 20 liquid, cross-correlated assets, 12–18 skills will statistically consolidate into 3–5 latent factors under most market regimes. The "skill diversity" narrative is almost certainly an illusion without aggressive decorrelation enforcement at the portfolio layer.

**Challenge (v2 correction):** The four proposed controls (exposure budgeting, correlation clustering, DR monitoring, regime gating) are correct in theory but each requires the evaluation engine to already be functioning, the portfolio layer to be stable, and the team to have bandwidth to maintain them simultaneously. Solo execution cannot reliably implement all four.

**Resolution:**
- Skill count reduced to 5–6 base skills (not 12–18)
- Factor controls implemented sequentially, starting with the two most tractable: DR monitoring + correlation clustering
- K3 kill criterion set at N_eff ≤ 2 after 3+ months of controls

**Current rule:** `PROTOCOL_SPEC.md` NN (skill count constraint), Phase 1 K3 criterion.

---

## 4. Treasury Layer Separation (v2 → v5 permanent)

**Initial position (v1):** Treasury yield not discussed.

**Challenge (v2):** The economic case for the system at $100k AUM depends critically on whether treasury yield on idle capital is included in the performance metric. Blending trading P&L and treasury P&L creates a system that can "survive" on yield alone while trading alpha is zero — which defeats the purpose.

**Resolution:** Four-stream P&L attribution is permanently non-negotiable. Stream (d) (treasury) is NEVER included in Net Sharpe. Treasury activates no earlier than Phase 5 (after Phase 1 exit criteria met + 3 months live capital). K5 kill criterion triggers if treasury yield exceeds 60% of total return in any 12-month period.

**Why this is frozen:** The four-stream rule is the primary protection against misclassifying a treasury-yield system as a trading-alpha system. Removing it would invalidate all performance comparisons.

**Current rule:** `PROTOCOL_SPEC.md` NN-2, Phase 5, K5.

---

## 5. Single Authoritative Regime Signal vs Layered Hierarchy (v2 → v5)

**Initial position (v2):** A "single authoritative regime signal" principle — prevent definitional drift across layers.

**Challenge (v3 extension):** The architecture naturally developed four regime-adjacent signals operating on incompatible time horizons: 12% DD circuit breaker, 1W regime overlay, daily correlation trigger, crypto funding exit. Collapsing these into one signal would force them to share a time horizon they don't have, destroying their individual utility.

**Challenge (v4 audit):** v3 introduced these four signals with no conflict resolution protocol, de facto abandoning the v2 principle without acknowledging it. When two signals conflict, there is no defined behavior.

**Resolution:** Replace the v2 single-signal principle with a layered precedence hierarchy (P1–P4). The v2 goal (preventing definitional drift) is preserved through explicit ordering with documented conflict resolution rules and recovery thresholds. Higher priority always overrides; no multiplicative combination; explicit hysteresis for recovery.

**Why P1 > P2 > P3 > P4:**
- P1 (DD breaker) operates on realized portfolio P&L — the most direct measure of system health
- P2 (funding exit) is asset-class-specific and must supersede routing decisions
- P3 (correlation trigger) affects the entire book and supersedes overlay decisions
- P4 (1W overlay) is a routing tool, not a risk rule

**Current rule:** `PROTOCOL_SPEC.md` Section D, `CHARTER.md` Section D.

---

## 6. Short Position IC Assumption (v3 assumption → v4 correction)

**Initial position (v3):** IC_short = IC_long = 0.04, used as the default working prior.

**Challenge (v4 audit):** This assumption was hidden and unsupported. Liquid equity shorts face squeeze noise, higher transaction costs, and funding drag that long positions do not. Using IC_long as the default for shorts creates systematically optimistic projections.

**Resolution:** Working prior for IC_short set explicitly at 0.02–0.03. IC_short > 0.04 is treated as suspect and requires a 0.015 haircut before reporting. IC_long and IC_short are never conflated.

**Why this matters for FLAM:** The incorrect IC assumption produced a spurious +0.31 gross Sharpe intermediate step for the short extension. The corrected FLAM derivation yields +0.046 gross marginal contribution, with net delta +0.01–0.05 after costs. All planning that assumed +0.04–0.10 as a floor must be updated.

**Current rule:** `PROTOCOL_SPEC.md` Phase 3 (IC_short assumption section), CHARTER.md Correction 1.

---

## 7. Kill Criterion K4: From Sign-Based to t-Statistic (v3 → v4 correction)

**Initial position (v3):** K4 triggered if short-side P&L is negative in aggregate after 12 months.

**Challenge (v4 audit):** At IC_short = 0.025 and 60 trades, the expected t-statistic is ~0.19 — well below any significance threshold. The probability of false-killing a marginally positive strategy (P(false kill | IC=0.025) ≈ 44%) makes this criterion nearly equivalent to a coin flip. It provides no information.

**Resolution:** K4 redesigned as: "Short-side t-statistic < 0.5 after 18 months AND ≥90 completed short-side trades." False-kill probability acknowledged at ~60% (at IC=0.025, 90 trades, expected t ≈ 0.24). This is accepted as a screening threshold, not a statistical test. Its function is to terminate a non-working short book early enough to redirect development capacity. A properly powered test would require ~1000 short trades — incompatible with the timeline.

**Why the deliberate tradeoff is acceptable:** The cost of false-killing the short extension is losing the +0.01–0.05 net Sharpe delta. The cost of continuing a dead short extension is 18 months of wasted development capacity. The asymmetry favors erring toward rejection.

**Current rule:** `PROTOCOL_SPEC.md` Phase 3, K4 definition and known limitation note.

---

## 8. Stop-Loss Asset-Class Specificity (v3 assumption → v4 correction)

**Initial position (v3):** 4% hard stop for all short positions.

**Challenge (v4 audit):** For crypto assets with daily vol of 2–4%, a 4% hard stop implies expected time-to-first-passage ≈ 1.8 days. This produces ~10–15 stop events per month per crypto short position. Turnover cost alone: 5 positions × 12 stop events/month × 0.05% fee × 4% avg weight ≈ 1.2% NAV/month = 14.4% NAV/year. This eliminates all expected short-side alpha before any edge is computed.

**Resolution:** Stop models split by asset class. Equity shorts: 4–6% hard stop. Crypto perpetual shorts: 12–18% or 3× 5-day realized ATR (whichever is wider). SimBroker must implement both models before Phase 3 paper trading begins. Running Phase 3 with a uniform 4% stop contaminates the cost evaluation.

**Why uniform stops fail for crypto:** The problem is not risk tolerance; it is that the stop must exceed the asset's noise level to have non-trivial holding time. A stop set inside the noise band generates maximum turnover with zero signal value.

**Current rule:** `PROTOCOL_SPEC.md` NN-6, Phase 3, Phase 4; `CHARTER.md` Correction 3.

---

## 9. Phase 4 (Crypto Perp Shorts) Expected Value (v3 → v4 → v5)

**Initial position (v3):** Phase 4 included as a committed phase with positive EV assumption.

**Challenge (v4 audit):** In any sustained bull crypto environment, perpetual funding rates average 15% or more annualized. With 30% short book / 50% in crypto perps:
```
Funding drag = 0.30 × 0.50 × 15% = 2.25% NAV/year
```
Corrected FLAM marginal contribution at IC_short = 0.025: ~0.55% additional return. Funding drag (2.25%) exceeds expected gross benefit (0.55%). Net EV is negative in this scenario.

**Resolution:** Phase 4 base planning assumption changed to "bypassed." Phase 4 is documented as a conditional option available after Phase 3 validation. It is not on the active roadmap. The P4K1 kill criterion (funding drag > 2.5% NAV trailing 3mo) is included for evaluation if Phase 4 is entered.

**Why not remove Phase 4 entirely:** The expected value depends on realized funding rates, which vary with market regime. In non-bull crypto environments, the case may be positive. Documenting Phase 4 as a conditional option preserves the decision point without committing to it.

**Current rule:** `PROTOCOL_SPEC.md` Phase 4 (optional header), `CHARTER.md` Deferred 1.

---

## 10. Hypothesis Acceleration Track (v5 addition)

**Initial position (pre-v5):** No structured mechanism for early learning during Phase 0.

**Challenge:** Phase 1 requires ≥15 months OOS before actionable results. Waiting with no feedback loop is demotivating and wasteful. Paper trading can generate early signals if hypotheses are properly scoped and separated from the main evaluation path.

**Resolution:** Hypothesis Acceleration Track (AT) formalized with strict constraints:
- Runs in parallel with Phase 0 only. Paper-only.
- AT results labeled "AT-[ID]" — never "OOS"
- Cannot substitute for Phase 1 OOS evaluation
- Promotion requires passing the full Phase 1 protocol
- Pre-registration required before any data examined
- Influencer-derived hypotheses (AT-INF) require 60-day embargo, historical base rate pre-check, and separate tracking

**What it can and cannot validate:** At 2–3 months, AT can screen exit overlays and stop variants for plausibility. It cannot validate net Sharpe, multi-regime robustness, or any kill criterion in either direction.

**Current rule:** `PROTOCOL_SPEC.md` Hypothesis Acceleration Track section.

---

## 11. CCA Role Constraint (v1 → v5 unchanged)

**Initial position (v1):** CCA described as a high-leverage component with regime classification authority.

**Challenge (v1 review):** "The CCA is the highest-leverage component and the highest-risk single point of failure. Its regime classification accuracy directly gates the value of every downstream component."

**Resolution (v2 + v5):** CCA limited to a research dashboard function. No live portfolio influence until:
- Era 4 minimum
- Phase 1–3 validated
- ≥300 resolved InsightHypothesis objects with outcome tracking

This is a multi-year data accumulation requirement. CCA development during Era 1–3 is explicitly deferred.

**Why:** CCA influence on portfolio decisions is only justified if its InsightHypothesis scoring is calibrated on sufficient historical data. Deploying CCA influence earlier creates unverifiable regime classification risk. The cost of deferral (lost potential signal) is lower than the cost of acting on miscalibrated CCA output.

**Current rule:** `PROTOCOL_SPEC.md` Out of Scope section, `CHARTER.md` Deferred 2.

---

## Summary: Decisions That Are Closed

The following design questions have been resolved and are not subject to re-litigation without a charter-level review:

| Question | Resolution | Rule |
|---|---|---|
| Evaluation engine timing | Phase 0, before all signal development | NN-3 |
| Net Sharpe target | 0.28–0.42 base; 0.28 kill floor | K1 |
| Skill count | 5–6 maximum | NN |
| P&L attribution structure | Four streams, permanently separated | NN-2 |
| Regime governance | P1–P4 hierarchy with precedence | Section D |
| Short IC assumption | 0.02–0.03 working prior; 0.04 treated as suspect | Phase 3 |
| K4 definition | t-stat < 0.5 after 18mo/90 trades | K4 |
| Stop-loss by asset class | Equity 4–6%; Crypto 12–18% or 3×ATR | NN-6 |
| Phase 4 status | Bypassed by default | Phase 4 |
| CCA influence timing | Deferred to Era 4 + 300 resolved hypotheses | Deferred 2 |
