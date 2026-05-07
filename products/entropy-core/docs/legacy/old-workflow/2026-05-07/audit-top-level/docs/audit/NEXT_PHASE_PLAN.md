# NEXT_PHASE_PLAN

**Date:** 2026-05-06
**Status:** Proposed — pending Spec Owner decision
**Source:** `POST_DK_STRATEGY_REVIEW.md`

## Proposed Next Block

`P0C Phase 0 Exit Evidence And D-K Admission Planning`

Objective:
Create a compact, auditable bridge from D-K fix closure to the next admissible
development block by:

- accepting or rejecting D-K fix closure;
- reconciling phase/current-state language;
- producing a Phase 0 exit evidence matrix;
- deciding which evidence gaps block future Phase 1/OOS labels;
- designing, but not yet executing, D-K admission into the main control plane.

## Required First Gate

### SO-DK-001 — Spec Owner D-K Fix Closure Decision

Allowed outputs:

- accept D-K fix closure and open P0C;
- reject D-K fix closure and route remediation;
- stop after D-K closure;
- request a narrower strategy review.

Acceptance criteria:

- F-DK-001/F-DK-002/F-DK-003 acceptance status recorded.
- D-K evidence disposition recorded as `archive_only_research_evidence`.
- Holdout, live, production, capital-ready, Growth/RDL/RBE, and performance
  claims remain blocked unless separately gated.

## Proposed P0C Task Shape

### P0C-001 — Current-State And Phase Semantics Sync

Objective:
Update `products/entropy-core/docs/ARCHITECTURE.md` and `products/entropy-core/docs/spec.md` current-state prose from
post-Phase1A to post-D-K fix closure without changing frozen protocol rules.

Acceptance criteria:

- Docs state D-K completed as archive-only/no-claim evidence.
- Docs state Phase 0 exit remains the prerequisite for any real Phase 1 OOS
  label.
- No production, capital-ready, live, holdout, or performance claim is added.

### P0C-002 — Phase 0 Exit Evidence Matrix

Objective:
Produce a matrix for canonical Phase 0 exit criteria.

Required rows:

- walk-forward leakage audit;
- SimBroker 100-fill calibration;
- Trial Registry operationality;
- 90-day data pipeline stability;
- P4 labels over >=3 years / >=15 assets;
- P1 DD circuit breaker.

Each row must include:

- `implemented`;
- `tested`;
- `evidence_present`;
- `human_acceptance_needed`;
- `blocked`;
- evidence pointer;
- missing task if any.

### P0C-003 — D-K Evidence Disposition Packet

Objective:
State exactly what D-K artifacts are and are not.

Acceptance criteria:

- D-K artifacts are classified as archive-only research/admission scaffolding.
- D-K artifacts are not OOS, not validation performance, not production, not
  capital-ready, and not a holdout trigger.
- P1I no-computation stat semantics remain explicit.

### P0C-004 — Phase 0 Evidence Gap Closure Plan

Objective:
Turn P0C-002 gaps into a minimal task sequence.

Expected outputs:

- proposed tasks for missing evidence;
- blocker status for each Phase 0 criterion;
- explicit decision whether a Phase 0 closure implementation block is ready to
  open.

### P0C-005 — D-K Control-Plane Admission Design

Objective:
Design the future bridge from D-K packet surfaces into the main architecture.
This task is design/contract only unless the Spec Owner separately opens
implementation.

Surfaces to design:

- Trial Registry admission for `Phase1FPreRegistrationSurface.trial_spec`;
- governance approval event before READY;
- validation read authorization bridge from registered metadata;
- persisted P1H `RunRecord`;
- evidence collector integration;
- baseline adapter contract that explains how P1E bounded observations would
  become future `WalkForwardStrategy` inputs without performance claims.

### P0C-006 — Strategy Closure Review

Objective:
Review P0C outputs and choose the next implementation block.

Allowed verdicts:

- `OPEN_PHASE0_EVIDENCE_CLOSURE_IMPLEMENTATION`;
- `OPEN_DK_CONTROL_PLANE_BRIDGE_IMPLEMENTATION`;
- `REMAIN_BLOCKED_PENDING_HUMAN_EVIDENCE`;
- `STOP_OR_ITERATE`.

## Forbidden During P0C

- OOS/performance/validated-alpha claims;
- holdout unlock or holdout reads;
- live feeds as a production dependency;
- broker integration or capital deployment;
- portfolio allocation as active trading logic;
- Growth/RDL/RBE activation;
- Phase 2 / 1W overlay;
- shorts, treasury, or CCA live influence;
- non-Python runtime escalation without benchmark evidence, ADR, task/CI
  updates, and explicit human approval.

## Evidence Requirements For Any Later Bridge Implementation

If P0C later opens D-K control-plane bridge implementation, require:

- TrialSpec hash/family/parameter-lock preservation tests;
- append-only Trial Registry/governance DB tests;
- approval-required-before-READY test;
- validation-read-only-with-registration test;
- forged holdout request rejection test;
- persisted RunRecord test;
- evidence collector test for registered run/leakage report only;
- regression test that no report exposes net Sharpe, drawdown, OOS claim,
  production label, or capital-ready label before a later explicit gate.
