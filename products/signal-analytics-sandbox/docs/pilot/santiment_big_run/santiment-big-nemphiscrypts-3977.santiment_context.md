# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-3977`
Source: `nemphiscrypts`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-16T17:01:29Z`
Window: `2026-04-09T17:01:29Z` to `2026-04-23T17:01:29Z`
Artifact SHA-256: `9a6f80ff93604f5fe36d4d0675be7f5443fc332d704d02591c4a7241ab54d189`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 2348.85507648327 | 2421.102411475347 | 72.247334992077 | 3.075853240815795824906376792 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 517 | 505 | -12 | -2.321083172147001934235976789 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.055337542545 | -0.015901644123 | -0.071239186668 | -128.735725136454918807779161 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 597638 | 603718 | 6080 | 1.017338254930242052881510212 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 588147975.2769407 | 533241219.1038195 | -54906756.1731212 | -9.335534335090978739433506992 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 635456985.0365115 | 657775667.8394047 | 22318682.8028932 | 3.512225583862428352400291811 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:ethereum:price_usd:2026-04-09T17:01:29Z:2026-04-23T17:01:29Z`: 15 points, sha256 `d359b6d038e0e503184a3e5a6e12a57561b2608adf91a0b5a26a54d976850d6d`
- `santiment:ethereum:social_volume_total:2026-04-09T17:01:29Z:2026-04-23T17:01:29Z`: 15 points, sha256 `b4dc62d95a2010022150d47c107070b8ea933f952ead04f5c7508d3da2de8aec`
- `santiment:ethereum:sentiment_weighted_total:2026-04-09T17:01:29Z:2026-04-23T17:01:29Z`: 15 points, sha256 `e62cb9d8d1258004736143688535146c9c0cd79527a7ebe6c064e406f4971856`
- `santiment:ethereum:daily_active_addresses:2026-04-09T17:01:29Z:2026-04-23T17:01:29Z`: 15 points, sha256 `d3aaf5b792f9d09caee71431fdc8e741726d9e805421c6c2d74042e2da448843`
- `santiment:ethereum:exchange_inflow_usd:2026-04-09T17:01:29Z:2026-04-23T17:01:29Z`: 15 points, sha256 `f69f0573373e4e4d66c999778855fe8d0e18d90dbfa09ce00508e8933b65f51b`
- `santiment:ethereum:exchange_outflow_usd:2026-04-09T17:01:29Z:2026-04-23T17:01:29Z`: 15 points, sha256 `752860feb2c161438bb08085bf899b9b13763335dcfba16758822ad515e21a3a`
