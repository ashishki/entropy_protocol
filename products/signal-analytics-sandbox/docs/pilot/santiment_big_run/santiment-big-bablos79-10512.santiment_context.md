# Santiment Context Artifact

Candidate: `santiment-big-bablos79-10512`
Source: `bablos79`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-06T11:00:51Z`
Window: `2026-04-29T11:00:51Z` to `2026-05-13T11:00:51Z`
Artifact SHA-256: `84ded94327926150574036820c99f158dcc48edfc74f7358d742f742c065db3e`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 81427.30524697408 | 80015.26666972411 | -1412.03857724997 | -1.734109427994908088897591908 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 3919 | 3551 | -368 | -9.390150548609339117121714723 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | -0.009827838576 | 0.082360102991 | 0.092187941567 | -938.0286504921527315081940353 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 723375 | 757083 | 33708 | 4.659823742871954380508035251 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 3014227267.1142106 | 2629835921.9060254 | -384391345.2081852 | -12.75256678227177675393800059 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 2831647607.175005 | 2832483253.375351 | 835646.200346 | 0.02951095320719243566312002883 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-29T11:00:51Z:2026-05-13T11:00:51Z`: 15 points, sha256 `6fd88d39aa0786ded75cf31881f6d80588aed1a5b165696634696a8826d22ad3`
- `santiment:bitcoin:social_volume_total:2026-04-29T11:00:51Z:2026-05-13T11:00:51Z`: 12 points, sha256 `f0aa2342a69378e61a4fae1f73336f449c8d25541424db05fb50c427bfe9693d`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-29T11:00:51Z:2026-05-13T11:00:51Z`: 12 points, sha256 `94869b1c6d2dfe56a9d04c650689061b70e525f03897fd6b7566c9a606aa0407`
- `santiment:bitcoin:daily_active_addresses:2026-04-29T11:00:51Z:2026-05-13T11:00:51Z`: 15 points, sha256 `782e2f9a96860af4bc21c5923a89ffb7ee4437c286c0b6c755f9c87fa75eee45`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-29T11:00:51Z:2026-05-13T11:00:51Z`: 12 points, sha256 `0e67b915c464021fc5d19828185dab7d6f641565e75ba4fd76b6a38da75290cf`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-29T11:00:51Z:2026-05-13T11:00:51Z`: 12 points, sha256 `07f59e0a57a895f5f61a1169dff53fcc62c2616bc9f546a9fd2c36907c394058`
