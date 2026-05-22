# Open-Source Audit Case Bank

Status: active protocol
Date: 2026-05-15

This document defines how Trader Risk Audit selects public/open-source and
synthetic audit cases before building the Phase 23 case packs. It is a
selection and evidence-quality protocol, not a customer evidence log.

## Purpose

The case bank exists to test whether reports are valid, readable,
reproducible, and claim-safe across varied data shapes. It must not be curated
only for impressive-looking violations. Preserved limitation, rejection, and
edge-case packs are part of the evidence because they prove the workflow can
say "not enough support" or "not runnable" without hiding weak cases.

Public/open-source packs are artifact-quality evidence only. They do not count
as paid-pilot evidence, PMF evidence, customer evidence, or willingness-to-pay
evidence.

## Allowed Source Classes

| Source class | Allowed when | Required notes |
|---|---|---|
| Public regulatory or disclosure datasets | The data is lawfully public and can be transformed into transaction-like audit input without pretending it is a trader's private export. | Source URL, access date, license/terms posture, transformation steps, and limitations. |
| Open-source sample trade datasets | The repository or dataset license permits local use and committed derived fixtures. | Repository/dataset URL, license, attribution requirements, privacy review, and any synthetic transformations. |
| Public documentation examples | The examples are explicitly published for documentation, testing, or education and do not include real private account details. | Publisher, page/version, access date, allowed use summary, and why the example is suitable. |
| Sanitized synthetic edge cases | The case is needed to exercise a schema, rule, limitation, or rejection path that is not available in public data. | Synthetic label, generation rationale, fields intentionally varied, and confirmation that no real person/account is represented. |
| Existing approved internal demo packs | The pack is already committed, reviewed, and labeled as demo/open-source artifact evidence. | Existing source note, current reviewed report status, and any known limitations. |

## Excluded Source Classes

The case bank must not include:

- private or customer exports;
- broker account ids, exchange account ids, Telegram handles, emails, phone
  numbers, payment identifiers, credentials, API keys, signatures, or private
  file paths;
- leaked, scraped, or terms-unclear datasets;
- datasets whose license forbids committed derived fixtures or internal demo
  use;
- live exchange network fetches or newly collected read-only API data;
- generated examples presented as public/open-source provenance;
- packs selected only because they create strong positive violations.

If source legality, terms, or privacy posture is unclear, the pack must be
classified as `rejected_source` or replaced with a clearly labeled synthetic
edge case.

## Selection Rationale

Every candidate must record why it was selected using these fields:

- `case_id`: stable directory-safe id;
- `source_class`: one allowed class above;
- `expected_case_type`: `positive_finding`, `limitation`, `reject`,
  `edge_schema`, or `mixed`;
- `data_shape`: for example disclosure-like, broker/export-like,
  exchange-fixture-like, or synthetic edge-case CSV;
- `rules_exercised`: supported deterministic rule types expected to run;
- `expected_limitations`: fields or semantics that should be missing,
  rejected, or manually reviewed;
- `selection_reason`: why this case improves coverage rather than flattering
  the product;
- `not_customer_evidence`: explicit `true`.

Selection is valid only when the rationale describes coverage, limitation, or
reproducibility value. "Looks good in a demo" is not sufficient by itself.

## License and Terms Notes

Each case pack source note must include:

- source URL or exact source description;
- access date in `YYYY-MM-DD`;
- license or terms summary;
- attribution requirements, if any;
- whether raw source data can be committed;
- if raw source data cannot be committed, the allowed derived fixture strategy;
- privacy review result;
- transformation steps from source data to audit input;
- limitations caused by the source shape.

Do not commit a source-derived fixture until the license/terms note states why
committing it is acceptable. When in doubt, keep only metadata in git and use a
sanitized synthetic fixture with honest provenance.

## Anti-Cherry-Pick Batch Composition

Each Phase 23 validation batch must attempt to include:

- at least one `positive_finding` case;
- at least one `limitation` or `reject` case;
- at least one `edge_schema` case when such a case is available;
- at least three distinct data shapes across the full Phase 23 bank;
- the existing SEC Form 4 pack as a reference baseline until superseded by the
  T99 contract validator.

If a category is unavailable in a batch, the batch note must say what was
searched, why the category was not available, and whether a synthetic edge case
will fill the coverage gap. Missing negative/limitation cases must not be
silently omitted.

## Case Statuses

| Status | Meaning |
|---|---|
| `candidate` | Source selected and source note drafted; audit artifacts may not exist yet. |
| `runnable` | Policy and input fixture are expected to run through the deterministic audit path. |
| `blocked_source` | License, privacy, provenance, or terms are not acceptable. |
| `blocked_schema` | Source is acceptable but does not have enough fields for current deterministic rules. |
| `validated` | Report, manifest, reproducibility result, reviewed report, and validation note exist with no unresolved P0/P1 report-validity issues. |
| `demo_eligible` | Manually selected from validated packs for later Phase 24 demo use. |

Blocked packs stay in the inventory with their reason. They are evidence about
limits and source availability, not clutter to delete.

## Inventory

T100 candidate batch:

| Case ID | Status | Source class | Expected case type | Data shape | Selection reason | Evidence label |
|---|---|---|---|---|---|---|
| `open_source_sec_form4_001` | runnable reference | public regulatory/disclosure | mixed | disclosure-like | Existing reviewed baseline from Phase 16; useful as the first reference pack for the T99 contract and report limitation language. | artifact-quality only |
| `public_sample_001` | runnable candidate | public-like approved internal demo pack | positive_finding | disclosure-like compact sample | Existing public-like sample exercises multiple violations and demo readability without private data. | artifact-quality only |
| `risk_audit_case_001` | runnable candidate | sanitized synthetic edge case | positive_finding | broker/export-like CSV | Existing synthetic broker-like pack exercises realized P&L, cooldown, forbidden asset, position size, and daily-loss behavior. | artifact-quality only |
| `synthetic_limit_leverage_001` | candidate | sanitized synthetic edge case | limitation | broker/export-like CSV | Preserves a missing-leverage limitation where max_leverage must not be guessed from unsupported input fields. | artifact-quality only |
| `synthetic_schema_reject_missing_price_001` | candidate | sanitized synthetic edge case | reject / edge_schema | malformed broker/export-like CSV | Preserves a schema-reject case where the required price column is absent and report generation should not run. | artifact-quality only |

## Candidate Detail

| Case ID | Expected evaluable fields | Expected limitations | Should produce |
|---|---|---|---|
| `open_source_sec_form4_001` | timestamp, symbol, side, quantity, price, fees, account_id | SEC disclosure rows are not a customer ledger; P&L/drawdown context is unsupported; position size is a transaction-notional proxy. | mixed positive findings plus explicit limitations |
| `public_sample_001` | timestamp, symbol, side, quantity, price, fees, account_id | Public-like derived fixture; not live downloaded source data and not market evidence. | positive findings |
| `risk_audit_case_001` | timestamp, symbol, side, quantity, price, fees, account_id | Synthetic provenance; should not be presented as public or customer evidence. | positive findings |
| `synthetic_limit_leverage_001` | timestamp, symbol, side, quantity, price, fees, account_id | No leverage field; max_leverage should become an unsupported-data limitation. | limitation |
| `synthetic_schema_reject_missing_price_001` | none until schema is fixed | Missing required `price` column; import should reject before audit outputs are created. | rejection |

Batch composition check:

- positive-finding case present: `public_sample_001`, `risk_audit_case_001`;
- limitation/reject case present: `synthetic_limit_leverage_001`,
  `synthetic_schema_reject_missing_price_001`;
- edge/schema case present: `synthetic_schema_reject_missing_price_001`;
- data shapes represented: disclosure-like, broker/export-like CSV,
  malformed/edge-case CSV;
- no case in this inventory is paid-pilot, PMF, or customer evidence.

## Evidence Boundary

The case bank may support product confidence and report-quality review. It must
not be used to claim:

- paid pilot demand;
- PMF;
- customer validation;
- conversion lift;
- profitability or performance improvement;
- readiness for hosted uploads, checkout, or real exchange fetching.

Those claims require separate privacy-safe market evidence or approved private
pilot evidence outside this open-source case-bank protocol.

## Coverage Matrix

Rule/data coverage for the current bank is tracked in
`docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`. That matrix is the Phase 24 source
for missing coverage decisions, including drawdown-only, leverage-supported,
fee-specific, session-timezone, realized-P&L wording, and no-breach control
follow-up cases.
