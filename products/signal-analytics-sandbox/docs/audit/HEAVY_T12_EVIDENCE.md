# HEAVY_T12_EVIDENCE

Date: 2026-05-07
Task: T12 Outcome Matching Engine
Rule registry version: 1.0.0

## Fixture Provenance

- Ledger fixture: synthetic `SignalRecord` instances in
  `tests/integration/test_outcome_matcher.py`; fixed timestamps, source_id
  `pilot`, deterministic evidence URLs, and fixed text SHA-256.
- Snapshot fixture: deterministic `PriceSnapshot` values built with
  `make_price_snapshot(...)`; provider_id `operator-file`, provider_status
  `operator_supplied`, fixed as_of/range timestamps, and deterministic Parquet
  OHLCV bytes.
- Reproducibility proof: `test_byte_identical_re_run` compares byte-identical
  outcomes Parquet bytes and SHA-256 values for the same records + snapshot.

## Enumerated Outcome Examples

1. `target_hit`: long BTC signal entry 100, stop 90, target 110; forward OHLCV
   reaches high 111 before stop, producing return_pct `10.000000`.
2. `stop_hit`: long BTC signal entry 100, stop 90, target 110; forward OHLCV
   reaches low 89 before target, producing return_pct `-10.000000`.
3. `timeout_no_hit`: covered by `outcome.long_target_stop.v1`; no target/stop
   hit before range end exits on the final close.
4. `excluded_ambiguous`: flat, unknown, or ambiguity-flagged signals are emitted
   as `excluded_ambiguous` with no numerical return fields.
5. `excluded_no_price`: signal asset absent from the snapshot assets, or without
   forward rows, is emitted as `excluded_no_price`.

## Determinism Notes

- Outcome math uses `Decimal` and banker's rounding to six decimal places before
  Parquet float conversion.
- Outcomes Parquet uses fixed column order, zstd compression, statistics
  disabled, and metadata `rule_registry_version=1.0.0`.
