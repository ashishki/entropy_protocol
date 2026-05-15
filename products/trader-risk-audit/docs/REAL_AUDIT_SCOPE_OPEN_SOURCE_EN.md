# Real Audit Scope - Open Source SEC Form 4

Status: locked for Phase 16 T63
Date: 2026-05-12
Language: English
Timezone: Europe/Moscow, UTC+03:00

## Decision

Because no private operator/customer export was supplied, Phase 16 will use a
verified public regulatory source for artifact validation instead of blocking
on private data.

This scope validates report artifact quality, traceability, limitation wording,
and reproducibility. It is not paid-pilot evidence, PMF evidence, customer
validation, or proof that traders will pay.

## Source

- Source type: public regulatory transaction records.
- Publisher: U.S. Securities and Exchange Commission.
- Source page: https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
- Data dictionary: https://www.sec.gov/files/insider_transactions_data_sets.pdf
- Selected dataset: Insider Transactions Data Sets, Form 4 non-derivative
  transaction rows for 2026 Q1, or the newest SEC quarter available when T64
  runs.
- Access date: 2026-05-12.

## Audit Subject

- Account label: `acct_open_sec_form4_msk_001`.
- Account type: anonymized public-source validation account, not a real
  customer brokerage account.
- Instrument universe: U.S. public company equity symbols present in the
  selected Form 4 non-derivative transaction rows.
- Source rows: only transaction rows with enough fields to map timestamp,
  symbol, side, quantity, price, and source traceability.
- Time period: 2026-01-01 through 2026-03-31, unless T64 finds that the newest
  SEC quarterly file differs; if so, T64 must record the exact quarter used.
- Timezone: convert source dates to Europe/Moscow at local start-of-day for
  report display and session grouping. Preserve original source dates in the
  intake/schema summary.

## Field Mapping

| SEC field | Audit field |
|---|---|
| `TRANS_DATE` | `timestamp` |
| `ISSUERTRADINGSYMBOL` | `symbol` |
| `TRANS_ACQUIRED_DISP_CD` | `side`, where `A` maps to `buy` and `D` maps to `sell` |
| `TRANS_SHARES` | `quantity` |
| `TRANS_PRICEPERSHARE` | `price` |
| `ACCESSION_NUMBER` plus source row key | source traceability metadata |

Rows must be excluded if required mapping fields are missing, price is absent
or zero for a scenario that needs notional value, the transaction is derivative
only, or the transaction code/side cannot be mapped safely.

## Policy

Use a custom open-source validation policy, not a trader-specific paid-pilot
policy. Initial supported checks:

- maximum transaction notional;
- forbidden or watchlist symbol scenario, if the selected rows contain a clear
  audit-safe symbol example;
- optional cooldown/sequence scenario only if the selected source rows support
  a deterministic same-account sequence without guessing intent.

Unsupported or ambiguous checks:

- daily realized P&L;
- account drawdown;
- leverage;
- broker/exchange fees;
- account balance or buying power;
- trader intent, strategy quality, or causal-loss claims.

These unsupported checks must appear as limitations, not guessed violations.

## Privacy Boundary

Do not commit raw SEC bulk files if they are larger than the minimum sanitized
fixture needed for T64/T65.

Allowed to commit after review:

- this scope note;
- sanitized source metadata;
- a compact derived CSV fixture with only audit-safe mapped fields;
- deterministic output artifacts generated from the sanitized fixture;
- source row ids/accession references needed for traceability.

Must not be committed:

- reporting owner names;
- signatures;
- remarks;
- footnotes;
- relationship titles;
- addresses or personal identifiers;
- free-text private notes;
- any private/customer export;
- credentials, API keys, account secrets, Telegram handles, emails, or payment
  identifiers.

Externally showable:

- the final English report only after T66/T67 manual validation and claim-safety
  review;
- redacted source summary and source-row traceability references;
- limitations explaining that this is public-source artifact validation, not a
  paid customer audit.

## Delivery Format

- Report language: English.
- Delivery artifact: Markdown report plus Telegram-ready local text packet.
- Delivery mode: local operator-controlled delivery only; no automated send.

## T64 Instructions

T64 should fetch or manually place the selected SEC dataset outside git, derive
a compact sanitized fixture, record the exact source URL and quarter, map only
safe fields, and produce an unsupported-field register before any report run.
