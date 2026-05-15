# Manual Validation - SEC Form 4 Open Source

Status: T66 manual validation complete
Date: 2026-05-12
Input fixture: `demo/open_source_sec_form4_001/trades.csv`
Violation artifact: `demo/open_source_sec_form4_001/output/violations.json`
Report: `demo/open_source_sec_form4_001/output/report.md`

## Validation Scope

This validation covers every generated violation plus one non-flagged control
row. The goal is correctness of source-row traceability and arithmetic, not a
claim that the SEC rows represent a customer account or a profitable/unprofitable
trader.

## Reviewed Examples

| Case | Source row id | Source values | Expected result | Artifact result | Verdict |
|---|---|---|---|---|---|
| largest notional | `sec_000114036126009622_8924543` | FANG, sell, 12650000 x 170.19 | 2152903500 > 1000000, breach | `sec_form4_max_transaction_notional_proxy`, evaluated value `2152903500` | pass |
| SVRE high notional | `sec_000173112226000397_8924105` | SVRE, buy, 260884800 x 2.64 | 688735872 > 1000000, breach | `sec_form4_max_transaction_notional_proxy`, evaluated value `688735872` | pass |
| SVRE watchlist | `sec_000173112226000397_8924105` | symbol SVRE | forbidden/watchlist symbol breach | `sec_form4_watchlist_symbol_svre`, evaluated value `SVRE` | pass |
| second SVRE notional | `sec_000173112226000397_8924106` | SVRE, buy, 86875200 x 2.65 | 230219280 > 1000000, breach | `sec_form4_max_transaction_notional_proxy`, evaluated value `230219280` | pass |
| second SVRE watchlist | `sec_000173112226000397_8924106` | symbol SVRE | forbidden/watchlist symbol breach | `sec_form4_watchlist_symbol_svre`, evaluated value `SVRE` | pass |
| CENX notional | `sec_000162828026018929_8928326` | CENX, sell, 150000 x 55.47 | 8320500 > 1000000, breach | `sec_form4_max_transaction_notional_proxy`, evaluated value `8320500` | pass |
| FANG threshold edge | `sec_000153983826000058_8932299` | FANG, sell, 6000 x 188.35 | 1130100 > 1000000, breach | `sec_form4_max_transaction_notional_proxy`, evaluated value `1130100` | pass |
| non-flagged control | `sec_000122520826003751_8928357` | NRG, sell, 5000 x 156.65 | 783250 <= 1000000, no notional breach and no watchlist breach | no violation row present | pass |

## Limitation Review

Accepted limitations:

- P&L is zero because the SEC fixture is transaction disclosure data, not an
  account ledger with realized P&L.
- Drawdown and daily-loss claims are not supported by the source.
- `max_position_size` is used only as a transaction-notional proxy.
- `SVRE` is a validation watchlist symbol, not a real restriction,
  recommendation, or view on that issuer.
- `max_leverage` correctly appears as unsupported because the source has no
  leverage field.

## Error Register

| ID | Severity | Area | Finding | External delivery status | Disposition |
|---|---|---|---|---|---|
| T66-P2-001 | P2 | report limitation wording | The generated report is mechanically correct but its first screen does not clearly say this is open-source artifact validation, that P&L is unsupported, or that max position size is a transaction-notional proxy. | allowed only after T67 polish | accepted for T67 |

No P0 or P1 correctness issues were found. External delivery remains blocked
until T67 claim-safety/report-polish review addresses or explicitly accepts
T66-P2-001.
