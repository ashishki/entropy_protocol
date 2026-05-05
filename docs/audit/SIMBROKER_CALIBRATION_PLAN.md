# SIMBROKER_CALIBRATION_PLAN
_Date: 2026-05-05 · Scope: P0.6-006 SimBroker calibration tooling_

## Purpose

Define how to produce Phase 0 SimBroker calibration evidence: fills within 15%
of market bid/ask data on >=100 manually verified fills across representative
assets.

This plan does not activate a provider, fetch external data, approve Phase 0, or
claim SimBroker calibration is complete.

## Gate Requirement

| Item | Requirement |
|------|-------------|
| Criterion | SimBroker fills within 15% of market bid/ask data |
| Minimum sample | >=100 manually verified fills |
| Coverage | Representative assets |
| Current status | `TOOLING_READY_EVIDENCE_MISSING` |
| Current implementation | Cost model, fill engine, `BidAskProvider`, calibration row validation, JSONL round-trip, and summary tooling exist |

## Current Implementation Surface

| Component | Current state |
|-----------|---------------|
| `entropy/simbroker/costs.py` | Deterministic cost decomposition |
| `entropy/simbroker/fills.py` | Deterministic fill price constrained to bar high/low |
| `entropy/simbroker/calibration.py` | `BidAskQuote`, provider boundary, `CalibrationRow`, `CalibrationSummary`, JSONL reader/writer, Markdown summary |
| `entropy/models/registry.py` | `FillLog` stores fill price and cost components |
| Tests | T15-T17 SimBroker tests pass in current baseline |

The missing piece is approved real evidence, not row validation or summary
tooling.

## Source Approval Required

Before evidence collection starts, the human owner must approve:

- data source name;
- whether source is broker quote export, exchange quote export, or approved
  historical quote dataset;
- asset universe;
- timestamp tolerance;
- timezone normalization rule;
- quote staleness limit;
- allowed spread anomalies and rejection rules;
- storage location for raw source extract;
- whether external network egress is allowed for the specific task.

No provider activation or network egress is authorized by this document.

## Representative Sample Design

Minimum sample:

- at least 100 fills total;
- at least 5 assets unless the approved target universe is smaller;
- at least 10 fills per included asset where possible;
- both buy and sell sides represented;
- multiple market conditions represented when available;
- no cherry-picking after seeing deviation outcomes.

Recommended stratification:

| Dimension | Minimum expectation |
|-----------|---------------------|
| Asset type | Include representative target assets from the Phase 0/Phase 1 universe |
| Side | Buy and sell |
| Spread regime | Normal and wider-spread intervals where naturally present |
| Bar frequency | Match the dataset/evaluation frequency being calibrated |
| Time | Multiple dates, not one isolated quote cluster |

## Calibration Row Schema

Each manually verified row should include:

| Field | Description |
|-------|-------------|
| `calibration_id` | Unique row ID |
| `symbol` | Asset symbol |
| `asset_class` | Equity, crypto, commodity, etc. if known |
| `side` | Buy or sell |
| `fill_ts` | SimBroker fill timestamp, UTC |
| `quote_ts` | Market quote timestamp, UTC |
| `quote_source` | Approved source identifier |
| `quote_source_hash` | Hash of raw quote/source extract |
| `bid` | Market bid |
| `ask` | Market ask |
| `mid` | `(bid + ask) / 2` |
| `spread` | `ask - bid` |
| `simbroker_fill_price` | SimBroker fill price |
| `bar_open` | Source OHLCV bar open, if available |
| `bar_high` | Source OHLCV bar high |
| `bar_low` | Source OHLCV bar low |
| `bar_close` | Source OHLCV bar close |
| `quantity` | Fill quantity |
| `commission` | SimBroker commission |
| `slippage` | SimBroker slippage component |
| `market_impact` | SimBroker market impact component |
| `borrow_rate` | SimBroker borrow component |
| `funding_rate` | SimBroker funding component |
| `total_cost` | Total SimBroker cost |
| `reference_price` | For buys: ask; for sells: bid unless source policy says otherwise |
| `absolute_deviation` | `abs(simbroker_fill_price - reference_price)` |
| `pct_deviation` | `absolute_deviation / reference_price` |
| `pass_15pct` | Boolean |
| `manual_verifier` | Human/verifier identifier |
| `manual_verification_ts` | Verification timestamp |
| `exclusion_reason` | Null unless row is excluded before scoring |

## Acceptance Calculation

Per row:

- buy reference price: approved ask quote;
- sell reference price: approved bid quote;
- `pct_deviation = abs(simbroker_fill_price - reference_price) / reference_price`;
- pass if `pct_deviation <= 0.15`.

Gate packet acceptance:

- at least 100 included rows;
- all included rows manually verified;
- no excluded row omitted because it failed after scoring;
- report shows per-asset count, pass count, max deviation, median deviation, and
  95th percentile deviation;
- any row above 15% is a failure unless a pre-scoring exclusion rule applies.

## Evidence Artifacts

Required files for the future evidence task:

| Artifact | Purpose |
|----------|---------|
| Raw quote extract | Source data used for manual verification |
| Source hash manifest | Hashes for raw quote extracts and transformed tables |
| Calibration table | Row-level schema above |
| Calibration summary | Aggregate counts and pass/fail |
| Manual verification notes | Human verification evidence |
| Provider/source approval note | Human approval for source and egress, if any |

Suggested future paths:

- `artifacts/simbroker/calibration/raw/`
- `artifacts/simbroker/calibration/calibration_rows.parquet`
- `artifacts/simbroker/calibration/calibration_summary.md`

These paths are recommendations only; no artifacts are generated by this plan.

## Failure Handling

| Failure | Required action |
|---------|-----------------|
| <100 included rows | Gate evidence incomplete |
| Missing manual verification | Row excluded; if count drops below 100, gate incomplete |
| Quote timestamp outside tolerance | Row excluded by pre-scoring rule |
| Deviation >15% | Calibration failure; do not tune after seeing failures without preregistered revision |
| Concentrated sample | Expand assets/dates before gate use |
| Missing source hash | Evidence invalid |

## Non-Closure Rules

- T15-T17 tests do not close calibration.
- A `BidAskProvider` implementation alone does not close calibration.
- Synthetic quotes do not close calibration.
- No tuning after outcome inspection without registering a new calibration
  revision.
- No OOS/performance report may imply calibrated execution until the calibration
  packet passes.

## Implemented Tooling

P0.6-006 added:

- calibration row model;
- JSONL table writer/reader;
- summary generator;
- schema/math validation checks;
- synthetic fixture tests for validation logic.

This does not close the gate until real approved quote evidence and manual
verification exist.
