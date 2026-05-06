# Phase 1A Development And Runtime Strategy

Date: 2026-05-05
Task: P1A-006
Status: `COMPLETE`
Decision: `DEFER_EXECUTABLE_SCAFFOLD_PENDING_WORKLOAD_STRATEGY`

## Executive Summary

Phase 1A has correctly built an archive-only planning foundation:

- P1A-001 froze the archive entry contract.
- P1A-002 froze the initial archive dataset manifest.
- P1A-003 created the archive split registration/read gate.
- P1A-004 registered the non-executable long-only baseline specification.
- P1A-005 closed the fix chain for a narrow scaffold only.

The next implementation should not proceed directly into executable baseline
scaffold. The protocol is moving toward workload-heavy simulation, hypothesis
testing, and walk-forward evaluation. If the system encodes the next layer as
Python object loops over bars, assets, fills, and trial variants, it can remain
protocol-correct while becoming too slow and expensive to operate.

Therefore the executable scaffold is deferred until the Phase 1A workload and
runtime strategy is explicit. Python remains the active implementation language
under the implementation contract, but Phase 1A must preserve clean boundaries
for columnar execution and later measured language escalation.

## What Has Been Built

Current completed artifacts are governance and evidence boundaries, not trading
or evaluation logic:

- archive-only dataset scope and split labels;
- immutable freeze and boundary manifests with hashes;
- validation-read metadata and locked holdout state;
- non-executable baseline skill-family specification;
- long-only/no-leverage portfolio constraints as registered specification
  shape;
- no-claim labels blocking live, OOS/performance, production, and capital-ready
  claims.

No executable alpha logic, allocation engine, backtest/evaluation run,
performance metric, live feed, Growth/RDL/RBE activation, or holdout read is
approved.

## Core Protocol Constraints

The core documents impose the following sequence constraints:

- Phase 1 is the long-only baseline phase after Phase 0 approval or explicit
  archive-only continuation approval.
- OOS labels and performance claims require proper walk-forward separation and
  leakage controls.
- Skill expansion, feature changes, and evaluation variants must remain
  preregistered and counted for multiplicity.
- Phase 1 reports must not blend performance streams or hide uncertainty.
- RDL and Growth/RBE remain dormant or monitoring-only in the current scope.

These constraints make task ordering as important as code correctness. A fast
but weakly governed evaluation engine would violate the protocol. A well
governed but operationally slow engine would create an economic and maintenance
risk under K2-style cost pressure.

## Runtime Strategy

Python remains the active Phase 0/1 language. The correct architecture is not
"all logic in Python loops"; it is Python as the orchestration and governance
surface over columnar and batch execution.

| Surface | Default stack | Boundary |
|---|---|---|
| Governance, registry, manifests, reports | Python | Deterministic rules, append-only evidence, auditability |
| Data scans, joins, features, rolling windows | Polars/DuckDB/Arrow | Columnar execution; avoid per-row Python loops |
| Walk-forward orchestration | Python | Coordinates registered trials, splits, leakage gates, hashes |
| Simulation batches and fill evaluation | Python API over vectorized kernels | Keep API stable; benchmark before optimization |
| Hot numeric kernels | Python/Polars first; Rust candidate later | Only after benchmark + ADR + human approval |
| Long-running feed or monitoring service | Not approved in Phase 1A | Go/Rust/Python decision deferred to live-provider gate |

Non-Python code remains prohibited without the existing language-escalation
requirements: measured bottleneck, reproducible benchmark, ADR, architecture and
task updates, CI/toolchain updates, and explicit human approval.

## Workload Risks

The next real bottleneck is likely not the current archive manifest tooling. It
is the cross-product of:

- assets;
- timeframes;
- walk-forward folds;
- skill families;
- hypothesis variants;
- SimBroker fill paths;
- leakage checks;
- statistical report calculations;
- registry/evidence persistence.

The main technical risk is accidental O(N assets * N bars * N trials) Python
object iteration. That shape must be rejected for Phase 1 evaluation workloads.

## Required Design Rules Before Scaffold

Future Phase 1A implementation tasks must follow these design rules:

1. Keep governance and audit logic deterministic Python.
2. Keep market data in immutable Parquet/Arrow-compatible layouts.
3. Prefer lazy Polars scans or DuckDB queries for feature and evaluation tables.
4. Batch by trial, symbol, split, or fold; do not write per-row database events
   for simulation internals.
5. Keep executable scaffold interfaces stable enough that hot kernels can later
   move behind the same Python API.
6. Do not add Rust, Go, C/C++, FFI, native extensions, or second services before
   the language-escalation gate is satisfied.
7. Do not benchmark on holdout or use benchmark output as performance evidence.
8. Do not emit OOS/performance, validated-alpha, production, or capital-ready
   labels from workload benchmarks.

## Recommended Task Sequence

The Phase 1A task sequence should be corrected as follows:

| Task | Name | Purpose |
|---|---|---|
| P1A-006 | Development And Runtime Strategy | This document; defers scaffold until workload strategy is explicit |
| P1A-007 | Workload Profile And Benchmark Contract | Define representative Phase 1A workload, runtime/memory targets, benchmark commands, allowed data, and non-claim labels |
| P1A-008 | Archive Baseline Executable Scaffold | Implement the minimum scaffold against the registered spec and read-gate, constrained by P1A-007 |
| P1A-009 | Scaffold Performance Probe | Run the benchmark harness on formation-only or synthetic non-claim data; record Python/Polars/DuckDB baseline |
| P1A-010 | Scaffold Closure Review | Decide whether Python stack is acceptable, needs optimization, or requires a language-escalation ADR |

P1A-007 must happen before executable scaffold so that the scaffold is shaped
for the expected workload instead of retrofitted after evaluation code exists.

## Go / No-Go

Verdict: `CONDITIONAL_GO_FOR_PLANNING_ONLY`.

Proceed to P1A-007 workload profile and benchmark contract.

Do not proceed directly to executable baseline scaffold until P1A-007 is
complete. Do not add non-Python implementation. Do not run Phase 1 evaluation,
portfolio/backtest evaluation, holdout reads, live feeds, Growth/RDL/RBE
activation, or performance claims.
