# Phase 36 Development Loop - Three-Channel Impact Evaluation

Date: 2026-05-22
Status: active_loop_plan

## Goal

Run the same evidence-completion and impact-scoring loop for:

- `bablos79`
- `nemphiscrypts`
- `pifagortrade`

Then compare what we actually learned across channels using both strict market
metrics and broader impact dimensions.

## Development Loop

### Step 1 - Source Coverage

For each channel:

- define the time window;
- list captured text rows;
- list missing periods and missing message IDs;
- list source-linked audio/image/chart artifacts;
- classify gaps as captured, deleted, unavailable, media-only, or blocked.

Output:

- per-channel corpus completion plan;
- cross-channel coverage table.

### Step 2 - Multimodal Intake

For each channel:

- text is hashed and tied to source URL/timestamp;
- audio is transcribed, then human/operator accepted or rejected;
- images/charts are OCR/vision draft only after source linkage;
- chart interpretation requires human/operator review.

Output:

- media linkage queue;
- transcript acceptance artifact;
- OCR draft artifact.

### Step 3 - Claim And Idea Normalization

Extract and review:

- explicit trade setups;
- directional bias;
- target/level calls;
- trend/regime calls;
- macro/event thesis;
- risk-management statements;
- methodology/process statements;
- watchlists;
- non-market commentary.

Output:

- normalized claim/idea ledger with review state;
- false-positive/false-negative review summary.

### Step 4 - Truth Mapping

For every reviewed item, decide what can be truth-tested:

- explicit setup -> entry/stop/target/outcome rules;
- directional call -> standardized horizon return;
- trend/regime call -> benchmark/regime proxy;
- target call -> target touch within horizon;
- risk statement -> methodology/risk evidence, not PnL;
- broad insight -> evidence-backed qualitative score, confidence-limited.

Output:

- provider/proxy map;
- truth-test method per claim;
- exclusion reasons.

### Step 5 - Impact Scoring

Score each channel separately on:

- signal performance;
- trend sense;
- insight depth;
- trading methodology;
- risk management;
- practical usefulness;
- creativity/differentiation;
- evidence confidence.

Output:

- dashboard-ready scorecard;
- confidence labels;
- paid-report evidence appendix.

### Step 6 - Cross-Channel Comparison

Compare channels only after each has passed the same loop.

Allowed comparison:

- "higher measurable signal count";
- "better evidence confidence";
- "stronger trend-sense evidence";
- "more complete risk discipline";
- "blocked by media/source gaps".

Disallowed comparison:

- universal "best channel";
- future-profit claims;
- investment recommendation;
- ranking without confidence/sample-size caveat.

## Current Channel State

| Channel | Current state | Next action |
|---|---|---|
| `bablos79` | Phase 36 gap documented; text recapture plan exists. | Build media linkage queue and execute/record text recapture results. |
| `nemphiscrypts` | V1 metrics exist but no Phase 36 completion pass yet. | Create corpus/media completion scope using the same template. |
| `pifagortrade` | V1 metrics exist but no Phase 36 completion pass yet. | Create corpus/media completion scope using the same template. |

## Dashboard vs Paid Report

Dashboard:

- show compact dimension scores;
- show confidence;
- show sample size;
- show external gate;
- show selected safe examples.

Paid deep report:

- explain why the scores exist;
- show source-backed examples and counterexamples;
- expose methodology/risk/insight evidence;
- include limitations and blocked claims;
- include full evidence appendix where allowed.

## Immediate Next Tasks

1. Finish `bablos79` media linkage queue.
2. Create equivalent corpus completion scopes for `nemphiscrypts` and
   `pifagortrade`.
3. Expand claim taxonomy so trend sense, insight depth, methodology, risk
   management, and creativity are first-class reviewed items.
4. Define dashboard score schema with confidence and paid-report boundary.
