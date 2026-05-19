# Real Open Data Source Selection

Status: selected for T117
Date: 2026-05-19
Audience: operator + development

## Decision

Selected source: Ethereum mainnet Uniswap V2 WETH/USDC pair `Swap` logs,
retrieved through public read-only JSON-RPC.

Evidence label:

- `real_open_data_rehearsal_not_private_evidence`

This is a development rehearsal source. It is real public on-chain data, not
synthetic data, but it is not private pilot evidence, paid-pilot evidence, PMF,
customer validation, market-demand evidence, or proof that traders will pay.

## Selected Source

| Field | Value |
|---|---|
| Chain | Ethereum mainnet |
| Protocol | Uniswap V2 |
| Pair | WETH/USDC |
| Pair contract | `0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc` |
| Event | `Swap(address indexed sender,uint256 amount0In,uint256 amount1In,uint256 amount0Out,uint256 amount1Out,address indexed to)` |
| Event topic | `0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822` |
| Primary access path | Public JSON-RPC `eth_getLogs` against `https://rpcfree.com/ethereum-rpc` |
| Fallback access path | Public JSON-RPC `eth_getLogs` against `https://ethereum.publicnode.com` |
| Committed case label | `real_open_dex_swaps_001` |

## Why This Source

- It is real executed DEX swap data recorded on Ethereum mainnet.
- It requires no Dune, BigQuery, exchange, or private-account credentials.
- It avoids selecting a random retail wallet and reduces doxxing risk.
- The pair-level log sequence is reproducible from public RPC.
- The event schema is published in the Uniswap V2 pair interface.

## Known Limitations

This source is weaker than an operator-approved private export:

- it is pair-level market flow, not one trader account ledger;
- `sender` is often a router contract, not the end trader;
- `to` can be a recipient, router, pair, or contract, not a safe customer label;
- event logs do not expose written trader risk rules;
- gas fees and user-level total costs are not available from the pair event;
- leverage, balances, account equity, deposits, withdrawals, and intent are not
  available;
- P&L is an audit-engine calculation on transformed rows, not verified
  trader-realized P&L.

These limitations must appear in the extraction contract, reviewed report, and
manual review note.

## Rejected Or Deferred Alternatives

| Source | Decision | Reason |
|---|---|---|
| Dune curated DEX trades | Deferred | Better account-like query path, but likely needs account/API/export workflow and operator approval for query cost/credentials. |
| Google BigQuery public blockchain datasets | Deferred | Real public chain data, but requires GCP access/cost controls and more decoding work. |
| Random public wallet DEX sequence | Rejected for first pass | Closer to account-like behavior, but creates unnecessary privacy/doxxing risk without a clearly public organization wallet. |
| SEC Insider Transactions Data Sets | Rejected for this phase | Official and real, but disclosure records are not a trader ledger and this repo already has an SEC reference case. |
| Binance public data | Rejected for this phase | Real exchange market tape, but not one account/trader and not suitable for trader-risk report claims. |

## Terms And Provenance Notes

- Ethereum mainnet logs are public blockchain data retrievable through standard
  JSON-RPC methods.
- Public RPC endpoints are used only for read-only access. No keys, secrets,
  account ids, or signed requests are required.
- `rpcfree.com` and `ethereum.publicnode.com` are access providers, not the
  data publisher.
- The Uniswap V2 pair event schema is sourced from the public Uniswap V2 core
  interface.
- Any committed rows must be transformed audit input, not private data.

## Boundary Language Required In Artifacts

Use this language in `source.md`, reviewed reports, dashboards, and ready-gate
updates:

> This pack uses real public Ethereum Uniswap V2 pair-level swap logs for a
> development rehearsal. It is not a private trader export, paid-pilot evidence,
> customer validation, PMF evidence, market-demand evidence, or trading advice.

## T117 Result

T117 is complete when `docs/REAL_OPEN_DATA_EXTRACTION_CONTRACT.md` defines the
exact block range, extraction command/query, field mapping, unsupported fields,
and privacy/provenance checklist before any transformed rows are committed.
