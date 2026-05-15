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

## Phase 23 - Open-Source Audit Case Bank

Input:

- public/open-source transaction-like datasets;
- existing SEC Form 4 pack;
- sanitized synthetic edge-case CSV exports;
- source notes that explain provenance, license/terms posture, and limitations.

Build:

- source-selection protocol that rejects cherry-picked-only case banks;
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
