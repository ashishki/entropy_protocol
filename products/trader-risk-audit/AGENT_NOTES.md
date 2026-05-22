# Agent Notes - Trader Risk Audit

Date: 2026-05-19

This file keeps only restart-relevant notes. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/archive/`,
and `docs/tasks.md`.

## Active State

- Phase: 26 Private Pilot Evidence Collection
- Last completed: T140 Dune Public Wallet Rehearsal Review
- Active task: T116 Operator-Approved Private Run And Reviewed Report Evidence
  (blocked pending operator private input)
- Baseline: 263 pass / 0 skip
- Primary roadmap: `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`

## Current Decision

The next priority is still T116 if an approved private/anonymized export exists
outside git. If it does not exist, run the Phase 30 concierge outreach loop
outside git and record only safe aggregate evidence. Phase 27, Phase 28, and
Phase 32 remain technical/report-review rehearsal evidence only.

## Operator Input Needed

- T116 is blocked until the operator supplies one approved private/anonymized
  artifact outside git;
- do not claim a private report was run or reviewed; T112 recorded only a safe
  blocker note because no operator-approved private input was supplied;
- paid-pilot ready gate is `needs_fixes`, not ready, until one private or
  anonymized report is run and manually reviewed outside git;
- collect future privacy-safe market evidence outside git before reopening T94;
- preserve the distinction between demo artifact quality and paid/customer
  validation evidence;
- Phase 29 report reviews and interviews can support product/market learning,
  but cannot make the paid-pilot ready gate `ready` without T116 evidence;
- Phase 29 is archived WARN with decision `continue_concierge_validation`
  because no aggregate outreach/report-review evidence was supplied;
- Phase 30 is archived WARN because the execution kit is ready but actual
  outreach responses/export willingness/paid evidence are still missing;
- Phase 31 is archived OK because aggregate evidence validation tooling is
  complete, but it does not create market/private/paid evidence;
- Phase 32 is archived WARN because Dune produced a useful real-public-data
  report-review artifact, but it is not private/customer/paid evidence;
- do not add real read-only exchange fetching before the T93/T94 CSV friction
  gate.

## Guardrails

- Raw private/customer trade data must not be committed.
- Phase 14/15 exchange-import work is complete but should be used only when it
  directly supports the selected real audit artifact or the T93/T94 friction
  gate.
- ADR-002 remains read-only, local, and historical only.
- No live exchange control, hosted uploads, hosted storage, checkout, order
  blocking, SaaS expansion, or trading advice.
- Phase 20 deep review found no stop-ship items; Phase 21 must keep funnel
  evidence privacy-safe and separate vanity/demo events from gate evidence.
- Phase 21 deep review found no stop-ship items. Do not implement real
  exchange network fetching unless T93 explicitly returns proceed.
- T93 returned defer, not proceed. T94-T97 remain blocked.
- Core is paused; do not open Core work from this product loop.
- Open-source validation batches must include positive, limitation/reject, and
  edge-case examples where available.

## Key Links

- `docs/CODEX_PROMPT.md`
- `docs/tasks.md`
- `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
- `docs/OPEN_SOURCE_CASE_BANK.md`
- `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md`
- `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`
- `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`
- `docs/PHASE24_REGRESSION_DECISIONS.md`
- `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md`
- `docs/archive/PHASE24_REVIEW.md`
- `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md`
- `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`
- `docs/private_pilot_runs/`
- `docs/PAID_PILOT_PACKAGE.md`
- `docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md`
- `docs/PAID_PILOT_READY_GATE.md`
- `docs/archive/PHASE25_REVIEW.md`
- `docs/archive/PHASE27_REVIEW.md`
- `demo/real_open_dex_swaps_001/`
- `docs/archive/PHASE28_REVIEW.md`
- `demo/real_open_dex_contract_sequence_001/`
- `docs/DUNE_PUBLIC_WALLET_REHEARSAL.md`
- `demo/dune_public_wallet_dex_001/`
- `docs/archive/PHASE32_REVIEW.md`
- `docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md`
- `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`
- `docs/PRE_PRIVATE_DISCOVERY_SCRIPT_RU.md`
- `docs/PRE_PRIVATE_REPORT_CONVERSATION_PACK.md`
- `docs/PRE_PRIVATE_EVIDENCE_CAPTURE_RUNBOOK.md`
- `docs/audit/PHASE23_ERROR_REGISTER.md`
- `docs/AUTOMATED_PILOT_ROADMAP.md`
- `docs/ARTIFACT_VALIDATION_ROADMAP.md`
- `docs/STARTER_POLICY_PROFILES_RU.md`
