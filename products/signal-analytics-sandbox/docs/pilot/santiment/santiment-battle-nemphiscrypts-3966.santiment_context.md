# Santiment Context Artifact

Candidate: `santiment-battle-nemphiscrypts-3966`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-08T09:03:24Z`
Window: `2026-04-01T09:03:24Z` to `2026-04-15T09:03:24Z`
Artifact SHA-256: `9e4e40db2df6ea7b8b9424f2a15dae6907eaf60c5479d1afe590983186bfc294`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 71115.12256459738 | 71774.36734210879 | 659.24477751141 | 0.9270106747163170418681859944 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2676 | 2651 | -25 | -0.9342301943198804185351270553 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.036792538272 | -0.003569926682 | -0.040362464954 | -109.7028551159157166181611358 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 643069 | 612459 | -30610 | -4.759986875436383965017750817 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 2140193036.746782 | 1586904091.9583719 | -553288944.7884101 | -25.85229160587502442932976514 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 2131820426.1113918 | 1815157893.9944155 | -316662532.1169763 | -14.85409034637094997932772243 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-01T09:03:24Z:2026-04-15T09:03:24Z`: 15 points, sha256 `00ac4e9ac5426821faf1a4c4280856d8ff53be106f06efa8a8c25d72be70a26f`
- `santiment:bitcoin:social_volume_total:2026-04-01T09:03:24Z:2026-04-15T09:03:24Z`: 15 points, sha256 `91a6be14af042b9f3690afb0773227366c1c56c77e71d76a8f5c6aab18fd5409`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-01T09:03:24Z:2026-04-15T09:03:24Z`: 15 points, sha256 `bbc21cc76451483aac317b01dbd34af6972f93d09b255f86c8c392ab224b8ae9`
- `santiment:bitcoin:daily_active_addresses:2026-04-01T09:03:24Z:2026-04-15T09:03:24Z`: 15 points, sha256 `a14fc87d65517d916a649c053004948816822a1c6759978419593d1c8370d25c`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-01T09:03:24Z:2026-04-15T09:03:24Z`: 15 points, sha256 `d7075b06274d7fab3bbceda6cdbdcd28ace9a20d7c44616d559c2ad0931620c3`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-01T09:03:24Z:2026-04-15T09:03:24Z`: 15 points, sha256 `50e662e22a8f5cbd04a5e737616fd12fd3bcdc5426de789e0f6bd8d6e5c3520e`
