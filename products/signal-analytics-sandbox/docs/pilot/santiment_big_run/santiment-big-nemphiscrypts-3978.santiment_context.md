# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-3978`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-17T13:01:58Z`
Window: `2026-04-10T13:01:58Z` to `2026-04-24T13:01:58Z`
Artifact SHA-256: `b5bc6c3bee521b06d779d9f712b54d68ea323f0b9d710d6f2eff4db64540261c`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 77124.50672883024 | 75738.82460973389 | -1385.68211909635 | -1.796681985880841000482908017 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2810 | 2412 | -398 | -14.16370106761565836298932384 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.004337555369 | -0.004056644742 | -0.008394200111 | -193.5237569759308356623769936 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 663827 | 566689 | -97138 | -14.63302938868108709046182213 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 4710581883.183789 | 2374469327.600815 | -2336112555.582974 | -49.59286588186939213692830022 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 4275712000.569435 | 2107594683.9431882 | -2168117316.6262468 | -50.70774917341250132128587059 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-10T13:01:58Z:2026-04-24T13:01:58Z`: 15 points, sha256 `2ccc4687f73085a0133733f34ffe56862fdf76064d1e32e85cfc316ed0f237fb`
- `santiment:bitcoin:social_volume_total:2026-04-10T13:01:58Z:2026-04-24T13:01:58Z`: 15 points, sha256 `2bbbcc58cb5acfdcef486a9d9012e3515f1d069c70d031e00301665bd6002ced`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-10T13:01:58Z:2026-04-24T13:01:58Z`: 15 points, sha256 `5bd69288b9e252dabad17a175111ded6ebdede3d0ed0c56f78f1cb6f346bc2a1`
- `santiment:bitcoin:daily_active_addresses:2026-04-10T13:01:58Z:2026-04-24T13:01:58Z`: 15 points, sha256 `ecafbe4853125d908f8671c6d75e0cd28d58d5d5e84973032c51d366feb58ab8`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-10T13:01:58Z:2026-04-24T13:01:58Z`: 15 points, sha256 `d7eab5f92bb7df3e39c17af5c8f7751ecb755565883b51a3b4189208778a926f`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-10T13:01:58Z:2026-04-24T13:01:58Z`: 15 points, sha256 `506308f4e5b7c4ac314d1e02b9253fa62df7332bc1b983f9ccb3e158cc608848`
