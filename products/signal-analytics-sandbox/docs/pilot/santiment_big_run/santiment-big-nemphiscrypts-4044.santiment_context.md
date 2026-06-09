# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4044`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-04T06:13:53Z`
Window: `2026-04-27T06:13:53Z` to `2026-05-11T06:13:53Z`
Artifact SHA-256: `3b7da89e48b529ed93f4c032c456bac74b8e340d1fa9788748d4b9ecdbb8ed3d`

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

- `santiment:bitcoin:price_usd:2026-04-27T06:13:53Z:2026-05-11T06:13:53Z`: 15 points, sha256 `c9f5bf33bfe894d6fc69098b8d3e14faa25fc57549ec07a0d846afcbb59b5cdd`
- `santiment:bitcoin:social_volume_total:2026-04-27T06:13:53Z:2026-05-11T06:13:53Z`: 14 points, sha256 `fca9becd4c5a123c7b2bc7b16892e841e7ce1d080f41f768046c0db583d87417`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-27T06:13:53Z:2026-05-11T06:13:53Z`: 14 points, sha256 `1e998207977ef2e5574d4579c1897e87a6d71dfab213a98bd4cad3ce6a6fa474`
- `santiment:bitcoin:daily_active_addresses:2026-04-27T06:13:53Z:2026-05-11T06:13:53Z`: 15 points, sha256 `1b4203d507384218739fffe0a1fd4aa888cb080e55ab2cc8c493791d5b4b2b55`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-27T06:13:53Z:2026-05-11T06:13:53Z`: 14 points, sha256 `3e9d4fd244feb4b767a5ea67f41e8ec07fab9cab60dc9e920875186d09b2fd78`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-27T06:13:53Z:2026-05-11T06:13:53Z`: 14 points, sha256 `e588036073bf11080955c6a9b76885dbbb6fa733d6a3c9158b77512424f0b921`
