# Public Sample 001 Source Metadata

source_name: SEC EDGAR Insider Transactions Data Sets / Form 4 public-like derived fixture
source_url: https://www.sec.gov/dera/data/form-345
source_publisher: U.S. Securities and Exchange Commission
source_accessed_date: 2026-05-08
source_license_or_terms: Public source candidate; terms must be rechecked before replacing this public-like fixture with a live downloaded sample.
source_record_type: Form 4 non-derivative transaction-like rows
public_sample_label: internal validation; demo artifact; public-like sample
fields_used: TRANS_DATE, ISSUERTRADINGSYMBOL, TRANS_ACQUIRED_DISP_CD, TRANS_SHARES, TRANS_PRICEPERSHARE, ACCESSION_NUMBER plus derived source row key
fields_removed: reporting owner names, signatures, remarks, footnotes, relationship titles, owner addresses, owner identifiers, issuer contact fields, and all unnecessary personal fields
privacy_reviewed_by: operator
privacy_review_date: 2026-05-08
fixture_generation_command: .venv/bin/python -m trader_risk_audit audit --trades demo/public_sample_001/trades.csv --policy demo/public_sample_001/policy.yaml --output-dir demo/public_sample_001/output
intended_use: internal_validation; demo_only

## Why This Fixture Is Allowed

This committed pack is a public-like derived fixture for internal validation. It
uses the SEC Form 4 candidate field mapping from
`docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md`, but the committed rows are compact
audit-safe examples rather than a live downloaded SEC file. The pack contains no
reporting owner names, signatures, remarks, footnotes, broker account ids,
Telegram handles, emails, payment identifiers, account balances, API keys,
private notes, or paid pilot files.

## Why This Is Not Market Validation

This pack is not a qualified prospect call, paid pilot report, repeat
commitment, referral, PMF evidence, customer validation, or proof that traders
will pay. It can show artifact quality, deterministic reproducibility,
source-row traceability, and demo readability only.

## Transformation Notes

- `TRANS_DATE` maps to `timestamp`.
- `ISSUERTRADINGSYMBOL` maps to `symbol`.
- `TRANS_ACQUIRED_DISP_CD` maps to `side`, where `A` is buy-like and `D` is
  sell-like.
- `TRANS_SHARES` maps to `quantity`.
- `TRANS_PRICEPERSHARE` maps to `price`.
- `ACCESSION_NUMBER` plus row key is represented through the committed CSV row
  order and generated source row ids.

## Starter Profile Context

The generated report uses the `hard` starter profile because T31 needs a compact
internal stress test with at least three explainable risk scenarios. The starter
profile is a customizable audit preset, not investment advice, not a strategy
recommendation, not an optimal risk setting, and not a replacement for trader
custom rules or prop/funded account rules.

Soft and medium profiles remain available in `templates/policies/` for
comparison. A stricter profile may produce more flags, but this pack does not
claim that `hard` is objectively best.

## Telegram Demo Boundary

If this pack is shown through Telegram in a later demo, the allowed flow is
upload, audit id/status, local operator run, and operator-approved report
delivery under ADR-001. It must not add broker APIs, signal parsing, order
blocking, auto-advice, live trading behavior, or report delivery without
operator approval.
