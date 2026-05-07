# Trader Risk Audit Report

This audit is not investment advice and does not control live trading.

## Summary

- Trades reviewed: 4
- Accounts reviewed: 1
- Source files: attribution_overlap.csv

### Repeated Patterns

- rule_forbidden_assets: 1
- rule_max_position_size: 1

### Worst Violation Days

- 2026-01-15: 2

## Policy

- Schema version: 1
- Account scope: acct_demo_001
- Rules reviewed: 3
- Rule IDs: rule_forbidden_assets, rule_max_position_size, rule_max_leverage

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| rule_forbidden_assets | 2026-01-15T10:00:00+00:00 | trade_e954700b528bf5b4 | BTCUSD | test | breach | 99 |
| rule_max_position_size | 2026-01-15T10:00:00+00:00 | trade_e954700b528bf5b4 | BTCUSD | test | breach | 99 |

## P&L Attribution

- Total P&L: 98
- Compliant P&L: -1
- Violating P&L: 99
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- rule_max_leverage: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
