# Public Sample Source Policy RU

## Назначение

Этот документ задает правила для public sample pack в Phase 7. Public samples
нужны только для internal validation и demo artifacts: проверить, что Trader
Risk Audit может воспроизводимо импортировать публичные или публично-похожие
записи, прогнать их через audit presets, показать explainable violations и
подготовить понятный demo до outreach к реальным трейдерам.

Public sample artifacts не являются qualified prospect calls, paid pilot
reports, repeat commitments, referrals или PMF evidence. Их нельзя считать
market validation, готовностью платить, доказательством retention или
доказательством ценности для реального трейдера.

## Acceptable Source Types

Разрешенные источники для internal validation:

- Public regulatory datasets with stable public access and documented reuse
  terms.
- Public exchange or venue trade-print samples, only when they are explicitly
  public and can be labeled as market prints, not account history.
- Fully synthetic or anonymized internal fixtures that contain no real customer,
  broker, Telegram, payment, account, or private-note data.
- Public-like examples supplied by the operator only after the operator records
  why the data is safe to commit and which private fields were removed.

Запрещенные источники:

- Real customer exports, paid pilot files, broker statements, screenshots,
  Telegram messages, private group content, payment records, emails, or CRM
  notes.
- Any file containing broker API keys, exchange API keys, access tokens,
  passwords, seed phrases, raw Telegram handles, emails, phone numbers, account
  ids, account balances, signatures, remarks, footnotes, or free-text private
  notes.
- Datasets whose license or terms are unknown, unclear, paywalled, private, or
  incompatible with committing a derived fixture to this repository.

## Required Source Metadata

Every committed public sample pack must include source metadata next to the
fixture or in the evidence pack:

- `source_name`
- `source_url`
- `source_publisher`
- `source_accessed_date`
- `source_license_or_terms`
- `source_record_type`
- `public_sample_label`
- `fields_used`
- `fields_removed`
- `privacy_reviewed_by`
- `privacy_review_date`
- `fixture_generation_command`
- `intended_use`

`intended_use` must say `internal_validation` or `demo_only`. It must not say
paid pilot, prospect evidence, PMF evidence, customer proof, or market proof.

## License and Terms Check

Before a public sample is committed, the operator must:

1. Read the publisher license, terms of use, access notes, or data dictionary.
2. Record the exact source URL and access date.
3. Confirm that the committed artifact is allowed as a derived internal/demo
   fixture.
4. Record any attribution text required by the publisher.
5. Reject the source if the terms are missing, unclear, private, or prohibit
   redistribution of derived samples.

No source is accepted because it is "on the internet." Public availability is
not enough; source terms must be checked and recorded.

## Primary Candidate for T31

Primary candidate: SEC EDGAR Insider Transactions Data Sets / Form 4
non-derivative transactions.

T31 may use only rows that can support deterministic trade-like audit examples:

- transaction rows with required date, ticker, shares, and price fields;
- transaction codes `P` or `S`, where available;
- non-derivative transaction data only for the first sample pack.

Candidate mapping for T31:

| Source field | Sample field |
|---|---|
| `TRANS_DATE` | `timestamp` |
| `ISSUERTRADINGSYMBOL` | `symbol` |
| `TRANS_ACQUIRED_DISP_CD` | buy/sell direction mapping, where `A` = buy-like and `D` = sell-like |
| `TRANS_SHARES` | `quantity` |
| `TRANS_PRICEPERSHARE` | `price` |

Fields to remove before committing any derived sample:

- reporting owner names;
- signatures;
- remarks;
- footnotes;
- relationship titles;
- owner addresses or identifiers;
- any personal or unnecessary issuer/contact fields;
- any field not required for the deterministic audit scenario.

If SEC Form 4 data cannot produce at least three explainable risk scenarios,
the backup source is public exchange trade-print samples. Backup samples must be
labeled as market trade prints, not trader account history, and must not imply
they show a real user's discipline behavior.

## Privacy and Secret Rejection Criteria

A public sample pack must be rejected or regenerated if it contains:

- real customer names, emails, phone numbers, Telegram handles, payment ids, or
  broker account ids;
- account balances, private notes, raw exports from prospects, paid pilot
  reports, or screenshots;
- credentials, API keys, bearer tokens, session cookies, seed phrases,
  passwords, or private keys;
- reporting owner names, signatures, remarks, or footnotes from public filings;
- enough fields to re-identify a person when those fields are not required for
  the audit scenario.

Allowed committed values are limited to audit-safe fields such as synthetic
account ids, timestamps, symbols, sides, quantities, prices, source row ids,
policy profile names, non-sensitive source metadata, and deterministic output
hashes.

## Evidence Labeling Rules

Every public sample artifact, report, manifest, and README note must label the
sample as one of:

- `internal validation`
- `demo artifact`
- `synthetic fixture`
- `public sample`

The label must not say or imply:

- qualified prospect call;
- paid pilot report;
- repeat commitment;
- referral;
- PMF evidence;
- customer validation;
- proof that traders will pay.

Public sample results may prove artifact quality, reproducibility,
source-row traceability, explainability, and demo clarity. They do not prove
market pull.

## Starter Policy Profile Boundary

Phase 7 public samples may be run through `soft`, `medium`, and `hard` starter
audit presets from `docs/STARTER_POLICY_PROFILES_RU.md` and
`templates/policies/starter_policy_*.yaml`.

These profiles are customizable audit presets for internal validation and demos.
They are not investment advice, strategy recommendations, optimal risk
settings, or replacements for trader custom rules or prop/funded account rules.
If real trader rules exist, those rules have priority over starter templates.

## Outreach Readiness Gate

Trader outreach may start only after internal validation shows all of the
following:

- Reproducible reports: the same sample input, policy profile, and command
  produce stable deterministic artifacts and manifest hashes.
- Explainable violations: each violation can be explained from source rows,
  thresholds, evaluated values, timestamps, and report text.
- At least three risk scenarios: the public sample pack demonstrates three
  distinct explainable scenarios, such as daily loss, cooldown, forbidden asset,
  position size, or drawdown behavior.
- Two-minute readable demo: the founder can explain the sample source, privacy
  removals, audit profile, top violations, limitations, and no-advice boundary
  in under two minutes.

Passing this readiness gate permits manual outreach conversations. It still
does not count as paid pilot evidence or PMF evidence. The market validation
gate remains the paid-audit evidence log: 3 paid audit reports from 10 qualified
prospects within 14 days, then at least 2 repeat audit commitments within
30 days.

## Telegram Demo Boundary

Telegram may be used in later demo work only as a simple upload, audit id/status,
and operator-approved report delivery surface under ADR-001. Public sample demo
work must not add broker APIs, signal parsing, order blocking, auto-advice, live
trading behavior, report delivery without operator approval, or AI-owned
violation truth.
