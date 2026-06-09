# Santiment Big Run

Date: 2026-06-09
Status: completed live provider run

## Method

- Source: `docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json`.
- Scope: all rows with a supported crypto asset: BTC, ETH, SOL, TON, AVAX, ARB, SUI, DOT.
- Multi-asset rows use the first supported crypto asset as the Santiment slug target.
- Directional score counts only `long` and `short` rows. `mixed` and `unknown` rows are context-only.
- Favorable means price rose after a long post or fell after a short post.
- Guardrail: Santiment context is retrospective enrichment only and does not change auto-validation decisions.

## Channel Ranking

| rank | channel | candidates | directional | favorable | favorable rate | partial metric rows | avg price context | confidence |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | pifagortrade | 17 | 8 | 6 | 75.00 | 2 | 0.20 | high |
| 2 | nemphiscrypts | 18 | 10 | 5 | 50.00 | 7 | -0.15 | medium |
| 3 | bablos79 | 6 | 1 | 0 | 0.00 | 0 | 0.06 | medium |

## Interpretation

- `pifagortrade` ranks first on directional Santiment alignment: 6/8 directional rows were favorable.
- `mixed` and `unknown` rows remain useful for narrative/context analysis, but they are not scored as wins or losses.
- Partial metric rows are retained with blockers instead of being dropped, so coverage gaps are visible.

## Row Details

| candidate | channel | asset | direction | price % | social % | sentiment % | favorable | blockers |
|---|---|---:|---|---:|---:|---:|---|---|
| santiment-big-bablos79-10250 | bablos79 | BTC | long | -0.55 | 0.67 | -89.33 | false | none |
| santiment-big-bablos79-10256 | bablos79 | BTC | mixed | -3.57 | 4.87 | -100.91 |  | none |
| santiment-big-bablos79-10328 | bablos79 | TON | unknown | 4.83 | -17.57 | -1041.39 |  | none |
| santiment-big-bablos79-10512 | bablos79 | BTC | mixed | -1.73 | -9.39 | -938.03 |  | none |
| santiment-big-bablos79-10518 | bablos79 | ETH | unknown | 0.70 | 3.32 | -302.47 |  | none |
| santiment-big-bablos79-10520 | bablos79 | ETH | unknown | 0.70 | 3.32 | -302.47 |  | none |
| santiment-big-nemphiscrypts-3962 | nemphiscrypts | BTC | mixed | -1.11 | 25.40 | 187.61 |  | none |
| santiment-big-nemphiscrypts-3964 | nemphiscrypts | SUI | unknown | -4.80 | 47.06 | -113.62 |  | missing_santiment_points:daily_active_addresses; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-nemphiscrypts-3966 | nemphiscrypts | BTC | long | 0.93 | -0.93 | -109.70 | true | none |
| santiment-big-nemphiscrypts-3976 | nemphiscrypts | BTC | mixed | 2.61 | 7.58 | -88.17 |  | none |
| santiment-big-nemphiscrypts-3977 | nemphiscrypts | ETH | short | 3.08 | -2.32 | -128.74 | false | none |
| santiment-big-nemphiscrypts-3978 | nemphiscrypts | BTC | long | -1.80 | -14.16 | -193.52 | false | none |
| santiment-big-nemphiscrypts-3996 | nemphiscrypts | SUI | long | 0.01 | -8.70 |  | true | missing_santiment_points:daily_active_addresses; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-nemphiscrypts-4018 | nemphiscrypts | ETH | long | 1.69 | 26.37 | 5684.73 | true | none |
| santiment-big-nemphiscrypts-4023 | nemphiscrypts | ETH | unknown | 0.92 | -17.38 | -181.52 |  | none |
| santiment-big-nemphiscrypts-4024 | nemphiscrypts | ETH | long | 0.92 | -17.38 | -181.52 | true | none |
| santiment-big-nemphiscrypts-4043 | nemphiscrypts | BTC | long | 1.39 | 22.85 | -93.61 | true | none |
| santiment-big-nemphiscrypts-4044 | nemphiscrypts | BTC | unknown | 1.39 | 22.85 | -93.61 |  | none |
| santiment-big-nemphiscrypts-4061 | nemphiscrypts | BTC | long | -1.73 | -9.39 | -938.03 | false | none |
| santiment-big-nemphiscrypts-4091 | nemphiscrypts | BTC | long | -0.65 |  |  | false | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-nemphiscrypts-4094 | nemphiscrypts | ETH | unknown | 0.19 |  |  |  | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-nemphiscrypts-4096 | nemphiscrypts | ETH | short | 0.19 |  |  | false | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:daily_active_addresses; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-nemphiscrypts-4114 | nemphiscrypts | SOL | unknown | -3.28 |  |  |  | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-nemphiscrypts-4117 | nemphiscrypts | BTC | mixed | -2.66 |  |  |  | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-pifagortrade-3213 | pifagortrade | BTC | mixed | -0.01 | -27.34 | -284.99 |  | none |
| santiment-big-pifagortrade-3214 | pifagortrade | BTC | short | -0.52 | -2.43 | -180.09 | true | none |
| santiment-big-pifagortrade-3222 | pifagortrade | BTC | mixed | 4.38 | -4.52 | -6.18 |  | none |
| santiment-big-pifagortrade-3224 | pifagortrade | BTC | mixed | -1.11 | 25.40 | 187.61 |  | none |
| santiment-big-pifagortrade-3233 | pifagortrade | BTC | mixed | 5.34 | 28.42 | -103.25 |  | none |
| santiment-big-pifagortrade-3234 | pifagortrade | BTC | long | 0.85 | -7.32 | -158.28 | true | none |
| santiment-big-pifagortrade-3245 | pifagortrade | BTC | mixed | -2.49 | -9.66 | -885.85 |  | none |
| santiment-big-pifagortrade-3247 | pifagortrade | BTC | mixed | -1.03 | -11.78 | 597.25 |  | none |
| santiment-big-pifagortrade-3248 | pifagortrade | BTC | long | -1.64 | 64.48 | -285.42 | false | none |
| santiment-big-pifagortrade-3255 | pifagortrade | BTC | short | -0.14 | -14.02 | 333.33 | true | none |
| santiment-big-pifagortrade-3259 | pifagortrade | BTC | short | 0.61 | -4.72 | 806.57 | false | none |
| santiment-big-pifagortrade-3263 | pifagortrade | ETH | mixed | 0.70 | 3.32 | -302.47 |  | none |
| santiment-big-pifagortrade-3265 | pifagortrade | BTC | unknown | -0.49 |  |  |  | none |
| santiment-big-pifagortrade-3267 | pifagortrade | BTC | short | -0.49 |  |  | true | none |
| santiment-big-pifagortrade-3273 | pifagortrade | BTC | short | -1.18 |  |  | true | none |
| santiment-big-pifagortrade-3277 | pifagortrade | BTC | mixed | -0.26 |  |  |  | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
| santiment-big-pifagortrade-3280 | pifagortrade | BTC | long | 0.94 |  |  | true | missing_santiment_points:social_volume_total; missing_santiment_points:sentiment_weighted_total; missing_santiment_points:exchange_inflow_usd; missing_santiment_points:exchange_outflow_usd |
