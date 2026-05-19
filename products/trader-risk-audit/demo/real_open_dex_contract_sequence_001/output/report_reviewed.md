# Trader Risk Audit Report - Real Open DEX Contract-Scoped Sequence Reviewed Copy

Reviewed status: T122 development review complete.

This is real-open-data development rehearsal only. It is not a private trader
export, paid-pilot evidence, PMF evidence, customer validation, market-demand
evidence, proof that traders will pay, trading advice, or live trading control.

Material limitations preserved:

- source rows are Uniswap V2 WETH/USDC pair-level swap logs filtered by a
  repeated public contract recipient, not one verified trader account ledger;
- `account_id` is a safe contract-recipient-scope label, not a wallet or
  customer id;
- side is derived relative to WETH and does not represent verified trader
  intent;
- fees are set to `0` only as a canonical schema placeholder; gas, LP fees, and
  all-in user execution costs are unsupported;
- P&L attribution is an audit-engine rehearsal calculation on transformed rows,
  not verified trader-realized P&L;
- leverage, margin, account balances, deposits, withdrawals, and private rules
  are unsupported.

# Trader Risk Audit Report

This audit is not investment advice and does not control live trading.

## Executive Summary

- Rules reviewed: 2
- Violations recorded: 0
- Affected P&L: 0
- Selected policy profile: custom/unspecified

## Summary

- Trades reviewed: 40
- Accounts reviewed: 1
- Source files: trades.csv

### Repeated Patterns

- None

### Worst Violation Days

- None

## Policy

- Schema version: 1
- Account scope: real_open_uniswap_v2_contract_recipient_scope
- Rules reviewed: 2
- Rule IDs: real_open_contract_max_position_size, real_open_contract_max_leverage_unsupported

## Violations

No deterministic violations were recorded.

## P&L Attribution

- Total P&L: 0
- Compliant P&L: 0
- Violating P&L: 0
- Unclassified P&L: 0
- Reconciliation delta: 0

## Limitations

- real_open_contract_max_leverage_unsupported: unsupported_leverage_data (leverage)

## Next Review

- Review any unresolved unsupported-data limitations.
- Confirm policy thresholds before report delivery.
- Re-run the audit after rule or export changes.
