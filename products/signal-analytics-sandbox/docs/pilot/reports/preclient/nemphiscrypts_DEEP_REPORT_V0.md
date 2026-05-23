# nemphiscrypts Internal Deep Report V0

Date: 2026-05-23
Status: `internal_only_deep_report_v0`
Allowed audience: `internal_only`

## Gate Status

- Decision: `internal_only`.
- This report is not approved for public dashboard display or paid delivery.
- Media/OCR/chart/RR claims require human/operator review and external gate approval before customer-facing use.

## Evidence Base

- Evidence appendix: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- Dashboard card: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.md`.
- Model packet: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`.
- V1 utility examples: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.
- Paid boundary: `docs/specs/PAID_CHANNEL_REPORT_BOUNDARY.md`.

## Executive Summary

nemphiscrypts is currently useful as an internal diligence lead, not as an externally approved channel score. Public Telegram crypto commentary with chart-driven directional ideas. The card-level gate remains `internal_only_not_dashboard_safe` and every media/RR claim is blocked pending review gates.

## Source And Period

- Source type: `public_telegram_channel`.
- Evaluated window: `2026-03-22..2026-05-22`.
- Primary markets: crypto perpetuals, BTC/USDT, ETH/USDT, SOL/USDT, SUI/USDT.

## Source Style

- Content style: directional crypto ideas, charts, watchlist-like posts.
- Evidence reference: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.

## Measurable Claims

- V1 evaluable text claims: `49`.
- Confirmed / contradicted: `28` / `21`.
- Primary hit rate: `57.142857%`.
- Average 7d directional return: `0.434858%`.
- Evidence reference: `docs/pilot/three_channel_V1_METRIC_RESULTS.json`.

## Media Findings

- Public media refs: `63`.
- Modality counts: `{'image': 63}`.
- Evidence kind counts: `{'context_only': 2, 'media_backed_claim': 1, 'media_processing_blocker': 2, 'media_review_queue': 45, 'provider_gap': 1, 'rejected_noise': 13, 'text_only_claim_metric_summary': 1}`.
- Model-reviewed packet candidates: `1`.
- Evidence reference: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.

## Setup And RR Findings

- Summary: RR is blocked for the accepted media candidate because target and position fields are missing.
- Dashboard-safe RR rows: `0`.
- Evidence reference: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`.

## Model-Reviewed Candidates

| post | modality | evidence types | setup/RR status | required action |
|---|---|---|---|---|
| [3958](https://t.me/nemphiscrypts/3958) | image | directional_thesis, explicit_trade_setup | `rr_blocked` | `operator_review_missing_setup_fields` |

## Confirmed Example

- Source: [long BTC](https://t.me/nemphiscrypts/3344), 7d result `0.486250%`, Binance provider path.
- Evidence reference: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.

## Contradicted Example

- Source: [long BTC](https://t.me/nemphiscrypts/3376), 7d result `-1.605656%`, Binance provider path.
- Evidence reference: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.

## Strengths

- V1 text metrics have a larger crypto sample than bablos79. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.
- Media review found one model-reviewed setup candidate with entry and stop fields. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.
- Coverage is mostly crypto, which simplifies provider routing through Binance proxies. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.

## Weaknesses

- The model-reviewed setup lacks targets and position sizing. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- All media-derived claims are blocked pending operator review. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- Provider gaps and unsupported assets remain material exclusions. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.

## Limitations

- Model-reviewed media is triage only and cannot be used as customer-facing truth.
- Provider gaps are exclusions, not source failures.
- RR/setup conclusions need operator classification and market recompute.
- The external gate is still `approve_internal_only`.

## Report Decision

- `internal_only` until human/operator review and external gate pass.
- Suitable next use: input to `SAS-PRECLIENT-006` paid-style internal demo selection, not external delivery.
