# Entropy Protocol — Architecture Model

**Classification:** Confidential — Internal Audit Document  
**Filename:** `docs/audit/ARCH_MODEL.md`  
**Audit Cycle:** Cycle 1 — Phase 0 (Pre-Development)  
**Pipeline Step:** Step 2 — Architecture Review  
**Pipeline Version:** v1.0  
**Date:** 2026-03-04  
**Status:** Draft — Awaiting Spec Owner Acceptance  
**Prior step input acknowledged:** `docs/audit/META_ANALYSIS.md` (2026-03-04, Cycle 1)  
**Full run / Partial run:** Full run: Yes / Partial run: No

---

## 1. Component Inventory

| Module | Purpose | Current activation state | Active from | Key inputs | Key outputs | Scope provenance |
|---|---|---|---|---|---|---|
| Data Pipeline | Ingest, clean, and store market data for evaluation and research | Active (build-required) | Phase 0 | Raw OHLCV/market feeds | Clean feature store / datasets | Present in AUDIT_v1 scope |
| SimBroker | Simulate fills/costs for paper and evaluation accuracy | Active (build-required) | Phase 0 | Order intents, market data, funding/borrow assumptions | Fill logs, cost estimates, slippage estimates | Present in AUDIT_v1 scope |
| Walk-Forward Harness | Leakage-resistant IS/OOS evaluation engine | Active (build-required) | Phase 0 | Feature store, registered strategy specs | OOS records, CI estimates, phase-gate evidence | Present in AUDIT_v1 scope |
| Trial Registry | Pre-registration and multiplicity accounting | Active (policy-required) | Phase 0 | Hypothesis specs (AT, Main Track, RDL), metadata | Locked trial records, trial counts, audit trail | Present in AUDIT_v1 scope; RDL namespace added v1.2 |
| Portfolio Layer | Convert skill and regime states into position targets | Conditional (not yet live) | Phase 1 | Skill signals, regime states (P1–P4), covariance/correlation estimates | Position targets, gross exposure profile | Present in AUDIT_v1 scope |
| Skills (base 5–6) | Generate directional signals for baseline system | Conditional (not yet live) | Phase 1 | Feature data, asset universe | Raw signal scores | Present in AUDIT_v1 scope |
| P&L Attribution Engine | Enforce four-stream decomposition and metric integrity | Conditional (spec-active, runtime from Phase 1) | Phase 1 | Trade logs, fill/cost logs, treasury logs | Streams (a)-(d), net Sharpe inputs | Present in AUDIT_v1 scope |
| Regime Signal Hierarchy (P1-P4) | Risk-state governance and override precedence | Conditional (P1/P4 implemented in Phase 0 infra; operational from Phase 1) | Phase 1 operational | DD/HWM, funding rates, rolling correlations, weekly regime labels | Exposure throttles, routing constraints, state transitions | Present in AUDIT_v1 scope |
| P1 DD Circuit Breaker | Highest-priority drawdown control | Conditional | Phase 1 | DD from HWM | 50% exposure cap + addition suspension | Present in AUDIT_v1 scope |
| P2 Funding Exit | Crypto funding risk override | Dormant until crypto shorts exist | Phase 4 practical relevance | 8h funding windows | Exit crypto short sleeve | Present in AUDIT_v1 scope |
| P3 Correlation Trigger | Correlation-based gross reduction mechanism | Conditional | Phase 1 | 20d rolling pairwise correlation population (unspecified) | 35-50% gross reduction over 3 days | Present in AUDIT_v1 scope |
| P4 Weekly Regime Overlay | Weekly regime-driven routing/sizing overlay | Conditional, algorithm undefined | Phase 2 operational; labels required in Phase 0 artifact | 1W signal algorithm + OHLCV | Regime labels (trending/mean-reverting/stress), routing adjustments | Present in AUDIT_v1 scope |
| 1W Regime Overlay (Phase 2 module) | Overlay-only weekly adjustment to reduce false-trigger events | Dormant | Phase 2 | P4 state, selected skill states | Modified routing/allocation for <=2 skill instances | Present in AUDIT_v1 scope |
| Equity Shorts | Add short sleeve by substitution under gross<=1.0 | Dormant | Phase 3 | Mirrored/repurposed signals, borrow quotes | Short targets, short P&L stream | Present in AUDIT_v1 scope |
| Crypto Perpetual Shorts | Optional short extension with funding drag constraints | Dormant (base plan bypass) | Phase 4 | Perp prices, funding rates, basis data | Crypto short targets, funding P&L stream | Present in AUDIT_v1 scope |
| Exit Overlays (AT -> Main) | Test alternative exit logic without changing entry logic | Scaffolding/Research active in AT; promotion conditional | AT in Phase 0 parallel; Main Track use Phase 1+ only via preregistered promotion | Pre-registered exit hypotheses, paper trade data | Overlay performance deltas, promotion candidates | Present in AUDIT_v1 scope |
| Treasury Layer | Generate yield on idle capital, separately attributed | Dormant | Phase 5 | Idle cash allocation decisions | Treasury P&L stream (d) | Present in AUDIT_v1 scope |
| Insight Layer / Chief Context Agent | Research hypothesis generation and narrative context | Research-only / no live influence | Era 4 minimum for live influence | Text/event sources, resolved hypotheses | InsightHypothesis objects, dashboard context | Present in AUDIT_v1 scope (deferred live) |
| Growth Layer (module) | Structural monitoring and governed risk-budget escalation path | Locked by default; monitoring-only | Built in Phase 0 as instrumentation; active influence only via RBE activation | Fill/cost logs, N_eff trends, utilization, Sharpe/DD | Monitoring metrics, review triggers, RBE step state | **Added in v1.1 (post-AUDIT_v1)** |
| Growth Submodule 1: Cost & Execution Monitor | Detect slippage and cost drift | Monitoring-only | Phase 0 build | Fill logs, costs, gross P&L | CRR, slippage drift, turnover metrics | **Added in v1.1** |
| Growth Submodule 2: Diversification Controller | Improve N_eff via allocation controls only | Monitoring/control within policy bounds | Phase 1 runtime after build | Skill P&L, rolling correlations, clustering | Cluster caps, N_eff trend, allocation recommendations | **Added in v1.1** |
| Growth Submodule 3: Capital Utilization Monitor | Track deployment efficiency and idle capital profile | Monitoring-only | Phase 0 build (reporting Phase 1+) | Position and cash logs | Utilization metrics, compliance flags | **Added in v1.1** |
| Growth Submodule 4: RBE (Risk Budget Escalator) | Govern reversible risk-budget step changes | Locked (Step 0 only unless formally activated) | Phase 1+ only after formal activation | Rolling Sharpe/DD, N_eff trend, cost-drag trend, activation log | RBE step state (0-4), activation/rollback log | **Added in v1.1** |
| RDL (Research Discovery Layer) | Structured research pipeline for hypothesis/label/feature/event artifacts | Dormant operationally until Phase 2; scaffolding-only in Phase 0-1 | Phase 2 operational | Feature/event/text data, hypothesis templates | RDL objects routed to Trial Registry | **Added in v1.2 (post-AUDIT_v1)** |
| RDL-1 Hypothesis Generator | Build `CandidateHypothesis` artifacts for registry submission | Scaffolding-only pre-Phase 2 | Phase 2 operational | Text feeds, AT candidates, open questions | CandidateHypothesis objects | **Added in v1.2** |
| RDL-2 Market State Labeler | Build `RegimeTag` objects for market-state research | Scaffolding-only pre-Phase 2; blocked by unresolved P4 spec | Phase 2 operational | OHLCV features, P4 prereg spec (missing) | RegimeTag objects | **Added in v1.2** |
| RDL-3 Feature Library | Versioned `FeatureSpec` catalog for preregistered tests | Scaffolding-only pre-Phase 2 | Phase 2 operational | Feature transforms + store | FeatureSpec versions bound to registry IDs | **Added in v1.2** |
| RDL-4 Event Label Builder | Build `EventLabel` objects for conditioning and base-rate studies | Scaffolding-only pre-Phase 2 | Phase 2 operational | Calendar/funding/text event data | EventLabel objects | **Added in v1.2** |

---

## 2. Data Flow Map

### 2.1 Primary Evaluation Flow

| Step | Source -> Target | Artifact / state |
|---|---|---|
| 1 | Raw market feeds -> Data Pipeline | Cleaned, time-indexed OHLCV/market dataset |
| 2 | Data Pipeline -> Feature Store / Scaffolding datasets | Feature inputs for skills and research artifacts |
| 3 | Feature Store -> Skills | Skill-level signal scores |
| 4 | Skills + P1-P4 states -> Portfolio Layer | Position targets under leverage and regime constraints |
| 5 | Portfolio Layer -> SimBroker | Simulated orders/fills with explicit costs |
| 6 | SimBroker + trade logs -> P&L Attribution Engine | Streams (a), (b), (c), (d) and active-book return series |
| 7 | P&L + configuration snapshots -> Walk-Forward Harness | OOS metrics, CI outputs, phase-gate evidence |
| 8 | Harness runs + hypothesis specs -> Trial Registry | Trial records and multiplicity inputs for Harvey-Liu deflation |

### 2.2 Regime Signal and Control Flow

| Flow | Description | Current architectural state |
|---|---|---|
| P4 algorithm -> regime label -> P4 state -> Portfolio Layer | Weekly regime overlay affects routing/sizing inside active exposure budget | **Algorithm source unspecified (RS-03, P0)** |
| P1/P2/P3 triggers -> precedence rules -> Portfolio Layer | Higher-priority state overrides lower-priority directives | Partial: precedence defined; concurrent recovery paths under-specified (RS-06, P1) |
| Growth monitors -> metrics/review flags -> RBE activation gate -> conditional portfolio influence | Monitoring outputs feed governance pathway, not automatic actions by default | Activation boundary exists but operational review mechanics undefined (RS-11, P0) |
| RDL-2 RegimeTag outputs -> research routing (Phase 2+) | Market-state tags intended for Phase 2+ research integration | RDL-2 depends on unresolved P4 prereg spec (RS-03/RS-13) |

### 2.3 Trial Counting Flow

| Hypothesis source | Trial namespace | Trial count inception | Architectural implication |
|---|---|---|---|
| Acceleration Track hypotheses | `AT-*` | At preregistration submission | Counts toward multiplicity budget |
| Main Track signal/overlay specs | Existing Main Track IDs | At preregistration submission | Counts toward multiplicity budget |
| RDL hypotheses (RDL-1) | `RDL-*` | **At submission, not promotion** | Expands trial budget before operational deployment (RS-12, P0 with RS-01 dependency) |
| Growth/RBE policy experiments | Registry entry required before activation | At preregistration submission | Governance becomes multiplicity-coupled if treated as experiment objects |

---

## 3. Phase Dependency Map

| Module | Active from | Gate condition | Depends on (prior phase deliverables) |
|---|---|---|---|
| Data Pipeline | Phase 0 | Start condition | Provider integration + feed continuity controls |
| SimBroker | Phase 0 | Build + calibration criteria in Phase 0 exit list | Bid/ask validation on >=100 fills |
| Walk-Forward Harness | Phase 0 | Leakage audit must pass | Temporal-split architecture + registry linkage |
| Trial Registry | Phase 0 | Operational before AT/Main evaluation claims | Schema lock, immutable logs |
| Growth Layer instrumentation (Submodules 1-3) | Phase 0 build | Operational confirmation prior to Phase 1 start | Fill schema, correlation pipeline, utilization log |
| Phase 1 baseline engine (skills + portfolio + attribution) | Phase 1 | Phase 0 exit criteria all met | Harness + SimBroker + registry + P1/P4 implementation artifacts |
| P3 correlation control | Phase 1 | Phase 1 runtime | **Locked population definition required (currently missing, RS-04)** |
| 1W Regime Overlay | Phase 2 | Phase 1 exit + rho(4H,1W) requirement + P2 criteria | **P4 algorithm defined and versioned; matched paper comparison** |
| RDL operational routing | Phase 2 | Phase 2 boundary explicitly satisfied | Scaffolding artifacts from Phase 0-1 + dormancy enforcement controls |
| Equity Shorts | Phase 3 | Phase 2 exit + sample/kill thresholds | Borrow model calibration + short-side trial governance |
| Crypto Perp Shorts | Phase 4 | Phase 3 exit + funding viability | Funding/basis telemetry + P4K criteria controls |
| Treasury Layer | Phase 5 | Phase 1 exit + >=3 months live capital | Stable active-book metrics and P&L separation |
| RBE Step >0 activation | Phase 1+ conditional | Charter-level review + preregistered activation experiment | Governance artifact + rollback condition wiring + stop-condition monitors |

Cross-phase dependency of concern:
- Phase 0 requires P4 historical labels over >=3 years, while Phase 1 requires regime-spanning OOS certification. If P4 uses fitted parameters, label vintage can contaminate later gate evidence (RS-07, P1).

---

## 4. Integration Points

| Source -> Target | Data/signal type | Phase-gated? | Potential evaluation-vs-execution divergence? |
|---|---|---|---|
| Data Pipeline -> Walk-Forward Harness | Time-indexed feature datasets | No (Phase 0 core) | Yes; timestamp convention ambiguity can leak future info in execution replicas (RS-17) |
| Skills -> Portfolio Layer | Signal scores and confidence states | Yes (Phase 1+) | Yes; if execution runtime uses different preprocessing/window semantics |
| Regime hierarchy (P1-P4) -> Portfolio Layer | Exposure/routing override states | Yes (Phase 1+) | Yes; undefined concurrent recovery states can diverge across implementations (RS-06) |
| P4 labeling process -> Phase 0/1 gate evidence | Historical regime labels, regime instance counts | Yes | **Yes; undefined P4 algorithm makes gate evidence non-reproducible (RS-03)** |
| SimBroker -> P&L Attribution/Kill Criteria monitors | Fill/cost records, cost drift metrics | Yes | Yes; Phase 1 has flags but no kill action, allowing contaminated pass decisions (RS-08) |
| Trial Registry -> Harvey-Liu computation pipeline | Trial count, prereg metadata | No | **Yes; formula variant undefined and count scope changed by RDL submissions (RS-01, RS-12)** |
| RDL-1 -> Trial Registry | `CandidateHypothesis` prereg entries (`RDL-*`) | Yes (operational Phase 2+, scaffolding before) | Yes; submission-time counting can inflate haircut before promotion decisions (RS-12) |
| RDL-2 -> Regime research routing | `RegimeTag` objects | Yes (Phase 2+) | Yes; unresolved P4 spec makes label semantics unstable across tools (RS-03, RS-13) |
| RDL-3 -> Evaluation pipeline | Versioned `FeatureSpec` references | Yes (Phase 2+) | Yes; purge/embargo conventions for version changes unspecified (RS-16) |
| RDL-4 -> Conditioning/event logic | `EventLabel` objects + timestamped events | Yes (Phase 2+) | Yes; timestamp normalization conventions undefined (RS-17) |
| Growth monitors -> RBE | CRR/N_eff/utilization + Sharpe/DD trends | Yes (activation only) | Yes; charter-level review artifact undefined, allowing inconsistent activation practices (RS-11, RS-15) |
| RBE step state -> Portfolio Layer policy | Step-specific risk budget constraints | Yes | Yes; kill-criteria interaction not specified when risk budget changes (RS-15) |

---

## 5. Architectural Assumptions (Stated and Unstated)

| ID | Assumption text | Source status | RS link | Severity |
|---|---|---|---|---|
| A-01 | Harvey-Liu deflation can be consistently computed from registry metadata without specifying formula variant | Stated requirement, formula unstated | RS-01, RS-12 | P0 |
| A-02 | P4 can produce reproducible 3-year historical labels despite no formal algorithm spec | Stated outcome, mechanism unstated | RS-03 | P0 |
| A-03 | P3 trigger uses a consistent correlation population across phases | Stated trigger threshold, population unstated | RS-04 | P0 |
| A-04 | Concurrent P1/P3 activation and recovery paths are deterministic in implementation | Partially stated precedence, recovery sequencing unstated | RS-06 | P1 |
| A-05 | Phase 0 P4 labeling process does not contaminate Phase 1 OOS regime-span certification | Unstated but required for valid gate evidence | RS-07 | P1 |
| A-06 | SimBroker drift flags in Phase 1 are sufficient without a kill action | Stated as flag-only policy | RS-08 | P1 |
| A-07 | N_eff computation method choice does not change K3 boundary decisions materially | Unstated; conflicting candidate formulas in prior audit context | RS-09 | P1 |
| A-08 | K4 screening threshold is acceptable despite both high false-kill and missed-kill risk | Stated tradeoff, incomplete calibration record | RS-10 | P1 |
| A-09 | Growth Layer remains monitoring-only unless governance activation is explicit and auditable | Stated policy, activation artifact unspecified | RS-11 | P0 |
| A-10 | RDL dormancy in Phase 0-1 can be externally verified | Stated policy, enforcement artifact unstated | RS-13 | P0 |
| A-11 | Growth/RDL additions cannot violate frozen NN constraints due to policy text alone | Unstated; requires explicit guardrails | RS-14 | P0 |
| A-12 | RBE step changes do not alter kill-criteria validity windows or trigger semantics | Unstated | RS-15 | P1 |
| A-13 | FeatureSpec versioning can coexist with current purge/embargo phrasing without explicit formula | Unstated | RS-16 | P2 |
| A-14 | Event labels can be safely integrated without explicit timestamp normalization standard | Unstated | RS-17 | P2 |
| A-15 | 35-50% P3 reduction band can be operationalized consistently absent a selection function | Stated range, selection rule unstated | RS-18 | P2 |

---

## 6. New Surface Analysis (v1.1/v1.2 Additions)

### 6.1 Growth Layer (v1.1)

#### Monitoring -> RBE Activation Pathway

| Stage | Current specification state | Gap |
|---|---|---|
| Monitoring metrics produced (CRR, N_eff trend, utilization, cost drag) | Defined in Section E/J1 | No direct formula-to-action binding beyond review triggers |
| Eligibility for RBE Step >0 | Requires charter-level review + preregistration | "Charter-level review" actor/process/output artifact not operationally defined |
| Activation execution | Steps cannot be skipped; rollback automatic on stop conditions | Stop-condition mapping to existing kill criteria not fully documented |
| Active influence boundary | Step 0 monitoring-only; active influence only after formal activation | Transition criteria are governance text, not machine-checkable control |

Assessment:
- Triggering is currently judgment-mediated, not formula-specified. That is acceptable only if governance artifacts are explicit and auditable.
- Missing operational definition of review authority and required output creates a policy-to-implementation gap (RS-11, P0).
- Interaction with NN-1 to NN-6 is not explicitly mapped per step; risk exists that risk-budget changes alter effective leverage/exposure behavior without explicit invariant checks (RS-14, RS-15).

### 6.2 RDL (v1.2)

#### Scaffolding vs Operational Boundary by Submodule

| Submodule | Scaffolding mode (Phase 0-1) | Operational mode (Phase 2+) | Missing boundary artifact |
|---|---|---|---|
| RDL-1 Hypothesis Generator | Object schema/logging only | Registry-routable candidate generation | No explicit state flag/audit test proving non-operational mode |
| RDL-2 Market State Labeler | Schema validation/logging only | RegimeTag production for routing research | Depends on unresolved P4 prereg spec; no dormancy attestation artifact |
| RDL-3 Feature Library | Feature schema + dataset prep only | Versioned FeatureSpec used in evaluations | No purge/embargo formula for midstream feature-version transitions |
| RDL-4 Event Label Builder | Event dataset collection/logging only | Event conditioning support for hypotheses | No timestamp convention control standard |

#### RDL-1 -> Trial Registry pipeline and trial count inception
- RDL submissions are counted at submission time, not promotion time.
- This shifts multiplicity burden earlier and can inflate Harvey-Liu haircuts during research backlog growth.
- Because Harvey-Liu formula remains unspecified, effect size of this inflation is not auditable (RS-01 + RS-12, P0).

#### RDL-2 dependency on F-4 (P4 algorithm)
- RDL-2 inputs reference a P4 prereg specification "when defined per F-4 resolution".
- Without F-4 resolution, RDL-2 cannot have stable semantics, even in later phases.

#### RDL-3 and purge/embargo interaction
- Feature version-locking is defined, but embargo duration formula remains unspecified in core spec.
- New feature versions can create leakage ambiguity across adjacent windows without explicit embargo mechanics (RS-16, P2).

#### RDL-4 and timestamp leakage interaction
- Event labels combine calendar, funding, and text markers with potentially heterogeneous time conventions.
- No canonical timestamp normalization standard is defined for label generation or downstream joins (RS-17, P2).

---

## 7. Severity-Flagged Architecture Gaps

| Gap ID | Description | Severity | RS ID |
|---|---|---|---|
| AG-01 | Harvey-Liu computation node exists but formula and parameterization are undefined; RDL count-inflation magnifies uncertainty | P0 | RS-01, RS-12 |
| AG-02 | P4 production node required by multiple gates but no algorithmic specification exists | P0 | RS-03 |
| AG-03 | P3 trigger population undefined at architecture boundary (data source and population scope not locked) | P0 | RS-04 |
| AG-04 | Growth Layer RBE transition not operationally auditable (undefined review authority/artifact/state flag) | P0 | RS-11, RS-13 |
| AG-05 | New module interactions with frozen non-negotiables are policy-stated but not mapped as enforceable checks | P0 | RS-14 |
| AG-06 | Concurrent P1/P3 state recovery path not fully defined; implementation divergence likely | P1 | RS-06 |
| AG-07 | P4 label vintage contamination boundary between Phase 0 calibration and Phase 1 OOS evidence not specified | P1 | RS-07 |
| AG-08 | Phase 1 SimBroker drift handling lacks kill action despite gate-critical dependence | P1 | RS-08 |
| AG-09 | RBE step changes lack explicit interaction rules with kill criteria measurement windows/thresholds | P1 | RS-15 |
| AG-10 | RDL feature/event integration lacks purge-embargo and timestamp standards | P2 | RS-16, RS-17 |
| AG-11 | P3 reduction range (35-50%) lacks deterministic selection function | P2 | RS-18 |

---

## 8. Gaps Requiring Immediate Spec Clarification

The following gaps block reliable Step 3-5 outputs if left unresolved or unbounded:

1. **P4 algorithm specification and versioning boundary** (AG-02, P0, RS-03).  
Why immediate: Step 3 invariant extraction cannot formalize a non-existent rule.

2. **Harvey-Liu formula variant + trial aggregation rules including `RDL-*` submission-time counting** (AG-01, P0, RS-01/RS-12).  
Why immediate: Invariant and drift checks on multiplicity control are not machine-checkable without formula definition.

3. **P3 correlation population and deterministic reduction selection rule (35-50%)** (AG-03/AG-11, P0/P2, RS-04/RS-18).  
Why immediate: Step 4 drift assertions need a single invariant statement for trigger and action.

4. **Growth Layer/RBE governance artifact definition (who approves, what record proves activation, how dormancy is externally verifiable)** (AG-04, P0, RS-11/RS-13).  
Why immediate: Step 5 adversarial review will otherwise classify any activation path as governance-bypass-prone.

5. **RBE interaction with kill criteria and frozen NN checks** (AG-05/AG-09, P0/P1, RS-14/RS-15).  
Why immediate: Changes in risk budget without explicit invariant coupling can invalidate phase-gate comparability.

6. **Phase boundary controls for RDL-3/RDL-4 (purge-embargo formula, timestamp convention standard)** (AG-10, P2, RS-16/RS-17).  
Why immediate: Needed to prevent leakage-class ambiguity when Step 5 stress-tests execution realism.

---

Prepared for Step 3 input (`docs/audit/PROMPT_2_INVARIANTS.md`).
