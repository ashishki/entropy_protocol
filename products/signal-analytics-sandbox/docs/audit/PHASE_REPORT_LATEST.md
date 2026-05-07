# Phase 3 Report - Ledger I/O + Dedup

Date: 2026-05-07
Health: WARN

## What Was Built

Phase 3 added deterministic ledger persistence and deduplication:

- `write_ledger()` writes Parquet with canonical column order.
- `read_ledger()` round-trips records back into `SignalRecord`.
- Duplicate dedup keys are rejected unless explicitly forced.
- Forced duplicates receive the `duplicate_dedup_key` ambiguity flag.
- Empty ledgers persist schema with zero rows.
- `deduplicate()` and `flag_ambiguous()` provide pure deterministic ambiguity
  handling over `SignalRecord`.

## Why It Matters

The ledger is the durable boundary between extraction/review and later outcome
matching. Phase 3 makes that boundary reproducible: repeated writes of the same
record set produce byte-identical Parquet files under the test fixture, and
deduplication uses the canonical T06 dedup-key formula.

## Validation

- `python -m pytest tests/ -q` -> 38 passed
- `ruff check src/ tests/` -> pass
- `ruff format --check src/ tests/` -> pass
- `pyright` -> pass

## Review Outcome

Deep review Cycle 3 completed with:

- P0: 0
- P1: 0
- P2: 0
- Stop-Ship: No for Phase 3 archive

Archive: `docs/archive/PHASE3_REVIEW.md`

## Open Risks

ADR-001 remains open and now blocks Phase 4 / T09. This is why health is WARN
despite a clean Phase 3 review.

## Next Phase

Phase 4 starts with T09, but implementation must wait until ADR-001 is accepted.

## Notification Summary

Ph3 Ledger/Dedup DONE
Built: ledger Parquet I/O, dedup/ambiguity flags
Tests: 31->38 pass
Issues: P1:0 P2:0
Health: WARN
Next: ADR-001 before Ph4 T09
