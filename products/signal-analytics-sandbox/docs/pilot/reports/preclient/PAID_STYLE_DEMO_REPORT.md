# Paid-Style Demo Report

Date: 2026-05-23
Status: `internal_demo_only`
Selected channel: `pifagortrade`
Allowed audience: `internal_only`

## Gate Status

- Decision: `internal_demo_only`.
- This artifact is a product-format demo, not an approved paid deliverable.
- No public display or external delivery is approved by this report.
- Media/OCR/chart/RR claims remain blocked until human/operator review and
  external gate approval.

## Selection Basis

`pifagortrade` is selected for the demo because the current evidence set gives
it the richest report surface, not because the channel is endorsed.

| evidence dimension | `bablos79` | `nemphiscrypts` | `pifagortrade` | source |
|---|---:|---:|---:|---|
| V1 evaluable text claims | 14 | 49 | 107 | `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json` |
| model-reviewed packet candidates | 1 | 1 | 7 | `docs/pilot/preclient_MODEL_REVIEW_PACKET.md` |
| public media refs | 196 | 63 | 36 | `docs/pilot/preclient_EVIDENCE_APPENDIX.md` |
| dashboard-safe RR rows | 0 | 0 | 0 | `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json` |

The selection is evidence-based: `pifagortrade` has the largest V1 evaluable
sample and the highest count of model-reviewed packet candidates. It also has
material weaknesses: 51 contradicted V1 text claims, slightly negative average
7d directional return, blocked RR, and several post-factum media rows.

## Product Promise Shown

This demo shows the paid-report shape:

- compact source profile;
- measurable historical text outcomes;
- source-linked examples and counterexamples;
- media/OCR review state;
- post-factum versus real-time distinction;
- setup/RR review queue;
- blocker register and gate status.

It does not show a channel endorsement, a public ranking, or external approval.

## Free Preview

The free card would show only compact internal fields:

- source type: `public_telegram_channel`;
- evaluated window: `2026-03-22..2026-05-22`;
- V1 evaluable text claims: `107`;
- confirmed / contradicted: `56` / `51`;
- primary hit rate: `52.336449%`;
- average 7d directional return: `-0.153127%`;
- media refs: `36`;
- model-reviewed packet candidates: `7`;
- gate: `internal_only_not_dashboard_safe`.

Source: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.md`.

## Locked Section: Evidence Appendix Preview

The paid-style report can expose the evidence trail without copying raw media:

| evidence slice | count / status | reference |
|---|---:|---|
| pifagortrade appendix rows | 38 | `docs/pilot/preclient_EVIDENCE_APPENDIX.md` |
| media-backed candidates | 3 | `docs/pilot/preclient_EVIDENCE_APPENDIX.md` |
| media post-factum rows | 4 | `docs/pilot/preclient_EVIDENCE_APPENDIX.md` |
| media processing blockers | 6 | `docs/pilot/preclient_EVIDENCE_APPENDIX.md` |
| provider-gap summary rows | 1 | `docs/pilot/preclient_EVIDENCE_APPENDIX.md` |

Example source refs:

- [pifagortrade/3214](https://t.me/pifagortrade/3214) - setup/risk/position
  candidate, RR blocked pending missing-field review.
- [pifagortrade/3225](https://t.me/pifagortrade/3225) - post-factum position
  evidence requiring classification.
- [pifagortrade/3234](https://t.me/pifagortrade/3234) - directional setup
  candidate requiring operator acceptance and market recompute.

## Locked Section: Post-Factum Vs Real-Time Distinction

The demo must separate real-time claims from screenshots that appear to describe
already-managed or already-closed positions.

| class | rows | interpretation |
|---|---|---|
| setup-like candidates | 3214, 3218, 3234 | useful for review, not accepted as real-time calls yet |
| post-factum candidates | 3225, 3264, 3274, 3276 | useful for process/risk review, not counted as predictive calls |
| rejected/noise rows | 5 appendix rows | excluded from channel outcome claims |

This distinction is one of the product's core paid-report values: it prevents a
channel from getting credit for screenshots that do not establish a source-time
call.

## Locked Section: Setup And RR Review

Current setup/RR state:

- dashboard-safe RR rows: `0`;
- model-reviewed packet rows: `7`;
- rows requiring missing-field review: `1`;
- rows requiring setup acceptance and market recompute: `2`;
- rows requiring post-factum classification or rejection as predictive signal:
  `4`.

Why RR is still blocked:

- some rows have missing or ambiguous target/stop/direction fields;
- some rows are screenshots of managed or closed positions;
- none has human/operator acceptance;
- no candidate has been recomputed through an approved market-data path for
  report use.

Source: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`.

## Locked Section: Counterexamples

The report must include counterexamples beside strengths.

- V1 contradicted example: [long ETH](https://t.me/pifagortrade/2647), 7d
  result `-0.281887%`, Binance provider path.
- Aggregate V1 text result: 56 confirmed / 51 contradicted over 107 evaluable
  text claims.
- Average 7d directional return is `-0.153127%`, so the measured text sample is
  not a one-sided positive story.

Source: `docs/pilot/reports/preclient/pifagortrade_DEEP_REPORT_V0.md`.

## Locked Section: Limitations

- This demo is internal only.
- Model-reviewed media is triage, not accepted truth.
- Provider gaps are exclusions, not source failures.
- Post-factum rows must not be treated as predictive calls.
- RR and setup conclusions require operator classification and market
  recompute.
- The current external gate remains `approve_internal_only`.

## Internal Demo Decision

`pifagortrade` is the current paid-style demo candidate because it best shows
the product format: compact metrics, evidence appendix, media review,
post-factum separation, setup/RR blockers, and counterexamples in one report.

Next required step: run Phase 37 deep review, then continue internal hardening
until human/operator acceptance, approved provider coverage, and market outcome
recompute make a buyer-demo subset safe.
