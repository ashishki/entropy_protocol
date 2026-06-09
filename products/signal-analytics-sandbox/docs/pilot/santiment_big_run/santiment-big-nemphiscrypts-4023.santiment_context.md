# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4023`
Source: `nemphiscrypts`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-01T12:14:55Z`
Window: `2026-04-24T12:14:55Z` to `2026-05-08T12:14:55Z`
Artifact SHA-256: `cf9771fbf675b0d12f9ac18d7cd90a7ef03d12e313c8f0493752efa28e9d07a2`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 2294.990847883549 | 2316.095195313837 | 21.104347430288 | 0.9195830758867960282036354701 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 1404 | 1160 | -244 | -17.37891737891737891737891738 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.038549083144 | -0.031423629741 | -0.069972712885 | -181.515893967223844694821051 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 598311 | 439971 | -158340 | -26.46449756063318240847987084 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 495547135.22804654 | 156022096.28718546 | -339525038.94086108 | -68.51518549988480310615275831 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 485532339.52336717 | 141300240.4309037 | -344232099.09246347 | -70.89787251460654632730774332 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:ethereum:price_usd:2026-04-24T12:14:55Z:2026-05-08T12:14:55Z`: 15 points, sha256 `727d8866fea4a40ed95313a20032c0fc9ad74a92a4bc4ad2cd89b50e62e59779`
- `santiment:ethereum:social_volume_total:2026-04-24T12:14:55Z:2026-05-08T12:14:55Z`: 15 points, sha256 `d405710312429aac608987fe75c68a9fcf493fb5d6f28063174967e43bccc432`
- `santiment:ethereum:sentiment_weighted_total:2026-04-24T12:14:55Z:2026-05-08T12:14:55Z`: 15 points, sha256 `cb0f8099d0629f6b880619a0edd1496e63a887b36cb124bed1a6e51615f005d4`
- `santiment:ethereum:daily_active_addresses:2026-04-24T12:14:55Z:2026-05-08T12:14:55Z`: 15 points, sha256 `bd057e5ffdb69db5f7355e1bf358c424aa14f2a465b74c4d0f3c480aa23e5e33`
- `santiment:ethereum:exchange_inflow_usd:2026-04-24T12:14:55Z:2026-05-08T12:14:55Z`: 15 points, sha256 `b62e1a8a1daf57c17816590b88097aa81babdd358ce7c5b4d1eb33f0d4bcdbf4`
- `santiment:ethereum:exchange_outflow_usd:2026-04-24T12:14:55Z:2026-05-08T12:14:55Z`: 15 points, sha256 `d0c4a1d974fac43252908f5c5ba828c503854abcf6671349767d36567f77f7e7`
