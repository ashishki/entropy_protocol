# Trader Risk Audit Report - Public Sample Reviewed Copy

Reviewed status: T102 manual review complete.

This is artifact-quality validation only. It is not paid-pilot evidence, PMF
evidence, customer validation, or proof that traders will pay. The fixture is a
public-like derived sample for internal report-quality review.

Material limitations preserved:

- source rows are compact public-like examples, not a private customer ledger;
- affected P&L can remain `0` on violation rows when the flagged rows are not
  the realized closing rows;
- the `hard` starter profile is a stress-test preset, not advice or an optimal
  risk setting.

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 5
- Violations recorded: 9
- Affected P&L: 0
- Selected policy profile: hard

## Summary

- Trades reviewed: 4
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- public_sample_hard_cooldown_after_loss: 2
- public_sample_hard_forbidden_assets: 1
- public_sample_hard_max_daily_loss: 2
- public_sample_hard_max_drawdown: 2
- public_sample_hard_max_position_size: 2

### Worst Violation Days

- 2026-02-03: 9

## Policy

- Schema version: 1
- Account scope: acct_public_sample_001
- Rules reviewed: 5
- Rule IDs: public_sample_hard_max_daily_loss, public_sample_hard_max_drawdown, public_sample_hard_cooldown_after_loss, public_sample_hard_max_position_size, public_sample_hard_forbidden_assets

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| public_sample_hard_cooldown_after_loss | 2026-02-03T10:10:00+00:00 | trade_fcdefbab78fa75d6 | 2026-02-03T10:10:00+00:00 | 2026-02-03T11:00:00+00:00 | breach | 0 |
| public_sample_hard_forbidden_assets | 2026-02-03T10:10:00+00:00 | trade_fcdefbab78fa75d6 | RISKY | RISKY | breach | 0 |
| public_sample_hard_max_daily_loss | 2026-02-03T10:10:00+00:00 | trade_fcdefbab78fa75d6 | 4000 | 1000 | breach | 0 |
| public_sample_hard_max_drawdown | 2026-02-03T10:10:00+00:00 | trade_fcdefbab78fa75d6 | 4000 | 3000 | breach | 0 |
| public_sample_hard_max_position_size | 2026-02-03T10:10:00+00:00 | trade_fcdefbab78fa75d6 | 12500 | 10000 | breach | 0 |
| public_sample_hard_cooldown_after_loss | 2026-02-03T10:20:00+00:00 | trade_e2e7f893f961653e | 2026-02-03T10:20:00+00:00 | 2026-02-03T11:00:00+00:00 | breach | 0 |
| public_sample_hard_max_daily_loss | 2026-02-03T10:20:00+00:00 | trade_e2e7f893f961653e | 4000 | 1000 | breach | 0 |
| public_sample_hard_max_drawdown | 2026-02-03T10:20:00+00:00 | trade_e2e7f893f961653e | 4000 | 3000 | breach | 0 |
| public_sample_hard_max_position_size | 2026-02-03T10:20:00+00:00 | trade_e2e7f893f961653e | 12000 | 10000 | breach | 0 |

## P&L Attribution

- Total P&L: -4000
- Compliant P&L: -4000
- Violating P&L: 0
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

No unsupported-data limitations were recorded.

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
