# SimBroker Calibration Candidate Row Plan

Date: 2026-05-05
Status: IMPLEMENTED_NOT_GATE_EVIDENCE

## Scope

Define and implement the safe path for turning real SimBroker fill logs and
approved public quote snapshots into manually verified calibration rows.

## Implemented Path

Code:

- `entropy/simbroker/calibration.py::build_calibration_row_from_fill`

Inputs:

- real `FillLog` from SimBroker;
- approved `BidAskQuote`;
- approved quote source identifier;
- raw quote source hash;
- manual verifier identifier;
- manual verification timestamp;
- optional OHLCV bar fields;
- quote timestamp tolerance.

Output:

- one validated `CalibrationRow` with method `SB-CAL-15PCT-v1`;
- `evidence_claim=not_phase_gate_approval`;
- buy rows reference ask;
- sell rows reference bid;
- deviation and 15% pass flag computed deterministically;
- stale quote matches are excluded with `quote_timestamp_outside_tolerance`.

## Acceptance Boundary

This plan does not close SimBroker calibration. To close the Phase 0 calibration
criterion, a future packet must include:

- >=100 included calibration rows;
- real SimBroker fill logs;
- approved quote sources and raw source hashes;
- manual verification notes;
- representative assets;
- no post-hoc tuning after deviation outcomes are visible.

## Verification

Tests:

- `tests/unit/test_simbroker.py::test_build_calibration_row_from_fill_uses_side_reference_and_cost_fields`
- `tests/unit/test_simbroker.py::test_build_calibration_row_from_fill_excludes_stale_quote_without_failing`
- `tests/unit/test_simbroker.py::test_build_calibration_row_from_fill_rejects_symbol_mismatch`

## Next Step

Start P0.7-020: SimBroker Calibration Packet Assembly Dry Run. Use fixture fill
logs and fixture quotes to verify packet assembly mechanics end-to-end while
keeping all generated rows marked as non-gate fixtures.
