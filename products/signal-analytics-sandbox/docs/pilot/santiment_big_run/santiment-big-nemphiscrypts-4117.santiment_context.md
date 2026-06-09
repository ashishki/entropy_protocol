# Santiment Context Artifact

Candidate: `santiment-big-nemphiscrypts-4117`
Source: `nemphiscrypts`
Asset: `BTC` / `bitcoin`
Provider: `santiment_sanapi`
Post timestamp: `2026-05-21T11:26:26Z`
Window: `2026-05-14T11:26:26Z` to `2026-05-28T11:26:26Z`
Artifact SHA-256: `a65594c76e842d21f175959b53844dd1b40f0d5b466602f25e1f87dfd2485f38`

## Features

| feature | metric | pre | post | delta | pct_change | interpretation |
|---|---:|---:|---:|---:|---:|---|
| price_usd:post_vs_pre | price_usd | 77538.11352004793 | 75479.21522489628 | -2058.89829515165 | -2.655337100275608171551292987 | down_price_context_after_post |
| daily_active_addresses:post_vs_pre | daily_active_addresses | 639627 | 680032 | 40405 | 6.316962854913879495393408971 | up_metric_context_after_post |

## Metric Refs

- `santiment:bitcoin:price_usd:2026-05-14T11:26:26Z:2026-05-28T11:26:26Z`: 15 points, sha256 `03ab8117c0821f84bacbdeb2197ba41ae317224118a73b4befd7ded9cf9aacab`
- `santiment:bitcoin:social_volume_total:2026-05-14T11:26:26Z:2026-05-28T11:26:26Z`: 0 points, sha256 `2f2f1a508f7338acc8ecfdd4acf4c258a8becf1d48b3a5fefaacb2d977cc9458`
- `santiment:bitcoin:sentiment_weighted_total:2026-05-14T11:26:26Z:2026-05-28T11:26:26Z`: 0 points, sha256 `af64d7f393eb8ea7bd5c4e1a00f93558190c27f41145d7aba15cb595603802b2`
- `santiment:bitcoin:daily_active_addresses:2026-05-14T11:26:26Z:2026-05-28T11:26:26Z`: 15 points, sha256 `236b94376c6ce35c6eabbb415da11cf6d46433399cc6317823b8dba6a20577c7`
- `santiment:bitcoin:exchange_inflow_usd:2026-05-14T11:26:26Z:2026-05-28T11:26:26Z`: 0 points, sha256 `21f9e568b209fc65cf3e13fddbf8aa183b4aa864b935acaf7f2bba61ed58e8f6`
- `santiment:bitcoin:exchange_outflow_usd:2026-05-14T11:26:26Z:2026-05-28T11:26:26Z`: 0 points, sha256 `4e8cdc84d8b077cbd60ea2dcb116eb3766a2c4bddc7db37da40f89ca3b5fefef`

## Blockers

- `missing_santiment_points:social_volume_total`
- `missing_santiment_points:sentiment_weighted_total`
- `missing_santiment_points:exchange_inflow_usd`
- `missing_santiment_points:exchange_outflow_usd`
