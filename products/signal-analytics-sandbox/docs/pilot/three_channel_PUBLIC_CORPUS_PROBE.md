# Three-Channel Public Corpus Probe

Date: 2026-05-17T09:32:50Z
Status: public_probe_completed_operator_mapping_required

## Boundary

- Sources: public Telegram `/s/` pages only.
- No private Telegram, login-walled, paywalled, or access-control bypass source was used.
- This artifact does not fetch market data, compute outcomes, approve proxies, or create external claims.
- Candidate labels are review queues, not investment advice and not proof of author skill.

## Summary

| channel | text rows | market candidates | explicit setups | position/trade language | directional bias | first pass |
|---|---:|---:|---:|---:|---:|---|
| `bablos79` | 528 | 202 | 3 | 33 | 127 | `fixed_horizon_directional_backtest` |
| `nemphiscrypts` | 514 | 336 | 18 | 21 | 226 | `fixed_horizon_directional_backtest` |
| `pifagortrade` | 492 | 425 | 43 | 60 | 271 | `position_disclosure_and_directional_backtest` |

## Interpretation

- `pifagortrade` is the best first candidate for classic setup/directional backtesting because it has the largest number of explicit setup fields and trade-language rows.
- `nemphiscrypts` is suitable for crypto directional and scenario backtesting after operator-approved BTC/ETH/alt proxy rules.
- `bablos79` remains more mixed: useful rows exist, but many are context or position-management fragments, so it needs stricter operator mapping.

## Operator Decisions Needed

1. Approve the per-channel first-pass evaluator type: setup, directional fixed-horizon, position disclosure, or context-only.
2. Approve proxy mapping rules before any market data fetch, especially Russian equities/futures for `bablos79` and BTC/ETH/alt proxies for crypto channels.
3. Approve horizon rules per candidate type: immediate next close, 1d/3d/7d/30d, next disclosure, or invalid if no timestamp/asset.
4. Decide whether scenario posts without explicit entry/stop/target can be evaluated as directional forecasts or kept as context only.

## Top Candidates

### `bablos79`

| candidate | timestamp | category | assets | source |
|---|---|---|---|---|
| `bablos79-10257` | `2026-03-25T08:02:57+00:00` | `explicit_setup_candidate` | SMLT | [source](https://t.me/bablos79/10257) |
| `bablos79-10335` | `2026-04-10T08:59:40+00:00` | `explicit_setup_candidate` | SBER | [source](https://t.me/bablos79/10335) |
| `bablos79-10501` | `2026-05-05T12:55:18+00:00` | `explicit_setup_candidate` | MAGN | [source](https://t.me/bablos79/10501) |
| `bablos79-9999` | `2026-02-18T18:00:57+00:00` | `position_or_trade_language_candidate` | GOLD, GOLDM | [source](https://t.me/bablos79/9999) |
| `bablos79-10008` | `2026-02-19T18:04:22+00:00` | `position_or_trade_language_candidate` | GD, NKNC, PRMD, VTBR, WUSH | [source](https://t.me/bablos79/10008) |
| `bablos79-10009` | `2026-02-19T18:19:49+00:00` | `position_or_trade_language_candidate` | GD, NKNC, PRMD, VTBR, WUSH | [source](https://t.me/bablos79/10009) |
| `bablos79-10013` | `2026-02-20T14:47:42+00:00` | `position_or_trade_language_candidate` | VTBR | [source](https://t.me/bablos79/10013) |
| `bablos79-10122` | `2026-03-06T15:01:32+00:00` | `position_or_trade_language_candidate` | BR, CN, NKNC, PRMD, SI, VTBR, WUSH | [source](https://t.me/bablos79/10122) |
| `bablos79-10142` | `2026-03-09T14:17:17+00:00` | `position_or_trade_language_candidate` | VTBR | [source](https://t.me/bablos79/10142) |
| `bablos79-10162` | `2026-03-13T07:30:36+00:00` | `position_or_trade_language_candidate` | CNY, NG, NKNC, PRMD, SI, SPY, WUSH | [source](https://t.me/bablos79/10162) |
| `bablos79-10208` | `2026-03-20T08:56:19+00:00` | `position_or_trade_language_candidate` | PHOR | [source](https://t.me/bablos79/10208) |
| `bablos79-10219` | `2026-03-20T14:08:33+00:00` | `position_or_trade_language_candidate` | CN, NG, NKNC, PHOR, PRMD, SI, SPYF | [source](https://t.me/bablos79/10219) |
| `bablos79-10277` | `2026-03-27T15:46:33+00:00` | `position_or_trade_language_candidate` | CNY, GOLD, NG, NVTK, PRMD, SI, SPYF, VTBR | [source](https://t.me/bablos79/10277) |
| `bablos79-10331` | `2026-04-10T07:20:43+00:00` | `position_or_trade_language_candidate` | GD | [source](https://t.me/bablos79/10331) |
| `bablos79-10332` | `2026-04-10T07:28:51+00:00` | `position_or_trade_language_candidate` | NVTK | [source](https://t.me/bablos79/10332) |
| `bablos79-10333` | `2026-04-10T07:44:50+00:00` | `position_or_trade_language_candidate` | NVTK | [source](https://t.me/bablos79/10333) |
| `bablos79-10338` | `2026-04-10T12:16:29+00:00` | `position_or_trade_language_candidate` | LENT | [source](https://t.me/bablos79/10338) |
| `bablos79-10339` | `2026-04-11T06:11:51+00:00` | `position_or_trade_language_candidate` | CNY, SI, SPYF, VTBR | [source](https://t.me/bablos79/10339) |
| `bablos79-10352` | `2026-04-13T12:42:08+00:00` | `position_or_trade_language_candidate` | VTBR | [source](https://t.me/bablos79/10352) |
| `bablos79-10357` | `2026-04-14T05:48:52+00:00` | `position_or_trade_language_candidate` | CBOM | [source](https://t.me/bablos79/10357) |

### `nemphiscrypts`

| candidate | timestamp | category | assets | source |
|---|---|---|---|---|
| `nemphiscrypts-3380` | `2025-05-11T13:09:10+00:00` | `explicit_setup_candidate` | BRIAN | [source](https://t.me/nemphiscrypts/3380) |
| `nemphiscrypts-3384` | `2025-05-12T13:00:22+00:00` | `explicit_setup_candidate` | BNB | [source](https://t.me/nemphiscrypts/3384) |
| `nemphiscrypts-3399` | `2025-05-18T08:39:30+00:00` | `explicit_setup_candidate` | TONGUE | [source](https://t.me/nemphiscrypts/3399) |
| `nemphiscrypts-3451` | `2025-06-06T16:57:40+00:00` | `explicit_setup_candidate` | BRIAN | [source](https://t.me/nemphiscrypts/3451) |
| `nemphiscrypts-3517` | `2025-06-16T15:49:27+00:00` | `explicit_setup_candidate` | ETH, ETHOS | [source](https://t.me/nemphiscrypts/3517) |
| `nemphiscrypts-3519` | `2025-06-17T14:08:01+00:00` | `explicit_setup_candidate` | USDC/USDT | [source](https://t.me/nemphiscrypts/3519) |
| `nemphiscrypts-3526` | `2025-06-22T13:15:10+00:00` | `explicit_setup_candidate` | SOL | [source](https://t.me/nemphiscrypts/3526) |
| `nemphiscrypts-3539` | `2025-07-02T07:00:37+00:00` | `explicit_setup_candidate` | AVAX, SOL | [source](https://t.me/nemphiscrypts/3539) |
| `nemphiscrypts-3590` | `2025-08-05T07:59:47+00:00` | `explicit_setup_candidate` | USDC/USDT | [source](https://t.me/nemphiscrypts/3590) |
| `nemphiscrypts-3627` | `2025-09-06T09:48:12+00:00` | `explicit_setup_candidate` | ETHENA | [source](https://t.me/nemphiscrypts/3627) |
| `nemphiscrypts-3663` | `2025-09-16T16:50:43+00:00` | `explicit_setup_candidate` | BTC-E | [source](https://t.me/nemphiscrypts/3663) |
| `nemphiscrypts-3780` | `2025-10-19T10:42:48+00:00` | `explicit_setup_candidate` | ETH, USDT | [source](https://t.me/nemphiscrypts/3780) |
| `nemphiscrypts-3936` | `2026-03-08T14:34:55+00:00` | `explicit_setup_candidate` | OPTIONS/HFT | [source](https://t.me/nemphiscrypts/3936) |
| `nemphiscrypts-3975` | `2026-04-15T20:07:29+00:00` | `explicit_setup_candidate` | ETHEREAL, SOLAYER | [source](https://t.me/nemphiscrypts/3975) |
| `nemphiscrypts-3984` | `2026-04-18T19:27:24+00:00` | `explicit_setup_candidate` | BR, SIREN | [source](https://t.me/nemphiscrypts/3984) |
| `nemphiscrypts-3996` | `2026-04-23T17:03:09+00:00` | `explicit_setup_candidate` | APTOS, SUI | [source](https://t.me/nemphiscrypts/3996) |
| `nemphiscrypts-4007` | `2026-04-26T05:54:12+00:00` | `explicit_setup_candidate` | MELANIA, TRUMP | [source](https://t.me/nemphiscrypts/4007) |
| `nemphiscrypts-4050` | `2026-05-05T13:18:51+00:00` | `explicit_setup_candidate` | ARBITRUM, SIREN | [source](https://t.me/nemphiscrypts/4050) |
| `nemphiscrypts-3397` | `2025-05-17T10:31:40+00:00` | `position_or_trade_language_candidate` | ETHOS | [source](https://t.me/nemphiscrypts/3397) |
| `nemphiscrypts-3413` | `2025-05-22T17:22:22+00:00` | `position_or_trade_language_candidate` | OPENSEA | [source](https://t.me/nemphiscrypts/3413) |

### `pifagortrade`

| candidate | timestamp | category | assets | source |
|---|---|---|---|---|
| `pifagortrade-2510` | `2024-05-15T08:47:11+00:00` | `explicit_setup_candidate` | BTCUSD | [source](https://t.me/pifagortrade/2510) |
| `pifagortrade-2578` | `2024-07-14T15:30:14+00:00` | `explicit_setup_candidate` | BTC, SIGN-UP, USDT | [source](https://t.me/pifagortrade/2578) |
| `pifagortrade-2606` | `2024-08-05T15:25:57+00:00` | `explicit_setup_candidate` | SIGN-UP, USDT | [source](https://t.me/pifagortrade/2606) |
| `pifagortrade-2655` | `2024-10-11T18:00:10+00:00` | `explicit_setup_candidate` | BTC, SIGN-UP, USDT | [source](https://t.me/pifagortrade/2655) |
| `pifagortrade-2676` | `2024-11-07T16:39:40+00:00` | `explicit_setup_candidate` | SI | [source](https://t.me/pifagortrade/2676) |
| `pifagortrade-2690` | `2024-11-26T13:30:09+00:00` | `explicit_setup_candidate` | BTCPARSER, OPPORTUNITY, USDT | [source](https://t.me/pifagortrade/2690) |
| `pifagortrade-2701` | `2024-12-05T20:39:29+00:00` | `explicit_setup_candidate` | BTC | [source](https://t.me/pifagortrade/2701) |
| `pifagortrade-2702` | `2024-12-06T10:00:12+00:00` | `explicit_setup_candidate` | USDT | [source](https://t.me/pifagortrade/2702) |
| `pifagortrade-2705` | `2024-12-09T10:23:39+00:00` | `explicit_setup_candidate` | BTC | [source](https://t.me/pifagortrade/2705) |
| `pifagortrade-2706` | `2024-12-10T20:30:09+00:00` | `explicit_setup_candidate` | BTC | [source](https://t.me/pifagortrade/2706) |
| `pifagortrade-2710` | `2024-12-11T09:41:41+00:00` | `explicit_setup_candidate` | BTC, GOLDMAN, USDT | [source](https://t.me/pifagortrade/2710) |
| `pifagortrade-2713` | `2024-12-17T09:30:07+00:00` | `explicit_setup_candidate` | BTC, USDT | [source](https://t.me/pifagortrade/2713) |
| `pifagortrade-2773` | `2025-02-03T03:12:19+00:00` | `explicit_setup_candidate` | BTC-, ETH | [source](https://t.me/pifagortrade/2773) |
| `pifagortrade-2774` | `2025-02-03T08:37:43+00:00` | `explicit_setup_candidate` | USDT | [source](https://t.me/pifagortrade/2774) |
| `pifagortrade-2785` | `2025-02-17T09:51:51+00:00` | `explicit_setup_candidate` | BTC, USDT | [source](https://t.me/pifagortrade/2785) |
| `pifagortrade-2795` | `2025-02-25T09:04:30+00:00` | `explicit_setup_candidate` | BTC, USDT | [source](https://t.me/pifagortrade/2795) |
| `pifagortrade-2805` | `2025-03-01T07:00:11+00:00` | `explicit_setup_candidate` | BTC, ETH, USDT | [source](https://t.me/pifagortrade/2805) |
| `pifagortrade-2811` | `2025-03-08T14:30:14+00:00` | `explicit_setup_candidate` | BTC-, USDT | [source](https://t.me/pifagortrade/2811) |
| `pifagortrade-2812` | `2025-03-10T18:32:33+00:00` | `explicit_setup_candidate` | USDT | [source](https://t.me/pifagortrade/2812) |
| `pifagortrade-2824` | `2025-03-31T13:17:51+00:00` | `explicit_setup_candidate` | USDT | [source](https://t.me/pifagortrade/2824) |
