# Santiment Context Artifact

Candidate: `santiment-big-pifagortrade-3214`
Source: `pifagortrade`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-03-28T06:32:09Z`
Window: `2026-03-21T06:32:09Z` to `2026-04-04T06:32:09Z`
Artifact SHA-256: `8dcfc703256b58b30ec09016c21301cbd67d1ee85f52b8006bf29de2edd173b7`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 66319.6918007053 | 65973.13043144201 | -346.56136926329 | -0.5225617910057965192293552202 | down_price_context_after_post |
| social_volume_total:post_vs_pre | social_volume_total | 2057 | 2007 | -50 | -2.430724355858045697617890131 | down_social_context_after_post |
| sentiment_weighted_total:post_vs_pre | sentiment_weighted_total | -0.027560956843 | 0.02207337691 | 0.049634333753 | -180.0892981899728596443780586 | up_social_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 558679 | 497125 | -61554 | -11.01777586055677768450219178 | down_metric_context_after_post |
| exchange_inflow_usd:post_vs_pre | exchange_inflow_usd | 942504086.3530341 | 853913171.9040399 | -88590914.4489942 | -9.399525766704280240674462667 | down_exchange_flow_context_after_post |
| exchange_outflow_usd:post_vs_pre | exchange_outflow_usd | 880865023.8985589 | 899047346.8345118 | 18182322.9359529 | 2.064144045075263474748753686 | up_exchange_flow_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-03-21T06:32:09Z:2026-04-04T06:32:09Z`: 15 points, sha256 `dfb3574e2bc4bb910a89ad72f009fc3912f6a5b93b6d20a5c67542053c90a6f6`
- `santiment:bitcoin:social_volume_total:2026-03-21T06:32:09Z:2026-04-04T06:32:09Z`: 15 points, sha256 `3cf8d699bb22d7fcf01dedbbeaf343f7538300a1111bf7c0d6580efbcb4a4339`
- `santiment:bitcoin:sentiment_weighted_total:2026-03-21T06:32:09Z:2026-04-04T06:32:09Z`: 15 points, sha256 `7484adca50aa660b0620242a5a447963248db48e99fca60632f1a06915e29497`
- `santiment:bitcoin:daily_active_addresses:2026-03-21T06:32:09Z:2026-04-04T06:32:09Z`: 15 points, sha256 `0835a0d20fb67b1e8c0d2849d356179c4456a5e9458fd7f4770401f031fbce27`
- `santiment:bitcoin:exchange_inflow_usd:2026-03-21T06:32:09Z:2026-04-04T06:32:09Z`: 15 points, sha256 `bf4ac58a687ba34a248aba7aa845b4c505032814539d4abce62667c887c0583a`
- `santiment:bitcoin:exchange_outflow_usd:2026-03-21T06:32:09Z:2026-04-04T06:32:09Z`: 15 points, sha256 `6d5d0a4646f11751324afb0e9dcfaa200cec41f349a22a996ce5603df862e0f7`
