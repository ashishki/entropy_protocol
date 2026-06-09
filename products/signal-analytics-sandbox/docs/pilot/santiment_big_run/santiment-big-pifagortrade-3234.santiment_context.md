# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3234`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-14T05:38:21Z`
Window: `2026-04-07T05:38:21Z` to `2026-04-21T05:38:21Z`
Artifact SHA-256: `0fb595cfeefeaccd102f11ac58e21636c4ae5bf2fbfd8dce8e808b9287a22209`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 74182.02650290522 | 74810.87456393745 | 628.84806103223 | 0.8477094663996570315321109272 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2542 | 2356 | -186 | -7.317073170731707317073170732 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.008428430347 | -0.004911929611 | -0.013340359958 | -158.2781064655572931674842492 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 660788 | 634125 | -26663 | -4.03503090249822938673220458 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 4373186015.029364 | 2353485154.028308 | -2019700861.001056 | -46.18374004810071191477263761 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 4410452716.396477 | 2753268651.3159413 | -1657184065.0805357 | -37.57401272934457147348944673 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-07T05:38:21Z:2026-04-21T05:38:21Z`: 15 points, sha256 `d60a7ffe1fdc10262b8cdb7249e0eabe333107a21974f1096c48a2aa7a280a14`
- `santiment:bitcoin:social_volume_total:2026-04-07T05:38:21Z:2026-04-21T05:38:21Z`: 15 points, sha256 `5f9926d21b53f69167cf4931c10db3792db6252d648f64a5c2895db6eb0f6f6c`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-07T05:38:21Z:2026-04-21T05:38:21Z`: 15 points, sha256 `1c72b2e63c5b14121a6192f54af7624c579058074fbc073df1dc6ea7ef8a33bb`
- `santiment:bitcoin:daily_active_addresses:2026-04-07T05:38:21Z:2026-04-21T05:38:21Z`: 15 points, sha256 `ac0ada92c43a776cab7845f428376ee9fb9e806b3fdf3ecf6e83fd1f519979f9`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-07T05:38:21Z:2026-04-21T05:38:21Z`: 15 points, sha256 `6b717b4606979049267762f727c52a95495dd4e048401e5a161c1794826c5668`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-07T05:38:21Z:2026-04-21T05:38:21Z`: 15 points, sha256 `a7a6804332e019c0c03e026f7a4866bf38171691b48b334d765ca4a8a518e1c2`
