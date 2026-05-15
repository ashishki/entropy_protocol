# HEAVY_T14_EVIDENCE

Date: 2026-05-07
Task: T14 Markdown Report Generator

## Canonical Disclaimer

`src/signal_sandbox/reports/disclaimers.py:CANONICAL_DISCLAIMER` is rendered
exactly once and validated by `validate_disclaimer(...)`.

Canonical text:

> This report is historical research only. It is not financial advice, investment advice, trading advice, or a recommendation to buy, sell, or hold any asset.

## Provenance Block Format

The report's `## Provenance` section emits each of these values exactly once:

- `Provider: <snapshot.provider_id>`
- `Snapshot as_of_utc: <snapshot.as_of_utc.isoformat()>`
- `Snapshot SHA-256: <snapshot.sha256>`
- `Ledger SHA-256: <ledger_sha256>`
- `Outcomes SHA-256: <sha256(outcomes_parquet_bytes)>`
- `Summary SHA-256: <sha256(summary.canonical_json_bytes)>`

## Rendered Sample

```markdown
# Signal Analytics Report: pilot

## Disclaimer

This report is historical research only. It is not financial advice, investment advice, trading advice, or a recommendation to buy, sell, or hold any asset.

## Provenance

- Provider: operator-file
- Snapshot as_of_utc: 2026-05-07T12:00:00+00:00
- Snapshot SHA-256: <snapshot-sha>
- Ledger SHA-256: <ledger-sha>
```

## Verification

- `tests/integration/test_report_generator.py::test_byte_identical_re_run`
  verifies deterministic Markdown bytes.
- `test_disclaimer_present_and_canonical` verifies disclaimer integrity.
- `test_provenance_complete` verifies required provenance values exactly once.
- `test_per_signal_evidence_present` verifies evidence URL, capture timestamp,
  and text SHA-256 are present per signal.
- `test_prototype_snapshot_gated` verifies prototype snapshot approval behavior.
- `test_excluded_signals_separated` verifies excluded signals are separated from
  the evaluated outcome table.
