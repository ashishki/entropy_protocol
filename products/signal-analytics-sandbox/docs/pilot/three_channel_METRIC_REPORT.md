# Three-Channel Metric Report V0

Date: 2026-05-17T09:56:15Z
Status: historical_metric_results_v0_open_public_data

## Boundary

- Sources: public Telegram `/s/` pages only.
- Market validation: open/public daily OHLCV windows via Binance public klines and MOEX ISS candles.
- Storage posture: no bulk market-history database; this run stores only compact per-claim metrics and provider confirmation metadata.
- Primary comparison horizon: `7d` directional return after the public post timestamp using the first available daily candle on/after the post date.
- This is historical research, not investment advice or a future-profit claim.

## V0 Evaluation Rules

- Included rows must have public timestamp, supported asset/proxy, and single long/short direction.
- Supported V0 providers: Binance public daily klines for crypto and MOEX ISS daily candles for supported MOEX shares.
- Unsupported assets, missing direction, mixed direction, media-only rows, and non-market rows are excluded from performance but retained in coverage counts.
- Multi-asset posts are evaluated as asset-level claims, so one post may produce more than one measured row.

## Channel Comparison

| channel | text rows | normalized claims | 7d evaluable | confirmed | contradicted | hit rate | avg directional 7d return | avg MFE | avg MAE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bablos79` | 528 | 20 | 19 | 11 | 8 | 57.894737 | 0.381485 | 3.861603 | -3.295579 |
| `nemphiscrypts` | 514 | 53 | 53 | 31 | 22 | 58.490566 | 0.857037 | 8.111611 | -7.282735 |
| `pifagortrade` | 492 | 114 | 112 | 60 | 52 | 53.571429 | 0.071093 | 6.455524 | -6.894253 |

## Interpretation

- `primary_hit_rate` counts whether the price moved in the stated direction over the 7-day window.
- `avg_directional_return_pct` is the conditional return of a simple direction-only position: long keeps raw return, short flips the sign.
- `avg_mfe_pct` and `avg_mae_pct` show favorable/adverse excursion during the same 7-day window.
- Unevaluable rows are not treated as failures; they remain in coverage and exclusion counts.

## Exclusions

### `bablos79`
- `mixed_direction`: 11
- `no_direction`: 38
- `no_supported_asset_or_proxy`: 75
- `no_text`: 63
- `not_market_related`: 384

### `nemphiscrypts`
- `mixed_direction`: 32
- `no_direction`: 17
- `no_supported_asset_or_proxy`: 128
- `no_text`: 15
- `not_market_related`: 291

### `pifagortrade`
- `mixed_direction`: 90
- `no_direction`: 28
- `no_supported_asset_or_proxy`: 162
- `no_text`: 5
- `not_market_related`: 133

## Confirmed Examples

### `bablos79`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `10114` | `LKOH` | `long` | 2.741306 | [source](https://t.me/bablos79/10114) |
| `10208` | `PHOR` | `short` | 4.443290 | [source](https://t.me/bablos79/10208) |
| `10332` | `NVTK` | `short` | 5.505554 | [source](https://t.me/bablos79/10332) |
| `10338` | `LENT` | `long` | 0.796253 | [source](https://t.me/bablos79/10338) |
| `10359` | `SMLT` | `long` | 0.163399 | [source](https://t.me/bablos79/10359) |

### `nemphiscrypts`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `3344` | `BTC` | `long` | 0.486250 | [source](https://t.me/nemphiscrypts/3344) |
| `3367` | `ETH` | `long` | 15.461699 | [source](https://t.me/nemphiscrypts/3367) |
| `3372` | `ETH` | `long` | 8.190905 | [source](https://t.me/nemphiscrypts/3372) |
| `3387` | `BTC` | `long` | 2.706863 | [source](https://t.me/nemphiscrypts/3387) |
| `3395` | `BTC` | `long` | 7.644773 | [source](https://t.me/nemphiscrypts/3395) |

### `pifagortrade`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `2334` | `BTC` | `long` | 14.554088 | [source](https://t.me/pifagortrade/2334) |
| `2454` | `BTC` | `long` | 4.915714 | [source](https://t.me/pifagortrade/2454) |
| `2454` | `ETH` | `long` | 5.204980 | [source](https://t.me/pifagortrade/2454) |
| `2512` | `BTC` | `long` | 4.471041 | [source](https://t.me/pifagortrade/2512) |
| `2643` | `BTC` | `long` | 3.182273 | [source](https://t.me/pifagortrade/2643) |

## Contradicted Examples

### `bablos79`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `10217` | `VTBR` | `long` | -3.387463 | [source](https://t.me/bablos79/10217) |
| `10250` | `BTC` | `long` | -5.795072 | [source](https://t.me/bablos79/10250) |
| `10257` | `SMLT` | `long` | -5.937235 | [source](https://t.me/bablos79/10257) |
| `10335` | `SBER` | `short` | -2.073813 | [source](https://t.me/bablos79/10335) |
| `10388` | `GAZP` | `long` | -1.146936 | [source](https://t.me/bablos79/10388) |

### `nemphiscrypts`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `3376` | `BTC` | `long` | -1.605656 | [source](https://t.me/nemphiscrypts/3376) |
| `3405` | `BTC` | `long` | -1.698415 | [source](https://t.me/nemphiscrypts/3405) |
| `3505` | `AVAX` | `long` | -11.146329 | [source](https://t.me/nemphiscrypts/3505) |
| `3505` | `ETH` | `long` | -9.286934 | [source](https://t.me/nemphiscrypts/3505) |
| `3522` | `DOT` | `long` | -7.018038 | [source](https://t.me/nemphiscrypts/3522) |

### `pifagortrade`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `2498` | `BTC` | `long` | -4.798798 | [source](https://t.me/pifagortrade/2498) |
| `2647` | `ETH` | `long` | -0.281887 | [source](https://t.me/pifagortrade/2647) |
| `2699` | `BTC` | `short` | -3.155026 | [source](https://t.me/pifagortrade/2699) |
| `2710` | `BTC` | `long` | -0.910744 | [source](https://t.me/pifagortrade/2710) |
| `2713` | `BTC` | `long` | -7.038440 | [source](https://t.me/pifagortrade/2713) |
