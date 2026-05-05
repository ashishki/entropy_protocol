# PHASE0_STRATEGIC_DECISION
_Date: 2026-05-05 · Scope: PSR-002 strategic decision after T01-T24_

## Decision

Decision: proceed to **Phase 0.5 Foundation Closure and Evidence Hardening**.

T01-T24 are accepted as the current implementation foundation baseline. The
formal Phase 0 gate is **not approved**. Phase 1 must not start automatically.

This is a strategic acceptance of the foundation as useful infrastructure, not a
claim that Phase 0 exit criteria are fully satisfied.

## Decision Status

| Item | Status |
|------|--------|
| T01-T24 implementation foundation | Accepted as baseline |
| Test baseline | 135 passed with PostgreSQL 16 Docker container |
| Phase gate approval | `NOT_APPROVED` |
| Live capital | None |
| OOS performance claims | None |
| Formula validation claims | None |
| Next stage | Phase 0.5 hardening before Phase 1 |

## Documents Reviewed

- `docs/core/PROTOCOL_SPEC.md`
- `docs/core/CHARTER.md`
- `docs/core/GLOSSARY.md`
- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/tasks.md`
- `docs/CODEX_PROMPT.md`
- `docs/audit/REVIEW_REPORT.md`
- `docs/audit/PHASE0_FOUNDATION_REVIEW.md`
- `docs/audit/POST_PHASE_STRATEGY_REVIEW.md`
- `docs/audit/NEXT_PHASE_PLAN.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`

## What Actually Exists After T01-T24

The current system has a coherent deterministic foundation:

- project package, CI spec, smoke tests, CLI health boundary;
- Pydantic domain models for market, registry, run, fill, and performance data;
- PostgreSQL schema, Alembic migration, and rollback-safe integration tests;
- deterministic dataset, run, and policy hashing;
- append-only Trial Registry write/read paths and Experiment Readiness Gate;
- local fixture ingestion to deterministic Parquet plus data quality checks;
- SimBroker cost, fill, and calibration interface surfaces;
- single-split walk-forward runner with leakage checklist gating before OOS;
- four-stream P&L attribution with stream (d) excluded from Net Sharpe;
- deterministic P1/P3 governance state machine with append-only events;
- provisional statistical helper stubs for Sharpe CI, Harvey-Liu, and N_eff;
- deterministic implementation-evidence artifacts with `NOT_APPROVED` default.

This is sufficient implementation evidence for a foundation checkpoint. It is
not sufficient research evidence for Phase 1 or for any OOS performance claim.

## Fit Against Protocol Strategy

Verdict: **aligned but not gate-complete**.

The foundation supports the core strategy in three important ways:

- It implements the "evaluation engine first" posture from NN-3.
- It creates preregistration, hashing, leakage, and attribution boundaries before
  any trading-edge claim.
- It preserves human approval boundaries and avoids automatic phase-gate
  approval.

The gap is that the protocol's Phase 0 exit criteria are stronger than the
T01-T24 implementation acceptance criteria. Current tests prove that the
machinery exists and behaves deterministically on fixtures and synthetic cases.
They do not prove that the machinery has produced the real operating evidence
required by the core spec.

## Phase 0 Exit Criteria Gap

| Core Phase 0 Exit Criterion | Current State | Decision |
|-----------------------------|---------------|----------|
| Walk-forward harness passes leakage audit with zero forward-looking features verified by temporal shuffling | Leakage checklist and OOS block implemented; synthetic detector tests pass | Needs real registered-run leakage evidence and temporal-shuffling audit semantics before gate approval |
| SimBroker fills within 15% of market bid/ask data on >=100 manually verified fills | Cost/fill engine and bid/ask provider interface exist; no real calibration evidence | Hard blocker before Phase 0 gate approval |
| Trial registry operational with every test run logged with parameters, data hash, date, result | Append-only registry, hashes, readiness gate, and run metadata exist | Substantially satisfied for implementation baseline; needs gate packet evidence |
| Data pipeline stable with zero unexplained gaps over >=90 continuous days of feed monitoring | Local fixture ingestion and data quality checks exist; no 90-day monitoring evidence | Hard blocker before Phase 0 gate approval unless charter-level exit criterion is revised |
| P4 weekly regime signal produces >=3 years of 1D labels on >=15 of 20 assets | P4 remains out of current implementation scope; deterministic spec exists | Hard blocker or charter-level waiver required before Phase 1 |
| P1 DD circuit breaker implemented, synthetic-tested, and verified | P1 implemented and synthetic tests pass under D-018 | Satisfied for implementation baseline |

## Option Analysis

### Option A: Start Phase 1 Now

Decision: **reject**.

Reason:

- Phase 0 gate is still `NOT_APPROVED`.
- Several core Phase 0 exit criteria lack real evidence.
- Sharpe CI, Harvey-Liu, N_eff/K3, purge/embargo, and P4 remain provisional or
  unimplemented surfaces.
- Starting Phase 1 would create pressure to interpret fixture/synthetic evidence
  as research validation.

### Option B: Phase 0.5 Foundation Closure and Evidence Hardening

Decision: **select**.

Reason:

- It preserves the implemented foundation without overstating it.
- It directly targets the gap between implementation evidence and protocol exit
  evidence.
- It allows formula/evidence debt to be resolved before downstream reports rely
  on it.
- It keeps Phase 1 sequencing intact and avoids OOS/performance claims.

### Option C: Additional Audit/Research Stage Only

Decision: **reject as standalone; include as a Phase 0.5 workstream**.

Reason:

- Formula review and external research are necessary, but audit alone will not
  produce data stability evidence, SimBroker calibration evidence, P4 labels, or
  a gate packet.
- A pure research stage would leave the executable task graph unclear.

### Option D: Architecture Replanning

Decision: **reject**.

Reason:

- The current architecture is aligned with the protocol: Python/T1,
  deterministic runtime, no LLM path, append-only registry, human gates, and
  no external egress in Phase 0.
- The problem is not architectural direction. The problem is incomplete exit
  evidence and provisional formulas.

### Option E: Approve Phase 0 Gate With Caveats

Decision: **reject**.

Reason:

- Caveated approval would blur the protocol distinction between implementation
  foundation and gate evidence.
- The core spec says there is no partial Phase 0.

## Selected Stage: Phase 0.5

### Objective

Convert the T01-T24 foundation into a gate-ready Phase 0 package or produce a
formal charter-level decision explaining why any original Phase 0 exit criterion
is being revised.

### Boundaries / Non-Goals

- No Phase 1 implementation.
- No live capital.
- No production trading.
- No OOS performance claims.
- No paper results represented as OOS.
- No use of statistical stubs as validated formulas.
- No synthetic closure of F-30 or F-31.
- No RDL portfolio influence or RDL promotion telemetry closure.
- No K-report closure without generated K-report artifacts.
- No non-Python runtime/language escalation without D-012 benchmark and ADR.
- No external data provider activation by default; any provider egress requires
  explicit approval and a narrow task.

## Phase 0.5 Task Plan

### P0.5-001: Phase 0 Exit Criteria Gap Register

Create a gate checklist mapping every core Phase 0 exit criterion to current
evidence, missing evidence, owner, artifact path, and blocker status.

Evidence:

- `docs/audit/PHASE0_EXIT_GAP_REGISTER.md`
- updates to `docs/EVIDENCE_INDEX.md`

### P0.5-002: Formula And Evidence Debt Register

Rank unresolved surfaces by gate impact: Harvey-Liu, Sharpe CI, N_eff/K3,
purge/embargo, P4, F-30, and F-31.

Evidence:

- `docs/audit/FORMULA_EVIDENCE_DEBT.md`
- explicit block/non-block disposition for Phase 1 entry

### P0.5-003: Sharpe CI And Harvey-Liu Review Packets

Produce independent reproducibility packets for `CI-SR-ACF-v1` and `HL-HB-v1`,
including worked examples, report fields, and failure cases.

Evidence:

- `docs/audit/SHARPE_CI_REVIEW.md`
- `docs/audit/HARVEY_LIU_REVIEW.md`
- decision-log entries accepting, revising, or rejecting the helpers

### P0.5-004: Purge/Embargo And Walk-Forward Design Decision

Replace or explicitly retain the temporary N-consecutive-bar embargo assumption
with a canonical derivation tied to holding period, feature lookback, and bar
frequency.

Evidence:

- `docs/audit/PURGE_EMBARGO_DECISION.md`
- task graph updates for any required splitter changes

### P0.5-005: P4 Labeler Gate Decision

Decide whether to implement `P4-RBL-v1` before Phase 1 or seek a charter-level
revision of the Phase 0 exit criterion. The default is implementation/evidence,
because phase exit criteria are frozen unless formally reviewed.

Evidence:

- `docs/audit/P4_GATE_DECISION.md`
- if implementation proceeds later: label artifacts covering >=3 years of 1D
  data on >=15 of 20 target assets

### P0.5-006: SimBroker Calibration Evidence Plan

Define the evidence path for the >=100 manually verified bid/ask fill checks and
the acceptance packet for the 15% accuracy threshold.

Evidence:

- `docs/audit/SIMBROKER_CALIBRATION_PLAN.md`
- future calibration evidence table with quote source, fill scenario, expected
  fill, simulated fill, deviation, and reviewer

### P0.5-007: Data Pipeline Stability Plan

Define how the project will satisfy the >=90 continuous days of feed monitoring
criterion without contaminating Phase 1 or making performance claims.

Evidence:

- `docs/audit/DATA_STABILITY_PLAN.md`
- provider approval decision if external egress becomes necessary
- future 90-day gap-monitoring artifact

### P0.5-008: Architecture And Spec Reality Sync

Update non-core implementation docs to reflect that T01-T24 are complete but
Phase 0 is not gate-approved, and mark provisional surfaces explicitly.

Evidence:

- updates to `docs/ARCHITECTURE.md`
- updates to `docs/spec.md`
- updates to `docs/tasks.md`
- updates to `docs/EVIDENCE_INDEX.md`

### P0.5-009: Phase 0 Gate Packet

Assemble the final gate packet after the prior hardening artifacts exist.

Evidence:

- `docs/audit/PHASE0_GATE_PACKET.md`
- human approval or rejection recorded in `docs/DECISION_LOG.md`
- `docs/CODEX_PROMPT.md` updated to the first approved post-gate task

## Required Evidence Before Moving Beyond Phase 0.5

- Phase 0 exit gap register complete.
- Formula/evidence debt register complete.
- Sharpe CI and Harvey-Liu either independently accepted or explicitly blocked.
- Purge/embargo derivation accepted or its provisional status explicitly blocks
  Phase 1 OOS claims.
- P4 labeler criterion satisfied or formally revised by charter-level review.
- SimBroker calibration plan accepted and, before gate approval, calibration
  evidence produced.
- Data stability plan accepted and, before gate approval, monitoring evidence
  produced.
- Phase 0 gate packet reviewed by the human sponsor.

## Conditions For Phase 1 Planning

Phase 1 planning may begin only after P0.5-001 through P0.5-008 are complete
enough to define a clean task graph and the human sponsor explicitly accepts the
remaining blockers.

Phase 1 implementation may begin only after one of these is true:

1. all core Phase 0 exit criteria are evidenced and the Phase 0 gate is approved;
2. a charter-level review formally revises a Phase 0 exit criterion and records
   why proceeding remains protocol-safe.

In both cases, the Phase 1 task graph must preserve no-live-capital and
no-performance-claim boundaries until the Phase 1 protocol itself authorizes the
relevant evidence labels.

## Risks Reduced By This Decision

- Prevents premature Phase 1 start from a test-only foundation.
- Prevents stubs from becoming silently treated as formulas.
- Forces P4, SimBroker calibration, data stability, and purge/embargo gaps into
  named artifacts.
- Preserves frozen phase-gate discipline.
- Keeps RDL/K-report evidence gates honest.

## Risks Remaining

- Formula review may reject or materially revise current helper stubs.
- Real data provider selection may introduce quality, cost, or egress issues.
- The 90-day data stability criterion creates calendar-time latency.
- P4 implementation may expand Phase 0.5 more than desired unless a formal
  charter decision narrows the gate.
- Solo maintenance burden remains a strategic risk.
- F-30 and F-31 remain future hard gates for RDL promotion and K-report evidence.

## Final Ruling

`ACCEPT_FOUNDATION_WITH_CONSTRAINTS`.

The foundation is strategically useful and should be preserved. The next phase is
Phase 0.5 Foundation Closure and Evidence Hardening. Phase 1 remains
stop-shipped until the Phase 0 gate is approved or a formal charter-level
revision changes the gate criteria.
