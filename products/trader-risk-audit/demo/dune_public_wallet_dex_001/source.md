# Dune Public Wallet DEX Source Metadata

source_name: Dune `dex.trades` Ethereum submitter-scoped DEX rows
source_label: real_open_dune_public_wallet_rehearsal_not_private_evidence
source_access_path: Dune API SQL execution
source_dataset: dex.trades
source_blockchain: ethereum
source_time_window: trailing 14 days at Dune execution time
source_discovery_execution_id: 01KS03EPE54GHM030GTF2TDXMY
source_extract_execution_id: 01KS03JCBRKKNRN8YP1K7DQ9KD
source_accessed_date: 2026-05-19
public_wallet_scope: 0xc468315a...f74ca6
row_count_committed: 80
privacy_reviewed_by: codex
privacy_review_date: 2026-05-19

## Boundary

This pack uses real public Ethereum DEX rows returned by Dune for a public
`tx_from` address. It is a development rehearsal only. It is not a private
trader export, paid-pilot evidence, PMF evidence, customer validation,
market-demand evidence, proof that traders will pay, trading advice, or live
trading control.

## Selection Query

The discovery query searched public Ethereum `dex.trades` rows over the trailing
14-day window for submitter addresses with 20-150 trades and ranked them by
USD volume. The selected address had 127 rows and about 4.1M USD notional in the
discovery result.

```sql
select
  tx_from as wallet,
  count(*) as trades,
  approx_distinct(tx_hash) as transactions,
  sum(amount_usd) as volume_usd,
  min(block_time) as first_trade,
  max(block_time) as last_trade
from dex.trades
where blockchain = 'ethereum'
  and block_time >= now() - interval '14' day
  and amount_usd between 100 and 50000
  and tx_from is not null
group by 1
having count(*) between 20 and 150
order by volume_usd desc
limit 20
```

## Extraction Query

```sql
select
  block_time,
  blockchain,
  project,
  version,
  tx_hash,
  evt_index,
  tx_from,
  tx_to,
  taker,
  maker,
  token_pair,
  token_bought_symbol,
  token_sold_symbol,
  token_bought_amount,
  token_sold_amount,
  amount_usd
from dex.trades
where blockchain = 'ethereum'
  and block_time >= now() - interval '14' day
  and amount_usd is not null
  and token_bought_amount is not null
  and token_bought_amount > 0
  and tx_from = 0xc468315a2df54f9c076bd5cfe5002ba211f74ca6
order by block_time, tx_hash, evt_index
limit 80
```

## Transformation Summary

- `timestamp`: Dune `block_time` rendered as UTC ISO-8601.
- `symbol`: Dune `token_bought_symbol`, uppercased.
- `side`: fixed to `buy` because the committed row captures the bought token
  side of each public DEX swap.
- `quantity`: Dune `token_bought_amount`.
- `price`: Dune `amount_usd / token_bought_amount`.
- `fees`: `0` schema placeholder; gas, LP fee, MEV/slippage, and all-in user
  execution costs are unsupported by this source.
- `account_id`: safe public scope label, not a wallet owner or customer id.

## Provenance Sample

| Row | Timestamp | Project | Pair | Amount USD | Truncated transaction hash | Event index |
|---:|---|---|---|---:|---|---:|
| 1 | 2026-05-05 20:43:47.000 UTC | uniswap | USDe-USDT | 720057.4470756935 | `0xe53a4eaf33...` | 575 |
| 2 | 2026-05-05 20:43:47.000 UTC | fluid | USDe-USDT | 280023.0335674039 | `0xe53a4eaf33...` | 582 |
| 3 | 2026-05-06 00:54:35.000 UTC | uniswap | USDe-USDT | 679855.8257265163 | `0xf0923a8b11...` | 719 |
| 4 | 2026-05-06 00:54:35.000 UTC | fluid | USDe-USDT | 319930.9950324409 | `0xf0923a8b11...` | 726 |
| 5 | 2026-05-06 17:51:23.000 UTC | uniswap | USDC-USDT | 319999.78410140704 | `0x4eb4e5c6a4...` | 939 |

## Fields Not Supported

- private wallet owner or trader identity;
- private exchange account id;
- written user risk rules;
- gas, LP fees, MEV/slippage, and all-in execution costs;
- leverage and margin;
- account equity, deposits, withdrawals, and balances;
- verified realized trader P&L;
- order intent, stop-loss intent, or strategy.

## Privacy Review

No private rows, credentials, payment identifiers, private paths, screenshots,
customer identifiers, or wallet-owner claims are committed. The full public
address appears only inside the Dune SQL provenance query so the extraction can
be independently re-run; the committed audit `account_id` is a safe scope label.
