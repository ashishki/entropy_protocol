# Channel Impact Framework

Date: 2026-05-22
Status: draft_v1_internal

## Purpose

This framework defines how Signal Analytics Sandbox should evaluate a public
market channel beyond raw PnL. PnL is useful, but channel impact also includes
trend sense, insight depth, methodology, risk discipline, practical usefulness,
and evidence quality.

The product goal is two-layered:

1. A lightweight dashboard that compares channels using simple, explainable
   metrics and confidence labels.
2. A paid deep report that explains why a channel scored that way, with
   evidence, examples, counterexamples, limitations, and source links.

## Source Of Truth Model

| Layer | Source of truth | What it proves | What it does not prove |
|---|---|---|---|
| Author statement | Public post, source-linked audio, source-linked image/chart, timestamp, hash | What the author actually said before/at the time. | Whether the claim was true or useful. |
| Interpretation | Normalized claim/idea ledger plus review decision | How the system and reviewer understood the statement. | Final market truth if the claim is ambiguous. |
| Market outcome | Approved provider/proxy snapshot and deterministic rule | What happened in market data after the claim. | Author intent if the original statement lacked direction/horizon/setup. |
| Product conclusion | Report/gate artifact | What can be safely shown internally or externally. | Investment advice or future performance. |

Model output is never the sole truth. LLM/OCR/transcript output is draft until
reviewed. Ambiguous claims are not wins or losses.

## Impact Dimensions

### 1. Signal Performance

Measures whether explicit market calls worked under deterministic rules.

Example metrics:

- measurable claim count;
- directional hit rate;
- average/median directional return;
- MFE/MAE;
- target hit / stop hit / timeout;
- realized R multiple where entry/stop/target exist;
- benchmark-relative return;
- provider/proxy coverage.

Use when the author gives enough structure to test the idea.

### 2. Trend Sense

Measures whether the channel helps a reader understand market regime.

Evidence examples:

- early risk-on/risk-off calls;
- sector rotation calls;
- trend continuation/reversal calls;
- volatility or liquidity regime calls;
- correct invalidation when regime changes.

Metric shape:

- regime call count;
- horizon-aligned directional accuracy;
- benchmark-relative regime accuracy;
- stale-view penalty;
- confidence based on sample size and clarity.

### 3. Insight Depth

Measures whether the author explains why a market move or setup matters.

Review criteria:

- causal thesis exists;
- catalyst is named;
- non-obvious relationship is explained;
- counter-scenario or invalidation exists;
- thesis can be checked later;
- claim is not generic "up or down" wording.

This dimension can be useful even when no trade setup exists, but confidence
must be lower if the thesis cannot be outcome-tested.

### 4. Trading Methodology

Measures whether the author has a consistent way of working with the market.

Signals:

- entry logic;
- exit logic;
- level work;
- follow-up discipline;
- position management;
- update after invalidation;
- no rewriting of past calls.

This is scored from reviewed sequences, not isolated lucky posts.

### 5. Risk Management

Measures whether the channel protects the reader from bad decision-making.

Evidence:

- stops or invalidation;
- risk sizing language;
- volatility warnings;
- no all-in pressure;
- no endless averaging down without invalidation;
- loss acknowledgement;
- distinction between idea and position.

Risk score should be shown separately from performance. A channel can have good
ideas and poor risk discipline.

### 6. Practical Usefulness

Measures whether a subscriber can realistically act on or learn from the
channel.

Inputs:

- clarity of timeframe;
- speed of stale signal decay;
- follow-up rate;
- noise ratio;
- setup completeness;
- reader effort needed to extract value;
- translation from thesis to action.

### 7. Creativity / Differentiation

Measures whether the channel provides something non-commodity.

Evidence:

- unique source synthesis;
- unusual but testable cross-market links;
- differentiated watchlists;
- clear mental models;
- early framing before consensus;
- useful scenario planning.

This must be evidence-backed. "Interesting style" is not enough.

### 8. Evidence Confidence

Measures whether the score itself should be trusted.

Inputs:

- source coverage;
- multimodal coverage;
- review coverage;
- sample size;
- deleted/unavailable rows;
- provider/proxy support;
- timestamp quality;
- false-positive/false-negative review;
- media acceptance status.

Every dashboard score needs a confidence label: high, medium, low, or blocked.

## Dashboard Score Shape

The future dashboard should avoid a single universal "best channel" rank.
Instead, show separate dimensions:

| Dashboard field | Meaning |
|---|---|
| `measurable_claims` | Count of claims that could be tested. |
| `signal_performance` | Strict outcome metrics for explicit calls. |
| `trend_sense` | Regime/directional market-view quality. |
| `insight_depth` | Quality of causal and non-obvious thesis work. |
| `methodology_clarity` | Whether the author has a repeatable trading process. |
| `risk_discipline` | Whether risk, invalidation, and loss handling are present. |
| `practical_usefulness` | Whether a subscriber can use the channel efficiently. |
| `creativity` | Differentiated, testable thinking. |
| `evidence_confidence` | Trust level of the assessment itself. |
| `external_gate` | Whether the result can be shown externally. |

## Paid Deep Report Boundary

Paid report contains what the dashboard should not fully expose:

- full claim ledger;
- confirmed and contradicted examples;
- author style and methodology notes;
- risk-management evidence;
- multimodal evidence review;
- source coverage gaps;
- exact provider/proxy decisions;
- why scores are high/low/confidence-limited;
- what kind of user may benefit from the channel;
- what should not be trusted.

The public/free surface can publish selected safe excerpts, aggregate scores,
and limitations, but not the full evidence analysis if that is the paid product.

## Scoring Rules

- Do not combine dimensions into a single leaderboard score by default.
- Low sample size must cap confidence.
- Unsupported media cannot improve scores.
- Provider gaps are exclusions, not losses.
- Ambiguous claims are neither wins nor losses.
- If an author did not state a target, do not pretend target accuracy exists.
- If a standardized horizon is used, label it as system-defined, not author-stated.
- Never produce investment advice or future-profit language.
