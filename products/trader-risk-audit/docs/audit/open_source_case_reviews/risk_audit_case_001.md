# Open-Source Case Review - risk_audit_case_001

Date: 2026-05-15
Status: pass with synthetic-provenance caveat

## Scope

- Source note: `demo/risk_audit_case_001/source.md`
- Generated report: `demo/risk_audit_case_001/output/report.md`
- Reviewed report: `demo/risk_audit_case_001/output/report_reviewed.md`
- Manifest: `demo/risk_audit_case_001/output/manifest.json`
- Run status: `demo/risk_audit_case_001/output/run_status.json`

## Review Result

The pack is valid as a synthetic positive-finding case. It has 13
deterministic findings, non-zero violating P&L, and a passed reproducibility
status. Source-row traceability is present in the violation table.

## Issues

No P0 or P1 report-validity issues found.

P2 caveat: because the data is synthetic, the report must be used only for
deterministic evaluator and attribution coverage. The reviewed copy explicitly
states that it is not customer or market evidence.

## Demo Eligibility

Eligible for internal positive-finding coverage only. Keep synthetic provenance
visible.
