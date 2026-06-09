# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3233`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-04-12T14:16:52Z`
Window: `2026-04-05T14:16:52Z` to `2026-04-19T14:16:52Z`
Artifact SHA-256: `b38cc2df61b0d7bb821c97b3564a65e0dc7c34fab8ee35f0fca0660ce50eeb67`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 70757.61922350423 | 74532.7393449206 | 3775.12012141637 | 5.335284260330727063663084852 | up_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 1770 | 2273 | 503 | 28.41807909604519774011299435 | up_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | 0.014982939987 | -0.000486959715 | -0.015469899702 | -103.2500945436777581080756417 | down_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 522286 | 624198 | 101912 | 19.51268079175011392225715413 | up_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 634963387.8968811 | 2121462546.9693403 | 1486499159.0724592 | 234.107853682087988911036022 | up_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 673334638.421383 | 2595489801.472723 | 1922155163.05134 | 285.4680352636821022958926475 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-04-05T14:16:52Z:2026-04-19T14:16:52Z`: 15 points, sha256 `611f3af633b7426c6c92656c7fad774c2ce9d5341d8c66630ddac120025e55d9`
- `santiment:bitcoin:social_volume_total:2026-04-05T14:16:52Z:2026-04-19T14:16:52Z`: 15 points, sha256 `d228c0fe489703ce84bb0c20e8f2de33b3d96a5d1ef7965580d604ba39db329e`
- `santiment:bitcoin:sentiment_weighted_total:2026-04-05T14:16:52Z:2026-04-19T14:16:52Z`: 15 points, sha256 `cd65f0361731b34aa7a81ed7ed8f93a0e93464269dfd2ffbfcd780d72114f178`
- `santiment:bitcoin:daily_active_addresses:2026-04-05T14:16:52Z:2026-04-19T14:16:52Z`: 15 points, sha256 `cf0d9c327c6577c44222a499fa3a8db0bc6b957234cb5eb384ee45df8f049d08`
- `santiment:bitcoin:exchange_inflow_usd:2026-04-05T14:16:52Z:2026-04-19T14:16:52Z`: 15 points, sha256 `34c76a0316fe0917be15df8b20080bcedcb0979d355aef2eec4a0274a1865db2`
- `santiment:bitcoin:exchange_outflow_usd:2026-04-05T14:16:52Z:2026-04-19T14:16:52Z`: 15 points, sha256 `6730c35d3e9c63807ded6dac8eb0b651f91a82ae2aa6840e85a7f28091a4e1be`
