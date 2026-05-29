# Channel Quant Metrics V2

Status: internal metric contract
Date: 2026-05-19
Owner: codex

## Purpose

This spec defines quant-grade channel utility metrics for reviewed public
source claims. It is a calculation contract, not marketing copy and not a
ranking system. Metrics may be reported only with their sample size, coverage,
exclusions, provider limits, and confidence warnings.

## Eligible Inputs

A row can enter Quant Metrics V2 only when all required fields are explicit or
approved by review:

- public or operator-authorized evidence reference;
- normalized channel, author, timestamp, text span, and claim type;
- canonical asset and direction semantics where needed;
- approved provider/proxy and deterministic horizon;
- deterministic outcome status or explicit exclusion reason.

Unsupported provider rows, unreviewed media/OCR/chart claims, ambiguous
shorthand, and rows missing levels required for their metric stay excluded.
They count in coverage denominators, not wins or losses.

## Metric Dictionary

### Extraction Precision

Formula:

`precision = accepted_extracted_claims / reviewed_extracted_claims`

Use this for parser or model quality. The denominator is every extracted claim
that received a human or documented confidence-gate review. Rejected
false-positive claims stay in the denominator. Do not compute precision from
only scoreable market outcomes.

### Extraction Recall

Formula:

`recall = accepted_extracted_claims / accepted_claims_in_reviewed_corpus`

Use this only when a reviewed source corpus or audited sample contains both
machine-found claims and manually found missed claims. If the missed-claim pass
is incomplete, emit `recall_unavailable` and report the review gap.

### Hit Rate By Type

Formula:

`hit_rate_by_type = confirmed_count / (confirmed_count + contradicted_count)`

Group by `claim_type`, and optionally by asset, horizon, and direction. Neutral,
excluded, missing-provider, missing-level, and insufficient-data rows do not
enter the hit-rate denominator, but their counts must be shown next to the rate.

Minimum groups:

- `directional_thesis`
- `trade_setup`
- `risk_warning`
- `market_regime`
- `post_factum_or_context`

### Return Percent

Formula:

`return_pct = direction_adjusted_exit_change_pct`

For long claims this is `(exit_price - anchor_price) / anchor_price * 100`.
For short claims this is `(anchor_price - exit_price) / anchor_price * 100`.
Anchor and exit selection must come from the approved outcome policy.

### MFE And MAE

Maximum favorable excursion:

`mfe_pct = max(direction_adjusted_path_change_pct)`

Maximum adverse excursion:

`mae_pct = min(direction_adjusted_path_change_pct)`

MFE/MAE require intrahorizon price path data. If only endpoint data exists,
emit `mfe_mae_unavailable` instead of approximating path behavior.

### RR

Formula:

`rr = abs(target_price - entry_price) / abs(entry_price - stop_price)`

RR is allowed only for setup claims with explicit or approved entry, stop, and
target. Missing levels are blockers, not inferred values. For short setups the
same absolute-distance formula applies after validating level ordering.

### R Multiple

Formula:

`r_multiple = realized_directional_pnl / initial_risk`

For long setups:

`initial_risk = entry_price - stop_price`

For short setups:

`initial_risk = stop_price - entry_price`

`initial_risk` must be positive. If the setup never fills, report
`setup_not_filled`. If the setup fills but lacks stop approval, emit
`r_multiple_unavailable`.

### Benchmark-Relative Return

Formula:

`benchmark_relative_return_pct = claim_return_pct - benchmark_return_pct`

The benchmark asset, provider, horizon, and direction semantics must be
approved before calculation. If benchmark data is missing, emit
`missing_benchmark_data`; do not treat that row as outperformance or
underperformance.

### Drawdown

Formula:

`drawdown_t = cumulative_metric_t - running_peak_t`

`max_drawdown = min(drawdown_t)`

Drawdown can be computed on cumulative R multiples for setup rows or cumulative
return percent for directional rows. The report must label which curve was
used. Mixed claim types require separate curves or an explicit normalized
portfolio model.

## Coverage Metrics

Every channel report must include:

- total source rows;
- market-adjacent candidate rows;
- extracted claim rows;
- reviewed claim rows;
- accepted claim rows;
- outcome-evaluable rows;
- provider-gap exclusions;
- media/OCR/transcript blockers;
- missing-level blockers;
- benchmark-data exclusions.

Coverage ratios are diagnostic. They are not performance scores.

## Sample-Size And Confidence Warnings

Required warnings:

- `thin_sample`: fewer than 30 evaluable outcomes for a channel or metric group;
- `provisional_sample`: 30 to 99 evaluable outcomes;
- `small_type_bucket`: fewer than 10 evaluable outcomes for a claim type;
- `low_review_coverage`: less than 95 percent of extracted claims reviewed;
- `low_provider_coverage`: less than 80 percent of accepted claims scoreable by
  approved providers;
- `missing_recall_audit`: recall is requested without a completed missed-claim
  audit;
- `media_unreviewed`: media/OCR/transcript evidence exists but is not accepted
  for the reported metric;
- `benchmark_incomplete`: benchmark-relative metrics requested while benchmark
  data is missing for any included row.

Confidence tier:

- `high`: at least 100 evaluable outcomes, review coverage >= 95 percent,
  provider coverage >= 80 percent, and no unresolved blocker affecting the
  metric being summarized;
- `medium`: at least 30 evaluable outcomes and all exclusions are explicit;
- `low`: fewer than 30 evaluable outcomes or any unresolved review/provider
  blocker.

Confidence tier describes evidence strength only. It must not be converted into
investment advice, a channel leaderboard, or a future-profit claim.

## Reporting Rules

- Always display numerator and denominator beside each percentage.
- Always separate extraction quality from market outcome quality.
- Always separate coverage, clarity, outcome, risk, and limitation sections.
- Never rank channels unless a later external policy explicitly allows it.
- Never fill missing provider, benchmark, stop, target, or path data with
  guessed values.
