# Phase 1A Scaffold Performance Probe Packet

Date: 2026-05-05
Task: P1A-009
Status: `COMPLETE`
Decision: `SCAFFOLD_PROBE_COMPLETE_MECHANICS_ONLY`

## Scope

P1A-009 implemented a mechanics-only scaffold benchmark probe under the P1A-007
workload contract.

The probe writes deterministic synthetic non-claim scaffold-shaped rows to a
Parquet artifact and writes a JSON benchmark manifest with runtime, memory,
artifact size, backend path, replay hash, code hash, and no-claim labels.

The probe does not read holdout, does not read live/provider data, does not
compute alpha, does not allocate a portfolio, does not run backtest/evaluation,
and does not emit strategy performance metrics or OOS/performance claims.

## Implemented Surface

Code:

- `entropy/evidence/phase1a_scaffold_probe.py`
- `entropy/evidence/__init__.py`

Tests:

- `tests/unit/test_phase1a_scaffold_probe.py`

The probe:

- supports the `polars` backend only;
- accepts metadata-only, formation-only, or deterministic synthetic non-claim
  data boundary labels;
- rejects holdout data boundaries;
- rejects non-Polars backend labels;
- writes Parquet/Arrow-compatible artifacts;
- records benchmark manifest fields required by P1A-007;
- keeps replay hash deterministic for the same scaffold/config inputs;
- avoids strategy metric fields such as Sharpe, drawdown, return, IC, alpha,
  edge, PnL, hit rate, and trade quality.

## Boundary

Allowed:

- implementation benchmark mechanics;
- deterministic synthetic non-claim scaffold-shaped rows;
- runtime and memory facts;
- artifact size;
- backend label;
- replay hash.

Forbidden and not implemented:

- alpha signal generation;
- score, weight, position, return, or PnL generation;
- portfolio allocation;
- backtest or walk-forward evaluation;
- strategy performance metrics;
- archive holdout read/unlock;
- live/provider/broker integration;
- Growth/RDL/RBE activation;
- Rust, Go, C/C++, FFI, native extensions, or second runtime services;
- OOS/performance, validated-alpha, production, or capital-ready claims.

## Verification

- `.venv/bin/pytest tests/unit/test_phase1a_scaffold_probe.py -q` -> `5 passed`
- `.venv/bin/ruff check entropy/evidence/phase1a_scaffold_probe.py entropy/evidence/__init__.py tests/unit/test_phase1a_scaffold_probe.py` -> passed
- `.venv/bin/ruff format --check entropy/evidence/phase1a_scaffold_probe.py entropy/evidence/__init__.py tests/unit/test_phase1a_scaffold_probe.py` -> passed
- `.venv/bin/pyright --pythonpath .venv/bin/python entropy/evidence/phase1a_scaffold_probe.py` -> `0 errors`
- `.venv/bin/pytest tests/unit/test_phase1a_freeze.py tests/unit/test_phase1a_registration.py tests/unit/test_phase1a_baseline.py tests/unit/test_phase1a_scaffold.py tests/unit/test_phase1a_scaffold_probe.py -q` -> `24 passed`
- `.venv/bin/pyright --pythonpath .venv/bin/python entropy/evidence/phase1a_scaffold.py entropy/evidence/phase1a_scaffold_probe.py` -> `0 errors`
- `.venv/bin/pytest -q` -> `216 passed, 20 skipped`

## Next Step

Proceed to P1A-010 Scaffold Closure Review.

P1A-010 must review P1A-008 and P1A-009 only. It must not approve Phase 1
evaluation, holdout reads, non-Python runtime/toolchain additions, live feeds,
Growth/RDL/RBE activation, or OOS/performance claims.
