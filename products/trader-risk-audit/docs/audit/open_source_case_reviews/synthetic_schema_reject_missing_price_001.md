# Open-Source Case Review - synthetic_schema_reject_missing_price_001

Date: 2026-05-15
Status: pass as rejected schema case

## Scope

- Source note: `demo/synthetic_schema_reject_missing_price_001/source.md`
- Run status: `demo/synthetic_schema_reject_missing_price_001/output/run_status.json`

## Review Result

The pack is valid as a rejected edge/schema case. The audit command rejected
the malformed CSV because the required `price` column is absent. No partial
report artifacts were generated.

## Issues

No P0 or P1 report-validity issues found.

No P2 issue. The rejection is expected and should stay in the case bank to
prevent cherry-picking only runnable positive examples.

## Demo Eligibility

Not demo-report eligible. It is evidence that schema rejection is explicit and
safe.
