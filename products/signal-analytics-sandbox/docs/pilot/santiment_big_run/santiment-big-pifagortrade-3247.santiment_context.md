# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3247`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-23T08:04:00Z`
Window: `2026-04-16T08:04:00Z` to `2026-04-30T08:04:00Z`
Artifact SHA-256: `e8124e6f7f1726896d4687420cf5df859c2be5a289a4c944df62e07e96f03199`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 78263.82377322465 | 77457.21406952443 | -806.60970370022 | -1.03062905032270418587135296 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2742 | 2419 | -323 | -11.77972283005105762217359592 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.004705431453 | 0.03280857402 | 0.028103142567 | 597.2490057013269171939629996 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 635450 | 664656 | 29206 | 4.596112990793925564560547643 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 2994923690.7513885 | 3636637752.3417134 | 641714061.5903249 | 21.42672494701616096340302659 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 3317525066.294625 | 3428091636.816366 | 110566570.521741 | 3.332802866964735378225629008 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-16T08:04:00Z:2026-04-30T08:04:00Z`: 15 points, sha256 `c57136853b9a630e8fca57f72edda2458be661c33f47991bfcb45e7a7d2ac516`
- `santiment:bitcoin:social_volume_total:2026-04-16T08:04:00Z:2026-04-30T08:04:00Z`: 15 points, sha256 `8946f770afb28c6fcfd29f7abe6db60c6cee7fb74e60d72f5bbe624067eefb3b`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-16T08:04:00Z:2026-04-30T08:04:00Z`: 15 points, sha256 `129680dace89b24c1f09ff36b3fd0b7c2bb8f3c5fc7caa12dca452a21d7ffd82`
- `santiment:bitcoin:daily_active_addresses:2026-04-16T08:04:00Z:2026-04-30T08:04:00Z`: 15 points, sha256 `af24d05223749b507eeae0217dff65998196cbf21e6a197c0b3a47555c940029`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-16T08:04:00Z:2026-04-30T08:04:00Z`: 15 points, sha256 `14438e6c8b1edcaab2a95a3c9c54ec2f39e51ff622bf93a6fd4d9d17451c370d`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-16T08:04:00Z:2026-04-30T08:04:00Z`: 15 points, sha256 `a99c357923174f33edeb0b177f2dd7f0d540dfcde3d5beaddd81e848da5ad79a`
