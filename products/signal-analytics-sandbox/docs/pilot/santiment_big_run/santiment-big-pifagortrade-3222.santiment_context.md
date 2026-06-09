# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3222`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-06T06:07:36Z`
Window: `2026-03-30T06:07:36Z` to `2026-04-13T06:07:36Z`
Artifact SHA-256: `6580c000289b44ac3251a0cb4c5d0451d9138646b80b672688591e589e038b31`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 68896.75374779342 | 71913.6133848375 | 3016.85963704408 | 4.378812459129399837594899035 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2235 | 2134 | -101 | -4.519015659955257270693512304 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.01363478536 | 0.012792622241 | -0.000842163119 | -6.176577751422703730775854326 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 605103 | 638320 | 33217 | 5.48947865074210506310495899 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 1728566344.34144 | 1902889833.6419864 | 174323489.3005464 | 10.08485962203326662170217601 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 1703393814.6558163 | 1811891994.3556254 | 108498179.6998091 | 6.369529979873267530758121691 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-03-30T06:07:36Z:2026-04-13T06:07:36Z`: 15 points, sha256 `3c1350a9c79e44079e462750d9356b806980889c775a7dc450ae713e675904fe`
- `santiment:bitcoin:social_volume_total:2026-03-30T06:07:36Z:2026-04-13T06:07:36Z`: 15 points, sha256 `d0a25e02ce0cb1ae198f32cb80a23c9623157c587da4d5545afcf2c267ee7a48`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-30T06:07:36Z:2026-04-13T06:07:36Z`: 15 points, sha256 `b575b4108cf49b85c38299dada4acf489d1aa4bf0bc9f02b519c1ea161209d71`
- `santiment:bitcoin:daily_active_addresses:2026-03-30T06:07:36Z:2026-04-13T06:07:36Z`: 15 points, sha256 `9a5f452b2abe3ff48e8e2480003c091cb990dd70c91ced314453ba419112ef96`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-30T06:07:36Z:2026-04-13T06:07:36Z`: 15 points, sha256 `be6f7f98e507365d1b350560b9e6114e3e97bf86000386681e5afe20921c9c07`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-30T06:07:36Z:2026-04-13T06:07:36Z`: 15 points, sha256 `6cfef55dc001ab61f7ac391f95f35dddad286aa931f98cc7f83098babee15985`
