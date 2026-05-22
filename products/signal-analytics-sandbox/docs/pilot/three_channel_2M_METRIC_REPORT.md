# Three-Channel Metric Report V0

Date: 2026-05-22T06:17:26Z
Status: historical_metric_results_v0_open_public_data

## Boundary

- Sources: public Telegram `/s/` pages only.
- Date window: `2026-03-22` through `2026-05-22` inclusive.
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

| channel | coverage | text rows | normalized claims | 7d evaluable | confirmed | contradicted | hit rate | avg directional 7d return | avg MFE | avg MAE |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bablos79` | 2026-03-23T07:43:07+00:00 -> 2026-05-21T21:07:23+00:00 | 340 | 21 | 17 | 10 | 7 | 58.823529 | 0.213022 | 3.395637 | -3.098168 |
| `nemphiscrypts` | 2026-03-23T18:12:48+00:00 -> 2026-05-22T03:19:44+00:00 | 132 | 9 | 5 | 4 | 1 | 80.000000 | -0.148958 | 4.439903 | -3.737571 |
| `pifagortrade` | 2026-03-27T09:40:35+00:00 -> 2026-05-20T16:06:46+00:00 | 54 | 7 | 6 | 5 | 1 | 83.333333 | 5.382339 | 8.727584 | -3.017294 |

## Interpretation

- `primary_hit_rate` counts whether the price moved in the stated direction over the 7-day window.
- `avg_directional_return_pct` is the conditional return of a simple direction-only position: long keeps raw return, short flips the sign.
- `avg_mfe_pct` and `avg_mae_pct` show favorable/adverse excursion during the same 7-day window.
- Unevaluable rows are not treated as failures; they remain in coverage and exclusion counts.

## Exclusions

### `bablos79`
Evaluation statuses:
- `evaluated`: 17
- `no_primary_horizon`: 4

Extraction exclusions:
- `mixed_direction`: 5
- `no_direction`: 38
- `no_supported_asset_or_proxy`: 47
- `no_text`: 41
- `not_market_related`: 229

### `nemphiscrypts`
Evaluation statuses:
- `evaluated`: 5
- `no_primary_horizon`: 4

Extraction exclusions:
- `mixed_direction`: 3
- `no_direction`: 2
- `no_supported_asset_or_proxy`: 47
- `no_text`: 1
- `not_market_related`: 73

### `pifagortrade`
Evaluation statuses:
- `evaluated`: 6
- `no_primary_horizon`: 1

Extraction exclusions:
- `mixed_direction`: 7
- `no_direction`: 1
- `no_supported_asset_or_proxy`: 20
- `no_text`: 1
- `not_market_related`: 21

## Confirmed Examples

### `bablos79`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `10332` | `NVTK` | `short` | 5.505554 | [source](https://t.me/bablos79/10332) |
| `10338` | `LENT` | `long` | 0.796253 | [source](https://t.me/bablos79/10338) |
| `10359` | `SMLT` | `long` | 0.163399 | [source](https://t.me/bablos79/10359) |
| `10386` | `SBER` | `long` | 0.407571 | [source](https://t.me/bablos79/10386) |
| `10426` | `CHMF` | `short` | 5.023744 | [source](https://t.me/bablos79/10426) |

### `nemphiscrypts`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `3977` | `ETH` | `short` | 0.762722 | [source](https://t.me/nemphiscrypts/3977) |
| `3978` | `BTC` | `long` | 0.473752 | [source](https://t.me/nemphiscrypts/3978) |
| `4018` | `ETH` | `long` | 1.486151 | [source](https://t.me/nemphiscrypts/4018) |
| `4024` | `ETH` | `long` | 0.497903 | [source](https://t.me/nemphiscrypts/4024) |

### `pifagortrade`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `3259` | `BTC` | `short` | 0.495702 | [source](https://t.me/pifagortrade/3259) |
| `3259` | `ETH` | `short` | 3.634831 | [source](https://t.me/pifagortrade/3259) |
| `3267` | `BTC` | `short` | 5.780800 | [source](https://t.me/pifagortrade/3267) |
| `3267` | `TON` | `short` | 22.835280 | [source](https://t.me/pifagortrade/3267) |
| `3273` | `BTC` | `short` | 2.078401 | [source](https://t.me/pifagortrade/3273) |

## Contradicted Examples

### `bablos79`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `10250` | `BTC` | `long` | -5.795072 | [source](https://t.me/bablos79/10250) |
| `10257` | `SMLT` | `long` | -5.937235 | [source](https://t.me/bablos79/10257) |
| `10335` | `SBER` | `short` | -2.073813 | [source](https://t.me/bablos79/10335) |
| `10388` | `GAZP` | `long` | -1.146936 | [source](https://t.me/bablos79/10388) |
| `10442` | `X5` | `long` | -3.015075 | [source](https://t.me/bablos79/10442) |

### `nemphiscrypts`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `3996` | `SUI` | `long` | -3.965317 | [source](https://t.me/nemphiscrypts/3996) |

### `pifagortrade`

| post | asset | direction | 7d directional return | evidence |
|---|---|---|---:|---|
| `3255` | `BTC` | `short` | -2.530982 | [source](https://t.me/pifagortrade/3255) |
