# Archive-Only Continuation Decision

Date: 2026-05-05
Decision ID: D-028
Task: PSR-003
Status: APPROVED

## Decision

Proceed to **Phase 1A Archive-Only Baseline Planning and Instrumentation**.

Do not start live monitoring, live trading, streaming provider work, RDL
hypothesis generation, Growth Layer escalation, or OOS/performance claims.

## Rationale

The archive-only Phase 0 research foundation is now closed for the current
scope: P4 evidence, SimBroker calibration evidence, archive data-stability
evidence, leakage/temporal-shuffling, purge/embargo methodology, statistical
report boundaries, registry evidence, and P1 governance evidence are all
packaged.

The next useful step is not another Phase 0 evidence loop and not live
operation. The protocol's next structural target is Phase 1 Long-Only Baseline,
but it must be entered through an archive-only planning and instrumentation
stage so that trial registration, dataset freeze, skill boundaries, portfolio
constraints, Growth Layer monitoring requirements, and no-claim reporting rules
are explicit before any strategy implementation.

## Rejected Options

| Option | Decision | Reason |
|---|---|---|
| Continue live data-stability monitoring now | Rejected | Owner scoped current work to archives only; live evidence is a future hard gate |
| Start Phase 1 implementation immediately | Rejected | Phase 1 needs a task graph and frozen archive evaluation contract first |
| Start RDL work | Rejected | RDL is dormant until Phase 2; pre-Phase-2 work may only be scaffolding after explicit task approval |
| Start Growth Layer/RBE escalation | Rejected | Growth Layer monitoring may be instrumented, but escalation remains locked |
| Reopen Phase 0 evidence collection | Rejected | Archive-only foundation closure has enough evidence for strategist continuation |

## Phase 1A Objective

Create the archive-only entry contract for Phase 1 Long-Only Baseline:

- define admissible archive datasets and freeze rules;
- define baseline long-only skill boundaries before any skill code;
- define portfolio-layer constraints for archive simulation;
- map Growth Layer monitoring requirements that must exist before Phase 1 is
  declared started;
- preserve RDL dormancy and no-live/no-OOS-claim boundaries;
- produce a task graph that can be implemented incrementally with tests.

## First Task

Start `P1A-001: Phase 1 Archive Entry Contract`.

This task should be documentation/design only unless it discovers a small
existing-code sync that is required to make the contract testable.

## Boundary

Phase 1A authorizes archive-only planning and instrumentation. It does not
authorize live capital, live feeds, streaming providers, live broker
integration, OOS/performance claims, RDL portfolio influence, RBE activation, or
automatic phase-gate approval.

