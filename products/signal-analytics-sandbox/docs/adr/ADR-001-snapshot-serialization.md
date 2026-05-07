# ADR-001 — `PriceSnapshot` Serialization Format

Status: **OPEN — research pending**
Date opened: 2026-05-07
Owner: operator (decision); codex (implementation after decision)
Related: D-008 (DECISION_LOG), T09, T11 (tasks.md)

---

## Context

The reproducibility contract (IMPLEMENTATION_CONTRACT §PSR-2) requires that re-running `signal-sandbox match` and `signal-sandbox report` on the same approved ledger and the same persisted `PriceSnapshot` produces byte-identical outputs. Snapshots are persisted to disk and verified at load time via SHA-256 (PSR-5).

This places a hard constraint on the serialization format used by `PriceSnapshot.canonical_bytes()` (T09) and `save_snapshot()` (T11): the chosen format must produce **byte-identical output across runs and across the supported development platforms** (Linux, macOS) for the same input OHLCV data.

The decision is deferred from Phase 1 bootstrap to ADR-001 because the choice has subtle pitfalls (per-write timestamps, dictionary key ordering, compression-library version sensitivity, parquet metadata, float NaN canonicalization).

## Research Question

> Which serialization format for `PriceSnapshot` produces byte-identical output across re-runs on Linux + macOS, supports SHA-256 round-trip verification, integrates with the project's polars/pandas stack, and remains stable across reasonable dependency upgrades?

## Candidates

| Format | Pros | Cons / Risk |
|--------|------|-------------|
| **Parquet (zstd, statistics off, no dictionary, fixed pyarrow version)** | Native to polars/pandas; columnar; project already uses Parquet for ledgers (T07); single serialization library across the project | Parquet writer metadata may include creator-version / per-write timestamp unless explicitly disabled; needs careful pyarrow flag tuning; future pyarrow upgrade can shift bytes |
| **Canonical JSON (RFC-8785) over a fixed schema** | Trivially deterministic; debuggable by hand; no library version risk | Verbose for OHLCV (10x size); slower to load; loses columnar advantage |
| **MessagePack (canonical mode)** | Compact binary; deterministic with sorted keys; small dependency footprint | Adds a serialization library not otherwise used; slower than Parquet for tabular data |
| **CSV with locked dialect + sorted rows** | Human-readable; trivially deterministic | No types; precision loss on round-trip; unsuitable for Decimal-like guarantees |

## Pre-research Bias

D-008 currently leans toward **Parquet** because it keeps the project on a single tabular serialization library. The research question is whether Parquet's determinism can be guaranteed in practice with reasonable flag tuning, or whether one of the other candidates is materially safer.

## Required Research Outputs

A research note written to `docs/research/snapshot-serialization.md` (when the experimental Research Companion is invoked) or attached as comments to this ADR. The note must answer:

1. For each candidate, the exact configuration (flags, library versions, pinned dependencies) that produces byte-identical output on Linux + macOS for the same input.
2. Concrete failure modes observed for the rejected candidates (e.g., "pyarrow 15.x embeds creator-version in Parquet footer").
3. Migration path if the chosen format's library makes a breaking change.
4. SHA-256 round-trip verification recipe.
5. Per-format performance / size estimates for a representative `PriceSnapshot` (e.g., 1 asset × 1-minute OHLCV × 30 days).

## Decision

**Pending.** Do not start T09 implementation until this ADR is in `Status: ACCEPTED`. The orchestrator must surface this ADR on the Phase 4 strategy review.

When the decision is recorded:
- Update this ADR's Status, Decision, and Consequences sections.
- Update `docs/DECISION_LOG.md` row D-008 with the canonical-source reference (`docs/adr/ADR-001-snapshot-serialization.md`) and the chosen format.
- Update `docs/IMPLEMENTATION_CONTRACT.md §PSR-5` only if the chosen format imposes additional rules (e.g., a pinned pyarrow version) — that requires its own ADR.

## Consequences

To be filled in when the decision is recorded.
