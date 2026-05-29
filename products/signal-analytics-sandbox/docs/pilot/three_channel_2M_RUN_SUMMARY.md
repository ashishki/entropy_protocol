# Three-Channel Two-Month Run Summary

Date: 2026-05-22
Window: `2026-03-22` through `2026-05-22` inclusive
Status: `internal_historical_research_not_external_ready`

## What Was Run

The run collected public Telegram `/s/` text rows for `bablos79`,
`nemphiscrypts`, and `pifagortrade`, normalized directional market claims, and
validated 7-day directional outcomes through open public market APIs:

- Binance public daily klines for supported crypto assets;
- MOEX ISS daily candles for supported Russian equities.

No private Telegram, login-walled, paywalled, or access-control bypass source
was used. No bulk market database was stored.

## Top-Line Result

| Channel | Text rows | Normalized claims | 7d evaluable | Confirmed / contradicted | Hit rate | Avg 7d directional return |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bablos79` | 340 | 21 | 17 | 10 / 7 | 58.823529% | 0.213022% |
| `nemphiscrypts` | 132 | 9 | 5 | 4 / 1 | 80.000000% | -0.148958% |
| `pifagortrade` | 54 | 7 | 6 | 5 / 1 | 83.333333% | 5.382339% |

Total: 526 text rows, 37 normalized claims, 28 7-day evaluable rows,
19 confirmed, 9 contradicted.

## Plain-Language Takeaways

- `bablos79` produced the largest two-month text sample and the largest number
  of evaluable rows, but the edge is modest: 10 confirmed vs 7 contradicted,
  with average 7-day directional return close to flat.
- `nemphiscrypts` has a high hit rate in this window, but only 5 evaluable rows.
  The average return is slightly negative, which means the one miss or sizing of
  moves matters more than the raw hit-rate headline.
- `pifagortrade` looks strongest in this narrow two-month strict sample:
  5 confirmed vs 1 contradicted and the highest average directional return.
  The sample is still small, so this is a promising lead, not a final ranking.

## Important Caveats

- Fresh posts near the end of the window may not have a full 7-day future
  window yet. These are marked `no_primary_horizon`, not counted as losses.
- This run uses simple direction-only 7-day validation. It does not yet compute
  real trade PnL, position sizing, stops, targets, RR, or liquidation behavior.
- Multi-asset posts can create more than one claim row.
- Unsupported assets, mixed direction, no direction, media-only rows, and
  non-market rows are exclusions, not author failures.
- Media, OCR, charts, and audio are still excluded unless source-linked and
  human/operator accepted.
- The result is internal research only, not investment advice, not a public
  dashboard, and not a paid deep report.

## Next Useful Step

Use this two-month window as the first repeatable baseline, then improve the
quality of the next run by adding:

- operator review for the 37 normalized claims;
- setup/RR parsing for stops, targets, entries, and management updates;
- confidence labels for small samples;
- media linkage only where public source linkage and acceptance exist;
- a rerun after late-window posts have full 7-day outcome coverage.
