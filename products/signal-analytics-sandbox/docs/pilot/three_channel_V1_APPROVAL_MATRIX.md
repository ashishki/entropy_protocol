# Three-Channel V1 Approval Matrix

Date: 2026-05-19
Status: internal_v1_approved_for_calibration

## Scope

This matrix completes `SAS-V1-001`. It converts the V0 metric run and the
`bablos79` proxy/horizon approval record into explicit V1 permissions for the
three pilot channels:

- `bablos79`
- `nemphiscrypts`
- `pifagortrade`

The matrix is an internal research control. V0 numbers and any V1 recompute
remain internal until false-positive review, extractor calibration, and the V1
external-ready gate complete.

## Global Evaluator Rules

| Area | V1 decision | Notes |
|---|---|---|
| Primary evaluator | approved | Asset-level historical directional outcome. |
| Primary horizon | approved | `7d` directional return. |
| Secondary horizons | approved | `1d` and `3d` diagnostics only. |
| Timestamp basis | approved | Public Telegram post timestamp; first available daily candle on or after post date. |
| Claim unit | approved | One normalized asset-level claim per approved asset. |
| Long method | approved | Raw forward return over the approved horizon. |
| Short method | approved | Directional return is negative raw forward return. |
| Basket method | approved_with_limits | Equal-weight only after asset-level outcomes exist; unsupported assets are excluded. |
| V0 publication | rejected_now | V0 metrics are internal until V1 review and external gate pass. |
| Investment advice | rejected | Reports must not recommend trades or future profit. |

## Claim-Type Decisions

| Claim type | Decision | Applies to | Rationale |
|---|---|---|---|
| `directional_thesis` | approved_internal_v1 | all three channels | V0 used this type for explicit bullish/bearish asset statements. Needs false-positive review before external use. |
| `position_disclosure` | approved_internal_v1_with_proxy_limits | `bablos79`; future rows in all channels if explicit sides exist | Supported when timestamped side and approved provider/proxy exist. |
| `trade_setup` | needs_operator_input | all three channels | Entry/stop/target/RR extraction is not reviewed yet. |
| `trade_management` | rejected_unless_linked | all three channels | Close/move-stop/update fragments need linked original setup. |
| `risk_warning` | context_only | all three channels | Useful explanation, not directional performance evidence by itself. |
| `market_context` | context_only | all three channels | Broad macro/index comments need explicit benchmark/proxy/horizon approval. |
| `transcript_media_claim` | internal_only_pending_review | all three channels | Audio transcript claims require human/operator acceptance before customer-facing metrics. |
| `image_ocr_chart_claim` | unsupported_now | all three channels | No reviewed source-linked OCR/chart claim path is approved yet. |

## Channel Matrix

| Channel | Approved evaluator types | Allowed claim types | Default horizons | Provider/proxy rules | Exclusion statuses |
|---|---|---|---|---|---|
| `bablos79` | asset-level directional outcome; partial position-disclosure outcome | `directional_thesis`, approved `position_disclosure` assets | primary `7d`; secondary `1d`, `3d` | Binance spot USDT for approved crypto assets; MOEX ISS daily candles for approved MOEX shares; `SBRF` maps to `SBER`; `bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md` controls extra position rows | `no_supported_asset_or_proxy`, `mixed_direction`, `no_direction`, `not_market_related`, `no_text`, `do_not_fetch`, `context_only`, `internal_only_pending_review` |
| `nemphiscrypts` | asset-level directional outcome | `directional_thesis` only until review finds explicit setups/positions | primary `7d`; secondary `1d`, `3d` | Binance spot USDT for approved crypto assets from V0; non-crypto aliases need provider expansion | `no_supported_asset_or_proxy`, `mixed_direction`, `no_direction`, `not_market_related`, `no_text`, `context_only`, `internal_only_pending_review` |
| `pifagortrade` | asset-level directional outcome | `directional_thesis` only until review finds explicit setups/positions | primary `7d`; secondary `1d`, `3d` | Binance spot USDT for approved crypto assets from V0; non-crypto aliases need provider expansion | `no_supported_asset_or_proxy`, `mixed_direction`, `no_direction`, `not_market_related`, `no_text`, `context_only`, `internal_only_pending_review` |

## V0 Provider And Proxy Class Decisions

| Provider/proxy class | V0 use | V1 decision | Rationale |
|---|---|---|---|
| Binance public daily klines, crypto spot `USDT` pairs | `BTCUSDT`, `ETHUSDT`, `TONUSDT`, `AVAXUSDT`, `ARBUSDT`, `SOLUSDT`, `SUIUSDT`, `DOTUSDT` | approved_internal_v1 | Public API path exists; compact provider confirmation is persisted in V0 JSON. |
| MOEX ISS public daily share candles | `LKOH`, `SBER`, `SMLT`, `CHMF`, `MAGN`, `PHOR`, `VTBR`, `NVTK`, `LENT`, `GAZP`, `X5`, `SFIN` | approved_internal_v1 | Public ISS candle path exists; compact provider confirmation is persisted in V0 JSON. |
| `SBRF` alias | not used directly in V0; approved in `bablos79` repair | approved_internal_v1_as_alias | May map to `SBER` only when source text uses the Sberbank legacy/common alias. |
| `WUSH` MOEX share | approved in `bablos79` repair | approved_internal_v1 | Public MOEX ISS candle path approved for position rows. |
| Futures-style proxies | `BR`, `SI`, `NG`, `MIX` and similar | needs_operator_input | Requires explicit contract/proxy semantics, rollover rules, and provider path. |
| FX/currency proxies | `CNY`, `CN` and similar | needs_operator_input | Requires explicit pair definition, provider path, and direction semantics. |
| US ETF/fund proxies | `SPY`, `QQQ` | approved_internal_v1_with_prototype_provider | Explicit liquid US fund symbols route to gated `yfinance_dev`; no bulk database use. |
| Ambiguous US fund aliases | `SPYF` and similar | needs_operator_input | Exact venue/provider mapping must be approved before scoring. |
| Liquid US equity proxies | `AAPL`, `MSFT`, `NVDA`, `TSLA`, `AMD` | approved_internal_v1_with_prototype_provider | Explicit liquid US equity symbols route to gated `yfinance_dev`; unsupported names remain exclusions. |
| Commodity proxies | `GOLD` and similar | needs_operator_input | Requires explicit spot/futures/ETF proxy choice. |
| Ambiguous/local aliases | `GD`, `NKNC`, `PRMD` and similar | rejected_until_mapped | No stable approved provider/proxy mapping in the current matrix. |

## Channel V0 Baseline For Calibration

| Channel | Public text rows | Normalized claims | 7d evaluable | 7d hit rate | Avg 7d directional return | Provider classes |
|---|---:|---:|---:|---:|---:|---|
| `bablos79` | 528 | 20 | 19 | 57.894737% | 0.381485% | Binance crypto, MOEX ISS shares |
| `nemphiscrypts` | 514 | 53 | 53 | 58.490566% | 0.857037% | Binance crypto |
| `pifagortrade` | 492 | 114 | 112 | 53.571429% | 0.071093% | Binance crypto |

## Required Before V1 Recompute

1. Run `SAS-V1-002` false-positive/false-negative review across included and
   excluded rows.
2. Apply deterministic extractor calibration before treating V1 counts as
   product metrics.
3. Use `src/signal_sandbox/claims/provider_config.py` for approved
   provider/proxy routing and fetch planning.
4. Keep unsupported providers/proxies as exclusions, not wins/losses.
5. Keep transcript/OCR/chart claims out of customer-facing metrics until
   reviewed.

## External-Use Boundary

This matrix does not approve external delivery. It only approves the internal
V1 research path. Customer-facing use still requires the V1 metric recompute,
limitations-first report, and `three_channel_V1_EXTERNAL_READY_GATE.md`.
