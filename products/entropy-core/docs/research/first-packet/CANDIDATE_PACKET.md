# First Research Candidate Packet

Status: CANDIDATE_ONLY_NOT_REGISTERED
Schema version: first-research-candidate/v1
Candidate id: FRC-001-VC-BREAKOUT-CONTINUATION
Hypothesis family: Volatility Compression
Scope: archive-only BTC local fixture bars; no holdout, live feed, broker, exchange, production, capital-ready, or OOS/performance surface
Required gate: human_registration_required
Evaluation status: not_evaluated

## Hypothesis

When a liquid BTC archive bar sequence shows 20-bar realized volatility compression followed by an upside close beyond the prior 10-bar high, the next archive evaluation window should exhibit higher net stream-a-minus-cost outcome than an always-flat baseline under the preregistered no-claim harness.

## Frozen Parameters

| Name | Value | Rationale |
|------|-------|-----------|
| compression_window_bars | 20 | Freezes the realized-volatility lookback before any evaluation run. |
| breakout_window_bars | 10 | Freezes the prior-high breakout reference before hash binding. |
| holding_window_bars | 5 | Freezes the archive evaluation holding horizon for the first packet. |

## Readiness Fields

- Primary metric: net_stream_a_minus_cost_status
- Baseline comparator: always_flat_archive_baseline
- Minimum sample requirement: at least 30 archive fixture candidate events before any summary
- Invalidation condition: Reject as not ready if leakage checks fail, required hashes are missing, or sample count is below the frozen minimum.

## Leakage Risks

- post-hoc threshold tuning after inspecting evaluation output
- look-ahead from using future bars in compression or breakout labels
- reuse of calibration information across future holdout boundaries

## Hash Placeholders

- dataset_hash: PENDING_T16_DATASET_HASH_BINDING
- code_hash: PENDING_T17_CODE_HASH_BINDING
- policy_hash: PENDING_T17_POLICY_HASH_BINDING
- parameter_hash: PENDING_T15_PARAMETER_HASH_BINDING

## No-Claim Labels

- archive_only_candidate
- human_registration_required
- not_evaluated
- not_holdout_unlock
- not_oos_performance
- not_phase_gate_approval
- not_production
- not_capital_ready
- not_live_feed
- not_broker_exchange

## Requested Surfaces

- archive_local_fixture
