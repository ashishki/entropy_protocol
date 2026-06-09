# Santiment Context Artifact

Candidate: `santiment-battle-pifagortrade-3263`
Source: `pifagortrade`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-07T10:24:49Z`
Window: `2026-04-30T10:24:49Z` to `2026-05-14T10:24:49Z`
Artifact SHA-256: `94a5df884963d764b6a05b1073ea308747267d24382033a0c7b1388c3f5a2f11`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 2290.977956574309 | 2307.014137329791 | 16.036180755482 | 0.6999709756902612331038517254 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 1084 | 1120 | 36 | 3.321033210332103321033210332 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.012534467493 | -0.025379022463 | -0.037913489956 | -302.4738783452362175271229929 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 691710 | 547625 | -144085 | -20.83026123664541498604906681 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 663974102.8306204 | 799162345.8016883 | 135188242.9710679 | 20.36046924040264584799883979 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 550498087.9034127 | 546299492.8720958 | -4198595.0313169 | -0.7626902115695562384440692177 | down_exchange_flow_context_after_post |

## Metric Refs

- `santiment:ethereum:price_usd:2026-04-30T10:24:49Z:2026-05-14T10:24:49Z`: 15 points, sha256 `909f8ce39861d83d74c0c5f6e9a739a6f0caef1289f76f59bf7deb5e1ea175f3`
- `santiment:ethereum:social_volume_total:2026-04-30T10:24:49Z:2026-05-14T10:24:49Z`: 11 points, sha256 `8b8b257308512a52091c77ea604b917391b0eb797afd223d07539a462456e79d`
- `santiment:ethereum:sentiment_weighted_total:2026-04-30T10:24:49Z:2026-05-14T10:24:49Z`: 11 points, sha256 `498cf882aa602c06355e38be5fa636876fd1ad64f26b9b7afa79d096d037dbf2`
- `santiment:ethereum:daily_active_addresses:2026-04-30T10:24:49Z:2026-05-14T10:24:49Z`: 15 points, sha256 `d051ea0154047c84571b923c89b41c5931931c86a2d0671b44af3c18094af0d5`
- `santiment:ethereum:exchange_inflow_usd:2026-04-30T10:24:49Z:2026-05-14T10:24:49Z`: 11 points, sha256 `5d18eadee3ab8786448d6ba6110f050f91b75c395bb7e08b82b3669ff84f6631`
- `santiment:ethereum:exchange_outflow_usd:2026-04-30T10:24:49Z:2026-05-14T10:24:49Z`: 11 points, sha256 `4906f2a88ee0c55d9fd971d7977f3c2875e6b7982f4414de6d7ac3f1208dbea7`
