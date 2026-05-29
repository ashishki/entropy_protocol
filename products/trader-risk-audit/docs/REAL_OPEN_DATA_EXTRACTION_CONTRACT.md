# Real Open Data Extraction Contract

Status: selected for T118
Date: 2026-05-19
Audience: operator + development

This contract defines how `real_open_dex_swaps_001` may transform real public
Uniswap V2 WETH/USDC swap logs into the Trader Risk Audit CSV shape. It must be
followed before any case-pack rows are committed.

## Source Query

Primary endpoint:

```bash
curl -sS -X POST https://rpcfree.com/ethereum-rpc \
  -H 'Content-Type: application/json' \
  --data '{
    "jsonrpc": "2.0",
    "method": "eth_getLogs",
    "params": [{
      "fromBlock": "<from_block_hex>",
      "toBlock": "<to_block_hex>",
      "address": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
      "topics": [
        "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
      ]
    }],
    "id": 1
  }'
```

Fallback endpoint:

```bash
https://ethereum.publicnode.com
```

Use a bounded block range that returns a small stable sample, target 20-100
swap logs. Record the final block range in `demo/real_open_dex_swaps_001/source.md`.

## Event Schema

Uniswap V2 `Swap` event:

```solidity
event Swap(
    address indexed sender,
    uint amount0In,
    uint amount1In,
    uint amount0Out,
    uint amount1Out,
    address indexed to
);
```

Token assumptions for the selected pair:

| Token | Address | Decimals | Role |
|---|---|---:|---|
| USDC | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | 6 | token0 |
| WETH | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | 18 | token1 |

If `token0()` or `token1()` calls disagree with these assumptions, stop and
update this contract before generating rows.

## Canonical Mapping

Side is defined relative to WETH, not relative to an end-user account.

| Canonical field | Mapping |
|---|---|
| `timestamp` | `blockTimestamp` from log if provided by the endpoint; otherwise fetch `eth_getBlockByNumber` and use block timestamp. Render UTC ISO-8601. |
| `symbol` | `WETHUSDC` for every row. |
| `side` | `buy` when `amount1Out > 0` and `amount0In > 0`; `sell` when `amount1In > 0` and `amount0Out > 0`; reject ambiguous rows. |
| `quantity` | WETH amount: `amount1Out / 1e18` for buys, `amount1In / 1e18` for sells. |
| `price` | USDC per WETH: USDC amount divided by WETH quantity. USDC amount is `amount0In / 1e6` for buys and `amount0Out / 1e6` for sells. |
| `fees` | `0` only as a schema placeholder. Report and review must state that gas, LP fee, and user-level all-in costs are unsupported by this source. |
| `account_id` | `real_open_uniswap_v2_weth_usdc_pair_scope`; never a wallet address. |
| `source_row_number` | Deterministic 1-based ordering by `(blockNumber, transactionIndex, logIndex)`. |

## Unsupported Fields

The following are unsupported and must be visible in `source.md`,
`report_reviewed.md`, and manual review:

- user identity or trader account;
- private wallet owner;
- written user risk rules;
- gas fees and all-in execution costs;
- leverage and margin;
- account equity, deposits, withdrawals, and balances;
- verified realized trader P&L;
- order intent, stop-loss intent, or strategy.

## Policy Constraints

Only use rules that are meaningful for the transformed row shape:

- `max_position_size` or max notional threshold;
- `cooldown_after_loss` as an engine-behavior rehearsal only, with P&L caveat;
- `forbidden_assets` only if intentionally showing a deterministic finding;
- `max_leverage` only to produce an unsupported-data limitation.

Do not claim that these are real trader-written rules. Use a rehearsal policy
label and source limitation text.

## Privacy And Provenance Checklist

Before committing a case pack:

- [ ] Source is real public Ethereum mainnet data.
- [ ] No synthetic rows were created.
- [ ] No raw private data, private paths, credentials, account ids, payment
      identifiers, screenshots, or customer identifiers are committed.
- [ ] Full wallet addresses are not used as `account_id`.
- [ ] Full transaction hashes appear only in `source.md` or reviewed source
      refs if needed for provenance; report copy may use truncated refs.
- [ ] `fees=0` is documented as unsupported-cost placeholder, not a zero-fee
      claim.
- [ ] Ready gate remains `needs_fixes` unless T116 private evidence separately
      exists.

## Extraction Stop Conditions

Stop and update this contract if:

- public RPC access requires a secret, paid key, or account login;
- logs lack timestamps and block timestamp lookup is unavailable;
- more than 5% of candidate rows are ambiguous side mappings;
- transformed values require fabricated quantities, prices, fees, or P&L;
- selected rows expose a private individual as the apparent target of the
  analysis;
- report wording cannot preserve the pair-level market-flow limitation.
