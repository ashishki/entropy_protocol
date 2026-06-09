# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4061`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-06T09:11:25Z`
Window: `2026-04-29T09:11:25Z` to `2026-05-13T09:11:25Z`
Artifact SHA-256: `ae00f3d182ac4fb2bba5ac8b765a9139ddfb865ab09b3a92d038d6f1df97c476`

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

- `santiment:bitcoin:price_usd:2026-04-29T09:11:25Z:2026-05-13T09:11:25Z`: 15 points, sha256 `875eab48db9593d572d69f15f7f0ff1d3b5bcfcf33bc9f64e5ab2270275506a0`
- `santiment:bitcoin:social_volume_total:2026-04-29T09:11:25Z:2026-05-13T09:11:25Z`: 12 points, sha256 `6c3fbe85e127743713e78c568ff8ae481d2f18be121636fe461f73b1cb889798`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-29T09:11:25Z:2026-05-13T09:11:25Z`: 12 points, sha256 `ca52c83d4c86c4a5955b6d5042f96c5f0aa01897e736467a0f3c302be24112b9`
- `santiment:bitcoin:daily_active_addresses:2026-04-29T09:11:25Z:2026-05-13T09:11:25Z`: 15 points, sha256 `55acc63b36fb79d69d31720b4e016826e20aeb8de90e764f45f85dcf0e44c2b6`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-29T09:11:25Z:2026-05-13T09:11:25Z`: 12 points, sha256 `83c8f2514f04de256956462034ddea1562aeb0755233198b597f0b192990e8de`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-29T09:11:25Z:2026-05-13T09:11:25Z`: 12 points, sha256 `30e2b8e9a39f2b3b2d8df9d9f9eb720946f362b8973c39ef1df5e9821fde5b9e`
