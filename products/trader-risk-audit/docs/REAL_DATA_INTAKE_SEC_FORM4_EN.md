# Real Data Intake - SEC Form 4 Open Source

Status: T64 intake and schema mapping complete
Date: 2026-05-12
Scope note: `docs/REAL_AUDIT_SCOPE_OPEN_SOURCE_EN.md`
Fixture: `demo/open_source_sec_form4_001/trades.csv`
Policy: `demo/open_source_sec_form4_001/policy.yaml`

## Source

- Publisher: U.S. Securities and Exchange Commission.
- Source page: https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
- Downloaded source: https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2026q1_form345.zip
- SEC page update note: March 31, 2026.
- Raw source location during this run:
  `/tmp/trader-risk-audit-sec/2026q1_form345.zip`
- Raw source committed: no.

## Source Coverage

The raw 2026 Q1 zip contains these relevant files:

| Raw file | Used? | Reason |
|---|---:|---|
| `SUBMISSION.tsv` | yes | issuer trading symbol keyed by accession number |
| `NONDERIV_TRANS.tsv` | yes | non-derivative transaction rows |
| `DERIV_TRANS.tsv` | no | derivative transactions are out of scope |
| `DERIV_HOLDING.tsv` | no | holdings are out of scope |
| `NONDERIV_HOLDING.tsv` | no | holdings are out of scope |
| `REPORTINGOWNER.tsv` | no | contains reporting-owner data not required for audit fixture |
| `OWNER_SIGNATURE.tsv` | no | contains signatures and is privacy-excluded |
| `FOOTNOTES.tsv` | no | footnotes are privacy-excluded |

Raw row counts observed during intake:

| Filter | Count |
|---|---:|
| total `NONDERIV_TRANS.tsv` rows | 103733 |
| rows with transaction code `P` or `S` | 28757 |
| rows with mappable acquired/disposed side `A` or `D` | 28757 |
| rows with required date, shares, and price fields | 28699 |
| rows with positive price and quantity | 28585 |
| rows with joined issuer trading symbol | 28585 |
| committed sanitized fixture rows | 6 |

## Field Mapping

| SEC source field | Sanitized fixture field | Mapping rule |
|---|---|---|
| `TRANS_DATE` | `timestamp` | converted from SEC date-only value to Europe/Moscow local start-of-day |
| `ISSUERTRADINGSYMBOL` | `symbol` | upper-case public ticker as provided through `SUBMISSION.tsv` |
| `TRANS_ACQUIRED_DISP_CD` | `side` | `A` -> `buy`, `D` -> `sell` |
| `TRANS_SHARES` | `quantity` | decimal string copied from source |
| `TRANS_PRICEPERSHARE` | `price` | decimal string copied from source |
| n/a | `fees` | set to `0`; SEC Form 4 does not provide broker fees |
| n/a | `account_id` | fixed anonymized label `acct_open_sec_form4_msk_001` |
| `ACCESSION_NUMBER` + `NONDERIV_TRANS_SK` | `row_id` | sanitized trace id with punctuation removed |

## Selected Rows

| Fixture row | SEC date | Timestamp used | Symbol | Side | Quantity | Price | Source trace |
|---:|---|---|---|---|---:|---:|---|
| 2 | 11-MAR-2026 | 2026-03-11T00:00:00+03:00 | SVRE | buy | 260884800 | 2.64 | `0001731122-26-000397` / `8924105` |
| 3 | 12-MAR-2026 | 2026-03-12T00:00:00+03:00 | FANG | sell | 12650000 | 170.19 | `0001140361-26-009622` / `8924543` |
| 4 | 12-MAR-2026 | 2026-03-12T00:00:00+03:00 | SVRE | buy | 86875200 | 2.65 | `0001731122-26-000397` / `8924106` |
| 5 | 16-MAR-2026 | 2026-03-16T00:00:00+03:00 | CENX | sell | 150000 | 55.47 | `0001628280-26-018929` / `8928326` |
| 6 | 16-MAR-2026 | 2026-03-16T00:00:00+03:00 | NRG | sell | 5000 | 156.65 | `0001225208-26-003751` / `8928357` |
| 7 | 18-MAR-2026 | 2026-03-18T00:00:00+03:00 | FANG | sell | 6000 | 188.35 | `0001539838-26-000058` / `8932299` |

## Unsupported Field Register

| Field / concept | Status | Handling |
|---|---|---|
| realized P&L | unavailable | do not run daily loss or drawdown rules for this fixture |
| account balance / equity | unavailable | report as limitation only |
| leverage | unavailable | `max_leverage` is kept as unsupported-data limitation |
| broker/exchange fees | unavailable | fixture uses `fees=0` and documents the assumption |
| account ownership / reporting owner | privacy-excluded | not committed and not used in report truth |
| transaction intent / strategy | unavailable | no intent, advice, or causal-loss claims |
| derivative transactions | excluded | outside this Phase 16 fixture scope |
| holdings after transaction | excluded | not required for T64 artifact intake |

## Validation Output

Manual validation command:

```bash
.venv/bin/python - <<'PY'
from trader_risk_audit.trades.importers import normalize_csv
from trader_risk_audit.policy.schema import load_policy

records = normalize_csv("demo/open_source_sec_form4_001/trades.csv")
policy = load_policy("demo/open_source_sec_form4_001/policy.yaml")
print(f"records={len(records)}")
print(f"first_row={records[0].row_id}")
print(f"policy_rules={','.join(rule.rule_id for rule in policy.rules)}")
PY
```

Observed output:

```text
records=6
first_row=sec_000173112226000397_8924105
policy_rules=sec_form4_max_transaction_notional_proxy,sec_form4_watchlist_symbol_svre,sec_form4_leverage_unsupported_register
```

## T65 Readiness

T65 may run the existing deterministic audit command against the committed
fixture and policy. Expected limitations:

- `max_position_size` is being used as a transaction-notional proxy because the
  existing evaluator checks absolute quantity times price for each row.
- `forbidden_assets` is a validation watchlist scenario, not a real trading
  prohibition for SEC insiders.
- `max_leverage` should remain an unsupported-data warning because SEC Form 4
  does not include leverage.
- P&L and drawdown reports must not claim account-level trading performance.
