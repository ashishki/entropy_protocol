# Open-Source Audit Batch Index

Status: T101 generated
Date: 2026-05-15

This index summarizes the Phase 23 candidate batch without raw private rows.
All packs are artifact-quality evidence only. They are not paid-pilot, PMF, or
customer evidence.

## Batch Summary

| Case ID | Pack status | Case type | Data shape | Findings | Limitations | Reproducibility | Notes |
|---|---|---|---|---:|---:|---|---|
| `open_source_sec_form4_001` | complete | mixed | disclosure-like | 7 | 3 | passed | Existing SEC reference pack; reviewed report already exists from Phase 16. |
| `public_sample_001` | complete | positive_finding | disclosure-like compact sample | 9 | 0 | passed | Existing public-like demo pack; generated report copied to review slot for T102 manual review. |
| `risk_audit_case_001` | complete | positive_finding | broker/export-like CSV | 13 | 0 | passed | Synthetic positive pack with realized P&L and multiple deterministic violations. |
| `synthetic_limit_leverage_001` | complete | limitation | broker/export-like CSV | 0 | 1 | passed | Max-leverage rule preserved as unsupported because no leverage field exists. |
| `synthetic_schema_reject_missing_price_001` | rejected | reject / edge_schema | malformed broker/export-like CSV | 0 | 0 | not_applicable | Missing required `price` column; no report artifacts generated. |

## Runnable Artifacts

Each complete pack has:

- `output/normalized_trades.json`;
- `output/violations.json`;
- `output/attribution_summary.json`;
- `output/report.md`;
- `output/report_reviewed.md`;
- `output/telegram_packet.txt`;
- `output/manifest.json`;
- `output/reproducibility_status.json`;
- `output/run_status.json`.

`report_reviewed.md` is a review slot for T102 except where a prior reviewed
report already exists. T102 remains responsible for manual validation notes and
error-register decisions.

## Rejected Pack

`synthetic_schema_reject_missing_price_001` has no partial report claims. Its
only generated output is `output/run_status.json`, which records the safe
schema error:

```text
missing canonical fields: price; inspected columns: timestamp, symbol, side, quantity, fees, account_id
```

## Evidence Boundary

This batch proves artifact execution coverage only. It does not justify hosted
uploads, checkout, real exchange fetching, broker control, trading advice, or
customer validation claims.
