# Phase 1A Workload Profile And Benchmark Contract

Date: 2026-05-05
Task: P1A-007
Status: `COMPLETE`
Decision: `WORKLOAD_PROFILE_AND_BENCHMARK_CONTRACT_APPROVED`

## Executive Summary

This contract defines the workload and benchmark boundaries that must shape the
Phase 1A executable scaffold.

The purpose is operational architecture only: prove that future code is shaped
for large archive simulations and hypothesis batches before scaffold APIs become
sticky. This contract does not run evaluation, compute alpha, compute portfolio
returns, read holdout, approve Phase 1, or authorize any performance claim.

Python remains the control plane. Polars, DuckDB, Arrow, and Parquet are the
default data plane. Rust, Go, C/C++, FFI, native extensions, or second runtime
services remain prohibited unless the language-escalation gate is satisfied.

## Authorized Inputs

Allowed benchmark inputs:

- P1A-002 frozen archive manifest metadata;
- P1A-003 registration boundary metadata;
- P1A-004 baseline registration metadata;
- `ARCHIVE_FORMATION` market data only when a future benchmark actually reads
  real archive rows;
- synthetic non-claim stress data generated from documented deterministic rules.

Restricted inputs:

- `ARCHIVE_VALIDATION` data may be used only after registration metadata is
  supplied and only for non-claim workload mechanics in a separately approved
  implementation task.
- `ARCHIVE_HOLDOUT` data remains locked. No benchmark may read, summarize,
  profile, sample, or infer from holdout rows.
- Live, streaming, broker, or provider data is not approved.

Benchmark outputs must be labeled `implementation_benchmark_only` and
`not_phase_gate_evidence`.

## Non-Claim Boundary

Benchmark artifacts may report:

- wall-clock runtime;
- peak memory;
- rows processed per second;
- trial-shape throughput;
- artifact size;
- deterministic replay hash;
- top runtime hotspots;
- backend used: Python, Polars, DuckDB, Arrow.

Benchmark artifacts must not report:

- Sharpe, drawdown, return, IC, alpha, edge, P&L, hit rate, or trade quality;
- OOS, validated-alpha, production, capital-ready, or phase-gate labels;
- conclusions about whether any skill family works;
- comparisons that imply strategy quality.

## Representative Workload Shapes

The scaffold must be compatible with the following workload shapes.

| ID | Purpose | Shape | Data boundary |
|---|---|---|---|
| W0 | Scaffold smoke workload | 15 assets, 1d, registered six-family baseline metadata, formation read-gate checks | Metadata and formation-only mechanics |
| W1 | Archive feature-table workload | 15 assets, 1d, 2020-01-01 through 2025-12-31 shape, OHLCV-derived columns only | No holdout reads during P1A-007/P1A-008 |
| W2 | Hypothesis-batch planning workload | 6 skill families x 10 trial-shape variants x split-aware artifact manifests | Synthetic or formation-only; no alpha logic |
| W3 | Simulation-shape stress workload | synthetic signal/fill-shaped tables sized to future SimBroker batches | Synthetic only; no strategy semantics |
| W4 | Scale reserve workload | 80 assets x 4 timeframes x 100 trial-shape variants | Synthetic only; used for API shape, not claims |

W4 does not approve expansion to 80 assets or additional timeframes. It is a
stress shape that prevents the API from assuming the current small archive
universe is the permanent maximum.

## Runtime Targets

These targets are planning thresholds for future benchmark tasks. They are not
performance claims about current code.

| Context | Target |
|---|---|
| Local smoke benchmark | Completes W0 within 30 seconds on a local workstation |
| CI benchmark subset | Completes deterministic synthetic subset within 60 seconds |
| Formation feature-table benchmark | Processes W1 formation-scope table without exceeding 4 GB peak memory |
| Research batch benchmark | Processes W2 trial-shape workload at >= 100 trial-shapes/hour on local workstation class hardware |
| Replay stability | Repeated benchmark run produces the same replay hash for the same inputs and code hash |

If hardware differs materially, the benchmark packet must record CPU, RAM,
storage type, Python version, Polars version, DuckDB version, and command.

## Required Benchmark Packet Fields

Future benchmark artifacts must include:

- benchmark ID and version;
- task ID;
- input manifest paths and hashes;
- data boundary label: synthetic, formation-only, or metadata-only;
- command;
- environment summary;
- backend path used;
- wall-clock runtime;
- peak memory;
- rows processed;
- artifact bytes written;
- deterministic replay hash;
- code hash;
- policy hash or contract hash;
- no-claim labels;
- failure reason if a target is missed.

## Storage Boundary

Large benchmark intermediates must be Parquet or Arrow-compatible artifacts.
PostgreSQL is for metadata only:

- benchmark run ID;
- status;
- manifest pointers;
- hashes;
- aggregate runtime/memory facts.

Per-row simulation, feature, fill, or signal-shaped outputs must not be written
to PostgreSQL in Phase 1A benchmark paths.

## Implementation Constraints For P1A-008

The executable scaffold must:

1. expose batch/table-oriented APIs, not per-bar strategy callbacks;
2. accept manifest/spec metadata separately from table data;
3. keep read-gate authorization separate from physical data loading;
4. make holdout reads impossible by construction;
5. return implementation-state artifacts, not performance reports;
6. preserve a stable boundary where a future Rust kernel could replace a
   Python/Polars implementation without changing registry or audit semantics.

The scaffold must not introduce a benchmark runner that computes strategy
results. If timing helpers are needed, they must remain mechanics-only and
formation/synthetic scoped.

## Optimization And Escalation Path

If a future benchmark misses a target, the order of response is:

1. inspect projection and predicate pushdown;
2. remove accidental Python row loops;
3. switch eager operations to lazy Polars or DuckDB queries where appropriate;
4. batch filesystem and Parquet writes;
5. separate metadata writes from data-plane artifacts;
6. rerun the benchmark and record before/after results;
7. only then open a language-escalation ADR if targets are still missed.

Language escalation requires the existing contract:

- reproducible Python/Polars/DuckDB baseline;
- explicit target threshold missed after optimization;
- candidate implementation benchmark;
- ADR covering language, affected modules, CI/toolchain, packaging, ownership,
  rollback, and human approval;
- architecture, task, and CI updates before code is added.

## Go / No-Go

Verdict: `GO_FOR_P1A-008_SCAFFOLD_ONLY_WITH_WORKLOAD_BOUNDARY`.

Proceed to P1A-008 Archive Baseline Executable Scaffold.

P1A-008 must follow this contract. It must not implement alpha logic,
portfolio/backtest evaluation, performance metrics, holdout reads, live feeds,
Growth/RDL/RBE activation, non-Python runtime/toolchain additions, or
OOS/performance claims.
