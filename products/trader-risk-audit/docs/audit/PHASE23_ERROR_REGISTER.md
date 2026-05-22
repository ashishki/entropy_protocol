# Phase 23 Error Register

Status: T102 manual review
Date: 2026-05-15

## Summary

| Severity | Count | Demo block? |
|---|---:|---|
| P0 | 0 | Yes if any appear |
| P1 | 0 | Yes if any appear |
| P2 | 3 | No, but wording must stay visible |

No unresolved P0 or P1 findings block continued Phase 23 work. P2 findings are
documentation/report-wording caveats that must remain visible in reviewed
reports and later quality dashboards.

## Findings

| ID | Severity | Case | Area | Finding | Demo status | Disposition |
|---|---|---|---|---|---|---|
| PH23-P2-001 | P2 | `open_source_sec_form4_001` | source limitation | SEC Form 4 rows are disclosure records, not a customer account ledger; P&L, drawdown, leverage, and trading intent remain unsupported. | Internal reference only | Accepted limitation; preserved in reviewed report and review note. |
| PH23-P2-002 | P2 | `public_sample_001` | P&L wording | Generated report can show affected P&L as `0` while loss/drawdown violations exist because flagged rows may not be realized closing rows. | Allowed only with reviewed-copy caveat | Accepted wording caveat; reviewed report preserves it. |
| PH23-P2-003 | P2 | `risk_audit_case_001` | provenance | Synthetic positive findings prove deterministic evaluator coverage, not customer outcome or market demand. | Internal positive-finding coverage only | Accepted provenance caveat; reviewed report preserves it. |

## Rejected / Weak Case Visibility

`synthetic_limit_leverage_001` remains visible as a limitation case with no
violations and one unsupported leverage limitation.

`synthetic_schema_reject_missing_price_001` remains visible as a rejected
schema case with only `output/run_status.json` and no partial report claims.

Neither case should be removed from the batch because both protect against
cherry-picking only attractive positive reports.
