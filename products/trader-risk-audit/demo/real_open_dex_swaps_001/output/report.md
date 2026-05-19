# Trader Risk Audit Report

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 2
- Violations recorded: 8
- Affected P&L: -6.85913150435952
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 40
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- real_open_max_position_size: 8

### Worst Violation Days

- 2026-05-19: 8

## Policy

- Schema version: 1
- Account scope: real_open_uniswap_v2_weth_usdc_pair_scope
- Rules reviewed: 2
- Rule IDs: real_open_max_position_size, real_open_max_leverage_unsupported

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| real_open_max_position_size | 2026-05-19T06:38:59+00:00 | trade_4f95b0f9e4741224 | 1184.5716759665697 | 1000 | breach | 0 |
| real_open_max_position_size | 2026-05-19T06:39:11+00:00 | trade_5d59a5dde69ce37e | 1436.3095461627806 | 1000 | breach | 0 |
| real_open_max_position_size | 2026-05-19T06:39:23+00:00 | trade_f98c0ff1644ce333 | 1797.085756287398 | 1000 | breach | 0 |
| real_open_max_position_size | 2026-05-19T07:09:23+00:00 | trade_93d33dfc45b56225 | 2394.74503649139552 | 1000 | breach | 0 |
| real_open_max_position_size | 2026-05-19T07:10:23+00:00 | trade_cc3fb1063a40a20b | 1499.99662087334702 | 1000 | breach | -6.85913150435952 |
| real_open_max_position_size | 2026-05-19T07:39:11+00:00 | trade_689fb7516c928276 | 2428.79649624949422 | 1000 | breach | 0 |
| real_open_max_position_size | 2026-05-19T07:43:11+00:00 | trade_ca3861923de84d9e | 2334.68603753634076 | 1000 | breach | 0 |
| real_open_max_position_size | 2026-05-19T07:48:11+00:00 | trade_9a6867e86b900c51 | 1608.02476393183476 | 1000 | breach | 0 |

## P&L Attribution

- Total P&L: -11.06072931038785
- Compliant P&L: -4.20159780602833
- Violating P&L: -6.85913150435952
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- real_open_max_leverage_unsupported: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
