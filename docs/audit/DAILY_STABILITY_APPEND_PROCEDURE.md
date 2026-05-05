# Daily Stability Append Procedure

Date: 2026-05-05
Status: PROCEDURE_READY

## Purpose

Define how future sessions append real data-stability monitor rows without
overwriting prior evidence.

## Procedure

1. Fetch approved public quote snapshots from Coinbase Exchange public API and
   Kraken public API.
2. Record raw extracts and SHA-256 hashes.
3. Convert each successful snapshot into a `DataStabilityRow`.
4. Append rows to the cumulative monitoring JSONL.
5. Rebuild the summary from the full cumulative row set.
6. Keep `evidence_claim=not_phase_gate_approval` until >=90 continuous days are
   present and reviewed.

## Storage

Recommended cumulative paths:

- `artifacts/evidence/data_stability/live_monitor/DATA_STABILITY_ROWS.jsonl`
- `artifacts/evidence/data_stability/live_monitor/DATA_STABILITY_SUMMARY.md`
- `artifacts/evidence/data_stability/live_monitor/raw/YYYY-MM-DD/`

## Non-Overwrite Rule

Daily rows must be appended. Prior rows and raw extracts must not be rewritten
except through an explicit correction packet that records the old hash, new hash,
reason, and reviewer.

## Gate Boundary

The 90-day gate remains open until a packet contains at least 90 continuous
monitored days, all target symbol-days are present, unexplained gaps are zero,
hashes are present, and the packet is reviewed.
