# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3248`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-26T05:22:22Z`
Window: `2026-04-19T05:22:22Z` to `2026-05-03T05:22:22Z`
Artifact SHA-256: `29cfed81b4ac7430b3a3d4cd9ea34d6b3fbbad04d4488c597e49ead514ebda8b`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 78661.01461710568 | 77371.82563555888 | -1289.1889815468 | -1.638917305887956408574197336 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2024 | 3329 | 1305 | 64.47628458498023715415019763 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.061623958898 | -0.114265529544 | -0.175889488442 | -285.4238701754496941343198804 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 518529 | 633848 | 115319 | 22.2396432986390346537994982 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 783635801.6824999 | 2232908628.434068 | 1449272826.7515681 | 184.9421406780952029033370973 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 738579754.8618383 | 2134081650.583285 | 1395501895.7214467 | 188.9439680055263494521172325 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-19T05:22:22Z:2026-05-03T05:22:22Z`: 15 points, sha256 `4370f0f522e5bfc450da325c500a4cf79af0822ea8ce76df41c6b512f62e44e6`
- `santiment:bitcoin:social_volume_total:2026-04-19T05:22:22Z:2026-05-03T05:22:22Z`: 15 points, sha256 `d6f0c47c6cea291282701ac5144987bf38bc35e790d5a4f3d28cf42b6a9bfe6f`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-19T05:22:22Z:2026-05-03T05:22:22Z`: 15 points, sha256 `f5ec5ee78591ab38c8f534b05d0c5bbfc7d0b80270da3420a46e4df0fe7bdc81`
- `santiment:bitcoin:daily_active_addresses:2026-04-19T05:22:22Z:2026-05-03T05:22:22Z`: 15 points, sha256 `c45077ab9f02ace9c66cebf8d1870519d949b3c88f161524082c93c0ec016dcb`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-19T05:22:22Z:2026-05-03T05:22:22Z`: 15 points, sha256 `bede66a09842d8d898053f8d0782401505dad730976dd8879df01da5ed48eba4`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-19T05:22:22Z:2026-05-03T05:22:22Z`: 15 points, sha256 `95dee153ce4d265ebb5687b7f5a15eb4433ff33b19a11005604baa5d8e9356ab`
