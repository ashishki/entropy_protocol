# Open-Source Case Review - synthetic_limit_leverage_001

Date: 2026-05-15
Status: pass as limitation case

## Scope

- Source note: `demo/synthetic_limit_leverage_001/source.md`
- Generated report: `demo/synthetic_limit_leverage_001/output/report.md`
- Reviewed report: `demo/synthetic_limit_leverage_001/output/report_reviewed.md`
- Manifest: `demo/synthetic_limit_leverage_001/output/manifest.json`
- Run status: `demo/synthetic_limit_leverage_001/output/run_status.json`

## Review Result

The pack is valid as a limitation case. It has 0 deterministic violations, 1
unsupported-data limitation, and a passed reproducibility status. The report
correctly refuses to infer max leverage from a CSV without leverage fields.

## Issues

No P0 or P1 report-validity issues found.

No new P2 issue. The limitation is the expected behavior for this pack and
must remain visible in any demo or quality dashboard.

## Demo Eligibility

Eligible as the preserved limitation/reject-side example, not as a positive
finding case.
