# Trader Risk Audit Report

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 3
- Violations recorded: 7
- Affected P&L: 0
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 6
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- sec_form4_max_transaction_notional_proxy: 5
- sec_form4_watchlist_symbol_svre: 2

### Worst Violation Days

- 2026-03-11: 2
- 2026-03-12: 3
- 2026-03-16: 1
- 2026-03-18: 1

## Policy

- Schema version: 1
- Account scope: acct_open_sec_form4_msk_001
- Rules reviewed: 3
- Rule IDs: sec_form4_max_transaction_notional_proxy, sec_form4_watchlist_symbol_svre, sec_form4_leverage_unsupported_register

## Violations

| Rule ID | Timestamp | Source Row IDs | Evaluated Value | Threshold | Severity | P&L Impact |
| --- | --- | --- | --- | --- | --- | --- |
| sec_form4_max_transaction_notional_proxy | 2026-03-11T00:00:00+03:00 | sec_000173112226000397_8924105 | 688735872 | 1000000 | breach | 0 |
| sec_form4_watchlist_symbol_svre | 2026-03-11T00:00:00+03:00 | sec_000173112226000397_8924105 | SVRE | SVRE | breach | 0 |
| sec_form4_max_transaction_notional_proxy | 2026-03-12T00:00:00+03:00 | sec_000114036126009622_8924543 | 2152903500 | 1000000 | breach | 0 |
| sec_form4_max_transaction_notional_proxy | 2026-03-12T00:00:00+03:00 | sec_000173112226000397_8924106 | 230219280 | 1000000 | breach | 0 |
| sec_form4_watchlist_symbol_svre | 2026-03-12T00:00:00+03:00 | sec_000173112226000397_8924106 | SVRE | SVRE | breach | 0 |
| sec_form4_max_transaction_notional_proxy | 2026-03-16T00:00:00+03:00 | sec_000162828026018929_8928326 | 8320500 | 1000000 | breach | 0 |
| sec_form4_max_transaction_notional_proxy | 2026-03-18T00:00:00+03:00 | sec_000153983826000058_8932299 | 1130100 | 1000000 | breach | 0 |

## P&L Attribution

- Total P&L: 0
- Compliant P&L: 0
- Violating P&L: 0
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- sec_form4_leverage_unsupported_register: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
