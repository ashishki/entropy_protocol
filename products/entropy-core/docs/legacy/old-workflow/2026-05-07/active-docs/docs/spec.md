# Feature Specification — Entropy Protocol

Version: 1.0
Date: 2026-05-01
Status: Active

---

## Overview

Entropy Protocol provides a governed systematic capital-allocation research framework for a solo researcher/operator. Its primary function is to build leakage-resistant, auditable evaluation infrastructure before any trading-edge claim is made. The system enforces strict separation between in-sample (IS) and out-of-sample (OOS) data, preregistration of all trial specifications before data examination, deterministic four-stream P&L attribution, and a governance state machine with human-gated phase transitions. The v1 milestone (Phase 0) is complete when all evaluation infrastructure is operational with machine-checkable evidence and a leakage audit that passes — no live capital is deployed and no OOS performance claims are made in this phase.

### Current Post-Phase-1A Status

T01-T24 are implemented and verified as the foundation baseline. Archive-only
evidence hardening and Phase 1A archive-only baseline planning/instrumentation
are complete through scaffold/probe closure. Current work is post-Phase-1A
audit readiness and current-state sync.

Closed Phase 1A foundation surfaces:

- archive dataset freeze and split registration;
- non-executable baseline specification registration;
- executable non-trading scaffold;
- mechanics-only probe with no strategy metric fields;
- prompt metadata refresh and post-Phase-1A deep review.

No full Phase 1 evaluation/trading, archive holdout read, live feed, broker
integration, Growth/RDL/RBE activation, non-Python runtime/toolchain
introduction, OOS/performance claim, live capital decision, or phase-gate
approval is authorized by the current implementation baseline.

---

## User Roles

| Role | Description |
|------|-------------|
| Solo researcher/operator | Single user who registers trials, ingests data, runs walk-forward evaluations, inspects results, and approves phase gates. All human approval boundaries are gated on this role. No external authentication in v1. |

---

## Feature Areas

---

### 1. Trial Registry

#### Description

The Trial Registry is the preregistration system for all trial specifications. A trial spec must be registered — and all hashes must be locked — before any data from the evaluation window is examined. The registry is append-only: no UPDATE or DELETE is permitted on `trial_registry` or `governance_events` tables. Each trial belongs to a hypothesis family, enabling multiplicity tracking. Trial count per family is visible at all times.

#### Acceptance Criteria

1. A TrialSpec submitted to the write path with all required fields and all hashes present is accepted and assigned a unique TrialID; the record is INSERTed into `trial_registry` with status PENDING.
2. A TrialSpec submitted without at least one of `dataset_hash`, `code_hash`, or `policy_hash` is rejected with a structured error listing the missing fields; no DB write occurs.
3. A TrialSpec with a duplicate `trial_id` is rejected with a DuplicateTrialError; no DB write occurs.
4. The Experiment Readiness Gate returns READY when a registered trial has: all required spec fields populated, family tag assigned, all three hashes present, and no duplicate trial ID.
5. The Experiment Readiness Gate returns a list of named failures when any required field is absent, family tag is missing, or any hash is missing.
6. Human approval (a GovernanceEvent of type APPROVAL) is required before a trial transitions to READY status; the transition without a matching approval event is blocked in code.
7. The read path returns a TrialSpec by trial_id; returns a list of trials by family tag; returns a list by status.
8. The trial-count-per-family query returns the correct count of all registered trials in a family, including PENDING and READY entries.
9. All writes to `trial_registry` and `governance_events` are INSERT-only; any UPDATE or DELETE attempted through the application layer raises a RegistryMutationError.

#### Out of Scope for v1

- Web UI for trial registration
- Bulk import of trial specs
- Automated trial approval (all approvals are human-recorded)
- Harvey-Liu trial count tracking beyond family count (full cross-namespace count is a Phase 1+ concern)

---

### 2. Data Pipeline

#### Description

The data pipeline ingests OHLCV market data, validates quality, and stores versioned Parquet files. The DataProvider abstraction enforces a provider-neutral boundary — no hard-coded provider. The local fixture adapter uses CSV/Parquet fixture files for Phase 0. Every dataset ingested has its hash recorded in the DB alongside provenance metadata.

#### Acceptance Criteria

1. The DataProvider abstract base class defines `fetch_ohlcv`, `list_symbols`, and `check_health` as abstract methods; any concrete implementation that does not implement all three raises TypeError at instantiation.
2. The local fixture adapter reads OHLCV data from local CSV or Parquet files and writes versioned Parquet to `ENTROPY_DATA_DIR/market/`; the output file is readable by Polars and has the correct schema.
3. After ingestion, the dataset hash (SHA-256 of sorted rows + schema fingerprint) is recorded in the DB in the same transaction as the provenance record; if either write fails, the transaction rolls back.
4. The data quality check raises TimestampNormalizationError when OHLCV bars contain timestamps not in UTC.
5. The data quality check raises GapDetectionError when the gap between consecutive bars exceeds the configured `max_gap_seconds`.
6. The data quality check raises OHLCVSanityError when any of the following are true: close price ≤ 0, volume < 0, high < max(open, close), low > min(open, close).
7. A DataQualityReport is returned with per-check PASS/FAIL results and the count of affected bars for each failure type.
8. The DataIngestionError hierarchy includes DataProviderError, DataQualityError, TimestampNormalizationError, GapDetectionError, OHLCVSanityError.
9. The provider registry maps provider names to DataProvider implementations; requesting an unregistered provider raises ProviderNotFoundError.

#### Out of Scope for v1

- Live data provider adapters (Binance, Kaiko, CCData)
- Real-time streaming ingestion
- Incremental Parquet append (full write per ingestion in Phase 0)
- Data lineage graph beyond provenance record in DB
- Phase 0 90-day stability closure; `products/entropy-core/docs/audit/archive/p0_5/DATA_STABILITY_PLAN.md` defines
  the future evidence packet, but no provider is active and no monitoring
  evidence exists yet

---

### 3. SimBroker

#### Description

SimBroker is a deterministic execution simulation engine. Given a strategy signal, OHLCV bar, and cost model parameters, it produces a FillLog entry with exact cost breakdown. All formulas are tested with worked examples. Fills are constrained to the bar's high-low range. No lookahead is used.

#### Acceptance Criteria

1. The cost model computes the total fill cost as the sum of: fixed commission + percentage commission + slippage (linear model) + square-root market impact; given the same inputs, the output is identical across any number of invocations.
2. Given a worked example with known parameters (commission=0.08%, slippage=0.02%, impact=0.02%, fill price within bar range), the computed total cost matches the expected value within floating-point tolerance.
3. The fill engine rejects a fill where the proposed fill price is outside the bar's [low, high] range; the fill is constrained to the bar boundary and a FillLog is produced with `constrained=True`.
4. The fill engine produces a FillLog entry for every accepted fill; the FillLog includes: timestamp, symbol, side, quantity, fill_price, commission, slippage, market_impact, borrow_rate, funding_rate, total_cost, constrained.
5. Given the same signal, OHLCV bar, and cost model configuration, the fill engine produces byte-identical FillLog output on two separate invocations (determinism test).
6. The borrow/funding rate hooks accept a rate of zero (no borrow/funding) and a positive rate; both produce valid FillLog entries with the correct cost component.
7. The BidAskProvider stub implements the abstract interface; its no-op mock returns None for all methods and passes all unit tests.
8. The BidAskProvider abstract interface defines `get_bid_ask` as an abstract method; the no-op mock returns None without raising.

#### Out of Scope for v1

- Live broker API integration
- Real bid/ask calibration from broker data (stub only in Phase 0)
- Order routing simulation
- Partial fills
- Phase 0 calibration closure; `products/entropy-core/docs/audit/archive/p0_5/SIMBROKER_CALIBRATION_PLAN.md`
  defines the future >=100-fill evidence packet, but no provider is active and
  no calibration evidence exists yet

---

### 4. Walk-Forward Harness

#### Description

The walk-forward harness enforces strict IS/OOS time separation with configurable embargo bands. The IS/OOS splitter purges N bars before the OOS start. The leakage detection checklist runs machine-checkable audits. The walk-forward runner orchestrates the full pipeline and records reproducible RunRecords.

#### Acceptance Criteria

1. The IS/OOS splitter returns IS and OOS windows where the last IS bar timestamp is strictly before the first OOS bar timestamp minus the embargo band; no IS bar has a timestamp within the embargo band.
2. Given a dataset with a known OOS start and embargo of N bars, the splitter excludes exactly N bars before the OOS start from both windows.
3. The splitter raises LeakageError if any feature value in the IS window was computed using data timestamped after the IS cutoff.
4. The leakage detection checklist reports FAIL for normalization leakage when a feature is computed on the full series including OOS bars.
5. The leakage detection checklist reports FAIL for regime label look-ahead when a regime label is assigned using data after the OOS start timestamp.
6. The leakage detection checklist reports FAIL for universe selection bias when symbol selection uses return data from the OOS period.
7. The leakage detection checklist reports FAIL for within-window optimization when parameters are re-fitted inside the OOS window.
8. The LeakageReport contains a PASS/FAIL verdict per check, a description of each failure, and the total check count.
9. The walk-forward runner produces a RunRecord that includes: trial_id, dataset_hash, code_hash, policy_hash, simbroker_version, IS start/end, OOS start/end, embargo_bars, leakage_report_status; the RunRecord is written to the `runs` table.
10. A RunRecord without all four hashes (dataset_hash, code_hash, policy_hash, simbroker_version) is rejected by the runner with an IncompleteRunRecordError before any DB write.

#### Out of Scope for v1

- Rolling walk-forward (multiple IS/OOS folds); Phase 0 implements a single split
- Parallel walk-forward runs
- Online parameter optimization inside the IS window
- Final Phase 1 OOS purge/embargo methodology; D-023 keeps the current N-bar
  embargo as scaffold-only until derived methodology exists

---

### 5. P&L Attribution

#### Description

The P&L Attribution Engine decomposes all trade returns into exactly four streams per protocol spec NN-2. Net Sharpe is computed ONLY from streams (a)+(b)+(c). Stream (d) carry is reported separately and never included in the primary metric. All formulas are tested with worked examples.

#### Acceptance Criteria

1. Given a list of FillLog entries, the engine computes stream (a) long-only gross returns as the sum of PnL from long entries and exits only.
2. Given a list of FillLog entries, the engine computes stream (b) overlay strategy returns as the PnL attributable to the overlay signals (net of long-only baseline).
3. Given a list of FillLog entries, the engine computes stream (c) cost drag as the sum of all SimBroker cost components (commission + slippage + market impact + borrow).
4. Given a list of FillLog entries, the engine computes stream (d) carry/funding as the sum of funding rate charges, reported separately from (a)(b)(c).
5. Net Sharpe is computed as mean(annual returns from (a)+(b)+(c)) / stdev(annual returns from (a)+(b)+(c)); stream (d) is never passed to the net Sharpe computation function.
6. Given a worked example with known streams and known expected net Sharpe, the engine output matches the expected value within floating-point tolerance.
7. A DrawdownRecord is produced for each drawdown event; it contains: start_timestamp, end_timestamp, peak_value, trough_value, drawdown_pct, recovery_timestamp (or None if not recovered).
8. PerformanceMetrics aggregates: net Sharpe, max drawdown, Calmar ratio, N_eff (stub), Harvey-Liu deflated Sharpe (stub); all fields are populated or explicitly None with a reason code.
9. The PnLStreams object enforces that streams (a), (b), (c), (d) are stored in separate fields and cannot be implicitly combined; accessing `net_sharpe_streams` returns only (a)+(b)+(c).

#### Out of Scope for v1

- Real-time P&L streaming
- Multi-currency P&L (single currency in Phase 0)
- Brier score attribution for CCA-influenced signals

---

### 6. Governance State Machine

#### Description

The governance state machine implements the P1 drawdown circuit breaker and the P3 correlation trigger. P1 trips at the drawdown threshold, blocks new trades while active, and resets on recovery. P3 fires at the IC_long threshold with a cooldown period. All state transitions are logged as GovernanceEvents.

#### Acceptance Criteria

1. The P1 circuit breaker trips when realized drawdown from the high-water mark reaches or exceeds the configured threshold (12% per protocol spec); after tripping, `is_p1_active()` returns True.
2. While P1 is active, `can_open_new_position()` returns False; when P1 is inactive, it returns True.
3. The P1 circuit breaker resets when the high-water mark gap falls below the recovery threshold (8%) AND at least 5 business days have elapsed since the trip; after reset, `is_p1_active()` returns False.
4. Two consecutive P1 trip calls with the same state produce the same outcome as one call (idempotency).
5. The P1 circuit breaker correctly handles the boundary condition: drawdown exactly at the threshold (≥12%) trips P1; drawdown just below (11.99%) does not trip.
6. The P3 correlation trigger fires when the 20-day rolling average pairwise correlation exceeds the configured IC_long threshold (0.55 per protocol spec); after firing, `is_p3_active()` returns True.
7. The P3 trigger enforces a cooldown period: once fired, it does not fire again until both the correlation falls below 0.45 (hysteresis band) AND the cooldown period elapses.
8. Every state transition (P1 trip, P1 reset, P3 fire, P3 clear) produces a GovernanceEvent with: event_type, timestamp, prior_state, next_state, reason_code, policy_hash.
9. GovernanceEvents are written as INSERT-only to `governance_events`; no UPDATE or DELETE is attempted.
10. A synthetic test suite covers: P1 trip, P1 reset, P3 fire, P3 clear, P1+P3 concurrent, idempotency, boundary conditions at exact threshold values.

#### Out of Scope for v1

- P2 funding exit trigger (crypto perp only; Phase 3+)
- P4 weekly regime overlay (Phase 2+)
- RBE step transitions (locked until Phase 1 exit)
- Automated recovery actions (circuit breaker logs events; position management is out of scope)

---

### 7. Phase Gate Evidence

#### Description

The phase gate evidence system generates reproducible evaluation reports and collects leakage audit evidence. A report for a given trial_id fetches all relevant registry data, hashes, and run records, then renders a reproducible Markdown document. The EVIDENCE_INDEX is updated whenever the leakage checklist passes on a registered run.

Current post-Phase-1A boundary: report helpers and Phase 1A packets produce
implementation/foundation evidence only and default phase gates to
`NOT_APPROVED` unless explicit human approval exists. They do not authorize
Phase 1 evaluation/trading, holdout reads, live feeds, Growth/RDL/RBE
activation, non-Python runtime/toolchain introduction, OOS/performance claims,
production labels, or capital-ready labels.

#### Acceptance Criteria

1. The evaluation report generator produces a Markdown report for a given trial_id that includes: trial_id, trial spec fields, dataset_hash, code_hash, policy_hash, IS/OOS window, leakage report status, and net Sharpe (or "not yet computed" if not available).
2. Two invocations of the report generator for the same trial_id with identical DB state produce byte-identical Markdown output.
3. The leakage audit evidence collector runs the T19 leakage checklist on all RunRecords for a given trial_id and appends a row to EVIDENCE_INDEX with: trial_id, run_id, check date, per-check verdicts, overall status.
4. The Phase 0 gate report lists all T01–T24 tasks with their test file paths and PASS/FAIL status based on whether the test function exists and passes.
5. The evidence collector raises EvidenceCollectionError if any run for the given trial_id has no LeakageReport; partial evidence is not accepted.

#### Out of Scope for v1

- HTML or PDF report output
- Automated email/notification of reports
- Phase 1+ exit artifact generation (KPI dashboards, Sharpe CI charts)
- Automatic phase-gate approval or any conversion of provisional helper output
  into OOS/performance claims
