# Entropy Protocol — Architect Brief
**Classification:** Confidential — Onboarding Document
**Filename:** `audience/ARCHITECT_BRIEF.md` (stable)
**Audience:** Senior Systems Architect / CTO
**Version:** 1.2
**Date:** 2026-03-04
**Purpose:** Enable an experienced architect to understand system design, evaluation integrity, and operational viability. Read this before `PROTOCOL_SPEC.md`. Then read `EVOLUTION.md` for design decision history.

This document assumes familiarity with systematic trading concepts at the level of someone who has built or overseen production quant systems. Heavy quant notation is used where precise — trading intuition explanations are omitted.

### Current Hardening Focus (v1.3 Alignment)

The near-term objective is to reduce governance ambiguity, not to expand feature surface:
- deterministic P3 trigger and explicit P1/P3/P4 transition semantics;
- explicit RDL boundary matrix with attestation hooks;
- normalized net Sharpe definition `(a+b+c)` across all reporting tables;
- GE-2/GE-3 bright-line for persistent near-zero weights;
- operational definition of RBE charter-level approval artifact.

---

## A. Architectural Overview

### System Classification

Research Lab (current). Conditional destination: Capital Allocation Framework if Phase 1 exit criteria met after ≥15 months OOS.

### Core Constraint Set

- Gross leverage ≤ 1.0 (hard rule, not a risk limit): |longs| + |shorts| ≤ 100% NAV
- Timeframes: 4H and 1D primary; 1W overlay (Phase 2+, conditional)
- Universe: ~20 liquid assets, top-4 per sector (large-cap equities, crypto majors, commodities, FX)
- Max drawdown: ≤20% enforced structurally, not passively
- Skills (signal generators): 5–6 base, no expansion without OOS marginal Sharpe contribution > 0.05

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Data Layer                                                 │
│  OHLCV ingestion → cleaning → Parquet feature store         │
│  Free sources (MVP); professional sources (later)           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Evaluation Engine (Phase 0 prerequisite)                   │
│  Walk-forward harness | Trial registry | Leakage audit      │
│  SimBroker (cost simulation) | P&L attribution (4-stream)   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Skill Layer (Phase 1+)                                     │
│  5–6 base skills × 2 timeframes × ~20 assets               │
│  Clusters: trend, reversion, vol-regime                     │
│  Short skills added in Phase 3 (substitution, not addition) │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Portfolio Layer (Phase 1+)                                 │
│  Vol targeting | Correlation control | Regime routing       │
│  N_eff monitoring | Weight allocation (gross ≤ 1.0)        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Regime Signal Hierarchy (P1–P4, always active Phase 1+)    │
│  P1: DD circuit breaker | P2: Funding exit (Phase 4+)       │
│  P3: Correlation trigger | P4: Weekly overlay (Phase 2+)    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Pluggable Modules (phase-gated)                            │
│  1W overlay | Equity shorts | Crypto perp shorts (bypassed) │
│  Treasury layer | Exit overlays (via AT)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Insight Layer / CCA (research-only; no live influence)     │
│  Text ingestion | InsightHypothesis objects | Source scoring │
│  Dashboard only until Era 4 + 300+ resolved hypotheses      │
└─────────────────────────────────────────────────────────────┘
```

### Key Data Flows

- Signal → Portfolio Layer → Position targets → SimBroker (fills + costs) → P&L attribution engine → four-stream decomposition
- Regime signals (P1–P4) → Portfolio Layer (override hierarchy)
- Trial registry → Evaluation engine (every run logged before execution)
- AT paper trades → separate track → promotion protocol → Phase 1 queue (not back-merged into OOS results)

### What Is Deliberately Excluded

- No real-time tick data; 4H bars are the minimum granularity
- No execution infrastructure (simulation-only at current stage)
- CCA has no write path to the portfolio layer in any phase until Era 4 conditions are met
- No dynamically-constructed signal combinations; skills are fixed specifications within pre-registered bounds

---

## B. Integrity Controls

### Walk-Forward Harness Design

- Training window: 4 years
- Validation window: 1 year (parameter selection)
- Test window (locked OOS): 1 year
- Roll frequency: annual
- ~5 OOS years across 10+ year span; multiple regime exposures

**Leakage prevention mechanisms:**
- Regime labels computed using only information available at start of each test window (no look-ahead on regime labels)
- Feature normalization parameters (e.g., rolling volatility estimators) use only data through the start of the test window
- Portfolio weights computed from walk-forward calibrated parameters only; no in-sample optimization within the OOS window
- Temporal shuffling test: each feature is shuffled across time; if the shuffled version produces similar or better results, the feature is forward-looking
- Purge/embargo applied to training-validation boundary proportional to maximum holding period to prevent label leakage from overlapping trade horizons

### Trial Registry

- Every signal specification is pre-registered before any data from the evaluation window is examined
- Registry schema includes: AT-ID or Phase-ID, hypothesis statement, entry condition (locked), evaluation metric, threshold, minimum sample, expiry, data hash of the dataset to be used
- Version-locked: no retroactive modification of registered specs
- Trial count visible at all times in evaluation logs
- Harvey-Liu haircut applied at every evaluation report when net Sharpe < 0.40
- Deflated Sharpe reported alongside raw Sharpe

### P&L Attribution Engine (Four-Stream — Non-Negotiable)

Every performance report decomposes into exactly four streams:
- **(a)** Long P&L
- **(b)** Short P&L
- **(c)** Borrow/Funding P&L (equity borrow + crypto perp funding — separated from (b))
- **(d)** Treasury P&L (idle capital yield — separated from trading book entirely)

Net Sharpe = (a)+(b)+(c) only. Stream (d) excluded from all primary metrics. Blending is a kill-criterion-level failure (K5 triggers when (d) > 60% of total in any 12 months).

### Separation of Concerns

- Regime parameters (P1–P4 thresholds) are **policy parameters**: fixed before evaluation, never optimized for Sharpe
- DD circuit breaker threshold (12%), correlation trigger (0.55), funding exit threshold (0.05%/8hr) cannot be modified during an active evaluation window
- CCA has no write path to the portfolio layer — read-only dashboard interface only

### CI Reporting

- Net Sharpe always reported with 68% confidence interval
- CI is computed via canonical method `CI-SR-ACF-v1` with autocorrelation-consistent adjustment
- CI is mandatory uncertainty disclosure; frozen kill thresholds remain unchanged

---

## C. Regime Signal Governance

### Precedence Hierarchy (P1 highest; P4 lowest)

| Priority | Signal | Trigger | Action | Recovery |
|---|---|---|---|---|
| P1 | Hard DD circuit breaker | Realized DD ≥ 12% from HWM | Cut all to 50%; suspend new additions 5 business days | HWM gap < 8% AND ≥5 days |
| P2 | Funding exit (crypto perps) | Perp funding > 0.05%/8hr × ≥3 consecutive windows | Exit all crypto short positions | Funding < 0.03%/8hr × ≥5 windows |
| P3 | Daily correlation trigger | 20-day rolling avg pairwise ρ > 0.55 | Cut gross 35–50% over 3 business days | ρ < 0.45 (hysteresis = 0.10) |
| P4 | Weekly regime overlay | 1W signal state | Adjust skill routing within current exposure budget | Weekly close; no recovery period |

### Conflict Resolution Properties

- Higher priority **always** wins; no blending or averaging across priorities
- Signals do not combine multiplicatively: P3 fires (reduce to 65% gross) → P4 routing applies to the 65% book, not original sizing
- P2 and P3 are active simultaneously: P3 reduction applies to the long book; P2 exits crypto shorts independently
- P1 overrides all: when P1 is active, P4 routing adjustments are moot because gross is already halved

### Recovery Rules (explicit — no implicit clearing)

- P1: Does not clear when price recovers above trigger; requires both condition clearance AND minimum elapsed time
- P2: Recovery threshold (0.03%/8hr) is lower than trigger threshold (0.05%/8hr) — asymmetric hysteresis by design
- P3: Recovery threshold (0.45) is materially lower than trigger (0.55) — 0.10 band prevents rapid cycling

### Regime Label Immutability

Regime labels applied to historical OOS windows are frozen at evaluation time. A recalibration of the 1W signal in Phase 2 does not retroactively change Phase 1 regime labels. All performance reports reference the signal version active at evaluation time. This prevents retroactive improvement of reported performance through regime relabeling — a common implicit failure mode in iterative systems.

### Concurrent State Semantics (Now Explicit)

Nested transitions are now defined at policy level:
- if P1 activates during a P3 ramp, the P3 ramp is paused and resumed after P1 clears;
- P4 updates during P1-active windows are track-only (logged, no exposure effect);
- transition logs must include state before/after and policy hash.

---

## D. Complexity and Maintenance Budget (Solo Constraints)

### Current Scope (Phase 0–1)

The MVP architecture is deliberately constrained:
- 5–6 fixed skills (not 12–18 as in earlier iterations)
- Walk-forward harness: one evaluation framework, no ensemble meta-learner
- Portfolio layer: vol targeting + correlation clustering + N_eff monitoring — 3 controls, not 7
- CCA: read-only, no live portfolio influence — removes the highest-complexity, highest-failure-risk component from the execution path

### Maintenance Budget Estimate

| Phase | Estimated maintenance hrs/month |
|---|---|
| Phase 0–1 | 15–40 hrs (data pipeline, WFO management, schema evolution, debugging) |
| Phase 3–4 (shorts active) | 25–58 hrs (adds 10–18 hrs for short-side borrow tracking, stop management, cost model drift) |

At 80 hrs/month total availability (part-time developer): Phase 3–4 maintenance can consume 31–73% of available time. This is a hard constraint on iteration velocity.

### Hidden Maintenance Surface (Primary Failure Modes)

**Data source drift:** Free APIs change format, rate limits, and historical coverage without notice. Estimate 2–4 hrs/month steady state; 10–20 hrs during a major API change.

**SimBroker calibration drift:** Market microstructure evolves. A cost model calibrated in Phase 0 will drift by Phase 3 without quarterly recalibration (4–8 hrs/cycle).

**Walk-forward window growth:** A full WFO run over 3+ years of data may take 4–8 hrs by Phase 3. This creates incentive to run abbreviated checks that compromise rigor.

**Schema evolution:** Each feature definition change or metric addition requires historical data migration. Estimate 5–15 hrs/change; 2–4 changes/era is realistic.

**"Was working last week" debugging:** Stochastic pipeline failures, silent numerical errors in OOS calculations, and version-induced behavior changes. Estimate 5–10 hrs/month.

### Where Complexity Accumulates Silently

Three locations of inevitable technical debt:

1. **Evaluation engine:** If leakage controls are patched rather than architected correctly from Phase 0, each fix risks introducing new leakage vectors. By Phase 3, a patched harness may be producing unreliable results that have been normalized. Rebuilding is prohibitively expensive at that point. This is the most dangerous failure mode.

2. **Regime signal versioning:** The 1W overlay (Phase 2) and correlation trigger parameters will drift across eras. If historical regime labels are not immutable at evaluation time, Phase 1 performance records become inconsistent with any Phase 2 re-evaluation. The regime signal must be versioned with the same discipline as application code.

3. **Trial registry discipline:** In practice, solo developers test things informally before deciding whether to register them. Every informal test is an implicit trial that inflates the effective multiplicity budget without appearing in the Harvey-Liu count. This is the hardest integrity problem to solve architecturally because it is behavioral, not technical.

---

## E. Risk Register

| # | Risk | Severity | Likelihood | Primary Mitigation | Residual Risk |
|---|---|---|---|---|---|
| R1 | **Factor collapse (N_eff ≤ 2)** despite controls | High | Medium-High (P ≈ 35%) | DR monitoring + correlation clustering as hard constraints (not dashboards); K3 trigger | At k=6 skills, ρ_avg=0.3 → N_eff=2.4; barely above K3 threshold in normal conditions |
| R2 | **Evaluation engine leakage** — silent forward-look in features | High | Medium | Phase 0 temporal shuffling test; mandatory leakage audit checklist; no signal claims OOS label before Phase 0 complete | Any feature added post-Phase 0 must pass same audit; ongoing discipline required |
| R3 | **Cost model underestimation** — especially crypto funding in bull markets | High | Medium-High | Explicit cost table (Section C of master spec); 8-hour funding logging from Phase 4 day 1; K6 trigger at 20% deviation | Base case funding drag (2.25% NAV/year) already exceeds expected short-side gross benefit — Phase 4 EV may be negative |
| R4 | **Trial registry contamination** — informal pre-screening inflates Harvey-Liu budget | High | High (behavioral) | Written policy: any informal test must be logged even if not pursued; AT pre-registration required before examining evaluation window data | No technical enforcement possible; entirely behavioral |
| R5 | **Solo maintenance gravity** — maintenance burden crowds out development | Medium | High | Explicit maintenance budget in planning; Phase 3–4 decision gated on Phase 2 exit criteria; CCA excluded from live path | At 25–58 hrs/month maintenance vs 80 hrs/month availability, forward progress can stall for months |
| R6 | **Regime label retroactive contamination** — 1W signal recalibration changes historical regime assignments | High | Medium | Regime labels frozen at evaluation time (architecture requirement); regime signal versioned separately from skill parameters | Requires explicit version tagging in the evaluation engine; easy to miss during rapid iteration |
| R7 | **SimBroker circular bootstrap** — cannot validate against paper trading before paper trading exists | Medium | Confirmed (structural gap) | Phase 0 validates SimBroker against market bid/ask data directly (≥100 manually verified fills); paper trading supplements but does not bootstrap | Initial validation against bid/ask data is an approximation; first 30 days of paper trading will have unvalidated fills |
| R8 | **AT results bleed into OOS claims** — narrative conflation of "promising AT result" with "validated" | High | Medium-High | Strict labeling ("AT-[ID]" never "OOS"); separate tracking log; AT promotion protocol requires Phase 1 registration as new test | Behavioral; cannot be fully prevented by tooling |
| R9 | **K4 false kill on a working short book** — P(false kill at t < 0.5) ≈ 60% at IC=0.025 | Medium | High (structural; accepted) | K4 acknowledged as screening threshold, not significance test; 60% false-kill probability documented in kill criterion | No fix available at this sample size without waiting ~1000 trades; accepted tradeoff |
| R10 | **Free data quality degradation in live conditions** — 0.05–0.15 Sharpe unit degradation from data issues | High | Medium | SimBroker validation against market bid/ask in Phase 0; data quality monitoring as Phase 0 exit criterion; professional data migration path identified | At 0.10 Sharpe degradation, a 0.32 live system falls below K1 threshold (0.28) — existential risk to project |

---

## F. Security and Operational Concerns (Conceptual)

These are design-level considerations, not implementation recommendations. No production deployment exists at current stage.

### API Keys and Credential Management

- Data provider API keys should never be stored in source code or committed to version control
- Any environment variable or secrets management approach must be documented in the data pipeline spec before Phase 0 is declared complete
- Exchange API keys (Phase 3+ paper trading via broker interface) require explicit scope limitation: read-only for market data, order-limited for paper fills, no withdrawal permissions

### Data Integrity and Reproducibility

- Every evaluation run must be reproducible from a data hash + parameter set + code commit hash
- Raw OHLCV data must be immutable once ingested: no in-place correction of historical data; corrections applied as versioned overlays with explicit timestamps
- The trial registry must log the data hash of the dataset used in each evaluation; this is the primary defense against "same test, different data" contamination

### Audit Trail Requirements

- Walk-forward test results: input parameters, data hash, code version, output metrics — all logged atomically per run
- Kill criterion evaluation: logged with the exact metric value at trigger, not just the binary outcome
- AT hypothesis outcomes: logged at evaluation date with the sample that was evaluated; cannot be retroactively updated

### Reproducibility Risk

- At 4H resolution, bar data from different sources can differ in timestamp convention (UTC vs exchange local, bar-open vs bar-close alignment). If the evaluation engine and paper trading use different timestamp conventions, fills may occur on different bars, creating a systematic evaluation-vs-execution mismatch that is invisible in backtests.
- This should be a checklist item in the Phase 0 leakage audit.

### Operational Risk (Single-Operator)

- There is no redundancy in human oversight. If the primary developer is unavailable, there is no monitoring coverage.
- At minimum, automated alerts for: data pipeline gaps > N hours, DrawDown circuit breaker triggers, WFO job failures.
- Absence of automated alerting is an operational risk even in paper-trading mode — a missed P1 trigger in paper trading creates a false sense of safety about what would happen in live trading.

---

## G. Review Questions for CTO (CTO Question List)

These questions are intended for a structured review session. They are not rhetorical — each has an answer that would change an architecture decision.

### Architecture Brittleness

1. **Evaluation engine as single point of failure:** The entire project's evidentiary claims rest on the walk-forward harness. If a leakage bug is discovered in Phase 3, all prior OOS results are invalidated. What is your recommended approach to unit-testing temporal leakage controls in a WFO harness? Is temporal shuffling sufficient, or are there classes of leakage it cannot detect?

2. **Feature store versioning:** Features used in Phase 1 may need to change in Phase 2 (e.g., a new normalization approach). If the feature store is not versioned, Phase 1 results cannot be reproduced after Phase 2 feature changes. What is the minimum viable feature versioning architecture for a solo developer at this scale?

3. **Trial registry enforcement:** Pre-registration discipline is entirely behavioral — there is no technical mechanism preventing informal pre-screening. Have you seen architectures that partially enforce this (e.g., cryptographically timestamped hypothesis submissions, locked evaluation windows) that are feasible for a solo developer?

4. **Regime signal versioning:** The 1W overlay (Phase 2) adds a new layer to the P4 signal. If P4 parameters are recalibrated, historical regime labels should not change retroactively. How would you architect the regime signal versioning so that a Phase 2 recalibration cannot corrupt Phase 1 regime label records? Is this a database schema problem, a filesystem problem, or both?

5. **SimBroker as the primary cost validator:** The system's kill criteria (K1, K2, K6) are all computed against SimBroker outputs. If SimBroker has a systematic bias (e.g., consistently underestimates slippage in stress), all kill criteria will be miscalibrated in the same direction. What validation architecture would give you confidence in SimBroker cost accuracy beyond the 15%-bid/ask tolerance in Phase 0?

### State Management

6. **Portfolio state across system restarts:** In paper trading, if the system restarts mid-week, what is the correct behavior? Should it reconstruct portfolio state from the trade log, or start fresh? If the former, what is the minimum state that must be persisted and how is consistency guaranteed?

7. **Concurrent signal updates:** 4H bars arrive every 4 hours; 1D bars arrive daily; 1W bars arrive weekly. If a 1D and a 4H signal update occur simultaneously (e.g., at the 4H bar that is also a 1D close), what is the tie-breaking rule, and how is this tested to be consistent in the harness vs. in paper trading?

8. **Regime state machine:** The P1–P4 hierarchy has explicit recovery conditions (hysteresis windows, elapsed time gates). This is a stateful system. Where is the canonical regime state stored, and how is state inconsistency (e.g., P1 "active" in one component but "cleared" in another due to a restart) detected and resolved?

9. **Walk-forward parameter persistence:** Skill parameters are calibrated in the training/validation window and then frozen for the OOS test window. How are calibrated parameters stored and retrieved? If a calibration job fails mid-run, how does the harness detect partial state and avoid running an OOS evaluation against incompletely calibrated parameters?

### Evaluation Contamination Risks

10. **Multiplicity from informal exploration:** The trial registry logs formal tests. But in practice, a developer will examine data informally before deciding whether to register a hypothesis. This pre-screening is not logged but inflates the effective trial count. Is there any architecture pattern — beyond policy — that reduces this risk? For example, locked evaluation datasets that are inaccessible until a hypothesis is pre-registered?

11. **AT-to-OOS boundary enforcement:** AT results must never be combined with OOS results. In practice, both may be stored in the same database or reporting system. What is the minimum schema design that makes accidental combination of AT and OOS results technically difficult rather than just policy-prohibited?

12. **Harvey-Liu haircut automation:** The haircut requires knowing the total trial count across all tests for the same dimension. If different developers (or the same developer in different phases) run tests without a unified registry, the trial count will be incomplete. How would you implement trial count aggregation in a way that is robust to partial registry entries?

### Testability and Observability

13. **WFO harness test coverage:** What is the minimum test suite that would give you reasonable confidence that the walk-forward harness has no leakage? What are the test cases that are hardest to write and most likely to be skipped under solo development pressure?

14. **Cost model observability:** Stream (c) — borrow/funding costs — must be attributed at position level, not portfolio level. At Phase 3 with equity shorts and Phase 4 with crypto perps, stream (c) will have components from two different asset classes with different update frequencies. How would you architect the cost attribution to be auditable at the position level without creating an unmanageable reporting burden?

15. **N_eff monitoring architecture:** The portfolio layer must monitor N_eff continuously to detect K3 (factor collapse). N_eff requires a covariance matrix estimate, which requires a rolling window of skill P&L. What is the minimum viable implementation that gives accurate K3 triggering without introducing a look-ahead bias in the covariance estimate?

### Where to Simplify

16. **Minimum viable Phase 0:** What is the simplest walk-forward harness architecture that satisfies the Phase 0 exit criteria without over-engineering? Specifically: is an annual-roll WFO necessary, or would a simpler expanding-window OOS suffice for Phase 1 at this scale?

17. **Regime signal consolidation:** The four-layer hierarchy (P1–P4) is conceptually sound but adds state management complexity. Is there a simpler architecture that achieves the same conflict resolution properties? For example, could P1 and P3 be unified into a single exposure-reduction rule with different trigger levels?

18. **Portfolio construction complexity vs. value:** The portfolio layer includes vol targeting, correlation control (clustering), N_eff monitoring, and regime routing. For a 5-skill, 20-asset portfolio, is there evidence that this complexity outperforms simpler equal-risk budgeting with a single correlation threshold? What is the minimum portfolio construction that preserves the ≤20% DD guarantee?

19. **Data architecture:** The spec assumes Parquet + PostgreSQL. For a solo developer at Phase 0–1 scale (20 assets, 4H bars, 3–5 years history), is this the right choice? What is the operational cost of maintaining PostgreSQL vs. a pure filesystem-based Parquet store? Where would you draw the boundary between "dataset" (Parquet) and "state" (database)?

### Freeze and Change Control

20. **How to enforce the 6-month freeze:** The master spec declares a 6-month freeze period on non-negotiables. In practice, a solo developer under pressure to show progress will be tempted to make "small" changes to frozen parameters. What mechanisms — beyond documentation — would you recommend to make unauthorized changes detectable after the fact?

21. **Kill criterion as trigger for unfreeze:** The spec allows the freeze to break early if a kill criterion fires. What is the protocol for a borderline kill? For example, if K1 requires net Sharpe < 0.28 and the observed value is 0.285 ± 0.18 CI, the kill criterion is technically not triggered but the CI overlaps zero. How should the architecture handle ambiguous kill criterion evaluations?

22. **Change log discipline:** Every modification to frozen parameters, registered hypothesis specs, or cost model assumptions should be logged with a timestamp, justification, and the version it affected. What is the minimum change log architecture for a solo developer that would allow a future external audit to reconstruct the decision history?

### Minimum Viable Architecture for Integrity

23. **What is the single highest-leverage action for integrity?** If you could only ensure one architectural component is implemented correctly before Phase 1 begins, what would it be: (a) the WFO leakage audit, (b) the trial registry with trial count tracking, (c) the four-stream P&L attribution engine, or (d) the SimBroker cost validation? Justify your ranking.

24. **At what complexity point does solo execution become infeasible?** The spec adds modules sequentially (Phase 2: 1W overlay; Phase 3: equity shorts; Phase 4: crypto perps). At what point does the architecture become too complex for a solo developer to maintain without integrity degradation? Is there a specific module addition you would recommend against on complexity grounds alone?

25. **Portfolio layer as the primary alpha engine:** The spec explicitly frames the portfolio layer (vol targeting + correlation control + regime routing) as the primary alpha engine, not individual skill signals. This is architecturally coherent but creates an evaluation challenge: it is hard to attribute Sharpe improvements to portfolio construction vs. signal improvement without isolating each component. How would you architect a component-attribution framework that allows these contributions to be measured without introducing new overfitting surfaces?

---

## H. Current Review Focus (Cycle 1, In Progress)

These high-impact issues are actively being reviewed now and are expected to be resolved in the near-term remediation window:

- P4 algorithm formalization and reproducibility contract (Q-ID `A-01`, finding `F-4`)
- P3 trigger population + deterministic reduction selection (Q-ID `A-02`)
- RDL boundary unification and dormancy attestation model (Q-ID `B-02`, finding `F-23`)
- Harvey-Liu variant + trial aggregation canon (Q-ID `B-01`, findings `F-1`, `F-24`)
- Charter-level review operational schema for RBE activation (Q-ID `B-03`, finding `F-26`)
- RBE to kill-criteria interaction windows and RDL->RBE separation enforcement (Q-ID `B-04`, finding `F-31`)
- Net Sharpe composition consistency `(a+b+c)` across all artifacts (Q-ID `E-01`, finding `F-22`)
- K3 estimator and temporal wording lock (Q-ID `C-02`, `E-02`, finding `F-29`)
- GE-2/GE-3 zero-weight classification hard rule (Q-ID `B-05`, finding `F-32`)

Traceability:
- Question set: `docs/audit/QUESTION_POOL.md`
- Finding inventory and acceptance criteria: `docs/audit/REVIEW_REPORT.md`

---

## Next Actions (1–2 Weeks)

For a structured architecture review session:
- [ ] Review Section B (Integrity Controls) against Phase 0 exit criteria checklist — identify any criterion that is ambiguous or untestable
- [ ] Review Section E (Risk Register) — add or modify risks based on reviewer experience with comparable systems; mark any "Low" residual risks that reviewer disagrees with
- [ ] Provide written answers to questions 1, 2, 4, 6, 13, and 23 (minimum set covering highest-leverage architectural decisions)
- [ ] Identify any Non-Negotiable in Section B of the master spec that has an implementation ambiguity that would prevent it from being verified by a third party

For the project owner:
- [ ] Circulate this document to CTO reviewer at least 1 week before review session
- [ ] Prepare Phase 0 architecture sketch (WFO harness design, data model, trial registry schema) for review session
- [ ] Document the chosen technology stack before the session so technical questions are grounded in actual choices

---

*Document Version: 1.2 | Date: 2026-03-04*
*Classification: Confidential — External Review Document*
*For: CTO / Senior Systems Architect reviewer*
*Companion documents: entropy_protocol_master_spec_v1.md (full spec), entropy_protocol_trader_review_v1.md (trader version)*
