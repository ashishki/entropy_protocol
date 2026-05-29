# Open-Source Audit Validation Roadmap

Status: active
Date: 2026-05-15

## Goal

Build enough real, inspectable audit evidence before approaching warm prospects.
The goal is not to force positive findings. The goal is to prove that Trader
Risk Audit produces valid, readable, reproducible, and claim-safe reports across
multiple open-source or operator-approved datasets.

Operating sequence:

```text
source selection -> case pack -> deterministic audit -> manual validation ->
error register -> polished demo pack -> private/operator-approved pilot
```

## Current Decision

Core is paused. Real exchange fetching remains blocked by the T93 defer
decision. The next work is Product 1 only: expand open-source validation and
prepare the product for real private/operator-approved audit packs.

Do not reopen T94-T97 unless new privacy-safe market evidence proves CSV/export
friction is the binding conversion blocker.

## Phase Map

| Phase | Name | Purpose | Gate |
|---|---|---|---|
| 23 | Open-Source Audit Case Bank | Create a curated bank of open-source and synthetic edge-case audit packs. | At least 5 candidate packs exist with source notes, policies, reports, manifests, validation notes, and limitations. |
| 24 | Multi-Case Report Quality Loop | Compare packs, find weak report language/calculation edge cases, and stabilize a demo-quality report format. | At least 3 packs are polished enough for internal demo, including one strong positive case and one limitation/reject case. |
| 25 | Private Pilot Readiness | Prepare safe intake, validation, delivery, and feedback artifacts for 1-3 operator-approved private/anonymized trade exports. | A warm prospect can receive a reviewed paid-pilot report without raw data entering git or unsafe claims entering the report. |
| 26 | Private Pilot Evidence Collection | Run and review one operator-approved private/anonymized artifact outside git when supplied. | Private report evidence exists safely, or the operator-input blocker remains explicit. |
| 27 | Real Open Data Rehearsal | Exercise the workflow with real public non-synthetic data. | Real public data improves technical rehearsal coverage without claiming private/paid/customer evidence. |
| 28 | Account-Scoped Real Open Data Rehearsal | Improve open-data coverage with a scoped public contract-recipient sequence. | Scoped public data is reviewed honestly and remains non-private evidence. |
| 29 | Pre-Private Hypothesis Validation | Strengthen technical/product/market hypothesis evidence while no private export is available. | Evidence is classified honestly; if export willingness appears, return to T116; otherwise narrow ICP, revise offer, continue concierge validation, or pause/pivot. |
| 30 | Concierge Validation Execution Kit | Prepare the operator to run the first 10-15 validation conversations manually. | Execution materials are complete, but actual aggregate outreach/export/paid evidence must come from operator-led conversations outside git. |

## Phase 23 - Open-Source Audit Case Bank

Input:

- public/open-source transaction-like datasets;
- existing SEC Form 4 pack;
- sanitized synthetic edge-case CSV exports;
- source notes that explain provenance, license/terms posture, and limitations.

Build:

- source-selection protocol in `docs/OPEN_SOURCE_CASE_BANK.md` that rejects
  cherry-picked-only case banks;
- case-pack directory convention;
- per-case source note, policy, expected limitations, and audit run command;
- batch inventory that separates positive-finding, limitation, reject, and
  edge-case packs;
- manual validation template for each pack.

Outputs:

- `docs/OPEN_SOURCE_CASE_BANK.md`;
- `demo/<case_id>/source.md`;
- `demo/<case_id>/policy.yaml`;
- `demo/<case_id>/trades.csv` or approved public fixture;
- `demo/<case_id>/output/report.md`;
- `demo/<case_id>/output/report_reviewed.md`;
- `demo/<case_id>/output/manifest.json`;
- `demo/<case_id>/output/reproducibility_status.json`;
- `docs/audit/open_source_case_reviews/<case_id>.md`.

Gate:

- at least 5 case packs exist;
- at least 3 different data shapes are represented;
- every pack has a source note, policy, report, manifest, reviewed report, and
  validation note;
- negative/limitation packs are preserved and not hidden;
- no private/customer data is committed.

Out of scope:

- hosted upload;
- checkout;
- real exchange network fetching;
- broker control;
- trading advice.

## Phase 24 - Multi-Case Report Quality Loop

Input:

- Phase 23 case packs;
- validation notes and error registers;
- existing SEC Form 4 reviewed report baseline.

Build:

- report-quality scorecard for readability, traceability, limitation clarity,
  and claim safety;
- rule/data coverage matrix showing which policies and data fields each case
  exercises;
- comparison dashboard across case packs;
- regression tests for any discovered calculation/reporting bugs;
- polished internal demo pack selected from the strongest validated cases.

Outputs:

- `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`;
- `docs/REPORT_QUALITY_SCORECARD.md`;
- `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`;
- `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md`;
- updated `demo/<case_id>/output/report_reviewed.md` for selected packs.

Gate:

- at least 3 case packs pass manual validation without P0/P1 report issues;
- at least one pack shows meaningful violations;
- at least one pack shows limitations/reject behavior;
- report wording stays non-advice and non-performance-promise;
- reproducibility is proven for selected demo packs.

Out of scope:

- broad product landing page;
- multi-tenant UI;
- automated billing;
- live monitoring.

## Phase 25 - Private Pilot Readiness

Input:

- 1-3 operator-approved private/anonymized trade exports outside git;
- written risk rules from the same operator/prospect;
- Phase 24 demo/report standards.

Build:

- private data intake checklist;
- local-only redaction and retention checklist;
- per-private-run artifact manifest that stores only safe references in git;
- reviewed report delivery checklist;
- feedback log and paid-pilot decision artifact.

Outputs:

- `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md`;
- `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`;
- `docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md`;
- `docs/PAID_PILOT_READY_GATE.md`;
- local, non-git private artifact packs under operator-controlled paths.

Gate:

- at least one private/operator-approved report is run and manually validated;
- no raw private rows, handles, account ids, credentials, or private paths are
  committed;
- delivery wording is claim-safe;
- the operator can decide whether to show the paid-pilot offer to warm users.

Out of scope:

- real exchange fetch unless T93/T94 is reopened by evidence;
- public SaaS;
- payment processor integration;
- trading advice.

## Phase 26 - Private Pilot Evidence Collection

Input:

- one operator-approved private or anonymized artifact outside git;
- written rules or approved structured policy for that artifact;
- Phase 25 intake, report-review, run-note, package, feedback, and ready-gate
  artifacts.

Build:

- one local private/anonymized audit run outside git;
- one manually reviewed private report outside git;
- safe run-note metadata only in `docs/private_pilot_runs/`;
- updated `docs/PAID_PILOT_READY_GATE.md`.

Gate:

- at least one private/anonymized report is manually reviewed with P0:0 and
  P1:0, or the operator-input blocker remains explicit;
- no raw private rows, identifiers, credentials, payment details, screenshots,
  or private paths are committed;
- delivery decision is claim-safe and operator-owned.

Out of scope:

- open-source demos as a substitute for private evidence;
- SaaS, checkout, hosted uploads, live exchange control, order blocking, or
  trading advice.

## Phase 27 - Real Open Data Rehearsal

Input:

- real public data only;
- no synthetic rows;
- `docs/REAL_OPEN_DATA_REHEARSAL_PLAN.md`;
- existing open-source case-pack validator and report-review standards.

Preferred source:

- public on-chain DEX swaps from Dune curated datasets or equivalent BigQuery
  public blockchain data.

Fallback sources:

- SEC Insider Transactions Data Sets as official disclosure reference only;
- Binance public data as market-tape control only.

Build:

- source-selection note;
- extraction contract;
- one real-open-data case pack;
- manual review note and error register;
- dashboard/coverage/ready-gate update.

Gate:

- data is real and public;
- source provenance and field mapping are explicit;
- report is truthful and reproducible;
- no synthetic rows or private data are committed;
- artifact is labeled `real_open_data_rehearsal_not_private_evidence`;
- paid-pilot ready gate remains `needs_fixes` unless T116 is separately
  completed with private/anonymized evidence.

Out of scope:

- synthetic data;
- random private-person wallet doxxing;
- PMF, customer validation, paid-pilot evidence, or market-demand claims;
- SaaS, checkout, hosted uploads, live exchange control, order blocking, or
  trading advice.

## Phase 29 - Pre-Private Hypothesis Validation

Input:

- completed open-source and real-open-data case packs;
- `docs/PAID_PILOT_READY_GATE.md` with current `needs_fixes` decision;
- no operator-approved private/anonymized export yet;
- founder/operator access to warm conversations or domain reviewers.

Build:

- evidence ladder and matrix;
- discovery script focused on past behavior and current workaround;
- report conversation pack using existing validated artifacts;
- privacy-safe evidence capture runbook;
- phase gate that decides whether to return to T116, continue concierge
  validation, narrow ICP, revise the offer, or pause/pivot.

Outputs:

- `docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md`;
- `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`;
- `docs/PRE_PRIVATE_DISCOVERY_SCRIPT_RU.md`;
- `docs/PRE_PRIVATE_REPORT_CONVERSATION_PACK.md`;
- `docs/PRE_PRIVATE_EVIDENCE_CAPTURE_RUNBOOK.md`;
- `docs/archive/PHASE29_REVIEW.md` when evidence review is complete.

Gate:

- no private/customer identifiers or raw rows enter git;
- open/demo artifacts remain technical/product evidence only;
- market evidence is based on past behavior, current workaround, export
  willingness, and concrete next steps;
- paid evidence is counted only when a paid report, repeat commitment, or
  referral exists;
- if an approved anonymized export appears, T116 becomes the active task again.

Out of scope:

- substituting report reviews for private run evidence;
- counting demo artifacts as PMF or demand;
- SaaS, checkout, hosted uploads, live exchange control, order blocking, or
  trading advice.

## Phase 30 - Concierge Validation Execution Kit

Input:

- Phase 29 validation plan, discovery script, and report conversation pack;
- no approved private/anonymized export yet;
- no aggregate outreach/report-review evidence yet.

Build:

- two-week execution plan;
- ICP targeting rubric;
- manual RU outreach templates;
- safe aggregate evidence log template;
- conversation outcome scoring rubric;
- phase review archive.

Outputs:

- `docs/CONCIERGE_VALIDATION_EXECUTION_PLAN.md`;
- `docs/ICP_OUTREACH_TARGETING_RUBRIC.md`;
- `docs/OUTREACH_MESSAGE_TEMPLATES_RU.md`;
- `docs/SAFE_AGGREGATE_EVIDENCE_LOG_TEMPLATE.md`;
- `docs/CONVERSATION_OUTCOME_SCORING_RUBRIC.md`;
- `docs/archive/PHASE30_REVIEW.md`.

Gate:

- operator can run first 10-15 conversations manually;
- contact lists and detailed notes stay outside git;
- only aggregate non-identifying evidence may be summarized;
- T116 resumes if approved anonymized/private export appears outside git;
- paid-pilot ready gate remains `needs_fixes` until private run/review evidence
  exists.

Out of scope:

- automated outreach;
- CRM or hosted forms;
- SaaS, checkout, hosted uploads, live exchange control, order blocking, or
  trading advice;
- treating templates, rubrics, or empty aggregate logs as market evidence.

## Success Criteria

Minimum useful readiness before warm prospect conversations:

- 5-10 open-source/demo packs created;
- 3+ different data shapes exercised;
- 3+ manually validated report packs;
- 0 unresolved P0/P1 report-validity findings;
- one concise internal demo pack;
- one paid-pilot offer with limitations and delivery boundary;
- private data handling checklist ready.

## Anti-Cherry-Pick Rule

Do not select only examples with impressive-looking violations. Each validation
batch must include:

- at least one positive-finding case;
- at least one limitation or reject case;
- at least one edge-case CSV/schema case;
- explicit explanation of why the source was selected.

Good validation means the report is truthful, not flattering.

The canonical Phase 23 source-selection rules live in
`docs/OPEN_SOURCE_CASE_BANK.md`. If a candidate pack conflicts with that
protocol, reject or relabel the pack before running the audit.
