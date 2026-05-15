# Open Source SEC Form 4 Source Metadata

source_name: SEC EDGAR Insider Transactions Data Sets / Form 4 non-derivative transactions
source_url: https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2026q1_form345.zip
source_page: https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
source_publisher: U.S. Securities and Exchange Commission
source_accessed_date: 2026-05-12
source_period: 2026 Q1
source_record_type: Form 4 non-derivative transaction rows
public_sample_label: open-source artifact validation; not customer evidence
intended_use: artifact_validation_only
privacy_reviewed_by: codex
privacy_review_date: 2026-05-12

## Source Notes

The SEC page states that the Insider Transactions Data Sets are extracted from
the XML-based fillable portions of Forms 3, 4, and 5 and are provided in a
flattened format. The selected quarter is `2026q1_form345.zip`; the raw zip was
downloaded to `/tmp/trader-risk-audit-sec/2026q1_form345.zip` and is not
committed.

The SEC page was last reviewed or updated on March 31, 2026. The SEC page also
notes that the data is derived from filer-provided submissions and is not a
substitute for reviewing full Commission filings.

## Files Used

- `SUBMISSION.tsv`: source for issuer trading symbol and issuer metadata.
- `NONDERIV_TRANS.tsv`: source for non-derivative transaction date, side,
  shares, price, accession number, and transaction key.

## Fields Used

- `ACCESSION_NUMBER`
- `NONDERIV_TRANS_SK`
- `TRANS_DATE`
- `TRANS_CODE`
- `TRANS_ACQUIRED_DISP_CD`
- `TRANS_SHARES`
- `TRANS_PRICEPERSHARE`
- `ISSUERTRADINGSYMBOL`

## Fields Removed Or Not Committed

- reporting owner names;
- signatures;
- remarks;
- footnotes;
- relationship titles;
- addresses or personal identifiers;
- direct/indirect ownership text;
- issuer names and other non-required issuer metadata;
- raw SEC bulk files.

## Fixture Generation

The committed fixture was manually derived from rows that met all mapping
requirements:

- transaction code was `P` or `S`;
- acquired/disposed code was `A` or `D`;
- transaction date, symbol, shares, and price were present;
- price and share quantity were positive;
- row could be traced by accession number and non-derivative transaction key.

The date-only SEC transaction date was converted to Europe/Moscow local
start-of-day in the committed `timestamp` field. Original SEC dates are recorded
in `docs/REAL_DATA_INTAKE_SEC_FORM4_EN.md`.
