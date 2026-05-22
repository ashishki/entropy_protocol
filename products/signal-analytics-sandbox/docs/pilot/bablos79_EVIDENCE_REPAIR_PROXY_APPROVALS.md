# Evidence Repair Proxy Approvals - bablos79

Date: 2026-05-19
Status: operator_approved_internal_v1_rules

## Scope

This artifact completes `SAS-ER-001` for the `bablos79` evidence repair queue.
It approves a conservative internal-only proxy/horizon method for measurable
position-disclosure rows and rejects unsupported pieces as context.

These approvals do not make the report external-ready. Customer-facing use
still requires false-positive review, V1 extraction calibration, reviewed
media/OCR posture, and an external-ready gate.

## Global Outcome Rules

| Field | Approved rule |
|---|---|
| Timestamp basis | Public Telegram post timestamp; use first available daily candle on or after the post date. |
| Primary horizon | `7d` directional return. |
| Secondary horizons | `1d` and `3d` for sensitivity checks. |
| Position row unit | Asset-level claim; multi-asset posts produce one row per approved asset. |
| Long outcome | Raw forward return over the approved horizon. |
| Short outcome | Directional return is `-raw_return_pct` over the approved horizon. |
| Basket aggregation | Allowed only after asset-level outcomes exist; equal-weight over approved assets only. |
| Unsupported assets | Excluded with explicit reason; not treated as wins or losses. |
| Market-data posture | Open/public provider windows only; no bulk market-history database. |
| External posture | Internal V1 research only until external gate passes. |

## Approved Provider And Proxy Map

| Asset/proxy | Status | Provider | Provider symbol | Use | Rationale |
|---|---|---|---|---|---|
| `VTBR` | approved | MOEX ISS candles | `VTBR` | MOEX equity directional return | Public daily candles available; observed in V0. |
| `WUSH` | approved | MOEX ISS candles | `WUSH` | MOEX equity directional return | Public daily candles available. |
| `PHOR` | approved | MOEX ISS candles | `PHOR` | MOEX equity directional return | Public daily candles available; observed in V0. |
| `NVTK` | approved | MOEX ISS candles | `NVTK` | MOEX equity directional return | Public daily candles available; observed in V0. |
| `SBRF` | approved | MOEX ISS candles | `SBER` | MOEX equity directional return | Legacy/common Sberbank alias mapped to `SBER`. |
| `CHMF` | approved | MOEX ISS candles | `CHMF` | MOEX equity directional return | Public daily candles available; observed in V0. |
| `GAZP` | approved | MOEX ISS candles | `GAZP` | MOEX equity directional return | Public daily candles available; observed in V0. |
| `MAGN` | approved | MOEX ISS candles | `MAGN` | MOEX equity directional return | Public daily candles available; observed in V0. |
| `X5` | approved | MOEX ISS candles | `X5` | MOEX equity directional return | Public daily candles available in current V0 path. |
| `GD` | rejected_as_context | - | - | excluded | Ambiguous shorthand; no approved stable proxy in V1 matrix yet. |
| `NKNC` | rejected_as_context | - | - | excluded | Not in current approved provider/proxy list. |
| `PRMD` | rejected_as_context | - | - | excluded | Not in current approved provider/proxy list. |
| `BR` | rejected_as_context | - | - | excluded | Futures/proxy semantics not approved yet. |
| `CN` | rejected_as_context | - | - | excluded | Ambiguous shorthand; no approved stable proxy. |
| `SI` | rejected_as_context | - | - | excluded | Futures/proxy semantics not approved yet. |
| `CNY` | rejected_as_context | - | - | excluded | Currency pair/proxy semantics not approved yet. |
| `NG` | rejected_as_context | - | - | excluded | Futures/proxy semantics not approved yet. |
| `SPY` | rejected_as_context | - | - | excluded | US ETF provider path deferred to Phase 27 provider expansion. |
| `SPYF` | rejected_as_context | - | - | excluded | Ambiguous/local proxy; no approved stable provider path. |
| `GOLD` | rejected_as_context | - | - | excluded | Gold proxy/futures semantics not approved yet. |
| `MIX` | rejected_as_context | - | - | excluded | Broad index/proxy semantics not approved yet. |

## Position Disclosure Candidate Decisions

| capture_id | source | decision | approved assets | rejected/context assets | horizon | outcome method | reason |
|---|---|---|---|---|---|---|---|
| `bablos79-10008` | [source](https://t.me/bablos79/10008) | approved_for_proxy_mapping | long `VTBR`, long `WUSH` | long `NKNC`, long `PRMD`, short `GD` | `1d`, `3d`, `7d` | asset-level directional return | Row discloses timestamped sides; only approved MOEX assets may be evaluated. |
| `bablos79-10009` | [source](https://t.me/bablos79/10009) | approved_for_proxy_mapping | long `VTBR`, long `WUSH` | long `GD`, long `NKNC`, long `PRMD` | `1d`, `3d`, `7d` | asset-level directional return | Row discloses timestamped long basket; unsupported aliases excluded. |
| `bablos79-10122` | [source](https://t.me/bablos79/10122) | approved_for_proxy_mapping | long `VTBR`, long `WUSH` | long `BR`, long `CN`, long `NKNC`, long `PRMD`, long `SI` | `1d`, `3d`, `7d` | asset-level directional return | Partial approval for supported MOEX assets only. |
| `bablos79-10162` | [source](https://t.me/bablos79/10162) | approved_for_proxy_mapping | long `WUSH` | long `CNY`, long `NG`, long `NKNC`, long `PRMD`, long `SI`, short `SPY` | `1d`, `3d`, `7d` | asset-level directional return | Partial approval; currency/futures/US ETF proxies deferred. |
| `bablos79-10219` | [source](https://t.me/bablos79/10219) | approved_for_proxy_mapping | short `PHOR` | long `CN`, long `NG`, long `NKNC`, long `PRMD`, long `SI`, short `SPYF` | `1d`, `3d`, `7d` | asset-level directional return | Short `PHOR` has approved MOEX provider; remaining proxies excluded. |
| `bablos79-10277` | [source](https://t.me/bablos79/10277) | approved_for_proxy_mapping | short `NVTK`, short `VTBR` | long `CNY`, long `GOLD`, long `NG`, long `PRMD`, long `SI`, short `SPYF` | `1d`, `3d`, `7d` | asset-level directional return | Approved only for supported MOEX shorts. |
| `bablos79-10339` | [source](https://t.me/bablos79/10339) | approved_for_proxy_mapping | short `VTBR` | long `CNY`, long `SI`, short `SPYF` | `1d`, `3d`, `7d` | asset-level directional return | Approved only for supported MOEX short. |
| `bablos79-10391` | [source](https://t.me/bablos79/10391) | approved_for_proxy_mapping | short `SBRF` via `SBER` | long `CNY`, short `SPYF` | `1d`, `3d`, `7d` | asset-level directional return | Sberbank alias can be measured through `SBER`; remaining proxies excluded. |
| `bablos79-10526` | [source](https://t.me/bablos79/10526) | approved_for_proxy_mapping | short `CHMF`, short `GAZP`, short `MAGN`, short `X5` | long `NG` | `1d`, `3d`, `7d` | asset-level directional return | Supported MOEX short basket; `NG` futures proxy excluded. |
| `bablos79-10576` | [source](https://t.me/bablos79/10576) | rejected_as_context | - | long `NG`, short `MIX` | - | do_not_fetch | Both sides require futures/index proxy approval not present in V1 matrix. |

## Non-Position Candidate Policy

| Category | Decision | Reason |
|---|---|---|
| `trade_management_fragment` | rejected_as_context unless linked to an approved original setup | Closing/moved-stop fragments cannot be scored without entry context. |
| `directional_bias_candidate` | may be considered in Phase 27 extractor review | Needs false-positive review and stable proxy mapping before inclusion. |
| `market_context_candidate` | context_only by default | Broad macro/context rows need benchmark, direction, and horizon approval. |
| transcript/media claims | internal_only | No human/operator external acceptance yet. |
| image/OCR/chart claims | unsupported_now | No reviewed image/OCR source-linked claims yet. |

## Market-Data Permission

Only rows and assets marked `approved_for_proxy_mapping` above may request
market-data windows, and only for the approved provider/symbol/time window.
Every other row remains `do_not_fetch`.

## Remaining Blockers

- False-positive/false-negative review of V0 extraction is still required
  before customer-facing use.
- Provider expansion for futures, FX, broad indices, US ETFs, and gold remains
  Phase 27 work.
- Audio/OCR/image claims remain internal-only until reviewed and accepted.
- External delivery still requires a V1 external-ready gate.
