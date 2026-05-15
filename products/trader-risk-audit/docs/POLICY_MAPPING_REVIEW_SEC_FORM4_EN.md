# Policy Mapping Review - SEC Form 4 Open Source

Status: complete for T64
Date: 2026-05-12
Policy file: `demo/open_source_sec_form4_001/policy.yaml`

## Policy Type

This is a custom open-source validation policy. It is not a trader-specific
paid-pilot policy, investment advice, a recommended risk model, or a claim
about the selected issuers.

The policy exists to validate report mechanics: source-row traceability,
unsupported-data handling, limitation wording, deterministic rule output, and
manifest reproducibility in later T65-T67 tasks.

## Supported Rules

| Rule id | Type | Mapping decision | Ambiguity |
|---|---|---|---|
| `sec_form4_max_transaction_notional_proxy` | `max_position_size` | Supported by existing evaluator as `abs(quantity * price)` per row. Interpreted only as transaction-notional proxy for this fixture. | none after limitation wording |
| `sec_form4_watchlist_symbol_svre` | `forbidden_assets` | Supported by existing evaluator; `SVRE` is a validation watchlist symbol for traceability. | none after labeling as validation-only |
| `sec_form4_leverage_unsupported_register` | `max_leverage` | Existing evaluator emits unsupported-data warning because leverage is absent. | none; expected limitation |

## Rejected Or Deferred Rules

| Candidate rule | Reason |
|---|---|
| max daily loss | SEC Form 4 rows do not provide account-level realized P&L. |
| max drawdown | SEC Form 4 rows do not provide equity curve or account balance. |
| cooldown after loss | SEC Form 4 rows do not prove a trader's realized loss or behavioral cooldown context. |
| fee-sensitive P&L | SEC Form 4 rows do not include broker fees. |
| leverage breach | SEC Form 4 rows do not include leverage; keep as unsupported warning only. |

## Human Approval Boundary

No ambiguous policy mapping remains for T65 if the report keeps these labels:

- open-source artifact validation;
- not customer data;
- not paid-pilot evidence;
- transaction-notional proxy;
- unsupported P&L/drawdown/leverage limitations.

Changing this policy into a customer audit, a paid-pilot report, a real insider
trading conclusion, or a recommendation about the selected symbols requires a
new scope note and human approval.
