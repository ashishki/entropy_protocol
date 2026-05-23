# pifagortrade Internal Deep Report V0

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

pifagortrade is currently useful as an internal diligence lead, not as an externally approved channel score. Public Telegram trading channel with crypto charts, setup language, and post-trade screenshots. The card-level gate remains `internal_only_not_dashboard_safe` and every media/RR claim is blocked pending review gates.

## Source And Period

- Source type: `public_telegram_channel`.
- Evaluated window: `2026-03-22..2026-05-22`.
- Primary markets: BTC/USDT, ETH/USDT, TON/USDT, DOT/USDT.

## Source Style

- Content style: chart setups, position screenshots, risk/position management evidence.
- Evidence reference: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.

## Measurable Claims

- V1 evaluable text claims: `107`.
- Confirmed / contradicted: `56` / `51`.
- Primary hit rate: `52.336449%`.
- Average 7d directional return: `-0.153127%`.
- Evidence reference: `docs/pilot/three_channel_V1_METRIC_RESULTS.json`.

## Media Findings

- Public media refs: `36`.
- Modality counts: `{'image': 28, 'video': 6, 'voice': 2}`.
- Evidence kind counts: `{'media_backed_claim': 3, 'media_post_factum': 4, 'media_processing_blocker': 6, 'media_review_queue': 18, 'provider_gap': 1, 'rejected_noise': 5, 'text_only_claim_metric_summary': 1}`.
- Model-reviewed packet candidates: `7`.
- Evidence reference: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.

## Setup And RR Findings

- Summary: No dashboard-safe RR yet; candidates need operator classification and recompute.
- Dashboard-safe RR rows: `0`.
- Evidence reference: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`.

## Model-Reviewed Candidates

| post | modality | evidence types | setup/RR status | required action |
|---|---|---|---|---|
| [3214](https://t.me/pifagortrade/3214) | image | explicit_trade_setup, risk_management, position_management | `rr_blocked` | `operator_review_missing_setup_fields` |
| [3218](https://t.me/pifagortrade/3218) | image | directional_thesis, explicit_trade_setup | `rr_blocked` | `operator_review_for_setup_acceptance_and_market_recompute` |
| [3225](https://t.me/pifagortrade/3225) | image | post_factum, position_management, risk_management | `rr_blocked` | `operator_mark_post_factum_or_reject_as_predictive_signal` |
| [3234](https://t.me/pifagortrade/3234) | image | directional_thesis, explicit_trade_setup, risk_management | `rr_blocked` | `operator_review_for_setup_acceptance_and_market_recompute` |
| [3264](https://t.me/pifagortrade/3264) | image | post_factum, explicit_trade_setup | `rr_blocked` | `operator_mark_post_factum_or_reject_as_predictive_signal` |
| [3274](https://t.me/pifagortrade/3274) | image | explicit_trade_setup, post_factum | `rr_blocked` | `operator_mark_post_factum_or_reject_as_predictive_signal` |
| [3276](https://t.me/pifagortrade/3276) | image | post_factum, explicit_trade_setup | `rr_blocked` | `operator_mark_post_factum_or_reject_as_predictive_signal` |

## Confirmed Example

- Source: [long BTC](https://t.me/pifagortrade/2643), 7d result `3.182273%`, Binance provider path.
- Evidence reference: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.

## Contradicted Example

- Source: [long ETH](https://t.me/pifagortrade/2647), 7d result `-0.281887%`, Binance provider path.
- Evidence reference: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.

## Strengths

- Largest V1 evaluable claim count in the current metric artifact. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.
- Media review found the highest count of arbiter-accepted internal candidates. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.
- Several media rows contain explicit setup, risk, position, or post-factum evidence. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.

## Weaknesses

- Several accepted media candidates are post-factum and cannot be treated as forward-looking calls. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- RR is mostly blocked by missing or ambiguous stop, target, direction, or asset fields. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- Average directional return in V1 is slightly negative despite a near-even hit split. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.

## Limitations

- Model-reviewed media is triage only and cannot be used as customer-facing truth.
- Provider gaps are exclusions, not source failures.
- RR/setup conclusions need operator classification and market recompute.
- The external gate is still `approve_internal_only`.

## Report Decision

- `internal_only` until human/operator review and external gate pass.
- Suitable next use: input to `SAS-PRECLIENT-006` paid-style internal demo selection, not external delivery.
