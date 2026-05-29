# Trader Risk Audit Report - SEC Form 4 Open Source Validation

This audit is not investment advice and does not control live trading.

## Operator Summary

- What was audited: six sanitized SEC EDGAR Form 4 non-derivative transaction
  rows from 2026 Q1.
- Why this report exists: artifact validation for traceability,
  reproducibility, and claim safety before using private customer data.
- Scope label: open-source artifact validation, not customer evidence, paid
  pilot evidence, PMF evidence, or a view on any issuer.
- Timezone: Europe/Moscow, UTC+03:00.
- Account label: `acct_open_sec_form4_msk_001`.
- Strongest finding: five rows exceeded the 1000000 USD transaction-notional
  proxy threshold.
- Watchlist finding: two rows matched the validation-only `SVRE` watchlist
  symbol.
- Material limitation: this source is not an account ledger, so P&L, daily
  loss, drawdown, leverage, balances, and trading intent are unsupported.
- External delivery status: hold until operator approves the T67 reviewed
  report and delivery packet.

## Reviewed Artifacts

- Source fixture: `demo/open_source_sec_form4_001/trades.csv`
- Policy: `demo/open_source_sec_form4_001/policy.yaml`
- Generated report: `demo/open_source_sec_form4_001/output/report.md`
- Manifest: `demo/open_source_sec_form4_001/output/manifest.json`
- Manual validation: `docs/MANUAL_VALIDATION_SEC_FORM4_EN.md`

## Findings

| Rule ID | Source Row IDs | Evaluated Value | Threshold | Interpretation |
| --- | --- | --- | --- | --- |
| sec_form4_max_transaction_notional_proxy | sec_000173112226000397_8924105 | 688735872 | 1000000 | Transaction-notional proxy breach |
| sec_form4_watchlist_symbol_svre | sec_000173112226000397_8924105 | SVRE | SVRE | Validation-only watchlist match |
| sec_form4_max_transaction_notional_proxy | sec_000114036126009622_8924543 | 2152903500 | 1000000 | Transaction-notional proxy breach |
| sec_form4_max_transaction_notional_proxy | sec_000173112226000397_8924106 | 230219280 | 1000000 | Transaction-notional proxy breach |
| sec_form4_watchlist_symbol_svre | sec_000173112226000397_8924106 | SVRE | SVRE | Validation-only watchlist match |
| sec_form4_max_transaction_notional_proxy | sec_000162828026018929_8928326 | 8320500 | 1000000 | Transaction-notional proxy breach |
| sec_form4_max_transaction_notional_proxy | sec_000153983826000058_8932299 | 1130100 | 1000000 | Transaction-notional proxy breach |

## P&L And Unsupported Fields

- Reported P&L impact is `0` because the SEC Form 4 source does not provide an
  account ledger, realized P&L, fees, balances, or equity curve.
- `max_position_size` is used here as a transaction-notional proxy:
  `abs(quantity * price)`.
- Leverage is unsupported and must remain a limitation.
- Daily loss, drawdown, cooldown-after-loss, strategy quality, and trader intent
  are not evaluated for this source.

## Next Action

Use this reviewed report only as an internal artifact-quality proof. For a paid
pilot or customer-facing audit, replace the public-source fixture with an
operator-approved private export or approved read-only historical import and
repeat scope lock, intake mapping, audit run, manual validation, and claim
safety review.
