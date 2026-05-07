# FORMULA_EVIDENCE_DEBT
_Date: 2026-05-05 · Scope: P0.5-002 Formula and evidence debt register_

## Purpose

This register ranks unresolved formula and evidence surfaces by their impact on
Phase 0 gate approval, Phase 1 planning, and future claims. It separates direct
Phase 0 exit blockers from downstream statistical/reporting debt so the next
tasks can be sequenced without overstating the current foundation.

## Decision Summary

| Item | Status |
|------|--------|
| Phase 0 gate | `NOT_APPROVED` |
| Phase 1 implementation | Blocked |
| OOS/performance claims | Blocked |
| T23 statistical helpers | Provisional only |
| F-30/F-31 | Future real-evidence gates; no synthetic closure |
| Next task | P0.5-004 Purge/Embargo Design Decision |

The main strategic answer is: do not start Phase 1. Close or explicitly
disposition formula/evidence debt first, starting with the statistical surfaces
that can make performance reports appear more certain than the evidence allows.

## Ranking Rules

| Rank | Meaning |
|------|---------|
| `GATE_BLOCKER` | Blocks Phase 0 approval directly or requires charter-level revision |
| `CLAIM_BLOCKER` | Blocks OOS/performance/statistical validity claims, even if not one of the six Phase 0 exit criteria |
| `PRE_PHASE1_BLOCKER` | Must be resolved or explicitly bounded before Phase 1 implementation/planning can rely on it |
| `FUTURE_HARD_GATE` | Does not block immediate Phase 0.5 documentation work, but blocks the future artifact path it governs |
| `TRACKED_DEBT` | Must remain visible but is not the immediate next blocker |

## Debt Register

### FD-01: P4 Historical Regime Labels

| Field | Value |
|-------|-------|
| Rank | `GATE_BLOCKER` |
| Surface | P4 weekly regime signal / `P4-RBL-v1` |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Deterministic P4 Protocol and Phase 0 exit criteria |
| Current state | Deterministic method is specified in docs; no runtime labeler or label-vintage artifacts exist |
| Why it matters | P4 label coverage is an explicit Phase 0 exit criterion: >=3 years of 1D labels on >=15 of 20 target assets |
| Current artifact | `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` EC-05 |
| Required closure | P0.5-005 selected implementation/evidence path; implement labeler and produce >=3 years/15 assets label evidence |
| Blocking scope | Phase 0 approval and Phase 1 start |
| Next task | Future P4 implementation/evidence task after evidence plans |

### FD-02: SimBroker Calibration Evidence

| Field | Value |
|-------|-------|
| Rank | `GATE_BLOCKER` |
| Surface | >=100 manually verified bid/ask fill comparison; 15% acceptance target |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Phase 0 exit criteria; `products/entropy-core/docs/core/GLOSSARY.md` SimBroker |
| Current state | Cost model, fill engine, and provider interface exist; no real calibration packet exists |
| Why it matters | SimBroker cost realism is load-bearing for every downstream net Sharpe, cost drag, CRR, and kill/gate report |
| Current artifact | `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` EC-02 |
| Required closure | P0.5-006 defines source/provider boundary requirements, row schema, manual verification procedure, and deviation report; future real evidence still required |
| Blocking scope | Phase 0 approval and Phase 1 start |
| Next task | Future calibration implementation/evidence task |

### FD-03: Data Pipeline Stability Evidence

| Field | Value |
|-------|-------|
| Rank | `GATE_BLOCKER` |
| Surface | >=90 continuous days of target-universe feed monitoring with zero unexplained gaps |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Phase 0 exit criteria |
| Current state | Local fixture ingestion and data quality checks exist; no 90-day monitoring evidence exists |
| Why it matters | Phase 1 cannot rely on data whose continuity, provider boundary, and gap-disposition process are not evidenced |
| Current artifact | `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` EC-04 |
| Required closure | P0.5-007 defines monitoring plan, provider approval boundary, target universe requirements, artifact schema, and gap disposition policy; future real 90-day evidence still required |
| Blocking scope | Phase 0 approval and Phase 1 start, unless charter-level revision occurs |
| Next task | Future data-stability monitoring implementation/evidence task |

### FD-04: Registered Leakage / Temporal-Shuffling Gate Packet

| Field | Value |
|-------|-------|
| Rank | `GATE_BLOCKER` |
| Surface | Walk-forward leakage audit with zero forward-looking features verified by temporal shuffling |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Phase 0 exit criteria; `products/entropy-core/docs/spec.md` walk-forward evidence |
| Current state | T18/T19/T20 implementation and synthetic tests pass; no registered gate packet exists |
| Why it matters | Without registered-run leakage evidence, the system can block obvious synthetic leakage but cannot claim the Phase 0 leakage gate is passed |
| Current artifact | `products/entropy-core/docs/audit/PHASE0_EXIT_GAP_REGISTER.md` EC-01 |
| Required closure | Define temporal-shuffling gate semantics and attach registered RunRecord evidence |
| Blocking scope | Phase 0 approval, OOS labels, and any performance report |
| Next task | P0.5-008 and P0.5-009 |

### FD-05: Sharpe CI

| Field | Value |
|-------|-------|
| Rank | `CLAIM_BLOCKER` |
| Surface | `CI-SR-ACF-v1` Sharpe confidence interval |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Net Sharpe and CI fields; D-010 F-2 |
| Current state | T23 provides a provisional helper and deterministic bootstrap stub with explicit reason code |
| Why it matters | Incorrect CI language can make weak 15-month evidence look precise; the protocol explicitly treats K1 as a policy screen, not a powered statistical proof |
| Current artifact | `entropy/stats/analysis.py`; `tests/unit/test_stats.py`; `products/entropy-core/docs/audit/T23_FORMULA_GOVERNANCE_DISPOSITION.md` |
| Required closure | P0.5-003 marked this helper `REVISE_REQUIRED_FOR_GATE_USE`; implementation/report layer needs canonical autocorrelation/report fields and re-review |
| Blocking scope | OOS/performance/statistical confidence claims; Phase 1 report design |
| Next task | Future implementation/re-review after P0.5-004+ decisions |

### FD-06: Harvey-Liu Deflation

| Field | Value |
|-------|-------|
| Rank | `CLAIM_BLOCKER` |
| Surface | `HL-HB-v1` Holm-Bonferroni family-wise gate control |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Harvey-Liu section; D-010 F-1 |
| Current state | T23 provides a skeleton helper with method ID, adjusted p-value field, and stub reason code |
| Why it matters | Trial multiplicity is central to the protocol. Any gate or report that uses deflated Sharpe without independent review can understate search debt |
| Current artifact | `entropy/stats/analysis.py`; `tests/unit/test_stats.py`; `products/entropy-core/docs/audit/T23_FORMULA_GOVERNANCE_DISPOSITION.md` |
| Required closure | P0.5-003 marked this helper `BLOCKED_FOR_GATE_USE`; implementation/report layer needs family-table Holm-Bonferroni workflow and re-review |
| Blocking scope | OOS/performance/statistical validity claims; future phase reports where raw Sharpe < 0.40 |
| Next task | Future implementation/re-review after P0.5-004+ decisions |

### FD-07: Purge/Embargo Design

| Field | Value |
|-------|-------|
| Rank | `PRE_PHASE1_BLOCKER` |
| Surface | Walk-forward purge/embargo derivation |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Phase 0 track; `products/entropy-core/docs/audit/PHASE0_STRATEGIC_DECISION.md` |
| Current state | T18 implements documented temporary `N` consecutive-bar embargo before OOS start |
| Why it matters | A temporary embargo can be sufficient for implementation tests while still being under-specified for production OOS claims, especially for 4H bars and multi-day holding periods |
| Current artifact | `entropy/walkforward/splitter.py`; `tests/integration/test_walk_forward.py`; `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Required closure | P0.5-004 retained the assumption as scaffold only and blocked Phase 1 OOS claims until derived methodology exists |
| Blocking scope | Phase 1 OOS claim design and final gate packet confidence |
| Next task | Future purge/embargo methodology task before Phase 1 OOS claims |

### FD-08: N_eff / K3

| Field | Value |
|-------|-------|
| Rank | `PRE_PHASE1_BLOCKER` |
| Surface | Effective factor count estimator and K3 governance semantics |
| Canonical source | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` N_eff, K3, Growth Layer Submodule 2; `products/entropy-core/docs/core/GLOSSARY.md` |
| Current state | T23 provides a simple estimator `k / (1 + (k - 1) * rho_avg)`; no integration with diversification controller, DR monitoring, or empirical Phase 1 artifact exists |
| Why it matters | N_eff drives K3, diversification controller evidence, and FLAM breadth adjustment. A simple estimator can be a documented primitive but not a complete operational monitor |
| Current artifact | `entropy/stats/analysis.py`; `tests/unit/test_stats.py`; `products/entropy-core/docs/audit/T23_FORMULA_GOVERNANCE_DISPOSITION.md` |
| Required closure | Decide whether the simple estimator is sufficient for Phase 1 planning, define required inputs and reporting fields, and bind it to future diversification-controller evidence |
| Blocking scope | Phase 1 planning surfaces that rely on K3, N_eff optimization, or FLAM breadth |
| Next task | P0.5-008 or a new follow-up spawned from P0.5-002/P0.5-008 |

### FD-09: IC/BR/FLAM Breadth Controls

| Field | Value |
|-------|-------|
| Rank | `TRACKED_DEBT` |
| Surface | IC_long, BR_long, BR_eff, and FLAM planning controls |
| Canonical source | D-010 F-5; `products/entropy-core/docs/core/PROTOCOL_SPEC.md`; `products/entropy-core/docs/core/CHARTER.md`; `products/entropy-core/docs/core/GLOSSARY.md` |
| Current state | Canonical docs were corrected by D-016; no current runtime IC/BR/FLAM implementation is in scope |
| Why it matters | FLAM-style planning can become overconfident if unadjusted breadth or prior IC is treated as evidence |
| Current artifact | `products/entropy-core/docs/audit/D010_CLOSURE_PACKET.md`; canonical core docs |
| Required closure | Keep as reporting guardrail; require future IC/BR/FLAM implementation to show raw/adjusted BR, evidence label, and N_eff dependency |
| Blocking scope | Future FLAM reports and any IC/BR-derived claims |
| Next task | Not immediate unless P0.5-008 reality sync finds drift |

### FD-10: F-30 RDL Promotion Telemetry

| Field | Value |
|-------|-------|
| Rank | `FUTURE_HARD_GATE` |
| Surface | RDL queue runtime telemetry: FIFO, monthly cap, shock control |
| Canonical source | D-010 F-30; D-015 scope rule |
| Current state | Evidence contract exists in docs; no generated RDL promotion telemetry exists |
| Why it matters | RDL is dormant/scaffolding-only through Phase 0-1. Future RDL promotion claims need real telemetry, not text-only assertions |
| Current artifact | `products/entropy-core/docs/audit/D010_CLOSURE_PACKET.md`; `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Required closure | Real generated telemetry artifacts plus audit checks for FIFO, monthly cap, and shock control |
| Blocking scope | Any RDL promotion telemetry closure, RDL portfolio influence, or phase evidence that depends on RDL queue behavior |
| Next task | Future RDL task, not P0.5 immediate |

### FD-11: F-31 K-Report Epoch Coverage

| Field | Value |
|-------|-------|
| Rank | `FUTURE_HARD_GATE` |
| Surface | K-report epoch tags and mixed-epoch per-slice evidence |
| Canonical source | D-010 F-31; D-015 scope rule |
| Current state | Evidence contract exists in docs; no real K-report artifacts exist |
| Why it matters | Kill reports can be invalid if mixed evaluation epochs are aggregated without per-epoch slices |
| Current artifact | `products/entropy-core/docs/audit/D010_CLOSURE_PACKET.md`; `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Required closure | Real generated K-report evidence with epoch tags, per-epoch slices, policy hash, code hash, and dataset hash |
| Blocking scope | Any K1-K6 report-generation closure or phase-exit evidence using K reports |
| Next task | Future K-report task, not P0.5 immediate |

## Execution Order

| Order | Work | Reason |
|-------|------|--------|
| 1 | P0.5-003 Sharpe CI And Harvey-Liu Review Packets | Complete; CI requires revision and Harvey-Liu is blocked for gate use |
| 2 | P0.5-004 Purge/Embargo Design Decision | Complete; T18 embargo remains scaffold only and blocks Phase 1 OOS claims |
| 3 | P0.5-005 P4 Labeler Gate Decision | Complete; implementation/evidence path selected |
| 4 | P0.5-006 SimBroker Calibration Evidence Plan | Complete; future real quote/manual evidence still required |
| 5 | P0.5-007 Data Pipeline Stability Plan | Complete; future real 90-day monitoring evidence still required |
| 6 | P0.5-008 reality sync | Architecture/spec/task docs should reflect the accepted debt dispositions |
| 7 | P0.5-009 gate packet | Final assembly only after the above decisions/evidence exist |

## Non-Closure Rules

- T23 helper tests do not validate Sharpe CI, Harvey-Liu, or N_eff for gate use.
- A report may display provisional values only if it labels them as provisional
  and prevents phase-exit, OOS, RDL, K-report, P4, IC/BR, and FLAM claims.
- F-30 and F-31 cannot be closed by documentation, synthetic fixtures, or
  implementation existence. They require real generated runtime/audit artifacts.
- P4 cannot be treated as satisfied by a written algorithm alone; the Phase 0
  criterion requires historical labels over the specified data coverage.
- No debt item in this register authorizes Phase 1 implementation or live
  capital.

## Immediate Recommendation

Proceed to P0.5-008. SimBroker calibration and data stability now have evidence
plans, so the next step is to synchronize implementation-facing docs with the
actual Phase 0.5 state.
