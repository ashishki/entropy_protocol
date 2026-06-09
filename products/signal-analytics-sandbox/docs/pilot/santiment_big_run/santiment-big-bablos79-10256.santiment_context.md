# Santiment Context Artifact

Candidate: `santiment-big-bablos79-10256`
Source: `bablos79`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-03-25T07:10:43Z`
Window: `2026-03-18T07:10:43Z` to `2026-04-01T07:10:43Z`
Artifact SHA-256: `446cf825b0cf0c57a2c9982edffe079f024845f9f8986c9d22f1f45dbb0804fc`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 71317.34939984394 | 68772.94064481847 | -2544.40875502547 | -3.567727595651553751780031543 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2443 | 2562 | 119 | 4.871060171919770773638968481 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.065454059744 | -0.000598580724 | -0.066052640468 | -100.9145051144896635794533429 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 655913 | 623444 | -32469 | -4.950199188002067347346370631 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 1960881675.1601155 | 2102698423.3110065 | 141816748.150891 | 7.232295040918824162796953064 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 2448533257.4643106 | 2222765694.3114614 | -225767563.1528492 | -9.22052263184911831666926661 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-03-18T07:10:43Z:2026-04-01T07:10:43Z`: 15 points, sha256 `3a317dd22e291c0c020f3272d23fc47ed259a234c0fe2368b37679b8cff0804b`
- `santiment:bitcoin:social_volume_total:2026-03-18T07:10:43Z:2026-04-01T07:10:43Z`: 15 points, sha256 `8b00d2aacb5fe774923bb3aa0c9cf78ca5482e06bbee328cefa348b10eb96c81`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-18T07:10:43Z:2026-04-01T07:10:43Z`: 15 points, sha256 `8de5cf61bcde7c91afc81be08068697587d7243ee0ba79e0c628a8e66b229a28`
- `santiment:bitcoin:daily_active_addresses:2026-03-18T07:10:43Z:2026-04-01T07:10:43Z`: 15 points, sha256 `ebfb63f57ba6e0a1ddb97105351c6a41060724f195b696208eacd8e1f378765f`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-18T07:10:43Z:2026-04-01T07:10:43Z`: 15 points, sha256 `ba660ffe2f9270e18080833beef22b5709b02c7aa97877c1dab46c164da59278`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-18T07:10:43Z:2026-04-01T07:10:43Z`: 15 points, sha256 `c853423a4f069f12ae7006fd448fd67fd2badb45bacb7f767a7dd0bcf2dc7474`
