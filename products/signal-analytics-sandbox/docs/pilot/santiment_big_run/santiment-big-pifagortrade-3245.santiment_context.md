# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3245`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-18T17:48:36Z`
Window: `2026-04-11T17:48:36Z` to `2026-04-25T17:48:36Z`
Artifact SHA-256: `edd8630a40b8290b52e9fb1ce3bc4b8dab70e184db157c14a8a46fcf4fd28f6f`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 75738.82460973389 | 73854.24640440254 | -1884.57820533135 | -2.488259112868706434927146032 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2412 | 2179 | -233 | -9.660033167495854063018242123 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | -0.004056644742 | 0.031879056974 | 0.035935701716 | -885.8478866523333336542882315 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 566689 | 527619 | -39070 | -6.894434160536025933095577998 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 2374469327.600815 | 1591140944.5784674 | -783328383.0223476 | -32.9896189399856172985520909 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 2107594683.9431882 | 1417438459.8399777 | -690156224.1032105 | -32.74615510094037512497521767 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-11T17:48:36Z:2026-04-25T17:48:36Z`: 15 points, sha256 `d4b1c6a23753cc830cd2c6dabb3207f052f4d0963c0daf4a25c1a81556cbe209`
- `santiment:bitcoin:social_volume_total:2026-04-11T17:48:36Z:2026-04-25T17:48:36Z`: 15 points, sha256 `ba82f1dfd72e3b1b109cc7d97ce61d052000f2c7659ed0ddeec5bc62652384b3`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-11T17:48:36Z:2026-04-25T17:48:36Z`: 15 points, sha256 `a5cbac185c3840ec51b589880dac7a8329b1670017babc15626f3628918b589b`
- `santiment:bitcoin:daily_active_addresses:2026-04-11T17:48:36Z:2026-04-25T17:48:36Z`: 15 points, sha256 `35f9697185bcf794a968cb96e65cf6033a9dd7af0f0feb19bb1b17ac17d4070a`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-11T17:48:36Z:2026-04-25T17:48:36Z`: 15 points, sha256 `120949fe71201563b79f0d8cfffa9095f0c3102d16497d5635ac8a46dfa51c2f`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-11T17:48:36Z:2026-04-25T17:48:36Z`: 15 points, sha256 `cbf86d55030983976edf703f368070942b5894c1455a7180e57da1a9dd229296`
