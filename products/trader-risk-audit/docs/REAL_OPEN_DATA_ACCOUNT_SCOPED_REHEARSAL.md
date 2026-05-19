# Real Open Data Account-Scoped Rehearsal

Status: complete development rehearsal
Date: 2026-05-19
Audience: operator + development

This note records the no-key account-scoped fallback after confirming that Dune
CSV/API access requires an API key. It uses real public Ethereum data, not
synthetic rows, and it remains development rehearsal evidence only.

## Access Decision

| Route | Decision | Reason |
|---|---|---|
| Dune `dex.trades` CSV/API | blocked_for_no_key_run | Dune API result CSV requires an API key with read scope. |
| BigQuery blockchain datasets | deferred | Better query path, but requires Google Cloud access and cost controls. |
| Public JSON-RPC contract-recipient filter | selected | No account key, no paid query, real public logs, and lower privacy risk than a random EOA wallet. |

## Selected Source

| Field | Value |
|---|---|
| Chain | Ethereum mainnet |
| Protocol | Uniswap V2 |
| Pair | WETH/USDC |
| Pair contract | `0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc` |
| Filter | `Swap` logs where indexed `to` equals public contract `0x423d607bd4e213e9b64a54b324ab7f632feec647` |
| Contract check | `eth_getCode` returned non-empty code |
| Access | public read-only JSON-RPC `eth_getLogs` |
| Case pack | `demo/real_open_dex_contract_sequence_001/` |

## Why This Is Better Than Pair-Level Only

- It narrows the sample to one repeated public contract recipient.
- It avoids selecting a random retail EOA wallet.
- It creates a sequence that is closer to account-scoped behavior than all
  WETH/USDC pair flow.

## Remaining Limitations

- A contract recipient is not a verified trader or customer account.
- The contract may aggregate, route, or receive swaps for reasons not visible
  in the pair event.
- Written risk rules are rehearsal rules, not user-provided rules.
- Fees, leverage, balances, margin, deposits, withdrawals, and verified
  trader-realized P&L remain unsupported.
- The pack does not close T116 and does not move the paid-pilot ready gate out
  of `needs_fixes`.

## Result

The case pack produced:

- 40 transformed real public rows;
- 0 deterministic max-position findings under the rehearsal threshold;
- 1 unsupported leverage limitation;
- passed reproducibility;
- passed case-bank validation.

This is useful as a no-breach/control-style real-open-data rehearsal, not as
private, paid-pilot, customer-validation, PMF, or market-demand evidence.
