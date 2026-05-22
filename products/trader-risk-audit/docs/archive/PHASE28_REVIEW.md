# Phase 28 Review - Account-Scoped Real Open Data Rehearsal

Date: 2026-05-19
Cycle: 31
Scope: T122

## Verdict

- Stop-Ship: No
- Health: WARN
- P0: 0
- P1: 0
- P2: 2
- Paid-pilot ready gate: `needs_fixes`

## Summary

Phase 28 added `real_open_dex_contract_sequence_001`, a no-key account-scoped
fallback using real Ethereum mainnet Uniswap V2 WETH/USDC `Swap` logs filtered
to one repeated public contract recipient.

The pack is closer to account-scoped behavior than pair-level flow, but it is
still not a verified trader account ledger and cannot close T116.

## Findings

| ID | Severity | Finding | Status |
|----|----------|---------|--------|
| PH28-P2-001 | P2 | Contract-recipient filtered swaps are not a verified trader account ledger. | Accepted limitation |
| PH28-P2-002 | P2 | Fees and verified realized P&L remain unsupported by this source. | Accepted limitation |

## Checks

| Area | Verdict |
|---|---|
| Real public data, no synthetic rows | PASS |
| Contract-recipient scope | PASS_WITH_CAVEAT |
| Case-pack validation | PASS |
| Manual report review | PASS_WITH_CAVEATS |
| Ready gate remains `needs_fixes` | PASS |
| No forbidden scope expansion | PASS |

## Next

T116 remains blocked pending one operator-approved private/anonymized artifact
outside git. Dune/BigQuery can improve account-like extraction later if an
operator approves API/account/cost setup, but that still will not replace T116.
