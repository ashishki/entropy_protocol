# Phase 32 Error Register - Dune Public Wallet Rehearsal

Date: 2026-05-19
Scope: `demo/dune_public_wallet_dex_001/`

## Summary

| Severity | Count |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |

## Findings

| ID | Severity | Finding | Artifact | Status |
|---|---|---|---|---|
| PH32-P2-001 | P2 | Dune `tx_from` rows are public submitter-scoped DEX rows, not a verified private trader account ledger. | `demo/dune_public_wallet_dex_001/source.md` | Accepted limitation |
| PH32-P2-002 | P2 | Fees, gas, slippage/MEV, leverage, balances, and verified realized P&L are unsupported by the committed Dune transform. | `demo/dune_public_wallet_dex_001/output/report_reviewed.md` | Accepted limitation |

## Stop-Ship

No stop-ship issue for development rehearsal use.

Stop-ship remains active for paid-pilot/private-readiness claims because T116 is
still blocked.
