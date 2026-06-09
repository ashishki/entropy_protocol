# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-3976`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-16T16:51:28Z`
Window: `2026-04-09T16:51:28Z` to `2026-04-23T16:51:28Z`
Artifact SHA-256: `f9b6c690d7b3a798c305246fb2c182be1bf835f6d68b04cbadfb3e1d7c38da9d`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 75164.04273182277 | 77124.50672883024 | 1960.46399700747 | 2.608247142855520610119493006 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2612 | 2810 | 198 | 7.580398162327718223583460949 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.036676066495 | 0.004337555369 | -0.032338511126 | -88.17333541046084309647285146 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 661123 | 663827 | 2704 | 0.4090010482164438387410512113 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 4248528188.531408 | 4710581883.183789 | 462053694.652381 | 10.87561795870064487655055372 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 4591154796.620364 | 4275712000.569435 | -315442796.050929 | -6.870663482815530778968452377 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-09T16:51:28Z:2026-04-23T16:51:28Z`: 15 points, sha256 `f77e11d55d18964cf45a1095a2a17206a6447d4b31c2b7417ed2c1ab0e7c8a5d`
- `santiment:bitcoin:social_volume_total:2026-04-09T16:51:28Z:2026-04-23T16:51:28Z`: 15 points, sha256 `a7e3cd37c2e8f136230ad04f4a387beddb924aa36f3c63520d256bdb805b6a81`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-09T16:51:28Z:2026-04-23T16:51:28Z`: 15 points, sha256 `dd33cc22f0e0e7ed773d9160bc20018fb2ffa6313a3ffa6403ee7ea8c18cf331`
- `santiment:bitcoin:daily_active_addresses:2026-04-09T16:51:28Z:2026-04-23T16:51:28Z`: 15 points, sha256 `6ccaff5833e955d9433e48e69bfeef57ddd238b4f1df968122335ce19ea62b9a`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-09T16:51:28Z:2026-04-23T16:51:28Z`: 15 points, sha256 `90eb0a648318cf62d96627164ccf971a154d7116e229975fa27c5076cb386bb8`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-09T16:51:28Z:2026-04-23T16:51:28Z`: 15 points, sha256 `87a48b92ef8b80941a740d3caeadc038638f7093d5fc851dde0fc514c8c37f59`
