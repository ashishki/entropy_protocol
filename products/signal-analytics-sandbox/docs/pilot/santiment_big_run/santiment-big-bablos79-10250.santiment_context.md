# Santiment Context Artifact

Candidate: `santiment-big-bablos79-10250`
Source: `bablos79`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-03-23T21:14:05Z`
Window: `2026-03-16T21:14:05Z` to `2026-03-30T21:14:05Z`
Artifact SHA-256: `964dd8054bbc6eea9810e8e3d411a2c685861ec2be80675adb581015d88efb48`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 70919.92395192248 | 70531.62374150514 | -388.30021041734 | -0.5475192143191998623238177436 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2527 | 2544 | 17 | 0.6727344677483181638306292046 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.067900552135 | 0.007247119254 | -0.060653432881 | -89.32686255688869149134496946 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 627789 | 595164 | -32625 | -5.196809756144182201344719324 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 1537094786.1630068 | 2433962870.4829655 | 896868084.3199587 | 58.34826143407704371594146449 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 1738644648.6523015 | 2326859331.5201583 | 588214682.8678568 | 33.8317943993792742895173254 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-03-16T21:14:05Z:2026-03-30T21:14:05Z`: 15 points, sha256 `4c43e9ea1819db51e6a2889af68cc1c8665a86f0418a76d10c45441c35a17693`
- `santiment:bitcoin:social_volume_total:2026-03-16T21:14:05Z:2026-03-30T21:14:05Z`: 15 points, sha256 `43d631683e6e75a38df01e55c7e635c810daf6fceb2f9a8880c907ddc752c541`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-16T21:14:05Z:2026-03-30T21:14:05Z`: 15 points, sha256 `71569d81303b993ccde9ed48f227b2e535c77174f5ec3d93a2ad7b49d6f7ba81`
- `santiment:bitcoin:daily_active_addresses:2026-03-16T21:14:05Z:2026-03-30T21:14:05Z`: 15 points, sha256 `8da4e8c43e0b9de4a2e62e4f0eecc45752480b5b362fd00fa9d04a62d5b09186`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-16T21:14:05Z:2026-03-30T21:14:05Z`: 15 points, sha256 `a6fec9c7755b24211f6b8b94b285240bda0a98be7c7801fea5d1ce4e3b05b505`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-16T21:14:05Z:2026-03-30T21:14:05Z`: 15 points, sha256 `00c158b34e4d734f6fe338a73c531d414c05713c8638299b06888c5241d7f568`
