# Three-Channel V1 Channel Utility Report

Date: 2026-05-19
Status: customer_readable_candidate_internal_only

## Scope

This report compares three public Telegram channels using public-source text
evidence, reviewed extraction calibration, approved provider/proxy rules, and
deterministic historical outcome windows.

Channels:

- `bablos79`
- `nemphiscrypts`
- `pifagortrade`

This is not investment advice, not a trading recommendation, and not a promise of future performance.
It is a historical evidence-quality and signal-utility analysis.

## Gate Status

Decision: approve_internal_only.

This report is not approved for external/customer-facing delivery. It can be
used for internal product validation only until the external-ready gate is
rerun and explicitly approves delivery.

## Method Summary

| Step | What happened |
|---|---|
| Public source capture | Telegram public `/s/` pages only; no private or login-walled sources. |
| Claim extraction | V0 claims were reviewed and calibrated in V1. |
| Provider/proxy approval | Binance public daily klines and MOEX ISS daily candles are approved where mapped. |
| Outcome horizon | Primary `7d` directional return, with internal 1d/3d diagnostics. |
| Exclusions | False positives, context rows, unsupported proxies, unreviewed media, and missing setup links are not treated as wins or losses. |
| External boundary | This report remains internal until the external-ready gate approves delivery. |

## V1 Metric Summary

| Channel | V1 evaluable / V0 evaluable | 7d hit rate | Avg 7d directional return | Reviewed extraction exclusions | False-negative pass | Provider coverage |
|---|---:|---:|---:|---:|---:|---|
| `bablos79` | 14 / 19 | 64.285714% | 0.742848% | 5 | 0 reviewed rows | Binance crypto, MOEX ISS shares |
| `nemphiscrypts` | 49 / 53 | 57.142857% | 0.434858% | 4 | 1 extracted draft, 1 needs context | Binance crypto |
| `pifagortrade` | 107 / 112 | 52.336449% | -0.153127% | 6 | 2 extracted drafts, 1 needs context | Binance crypto |

## Confirmed Examples

| Channel | Source | Claim | 7d result | Notes |
|---|---|---|---:|---|
| `bablos79` | [10208](https://t.me/bablos79/10208) | short `PHOR` | 4.443290% | Kept after V1 review; MOEX ISS provider path. |
| `nemphiscrypts` | [3344](https://t.me/nemphiscrypts/3344) | long `BTC` | 0.486250% | Direct BTC long-zone wording; Binance provider path. |
| `pifagortrade` | [2643](https://t.me/pifagortrade/2643) | long `BTC` | 3.182273% | Kept in V1 recompute; Binance provider path. |

## Contradicted Examples

| Channel | Source | Claim | 7d result | Notes |
|---|---|---|---:|---|
| `bablos79` | [10250](https://t.me/bablos79/10250) | long `BTC` | -5.795072% | Direct buy wording, contradicted on the 7d window. |
| `nemphiscrypts` | [3376](https://t.me/nemphiscrypts/3376) | long `BTC` | -1.605656% | Similar BTC long-zone wording, contradicted on this window. |
| `pifagortrade` | [2647](https://t.me/pifagortrade/2647) | long `ETH` | -0.281887% | Kept in V1 recompute but contradicted over 7d. |

## What Changed From V0

| Channel | V0 evaluable | V1 evaluable | Delta | Main reason |
|---|---:|---:|---:|---|
| `bablos79` | 19 | 14 | -5 | Review removed false positives and context-dependent rows. |
| `nemphiscrypts` | 53 | 49 | -4 | Review removed management/context rows; false-negative pass found one extracted draft and one context row, neither added to customer-facing win/loss metrics. |
| `pifagortrade` | 112 | 107 | -5 | Review removed false positives and conditional setup/context rows; false-negative pass found two extracted drafts and one context row, none scoreable now. |

## Limitations

- V1 is still calibrated from a sampled extraction review, not full human review
  of every public row.
- Risk/reward rows are currently zero because extracted setup levels are not
  yet broadly available in the recomputed corpus.
- Futures, FX, US ETF/fund, commodity, and broad-index proxies still need
  explicit provider/proxy approval.
- Audio, OCR, and chart claims remain excluded from customer-facing metrics
  unless human/operator accepted.
- False-negative pass rows are not added to customer-facing win/loss metrics
  until their setup, context, provider, and linkage blockers are closed.
- The report must not be used as a leaderboard or future-profit claim.

## Conclusion

The current V1 artifacts are useful for internal product validation and for
showing how channel utility can be measured. They are not yet approved for
external paid delivery because the review coverage, provider expansion,
media posture, and external-ready gate are not sufficient.
