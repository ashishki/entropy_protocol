# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3273`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-15T11:53:36Z`
Window: `2026-05-08T11:53:36Z` to `2026-05-22T11:53:36Z`
Artifact SHA-256: `056b588128088909f194eb94915a0d795ea6bbf5d5ea570c4857649f5ff6e300`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 79071.77875021248 | 78142.21819353048 | -929.560556682 | -1.175590800377058805784559166 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 1420 |  |  |  | insufficient_pre_or_post_points |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.089357317512 |  |  |  | insufficient_pre_or_post_points |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 675479 | 576945 | -98534 | -14.58727806489913083900461746 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 322447685.7786611 |  |  |  | insufficient_pre_or_post_points |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 376317801.19047683 |  |  |  | insufficient_pre_or_post_points |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-05-08T11:53:36Z:2026-05-22T11:53:36Z`: 15 points, sha256 `1b5b57be47b852bbcfca975150f77f33bc7f33b30e1636e42374683483313209`
- `santiment:bitcoin:social_volume_total:2026-05-08T11:53:36Z:2026-05-22T11:53:36Z`: 3 points, sha256 `b3306520c53d4ec1ac4827a9c23c3b5bd9091fcab548d43a76102fd985652b3e`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-08T11:53:36Z:2026-05-22T11:53:36Z`: 3 points, sha256 `e5114008f49b5f7e4a08d14336e38e23430b574babae1c83f9ea06b7bca7910c`
- `santiment:bitcoin:daily_active_addresses:2026-05-08T11:53:36Z:2026-05-22T11:53:36Z`: 15 points, sha256 `d7ae7d8f5c85778c16a827ed28f44e8bc9f9c8b505c271ddbabb3dcf1412b11e`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-08T11:53:36Z:2026-05-22T11:53:36Z`: 3 points, sha256 `30fed3ce9daf2db7be6b4fbba765ff2ac4dcae1eab994a88dcc339670897321f`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-08T11:53:36Z:2026-05-22T11:53:36Z`: 3 points, sha256 `04111eac26d219edde23ec8a2e173a623cae846f3a46d605f3e3a2082b0ec4ab`
