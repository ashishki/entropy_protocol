# Dune Public Wallet DEX Case Review

Case: `dune_public_wallet_dex_001`
Date: 2026-05-19
Reviewer: codex

## Scope

Reviewed the Dune public wallet DEX case pack:

- source metadata: `demo/dune_public_wallet_dex_001/source.md`
- canonical input: `demo/dune_public_wallet_dex_001/trades.csv`
- policy: `demo/dune_public_wallet_dex_001/policy.yaml`
- reviewed report: `demo/dune_public_wallet_dex_001/output/report_reviewed.md`
- reproducibility status:
  `demo/dune_public_wallet_dex_001/output/reproducibility_status.json`

## Findings

| Severity | Count |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |

## Accepted P2 Caveats

| ID | Caveat | Status |
|---|---|---|
| PH32-P2-001 | Dune `tx_from` scope is a public submitter address, not a verified private trader account ledger or wallet-owner identity. | Accepted limitation |
| PH32-P2-002 | The transformed rows use bought-token side, schema-placeholder fees, and Dune USD amount; gas, LP fees, slippage/MEV, leverage, balances, and verified realized P&L are unsupported. | Accepted limitation |

## Evidence Checked

- Source metadata contains Dune execution IDs, SQL, transformation notes, and
  explicit unsupported fields.
- The committed CSV contains 80 canonical rows and a safe `account_id` label.
- The reviewed report records 76 deterministic max-position findings and one
  unsupported leverage limitation.
- Reproducibility status is `passed` with matching stable content hashes.
- `case-bank validate --case-dir demo/dune_public_wallet_dex_001` passed.

## Decision

Accepted for real-open-data development rehearsal and report-review
conversation use.

Not accepted as private report readiness, paid-pilot evidence, PMF evidence,
customer validation, market-demand evidence, or trading advice.
