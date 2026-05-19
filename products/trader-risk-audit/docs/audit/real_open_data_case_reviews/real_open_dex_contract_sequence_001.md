# Real Open Data Case Review - real_open_dex_contract_sequence_001

Status: T122 manual review complete
Date: 2026-05-19
Reviewer: codex

## Verdict

| Area | Verdict | Notes |
|---|---|---|
| Source truth | PASS | Rows are transformed from real public Ethereum mainnet Uniswap V2 WETH/USDC `Swap` logs. |
| Account-like interpretation | WARN | Rows are filtered to one public contract recipient, but this still is not one verified trader account ledger. |
| Contract privacy risk | PASS_WITH_CAVEAT | `eth_getCode` confirms the selected recipient is a contract, reducing random retail-wallet risk. |
| Side derivation | PASS_WITH_CAVEAT | Side is deterministic relative to WETH and does not prove trader intent. |
| P&L support | WARN | P&L attribution is a rehearsal calculation on transformed rows, not verified trader-realized P&L. |
| Fee support | WARN | `fees=0` is a schema placeholder; gas, LP fees, and all-in user costs are unsupported. |
| Limitation wording | PASS | Reviewed report header preserves material limitations before the generated body. |
| Claim safety | PASS | Reviewed report says this is not private, paid-pilot, PMF, customer, market-demand, advice, or live-control evidence. |
| Reproducibility | PASS | Baseline and rerun manifest content hashes match. |

## Source Summary

- Case pack: `demo/real_open_dex_contract_sequence_001/`
- Source label: `real_open_data_rehearsal_not_private_evidence`
- Source: Ethereum mainnet Uniswap V2 WETH/USDC pair-level `Swap` logs
- Filter: repeated public contract recipient
- Committed rows: 40
- Report findings: 0
- Limitations: 1 unsupported leverage limitation
- Reproducibility: passed

## Findings

| ID | Severity | Area | Finding | Disposition |
|---|---|---|---|---|
| PH28-P2-001 | P2 | source shape | Contract-recipient filtered swaps are more scoped than pair-level flow, but still do not prove one trader account ledger, customer identity, or private-report readiness. | Accepted limitation; keep header/dashboard caveat visible. |
| PH28-P2-002 | P2 | fees and P&L | Fees are unsupported by the pair event and P&L attribution is a rehearsal calculation on transformed rows, not verified realized trader P&L. | Accepted limitation; keep reviewed report caveat visible. |

No P0/P1 report-truth or privacy issues were found.

## Required Caveats For Any Demo

- This is real-open-data development rehearsal only.
- It is not private pilot evidence, paid-pilot evidence, PMF evidence,
  customer validation, market-demand evidence, or proof that traders will pay.
- The source is contract-recipient-scoped public market flow, not a customer
  account ledger.
- `account_id` is a safe contract-recipient-scope label, not a wallet or
  customer id.
- Fees and verified trader-realized P&L are unsupported.
- The paid-pilot ready gate remains `needs_fixes` until T116 private/anonymized
  evidence exists.
