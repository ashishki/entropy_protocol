# Trader Risk Audit Report - Synthetic Risk Audit Reviewed Copy

Reviewed status: T102 manual review complete.

This is artifact-quality validation only. It is not paid-pilot evidence, PMF
evidence, customer validation, or proof that traders will pay. The fixture is
synthetic and represents no real trader, broker account, or private export.

Material limitations preserved:

- findings are useful for deterministic rule and P&L-attribution coverage only;
- synthetic account label `demo_case_001` is not a real account id;
- the report must not be presented as market demand or customer outcome proof.

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 4
- Violations recorded: 13
- Affected P&L: 121
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 10
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- demo_cooldown_after_loss: 5
- demo_forbidden_asset: 2
- demo_max_daily_loss: 4
- demo_max_position_size: 2

### Worst Violation Days

- 2026-03-02: 11
- 2026-03-03: 2

## Policy

- Schema version: 1
- Account scope: demo_case_001
- Rules reviewed: 4
- Rule IDs: demo_max_daily_loss, demo_cooldown_after_loss, demo_forbidden_asset, demo_max_position_size

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| demo_cooldown_after_loss | 2026-03-02T10:10:00+00:00 | trade_d506c3bffc379ac5 | 2026-03-02T10:10:00+00:00 | 2026-03-02T10:40:00+00:00 | breach | -2 |
| demo_max_daily_loss | 2026-03-02T10:10:00+00:00 | trade_d506c3bffc379ac5 | 21 | 15 | breach | -2 |
| demo_cooldown_after_loss | 2026-03-02T10:20:00+00:00 | trade_3bdc690db1ae5140 | 2026-03-02T10:20:00+00:00 | 2026-03-02T10:40:00+00:00 | breach | 8 |
| demo_max_daily_loss | 2026-03-02T10:20:00+00:00 | trade_3bdc690db1ae5140 | 21 | 15 | breach | 8 |
| demo_cooldown_after_loss | 2026-03-02T10:35:00+00:00 | trade_d3cdbab4658565b9 | 2026-03-02T10:35:00+00:00 | 2026-03-02T10:40:00+00:00 | breach | -3 |
| demo_forbidden_asset | 2026-03-02T10:35:00+00:00 | trade_d3cdbab4658565b9 | BTCUSD | BTCUSD | breach | -3 |
| demo_max_daily_loss | 2026-03-02T10:35:00+00:00 | trade_d3cdbab4658565b9 | 21 | 15 | breach | -3 |
| demo_max_position_size | 2026-03-02T10:35:00+00:00 | trade_d3cdbab4658565b9 | 42000 | 10000 | breach | -3 |
| demo_forbidden_asset | 2026-03-02T10:50:00+00:00 | trade_3e24765be0d593da | BTCUSD | BTCUSD | breach | 117 |
| demo_max_daily_loss | 2026-03-02T10:50:00+00:00 | trade_3e24765be0d593da | 21 | 15 | breach | 117 |
| demo_max_position_size | 2026-03-02T10:50:00+00:00 | trade_3e24765be0d593da | 42120 | 10000 | breach | 117 |
| demo_cooldown_after_loss | 2026-03-03T10:05:00+00:00 | trade_abb4564445f9bddb | 2026-03-03T10:05:00+00:00 | 2026-03-03T10:43:00+00:00 | breach | -1 |
| demo_cooldown_after_loss | 2026-03-03T10:30:00+00:00 | trade_dd75227b6cbc59b7 | 2026-03-03T10:30:00+00:00 | 2026-03-03T10:43:00+00:00 | breach | 2 |

## P&L Attribution

- Total P&L: 47
- Compliant P&L: -74
- Violating P&L: 121
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

No unsupported-data limitations were recorded.

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
