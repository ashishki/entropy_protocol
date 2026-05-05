# NEXT_PHASE_PLAN
_Date: 2026-05-05 · Approved next stage: Phase 0.5 Foundation Closure and Evidence Hardening_

## Strategic Decision

PSR-002 decision: proceed to Phase 0.5, not Phase 1.

T01-T24 are accepted as the implementation foundation baseline, with 135 passing
tests. The Phase 0 gate remains `NOT_APPROVED`.

Canonical decision artifact: `docs/audit/PHASE0_STRATEGIC_DECISION.md`.

## Why Phase 0.5

The completed foundation is aligned with the protocol and architecture, but the
core Phase 0 exit criteria require evidence beyond fixture/synthetic tests:

- SimBroker calibration against >=100 manually verified market bid/ask fills;
- >=90 continuous days of stable data feed monitoring;
- P4 labels covering >=3 years of 1D data on >=15 of 20 target assets;
- real registered-run leakage/gate evidence, not only implementation tests;
- accepted formula/evidence dispositions for provisional statistical surfaces.

Starting Phase 1 now would confuse implementation evidence with research
validation. Replanning the architecture is not warranted because the deterministic
Python/T1 architecture remains aligned with the protocol.

## Stage Objective

Convert the T01-T24 foundation into a gate-ready Phase 0 package, or produce a
formal charter-level decision for any Phase 0 exit criterion that will be revised
before Phase 1.

## Boundaries / Non-Goals

- No Phase 1 implementation.
- No live capital.
- No production trading.
- No OOS performance claim.
- No paper result labeled as OOS.
- No use of T23 stubs as validated formulas.
- No synthetic closure of F-30/F-31.
- No RDL portfolio influence or RDL promotion telemetry closure.
- No K-report closure without generated K-report artifacts.
- No external data provider activation by default.
- No non-Python language/runtime escalation without D-012 evidence and ADR.

## Task List

### P0.5-001: Phase 0 Exit Criteria Gap Register

Owner: strategist  
Depends-On: PSR-002  
Type: documentation/audit

Objective:

Map every core Phase 0 exit criterion to current evidence, missing evidence,
owner, artifact path, and blocker status.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/PHASE0_EXIT_GAP_REGISTER.md` — complete
- `docs/EVIDENCE_INDEX.md` points to the register — complete
- `docs/CODEX_PROMPT.md` names the next approved task — complete; next task is P0.5-002

### P0.5-002: Formula And Evidence Debt Register

Owner: strategist  
Depends-On: P0.5-001  
Type: documentation/audit

Objective:

Rank unresolved surfaces by gate impact: Harvey-Liu, Sharpe CI, N_eff/K3,
purge/embargo, P4, F-30, and F-31.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/FORMULA_EVIDENCE_DEBT.md` — complete
- clear block/non-block disposition for Phase 1 planning and Phase 1
  implementation — complete; P0.5-003 is next

### P0.5-003: Sharpe CI And Harvey-Liu Review Packets

Owner: strategist/reviewer  
Depends-On: P0.5-002  
Type: formula audit

Objective:

Independently review `CI-SR-ACF-v1` and `HL-HB-v1`, including worked examples,
required report fields, and failure cases.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/SHARPE_CI_REVIEW.md` — complete; `CI-SR-ACF-v1` requires revision before gate/report use
- `docs/audit/HARVEY_LIU_REVIEW.md` — complete; `HL-HB-v1` is blocked for gate use
- decision-log entry accepting, revising, or blocking each helper — complete in D-022

### P0.5-004: Purge/Embargo Design Decision

Owner: strategist/reviewer  
Depends-On: P0.5-002  
Type: formula/design audit

Objective:

Resolve the temporary N-consecutive-bar embargo assumption or explicitly keep it
as a blocker for Phase 1 OOS claims.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/PURGE_EMBARGO_DECISION.md` — complete
- downstream task entries if splitter changes are required — no immediate code change required; future methodology task required before Phase 1 OOS claims

### P0.5-005: P4 Labeler Gate Decision

Owner: strategist/human  
Depends-On: P0.5-001  
Type: gate decision

Objective:

Decide whether to implement/evidence `P4-RBL-v1` before Phase 1 or run a
charter-level review to revise the Phase 0 exit criterion.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/P4_GATE_DECISION.md` — complete; implementation/evidence selected
- if implementation is selected later: label artifacts covering >=3 years of 1D
  data on >=15 of 20 target assets — required future evidence before Phase 0 gate approval

### P0.5-006: SimBroker Calibration Evidence Plan

Owner: strategist/codex later if approved  
Depends-On: P0.5-001  
Type: evidence design

Objective:

Define how to produce the >=100 manually verified bid/ask fill checks and the
15% accuracy acceptance packet.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/SIMBROKER_CALIBRATION_PLAN.md` — complete
- future calibration evidence table schema — complete
- provider/source approval if external quotes are required — required later; no provider activated by this plan

### P0.5-007: Data Pipeline Stability Plan

Owner: strategist/human  
Depends-On: P0.5-001  
Type: evidence design

Objective:

Define how to satisfy >=90 continuous days of feed monitoring without
contaminating Phase 1 or making performance claims.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/DATA_STABILITY_PLAN.md` — complete
- provider approval decision if external egress is required — required later; no provider activated by this plan
- future 90-day monitoring artifact format — complete

### P0.5-008: Architecture And Spec Reality Sync

Owner: codex  
Depends-On: P0.5-001, P0.5-002  
Type: documentation

Objective:

Update implementation-facing docs to reflect that T01-T24 are complete but Phase
0 is not gate-approved, and mark provisional surfaces explicitly.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/ARCHITECTURE.md` updated with Phase 0.5 status — complete
- `docs/spec.md` updated with implemented/provisional/gate-missing status — complete
- `docs/tasks.md` updated with executable Phase 0.5 task graph — complete
- `docs/EVIDENCE_INDEX.md` updated with Phase 0.5 evidence expectations — complete

### P0.5-009: Phase 0 Gate Packet

Owner: strategist/human  
Depends-On: P0.5-003, P0.5-004, P0.5-005, P0.5-006, P0.5-007, P0.5-008  
Type: gate review

Objective:

Assemble the final Phase 0 gate packet and record the human approval, rejection,
or reshape decision.

Status: complete on 2026-05-05.

Acceptance evidence:

- `docs/audit/PHASE0_GATE_PACKET.md` — complete
- `docs/DECISION_LOG.md` gate decision entry — complete in D-025
- `docs/CODEX_PROMPT.md` updated to the first approved post-gate task — complete; next task is P0.6-001

## Required Documents

Create or update during Phase 0.5:

- `docs/audit/PHASE0_EXIT_GAP_REGISTER.md`
- `docs/audit/FORMULA_EVIDENCE_DEBT.md`
- `docs/audit/SHARPE_CI_REVIEW.md`
- `docs/audit/HARVEY_LIU_REVIEW.md`
- `docs/audit/PURGE_EMBARGO_DECISION.md`
- `docs/audit/P4_GATE_DECISION.md`
- `docs/audit/SIMBROKER_CALIBRATION_PLAN.md`
- `docs/audit/DATA_STABILITY_PLAN.md`
- `docs/audit/PHASE0_GATE_PACKET.md`
- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/tasks.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/CODEX_PROMPT.md`
- `docs/DECISION_LOG.md`

## Evidence Required Before Phase 0 Gate Approval

- Current full test baseline remains at or above 135 passing tests.
- Ruff and pyright remain passing.
- Phase 0 exit gap register is complete.
- Formula/evidence debt register is complete.
- Sharpe CI and Harvey-Liu review packets have accepted dispositions.
- Purge/embargo design has accepted disposition.
- P4 gate criterion is satisfied or formally revised through charter-level
  review.
- SimBroker calibration evidence exists for the >=100 bid/ask checks.
- Data stability evidence exists for the >=90-day feed monitoring criterion.
- No synthetic evidence is used to close F-30 or F-31.
- Human gate decision is recorded.

## Conditions Before Moving Further

Phase 1 planning may begin only after the Phase 0.5 gap/debt registers and
reality-sync docs are complete enough to produce a clean task graph.

Phase 1 implementation may begin only after the Phase 0 gate is approved, or a
formal charter-level review revises the relevant Phase 0 exit criteria.

Any future Phase 1 task prompt must state explicitly:

- no live capital;
- no OOS/performance claim beyond approved evidence labels;
- no formula stub treated as validated;
- no RDL/K-report closure unless real generated artifacts exist.

## Proposed Next Action

Start P0.6-001: implement deterministic `P4-RBL-v1` labeler without provider
activation, Phase 1 implementation, or performance claims.
