# Entropy Protocol — Architecture Model

**Audit Cycle:** Cycle 3 — Post-Phase0 Archive-Only Gate Audit
**Pipeline Step:** Step 2 — Architecture Review
**Pipeline Version:** v1.0
**Date:** 2026-05-05
**Status:** Draft — Awaiting Spec Owner Acceptance
**Prior step input:** `docs/audit/META_ANALYSIS.md`
**Full run / Partial run:** Full run: Yes / Partial run: No

## Executive Architecture Verdict

Verdict: `ALIGNED_FOR_PHASE_1A_PLANNING_ONLY`.

The architecture supports moving into Phase 1A archive-only planning because the
Phase 0 foundation now has deterministic data, registry, SimBroker,
walk-forward, P4, leakage, and evidence machinery. It does not support Phase 1
strategy implementation, live operation, RDL activation, or Growth/RBE
activation until the Phase 1 archive entry contract is written and reviewed.

## Component Inventory

| Component | Current state | Active from | Inputs | Outputs | Gate risk |
|---|---|---|---|---|---|
| Data Pipeline | Implemented foundation; archive evidence packet complete | Phase 0 / Phase 1A archive | Approved archive OHLCV | Parquet datasets, hashes, stability rows | Live feed stability not proven |
| Trial Registry | Implemented foundation | Phase 0+ | Trial specs, run records | Append-only registry records | Phase 1A must define preregistration boundaries |
| Walk-Forward Harness | Implemented foundation | Phase 0+ | Dataset, strategy callbacks, leakage report | IS/OOS run records | Archive entry contract must freeze split policy |
| SimBroker | Implemented foundation; calibration evidence packet accepted | Phase 0+ | Fill logs, quotes, cost config | Fill/cost records | Live broker integration absent by design |
| P&L Attribution | Implemented foundation | Phase 1+ | Fill/cost/trade logs | Four streams, metrics scaffolds | No performance claims before registered archive evaluation |
| P1/P3 Governance | Implemented foundation | Phase 1+ | HWM/DD, correlations | Governance events, exposure state | Needs Phase 1A portfolio contract |
| P4 | Implemented/evidenced for archive foundation | Phase 0 evidence, Phase 1 reporting context | 1D archive data | Vintage labels | Must preserve label vintage/freeze |
| Statistical Helpers | Report-boundary accepted | Reporting only | Return series, trial family table | CI/HL report fields | Not independent formula validation |
| Growth Layer | Protocol-defined, runtime inactive except future monitoring/instrumentation | Phase 1A planning / later monitoring | Cost, N_eff, utilization | Monitoring facts only | RBE activation locked |
| RBE | Locked | Future charter-level review only | Growth metrics, review packet | Step state if approved | Must remain inactive |
| RDL | Dormant | Phase 2 operational; Phase 0-1 scaffolding only | Hypotheses/features/events | RDL objects | No Phase 1A generation or portfolio influence |

## Data Flow Map

| Flow | Status | Phase 1A requirement |
|---|---|---|
| Archive OHLCV -> Data Pipeline -> Dataset hashes | Working | Define dataset freeze and admissible windows |
| Dataset -> P4 labels -> evidence packet | Working | Define how labels are referenced without recalibration drift |
| Dataset -> Walk-forward harness -> Trial Registry | Foundation working | Define archive IS/OOS split and preregistration contract |
| SimBroker fills -> P&L attribution | Foundation working | Define long-only baseline cost assumptions and reporting fields |
| Governance state -> Portfolio constraints | Foundation working | Define portfolio-layer exposure rules before implementation |
| Growth metrics -> monitoring facts | Not yet Phase 1A-defined | Define monitoring-only outputs, no RBE activation |
| RDL objects -> Trial Registry | Not allowed in Phase 1A except explicitly approved scaffolding | Define dormancy attestation |

## Phase Dependency Map

| Module | Active from | Gate condition | Depends on |
|---|---|---|---|
| Phase 1A archive planning | Now | D-028 | Archive-only Phase 0 foundation closure |
| Phase 1 strategy implementation | After P1A contract approval | Frozen archive entry contract | P1A-001 and follow-on task graph |
| Live data stability | Future live gate | >=90 live monitored days | Provider activation and live monitoring approval |
| RDL operational mode | Phase 2 | Phase 2 start and registry controls | Phase 1 completion; RDL attestation |
| Growth/RBE active influence | Future explicit review | Charter-level review and preregistration | Monitoring evidence and RBE packet |

## Architectural Assumptions

| ID | Assumption | Severity | Status |
|---|---|---|---|
| AR-C3-001 | Archive-only evidence can close research foundation but not live readiness | P1 | Explicit in D-027 |
| AR-C3-002 | Phase 1A can plan archive evaluation before strategy implementation | P1 | Explicit in D-028 |
| AR-C3-003 | RDL remains dormant in Phase 1A | P1 | Must be enforced in P1A-001 |
| AR-C3-004 | Growth monitoring can be specified without RBE activation | P1 | Must be enforced in P1A-001 |
| AR-C3-005 | No OOS/performance claim is produced by archive foundation closure | P1 | Explicit in gate packets |

## Gaps Requiring Immediate Spec Clarification

1. P1A-001 must define admissible archive datasets, freeze rules, IS/OOS
   boundaries, and report labels.
2. P1A-001 must define RDL dormancy attestation for Phase 1A.
3. P1A-001 must define Growth Layer monitoring-only scope and explicitly block
   RBE activation.
4. Future live gate must remain separate from archive-only Phase 0 closure.
