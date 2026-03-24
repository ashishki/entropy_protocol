# Feasibility and Structural Validation of a Portfolio-Layer Alpha System

## Constraint-derived implications

Your v2 stress-test document explicitly lowers the project’s “reasonable” expectation to a **0.30–0.40 net Sharpe base case**, and frames the main threats as (i) **factor collapse / redundancy**, (ii) **solo execution bandwidth**, and (iii) the fact that **≤20% max drawdown is not an emergent property**—it must be structurally enforced. fileciteturn0file0L25-L44

Two implications are mathematically load-bearing:

First, a **0.30–0.40 net Sharpe** sits in the zone where **selection bias and multiple testing** can dominate perceived results unless you formalize trials attempted, leakage controls, and a correction framework. fileciteturn0file0L54-L66 citeturn1view0turn12view0turn15view2turn15view1

Second, because you are constrained to **20 liquid assets** and regard the **portfolio layer as the primary engine**, your “true” breadth depends less on the count of signals/skills and more on (a) how independent strategy P&Ls really are and (b) how aggressively you avoid correlation spikes collapsing the effective number of bets. fileciteturn0file0L40-L44L132-L155 citeturn14view2turn15view0turn14view1

The v2 document’s own internal logic already hints at the likely end-state: **“Research Lab → Capital Allocation Framework (not Niche Alpha Engine)”**, i.e., modest trading Sharpe plus explicit risk control plus treasury yield with *separately reported* accounting. fileciteturn0file0L403-L431

## Pretraining and leakage-resistant evaluation design

### What “pretraining agents on historical data” can realistically mean

In systematic trading, “pretraining” is only defensible if it is interpreted as:

A **one-time offline calibration** of *stable, low-degree-of-freedom* components (risk mapping, portfolio construction primitives, cost model priors) using long history, followed by **freezing** those components except for scheduled, explicitly governed updates.

If “pretraining” instead means repeatedly optimizing many knobs to maximize historical performance, you are doing specification search—in which case the correct question is not “what Sharpe did I get?” but “how many trials did I implicitly run and what is the probability the reported Sharpe is inflated?” citeturn12view0turn1view0turn10view3turn15view2

This distinction is not semantic: entity["people","Halbert White","econometrician uc sd"] formalizes that re-using a dataset for model selection creates *data-snooping risk*, where good results can arise “just by luck” from extensive search, motivating Reality Check-style methods. citeturn12view0turn12view0

### What should be calibrated offline

Given your architecture (portfolio layer primary, insight layer research-only until validated, ≤20% DD requirement), the offline “pretraining” target should be **risk-and-construction competence**, not signal cleverness. Concretely:

**Cost and execution model priors (SimBroker calibration).**  
Your v2 highlights that cost/model error can shave **0.05–0.15 Sharpe** and produce unexplained live degradation. fileciteturn0file0L59-L64 This is consistent with the more general warning from entity["people","David H. Bailey","mathematician quant finance"] and coauthors: without controlling for search/selection effects, backtests are not reliable evidence. citeturn1view0

**Risk translation layer (signal → position sizing) and “survival” overlays.**  
Because your DD cap is not passive, “pretraining” should establish the mapping from forecast strength to exposure that is robust under volatility clustering and correlation spikes—i.e., the risk layer must be calibrated before you add higher-variance features like regime routing. fileciteturn0file0L93-L123 citeturn15view0turn14view1

**Covariance / correlation estimation method selection.**  
For small universes, covariance estimation error is a first-order failure mode of portfolio optimization. entity["people","Olivier Ledoit","economist uzh"] and entity["people","Michael Wolf","economist uzh"] argue for shrinkage-type approaches because naive sample covariance inflates estimation error in mean-variance optimization. citeturn4view0turn4view1

**Factor redundancy controls chosen for solo feasibility.**  
Your v2 explicitly concludes that factor-collapse controls reduce redundancy but do not solve it, expecting effective N roughly **3–5** after controls and recommending fewer, simpler controls first. fileciteturn0file0L27-L31L133-L155

### What must not be trained (or must be fixed by policy)

To avoid overfitting, the following must be **policy-fixed** or only tuned within coarse, pre-declared ranges—never optimized to maximize Sharpe:

**Drawdown circuit breakers and correlation thresholds.**  
These are *risk appetite and survival parameters*, not alpha parameters. Optimizing them for Sharpe on one history incentivizes “tail-shaping” to the backtest path. Your v2 treats them as load-bearing constraints (dynamic vol targeting, correlation-triggered deleveraging, hard DD stop), which is the correct stance. fileciteturn0file0L107-L121

**Universe membership rules and “skill count” expansion.**  
Selecting assets/skills based on performance is a classic hidden multiple-testing channel; the v2 warns that “feature engineering time is also feature overfitting time” for solo iteration. fileciteturn0file0L62-L66L148-L155

**Regime labeling rules if they can retroactively change.**  
If you allow regime definitions to evolve and then relabel the past, you destroy the integrity of walk-forward results (your v2 explicitly flags this as a debt-accumulation trap). fileciteturn0file0L317-L321

### A robust walk-forward structure for 10+ years

For 4H–1D systems, “more bars” does not equal “more independent samples” because positions, labels, and volatility are autocorrelated. entity["people","Andrew W. Lo","finance professor mit"] shows Sharpe estimation and annualization can be materially distorted by serial correlation, changing confidence intervals and rankings. citeturn2view1

A walk-forward structure that respects regime diversity *and* avoids extreme variance in OOS estimates:

**Outer walk-forward (model selection + deployment simulation)**  
- Training (IS): **4 years**  
- Validation (parameter selection / model choice): **1 year**  
- Test (locked OOS): **1 year**  
- Roll frequency: **annual** (roll forward by 1 year each iteration)

This yields ~5 OOS years across a 10+ year span, producing multiple regime exposures without making each test slice too short to be interpretable.

**Inner loop (within training+validation): leakage-resistant cross-validation**  
Use a *time-series-aware* scheme (purging/embargo where labels overlap, and non-overlapping blocks) to avoid leakage that comes from overlapping holding periods and label horizons. citeturn5search0turn10view3  
If you have many candidate strategies, add a *combinatorial / cross-sectional* perspective—entity["people","Marcos Lopez de Prado","quant researcher cornell"]’s purged CV/CPCV concepts are designed to reduce leakage and produce a distribution of OOS outcomes rather than a single path-dependent estimate. citeturn5search0turn5search8

### Statistical corrections you should treat as mandatory

You are operating in the “selection bias dominates” regime unless you correct. The minimum viable correction stack:

**Deflated Sharpe Ratio / Probabilistic Sharpe framing.**  
Bailey et al. introduce a Deflated Sharpe approach explicitly to correct for (i) selection bias under multiple testing and (ii) non-normality; they argue that the number of trials attempted is information missing from most backtests, making performance claims unreliable without it. citeturn1view0

**Multiple-testing haircuts and/or false-discovery control.**  
entity["people","Campbell R. Harvey","finance professor duke"], entity["people","Yan Liu","finance professor texas a&m"], and entity["people","Heqing Zhu","finance professor univ oklahoma"] provide a framework implying higher significance hurdles in finance due to the “factor zoo,” including the well-known implication that a newly discovered factor should clear a much higher t-stat hurdle than the classical 2.0. citeturn15view1  
Their practical “haircut Sharpe” backtesting framework shows that when annualized Sharpe is **< 0.4**, the implied haircut is “almost always” >50% and sometimes much larger—i.e., marginal Sharpe systems are the ones most punished by multiplicity. citeturn15view2

**Data-snooping tests across strategy families.**  
Reality Check (White) and Superior Predictive Ability (SPA) tests exist specifically for “best-of-many” strategy selection problems. citeturn12view0turn11search1  
Given your solo iteration loop, you should assume you are implicitly doing “best-of-many” unless you hard-limit experimental degrees of freedom. fileciteturn0file0L62-L66

**Backtest-overfitting probability (PBO) reporting.**  
Bailey & López de Prado extend these ideas by defining and estimating the probability of backtest overfitting and discussing minimum track record length ideas. citeturn10view3

## Alpha realism and Sharpe fragility at 4H–1D

### Realistic Sharpe ranges for liquid assets on 4H–1D horizons

Your v2 baseline is already internally anchored: base-case **net Sharpe 0.28–0.42**, pessimistic **0.10–0.25**, optimistic **0.50–0.70**. fileciteturn0file0L70-L76

To sanity-check this against the broader literature, treat cross-asset trend-following as a *best-case upper bound* for scalable, liquid implementations. entity["people","T. J. Moskowitz","finance professor yale"], entity["people","Yao Hua Ooi","quant researcher man group"], and entity["people","Lasse H. Pedersen","finance professor copenhagen"] document statistically significant time-series momentum across futures; their reported gross Sharpe evidence includes an earlier-sample annualized Sharpe around ~1.1 for a diversified trend strategy (context: futures, long history, volatility scaling). citeturn10view0

However, your setting is deliberately harder:
- **Shorter horizon (4H–1D)** generally increases turnover sensitivity and raises the bar on cost modeling. fileciteturn0file0L59-L64  
- **Small universe (20 assets)** reduces breadth and increases factor crowding risk. fileciteturn0file0L65-L66  
- **No leverage beyond 1x** removes the easiest scaling lever; alpha must come from selection + construction, not grossing up. fileciteturn0file0L93-L123

Given these constraints, a defensible realism bracket is:

- **Gross Sharpe (before modeled costs):** ~0.35–0.70 (median ~0.50)  
- **Net Sharpe (after realistic costs + slippage + implementation drift):** ~0.15–0.45 (median ~0.30–0.35)  

The width of this interval is not hand-waving—it is the direct consequence of (i) multiplicity corrections biting hardest in the <0.4 region and (ii) the fragility of small Sharpe to small unmodeled frictions. citeturn15view2turn1view0turn10view3turn2view1

### Why a 0.30–0.40 system is structurally fragile

A 0.35 Sharpe at a 12% annual volatility target implies an expected excess return of roughly **4.2%/yr**. A **single** additional 1%/yr of unmodeled slippage/fees reduces Sharpe by about **0.08** (1% / 12%). This is why your v2 emphasizes SimBroker realism and warns about “unexplained degradation” of ~0.05–0.15 Sharpe from data/cost issues alone. fileciteturn0file0L59-L64

The second fragility is statistical: Sharpe is hard to estimate precisely with only 18–24 months of OOS because returns are autocorrelated and regimes shift. citeturn2view1turn14view1  
This creates a structural trap: if you allow ongoing tuning, you will almost certainly “improve” backtests while reducing true OOS validity—exactly the selection bias problem Bailey et al. warn about. citeturn1view0turn10view3

### Minimum Sharpe to justify operational complexity

There are two thresholds, and mixing them is a category error:

**Threshold for “research continuation.”**  
Net Sharpe **≥0.25–0.30** can justify continued iteration if (a) the evaluation is leakage-resistant and (b) performance is explainable by stable mechanisms rather than path-dependent luck. Your v2 even suggests reconsidering a kill threshold as low as ~0.30 given the revised base case. fileciteturn0file0L29-L34L368-L386

**Threshold for “operationally justified, complexity-bearing trading system.”**  
If you are building a multi-layer architecture with cost models, regime gating, clustering, etc., anything in the **<0.35–0.40** region is in the zone where multiple-testing haircuts are typically severe and where modest friction errors dominate. citeturn15view2turn1view0turn12view0  
So: **≥0.40 net Sharpe** is the minimum level at which complexity has a plausible positive expected value, and **≥0.50** is the level at which you can justify scaling the framework beyond “research lab” on purely quantitative grounds. fileciteturn0file0L403-L431

### Probability of Sharpe degradation in live trading

Given (i) selection bias, (ii) regime shifts, and (iii) implementation slippage, Sharpe degradation from backtest → live is the base case, not the tail case. citeturn1view0turn12view0turn10view3turn2view1

A defensible, skeptical set of probability statements for a solo-research pipeline:

- **P(live net Sharpe < backtest net Sharpe): ~70–85%**  
- **P(degradation ≥0.10 Sharpe): ~50–65%**  
- **P(degradation ≥0.20 Sharpe): ~25–40%**

These are not “universal constants”; they reflect the fact that strategy selection is almost always conditional on past performance, and both White-style data snooping and Bailey-style backtest overfitting frameworks are built precisely to quantify that this conditionality creates inflated in-sample metrics. citeturn12view0turn10view3turn1view0

## Factor collapse: independent factors and effective breadth

### How many independent factors are extractable in a 20-asset universe

Even if your 20 assets span multiple sectors/asset classes, the number of *stable* independent components is usually small because correlations are time-varying and because many apparent correlations are measurement noise.

Random matrix theory work (e.g., Laloux et al.) shows that in large equity universes, the majority of eigenvalues of the empirical correlation matrix often fall inside a “noise band,” implying only a small fraction of eigenvectors carry stable information. citeturn12view2  
Translating that intuition to a 20-asset universe is not “one-to-one,” but the structural conclusion is similar: you should assume **~2–4 robust components** across regimes, perhaps **up to ~5** if your universe is genuinely cross-asset (equities + rates + FX + commodities + crypto) and you explicitly cap exposures. citeturn12view2turn14view1turn15view0

This is consistent with your v2’s internal estimate: even after applying redundancy controls, expect effective N **3–5**, not 6–8. fileciteturn0file0L133-L145

### After clustering and exposure caps, what effective N is plausible

Here you should distinguish:

- **N_assets = 20** (count of instruments)  
- **N_eff_assets** = effective number of *independent risk bets* after correlation spikes  
- **N_eff_strats** = effective number of independent *strategy P&Ls* (skills) after factor redundancy

In bad regimes, correlations rise; this is not conjecture—Longin & Solnik find that correlations increase in bear markets (not bull markets) using tail methods, and Ang & Bekaert explicitly model regimes where correlations/volatility rise in “bad times.” citeturn15view0turn14view1  
Therefore **N_eff_assets is regime-dependent** and can drop sharply in stress.

A realistic planning range (not a promise):
- **Normal regime:** N_eff_assets ≈ 5–10  
- **Stress / macro shock regime:** N_eff_assets ≈ 2–4

This is exactly why your v2 argues that without regime-triggered de-risking, a 20% DD breach becomes a recurring structural exposure. fileciteturn0file0L93-L106

### Is 5–6 independent “skill clusters” achievable

Interpreting “skill cluster” as a distinct P&L stream, 5–6 is only achievable if the average pairwise correlation between skill returns is low.

Using the standard “effective number under equal weighting” approximation  
\[
N_{\text{eff}} \approx \frac{k}{1+(k-1)\rho}
\]
if you have \(k=6\) skills and average correlation \(\rho=0.3\), then \(N_{\text{eff}}\approx 2.4\); if \(\rho=0.5\), \(N_{\text{eff}}\approx 1.7\). This is the practical meaning of factor collapse: you can have “many skills” but only ~2 effective bets. citeturn14view2turn12view2turn15view0

Your v2’s recommendation—start with **5–6 base skills**, not 12–18—is structurally correct under solo constraints precisely because marginal skills tend to be correlated and expensive to maintain. fileciteturn0file0L146-L155L243-L270

### Structural controls that materially reduce redundancy

The controls that genuinely matter (and are solo-implementable) are the ones that (a) reduce estimation error and (b) enforce diversification mechanically:

**Diversification ratio / effective-number monitoring as a constraint, not a dashboard.**  
Choueifaty & Coignard define the diversification ratio explicitly as weighted-average vol divided by portfolio vol, and use it to formulate “most diversified” portfolios in correlated universes. citeturn12view3  
Meucci proposes an “effective number of bets” concept to quantify diversification as exposure to uncorrelated components. citeturn14view2  
If your portfolio layer is the alpha engine, these must become *hard constraints* (e.g., “do not deploy if N_eff < X”), not just reporting.

**Correlation-aware exposure caps (ex-ante gating).**  
Because correlations increase in bear markets, correlation thresholds must reduce gross exposure before DD accelerates. citeturn15view0turn14view1

**Shrinkage / denoising for covariance inputs.**  
Ledoit–Wolf style arguments (and broader RMT work) exist because naive covariance estimates embed noise that optimizers overreact to, harming OOS performance. citeturn4view0turn12view2

### Probability that skill count > 6 adds no real diversification

Under the modest-universe constraint, the skeptical answer is: **high**.

If the average correlation among incremental “skills” is even moderate (ρ ≈ 0.3–0.6), then beyond ~6 skills, additional skills add very little to \(N_{\text{eff}}\) and mostly increase maintenance burden. citeturn14view2turn12view2  
Given your own v2 assessment that effective N after controls is likely **3–5** and that adding skills is high-cost for solo execution, a reasonable probability statement is:

- **P(skill count > 6 adds <0.5 effective bets): ~70–85%**

This is the quantitative justification for the v2 recommendation to launch with 5–6 skills and add only with strong OOS marginal contribution. fileciteturn0file0L146-L155L243-L270

## Portfolio layer as the main engine and drawdown enforcement

### Where Sharpe gains usually come from: signals vs portfolio construction

You cannot manufacture alpha from nothing, but portfolio construction can convert *weak, noisy forecasts* into better realized risk-adjusted performance by:

- controlling exposure to time-varying volatility (volatility timing),
- reducing correlation concentration,
- reducing estimation error and turnover.

Empirically, volatility-managed portfolios (scaling risk down when lagged realized volatility is high) are reported by entity["people","Alan Moreira","finance professor rochester"] and entity["people","Tyler Muir","finance professor ucla"] to increase Sharpe for the market portfolio by about **25%** in their documented results. citeturn10view1  
A 25% Sharpe increase implies +0.10 Sharpe if you start from 0.40—exactly the threshold you asked about.

However, you must treat this as *conditional evidence*, not a law: later work finds many volatility-managed improvements are not statistically significant across broader sets of portfolios, implying that volatility timing is not universally robust. citeturn5search14

Minimum-variance portfolio evidence provides another “portfolio layer matters” datapoint: Clarke et al. report a historical Sharpe of **0.45** for a base-case minimum-variance portfolio versus **0.31** for the market portfolio (long sample, equities), illustrating that construction techniques can shift realized Sharpe meaningfully—*but* in a setting where estimation and turnover are carefully managed. citeturn14view0

The counterweight is crucial: DeMiguel et al. show that many optimized mean–variance variants fail to consistently beat naive 1/N out of sample because estimation error offsets theoretical gains. citeturn7search3  
So portfolio-layer improvements are real **only under strong regularization/constraints and cost control**.

### Conditions under which portfolio layer adds ≥0.10 Sharpe in your setup

Given your constraints (20 assets, 4H–1D, x1 leverage), ≥0.10 Sharpe improvement from the portfolio layer is plausible only if all of the following are true:

**The signals are weak-but-real (not noise).**  
If the base signals have near-zero true IC, portfolio construction cannot “optimize” noise into stable OOS returns; it will overfit. citeturn12view0turn10view3turn15view2

**Volatility and correlation are meaningfully time-varying and your construction reacts fast enough.**  
Moreira & Muir’s mechanism depends on volatility variation not being matched by proportional variation in expected returns; in that case, scaling down in high vol can improve the mean–variance tradeoff. citeturn10view1  
But regime models are fragile; regime-switching frameworks are useful, yet identification/estimation issues are well-known and can become circular if “regime” is inferred from the same performance you optimize. citeturn14view1turn9search7

**Covariance/correlation estimation is shrinkage/robust and turnover-bounded.**  
Otherwise you are in the DeMiguel failure mode: the optimizer “finds” patterns that don’t persist. citeturn7search3turn4view0turn12view2

In practical terms: the portfolio layer can add ≥0.10 Sharpe primarily by *reducing left-tail and volatility blowups* rather than by increasing mean returns. That aligns with your stated objective of max DD ≤20%. fileciteturn0file0L93-L123

### Is regime routing predictive or descriptive

In most trading systems, “regime routing” is **mostly descriptive** (a classifier of current conditions) rather than truly predictive of regime transitions.

But descriptive does not mean useless: volatility timing is explicitly descriptive (uses *lagged* realized vol) and can still improve Sharpe in some documented settings. citeturn10view1turn5search14

The statistical claim you should demand for “predictive regime routing” is stronger: evidence that regime transitions are forecastable with enough lead time to change allocations *before* primary losses occur, and that this survives walk-forward with frozen labels. Your own v2 calls out that regime-conditioned exposure limits can become circular because they require a reliable regime classifier, which is the open research question. fileciteturn0file0L137-L145

### Structural configuration to enforce ≤20% drawdown

Your v2 is already explicit: ≤20% DD is enforceable only with **active structural enforcement**, and without regime-triggered deleveraging, breaches become frequent because correlation collapses diversification during stress. fileciteturn0file0L93-L106

A minimal but mathematically coherent configuration (all of these are “hard rules,” not optimizer outputs):

**Dynamic volatility target with short lag.**  
Adjust exposure using realized volatility with a lag of ~≤5 trading days (v2 requirement). fileciteturn0file0L111-L113

**Correlation-triggered deleveraging.**  
If rolling average pairwise correlation exceeds a threshold (v2 cites **0.55**), cut gross exposure materially (v2 suggests 35–50%). fileciteturn0file0L114-L116  
This is consistent with regime literature showing correlations increase in bear markets. citeturn15view0turn14view1

**Hard drawdown circuit breaker.**  
At ~12% DD from high-water mark, reduce positions and pause new risk adds (v2 requirement). fileciteturn0file0L117-L119

**Stress analog calibration loop.**  
Run historical stress analogs and size down until worst-case DD is bounded (v2 requires ≤22% in stress analog simulations). fileciteturn0file0L120-L121

### How often 20% DD breaches occur without regime-triggered deleveraging

Your v2 provides a concrete frequency argument: with correlation spikes (ρ ≈ 0.7) the portfolio behaves like ~3–4 effective positions and a 20% drawdown becomes much more frequent, estimating ~**21% annual frequency** of reaching 20% DD under stress-like correlation conditions. fileciteturn0file0L101-L106

The direction of this result is supported by broader evidence that correlation increases in bear markets. citeturn15view0turn14view1  
So even if you disagree with the exact “21%” number, the structural verdict stands: **without dynamic de-risking, ≤20% DD is not a credible claim.** fileciteturn0file0L93-L106

## Treasury, solo execution risk, probabilistic outcomes, and hard verdict

### Treasury layer impacts for a 0.30–0.40 base Sharpe system

Your v2 quantifies that if utilization is ~50%, a 3–5% yield on idle capital could add about **1.5–2.5% annual return** on total capital and looks like **+0.06–0.12 Sharpe units** for a 12%-vol portfolio in a naive blended framing. fileciteturn0file0L179-L183

However, structurally:

- If the yield is truly “risk-free,” it should not increase Sharpe *measured properly as excess over the risk-free rate*; it increases absolute return and can improve economic viability. fileciteturn0file0L179-L183  
- If the yield carries tail risk (stablecoin lending / protocol risk), it can reduce survival probability despite improving average return—exactly why the v2 strongly warns against high-risk treasury instruments and calls separate accounting non-negotiable. fileciteturn0file0L188-L193L195-L208L230-L230

#### Yes/No decisions

**Does 3–5% passive yield materially improve long-term survival probability?**  
**Yes, conditionally**: if implemented via genuinely low-risk instruments and kept liquid enough to not interfere with de-risking. It improves economic runway and reduces the “carry cost” of being in cash during risk-off periods. fileciteturn0file0L179-L183L212-L230

**Does it statistically mask weak trading alpha?**  
**Yes.** Your v2 explicitly states this is the most important risk: blended reporting can make a weak or negative-alpha trading engine look “fine.” fileciteturn0file0L195-L208L230-L230

**Should treasury be introduced before or after 12 months of OOS trading validation?**  
**After.** The v2’s sequencing recommendation is unambiguous: establish a clean baseline (trading-only), then activate treasury later, with permanently separate P&L reporting. fileciteturn0file0L222-L230

### Where overfitting and evaluation bias most likely occur in this architecture

Under solo execution, your v2 points out the core structural hazard: iterative feature engineering is iterative backtesting, and without strict discipline you perform “multiple implicit backtests.” fileciteturn0file0L62-L66

The highest-risk loci:

**Overfitting hotspots**
- **Regime routing thresholds and gating logic**, because they affect all allocations and can be tuned to past crises. fileciteturn0file0L137-L145L317-L321  
- **Skill proliferation**, because it expands degrees of freedom and increases correlated noise. fileciteturn0file0L146-L155L243-L245  
- **Portfolio construction hyperparameters** (risk budgets, correlation constraints) if you optimize them for Sharpe instead of setting them by risk policy. fileciteturn0file0L107-L121L93-L106

**Evaluation bias hotspots**
- Leakage in walk-forward splits (overlapping labels/positions). citeturn5search0turn2view1  
- Silent data issues (“free data” errors, survivorship, timestamp inconsistencies), which your v2 estimates can directly degrade live metrics. fileciteturn0file0L59-L64  
- Cost model optimism, which is structurally indistinguishable from alpha in backtests unless validated. fileciteturn0file0L59-L64L296-L312

### Minimum architecture that preserves statistical integrity

Your own v2 simplification pass is basically the integrity-preserving architecture:

- Data layer + evaluation engine first  
- 5–6 base skills  
- portfolio layer as core engine  
- insight/CCA as dashboard/research only until validated  
- treasury as separate module with separate accounting

This is explicitly recommended as the “30% complexity reduction” architecture suitable for a solo developer. fileciteturn0file0L234-L270

### Probabilistic outcome model

These probabilities are necessarily subjective; I’m anchoring them to (i) your v2 probability estimates and (ii) the statistical difficulty of validating modest Sharpe under multiple testing and regime dependence. fileciteturn0file0L330-L361 citeturn15view2turn1view0turn12view0

**Net Sharpe ≥ 0.35 after 18 months (observed OOS)**  
Estimated probability: **~30%** (range **25–40%**).  
Reason: your v2 defines “success” with Sharpe ≥0.35 and gives **20–32%** at 18 months under stricter criteria (cost validation + DD constraint), so the marginally looser event “Sharpe ≥0.35” should be modestly higher but still constrained by multiplicity and short OOS windows. fileciteturn0file0L330-L353 citeturn15view2turn2view1

**Net Sharpe ≥ 0.50 after 24 months (observed OOS)**  
Estimated probability: **~20%** (range **15–30%**).  
Reason: this is essentially the “optimistic scenario” band in your v2 (0.50–0.70), and your v2 assigns non-trivial probability to the Niche Alpha Engine path by ~30 months, but multiplicity corrections penalize marginal Sharpe systems most and 24 months is still short for confirming 0.50 without overfitting. fileciteturn0file0L70-L76L424-L431 citeturn15view2turn10view3

**Factor collapse limiting effective N ≤ 2 (despite basic controls)**  
Estimated probability: **~35%** (range **25–45%**).  
Reason: your v2 explicitly makes “effective N ≤ 2 after controls” a kill criterion and argues redundancy controls only partially reduce collapse, while regime evidence shows correlations rise in bad times, compressing N_eff. fileciteturn0file0L379-L386L133-L145 citeturn15view0turn14view1turn14view2

**Insight layer adds positive measurable edge (statistically validated, marginal contribution > 0)**  
Estimated probability: **~25%** (range **15–35%**).  
Reason: your v2 repeatedly emphasizes statistical underpowering for early eras and even introduces a kill criterion for negative contribution after a large number of resolved hypotheses, implying the base expectation is “uncertain/likely non-actionable” rather than “likely positive.” fileciteturn0file0L40-L44L387-L390

**System becomes Capital Allocation Framework vs Niche Alpha Engine**  
Estimated probability of **Capital Allocation Framework**: **~55%** (range **45–65%**)  
Estimated probability of **Niche Alpha Engine**: **~30%** (range **20–40%**)  
Reason: your v2 explicitly reclassifies the most probable mature form as a capital allocation engine combining moderate trading alpha + risk controls + treasury yield, and provides probability ranges favoring that path over “pure alpha engine,” especially under solo constraints and modest Sharpe expectations. fileciteturn0file0L403-L431

### Hard verdict

**Classification:** **Capital Allocation Framework**  
(With the explicit caveat that without a rigor-first evaluation engine and frozen walk-forward governance, it degrades into **Statistically Fragile** by construction.) fileciteturn0file0L403-L433L40-L44

**Structural strengths**
- **Correct alpha locus:** portfolio layer treated as the main engine (consistent with both your v2 and broader evidence that construction/risk timing can move Sharpe materially). fileciteturn0file0L40-L44 citeturn10view1turn14view0  
- **Explicit realism on Sharpe and multiplicity risk:** base-case Sharpe reduced and factor-collapse controls treated as only partially effective. fileciteturn0file0L25-L34L133-L145  
- **Separation principle for treasury vs trading P&L:** prevents a common failure mode where yield masks lack of alpha. fileciteturn0file0L195-L208L222-L230

**Structural weaknesses**
- **Validation difficulty at low Sharpe:** 0.30–0.40 sits exactly where multiple-testing haircuts are harsh and OOS confirmation takes long, creating strong temptation to “keep tuning.” citeturn15view2turn1view0turn2view1  
- **Small-universe breadth ceiling:** with 20 assets, correlation spikes can collapse N_eff and neutralize diversification right when you need it most. fileciteturn0file0L93-L106L133-L145 citeturn15view0turn14view1  
- **Solo maintenance gravity:** your v2 estimates 15–40 hours/month of hidden maintenance in Era 2+, which competes directly with research bandwidth and integrity (schema drift, walk-forward management, debugging). fileciteturn0file0L296-L312

**Required corrections**
- **Pre-register degrees of freedom:** explicitly cap the number of variants/parameters you will consider per era, and report trial counts; otherwise backtests are not interpretable. citeturn1view0turn12view0turn15view2  
- **Treat drawdown controls as policy, not optimizable knobs:** dynamic vol targeting + correlation-trigger de-risking + DD circuit breaker must be fixed/rule-based and stress-tested, not Sharpe-optimized. fileciteturn0file0L107-L121  
- **Enforce “few skills, strong construction” until proven otherwise:** start at 5–6 skills maximum; expansion only with clearly measured marginal contribution under walk-forward. fileciteturn0file0L146-L155L243-L270

**Non-negotiable principles**
- **Leakage resistance is the system.** If evaluation is compromised, the project becomes statistically fragile regardless of reported Sharpe. fileciteturn0file0L40-L44L317-L321 citeturn12view0turn5search0  
- **Separate accounting for trading vs treasury forever.** Blended reporting destroys alpha inference. fileciteturn0file0L195-L208L222-L230  
- **Multiplicity corrections are not optional at Sharpe < 0.4.** This is the zone where haircuts are typically >50% and where “50% haircut” heuristics are explicitly called inappropriate. citeturn15view2turn1view0turn15view1