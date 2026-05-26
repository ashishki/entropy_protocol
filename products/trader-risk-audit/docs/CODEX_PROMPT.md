# CODEX_PROMPT.md

Version: 1.97
Date: 2026-05-19
Phase: Phase 26

This file is the compact session state for AI development. Do not paste long
history here; use links below.

## Current Phase

- Phase: Phase 26
- Name: Private Pilot Evidence Collection
- Business goal: collect and review one operator-approved private/anonymized
  report outside git, then update only safe run-note and ready-gate summaries.
- Phase gate: at least one private/anonymized report is manually reviewed with
  safe metadata only, or the operator-input blocker remains explicit.

## Current State

- Baseline: 263 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
- Last updated: 2026-05-19
- Open findings: P2 carry-forwards only; no P0/P1. Phase 29 added PH29-P2-001
  and Phase 30 added PH30-P2-001: no privacy-safe aggregate
  market/report-review/outreach evidence has been supplied yet. Phase 31 added
  no new findings. Phase 32 added PH32-P2-001 and PH32-P2-002 as accepted
  public-Dune source-shape limitations.
- Current priority: T116 remains blocked until one operator-approved
  private/anonymized export exists outside git. Until then, run the Phase 29
  concierge validation loop outside git and record only safe aggregate evidence.
- Last completed: T140 Dune Public Wallet Rehearsal Review

## Read First

1. `docs/tasks.md` Phase 26, T116
2. `docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md`
3. `docs/PRE_PRIVATE_OUTREACH_EVIDENCE_REVIEW.md`
4. `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
5. `docs/AUTOMATED_PILOT_ROADMAP.md`
6. `docs/IMPLEMENTATION_CONTRACT.md`
7. `docs/PILOT_INTAKE_CONTRACT_RU.md`
8. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
- `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md`
- `docs/audit/PHASE23_ERROR_REGISTER.md`
- `docs/audit/open_source_case_reviews/`
- `docs/ARTIFACT_VALIDATION_ROADMAP.md` and Phase 16 artifacts for the
  completed SEC open-source validation baseline
- `docs/STARTER_POLICY_PROFILES_RU.md` for `soft`, `medium`, and `hard`
  starter audit presets
- `docs/REAL_OPEN_DATA_REHEARSAL_PLAN.md` for the planned real-public-data
  rehearsal route
- `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`
- `docs/PRE_PRIVATE_DISCOVERY_SCRIPT_RU.md`
- `docs/PRE_PRIVATE_REPORT_CONVERSATION_PACK.md`
- `docs/PRE_PRIVATE_EVIDENCE_CAPTURE_RUNBOOK.md`
- `docs/PRE_PRIVATE_OUTREACH_EVIDENCE_REVIEW.md`
- `docs/archive/PHASE29_REVIEW.md`
- `docs/CONCIERGE_VALIDATION_EXECUTION_PLAN.md`
- `docs/ICP_OUTREACH_TARGETING_RUBRIC.md`
- `docs/OUTREACH_MESSAGE_TEMPLATES_RU.md`
- `docs/SAFE_AGGREGATE_EVIDENCE_LOG_TEMPLATE.md`
- `docs/CONVERSATION_OUTCOME_SCORING_RUBRIC.md`
- `docs/archive/PHASE30_REVIEW.md`
- `docs/AGGREGATE_EVIDENCE_VALIDATION_CLI.md`
- `docs/archive/PHASE31_REVIEW.md`
- `docs/DUNE_PUBLIC_WALLET_REHEARSAL.md`
- `docs/archive/PHASE32_REVIEW.md`
- Supporting cross-product cognition vault on this VPS:
  `/srv/codex-entropy/repos/product-3/engineering-cognition-vault/10-projects/entropy-protocol.md`.
  Product-local docs remain authoritative.

## Next Task

T116 Operator-Approved Private Run And Reviewed Report Evidence

Immediate intent:

- blocked until the operator supplies one approved private/anonymized artifact
  outside git;
- if supplied, run the local audit workflow only against that outside-git
  artifact and update safe metadata only;
- if not supplied, continue Phase 29 operator-led discovery/report review
  outside git and record only aggregate non-identifying evidence; the Dune
  public wallet report may be used as a report-review conversation artifact
  only, not as private/customer/paid evidence;
- do not commit private rows, identifiers, credentials, private paths,
  screenshots, payment identifiers, wallet ownership claims, or customer notes.

## Active Guardrails

- Phase 14/15 exchange-import work is complete but should run only when it
  directly supports the selected real audit artifact or the T93/T94 friction
  gate.
- Public/open-source artifact validation is allowed when private data is not
  supplied, but it is not paid pilot, PMF, or customer validation evidence.
- Phase 29 interviews and report reviews can support product/market learning,
  but they do not approve private report delivery unless T116 input exists.
- ADR-001 keeps Telegram as constrained demo/intake/delivery only.
- ADR-002 allows local read-only historical fill ingestion only.
- Phases 20-21 must stay local-first and deterministic: no SaaS accounts,
  hosted uploads, checkout, hosted storage, or background network import.
- No SaaS accounts, checkout, exchange write APIs, broker control, order
  blocking, signal analytics, AI advice, or live trading behavior.
- Core is paused; do not open Core tasks from this workspace.
- Phase 26 must preserve Phase 23/24/25 limitations: SEC source limits, public
  sample P&L wording, synthetic provenance, missing leverage, schema reject
  cases, open-source artifact-quality-only boundaries, and the Phase 25
  `needs_fixes` paid-pilot gate stay visible.

## Historical Pointers

- Completed through T140; details are in `docs/IMPLEMENTATION_JOURNAL.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/archive/`, and `docs/tasks.md`.
- T94-T97 remain blocked by T93 defer.
- Active planned work is T116. It remains blocked until operator private input
  exists outside git. Phase 29 provides the fallback concierge validation loop
  for collecting aggregate market/report-review evidence.
- Phase 23 follows `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`.
- Public sample and starter profile context lives in
  `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`,
  `docs/INTERNAL_VALIDATION_REVIEW_RU.md`, and
  `docs/STARTER_POLICY_PROFILES_RU.md`.
- Phase 19 added `audit-session run`, `audit-session bundle`, and a
  reproducibility gate. Cycle 24 deep review found P0:0, P1:0, P2:0,
  Stop-Ship: No.
- T83 added `preview build`, which renders a claim-safe redacted Markdown
  preview from a completed artifact bundle using counts, rule categories,
  limitation refs, and safe source coverage only.
- T84 added eligible manual paid-pilot CTA packaging for previews with
  48-72 hour turnaround, $49-$149 price hypothesis, and no checkout/SaaS scope.
- T85 added privacy-safe preview conversion events and local CLI append/summary
  without counting demo/open-source samples as market CTA evidence.
- T86 added a local paid unlock state machine and CLI status flow without
  checkout, accounts, payment identifiers, or unreviewed delivery.
- Cycle 25 deep review found P0:0, P1:0, P2:0, Stop-Ship: No.
- T88 added safe hypothesis funnel events, legacy customer-log coexistence,
  and docs defining gate evidence versus vanity/demo events.
- T89 added a local hypothesis dashboard CLI with market/demo separation,
  ratios, blocker tags, gate status, and safe next action output.
- T90 added explicit proceed / needs-more-evidence / pivot gate evaluation and
  docs warning that uploads/API connections alone are not PMF.
- T91 added privacy-safe CSV/Markdown evidence export with aggregate metrics,
  gate verdict, safe tags, source log names, and source log hashes.
- Cycle 26 deep review found P0:0, P1:0, P2:0, Stop-Ship: No.
- T93 deferred real local read-only exchange fetching because no market
  evidence log showed CSV/export friction as the binding blocker. T94-T97 are
  blocked.
- T98 added `docs/OPEN_SOURCE_CASE_BANK.md` with allowed/excluded source
  classes, license/terms notes, anti-cherry-pick batch composition, and the
  artifact-quality-only evidence boundary.
- T99 added `trader_risk_audit.validation.open_source_case`, `case-bank
  validate`, focused tests, and a committed SEC Form 4 reproducibility status
  artifact. The passing baseline is 256 tests.
- T100 listed five candidate packs in `docs/OPEN_SOURCE_CASE_BANK.md`,
  including positive, limitation, reject, and edge/schema cases across
  disclosure-like, broker/export-like, and malformed edge-case data shapes.
- T101 generated runnable artifacts/status for four packs, rejected the missing
  price schema pack without partial report claims, and added
  `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md`.
- T102 added per-pack review notes, `docs/audit/PHASE23_ERROR_REGISTER.md`,
  and reviewed-report limitation/provenance headers. Current register:
  P0:0, P1:0, P2:3.
- T103 archived Phase 23 review in `docs/archive/PHASE23_REVIEW.md`.
  Stop-Ship: No; P0:0, P1:0, P2:3. Phase 24 may proceed.
- T104 added `docs/REPORT_QUALITY_SCORECARD.md`; SEC Form 4 reviewed report
  scored 17/18 with no fail condition as internal reference.
- T105 added `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`, mapping packs to
  rule types, fields, unsupported fields, limitations, output sections, and
  explicit follow-up cases for drawdown-only, session-timezone, P&L wording,
  and no-breach coverage. Leverage and fee-specific rules remain accepted
  limitations unless future data supports them.
- T106 added `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`; it classifies
  `public_sample_001`, `risk_audit_case_001`, and
  `synthetic_limit_leverage_001` as controlled internal demo-quality, keeps
  SEC Form 4 as internal reference only, keeps the missing-price pack
  blocked/rejection-only, and names a session-timezone boundary case as the
  next concrete gap.
- T107 added `evidence_overclaim` claim-guard phrases and tests for unsafe
  open-source/demo wording such as "proves PMF" and "demo evidence proves
  customer demand"; negative boundary language remains allowed. Baseline is
  258 passing tests.
- T108 added `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md` with a positive
  pack, limitation pack, schema-reject explanation, safe excerpts, talk track,
  buyer promise, paid-pilot ask, and explicit forbidden claims.
- T109 archived Phase 24 in `docs/archive/PHASE24_REVIEW.md`. Stop-Ship: No;
  P0:0, P1:0, P2:3 accepted carry-forward caveats. Phase 25 may begin with
  private intake/redaction and report-review readiness, not SaaS or unreviewed
  delivery.
- T110 added `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md` and linked it from
  `docs/PILOT_INTAKE_CONTRACT_RU.md`; it defines allowed files, forbidden
  data, redaction, local storage, deletion trigger, operator approval, stop
  conditions, and existing local CLI command mapping.
- T111 added `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md` and linked private
  pilot use from `docs/REPORT_QUALITY_SCORECARD.md`; unresolved P0/P1 report
  truth, privacy, policy, advice, live-control, or performance-claim issues
  block delivery.
- T112 added `docs/private_pilot_runs/` with a safe run-note template and a
  blocker note recording that no operator-approved private/anonymized input was
  supplied in repo-visible context. Delivery remains
  `blocked_do_not_deliver`; no private report has been run or reviewed.
- T113 added `docs/PAID_PILOT_PACKAGE.md` and
  `docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md`; the package keeps the offer to
  one manual reviewed audit with no checkout/SaaS/live-control/advice scope,
  and the feedback template records only safe aggregate evidence.
- T114 added `docs/PAID_PILOT_READY_GATE.md`; decision is `needs_fixes` because
  no operator-approved private/anonymized report has been run and reviewed.
  The first-user ask and delivery promise are drafted, but SaaS, checkout,
  live-control, order blocking, advice, and unreviewed delivery remain
  forbidden.
- T115 archived Phase 25 in `docs/archive/PHASE25_REVIEW.md`. Stop-Ship: No;
  P0:0, P1:0, P2:4. Phase 25 artifacts are safe and complete, but paid-pilot
  delivery readiness remains `needs_fixes`. T116 is blocked pending one
  operator-approved private/anonymized artifact outside git.
- On 2026-05-19, the operator clarified that synthetic data should not be used
  for the fallback rehearsal. `docs/REAL_OPEN_DATA_REHEARSAL_PLAN.md` now
  defines a planned Phase 27 route using real public data only, preferably
  public on-chain DEX swaps, while preserving that it is not private, paid,
  customer, PMF, or market-demand evidence.
- T117-T121 completed Phase 27 real-open-data rehearsal using real Ethereum
  mainnet Uniswap V2 WETH/USDC pair-level Swap logs. The new case pack
  `demo/real_open_dex_swaps_001/` is reproducible and manually reviewed with
  P0:0, P1:0, P2:2 accepted caveats. Phase 27 is archived in
  `docs/archive/PHASE27_REVIEW.md`. T116 remains blocked and the ready gate
  remains `needs_fixes`.
- T122 completed Phase 28 account-scoped real-open-data rehearsal using real
  Uniswap V2 WETH/USDC swaps filtered to one repeated public contract
  recipient. `demo/real_open_dex_contract_sequence_001/` is reproducible,
  manually reviewed, and archived in `docs/archive/PHASE28_REVIEW.md` with
  P0:0, P1:0, P2:2 accepted caveats. T116 remains blocked and the ready gate
  remains `needs_fixes`.
- T123-T125 started Phase 29 pre-private hypothesis validation. They added an
  evidence ladder, evidence matrix, RU discovery script, report conversation
  pack, and evidence capture runbook. This work strengthens validation
  discipline while T116 is blocked, but it does not make the paid-pilot gate
  ready.
- T126 reviewed Phase 29 outreach evidence and found no supplied aggregate
  problem-interview, report-review, export-willingness, manual-pilot, or
  approved-export evidence. Decision: `continue_concierge_validation`.
- T127 archived Phase 29 in `docs/archive/PHASE29_REVIEW.md`. Stop-Ship: No;
  P0:0, P1:0, P2:1. T116 remains blocked and `docs/PAID_PILOT_READY_GATE.md`
  remains `needs_fixes`.
- T128-T132 completed Phase 30 concierge validation execution kit with
  targeting rubric, RU outreach templates, safe aggregate evidence template,
  outcome scoring rubric, and archive review. Stop-Ship: No; P0:0, P1:0,
  P2:1. It enables operator outreach but does not create market/paid/private
  evidence.
- T133-T136 completed Phase 31 aggregate evidence safety tooling. Added
  `evidence aggregate-validate`, schema/tag/privacy validation, tests, docs,
  and archive review. Stop-Ship: No; P0:0, P1:0, P2:0. It reduces aggregate
  log privacy risk but does not create market/paid/private evidence. Baseline
  is 263 passing tests.

## Maintenance Rule

At every phase boundary update only:

- current phase;
- baseline and validation status;
- next task;
- open findings;
- links if canonical docs move.

Do not append long task logs here.
