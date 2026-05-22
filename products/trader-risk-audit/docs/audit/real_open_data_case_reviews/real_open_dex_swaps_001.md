# Real Open Data Case Review - real_open_dex_swaps_001

Status: T120 manual review complete
Date: 2026-05-19
Reviewer: codex

## Verdict

| Area | Verdict | Notes |
|---|---|---|
| Source truth | PASS | Rows are transformed from real public Ethereum mainnet Uniswap V2 WETH/USDC `Swap` logs. |
| Account-like interpretation | WARN | Pair-level swap logs are market-flow data, not one trader account ledger. |
| Side derivation | PASS_WITH_CAVEAT | Side is deterministic relative to WETH and does not prove trader intent. |
| P&L support | WARN | P&L attribution is an audit-engine rehearsal calculation on transformed rows, not verified trader-realized P&L. |
| Fee support | WARN | `fees=0` is a schema placeholder; gas, LP fees, and all-in user costs are unsupported. |
| Limitation wording | PASS | Reviewed report header preserves material limitations before the generated body. |
| Claim safety | PASS | Reviewed report says this is not private, paid-pilot, PMF, customer, market-demand, advice, or live-control evidence. |
| Reproducibility | PASS | Baseline and rerun manifest content hashes match. |

## Source Summary

- Case pack: `demo/real_open_dex_swaps_001/`
- Source label: `real_open_data_rehearsal_not_private_evidence`
- Source: Ethereum mainnet Uniswap V2 WETH/USDC pair-level `Swap` logs
- Block range: `0x17f6a00-0x17f6e6b`
- Committed rows: 40
- Report findings: 8 `real_open_max_position_size` findings
- Limitations: 1 unsupported leverage limitation
- Reproducibility: passed

## Findings

| ID | Severity | Area | Finding | Disposition |
|---|---|---|---|---|
| PH27-P2-001 | P2 | source shape | Pair-level Uniswap swaps are real public executions, but they are not one trader account ledger and cannot prove private-report readiness. | Accepted limitation; keep header/dashboard caveat visible. |
| PH27-P2-002 | P2 | fees and P&L | Fees are unsupported by the pair event and P&L attribution is a rehearsal calculation on transformed rows, not verified realized trader P&L. | Accepted limitation; keep reviewed report caveat visible. |

No P0/P1 report-truth or privacy issues were found.

## Required Caveats For Any Demo

- This is real-open-data development rehearsal only.
- It is not private pilot evidence, paid-pilot evidence, PMF evidence,
  customer validation, market-demand evidence, or proof that traders will pay.
- The source is pair-level market flow, not a customer account ledger.
- `account_id` is a safe pair-scope label, not a wallet or customer id.
- Fees and verified trader-realized P&L are unsupported.
- The paid-pilot ready gate remains `needs_fixes` until T116 private/anonymized
  evidence exists.

## Follow-Up

T121 should update the dashboard, coverage matrix, and paid-pilot ready gate to
include this pack as development rehearsal only.
