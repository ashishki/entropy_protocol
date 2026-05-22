# Phase 32 Review - Dune Public Wallet Rehearsal

Date: 2026-05-19
Scope: T137-T140
Health: WARN

## Summary

Phase 32 used Dune as a real public-data source and created
`demo/dune_public_wallet_dex_001`, a public Ethereum `dex.trades`
submitter-scoped case pack.

## Completed Work

- Queried Dune `dex.trades` through the API without committing the supplied key.
- Selected one public Ethereum `tx_from` scope from a 14-day discovery query.
- Extracted 80 real public DEX rows into canonical audit CSV format.
- Ran the deterministic audit workflow and produced a reviewed report.
- Recorded reproducibility status with matching stable manifest content hashes.
- Added source metadata, manual review, and an error register.

## Validation

- `case-bank validate --case-dir demo/dune_public_wallet_dex_001` -> passed.
- Reproducibility status -> passed.

## Findings

| Severity | Count |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |

P2 findings are accepted source-shape limitations:

- public Dune submitter scope is not a verified private trader ledger;
- execution costs, leverage, balances, and verified realized P&L are
  unsupported.

## Gate Decision

Stop-Ship: No for development rehearsal and report-review conversation use.

T116 remains blocked. The paid-pilot ready gate remains `needs_fixes` because no
operator-approved private or anonymized export has been run and reviewed outside
git.

## Next Action

Use the Dune reviewed report as a client conversation artifact to test whether
the report is understandable and trustworthy. Record only aggregate
non-identifying outcomes. If an approved private/anonymized export appears,
return to T116.
