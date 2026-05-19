# Trader Risk Audit Report - Synthetic Leverage Limitation Reviewed Copy

Reviewed status: T102 manual review complete.

This is artifact-quality validation only. It is not paid-pilot evidence, PMF
evidence, customer validation, or proof that traders will pay. The fixture is
synthetic and exists to prove the workflow preserves unsupported-data
limitations.

Material limitations preserved:

- no deterministic violations are expected for this pack;
- max leverage is unsupported because the CSV has no leverage field;
- the report must not infer leverage or hide the limitation to look stronger.

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 2
- Violations recorded: 0
- Affected P&L: 0
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 2
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- None

### Worst Violation Days

- None

## Policy

- Schema version: 1
- Account scope: synthetic_limit_leverage_001
- Rules reviewed: 2
- Rule IDs: synthetic_limit_max_leverage, synthetic_limit_max_position_size

## Violations

No deterministic violations were recorded.

## P&L Attribution

- Total P&L: 26
- Compliant P&L: 26
- Violating P&L: 0
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- synthetic_limit_max_leverage: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
