# bablos79 Internal Deep Report V0

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

bablos79 is currently useful as an internal diligence lead, not as an externally approved channel score. Public Telegram market commentary with MOEX equity coverage plus some crypto references. The card-level gate remains `internal_only_not_dashboard_safe` and every media/RR claim is blocked pending review gates.

## Source And Period

- Source type: `public_telegram_channel`.
- Evaluated window: `2026-03-22..2026-05-22`.
- Primary markets: MOEX equities, BTC/USDT.

## Source Style

- Content style: market commentary, macro/context notes, occasional chart or setup evidence.
- Evidence reference: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.

## Measurable Claims

- V1 evaluable text claims: `14`.
- Confirmed / contradicted: `9` / `5`.
- Primary hit rate: `64.285714%`.
- Average 7d directional return: `0.742848%`.
- Evidence reference: `docs/pilot/three_channel_V1_METRIC_RESULTS.json`.

## Media Findings

- Public media refs: `196`.
- Modality counts: `{'image': 94, 'video': 34, 'voice': 68}`.
- Evidence kind counts: `{'context_only': 2, 'media_backed_claim': 1, 'media_processing_blocker': 39, 'media_review_queue': 106, 'provider_gap': 1, 'rejected_noise': 48, 'text_only_claim_metric_summary': 1}`.
- Model-reviewed packet candidates: `1`.
- Evidence reference: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.

## Setup And RR Findings

- Summary: One internal RR-ready draft exists, but it still needs operator acceptance and market recompute.
- Dashboard-safe RR rows: `0`.
- Evidence reference: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`.

## Model-Reviewed Candidates

| post | modality | evidence types | setup/RR status | required action |
|---|---|---|---|---|
| [10450](https://t.me/bablos79/10450) | image | directional_thesis, explicit_trade_setup | `rr_ready_internal_draft` | `operator_review_for_setup_acceptance_and_market_recompute` |

## Confirmed Example

- Source: [short PHOR](https://t.me/bablos79/10208), 7d result `4.443290%`, MOEX ISS provider path.
- Evidence reference: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.

## Contradicted Example

- Source: [long BTC](https://t.me/bablos79/10250), 7d result `-5.795072%`, Binance provider path.
- Evidence reference: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`.

## Strengths

- Largest public text corpus in the current V1 metric artifact. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.
- Measurable text claims cover both MOEX equities and one crypto proxy. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.
- One model-reviewed media setup has entry, stop, target, and internal draft RR fields. Evidence: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`.

## Weaknesses

- Media evidence is model-reviewed only and remains blocked pending operator review. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- Many media rows are context, non-market, rejected noise, or video/manual blockers. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.
- The measurable text edge is modest and not approved for external display. Evidence: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`.

## Limitations

- Model-reviewed media is triage only and cannot be used as customer-facing truth.
- Provider gaps are exclusions, not source failures.
- RR/setup conclusions need operator classification and market recompute.
- The external gate is still `approve_internal_only`.

## Report Decision

- `internal_only` until human/operator review and external gate pass.
- Suitable next use: input to `SAS-PRECLIENT-006` paid-style internal demo selection, not external delivery.
