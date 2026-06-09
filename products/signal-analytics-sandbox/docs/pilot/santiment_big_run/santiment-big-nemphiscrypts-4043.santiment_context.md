# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4043`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-04T05:01:44Z`
Window: `2026-04-27T05:01:44Z` to `2026-05-11T05:01:44Z`
Artifact SHA-256: `d5e61944131cd52c4e24540bfccfa0386a716f4e2e8534af320ad832f327a8df`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 79823.52756678614 | 80930.73814844475 | 1107.21058165861 | 1.387072978868589211909550844 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 3348 | 4113 | 765 | 22.84946236559139784946236559 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | -0.016957420835 | -0.001084067165 | 0.01587335367 | -93.60712235930069727493438126 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 708443 | 738000 | 29557 | 4.172107000845516153028542875 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 3665376115.734984 | 3218316164.304626 | -447059951.430358 | -12.19683703157194822588817006 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 3716671894.12564 | 3177978216.0775104 | -538693678.0481296 | -14.49397992057243898397755063 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-27T05:01:44Z:2026-05-11T05:01:44Z`: 15 points, sha256 `b2518e028ff9e316ed532ca47a66fa7f957d433e57d60c5d36569af1ce48ca03`
- `santiment:bitcoin:social_volume_total:2026-04-27T05:01:44Z:2026-05-11T05:01:44Z`: 14 points, sha256 `d0edbd2b1d648a4c4beb220887641e948e67cd6d32437ba4a2fa80c62f4ecac6`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-27T05:01:44Z:2026-05-11T05:01:44Z`: 14 points, sha256 `55d1199cb282fe2cd4de4dd432bea3c57f7fcdafda848c439215889d91883d9c`
- `santiment:bitcoin:daily_active_addresses:2026-04-27T05:01:44Z:2026-05-11T05:01:44Z`: 15 points, sha256 `3a90ce5bd1559dfd50bb8a27efdeb10f4f99baf28891ce8ea0f09c47fc336adb`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-27T05:01:44Z:2026-05-11T05:01:44Z`: 14 points, sha256 `9a25e33fc730d510dc022974f3c4636b8053c28fcb34bf04830a3a078b2dde2c`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-27T05:01:44Z:2026-05-11T05:01:44Z`: 14 points, sha256 `128c9358697cdebfd5a0bc52ba6d2e8dee9cac5e195869d36c1448ddd99696bf`
