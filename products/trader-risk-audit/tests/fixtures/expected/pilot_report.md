# Trader Risk Audit Report

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 3
- Violations recorded: 2
- Affected P&L: 78
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 3
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- rule_forbidden_assets: 2

### Worst Violation Days

- 2026-02-03: 2

## Policy

- Schema version: 1
- Account scope: demo
- Rules reviewed: 3
- Rule IDs: rule_forbidden_assets, rule_max_position_size, rule_max_leverage

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| rule_forbidden_assets | 2026-02-03T09:30:00+00:00 | trade_4f729097bd9cfb00 | BTCUSD | BTCUSD | breach | 0 |
| rule_forbidden_assets | 2026-02-03T10:00:00+00:00 | trade_8c0a4df8d36bd9b7 | BTCUSD | BTCUSD | breach | 78 |

## P&L Attribution

- Total P&L: 77
- Compliant P&L: -1
- Violating P&L: 78
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- rule_max_leverage: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
