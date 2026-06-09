# Santiment Context Artifact

Candidate: `santiment-big-bablos79-10518`
Source: `bablos79`
Asset: `ETH` / `ethereum`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-07T05:30:30Z`
Window: `2026-04-30T05:30:30Z` to `2026-05-14T05:30:30Z`
Artifact SHA-256: `f8897ff88d87367b7fb7109d456d9734a9b3e7c46b90f9b1735360826d567aab`

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

- `santiment:ethereum:price_usd:2026-04-30T05:30:30Z:2026-05-14T05:30:30Z`: 15 points, sha256 `531dcbf9fdc5acedf4168921f684b247d8538cbd2bf6055c07a349c86d0c5a8b`
- `santiment:ethereum:social_volume_total:2026-04-30T05:30:30Z:2026-05-14T05:30:30Z`: 11 points, sha256 `ab2aeb00b6ce429e90090417330bdbe924432ecbd2b18a206c44e74bebf454d3`
- `santiment:ethereum:sentiment_weighted_total:2026-04-30T05:30:30Z:2026-05-14T05:30:30Z`: 11 points, sha256 `dbc8727fdeeb10cb028ce650f83b9d2134b40e0d362b92caa5d1c1360e0e75bf`
- `santiment:ethereum:daily_active_addresses:2026-04-30T05:30:30Z:2026-05-14T05:30:30Z`: 15 points, sha256 `69f0225329feaa97a6ef3b02095d7133175db4f711537613d1b56c2c74a61d54`
- `santiment:ethereum:exchange_inflow_usd:2026-04-30T05:30:30Z:2026-05-14T05:30:30Z`: 11 points, sha256 `796703eb91b3812dd827d1897b1d714d32555419fd934bc32614ec535e24c906`
- `santiment:ethereum:exchange_outflow_usd:2026-04-30T05:30:30Z:2026-05-14T05:30:30Z`: 11 points, sha256 `932cc5e4841d1aa95aea71926c6c8bb59cf70bf022baf81aa7008f952db94bbc`
