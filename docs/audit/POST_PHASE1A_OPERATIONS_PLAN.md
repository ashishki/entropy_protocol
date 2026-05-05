# Post-Phase-1A Operations Plan

Date: 2026-05-05
Status: `CODE_BLOCK_COMPLETE_PENDING_HUMAN_REVIEW`
Decision: `OPEN_PHASE1B_CODE_CLOSURE_REVIEW`

## Classification

This is not full Phase 1 evaluation/trading.

The next block is `Phase 1B — Long-Only Baseline Readiness Planning`. It belongs
to the Phase 1 workstream because it prepares the long-only baseline path, but
it remains pre-evaluation and non-claim until a separate human gate approves
Phase 1 implementation/evaluation.

## Why This Is Not Full Phase 1 Yet

Full Phase 1 means evaluating the long-only baseline through the governed
walk-forward/OOS path with admissible reports and phase-gate implications.

The current approved work is narrower:

- define the ordered operations;
- preserve archive split and holdout boundaries;
- prepare implementation and benchmark readiness;
- identify required gates before any evaluation;
- avoid OOS/performance, production, or capital-ready claims.

## Priority Order

| Priority | Task | Purpose | Output | Still forbidden |
|---|---|---|---|---|
| P0 | Phase taxonomy and gate map | Make clear what is Phase 1 readiness vs Phase 1 evaluation | Current-state task graph and handoff docs | Evaluation/trading/claims |
| P1 | Long-only baseline operations graph | Turn the next work into ordered tasks with dependencies | `docs/tasks.md` Phase 1B section | Alpha execution and backtest |
| P2 | Baseline implementation surface | Define interfaces, inputs, outputs, no-claim labels, and tests before code | `entropy/baseline/long_only.py` | Strategy performance metrics |
| P3 | Formation adapter and skill stubs | Prepare formation-only inputs and schema-only outputs | `entropy/baseline/features.py`, `formation.py`, `skills.py` | Alpha execution and validation/holdout reads |
| P4 | Mechanics benchmark | Record non-claim runtime/memory facts on synthetic formation-safe rows | `PHASE1B-BASELINE-SURFACE-BENCHMARK-v1` | Runtime escalation without ADR |
| P5 | Human closure gate | Decide whether to open the next bounded block | Explicit approval | Holdout/OOS/live/capital claims |

## Proposed Task Graph

### P1B-001 Phase Taxonomy And Gate Map

Objective: define terminology and gates:

- `Phase 1A`: archive-only baseline planning and scaffold/probe foundation;
- `Phase 1B`: long-only baseline readiness planning, no evaluation;
- `Phase 1 Implementation`: code path for baseline logic, only after explicit
  approval;
- `Phase 1 Evaluation`: governed walk-forward/OOS evaluation, only after a
  separate explicit gate;
- `Phase 1 Exit`: phase-gate claim, never automatic.

### P1B-002 Long-Only Baseline Operations Graph

Objective: convert the plan into ordered implementation/planning tasks with
dependencies, acceptance criteria, tests, and no-claim boundaries.

### P1B-003 Baseline Implementation Surface

Objective: define the bounded baseline implementation surface before code:

- allowed data splits;
- skill-family placeholder-to-implementation transition rules;
- Trial Registry/spec references;
- output schema;
- no performance claim fields;
- tests required before code can be considered complete.

### P1B-004 Baseline Formation Input Adapter

Objective: implement formation-only input preparation with strict feature
schema guards, deterministic sorting, replay hashes, and no claim fields.

### P1B-005 Baseline Skill Stub Outputs

Objective: implement schema-only no-claim outputs for all registered skill
families without alpha, score, weight, position, P&L, return, or metric fields.

### P1B-006 Baseline Mechanics Benchmark

Objective: implement a deterministic synthetic mechanics benchmark over the
surface, adapter, and stubs without strategy-performance interpretation.

### Future Evaluation Readiness Checklist

Objective: define the exact checklist that must be complete before any Phase 1
evaluation run:

- registered trial/spec status;
- leakage checklist requirements;
- walk-forward configuration;
- SimBroker/calibration status;
- statistical report fields;
- multiplicity/family accounting;
- holdout policy;
- human approval requirement.

### P1B-HUMAN-001 Phase 1B Code Closure Review

Objective: Spec Owner reviews the completed bounded Phase 1B readiness code
block and decides what, if anything, may begin next.

This gate still must not approve:

- Phase 1 evaluation;
- holdout read/unlock;
- portfolio/backtest evaluation;
- live feeds or broker integration;
- Growth/RDL/RBE activation;
- non-Python runtime/toolchain introduction;
- OOS/performance, production, or capital-ready claims.

## Operational Rule

Move task-by-task. After each code task, run light review, targeted tests, and
ruff/pyright when relevant. After a large block, run the deep review protocol
again before opening the next block.

## Current Recommendation

Open `P1B-HUMAN-001 Phase 1B Code Closure Review` next.
