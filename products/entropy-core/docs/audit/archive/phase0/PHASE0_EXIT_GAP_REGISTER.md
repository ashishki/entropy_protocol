# PHASE0_EXIT_GAP_REGISTER
_Date: 2026-05-05 · Scope: P0.5-001 Phase 0 exit criteria gap register_

## Purpose

This register maps the canonical Phase 0 exit criteria to the current T01-T24
implementation baseline, the evidence still missing, and the next closure path.

This is not a phase-gate approval. It is the control document for deciding what
must be produced before Phase 0 can be approved or before any charter-level
revision can be proposed.

## Gate Status

| Item | Status |
|------|--------|
| T01-T24 implementation foundation | Complete |
| Current local baseline | 135 passing tests with PostgreSQL 16 Docker container |
| Phase 0 gate | `NOT_APPROVED` |
| Phase 1 implementation | Blocked |
| OOS/performance claims | Blocked |
| Live capital | Blocked |
| Partial Phase 0 | Not allowed |

Canonical rule: Phase 0 has no kill criteria and no partial approval path. If
the infrastructure or evidence cannot be built, Phase 1 does not start.

## Canonical Sources

| Source | Relevant authority |
|--------|--------------------|
| `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Section F, Phase 0 | Primary Phase 0 exit criteria and Growth Layer build requirements |
| `products/entropy-core/docs/core/CHARTER.md` Phase 0 | Repeats all required exit criteria and the no-partial-Phase-0 rule |
| `products/entropy-core/docs/core/GLOSSARY.md` SimBroker / Trial Registry | SimBroker calibration target and Trial Registry semantics |
| `products/entropy-core/docs/ARCHITECTURE.md` Overview / Phase 0 Run Path | Machine-checkable evidence and no OOS/live-capital boundary |
| `products/entropy-core/docs/spec.md` Overview / Phase Gate Evidence | Implementation-facing Phase 0 evidence behavior |
| `products/entropy-core/docs/audit/PHASE0_STRATEGIC_DECISION.md` | D-021 strategic decision selecting Phase 0.5 |

## Exit Criteria Register

### EC-01: Walk-Forward Leakage Audit

| Field | Value |
|-------|-------|
| Canonical criterion | Walk-forward harness passes leakage audit: zero forward-looking features verified by temporal shuffling test |
| Current implementation/evidence | T18 splitter, T19 leakage checklist, and T20 runner exist; OOS execution is blocked when leakage checks are missing or failing; synthetic detector tests pass |
| Current artifacts | `entropy/walkforward/splitter.py`; `entropy/walkforward/leakage.py`; `entropy/walkforward/runner.py`; `tests/integration/test_leakage.py`; `tests/integration/test_walk_forward.py`; `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Gap | No registered-run Phase 0 leakage packet proving the temporal-shuffling audit on an approved dataset/window; temporal-shuffling semantics are not yet packaged as gate evidence |
| Status | `BLOCKED_EVIDENCE_PARTIAL_IMPLEMENTATION` |
| Blocker class | Hard blocker before Phase 0 gate approval |
| Owner | strategist/codex |
| Closure path | Define the gate leakage packet shape, run it through registered RunRecords, and attach machine-checkable evidence before P0.5-009 |
| Next task link | P0.5-008 for reality sync; P0.5-009 for gate packet assembly |

### EC-02: SimBroker Bid/Ask Calibration

| Field | Value |
|-------|-------|
| Canonical criterion | SimBroker fills within 15% of market bid/ask data on >=100 manually verified fills across representative assets |
| Current implementation/evidence | T15 cost model, T16 fill engine, and T17 bid/ask provider interface exist; fixture/synthetic tests pass |
| Current artifacts | `entropy/simbroker/costs.py`; `entropy/simbroker/fills.py`; SimBroker tests listed in `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Gap | No approved quote source, no manually verified fill sample, no >=100-fill comparison table, no deviation report, and no acceptance packet |
| Status | `BLOCKED_MISSING_EVIDENCE` |
| Blocker class | Hard blocker before Phase 0 gate approval |
| Owner | strategist/human for source approval; codex later if implementation is approved |
| Closure path | P0.5-006 defines the evidence plan; future work must approve source/provider boundaries and produce the >=100-fill packet |
| Next task link | Future calibration implementation/evidence task |

### EC-03: Trial Registry Operational

| Field | Value |
|-------|-------|
| Canonical criterion | Trial registry operational: every test run logged with parameters, data hash, date, result |
| Current implementation/evidence | T05 domain models, T07 schema, T08 hashes, T09 write path, T10 readiness gate, T11 read path, and T20 RunRecord persistence exist |
| Current artifacts | `entropy/models.py`; `entropy/registry/`; `entropy/hashing.py`; migration files; registry tests in `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Gap | Implementation is substantially present, but the Phase 0 gate still needs a packet showing the actual gate-relevant runs are logged with required parameters, hashes, dates, and results |
| Status | `IMPLEMENTED_PACKET_REQUIRED` |
| Blocker class | Gate-packet blocker, not an architecture blocker |
| Owner | codex/strategist |
| Closure path | Include registered-run extracts and reproducibility hashes in the final Phase 0 gate packet |
| Next task link | P0.5-009 |

### EC-04: Data Pipeline 90-Day Stability

| Field | Value |
|-------|-------|
| Canonical criterion | Data pipeline stable: zero unexplained gaps in target universe over >=90 continuous days of feed monitoring |
| Current implementation/evidence | T12 provider abstraction, T13 local fixture adapter, and T14 data quality checks exist; fixture tests pass |
| Current artifacts | `entropy/data/`; data-pipeline tests listed in `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Gap | No approved live or near-live provider, no target-universe monitoring run, no 90 continuous days of feed evidence, no unexplained-gap disposition log |
| Status | `BLOCKED_MISSING_EVIDENCE` |
| Blocker class | Hard blocker before Phase 0 gate approval unless a charter-level review revises the criterion |
| Owner | human for provider/source approval; strategist/codex for monitoring plan |
| Closure path | P0.5-007 defines the monitoring plan, artifact schema, gap disposition policy, and provider boundary; future work must collect a real 90-day packet |
| Next task link | Future data-stability monitoring implementation/evidence task |

### EC-05: P4 Historical Regime Labels

| Field | Value |
|-------|-------|
| Canonical criterion | P4 weekly regime signal produces historically labeled regime series covering >=3 years of 1D data on >=15 of 20 target assets |
| Current implementation/evidence | Deterministic `P4-RBL-v1` is specified in core docs; runtime labeler and label artifacts are not implemented |
| Current artifacts | `products/entropy-core/docs/core/PROTOCOL_SPEC.md` Deterministic P4 Protocol; `products/entropy-core/docs/core/CHARTER.md`; `products/entropy-core/docs/core/GLOSSARY.md` |
| Gap | No P4 labeler module, no label-vintage artifact generation, no approved 20-asset universe snapshot, no >=3-year 1D label set, no >=15-of-20 coverage evidence |
| Status | `BLOCKED_MISSING_IMPLEMENTATION_AND_EVIDENCE` |
| Blocker class | Hard blocker or charter-level revision before Phase 0 gate approval |
| Owner | strategist/human first; codex later if implementation is selected |
| Closure path | D-024 selects implementation/evidence path: implement `P4-RBL-v1` and produce >=3 years/15 assets label evidence before Phase 1 |
| Next task link | Future P4 implementation/evidence task after Phase 0.5 evidence plans |

### EC-06: P1 DD Circuit Breaker

| Field | Value |
|-------|-------|
| Canonical criterion | DD circuit breaker (P1) logic implemented, tested with synthetic data, and verified |
| Current implementation/evidence | T22 governance state machine implements deterministic P1 trip/reset and new-position blocking under D-018; synthetic tests pass |
| Current artifacts | `entropy/governance/state_machine.py`; `tests/unit/test_governance.py`; `products/entropy-core/docs/audit/T22_GOVERNANCE_DISPOSITION.md`; `products/entropy-core/docs/EVIDENCE_INDEX.md` |
| Gap | Needs to be included in the final gate packet with test references and verification baseline |
| Status | `IMPLEMENTED_PACKET_REQUIRED` |
| Blocker class | Gate-packet blocker only |
| Owner | codex/strategist |
| Closure path | Carry T22 evidence into P0.5-009; no new runtime architecture decision required for P1 itself |
| Next task link | P0.5-009 |

## Pre-Phase 1 Operational Confirmations

The Growth Layer items below are not additional Phase 0 exit criteria, but the
protocol says they must be operationally confirmed before Phase 1 is declared
started.

| Requirement | Current state | Gap | Status | Closure path |
|-------------|---------------|-----|--------|--------------|
| Cost & Execution Monitor / CRR support | FillLog supports estimated slippage, actual slippage, and cost components through SimBroker instrumentation | Need evidence packet showing CRR fields are populated in representative gate runs | `IMPLEMENTED_PACKET_REQUIRED` | Include in P0.5-009 and later SimBroker calibration packet |
| Capital Utilization Monitor | No dedicated Phase 1 utilization monitor module in current Phase 0 runtime | Need policy/artifact plan before Phase 1 starts; target 40-70% band is policy | `PRE_PHASE1_CONFIRMATION_REQUIRED` | Cover in P0.5-008 reality sync or future pre-Phase-1 task |
| Diversification Controller / daily correlation update | P3 governance state exists; no full diversification controller evidence | Need operational confirmation of daily correlation update path before Phase 1 starts | `PRE_PHASE1_CONFIRMATION_REQUIRED` | Cover in P0.5-008 reality sync or future pre-Phase-1 task |

## Priority Matrix

| Priority | Items | Rationale |
|----------|-------|-----------|
| P0 hard gate blockers | EC-02 SimBroker calibration; EC-04 90-day data stability; EC-05 P4 labels or charter revision | These are explicit Phase 0 exit criteria with no current gate evidence |
| P0 evidence blockers | EC-01 registered leakage/temporal-shuffling packet | Implementation exists, but current evidence is not yet the gate packet required by the protocol |
| Packet-required implemented items | EC-03 Trial Registry; EC-06 P1 DD circuit breaker; CRR field support | Implementation appears present, but the Phase 0 gate still needs a formal evidence packet |
| Formula/evidence debt adjacent to gate | Sharpe CI, Harvey-Liu, N_eff/K3, purge/embargo, F-30, F-31 | These do not all map one-to-one to the six Phase 0 exit criteria, but they can contaminate reports and downstream claims if left ambiguous |

## Required Next Actions

1. Use `products/entropy-core/docs/audit/FORMULA_EVIDENCE_DEBT.md` as the canonical ranking of
   formula/evidence debt.
2. Resolve the P4 gate decision path: implement/evidence the labeler or open a
   charter-level review.
3. Produce SimBroker and data-stability evidence plans before collecting
   external/provider-dependent evidence.
4. Keep Phase 1 implementation blocked until P0.5-009 records a human gate
   decision.

## Decision Boundary

This register supports Phase 0.5 execution only. It does not approve Phase 0,
does not authorize Phase 1, does not validate T23 statistical stubs, and does
not close F-30/F-31.
