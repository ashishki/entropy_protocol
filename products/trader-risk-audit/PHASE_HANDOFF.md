# Phase Handoff - Trader Risk Audit

Date: 2026-05-19

Use this file only for restart/context recovery. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/archive/`,
and `docs/tasks.md`.

## Current State

- Phase: 26 Private Pilot Evidence Collection
- Last completed: T140 Dune Public Wallet Rehearsal Review
- Active task: T116 Operator-Approved Private Run And Reviewed Report Evidence
  (blocked pending operator private input)
- Baseline: 263 pass / 0 skip
- Ruff: clean
- Open findings: P2 carry-forwards only; no P0/P1. Phase 23, Phase 25, Phase
  27, Phase 28, and Phase 32 caveats remain accepted/blocked limitations.
- Constraint state: T93 deferred real local read-only exchange fetching; Phase
  22 implementation tasks are blocked. Core is paused.
- Branch: product-local working branch

## Next Action

Read:

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md` Phase 26, T116
3. `docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md`
4. `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
5. `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`
6. `docs/PRE_PRIVATE_DISCOVERY_SCRIPT_RU.md`
7. `docs/PRE_PRIVATE_REPORT_CONVERSATION_PACK.md`
8. `docs/PRE_PRIVATE_EVIDENCE_CAPTURE_RUNBOOK.md`
9. `docs/PRE_PRIVATE_OUTREACH_EVIDENCE_REVIEW.md`
10. `docs/PAID_PILOT_READY_GATE.md`

Start T116 only after operator private input exists outside git. If it does not
exist, run the Phase 30 concierge outreach loop outside git and validate
aggregate logs with `evidence aggregate-validate` before promoting summaries.
The Dune report can support report-review conversations, but it is not
private/customer/paid evidence.
T98 created `docs/OPEN_SOURCE_CASE_BANK.md` with the
source-selection protocol, allowed/excluded source classes, license/terms
notes, anti-cherry-pick batch composition, and artifact-quality-only evidence
boundary. T99 added `trader_risk_audit.validation.open_source_case`,
`case-bank validate`, focused validator tests, and
`demo/open_source_sec_form4_001/output/reproducibility_status.json` so the SEC
Form 4 pack passes the directory contract. T100 listed five candidate packs in
`docs/OPEN_SOURCE_CASE_BANK.md`: SEC reference, `public_sample_001`,
`risk_audit_case_001`, `synthetic_limit_leverage_001`, and
`synthetic_schema_reject_missing_price_001`. T101 generated complete runnable
artifacts/status for SEC, public sample, risk audit, and synthetic leverage
limitation packs; rejected the missing-price schema pack with only
`output/run_status.json`; and wrote `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md`.
T102 added per-pack review notes under
`docs/audit/open_source_case_reviews/`, `docs/audit/PHASE23_ERROR_REGISTER.md`,
and reviewed-report limitation/provenance headers. Current register is P0:0,
P1:0, P2:3. T103 archived `docs/archive/PHASE23_REVIEW.md`, updated audit
index/state docs, and advanced to Phase 24 with no stop-ship findings. T104
added `docs/REPORT_QUALITY_SCORECARD.md`; SEC Form 4 reviewed report scored
17/18 with no fail condition as internal reference. T105 added
`docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`, mapping packs to rules, fields,
unsupported fields, limitations, output sections, and explicit follow-up
coverage cases. T106 added `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`,
classifying three controlled internal demo-quality packs, one internal
reference pack, and one blocked/rejection-only pack. T107 added
`evidence_overclaim` claim-guard phrases/tests and
`docs/PHASE24_REGRESSION_DECISIONS.md`; baseline is now 258 passing tests.
T108 added `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md` with positive,
limitation, and schema-reject examples plus safe excerpts, talk track, buyer
promise, and paid-pilot ask. T109 archived Phase 24 with Stop-Ship: No,
P0:0, P1:0, P2:3 accepted carry-forward caveats, and advanced to Phase 25.
T110 added `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md` and linked it from
`docs/PILOT_INTAKE_CONTRACT_RU.md`; it maps private intake to existing local
CLI commands and forbids committing private rows, identifiers, credentials,
private paths, and unapproved screenshots. Build the private report review
checklist next. T111 added `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md` and
scorecard linkage; unresolved P0/P1 truth, privacy, policy, advice,
live-control, or performance-claim issues block delivery. T112 added
`docs/private_pilot_runs/` with a safe run-note template and a blocker note:
no operator-approved private/anonymized input was supplied, no private report
was run or reviewed, and delivery remains `blocked_do_not_deliver`. T113 added
`docs/PAID_PILOT_PACKAGE.md` and
`docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md` for one manual reviewed audit,
safe feedback capture, no checkout, no SaaS, no live-control, no order
blocking, and no advice/performance claims. T114 added
`docs/PAID_PILOT_READY_GATE.md` with decision `needs_fixes`, not ready, because
no operator-approved private/anonymized report has been run and manually
reviewed. T115 archived Phase 25 with Stop-Ship: No, P0:0, P1:0, P2:4 and WARN
health. T116 remains the specific blocking fix for private delivery readiness:
one operator-approved
private/anonymized local run and manually reviewed report, with only safe
metadata committed. T117-T121 completed Phase 27 real-open-data rehearsal using
real Ethereum mainnet Uniswap V2 WETH/USDC pair-level Swap logs. The pack
`demo/real_open_dex_swaps_001/` is reproducible and manually reviewed with
P0:0, P1:0, P2:2 accepted caveats; it is development rehearsal only and does
not close T116.
T122 added `demo/real_open_dex_contract_sequence_001/`, using the same real
Uniswap V2 WETH/USDC source filtered to one repeated public contract recipient.
It is reproducible and manually reviewed with P0:0, P1:0, P2:2 accepted
caveats. It is development rehearsal only and does not close T116. T123-T125
started Phase 29 with an evidence ladder, evidence matrix, RU discovery script,
report conversation pack, and evidence capture runbook. T126 found no supplied
aggregate outreach/report-review evidence and chose
`continue_concierge_validation`. T127 archived Phase 29 with WARN health,
Stop-Ship: No, P0:0, P1:0, P2:1. T128-T132 added the Phase 30 concierge
validation execution kit and archived it with WARN health, Stop-Ship: No,
P0:0, P1:0, P2:1. T133-T136 added Phase 31 aggregate evidence safety tooling
and archived it with OK health, Stop-Ship: No, P0:0, P1:0, P2:0. T137-T140
added `demo/dune_public_wallet_dex_001/`, a Dune public Ethereum `dex.trades`
case pack with 80 real public rows, 76 max-position findings, one unsupported
leverage limitation, passed reproducibility, and P0:0, P1:0, P2:2 accepted
caveats. It is report-review/development evidence only and does not close T116.
T94-T97 are
blocked until future privacy-safe market evidence reopens T93. Phase 17 added deterministic local
`intake_session.json`,
sanitized `schema_profile.json`, safe `intake_report.md`, and Cycle 22 deep
review/archive with no stop-ship items. T74 added
`trader_risk_audit/policy/rule_catalog.py` for supported deterministic rule
types, threshold units, safe descriptions, starter profile applicability, and
availability requirements. T75 added `trader_risk_audit/policy/builder.py`
and `policy build` for deterministic generated `policy.yaml`. T76 added
`policy flow` for structured local rule-builder input and unavailable-rule
explanations. T77 added `policy unsupported append` and
`trader_risk_audit/policy/unsupported_register.py` for sanitized manual-review
limitations. T78 archived Cycle 23 with no stop-ship findings. T79 added
`trader_risk_audit/audit_session/runner.py` and `audit-session run`, which
gates on runnable intake/policy status, runs the deterministic audit internals,
and writes safe complete/blocked `run_status.json` without raw rows in
status/stdout. T80 added `trader_risk_audit/audit_session/artifact_bundle.py`
and `audit-session bundle`, which writes/validates `bundle_index.json` with
safe refs, hashes, status, preview state, and limitation register refs. T81
added `trader_risk_audit/audit_session/reproducibility.py`, which reruns a
session in a separate output directory and writes safe
`reproducibility_status.json` before preview/delivery. T82 archived Cycle 24
with P0:0, P1:0, P2:0 and no stop-ship items.
T83 added `trader_risk_audit/preview/model.py` and `preview build`, which
renders claim-safe redacted previews from bundle refs without source-row ids,
symbols, raw rows, or private output paths in CLI stdout. T84 added eligible
manual paid-pilot CTA packaging without checkout/SaaS/payment processing. T85
added privacy-safe preview conversion events and summary. T86 added local
paid-unlock state transitions with manual evidence references only. T87
archived Cycle 25 with P0:0, P1:0, P2:0 and no stop-ship items. T88 added
`HypothesisFunnelEvent`, combined legacy/new evidence loading, and docs that
separate gate evidence from vanity/demo events.
T89 added `evidence hypothesis-dashboard`, which summarizes legacy and funnel
evidence locally with market/demo separation, ratios, gate status, blocker tags,
and privacy-safe next action output.
T90 added `evaluate_hypothesis_gate`, which returns proceed,
needs_more_evidence, or pivot with concrete reasons and next action.
T91 added `evidence export`, which writes aggregate-only CSV/Markdown evidence
summaries with gate decision, safe tags, source log names, and source log
hashes while rejecting identifiers, phone numbers, credentials, payment ids,
raw-row-like fields, and private paths.
T92 archived Cycle 26 with P0:0, P1:0, P2:0 and no stop-ship items. Do not
implement real exchange network fetching unless T93 explicitly returns proceed.
T93 returned defer because no market customer evidence log shows CSV/export
friction as the binding blocker.

## Guardrails

- Raw private/customer trade data must not be committed.
- Phase 14/15 exchange-import work is complete but should be used only when it
  directly supports the selected real audit artifact or the T93/T94 friction
  gate.
- ADR-002 allows only local read-only historical ingestion.
- No live exchange control, order placement, hosted uploads, hosted storage,
  checkout, order blocking, SaaS expansion, or trading advice.
- Open-source validation must preserve positive, limitation/reject, and
  edge-case examples to avoid cherry-picking.

## Historical Pointers

- Completed through T140. T94-T97 blocked. Active route is T116 if approved
  private input appears; otherwise run Phase 30 concierge outreach
  outside git.
- New active roadmap: `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`.
- Detailed validation command history is in `docs/IMPLEMENTATION_JOURNAL.md`.
- Prior review artifacts are in `docs/archive/`.
