# Three-Channel V2 Utility Scorecard

Date: 2026-05-19
Status: internal_v2_validation_not_external_ready
Metric contract: `docs/specs/CHANNEL_QUANT_METRICS_V2.md`

## Method

- Uses reviewed V1 metric results from
  `docs/pilot/three_channel_V1_METRIC_RESULTS.json`.
- Separates coverage, clarity, extraction quality, outcome quality, risk
  quality, and limitations.
- Does not produce a single composite score.
- Does not approve external delivery.
- Unsupported provider, media, benchmark, and missing-level rows remain
  exclusions, not wins or losses.

## Coverage

| Channel | Public text rows | V1 evaluable claims | Provider-gap rows | Evaluable coverage |
|---|---:|---:|---:|---:|
| `bablos79` | 528 | 14 | 75 | 2.65% of public text rows |
| `nemphiscrypts` | 514 | 49 | 128 | 9.53% of public text rows |
| `pifagortrade` | 492 | 107 | 162 | 21.75% of public text rows |

Coverage is a data-readiness measure only. High coverage does not imply high
market utility.

## Clarity

| Channel | Main clarity blockers | Direction blockers | Context blockers |
|---|---|---:|---:|
| `bablos79` | Unsupported assets and no-direction rows | mixed 11, no direction 38 | needs_context 3 |
| `nemphiscrypts` | Unsupported assets and mixed-direction rows | mixed 32, no direction 17 | needs_context 3 |
| `pifagortrade` | Mixed-direction rows and unsupported assets | mixed 90, no direction 28 | needs_context 3 |

Clarity describes whether the source produced claims that can be normalized
without adding assumptions.

## Extraction Quality

| Channel | Reviewed false positives | Reviewed context exclusions | Pending false negatives | Review posture |
|---|---:|---:|---:|---|
| `bablos79` | 2 | 3 | 0 | low_review_coverage |
| `nemphiscrypts` | 1 | 3 | 2 | low_review_coverage, missing_recall_audit |
| `pifagortrade` | 3 | 3 | 3 | low_review_coverage, missing_recall_audit |

Extraction quality is not the same as market outcome quality. A clean parser can
still extract weak ideas, and a noisy parser can miss useful ideas.

## Outcome Quality

| Channel | Confirmed hits | Contradicted misses | Hit rate | Avg return | Avg MFE | Avg MAE |
|---|---:|---:|---:|---:|---:|---:|
| `bablos79` | 9 | 5 | 64.285714% | 0.742848% | 3.637653% | -3.060955% |
| `nemphiscrypts` | 28 | 21 | 57.142857% | 0.434858% | 7.991959% | -7.354706% |
| `pifagortrade` | 56 | 51 | 52.336449% | -0.153127% | 6.309542% | -7.010254% |

Outcome quality uses only V1 evaluable rows. Excluded rows are shown in coverage
and limitations rather than counted as misses.

## Risk Quality

| Channel | RR rows | R multiple rows | Setup risk posture |
|---|---:|---:|---|
| `bablos79` | 0 | 0 | No approved setup-level risk sample yet |
| `nemphiscrypts` | 0 | 0 | No approved setup-level risk sample yet |
| `pifagortrade` | 0 | 0 | No approved setup-level risk sample yet |

Risk quality is currently the weakest dimension: V1 mostly evaluates
directional asset calls, not complete entry/stop/target setups.

## Confidence And Sample Warnings

| Channel | Confidence tier | Required warnings |
|---|---|---|
| `bablos79` | `low` | thin_sample, small_type_bucket, low_review_coverage, low_provider_coverage |
| `nemphiscrypts` | `low` | provisional_sample, low_review_coverage, low_provider_coverage, missing_recall_audit |
| `pifagortrade` | `low` | low_review_coverage, low_provider_coverage, missing_recall_audit |

Confidence tier describes evidence strength only. All three channels remain
internal-only because review coverage, provider coverage, media acceptance, and
setup/RR coverage are incomplete.

## Limitations

- No customer-facing delivery is approved by the current gate.
- No unreviewed media/OCR/transcript claims are included.
- Benchmark-relative outcomes exist in code, but this V1 dataset does not yet
  include approved benchmark rows.
- Setup R multiple exists in code, but this V1 dataset has zero approved RR rows.
- Provider-gap exclusions remain material for all channels.
- The scorecard must be read as a diagnostic artifact, not a purchasing,
  trading, or subscription recommendation.
