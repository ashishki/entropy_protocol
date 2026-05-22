# Real Open DEX Swaps Source Metadata

source_name: Ethereum mainnet Uniswap V2 WETH/USDC pair Swap logs
source_label: real_open_data_rehearsal_not_private_evidence
source_access_path: public read-only JSON-RPC eth_getLogs
source_primary_endpoint: https://rpcfree.com/ethereum-rpc
source_fallback_endpoint: https://ethereum.publicnode.com
source_protocol: Uniswap V2
source_pair_contract: 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc
source_event_topic: 0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822
source_block_range_hex: 0x17f6a00-0x17f6e6b
source_block_range_decimal: 25127471-25127885
source_accessed_date: 2026-05-19
row_count_committed: 40
privacy_reviewed_by: codex
privacy_review_date: 2026-05-19

## Boundary

This pack uses real public Ethereum Uniswap V2 pair-level swap logs for a
development rehearsal. It is not a private trader export, paid-pilot evidence,
customer validation, PMF evidence, market-demand evidence, or trading advice.

## Source Notes

The selected rows are real `Swap` event logs emitted by the Uniswap V2
WETH/USDC pair contract. The event schema is documented in the public Uniswap
V2 pair interface and mapped in `docs/REAL_OPEN_DATA_EXTRACTION_CONTRACT.md`.

The raw JSON-RPC response was used as a temporary extraction artifact and is not
committed. The committed `trades.csv` is a transformed audit input only.

## Transformation Summary

- `timestamp`: log block timestamp rendered as UTC ISO-8601.
- `symbol`: fixed to `WETHUSDC`.
- `side`: derived relative to WETH, not an end-user account.
- `quantity`: WETH amount from `amount1In` or `amount1Out`.
- `price`: USDC amount divided by WETH quantity.
- `fees`: `0` schema placeholder; gas, LP fee, and all-in user execution costs
  are unsupported by this source.
- `account_id`: safe pair-scope label, not a wallet address.

## Provenance Sample

| Row | Block | Truncated transaction hash | Log index |
|---:|---:|---|---:|
| 1 | 25127471 | `0x9df7300e27...` | 914 |
| 40 | 25127885 | `0x87482f75a0...` | 644 |

## Fields Not Supported

- user identity or trader account;
- private wallet owner;
- written user risk rules;
- gas fees and all-in execution costs;
- leverage and margin;
- account equity, deposits, withdrawals, and balances;
- verified realized trader P&L;
- order intent, stop-loss intent, or strategy.

## Privacy Review

No private rows, credentials, payment identifiers, private paths, screenshots,
customer identifiers, or full wallet-address account labels are committed.
