# Product Artifact Bridge Notes

Version: 1.0
Date: 2026-05-12
Status: PHASE_15_SUPPORT_NOTES

These notes define narrow Core support boundaries for Trader Risk Audit and
Signal Analytics Sandbox artifact validation. They do not approve product
integration, product rewrites, public Core SDK work, hosted Core service work,
live execution, holdout/OOS expansion, or external delivery.

## Shared Bridge Rule

Core may provide:

- shared artifact contract fields;
- no-claim and decision-state vocabulary;
- reproducibility and validity checklist language;
- product-neutral review packet templates;
- deterministic hash/reference expectations.

Core must not provide:

- product-specific report logic;
- customer or public-source ingestion logic;
- domain-specific finding truth;
- report copy rewrites;
- delivery approval;
- live feed, broker/exchange, order, holdout, OOS, production, or capital-ready
  behavior.

Core-driven rewrites of Trader or Signal during artifact validation are
forbidden. Product agents own their own report generation and validation logic.

## Trader Risk Audit Bridge Notes

Trader artifacts should use the shared contract to make real audit reports
traceable without moving Trader logic into Core.

### Violation Record Shape

Product-local violation records should preserve:

- `violation_id`;
- `policy_id`;
- `rule_id`;
- `source_row_ids` or safe source fingerprints;
- `observed_value`;
- `threshold`;
- `unit`;
- `severity`;
- `occurred_at`;
- `attribution_ref`;
- `deterministic_owner`.

The product owns rule interpretation and violation truth. Core may only require
that material findings are traceable and manually reviewed.

### Policy And Config Hash

Trader artifact packets should include `policy_config_hash` over:

- approved policy/rule manifest;
- threshold and unit config;
- attribution method config;
- report generation config;
- redaction config if it changes visible evidence.

### Manifest Conventions

Trader manifests should separate:

- raw private export location or safe fingerprint;
- redacted source artifact refs;
- normalized violation table refs;
- generated report refs;
- error register refs;
- delivery decision refs.

Raw customer exports should remain product-local unless explicitly approved by
the product scope note.

### Report No-Claim Boundary

Trader report artifacts must preserve:

- not order blocking;
- not live trading;
- not broker/exchange execution;
- not production;
- not capital-ready;
- not investment advice;
- not Core phase-gate approval.

### Manual Validation Status

Trader external pilot readiness requires product-local manual review that the
same real audit inputs produce the same material findings, severities,
attribution refs, limitations, and no-claim language.

## Signal Analytics Sandbox Bridge Notes

Signal artifacts should use the shared contract to make public-source reports
traceable while preserving ambiguity and source-volatility boundaries.

### Source And Evidence Refs

Signal artifact packets should record:

- source list or capture pack refs;
- source capture timestamps;
- evidence table refs;
- unsupported-field register refs;
- ambiguity register refs;
- synthesis/review config refs;
- generated report refs;
- delivery decision refs.

Source refs should prefer stable checked-in captures or redacted source packs
when allowed. Live public pages may be referenced only with availability and
content-drift limitations.

### Reviewed And Draft Status Language

Signal artifacts should use explicit status language:

- `draft_not_reviewed`;
- `reviewed_internal_only`;
- `validated_for_controlled_external_pilot`;
- `blocked_by_ambiguity`;
- `blocked_by_source_traceability`;
- `rejected`.

Draft language must not imply advice, prediction, production readiness, or
automated signal execution.

### Ambiguity And Insufficient Evidence

Signal reports must preserve:

- ambiguity status for disputed or weakly sourced claims;
- insufficient-evidence status where source support is missing;
- source availability limitations;
- manual-review dependency for judgment-heavy findings.

The report should prefer `insufficient_evidence` over a confident claim when a
source ref does not support the finding.

### No-Advice And No-Future-Performance Boundary

Signal report artifacts must preserve:

- not trading advice;
- not investment recommendation;
- not future-performance prediction;
- not automated signal execution;
- not production;
- not capital-ready;
- not Core phase-gate approval.

## Ownership Boundary

| Boundary | Core owner | Product owner |
|---|---|---|
| Artifact field vocabulary | Yes | Adopt and extend product-locally. |
| Checklist vocabulary | Yes | Execute product-local review. |
| Hash/reference expectations | Yes | Generate product-local hashes and refs. |
| Report logic | No | Yes. |
| Domain truth | No | Yes. |
| Source ingestion | No | Yes. |
| Error register | Template only | Yes. |
| Delivery approval | No | Yes. |
| External pilot feedback | Template only | Yes. |

If a product needs more than this support, open a new scoped bridge task before
adding Core code or broadening Core ownership.
