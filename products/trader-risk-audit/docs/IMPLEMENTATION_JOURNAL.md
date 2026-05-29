# Implementation Journal - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-19
Status: append-only

This file records durable handoff context across agents and sessions. It is not the source of truth for architecture, policy, or task contracts.

---

## Journal Entry Template

```markdown
### YYYY-MM-DD - TNN - Short Title

- Scope: files, directories, or task ids
- Why this work happened: reason or trigger
- Decisions applied: Decision Log or ADR refs, or "none"
- Evidence collected: tests, evals, review reports, or manual checks
- Follow-ups: next task, open risk, or "none"
- Notes for next agent: only context worth carrying forward
```

## Entries

### 2026-05-19 - T137-T140 - Dune Public Wallet Rehearsal

- Scope: `demo/dune_public_wallet_dex_001/`,
  `docs/DUNE_PUBLIC_WALLET_REHEARSAL.md`,
  `docs/audit/real_open_data_case_reviews/dune_public_wallet_dex_001.md`,
  `docs/audit/PHASE32_ERROR_REGISTER.md`,
  `docs/archive/PHASE32_REVIEW.md`, and state docs.
- Why this work happened: the operator supplied Dune API access and asked to
  use real public data while no T116 private/anonymized export exists.
- Decisions applied: Dune public `dex.trades` rows can strengthen technical
  and report-review confidence, but they cannot be counted as private,
  customer, paid, PMF, market-demand, or willingness-to-pay evidence.
- Evidence collected: Dune API SQL execution succeeded; 80 real public
  Ethereum DEX rows were transformed into canonical audit input; reviewed
  report records 76 max-position findings and one unsupported leverage
  limitation; reproducibility status is passed; `case-bank validate` passed.
- Follow-ups: use the reviewed Dune report only for report-review
  conversations and record only aggregate non-identifying outcomes. Return to
  T116 if an approved private/anonymized export appears outside git.
- Notes for next agent: do not commit or document the supplied Dune key. The
  key was pasted in chat and should be rotated by the operator.

### 2026-05-19 - T136 - Aggregate Evidence Safety Tooling Review

- Scope: `docs/archive/PHASE31_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`,
  `AGENT_NOTES.md`, `MEMORY.md`.
- Why this work happened: Phase 31 needed a boundary review after adding local
  aggregate evidence validation tooling.
- Decisions applied: validator success is not market, private, paid, or PMF
  evidence; T116 remains blocked until approved private/anonymized export
  exists outside git.
- Evidence collected: focused aggregate validator tests passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 263 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: operator should run outreach outside git, validate aggregate logs
  locally, and resume T116 if approved anonymized/private export appears.
- Notes for next agent: Phase 31 is safety tooling only and should not be
  described as customer validation.

### 2026-05-19 - T133-T135 - Aggregate Evidence Safety Tooling

- Scope: `trader_risk_audit/evidence.py`, `trader_risk_audit/cli.py`,
  `tests/unit/evidence/test_aggregate_evidence.py`,
  `tests/integration/test_aggregate_evidence_cli.py`,
  `docs/AGGREGATE_EVIDENCE_VALIDATION_CLI.md`,
  `docs/SAFE_AGGREGATE_EVIDENCE_LOG_TEMPLATE.md`.
- Why this work happened: Phase 30 created an aggregate evidence template, but
  future logs needed local validation before any aggregate summary enters
  git-visible docs.
- Decisions applied: safety-only local tooling is allowed; no outreach
  automation, CRM, hosted forms, SaaS, checkout, live-control, order blocking,
  advice, or customer evidence claim.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/evidence/test_aggregate_evidence.py
  tests/integration/test_aggregate_evidence_cli.py -q --tb=short` -> 5 passed.
- Follow-ups: T136 archive/review, then operator-led outreach outside git.
- Notes for next agent: `evidence aggregate-validate` prints only aggregate
  counts and does not echo private input paths.

### 2026-05-19 - T132 - Concierge Validation Execution Review

- Scope: `docs/archive/PHASE30_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`,
  `AGENT_NOTES.md`, `MEMORY.md`.
- Why this work happened: The operator asked to continue phases without
  stopping; since T116 remains blocked, Phase 30 prepared the operator
  execution loop for collecting real aggregate validation evidence.
- Decisions applied: T116 remains blocked until approved private/anonymized
  export exists outside git; no new product automation is justified without
  outreach evidence.
- Evidence collected: docs-only phase review; no private data processed.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: operator should run the outreach loop outside git; resume T116
  if an approved anonymized/private export appears.
- Notes for next agent: Phase 30 completed with WARN health because it provides
  execution materials only, not actual customer/market/paid evidence.

### 2026-05-19 - T128-T131 - Concierge Validation Execution Kit

- Scope: `docs/CONCIERGE_VALIDATION_EXECUTION_PLAN.md`,
  `docs/ICP_OUTREACH_TARGETING_RUBRIC.md`,
  `docs/OUTREACH_MESSAGE_TEMPLATES_RU.md`,
  `docs/SAFE_AGGREGATE_EVIDENCE_LOG_TEMPLATE.md`,
  `docs/CONVERSATION_OUTCOME_SCORING_RUBRIC.md`.
- Why this work happened: Phase 29 ended with `continue_concierge_validation`
  but no aggregate evidence. The next useful docs work was to remove execution
  ambiguity for the operator's first 10-15 conversations.
- Decisions applied: manual founder-led validation before automation; no
  identifiers or raw private data in git; no SaaS/checkout/live-control/advice.
- Evidence collected: docs-only update; no product code changed.
- Follow-ups: T132 archive/review, then operator-led outreach outside git.
- Notes for next agent: The execution kit is not market evidence by itself.

### 2026-05-19 - T127 - Pre-Private Hypothesis Validation Review

- Scope: `docs/archive/PHASE29_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`,
  `AGENT_NOTES.md`, `MEMORY.md`.
- Why this work happened: Phase 29 needed a boundary review after the
  pre-private evidence system and T126 zero-evidence review.
- Decisions applied: Phase 29 decision is `continue_concierge_validation`;
  T116 remains blocked until approved private/anonymized export exists outside
  git.
- Evidence collected: docs-only phase review; no private data processed.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run operator-led discovery/report-review loop outside git, or
  resume T116 if approved anonymized export appears.
- Notes for next agent: Phase 29 completed with WARN health because market and
  paid evidence are still missing, not because of a product-code defect.

### 2026-05-19 - T126 - Pre-Private Outreach Evidence Review

- Scope: `docs/PRE_PRIVATE_OUTREACH_EVIDENCE_REVIEW.md`,
  `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`,
  `docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md`,
  `docs/PAID_PILOT_READY_GATE.md`.
- Why this work happened: The operator asked to proceed without private export;
  the only honest next step was to review whether aggregate outreach/report
  review evidence exists.
- Decisions applied: no aggregate rows were supplied; decision is
  `continue_concierge_validation`, not `return_to_t116`.
- Evidence collected: privacy review found no private rows, identifiers,
  screenshots, private paths, payment identifiers, wallet ownership claims,
  account ids, emails, handles, or customer notes committed.
- Follow-ups: collect safe aggregate evidence outside git using Phase 29
  scripts/runbook; resume T116 if an approved anonymized export appears.
- Notes for next agent: Do not mark the paid gate ready from this review. It is
  a zero-evidence review, not customer validation.

### 2026-05-19 - T125 - Pre-Private Evidence Capture Runbook

- Scope: `docs/PRE_PRIVATE_EVIDENCE_CAPTURE_RUNBOOK.md`,
  `docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md`,
  `docs/PAID_PILOT_READY_GATE.md`, state docs.
- Why this work happened: The operator asked what can support product
  hypothesis validation while no private/anonymized export is available yet.
- Decisions applied: T116 remains blocked; Phase 29 evidence can support
  product/market learning but cannot approve private report delivery.
- Evidence collected: docs-only update; no product code changed. Boundary
  rules now classify pre-private evidence as technical, product, market, paid,
  or blocked private evidence.
- Follow-ups: T126 should review only privacy-safe aggregate market/report
  review evidence. If an approved anonymized export exists outside git, return
  to T116.
- Notes for next agent: Do not commit names, handles, wallet ownership claims,
  account ids, raw rows, screenshots, private paths, payment identifiers, or
  private notes.

### 2026-05-19 - T124 - Discovery And Report Review Kit

- Scope: `docs/PRE_PRIVATE_DISCOVERY_SCRIPT_RU.md`,
  `docs/PRE_PRIVATE_REPORT_CONVERSATION_PACK.md`.
- Why this work happened: Phase 29 needed an operator-ready script for
  problem interviews, report review sessions, export willingness asks, and
  manual pilot asks.
- Decisions applied: use past-behavior questions only; open/demo reports are
  product review artifacts, not private/paid/PMF proof.
- Evidence collected: docs-only update; no product code changed.
- Follow-ups: collect aggregate evidence outside git using the runbook before
  T126 review.
- Notes for next agent: The report conversation pack points to existing
  validated reports and requires the operator to say the limitation boundary
  aloud.

### 2026-05-19 - T123 - Pre-Private Hypothesis Evidence Plan

- Scope: `docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md`,
  `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md`, `docs/tasks.md`.
- Why this work happened: The operator asked for a detailed plan to strengthen
  the hypothesis and product evidence before a private export exists.
- Decisions applied: T116 remains the only path to private report readiness;
  Phase 29 runs as pre-private validation while T116 is blocked.
- Evidence collected: docs-only update; no product code changed.
- Follow-ups: T124/T125 prepare discovery and safe capture; T126 reviews
  aggregate evidence when available.
- Notes for next agent: The strongest non-private evidence is report usefulness
  review, past-behavior pain, export willingness, and manual pilot acceptance.

### 2026-05-19 - T122 - Account-Scoped Real Open Data Rehearsal

- Scope: `demo/real_open_dex_contract_sequence_001/`,
  `docs/REAL_OPEN_DATA_ACCOUNT_SCOPED_REHEARSAL.md`,
  `docs/audit/real_open_data_case_reviews/real_open_dex_contract_sequence_001.md`,
  `docs/audit/PHASE28_ERROR_REGISTER.md`, `docs/archive/PHASE28_REVIEW.md`,
  dashboard/coverage/ready-gate/state docs.
- Why this work happened: The operator asked to proceed toward more
  account-like open data; Dune CSV/API access requires an API key, so the
  no-key route used real public logs filtered to a repeated contract recipient.
- Decisions applied: Phase 27 real-open-data plan; T116 remains blocked; ready
  gate remains `needs_fixes`.
- Evidence collected: generated 40 transformed rows from 54 real Ethereum
  mainnet Uniswap V2 WETH/USDC `Swap` logs filtered to a public contract
  recipient verified by `eth_getCode`; audit generated complete artifacts;
  rerun manifest content hash matched; `case-bank validate --case-dir
  demo/real_open_dex_contract_sequence_001` passed. Review found P0:0, P1:0,
  P2:2 accepted source-shape/fees-P&L caveats.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  `case-bank validate` passed for both `real_open_dex_swaps_001` and
  `real_open_dex_contract_sequence_001`. Boundary scan found only negative
  boundary language.
- Follow-ups: T116 remains blocked until operator private/anonymized input
  exists outside git.
- Notes for next agent: This pack is closer to account-scoped than pair-level
  flow, but it is still not a verified trader ledger and cannot count as
  private/paid/customer/PMF/market-demand evidence.

### 2026-05-19 - T121 - Real Open Data Rehearsal Gate Update

- Scope: `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`,
  `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`,
  `docs/PAID_PILOT_READY_GATE.md`, `docs/archive/PHASE27_REVIEW.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/META_ANALYSIS.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/audit/AUDIT_INDEX.md`, state docs.
- Why this work happened: Phase 27 needed to record what the real-open-data
  rehearsal proves and does not prove before returning to the T116 blocker.
- Decisions applied: Phase 27 real-open-data plan; Phase 25 ready gate
  `needs_fixes`; T93 defer decision.
- Evidence collected: Cycle 30 review found Stop-Ship: No, P0:0, P1:0, P2:2.
  Dashboard and coverage matrix include `real_open_dex_swaps_001` as
  development rehearsal only. `docs/PAID_PILOT_READY_GATE.md` remains
  `needs_fixes`. `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m trader_risk_audit.cli case-bank validate --case-dir
  demo/real_open_dex_swaps_001` -> passed. Boundary scans found only negative
  boundary language and forbidden-data exclusions.
- Follow-ups: T116 remains blocked until operator private/anonymized input
  exists outside git.
- Notes for next agent: Do not count Phase 27 as private, paid-pilot,
  customer-validation, PMF, market-demand, or willingness-to-pay evidence.

### 2026-05-19 - T119/T120 - Real Open Data Case Pack And Review

- Scope: `demo/real_open_dex_swaps_001/`,
  `docs/audit/real_open_data_case_reviews/real_open_dex_swaps_001.md`,
  `docs/audit/PHASE27_ERROR_REGISTER.md`, `docs/tasks.md`.
- Why this work happened: Phase 27 needed one real, public, non-synthetic
  rehearsal pack and manual review while T116 remains blocked on private input.
- Decisions applied: `docs/REAL_OPEN_DATA_SOURCE_SELECTION.md`,
  `docs/REAL_OPEN_DATA_EXTRACTION_CONTRACT.md`.
- Evidence collected: generated 40 transformed rows from real Ethereum mainnet
  Uniswap V2 WETH/USDC `Swap` logs; `audit` generated report, violations,
  attribution, manifest, and delivery packet; rerun manifest content hash
  matched; `case-bank validate --case-dir demo/real_open_dex_swaps_001` passed.
  T120 review found P0:0, P1:0, P2:2 accepted source-shape/fees-P&L caveats.
- Follow-ups: complete T121 dashboard, coverage, ready-gate, and Phase 27
  review updates.
- Notes for next agent: This pack is real open-data development rehearsal only.
  It is pair-level market-flow data, not a trader ledger, and it cannot close
  T116 or the paid-pilot ready gate.

### 2026-05-19 - T117/T118 - Real Open Data Source And Extraction Contract

- Scope: `docs/REAL_OPEN_DATA_SOURCE_SELECTION.md`,
  `docs/REAL_OPEN_DATA_EXTRACTION_CONTRACT.md`, `docs/tasks.md`.
- Why this work happened: The operator approved proceeding with real open-data
  rehearsal while private input remains unavailable.
- Decisions applied: Phase 27 real-open-data plan; T93 defer decision; Phase 25
  `needs_fixes` ready gate.
- Evidence collected: public JSON-RPC smoke checks succeeded for
  `https://rpcfree.com/ethereum-rpc` and `https://ethereum.publicnode.com`;
  `eth_getLogs` returned real Uniswap V2 WETH/USDC `Swap` logs for the selected
  pair. Validation pending after task batch.
- Follow-ups: implement T119 real-open-data case pack if bounded extraction
  produces unambiguous rows.
- Notes for next agent: Source is real public Ethereum mainnet Uniswap V2
  WETH/USDC pair-level swap logs, not account ledger data. It is labeled
  `real_open_data_rehearsal_not_private_evidence` and cannot close T116.

### 2026-05-19 - Real Open Data Rehearsal Development Plan

- Scope: `docs/REAL_OPEN_DATA_REHEARSAL_PLAN.md`, `docs/tasks.md`,
  `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`,
  README.
- Why this work happened: The operator does not currently have private pilot
  data and asked for a development plan using real open data only, with no
  synthetic rows.
- Decisions applied: `D-011`, `D-012`, T93 defer decision, Phase 25
  `needs_fixes` ready gate.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` ->
  passed. Boundary scan confirms Phase 27 labels the route as real open-data
  rehearsal only and keeps `docs/PAID_PILOT_READY_GATE.md` at `needs_fixes`
  unless T116 private evidence exists.
- Follow-ups: operator chooses source path before T117: Dune/on-chain preferred,
  BigQuery alternative, SEC official-reference fallback, Binance market-tape
  control only.
- Notes for next agent: The new plan is development rehearsal only. It must not
  close T116, must not make private/paid/PMF/customer-demand claims, and must
  use real public data only.

### 2026-05-15 - T115 - Private Pilot Readiness Deep Review

- Scope: `docs/archive/PHASE25_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`,
  `docs/audit/ARCH_REPORT.md`, `docs/audit/META_ANALYSIS.md`,
  `docs/audit/PHASE_REPORT_LATEST.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/tasks.md`, README and state docs.
- Why this work happened: Phase 25 required a boundary review before any
  paid-pilot readiness claim.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: Cycle 29 review found Stop-Ship: No, P0:0, P1:0, P2:4.
  Phase 25 artifacts are safe, but paid-pilot delivery readiness remains
  `needs_fixes` because no operator-approved private/anonymized report has been
  run and reviewed. `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  placeholder scan found none; `case-bank validate` passed for the four
  complete runnable packs.
- Follow-ups: T116 Operator-Approved Private Run And Reviewed Report Evidence,
  blocked until operator private input exists outside git.
- Notes for next agent: Do not claim private report readiness. The only next
  implementation route is safe metadata after an operator-approved private run;
  SaaS, checkout, hosted uploads, real exchange fetching, order blocking, and
  trading advice remain out of scope.

### 2026-05-15 - T114 - Paid Pilot Ready Gate

- Scope: `docs/PAID_PILOT_READY_GATE.md`, state docs.
- Why this work happened: Phase 25 needed an explicit ready / needs-fixes /
  reject decision before any warm paid-pilot delivery claim.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: acceptance criteria reviewed manually against
  `docs/PAID_PILOT_READY_GATE.md`, `docs/PAID_PILOT_PACKAGE.md`, and
  `docs/private_pilot_runs/pilot_waiting_for_input_001.md`.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` ->
  passed. Gate scan confirms status remains `needs_fixes` and private report
  delivery remains blocked.
- Follow-ups: run T115 Private Pilot Readiness Deep Review.
- Notes for next agent: Gate status is `needs_fixes`, not ready, because no
  operator-approved private/anonymized run was supplied, run, or manually
  reviewed. The exact first-user ask is drafted, but delivery readiness remains
  blocked until one private/anonymized report is reviewed outside git.

### 2026-05-15 - T113 - Paid Pilot Package And Feedback Log

- Scope: `docs/PAID_PILOT_PACKAGE.md`,
  `docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md`, state docs.
- Why this work happened: Phase 25 needed a manual paid-pilot offer and
  feedback capture loop before the go/no-go gate.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: acceptance criteria reviewed manually against
  `docs/PAID_PILOT_PACKAGE.md`,
  `docs/PRIVATE_PILOT_FEEDBACK_LOG_TEMPLATE.md`, and
  `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md`.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` ->
  passed. Boundary scan found only explicit exclusions and forbidden-data
  language.
- Follow-ups: implement T114 Paid Pilot Ready Gate.
- Notes for next agent: Package keeps the ask to one manual reviewed audit,
  $49-$149 pricing hypothesis, 48-72 hour turnaround after complete inputs,
  no checkout/payment processor, no SaaS, no live control, no order blocking,
  and no advice/performance promise. Feedback template records safe aggregate
  usefulness/trust/clarity/objection/payment/repeat/referral evidence only.

### 2026-05-15 - T112 - Local Private Pilot Artifact Run Notes

- Scope: `docs/private_pilot_runs/`, state docs.
- Why this work happened: Phase 25 needed a safe repo-visible way to record
  private pilot run metadata without committing private artifacts.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: safe blocker note created at
  `docs/private_pilot_runs/pilot_waiting_for_input_001.md`; acceptance
  criteria reviewed manually against `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md`
  and `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` ->
  passed. Privacy-marker scan found only checklist/template prohibitions and
  placeholders.
- Follow-ups: implement T113 Paid Pilot Package And Feedback Log.
- Notes for next agent: No operator-approved private/anonymized input exists in
  repo-visible context. T112 records blocker status only:
  `blocked_no_operator_approved_input` and `blocked_do_not_deliver`. Do not
  claim a private report was run or reviewed until an operator supplies an
  approved local artifact outside git.

### 2026-05-15 - T111 - Private Pilot Report Review Checklist

- Scope: `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`,
  `docs/REPORT_QUALITY_SCORECARD.md`, state docs.
- Why this work happened: Phase 25 needed a manual delivery gate before any
  private pilot report can be sent externally.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
  Acceptance criteria reviewed manually against
  `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`.
- Follow-ups: implement T112 Local Private Pilot Artifact Run Notes.
- Notes for next agent: Checklist blocks delivery for unresolved P0/P1 report
  truth, privacy, policy, advice, live-control, or performance-claim issues
  and defines safe external delivery statuses plus signoff fields.

### 2026-05-15 - T110 - Private Pilot Intake And Redaction Checklist

- Scope: `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md`,
  `docs/PILOT_INTAKE_CONTRACT_RU.md`, state docs.
- Why this work happened: Phase 25 needed a local-only private/anonymized input
  checklist before any private run-note or report-review work.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
  Acceptance criteria reviewed manually against
  `docs/PRIVATE_PILOT_INTAKE_CHECKLIST.md`.
- Follow-ups: implement T111 Private Pilot Report Review Checklist.
- Notes for next agent: Checklist forbids committing raw rows, account ids,
  credentials, Telegram handles, payment ids, private paths, and unapproved
  screenshots; maps intake to existing local CLI commands only.

### 2026-05-15 - T109 - Multi-Case Report Quality Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/archive/PHASE24_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, README and
  state docs.
- Why this work happened: Phase 24 required a boundary review before entering
  private-pilot readiness work.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  `case-bank validate` passed for all four complete runnable packs. Review
  found Stop-Ship: No, P0:0, P1:0, P2:3 accepted carry-forward caveats.
- Follow-ups: start T110 Private Pilot Intake And Redaction Checklist.
- Notes for next agent: Phase 24 gate is satisfied with 3 controlled internal
  demo-quality packs. This unblocks Phase 25 readiness checklists, not SaaS,
  checkout, live exchange control, or unreviewed private delivery.

### 2026-05-15 - T108 - Internal Demo Pack From Validated Cases

- Scope: `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md`,
  `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`, `demo/`, state docs.
- Why this work happened: Phase 24 needed a concise operator-only demo pack
  assembled from the strongest validated open-source/synthetic cases.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 258
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
  Acceptance criteria reviewed manually against
  `docs/INTERNAL_DEMO_PACK_OPEN_SOURCE_AUDITS.md`.
- Follow-ups: run T109 Multi-Case Report Quality Deep Review.
- Notes for next agent: Demo pack uses `risk_audit_case_001` as the positive
  case, `synthetic_limit_leverage_001` as the limitation case, and
  `synthetic_schema_reject_missing_price_001` as the edge-case rejection
  explanation. It keeps artifact quality separate from paid-pilot demand,
  customer PMF, or market evidence.

### 2026-05-15 - T107 - Regression Tests For Discovered Report Issues

- Scope: `trader_risk_audit/reporting/claim_guard.py`,
  `tests/unit/reporting/test_claim_guard.py`,
  `docs/PHASE24_REGRESSION_DECISIONS.md`, state docs.
- Why this work happened: Phase 24 needed discovered report-quality issues
  converted into regression coverage or documented docs-only reasons before
  demo-pack assembly.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/reporting/test_claim_guard.py -q --tb=short` -> 5 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 258 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T108 Internal Demo Pack From Open-Source Audits.
- Notes for next agent: Added `evidence_overclaim` claim-guard phrases for
  positive PMF/customer-demand/paid-pilot overclaims from open-source/demo
  artifacts. Docs-only decisions preserve the accepted Phase 23 P2 caveats.

### 2026-05-15 - T106 - Multi-Case Quality Dashboard

- Scope: `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`,
  `docs/REPORT_QUALITY_SCORECARD.md`, `docs/audit/PHASE23_ERROR_REGISTER.md`,
  state docs.
- Why this work happened: Phase 24 needed one operator-facing dashboard that
  separates demo-quality, internal-only, and blocked packs before regression
  and demo-pack tasks.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 256
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
  Acceptance criteria reviewed manually against
  `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`.
- Follow-ups: implement T107 Regression Tests For Discovered Report Issues.
- Notes for next agent: Dashboard classifies `public_sample_001`,
  `risk_audit_case_001`, and `synthetic_limit_leverage_001` as controlled
  internal demo-quality; SEC Form 4 remains internal reference only; missing
  price remains blocked/rejection-only. Next concrete data gap is a session
  timezone boundary fixture.

### 2026-05-15 - T105 - Open-Source Rule And Data Coverage Matrix

- Scope: `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`,
  `docs/OPEN_SOURCE_CASE_BANK.md`, `demo/`, state docs.
- Why this work happened: Phase 24 needed a pack-by-pack view of rule, field,
  limitation, output-section, and missing-coverage status before the quality
  dashboard.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 256
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
  Acceptance criteria reviewed manually against
  `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`.
- Follow-ups: implement T106 Multi-Case Quality Dashboard.
- Notes for next agent: Missing coverage is explicit, not hidden. Follow-up
  cases are drawdown-only, session-timezone boundary, realized-P&L wording, and
  no-breach control. Leverage support and fee-specific rules remain accepted
  limitations unless future data supports them.

### 2026-05-15 - T104 - Report Quality Scorecard

- Scope: `docs/REPORT_QUALITY_SCORECARD.md`,
  `demo/open_source_sec_form4_001/output/report_reviewed.md`,
  `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 24 needed a repeatable report-quality scoring
  aid before building coverage and dashboard views.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: pre-change `.venv/bin/python -m pytest tests -q
  --tb=short` -> 256 passed; `.venv/bin/python -m ruff check
  trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format
  --check trader_risk_audit tests` -> passed. Acceptance criteria reviewed
  manually against `docs/REPORT_QUALITY_SCORECARD.md`.
- Follow-ups: implement T105 Open-Source Rule And Data Coverage Matrix.
- Notes for next agent: SEC Form 4 reviewed report scored 17/18 with no fail
  condition. The scorecard is a review aid only, not a marketing or customer
  outcome claim.

### 2026-05-15 - T103 - Open-Source Case Bank Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE23_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `docs/ARCHITECTURE.md`, handoff docs.
- Why this work happened: Phase 23 required a boundary review before entering
  the multi-case report quality loop.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: Phase 23 review found Stop-Ship: No, P0:0, P1:0, P2:3;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 256 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: start T104 Report Quality Scorecard.
- Notes for next agent: P2 caveats are accepted limitations/wording/provenance
  items and should be carried into Phase 24 scorecard and coverage work, not
  hidden or treated as market validation.

### 2026-05-15 - T102 - Manual Validation Notes And Error Register

- Scope: `docs/audit/open_source_case_reviews/`,
  `docs/audit/PHASE23_ERROR_REGISTER.md`, `demo/*/output/report_reviewed.md`,
  `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 23 needed manual review notes and an error
  register before the boundary review.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 256
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run T103 Open-Source Case Bank Deep Review.
- Notes for next agent: Phase 23 register is P0:0, P1:0, P2:3. P2 findings
  are accepted limitation/provenance/wording caveats; no P0/P1 blocks Phase 24
  from the T102 review alone.

### 2026-05-15 - T101 - Batch Audit Run And Artifact Generation

- Scope: `demo/`, `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md`,
  `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 23 needed generated or explicitly rejected
  artifacts for every T100 candidate pack before manual validation.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `case-bank validate` passed for
  `open_source_sec_form4_001`, `public_sample_001`, `risk_audit_case_001`,
  and `synthetic_limit_leverage_001`; `.venv/bin/python -m pytest tests -q
  --tb=short` -> 256 passed; `.venv/bin/python -m ruff check
  trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format
  --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T102 Manual Validation Notes And Error Register.
- Notes for next agent: `docs/OPEN_SOURCE_AUDIT_BATCH_INDEX.md` summarizes
  status, finding count, limitation count, and reproducibility without raw
  rows. The missing-price pack has only `output/run_status.json` and no partial
  report artifacts.

### 2026-05-15 - T100 - First Open-Source Candidate Case Packs

- Scope: `docs/OPEN_SOURCE_CASE_BANK.md`, `demo/risk_audit_case_001/source.md`,
  `demo/synthetic_limit_leverage_001/`,
  `demo/synthetic_schema_reject_missing_price_001/`,
  `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 23 needed at least 5 listed candidate packs
  across multiple data shapes before batch audit generation.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: pre-change `.venv/bin/python -m pytest tests -q
  --tb=short` -> 256 passed; `.venv/bin/python -m ruff check
  trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format
  --check trader_risk_audit tests` -> passed. Acceptance criteria reviewed
  manually against `docs/OPEN_SOURCE_CASE_BANK.md`.
- Follow-ups: implement T101 Batch Audit Run And Artifact Generation.
- Notes for next agent: the T100 inventory lists five candidates and three
  data shapes. `synthetic_limit_leverage_001` is intended to preserve an
  unsupported leverage limitation. `synthetic_schema_reject_missing_price_001`
  is intended to reject before report generation.

### 2026-05-15 - T99 - Case Pack Directory Contract

- Scope: `trader_risk_audit/validation/open_source_case.py`,
  `trader_risk_audit/validation/__init__.py`, `trader_risk_audit/cli.py`,
  `tests/unit/test_open_source_case_contract.py`,
  `tests/integration/test_open_source_case_contract_cli.py`,
  `demo/open_source_sec_form4_001/output/reproducibility_status.json`,
  docs state.
- Why this work happened: Phase 23 needed a reusable contract validator before
  adding more open-source or synthetic case packs.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: `.venv/bin/python -m pytest tests/unit/test_open_source_case_contract.py tests/integration/test_open_source_case_contract_cli.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 256 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T100 First Open-Source Candidate Case Packs.
- Notes for next agent: `case-bank validate --case-dir <path>` checks required
  case files, manifest artifact entries, reproducibility status, and
  secret/private markers. The SEC Form 4 pack is now the passing reference
  pack.

### 2026-05-15 - T98 - Open-Source Source Selection Protocol

- Scope: `docs/OPEN_SOURCE_CASE_BANK.md`,
  `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`,
  `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 23 needed source-selection and
  anti-cherry-pick rules before creating more candidate audit packs.
- Decisions applied: `D-011`, `D-012`, T93 defer decision.
- Evidence collected: pre-change `.venv/bin/python -m pytest tests -q
  --tb=short` -> 253 passed; `.venv/bin/python -m ruff check
  trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format
  --check trader_risk_audit tests` -> passed. Acceptance criteria reviewed
  manually against `docs/OPEN_SOURCE_CASE_BANK.md`.
- Follow-ups: implement T99 Case Pack Directory Contract.
- Notes for next agent: `docs/OPEN_SOURCE_CASE_BANK.md` is the source
  selection protocol. It requires positive, limitation/reject, and edge/schema
  coverage where available and labels public/open-source packs as
  artifact-quality evidence only, not paid-pilot or PMF evidence.

### 2026-05-15 - T98-T115 Planning - Open-Source Audit Validation Route

- Scope: `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`,
  `MEMORY.md`, `docs/AUTOMATED_PILOT_ROADMAP.md`,
  `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator paused Core and asked to focus Product 1 on
  more real/open-source data and validation artifacts before going to warm
  prospects.
- Decisions applied: `D-011`, `D-010`, T93 defer decision.
- Evidence collected: documentation-only roadmap/task update. No product code
  changed in this planning step.
- Follow-ups: start T98 Open-Source Source Selection Protocol.
- Notes for next agent: validation success means truthful, reproducible
  reports with preserved limitations, not cherry-picked positive violations.
  T94-T97 real fetching remains blocked.

### 2026-05-15 - T93 - CSV Friction Decision Gate

- Scope: `docs/CSV_FRICTION_DECISION_REPORT.md`,
  `docs/EXCHANGE_API_IMPORT_PLAN_RU.md`,
  `docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, handoff docs.
- Why this work happened: Phase 22 requires an evidence decision before any
  ADR update or real local read-only exchange network fetching work.
- Decisions applied: `D-010`, `D-001`, ADR-002.
- Evidence collected: repo-visible market evidence counts are 0 for qualified
  prospects, valid exports/rules, CSV/export blockers, API objections, paid
  reports, repeat/referral signals, and paid intent. No market customer log was
  supplied in repo context.
- Follow-ups: none in the current roadmap. T94-T97 remain blocked unless a
  future privacy-safe evidence export reopens the gate.
- Notes for next agent: T93 verdict is defer, not proceed. Do not implement
  real exchange network fetching or ADR expansion from the current evidence.

### 2026-05-15 - T92 - Hypothesis Evidence Dashboard Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE21_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `docs/EVIDENCE_INDEX.md`,
  `docs/tasks.md`.
- Why this work happened: Phase 21 required a boundary review for evidence
  integrity, privacy-safe exports, demo/vanity separation, gate correctness,
  and false-PMF risk before Phase 22.
- Decisions applied: `D-010`, `D-001`, ADR-002.
- Evidence collected: Cycle 26 deep review found P0:0, P1:0, P2:0,
  Stop-Ship: No. `.venv/bin/python -m pytest tests -q --tb=short` -> 253
  passed; ruff check/format passed.
- Follow-ups: start T93 CSV Friction Decision Gate.
- Notes for next agent: Phase 22 must decide before building. T94-T97 stay
  blocked if T93 returns defer or reject.

### 2026-05-15 - T91 - Privacy-Safe Evidence Export

- Scope: `trader_risk_audit/evidence.py`, `trader_risk_audit/cli.py`,
  `tests/unit/evidence/test_evidence_export_privacy.py`,
  `tests/integration/test_evidence_export_cli.py`, docs state.
- Why this work happened: Phase 21 needs a shareable evidence snapshot for
  review/advisor discussions without exposing raw user data or identifiers.
- Decisions applied: `D-010`, `D-001`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/evidence/test_evidence_export_privacy.py
  tests/integration/test_evidence_export_cli.py -q --tb=short` -> 3 passed;
  ruff check passed.
- Follow-ups: run T92 Hypothesis Evidence Dashboard Deep Review.
- Notes for next agent: `evidence export` writes aggregate CSV/Markdown only.
  Provenance is source filename plus sha256; private source paths are not
  printed or exported.

### 2026-05-15 - T90 - Hypothesis Gate Rules

- Scope: `trader_risk_audit/evidence.py`,
  `docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md`,
  `tests/unit/evidence/test_hypothesis_gates.py`,
  `tests/test_hypothesis_evidence_docs.py`, docs state.
- Why this work happened: Phase 21 needs explicit proceed /
  needs-more-evidence / pivot rules before using evidence to decide whether to
  invest in real read-only import work.
- Decisions applied: `D-010`, `D-001`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/evidence/test_hypothesis_gates.py
  tests/test_hypothesis_evidence_docs.py -q --tb=short` -> 4 passed; ruff
  check passed.
- Follow-ups: implement T91 Privacy-Safe Evidence Export.
- Notes for next agent: uploads, API connections, policy builds, audit runs,
  and preview generation are supporting funnel evidence only. Paid reports,
  repeat commitments, and referrals drive gate decisions.

### 2026-05-15 - T89 - Evidence Dashboard CLI

- Scope: `trader_risk_audit/evidence.py`, `trader_risk_audit/cli.py`,
  `tests/integration/test_hypothesis_dashboard_cli.py`, docs state.
- Why this work happened: Phase 21 needs a local dashboard before any web UI
  so the operator can see funnel counts, ratios, gate status, objections,
  unsupported blockers, and next action.
- Decisions applied: `D-010`, `D-001`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/integration/test_hypothesis_dashboard_cli.py -q --tb=short` -> 3
  passed; ruff check passed.
- Follow-ups: implement T90 Hypothesis Gate Rules.
- Notes for next agent: `evidence hypothesis-dashboard` reads optional
  `--customer-log` and `--funnel-log`, excludes demo/open-source from paid
  gate counts, and keeps output aggregate-only.

### 2026-05-15 - T88 - Hypothesis Funnel Event Schema

- Scope: `trader_risk_audit/evidence.py`,
  `docs/PILOT_EVIDENCE_LOG_RU.md`,
  `docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md`,
  `tests/unit/evidence/test_hypothesis_funnel.py`,
  `tests/test_hypothesis_evidence_docs.py`, docs state.
- Why this work happened: Phase 21 needs one safe event schema for measuring
  funnel progression without turning pilot evidence into a CRM or leaking
  private data.
- Decisions applied: `D-010`, `D-001`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/evidence/test_hypothesis_funnel.py
  tests/test_hypothesis_evidence_docs.py -q --tb=short` -> 4 passed; ruff
  check passed.
- Follow-ups: implement T89 Evidence Dashboard CLI.
- Notes for next agent: new funnel events coexist with legacy
  `EvidenceRow` customer logs through `load_hypothesis_evidence`. Demo/open
  source events remain vanity/demo evidence and must not count as paid/customer
  validation.

### 2026-05-15 - T87 - Preview And Paid CTA Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE20_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `docs/EVIDENCE_INDEX.md`,
  `docs/tasks.md`.
- Why this work happened: Phase 20 required a boundary review for preview
  redaction, claim safety, paid CTA copy, conversion events, paid unlock
  boundary, and checkout/SaaS scope.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001, ADR-002.
- Evidence collected: Cycle 25 deep review found P0:0, P1:0, P2:0,
  Stop-Ship: No. `.venv/bin/python -m pytest tests -q --tb=short` -> 240
  passed; ruff check/format passed.
- Follow-ups: start T88 Hypothesis Funnel Event Schema.
- Notes for next agent: Phase 20 preview and paid CTA work is local-only,
  claim-guarded, no-checkout, and no-SaaS. Phase 21 should measure actual
  hypothesis evidence and keep demo/open-source usage separate from paid/PMF
  evidence.

### 2026-05-15 - T86 - Paid Unlock Boundary

- Scope: `trader_risk_audit/preview/unlock.py`,
  `trader_risk_audit/preview/__init__.py`, `trader_risk_audit/cli.py`,
  `tests/unit/preview/test_paid_unlock_boundary.py`,
  `tests/integration/test_paid_unlock_cli.py`, docs state.
- Why this work happened: Phase 20 needs local status transitions from preview
  to paid-requested, operator-reviewed, and delivered without implementing
  checkout/payment processing or leaking payment identifiers.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/preview/test_paid_unlock_boundary.py
  tests/integration/test_paid_unlock_cli.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 240 passed; ruff
  check/format passed.
- Follow-ups: run T87 Phase 20 deep review.
- Notes for next agent: `preview unlock` is a local JSON state transition tool.
  It stores safe manual payment/intent evidence only. Delivery is blocked until
  operator review and claim safety are both true.

### 2026-05-15 - T85 - Preview Conversion Events

- Scope: `trader_risk_audit/evidence.py`, `trader_risk_audit/cli.py`,
  `tests/unit/evidence/test_preview_events.py`,
  `tests/integration/test_preview_events_cli.py`, docs state.
- Why this work happened: Phase 20 needs privacy-safe measurement of preview
  generation, CTA exposure/acceptance, and objections without treating demos as
  paid evidence.
- Decisions applied: `D-010`, `D-001`, `D-006`.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/evidence/test_preview_events.py
  tests/integration/test_preview_events_cli.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 237 passed; ruff
  check/format passed.
- Follow-ups: implement T86 Paid Unlock Boundary.
- Notes for next agent: `evidence preview-event-append` and
  `preview-event-summary` are local CSV tools. Event schema stores safe event
  metadata only and excludes `public_sample_demo`, `internal_demo`, and
  `demo_artifact` from market CTA accepted/requested counts.

### 2026-05-15 - T84 - Paid Pilot CTA Copy And Package

- Scope: `trader_risk_audit/preview/cta.py`,
  `trader_risk_audit/preview/model.py`, `tests/test_paid_preview_cta.py`,
  `tests/unit/preview/test_preview_cta.py`, docs state.
- Why this work happened: Phase 20 needs preview packaging that can ask for a
  narrow manual paid pilot without implying checkout, SaaS, advice, live
  control, or guaranteed improvement.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/test_paid_preview_cta.py tests/unit/preview/test_preview_cta.py
  tests/unit/preview/test_preview_model.py tests/integration/test_preview_cli.py
  -q --tb=short` -> 6 passed; `.venv/bin/python -m pytest tests -q
  --tb=short` -> 234 passed; ruff check/format passed.
- Follow-ups: implement T85 Preview Conversion Events.
- Notes for next agent: CTA rendering is status-gated on complete previews and
  remains manual paid-pilot packaging only. No checkout, payment processing,
  account model, or hosted flow was added.

### 2026-05-15 - T83 - Claim-Safe Report Preview Model

- Scope: `trader_risk_audit/preview/`, `trader_risk_audit/cli.py`,
  `tests/unit/preview/test_preview_model.py`,
  `tests/integration/test_preview_cli.py`, docs state.
- Why this work happened: Phase 20 needs a limited preview from completed
  bundles that shows value without exposing full source-row tables, raw rows,
  or unsafe customer-facing claims.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/preview/test_preview_model.py tests/integration/test_preview_cli.py
  -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q
  --tb=short` -> 231 passed; `.venv/bin/python -m ruff check
  trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format
  --check trader_risk_audit tests` -> passed; light review passed with P0:0,
  P1:0.
- Follow-ups: implement T84 Paid Pilot CTA Copy And Package.
- Notes for next agent: `preview build` reads bundle refs and aggregate
  artifacts only. It counts normalized trades/violations, aggregates rule
  types, references limitation registers by safe names, runs claim guard, and
  writes `preview.md`. It does not emit symbols, source-row ids, raw rows, or
  private output directories in CLI stdout.

### 2026-05-15 - T82 - One-Click Audit Runner Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE19_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `docs/EVIDENCE_INDEX.md`,
  `docs/tasks.md`, `MEMORY.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 19 required a boundary review focused on
  deterministic audit session execution, safe status/bundle outputs,
  reproducibility, artifact drift, and runtime-tier scope before Phase 20.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001, ADR-002.
- Evidence collected: Cycle 24 deep review found P0:0, P1:0, P2:0,
  Stop-Ship: No. `.venv/bin/python -m pytest tests -q --tb=short` -> 228
  passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: start T83 Claim-Safe Report Preview Model in Phase 20.
- Notes for next agent: Phase 19 runner/bundle/reproducibility artifacts are
  local-only and deterministic. Preview work must consume safe bundle/status
  metadata and report artifacts without exposing raw rows, full source-row
  tables, or unsupported claims.

### 2026-05-15 - T81 - Automated Run Reproducibility Gate

- Scope: `trader_risk_audit/audit_session/reproducibility.py`,
  `trader_risk_audit/audit_session/__init__.py`,
  `tests/unit/audit_session/test_reproducibility_gate.py`,
  `tests/integration/test_audit_session_reproducibility.py`, docs state.
- Why this work happened: Phase 19 needs to prove automated audit session runs
  reproduce deterministic artifact hashes before preview or delivery can
  proceed.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/audit_session/test_reproducibility_gate.py
  tests/integration/test_audit_session_reproducibility.py -q --tb=short` -> 3
  passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 228 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  light review passed with P0:0, P1:0.
- Follow-ups: run T82 Phase 19 deep review.
- Notes for next agent: `run_reproducibility_gate` reruns a completed session
  into a separate output directory, recomputes stable manifest content hashes
  from artifact names/SHA/package version, ignores generated timestamps and
  local paths, writes `reproducibility_status.json`, and sets
  `blocked_reproducibility` on drift.

### 2026-05-15 - T80 - Artifact Bundle Index

- Scope: `trader_risk_audit/audit_session/artifact_bundle.py`,
  `trader_risk_audit/audit_session/__init__.py`, `trader_risk_audit/cli.py`,
  `tests/unit/audit_session/test_artifact_bundle.py`,
  `tests/integration/test_artifact_bundle_cli.py`, docs state.
- Why this work happened: Phase 19 needs a local dashboard substitute that
  points to automated run inputs, outputs, preview state, and limitation
  registers without exposing private trade rows.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/audit_session/test_artifact_bundle.py
  tests/integration/test_artifact_bundle_cli.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 225 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  light review passed with P0:0, P1:0.
- Follow-ups: start T81 Automated Run Reproducibility Gate.
- Notes for next agent: `audit-session bundle` writes and validates
  `bundle_index.json` from a run directory. Complete bundles require
  `run_status`, `manifest`, normalized trades, violations, attribution, report,
  and delivery packet refs. The index stores refs/hashes/status/preview state
  and limitation register refs only, not artifact contents.

### 2026-05-15 - T79 - Audit Session Runner

- Scope: `trader_risk_audit/audit_session/`, `trader_risk_audit/cli.py`,
  `tests/integration/test_audit_session_runner.py`, docs state.
- Why this work happened: Phase 19 needs a local one-click runner that can turn
  a ready intake session plus generated/approved policy into the complete audit
  artifact pack without developer intervention.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-002.
- Evidence collected: `.venv/bin/python -m pytest
  tests/integration/test_audit_session_runner.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 222 passed;
  `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed;
  light review passed with P0:0, P1:0.
- Follow-ups: start T80 Artifact Bundle Index.
- Notes for next agent: `audit-session run` resolves the safe source export ref
  from `intake_session.json`, gates on `ready_for_audit` intake status and a
  runnable policy status, runs the existing deterministic audit internals, and
  writes `run_status.json` with safe refs/status only. Blocked runs return code
  2 before report/manifest generation.

### 2026-05-15 - T78 - Structured Rule Builder Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE18_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `README.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `MEMORY.md`,
  `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 18 required a boundary review focused on
  deterministic policy generation, unsupported text safety, claim boundaries,
  policy validity, and runtime scope before Phase 19.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001, ADR-002.
- Evidence collected: Cycle 23 deep review found P0:0, P1:0, P2:1 architecture
  doc drift; the P2 was closed during the phase doc update.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 219 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: start T79 Audit Session Runner in Phase 19.
- Notes for next agent: Phase 18 policy/rule-builder artifacts are local-only,
  deterministic, and structured. Unsupported/free-text requests stay in a
  manual-review register and must not become executable rule truth.

### 2026-05-15 - T77 - Unsupported Rule Register

- Scope: `trader_risk_audit/policy/unsupported_register.py`,
  `trader_risk_audit/policy/__init__.py`, `trader_risk_audit/cli.py`,
  `tests/unit/policy/test_unsupported_rule_register.py`,
  `tests/integration/test_unsupported_rule_register_cli.py`, docs state.
- Why this work happened: Phase 18 needed unsupported/free-text rule requests
  preserved as limitations/manual-review items without letting them become
  executable deterministic policy rules.
- Decisions applied: `D-010`, `D-001`, `D-006`.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/policy/test_unsupported_rule_register.py
  tests/integration/test_unsupported_rule_register_cli.py -q --tb=short` -> 3
  passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 219 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run T78 Phase 18 deep review before Phase 19 begins.
- Notes for next agent: `policy unsupported append` refuses credential,
  handle, and private-note shaped text. Accepted unsupported requests are
  written to a local Markdown register with deterministic request ids,
  sanitized summaries, reason codes, and `manual_review_required` status.

### 2026-05-15 - T76 - Rule Builder Prompt Flow

- Scope: `trader_risk_audit/policy/rule_builder_flow.py`,
  `trader_risk_audit/policy/__init__.py`, `trader_risk_audit/cli.py`,
  `tests/unit/policy/test_rule_builder_flow.py`,
  `tests/integration/test_rule_builder_flow_cli.py`, docs state.
- Why this work happened: Phase 18 needs local structured policy-building
  flows before unsupported free-text rule requests can be safely captured.
- Decisions applied: `D-010`, `D-001`, `D-006`.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/policy/test_rule_builder_flow.py
  tests/integration/test_rule_builder_flow_cli.py
  tests/integration/test_policy_builder_cli.py -q --tb=short` -> 5 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 216 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T77 Unsupported Rule Register so free-text or
  unsupported requests are preserved as limitations/manual-review items, never
  executable rule truth.
- Notes for next agent: `policy flow` supports non-interactive structured
  inputs and an stdin-driven interactive path. It writes deterministic
  `policy.yaml` and can print unavailable catalog-rule explanations from a
  sanitized schema profile.

### 2026-05-15 - T75 - Profile-To-Policy Builder

- Scope: `trader_risk_audit/policy/builder.py`,
  `trader_risk_audit/policy/__init__.py`, `trader_risk_audit/cli.py`,
  `tests/unit/policy/test_policy_builder.py`,
  `tests/integration/test_policy_builder_cli.py`, docs state.
- Why this work happened: Phase 18 needs generated deterministic policies from
  starter profiles and structured threshold choices before adding prompt flow.
- Decisions applied: `D-010`, `D-001`, `D-006`.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/policy/test_policy_builder.py
  tests/integration/test_policy_builder_cli.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 212 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T76 Rule Builder Prompt Flow on top of
  `policy build`, the builder API, and the rule catalog availability output.
- Notes for next agent: `policy build` writes deterministic `policy.yaml` from
  an intake session JSON, starter/custom profile, explicit account ids, and
  catalog-validated threshold overrides. Custom free text remains outside
  executable policy.

### 2026-05-15 - T74 - Supported Rule Catalog

- Scope: `trader_risk_audit/policy/rule_catalog.py`,
  `trader_risk_audit/policy/__init__.py`,
  `tests/unit/policy/test_rule_catalog.py`, docs state.
- Why this work happened: Phase 18 needs a deterministic catalog before
  automated policy building can replace manual YAML authoring.
- Decisions applied: `D-010`, `D-001`, `D-006`.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/policy/test_rule_catalog.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 209 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T75 Profile-To-Policy Builder using the catalog and
  starter policy profile docs.
- Notes for next agent: The catalog exposes every supported schema rule type,
  threshold unit, safe description, starter-profile applicability, and
  availability requirements from sanitized intake profile fields. Arbitrary
  free text still must not become executable rule truth.

### 2026-05-14 - T73 - Automated Intake Profiler Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE17_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `README.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `MEMORY.md`,
  `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 17 required a boundary review focused on
  privacy, raw-row leakage, deterministic profiling, CLI output, docs, and
  operator handoff before Phase 18.
- Decisions applied: `D-010`, `D-001`, `D-006`, ADR-001, ADR-002.
- Evidence collected: Cycle 22 deep review found P0:0, P1:0, P2:1
  architecture doc drift; the P2 was closed during the phase doc update.
  `.venv/bin/python -m pytest tests -q --tb=short` -> 206 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: start T74 Supported Rule Catalog in Phase 18.
- Notes for next agent: Phase 17 intake artifacts are local-only and safe
  metadata surfaces. Phase 18 should build deterministic policy/rule selection
  on top of the intake profile without allowing arbitrary free text to become
  executable rule truth.

### 2026-05-14 - T72 - Actionable Intake Report

- Scope: `trader_risk_audit/intake/report.py`,
  `trader_risk_audit/cli.py`, `tests/unit/intake/test_intake_report.py`,
  `tests/integration/test_intake_report_cli.py`,
  `docs/AUTOMATED_PILOT_ROADMAP.md`.
- Why this work happened: Phase 17 needs a prospect-readable summary that turns
  intake/session profile metadata into concrete blockers, accepted fields,
  unsupported checks, and next action before paid audit work.
- Decisions applied: `D-010`, T70/T71 local intake artifacts, no-advice and
  privacy boundaries from the pilot intake contract.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/intake/test_intake_report.py
  tests/integration/test_intake_report_cli.py -q --tb=short` -> 4 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 206 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: T73 Phase 17 deep review should verify privacy, determinism,
  status semantics, and scope boundaries across T70-T72.
- Notes for next agent: The report renderer emits only status, reasons,
  accepted field mappings, unsupported column names, unsupported check labels,
  and next action. It does not emit CSV cell values.

### 2026-05-14 - T71 - CSV Schema Profiler

- Scope: `trader_risk_audit/intake/profiler.py`,
  `trader_risk_audit/trades/importers.py`, `trader_risk_audit/cli.py`,
  `tests/unit/intake/test_csv_profiler.py`,
  `tests/integration/test_intake_profile_cli.py`,
  `docs/AUTOMATED_PILOT_ROADMAP.md`.
- Why this work happened: Phase 17 needs safe CSV/export profiling before
  normalization so prospects and operators can see mappings, blockers, and
  coverage without exposing raw rows.
- Decisions applied: `D-010`, T70 intake session contract, and the local-first
  `T0` runtime boundary.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/intake/test_csv_profiler.py
  tests/integration/test_intake_profile_cli.py -q --tb=short` -> 3 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 202 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: T72 Actionable Intake Report should consume `schema_profile.json`
  and translate missing fields, unsupported columns, and coverage into safe next
  actions.
- Notes for next agent: The profiler outputs only file names, column names,
  counts, booleans, and timezone/coverage labels. It does not emit cell values
  or raw rows.

### 2026-05-14 - T70 - Automated Intake Session Contract

- Scope: `trader_risk_audit/intake/`, `trader_risk_audit/cli.py`,
  `tests/unit/intake/test_intake_session.py`,
  `tests/integration/test_intake_session_cli.py`,
  `docs/AUTOMATED_PILOT_ROADMAP.md`.
- Why this work happened: Phase 17 needs a deterministic local intake session
  metadata boundary before CSV schema profiling or any row parsing.
- Decisions applied: `D-010`, plus existing local-first/runtime `T0`
  boundaries in `docs/ARCHITECTURE.md`.
- Evidence collected: `.venv/bin/python -m pytest
  tests/unit/intake/test_intake_session.py
  tests/integration/test_intake_session_cli.py -q --tb=short` -> 5 passed;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 199 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: T71 CSV Schema Profiler should consume `intake_session.json` and
  keep raw private rows out of logs, docs, and committed fixtures.
- Notes for next agent: `trader_risk_audit.intake` is now a package preserving
  the prior intake-file validation imports while adding
  `trader_risk_audit.intake.session`.

### 2026-05-14 - Phase 17-22 - Automated Pilot Roadmap

- Scope: `docs/AUTOMATED_PILOT_ROADMAP.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `docs/DECISION_LOG.md`, `docs/EVIDENCE_INDEX.md`,
  `docs/ARTIFACT_VALIDATION_ROADMAP.md`.
- Why this work happened: Phase 16 proved artifact quality on a verified
  open-source report pack, but hypothesis validation still required repeated
  prospect runs with too much manual setup work.
- Decisions applied: `D-010`, plus existing `D-006`, `D-007`, `D-009`, ADR-002.
- Evidence collected: planning-only documentation pass;
  `.venv/bin/python -m pytest tests -q --tb=short` -> 194 passed;
  `.venv/bin/ruff check trader_risk_audit tests` -> passed;
  `.venv/bin/ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: start T70 Automated Intake Session Contract.
- Notes for next agent: Keep Phases 17-21 local-first and deterministic. Do not
  implement hosted uploads, checkout, SaaS accounts, or real exchange fetching
  before the explicit T93/T94 CSV friction decision gate.

### 2026-05-12 - T69 - External Pilot Ready Gate

- Scope: `docs/audit/PHASE16_ARTIFACT_VALIDATION_REVIEW.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`,
  `README.md`, `MEMORY.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 16 needed a go/no-go decision after internal
  demo packaging and claim-safety review.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: ready-gate review states controlled warm conversations
  are allowed with explicit open-source limits; paid/customer delivery still
  requires approved real trader input and written rules. No P0/P1 findings.
- Follow-ups: run mandatory Phase 16 phase-boundary deep review and archive it.
- Notes for next agent: Do not treat SEC open-source validation as PMF, paid
  pilot, customer proof, or issuer/trading advice. The paid pilot package is one
  manual audit report for `$49-$149`, 48-72 hours after complete approved input.

### 2026-05-12 - T68 - Internal Demo Pack

- Scope: `docs/INTERNAL_DEMO_PACK_SEC_FORM4_EN.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`.
- Why this work happened: Phase 16 needed operator-facing demo packaging around
  the reviewed SEC artifact without requiring the operator to open code or raw
  data.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: demo pack points to reviewed report, reviewed packet,
  manifest, run notes, intake summary, manual validation, and claim-safety
  review. Privacy review confirms no private customer data or reporting-owner
  fields are included.
- Follow-ups: run T69 external pilot ready gate.
- Notes for next agent: Use the demo pack for controlled warm conversations
  only. The ask is one paid audit pilot on approved private export/read-only
  import plus written rules; do not imply SaaS, advice, live control, or market
  validation proof.

### 2026-05-12 - T67 - Report Polish And Claim Safety Review

- Scope: `demo/open_source_sec_form4_001/output/report_reviewed.md`,
  `demo/open_source_sec_form4_001/output/telegram_packet_reviewed.txt`,
  `docs/REPORT_POLISH_SEC_FORM4_EN.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`.
- Why this work happened: T66 found P2 limitation wording risk in the generic
  first screen; T67 needed a readable, claim-safe reviewed report and packet
  before any internal demo packaging.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: existing `validate_report_claims` returned
  `report_reviewed.md=True` and `telegram_packet_reviewed.txt=True`; reviewed
  hashes are recorded in `docs/REPORT_POLISH_SEC_FORM4_EN.md`.
- Follow-ups: package T68 internal demo pack using the reviewed report and
  packet.
- Notes for next agent: T66-P2-001 is closed for internal/demo use. Do not
  present this as customer, paid-pilot, PMF, or issuer recommendation evidence.

### 2026-05-12 - T66 - Manual Calculation Validation

- Scope: `docs/MANUAL_VALIDATION_SEC_FORM4_EN.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`.
- Why this work happened: Phase 16 needed manual correctness validation before
  any report polish or external delivery.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: manually validated all seven generated violation rows
  plus one non-flagged control row against
  `demo/open_source_sec_form4_001/trades.csv`,
  `demo/open_source_sec_form4_001/output/violations.json`, and
  `demo/open_source_sec_form4_001/output/report.md`.
- Follow-ups: T67 must address or explicitly accept T66-P2-001: first-screen
  report wording needs clearer open-source validation and unsupported P&L /
  drawdown limitations.
- Notes for next agent: No P0/P1 correctness issues found. External delivery
  remains blocked until T67 claim-safety/report-polish review closes or accepts
  the P2 item.

### 2026-05-12 - T65 - First Real Audit Artifact Run

- Scope: `demo/open_source_sec_form4_001/output/`,
  `docs/FIRST_AUDIT_RUN_SEC_FORM4_EN.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`.
- Why this work happened: Phase 16 needed a complete deterministic report pack
  from the validated SEC Form 4 open-source fixture before manual validation.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: `.venv/bin/python -m trader_risk_audit audit --trades
  demo/open_source_sec_form4_001/trades.csv --policy
  demo/open_source_sec_form4_001/policy.yaml --output-dir
  demo/open_source_sec_form4_001/output` wrote normalized trades, violations,
  attribution summary, Markdown report, delivery packet, and manifest. Rerun in
  `/tmp/trader-risk-audit-sec/open_source_sec_form4_rerun` produced the same
  manifest content hash `9cfdd76e5904f3e512f6c04a9321706b7071e712b3868841c8817e93469907e8`.
- Follow-ups: run T66 manual calculation validation before any external
  delivery or report polish.
- Notes for next agent: The artifact pack is mechanically complete but not
  externally ready. T66/T67 must keep SEC-source limitations visible:
  transaction-notional proxy only, watchlist validation only, no customer P&L,
  no drawdown proof, no advice, and no paid-pilot evidence.

### 2026-05-12 - T64 - Real Data Intake And Policy Mapping

- Scope: `demo/open_source_sec_form4_001/`,
  `docs/REAL_DATA_INTAKE_SEC_FORM4_EN.md`,
  `docs/POLICY_MAPPING_REVIEW_SEC_FORM4_EN.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`.
- Why this work happened: Phase 16 needed a safe, traceable open-source intake
  and policy mapping before generating a report artifact.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: SEC 2026 Q1 Form 4 zip was downloaded to
  `/tmp/trader-risk-audit-sec/2026q1_form345.zip` and not committed. The
  sanitized fixture uses six non-derivative transaction rows with mapped SEC
  dates, tickers, side, quantity, price, and accession/key trace ids. Manual
  validation loaded six normalized trade records and three policy rules.
- Follow-ups: run T65 audit artifact generation against
  `demo/open_source_sec_form4_001/trades.csv` and
  `demo/open_source_sec_form4_001/policy.yaml`.
- Notes for next agent: Treat `max_position_size` as a transaction-notional
  proxy only, `SVRE` as validation watchlist only, and `max_leverage` as an
  expected unsupported-data limitation. Do not claim customer P&L, causal loss,
  advice, or paid-pilot validation from this source.

### 2026-05-12 - T63 - Real Audit Scope Lock

- Scope: `docs/REAL_AUDIT_SCOPE_OPEN_SOURCE_EN.md`, `docs/tasks.md`,
  `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`, `README.md`,
  `MEMORY.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Orchestrator Step 0 routed to Phase 16 T63. The
  operator clarified that absence of private data should not block artifact
  validation; valid open sources should be used instead.
- Decisions applied: `D-001`, `D-006`, `D-009`, ADR-002.
- Evidence collected: Step 0 placeholder check found no unresolved `{{...}}`
  placeholders in required docs. T63 scope is locked to SEC EDGAR Form 4
  open-source transaction records, English report language, Europe/Moscow
  timezone, and anonymized account `acct_open_sec_form4_msk_001`. No product
  tests were rerun because this was a docs/routing task.
- Follow-ups: implement T64 by deriving a compact sanitized CSV fixture from
  the selected SEC dataset, recording exact source metadata, unsupported
  fields, and policy mapping before any report run.
- Notes for next agent: Public/open-source artifact validation is allowed for
  Phase 16 when private data is unavailable. It proves artifact quality only;
  it is not paid pilot evidence, PMF evidence, customer validation, or proof
  that traders will pay.

### 2026-05-09 - T62 - Exchange Import Deep Review

- Scope: `docs/audit/STRATEGY_NOTE.md`, `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`, `docs/audit/REVIEW_REPORT.md`, `docs/audit/PHASE_REPORT_LATEST.md`, `docs/audit/AUDIT_INDEX.md`, `docs/archive/PHASE15_REVIEW.md`, `README.md`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`.
- Why this work happened: Phase 15 needed a boundary review focused on secrets, permissions, reproducibility, deterministic truth, evidence capture, and product scope before exchange import could be discussed in founder-led pilots.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 194 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; Cycle 20 deep review found P0:0, P1:0, P2:0, Stop-Ship: No.
- Follow-ups: no planned implementation task remains; next work should come from pilot evidence, review findings, or an explicit roadmap update.
- Notes for next agent: Phase 15 is complete and archived in `docs/archive/PHASE15_REVIEW.md`. Operator materials are ready for founder-led pilot conversations and local fixture/planning demonstrations, but real exchange network fetching remains unimplemented and must not be represented as available.

### 2026-05-09 - T61 - Exchange Import Evidence Fields

- Scope: `trader_risk_audit/evidence.py`, `trader_risk_audit/cli.py`, `docs/PILOT_EVIDENCE_LOG_RU.md`, `templates/pilot_customer_log.csv`, `tests/unit/test_evidence_capture.py`, `tests/test_pilot_evidence_log.py`.
- Why this work happened: Phase 15 needed pilot evidence capture to distinguish CSV pilots from read-only exchange-import pilots and track non-sensitive API setup objections.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/test_evidence_capture.py tests/test_pilot_evidence_log.py -q --tb=short` -> 9 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 194 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; light review passed with P0:0, P1:0.
- Follow-ups: run T62 Exchange Import Deep Review before treating exchange import as pilot-ready.
- Notes for next agent: Evidence rows now include `intake_method` values `csv_export`, `bybit_read_only_api`, and `binance_read_only_api`, plus `api_setup_objections`; old logs without these columns load as CSV rows. The validation summary counts CSV versus exchange-import pilots separately, but paid reports and repeat-use commitments remain the gate.

### 2026-05-09 - T60 - Exchange Import CLI Safety Guidance

- Scope: `docs/EXCHANGE_IMPORT_GUIDE_RU.md`, `docs/EXCHANGE_IMPORT_GUIDE_EN.md`, `tests/test_exchange_import_guidance.py`.
- Why this work happened: Phase 15 needed factual local command guidance, setup checklist, troubleshooting, and CSV fallback copy for read-only exchange import.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/test_exchange_import_guidance.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 191 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed. Review skipped under orchestrator doc/test-only skip rule.
- Follow-ups: implement T61 Exchange Import Evidence Fields.
- Notes for next agent: RU/EN exchange import guides show env-var and non-echo prompt examples, forbid persisted keys/secrets, document non-read-only/missing symbol/category/time range/rate limit/unverifiable permission failures, and keep CSV upload as fallback.

### 2026-05-09 - T59 - Exchange Import Operator Runbook

- Scope: `docs/AUDIT_WORKSPACE_RUNBOOK_RU.md`, `docs/PILOT_INTAKE_CONTRACT_RU.md`, `docs/EXCHANGE_API_IMPORT_PLAN_RU.md`, `tests/test_exchange_import_runbook.py`.
- Why this work happened: Phase 15 needed operator and intake docs to present read-only API import as an optional path alongside CSV upload without expanding product scope.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/test_exchange_import_runbook.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 188 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed. Review skipped under orchestrator doc/test-only skip rule.
- Follow-ups: implement T60 Exchange Import CLI Safety Guidance.
- Notes for next agent: Docs now distinguish `csv_export`, `bybit_read_only_api`, and `binance_read_only_api`; require read-only keys with trading/order, withdrawal, transfer, leverage/margin, and account-mutation permissions disabled; prefer IP allowlisting; and repeat local-secret/no-advice/no-live-control/no-order-blocking boundaries.

### 2026-05-09 - T58 - Binance Import-to-Audit Integration

- Scope: `trader_risk_audit/cli.py`, `tests/integration/test_binance_import_to_audit.py`, `tests/fixtures/exchange/binance/`.
- Why this work happened: Phase 14 needed proof that the Binance Spot fixture import path feeds the deterministic audit workflow end to end before the phase gate.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_binance_import_to_audit.py tests/integration/test_exchange_import_cli.py -q --tb=short` -> 5 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 185 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; light review passed with P0:0, P1:0.
- Follow-ups: run Phase 14 boundary review before starting T59.
- Notes for next agent: `exchange-import fixture` now routes Binance fixtures through `normalize_binance_spot_trades`, records `binance.spot.my_trades` as the raw snapshot endpoint label, writes normalized CSV row ids that survive the existing `audit` command, and keeps credentials/signatures out of report and audit manifest output.

### 2026-05-09 - T57 - Binance Raw-to-Canonical Normalizer

- Scope: `trader_risk_audit/exchange/binance.py`, `tests/unit/exchange/test_binance_normalizer.py`, `tests/fixtures/exchange/binance/`.
- Why this work happened: Phase 14 needed Binance Spot trade-history records mapped into canonical trade records before proving import-to-audit integration.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_binance_normalizer.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests/test_exchange_fixture_policy.py tests/unit/exchange/test_binance_normalizer.py -q --tb=short` -> 6 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 182 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; light review passed with P0:0, P1:0.
- Follow-ups: implement T58 Binance Import-to-Audit Integration, then run the Phase 14 boundary review.
- Notes for next agent: `normalize_binance_spot_trades` sorts synthetic/raw-like Binance Spot records by time, order id, trade id, and symbol; delegates canonical mapping to the shared exchange normalizer; replaces row ids with traceable `binance_spot_{symbol}_{order}_{trade}_{timestamp}` values; preserves fee asset and maker/taker metadata; and emits field-only unsupported-field warnings.

### 2026-05-09 - T56 - Binance Spot Trade Fetch Planner

- Scope: `trader_risk_audit/exchange/binance.py`, `trader_risk_audit/cli.py`, `tests/unit/exchange/test_binance_fetch_plan.py`, `tests/integration/test_binance_import_cli.py`.
- Why this work happened: Phase 14 needed deterministic Binance Spot `myTrades` request planning before fixture-backed Binance normalization and import-to-audit integration.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_binance_fetch_plan.py tests/integration/test_binance_import_cli.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 179 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; light review passed with P0:0, P1:0.
- Follow-ups: implement T57 Binance Raw-to-Canonical Normalizer.
- Notes for next agent: `plan_binance_spot_trade_fetches` requires explicit symbols plus timezone-qualified start/end times, normalizes symbols to sorted uppercase unique values, emits 24-hour Spot `myTrades` windows with safe endpoint metadata, and the CLI `exchange-import binance-spot-plan` prints the plan without network calls or credentials.

### 2026-05-09 - T55 - Binance Signed Account Request Helper

- Scope: `trader_risk_audit/exchange/binance.py`, `tests/unit/exchange/test_binance_signing.py`, targeted security review artifacts.
- Why this work happened: Phase 14 needed deterministic Binance account-data request signing before Binance fetch planning.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_binance_signing.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 176 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; targeted Cycle 18 security review archived in `docs/archive/CYCLE18_T55_SECURITY_REVIEW.md` with P0:0, P1:0, P2:0.
- Follow-ups: implement T56 Binance Spot Trade Fetch Planner.
- Notes for next agent: `BinanceSigner` builds deterministic HMAC-signed Spot `myTrades` requests from fixture credentials only. Repr/safe metadata redact API key and signature, and endpoint labels are limited to `binance.spot.my_trades`. No real Binance network client exists.

### 2026-05-09 - T54 - Bybit Import-to-Audit Integration

- Scope: `trader_risk_audit/exchange/bybit.py`, `trader_risk_audit/cli.py`, `trader_risk_audit/trades/schema.py`, `trader_risk_audit/trades/importers.py`, `tests/integration/test_bybit_import_to_audit.py`, `tests/fixtures/exchange/bybit/`, Phase 13 review artifacts.
- Why this work happened: Phase 13 needed proof that the Bybit read-only fixture import path feeds the deterministic audit workflow end to end.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/trades/test_importers.py tests/unit/exchange/test_bybit_normalizer.py tests/integration/test_bybit_import_to_audit.py -q --tb=short` -> 10 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 173 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; Phase 13 deep review archived in `docs/archive/PHASE13_REVIEW.md` with P0:0, P1:0, P2:1 fixed.
- Follow-ups: start Phase 14 with T55 Binance Signed Account Request Helper.
- Notes for next agent: Bybit fixture import now uses `normalize_bybit_executions`, writes `row_id` into `normalized_trades.csv`, and audit preserves Bybit execution ids in violation source rows. CSV imports reject duplicate row ids to avoid attribution bucket collisions. No real Bybit network code exists.

### 2026-05-09 - T53 - Bybit Raw-to-Canonical Normalizer

- Scope: `trader_risk_audit/exchange/bybit.py`, `tests/unit/exchange/test_bybit_normalizer.py`, `tests/fixtures/exchange/bybit/`.
- Why this work happened: Phase 13 needed Bybit execution records mapped into canonical trade records before proving import-to-audit integration.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_bybit_normalizer.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 169 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T54 Bybit Import-to-Audit Integration and then run the Phase 13 boundary review.
- Notes for next agent: `normalize_bybit_executions` sorts raw executions by execution timestamp, execution id, order id, and symbol before delegating to the shared exchange normalizer. Unsupported Bybit fields emit field-only warnings with record refs and do not include raw values. The committed Bybit execution fixture is synthetic and includes fixture-policy `fields_removed` metadata.

### 2026-05-09 - T52 - Bybit Execution Fetch Planner

- Scope: `trader_risk_audit/exchange/bybit.py`, `tests/unit/exchange/test_bybit_fetch_plan.py`, docs state.
- Why this work happened: Phase 13 needed deterministic Bybit execution-history fetch planning before raw-to-canonical Bybit normalization.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_bybit_fetch_plan.py tests/unit/exchange/test_bybit_permissions.py -q --tb=short` -> 6 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 166 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T53 Bybit Raw-to-Canonical Normalizer.
- Notes for next agent: `plan_bybit_execution_fetches` supports `spot` and `linear` only, slices ranges into seven-day windows, and `collect_bybit_cursor_pages` follows mocked `nextPageCursor` responses deterministically. Allowed endpoint labels are limited to execution history and key-info; no order/write endpoint labels or network execution exists.

### 2026-05-09 - T51 - Bybit API Key Metadata Check

- Scope: `trader_risk_audit/exchange/bybit.py`, `tests/unit/exchange/test_bybit_permissions.py`, targeted security review artifacts.
- Why this work happened: Phase 13 needed Bybit-specific read-only API key metadata inspection before execution fetch planning.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_bybit_permissions.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 163 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed; targeted Cycle 16 security review archived in `docs/archive/CYCLE16_T51_SECURITY_REVIEW.md` with P0:0, P1:0, P2:0.
- Follow-ups: implement T52 Bybit Execution Fetch Planner.
- Notes for next agent: `check_bybit_api_key_permissions` and `require_bybit_read_only_permissions` inspect fixture/mocked Bybit metadata only. They delegate to the shared credential contract, reject non-read-only or write/control permissions, and never include raw API key, secret, passphrase, or account id values in safe metadata or errors. No real Bybit network client exists yet.

### 2026-05-09 - T50 - Fixture-Backed Exchange Import CLI

- Scope: `trader_risk_audit/cli.py`, `tests/integration/test_exchange_import_cli.py`, `tests/integration/test_exchange_import_to_audit.py`, docs state.
- Why this work happened: Phase 12 needed local fixture-backed exchange import plumbing that writes raw snapshot, normalized trade CSV, and import manifest artifacts without real exchange network calls.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_exchange_import_cli.py tests/integration/test_exchange_import_to_audit.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 160 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 12 boundary review before starting T51 Bybit API Key Metadata Check.
- Notes for next agent: `exchange-import fixture` reads only local sanitized fixture JSON, writes `raw_snapshot.json`, `normalized_trades.csv`, and `import_manifest.json`, and the existing `audit` command consumes the normalized CSV. No Binance/Bybit network client exists yet.

### 2026-05-09 - T49 - Exchange Normalizer Interface

- Scope: `trader_risk_audit/exchange/normalizer.py`, `tests/unit/exchange/test_normalizer.py`, docs state.
- Why this work happened: Phase 12 needed a shared deterministic mapping layer from sanitized exchange raw records into existing canonical trade records before fixture-backed CLI import.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_normalizer.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 157 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T50 Fixture-Backed Exchange Import CLI.
- Notes for next agent: `normalize_exchange_records` maps Bybit/Binance-like aliases into `TradeRecord`, uses deterministic `exchange_...` row ids derived from exchange, symbol, execution/trade/order id, and timestamp, and raises safe field-only `ExchangeNormalizationError` messages.

### 2026-05-09 - T48 - Exchange Raw Snapshot Schema and Import Manifest

- Scope: `trader_risk_audit/exchange/snapshot.py`, `trader_risk_audit/exchange/manifest.py`, `tests/unit/exchange/test_snapshot_schema.py`, `tests/unit/exchange/test_import_manifest.py`, docs state.
- Why this work happened: Phase 12 needed deterministic local raw snapshot and import manifest structures before exchange normalization or fixture-backed CLI plumbing.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_snapshot_schema.py tests/unit/exchange/test_import_manifest.py -q --tb=short` -> 5 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 154 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T49 Exchange Normalizer Interface.
- Notes for next agent: raw snapshots reject credential/sensitive field names recursively, import manifests stay separate from final audit manifests, and manifest content hashes include artifact hashes plus exchange/time-range metadata while excluding `generated_at`.

### 2026-05-09 - T47 - Exchange Fixture and Redaction Policy

- Scope: `docs/EXCHANGE_FIXTURE_POLICY_RU.md`, `tests/test_exchange_fixture_policy.py`, `tests/fixtures/exchange/`, docs state.
- Why this work happened: Phase 11 needed a fixture/redaction gate before committing raw exchange-like examples for later import plumbing.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/test_exchange_fixture_policy.py tests/integration/test_pilot_fixture_pack.py -q --tb=short` -> 6 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 149 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 11 boundary review before starting T48 Exchange Raw Snapshot Schema and Import Manifest.
- Notes for next agent: exchange fixtures must be synthetic or explicitly sanitized, labeled `regression_test_only`, and scanned for API keys, signatures, account ids, balances, customer identifiers, and private notes. The committed Binance/Bybit examples are synthetic and contain no real account history.

### 2026-05-09 - T46 - Exchange Credential Permission Contract

- Scope: `trader_risk_audit/exchange/credentials.py`, `tests/unit/exchange/test_credentials.py`, `tests/integration/test_exchange_secret_redaction.py`, `docs/IMPLEMENTATION_CONTRACT.md`, docs state.
- Why this work happened: Phase 11 needed deterministic read-only permission handling and credential redaction before any exchange fixtures or connector code.
- Decisions applied: `D-009`, ADR-002
- Evidence collected: `.venv/bin/python -m pytest tests/unit/exchange/test_credentials.py tests/integration/test_exchange_secret_redaction.py -q --tb=short` -> 4 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 146 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T47 Exchange Fixture and Redaction Policy before any fixture-backed import plumbing or exchange network path.
- Notes for next agent: `inspect_exchange_permissions` rejects detectable write/control scopes, `inspect_bybit_api_key_metadata` reads fixture metadata only, unverifiable read-only status returns `needs_operator_review`, and `ExchangeCredentials.to_safe_metadata()` never returns raw API keys, secrets, passphrases, or account ids.

### 2026-05-09 - Roadmap - Read-Only Exchange Import Plan

- Scope: `docs/adr/ADR-002-read-only-exchange-import.md`, `docs/EXCHANGE_API_IMPORT_PLAN_RU.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `README.md`, architecture/scope docs.
- Why this work happened: user requested a safe way to connect Binance/Bybit accounts with limited API permissions and run existing Trader Risk Audit analysis over imported executions.
- Decisions applied: `D-009`, ADR-002 proposed
- Evidence collected: official Binance Spot account endpoint/security docs and Bybit V5 execution/API-key metadata docs reviewed; docs-only update, no code tests added.
- Follow-ups: start T45, then T46-T47 before any real exchange network code.
- Notes for next agent: read-only import is a planned local ingestion path only. Do not implement order placement, cancellation, withdrawals, transfers, leverage/margin mutation, hosted secrets, Telegram credential collection, signal analytics, or advice.

### 2026-05-09 - CODE-1 - Delivery Packet Manifest Hash

- Scope: `trader_risk_audit/cli.py`, demo/public sample manifests, pilot fixture manifest hashes, integration tests, docs state.
- Why this work happened: Cycle 8-11 carried a P2 metadata gap where `telegram_packet.txt` was generated for demos but default audit manifests did not hash it.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_audit_cli.py tests/integration/test_demo_pack.py tests/integration/test_public_sample_pack.py tests/integration/test_pilot_fixture_pack.py tests/integration/test_operator_runbook_cli.py -q --tb=short` -> 17 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 142 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: none.
- Notes for next agent: `audit` writes `telegram_packet.txt` before manifest generation and records it as `delivery_packet`. The packet uses stable `report.md` text so manifest content hashes do not depend on temporary output directories. `operator run` reuses the same packet instead of overwriting it after manifest creation.

### 2026-05-09 - T44 - Paid Pilot Offer Page

- Scope: `docs/PAID_PILOT_OFFER_RU.md`, `docs/PAID_PILOT_OFFER_EN.md`, `tests/test_paid_pilot_offer_page.py`, docs state.
- Why this work happened: Phase 10 needed a static paid pilot offer artifact that explains deliverables, inputs, privacy, price placeholder, and next step without building checkout or SaaS flow.
- Decisions applied: `D-001`, `D-006`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/test_paid_pilot_offer_page.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 142 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: Phase 10 boundary deep review completed. All currently planned tasks through T44 are complete.
- Notes for next agent: offer pages are static copy only. They reference demo script, before/after comparison, objection handling, and pilot intake contract; they do not add checkout, account system, broker control, PMF claims, guaranteed improvement, or live risk prevention.

### 2026-05-09 - T43 - ICP-Specific Demo Variants

- Scope: `docs/ICP_DEMO_VARIANTS_RU.md`, `docs/ICP_DEMO_VARIANTS_EN.md`, `tests/test_icp_demo_variants.py`, docs state.
- Why this work happened: Phase 10 needed targeted founder-led demo angles for likely early adopters without splitting the product before evidence.
- Decisions applied: `D-001`, `D-006`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/test_icp_demo_variants.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 139 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T44 Paid Pilot Offer Page, then run Phase 10 boundary deep review.
- Notes for next agent: ICP variants are positioning only. They keep one post-trade audit product boundary and map all ICPs to the same 10/5/3/2 validation evidence gate.

### 2026-05-09 - T42 - Objection Handling Pack

- Scope: `docs/OBJECTION_HANDLING_RU.md`, `docs/OBJECTION_HANDLING_EN.md`, `tests/test_objection_handling_pack.py`, docs state.
- Why this work happened: Phase 10 needed concise sales enablement for common pilot objections without drifting into legal, investment, performance, or live-control promises.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/test_objection_handling_pack.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 136 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T43 ICP-Specific Demo Variants.
- Notes for next agent: objection docs answer privacy, no broker API, no advice, journal comparison, pricing, and repeat-audit questions; they point back to pilot intake and the 10/5/3/2 paid pilot evidence gate.

### 2026-05-09 - T41 - Before/After Report Comparison

- Scope: `docs/BEFORE_AFTER_REPORT_COMPARISON_RU.md`, `docs/BEFORE_AFTER_REPORT_COMPARISON_EN.md`, `tests/test_before_after_comparison.py`, docs state.
- Why this work happened: Phase 10 needed a conversion asset that explains why a deterministic audit report is more useful than raw export rows.
- Decisions applied: `D-001`, `D-006`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/test_before_after_comparison.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 133 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T42 Objection Handling Pack.
- Notes for next agent: comparison docs use only public sample context and emphasize deterministic rule checks, source row ids, violation-attributed P&L, limitations, and paid pilot CTA without advice/performance/live-control claims.

### 2026-05-09 - T40 - Evidence Capture Automation

- Scope: `trader_risk_audit/evidence.py`, `trader_risk_audit/cli.py`, `docs/PILOT_EVIDENCE_LOG_RU.md`, `tests/unit/test_evidence_capture.py`, docs state.
- Why this work happened: Phase 9 needed local evidence capture so delivered reports are followed by paid status, objections, repeat intent, referrals, and gate counts.
- Decisions applied: `D-001`, `D-006`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/test_evidence_capture.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 130 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: Phase 9 boundary deep review completed; continue to T41 Before/After Report Comparison.
- Notes for next agent: `evidence append` writes local CSV rows using the existing customer log fields; obvious identifiers/raw rows are rejected. `evidence summary` excludes `public_sample_demo`, `internal_demo`, and `demo_artifact` rows from market-validation counts.

### 2026-05-09 - T39 - Operator Runbook CLI

- Scope: `trader_risk_audit/cli.py`, `docs/AUDIT_WORKSPACE_RUNBOOK_RU.md`, `tests/integration/test_operator_runbook_cli.py`, docs state.
- Why this work happened: Phase 9 needed a scriptable operator path from intake files to local audit outputs and queue references.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_operator_runbook_cli.py tests/unit/test_workspace_layout.py -q --tb=short` -> 6 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 127 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T40 Evidence Capture Automation, then run the Phase 9 boundary deep review.
- Notes for next agent: `operator prepare` copies intake files into a local workspace and records `ready_to_run`; `operator run` executes local audit, writes a delivery packet, and records report/packet/manifest refs with `ready_for_review`. CLI output stays at status/path references only.

### 2026-05-09 - T38 - Intake File Validator

- Scope: `trader_risk_audit/intake.py`, `trader_risk_audit/telegram_bot/storage.py`, `trader_risk_audit/telegram_bot/handlers.py`, `tests/unit/test_intake_file_validator.py`, `tests/unit/telegram_bot/test_intake_validation.py`, docs state.
- Why this work happened: Phase 9 needed earlier intake feedback so invalid files are not treated as runnable operator work.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/unit/test_intake_file_validator.py tests/unit/telegram_bot/test_intake_validation.py tests/unit/telegram_bot/test_handlers.py tests/integration/test_telegram_demo_happy_path.py -q --tb=short` -> 10 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 124 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T39 Operator Runbook CLI.
- Notes for next agent: `validate_intake_files` reports safe issue messages for missing CSV columns, unsupported extensions, size limit, missing profile, and missing custom policy. Telegram stores invalid uploads locally with `needs_user_fix` and returns concise feedback without raw rows.

### 2026-05-09 - T37 - Policy Profile Selector

- Scope: `trader_risk_audit/policy/profiles.py`, `trader_risk_audit/workspace.py`, `trader_risk_audit/telegram_bot/handlers.py`, `tests/unit/test_policy_profile_selector.py`, docs state.
- Why this work happened: Phase 9 needed profile selection recorded during intake without replacing trader-owned written rules or adding advice claims.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/unit/test_policy_profile_selector.py tests/unit/test_workspace_layout.py tests/unit/telegram_bot/test_handlers.py -q --tb=short` -> 9 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 120 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T38 Intake File Validator.
- Notes for next agent: `resolve_policy_profile` maps `soft`, `medium`, and `hard` to committed starter YAML templates; `custom` requires an explicit policy path. Workspace metadata stores only selected profile/source/path labels, with absolute paths reduced to file names.

### 2026-05-09 - T36 - Two-Minute Demo Script

- Scope: `docs/DEMO_SCRIPT_RU.md`, `docs/DEMO_SCRIPT_EN.md`, `tests/test_demo_script.py`, docs state.
- Why this work happened: Phase 8 needed founder-ready RU/EN scripts that turn the demo into a clear two-minute paid-pilot ask without drifting into feature discussion or unsupported claims.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/test_demo_script.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 117 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: Phase 8 boundary deep review completed; continue to T37 Policy Profile Selector.
- Notes for next agent: demo scripts explicitly push to real export, written rules, mapping approval, and one paid manual audit. They label the public sample as not market validation/PMF evidence and keep no-advice/no-live-control/no-broker/no-signal/no-order-blocking boundaries.

### 2026-05-09 - T35 - Report Polish for Demo Readability

- Scope: `trader_risk_audit/reporting/model.py`, `trader_risk_audit/reporting/markdown.py`, report fixtures, `tests/unit/reporting/test_demo_report_readability.py`, docs state.
- Why this work happened: Phase 8 needed audit reports to be readable in a two-minute founder-led demo without weakening deterministic evidence or claim boundaries.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/unit/reporting/test_demo_report_readability.py tests/unit/reporting/test_markdown_report.py tests/unit/reporting/test_report_model.py -q --tb=short` -> 9 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 114 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T36 Two-Minute Demo Script, then run the Phase 8 boundary deep review.
- Notes for next agent: reports now begin with `Executive Summary` showing rules reviewed, violations recorded, affected P&L, and selected policy profile. This is a presentation layer change only; source-row traceability, claim guard validation, and local-only scope remain unchanged.

### 2026-05-09 - T34 - Public Sample Demo Mode

- Scope: `trader_risk_audit/cli.py`, `trader_risk_audit/telegram_bot/handlers.py`, `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`, `tests/integration/test_public_sample_demo_mode.py`, docs state.
- Why this work happened: Phase 8 needed a local demo mode that shows the public sample audit before a prospect sends private files.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_public_sample_demo_mode.py tests/integration/test_telegram_demo_happy_path.py tests/test_baseline_smoke.py -q --tb=short` -> 9 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 111 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T35 Report Polish for Demo Readability.
- Notes for next agent: `demo public-sample` is read-only and reuses `demo/public_sample_001/output/report.md` plus `telegram_packet.txt`; it does not create a separate report format or count the public sample as prospect/paid/PMF evidence.

### 2026-05-09 - T33 - Telegram Demo Happy Path

- Scope: `trader_risk_audit/telegram_bot/handlers.py`, `trader_risk_audit/telegram_bot/delivery.py`, `tests/integration/test_telegram_demo_happy_path.py`, `docs/TELEGRAM_DEMO_FLOW_RU.md`, docs state.
- Why this work happened: Phase 8 needed a coherent mocked Telegram demo path from `/start` and `/new_audit` through public sample selection, audit id/status, and operator-approved delivery copy.
- Decisions applied: `D-001`, `D-006`, `D-008`, ADR-001
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_telegram_demo_happy_path.py tests/integration/test_telegram_pilot_flow.py tests/unit/telegram_bot -q --tb=short` -> 12 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 108 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T34 Public Sample Demo Mode.
- Notes for next agent: T33 added `TelegramDemoSample`, `/demo_sample`, and `build_approved_delivery_copy`. It remains mocked/local and does not add real Telegram network access, broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior.

### 2026-05-08 - T32 - Internal Outreach Readiness Review

- Scope: `docs/INTERNAL_VALIDATION_REVIEW_RU.md`, `tests/test_internal_readiness_review.py`, docs state.
- Why this work happened: Phase 7 needed an explicit go/no-go decision separating internal product confidence from market validation.
- Decisions applied: `D-001`, `D-006`, `D-007`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/test_internal_readiness_review.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 105 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run mandatory Phase 7 boundary deep review and archive it before advancing to Phase 8.
- Notes for next agent: readiness verdict is go for manual outreach, not PMF. Paid pilot gate remains 3 paid audit reports from 10 qualified prospects within 14 days, then 2 repeat commitments within 30 days.

### 2026-05-08 - T31 - Public Sample Evidence Pack

- Scope: `demo/public_sample_001/`, `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`, `tests/integration/test_public_sample_pack.py`, docs state.
- Why this work happened: Phase 7 needed a reproducible public-like internal validation pack before the outreach readiness review.
- Decisions applied: `D-001`, `D-006`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_public_sample_pack.py -q --tb=short` -> 5 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 102 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T32 Internal Outreach Readiness Review, then run Phase 7 boundary deep review.
- Notes for next agent: `demo/public_sample_001/` is internal/demo evidence only. It uses a public-like SEC Form 4-derived fixture path, hard starter profile context, generated deterministic audit artifacts, a copyable Telegram packet, and explicit non-market-validation labels.

### 2026-05-08 - T30 - Public Sample Source Policy

- Scope: `docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md`, `tests/test_public_sample_source_policy.py`, existing starter policy profile docs/templates/tests.
- Why this work happened: Phase 7 needed source, licensing, privacy, evidence-labeling, starter profile, and outreach readiness rules before building a public sample evidence pack.
- Decisions applied: `D-001`, `D-006`, `D-008`
- Evidence collected: `.venv/bin/python -m pytest tests/test_public_sample_source_policy.py tests/test_starter_policy_profiles.py -q --tb=short` -> 9 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 97 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T31 Public Sample Evidence Pack using the T30 policy, starter profiles, and ADR-001 Telegram boundary.
- Notes for next agent: T30 did not fetch public data or add sample artifacts. T31 must record exact source URL, access date, license/terms summary, transformation steps, privacy removals, and internal/demo labeling.

### 2026-05-07 - Phase 6 Planning - Pilot Validation and Telegram Intake

- Scope: `STARTUP_PRESSURE_TEST_RU.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`
- Why this work happened: founder requested a development-loop continuation that creates real demo/pilot artifacts and a simple Telegram path for file intake and report delivery.
- Decisions applied: `D-007`, `D-008`
- Evidence collected: planning-only update; no product code changed and no tests run.
- Follow-ups: start T21 Demo Audit Pack; do not implement Telegram bot work until T24 files the Telegram intake/delivery ADR.
- Notes for next agent: Telegram is allowed only as constrained intake/delivery. It must not accept broker API keys, block orders, parse signal channels, generate trading advice, or determine final violation truth.

### 2026-05-07 - T20 - Pilot Regression Fixture Pack

- Scope: `tests/integration/test_pilot_fixture_pack.py`, `tests/fixtures/pilot/trades.csv`, `tests/fixtures/pilot/policy.yaml`, `tests/fixtures/expected/pilot_violations.json`, `tests/fixtures/expected/pilot_attribution.json`, `tests/fixtures/expected/pilot_report.md`, `tests/fixtures/expected/pilot_manifest_hashes.json`, docs state.
- Why this work happened: Phase 5 needed a durable anonymized end-to-end regression pack to close the concierge pilot workflow baseline.
- Decisions applied: `D-001`, `D-006`
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_pilot_fixture_pack.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 61 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 5 boundary deep review and archive the result.
- Notes for next agent: pilot fixtures use synthetic `demo` account data only. The integration test regenerates local audit outputs and compares deterministic violations, attribution, report Markdown, manifest content hash, and artifact hashes to expected files.

### 2026-05-07 - T19 - Local Retention and Deletion Workflow

- Scope: `trader_risk_audit/storage/__init__.py`, `trader_risk_audit/storage/retention.py`, `trader_risk_audit/cli.py`, `tests/unit/storage/test_retention.py`, docs state.
- Why this work happened: Phase 5 needed local operator controls to list and delete manifest-referenced audit artifact groups without exposing raw trade data in command output.
- Decisions applied: `D-001`, `D-006`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/storage/test_retention.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 58 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T20 Pilot Regression Fixture Pack, then run Phase 5 boundary deep review.
- Notes for next agent: retention list reads only manifest metadata and report path. `delete_manifest_artifacts` returns the referenced path set for dry-runs without deleting files, and confirmed deletion requires `confirm_delete=True`.

### 2026-05-07 - T18 - Telegram-Ready Delivery Packet

- Scope: `trader_risk_audit/reporting/delivery.py`, `trader_risk_audit/reporting/__init__.py`, `tests/unit/reporting/test_delivery_packet.py`, docs state.
- Why this work happened: Phase 5 needed copyable Telegram-ready report text without enabling bot delivery, credentials, or network egress.
- Decisions applied: `D-001`, `D-006`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/reporting/test_delivery_packet.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 55 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T19 Local Retention and Deletion Workflow.
- Notes for next agent: `render_delivery_packet` validates the source report with claim guard, includes the required disclaimer and local report path, and truncates repeated pattern details deterministically when a character limit requires it. It does not send Telegram messages or read credentials.

### 2026-05-07 - T17 - End-to-End Audit CLI

- Scope: `trader_risk_audit/cli.py`, `tests/integration/test_audit_cli.py`, docs state.
- Why this work happened: Phase 5 needed the local audit command wired from fixtures and policy input through deterministic artifacts, report Markdown, and manifest output.
- Decisions applied: `D-001`, `D-006`
- Evidence collected: `.venv/bin/python -m pytest tests/integration/test_audit_cli.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 52 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T18 Telegram-Ready Delivery Packet.
- Notes for next agent: `audit` is local-only and writes `normalized_trades.json`, `violations.json`, `attribution_summary.json`, `report.md`, and `manifest.json`. Policy review gating runs before output files are written; unresolved review items return non-zero and produce no report.

### 2026-05-07 - T16 - Artifact Manifest and Reproducible Hashes

- Scope: `trader_risk_audit/artifacts/__init__.py`, `trader_risk_audit/artifacts/manifest.py`, `tests/unit/artifacts/test_manifest.py`, docs state.
- Why this work happened: Phase 4 needed reproducible manifest hashes before the end-to-end audit CLI can package complete audit outputs.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/artifacts/test_manifest.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 49 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 4 boundary deep review before starting T17.
- Notes for next agent: `compute_content_hash` includes package version plus artifact names and SHA-256 values only. `generated_at`, local paths, command, and command arguments remain manifest metadata and are excluded from deterministic content-hash inputs.

### 2026-05-07 - T15 - Claim Guard and Disclaimers

- Scope: `trader_risk_audit/reporting/claim_guard.py`, `trader_risk_audit/reporting/markdown.py`, `trader_risk_audit/reporting/__init__.py`, `tests/unit/reporting/test_claim_guard.py`, `tests/fixtures/expected/report_expected.md`, docs state.
- Why this work happened: Phase 4 needed deterministic report-language guardrails before artifact manifests and delivery packaging.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/reporting/test_claim_guard.py tests/unit/reporting/test_markdown_report.py -q --tb=short` -> 6 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 46 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T16 Artifact Manifest and Reproducible Hashes.
- Notes for next agent: Markdown reports now include the required not-investment-advice/no-live-control disclaimer. `validate_report_claims` returns structured categories and exact matched text for missing disclaimer and forbidden phrase failures.

### 2026-05-07 - T14 - Markdown Report Generator

- Scope: `trader_risk_audit/reporting/markdown.py`, `trader_risk_audit/reporting/__init__.py`, `tests/unit/reporting/test_markdown_report.py`, `tests/fixtures/expected/report_expected.md`, docs state.
- Why this work happened: Phase 4 needed deterministic Markdown rendering from the report model before claim guard validation and artifact manifests.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/reporting/test_markdown_report.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 43 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T15 Claim Guard and Disclaimers.
- Notes for next agent: Markdown rendering is a pure transformation of `ReportModel`; it does not add generation timestamps. Golden fixture `tests/fixtures/expected/report_expected.md` locks byte-identical output for the sample model.

### 2026-05-07 - T13 - Report Model and Summaries

- Scope: `trader_risk_audit/reporting/model.py`, `trader_risk_audit/reporting/__init__.py`, `tests/unit/reporting/test_report_model.py`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`
- Why this work happened: Phase 4 needed a deterministic report data model before Markdown rendering, claim guard validation, and artifact manifests.
- Decisions applied: `D-001`, `D-005`
- Evidence collected: `.venv/bin/python -m pytest tests/unit/reporting/test_report_model.py -q --tb=short` -> 3 passed; `.venv/bin/python -m pytest tests -q --tb=short` -> 40 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T14 Markdown Report Generator.
- Notes for next agent: report model only; no Markdown rendering yet. Unsupported-data warnings are represented as limitations and do not appear in the violation table.

### 2026-05-07 - T12 - Violation P&L Attribution

- Scope: `trader_risk_audit/evaluation/attribution.py`, `trader_risk_audit/evaluation/__init__.py`, `tests/unit/evaluation/test_attribution.py`, `tests/integration/test_attribution_golden.py`, `tests/fixtures/trades/attribution_overlap.csv`, `tests/fixtures/expected/attribution_overlap_expected.json`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 3 needed reconciled P&L attribution before report generation, with proof that overlapping violations do not double count top-level P&L.
- Decisions applied: `D-005`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 37 passed; `.venv/bin/python -m pytest tests/unit/evaluation/test_attribution.py tests/integration/test_attribution_golden.py -q --tb=short` -> 4 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 3 boundary review before starting T13.
- Notes for next agent: `attribute_pnl` assigns each row exactly one top-level bucket; rule-level attribution may overlap; `ensure_reconciled` raises before report generation when reconciliation delta is non-zero.

### 2026-05-07 - T11 - Violation Record Determinism

- Scope: `trader_risk_audit/evaluation/violations.py`, `trader_risk_audit/evaluation/__init__.py`, `tests/unit/evaluation/test_violation_records.py`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 3 needed stable violation ids, deterministic violation serialization ordering, and separate unsupported-data warning serialization before attribution work.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 33 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T12 violation P&L attribution with heavy-task evidence.
- Notes for next agent: `build_violation_id` hashes audit id, rule id, rule type, sorted source row ids, and evaluated timestamp only; generated timestamps and file system paths are excluded.

### 2026-05-07 - T10 - Loss, Drawdown, and Cooldown Evaluators

- Scope: `trader_risk_audit/evaluation/rules.py`, `trader_risk_audit/evaluation/violations.py`, `trader_risk_audit/evaluation/__init__.py`, `tests/unit/evaluation/test_loss_rules.py`, `tests/fixtures/policies/loss_rules_policy.yaml`, `tests/fixtures/trades/loss_rule_scenarios.csv`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 3 needed deterministic source-traceable evaluators for max daily loss, max drawdown, and cooldown-after-loss.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 30 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T11 deterministic violation ids and serialization.
- Notes for next agent: Threshold semantics are strict greater-than (`>`). Daily loss and drawdown flag trades after breach timestamps, and cooldown flags trades where `window_start < trade.timestamp <= window_end`.

### 2026-05-07 - T09 - Position and Asset Rule Evaluators

- Scope: `trader_risk_audit/evaluation/rules.py`, `trader_risk_audit/evaluation/violations.py`, `trader_risk_audit/evaluation/__init__.py`, `tests/unit/evaluation/test_position_asset_rules.py`, `tests/fixtures/policies/position_asset_policy.yaml`, `tests/fixtures/trades/position_asset_trades.csv`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 3 needed deterministic source-traceable evaluators for forbidden assets, position size, and unsupported leverage data.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 27 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T10 loss, drawdown, and cooldown evaluators.
- Notes for next agent: `evaluate_position_asset_rules` returns `EvaluationResult` with `ViolationRecord` and `UnsupportedDataWarning`; max leverage currently warns on missing leverage fields and emits no guessed violation.

### 2026-05-07 - T08 - Session Calendar and Aggregates

- Scope: `trader_risk_audit/evaluation/`, `tests/unit/evaluation/test_aggregates.py`, `tests/fixtures/trades/aggregate_scenarios.csv`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 3 needed deterministic session/day grouping, realized P&L aggregation, exposure totals, and equity curve inputs before rule evaluators.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 24 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T09 position and asset rule evaluators.
- Notes for next agent: `assign_session_date` uses configured timezone and session start; `build_daily_aggregates` subtracts fees from gross realized P&L; `build_equity_curve` records points for every closed trade event, including zero-gross closures with fees.

### 2026-05-07 - T07 - Policy Review Packet

- Scope: `trader_risk_audit/policy/review.py`, `trader_risk_audit/policy/validation.py`, `trader_risk_audit/policy/__init__.py`, `tests/unit/policy/test_policy_review.py`, `tests/fixtures/policies/ambiguous_policy.yaml`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 2 needed a deterministic human approval artifact and evaluation gate for ambiguous policy mappings.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 21 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 2 boundary review before starting T08.
- Notes for next agent: `build_review_packet` flags missing deterministic fields, `ensure_policy_ready_for_evaluation` blocks unresolved review packets, and `apply_review_decisions` preserves original `source_text` in rule params.

### 2026-05-07 - T06 - Risk Policy Schema

- Scope: `trader_risk_audit/policy/`, `tests/unit/policy/test_policy_schema.py`, `tests/fixtures/policies/valid_policy.yaml`, `tests/fixtures/policies/unsupported_rule_policy.yaml`, `pyproject.toml`, `requirements.txt`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 2 needed a versioned risk policy schema before policy review packets and evaluator entry points.
- Decisions applied: `D-001`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 18 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T07 policy review packet for ambiguous or incomplete rules.
- Notes for next agent: Policy loading uses Pydantic and PyYAML declared in runtime dependencies; unsupported rule types raise `UnsupportedRuleTypeError` with both `rule_id` and unsupported type.

### 2026-05-07 - T05 - Trade Export Importer

- Scope: `trader_risk_audit/trades/importers.py`, `trader_risk_audit/trades/__init__.py`, `tests/unit/trades/test_importers.py`, `tests/fixtures/trades/supported_export.csv`, `tests/fixtures/trades/missing_columns_export.csv`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 2 needed deterministic local CSV normalization from supported broker-like exports into canonical trade records.
- Decisions applied: `D-003`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 15 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T06 risk policy schema.
- Notes for next agent: `normalize_csv` injects `source_file` and CSV line-based `source_row_number`, sorts records by timestamp then source row number, and `serialize_trade_records` emits stable JSON.

### 2026-05-07 - T04 - Canonical Trade Schema

- Scope: `trader_risk_audit/trades/`, `tests/unit/trades/test_trade_schema.py`, `tests/fixtures/trades/valid_trades.csv`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 2 needed the canonical trade record boundary before importer and evaluator tasks.
- Decisions applied: `D-001`, `D-003`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 12 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T05 supported CSV importer using `TradeRecord.from_mapping`.
- Notes for next agent: side aliases are configurable, timestamps require timezone, and validation errors expose canonical field names through `TradeValidationError.fields`.

### 2026-05-07 - T03 - Baseline Smoke Tests

- Scope: `tests/test_baseline_smoke.py`, `docs/CODEX_PROMPT.md`, `docs/EVIDENCE_INDEX.md`
- Why this work happened: Phase 1 needed a smoke baseline for package import behavior, CLI command surface, and the shared tracing boundary before domain behavior starts.
- Decisions applied: `D-001`, `D-006`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 9 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: run Phase 1 boundary review before starting T04.
- Notes for next agent: CLI command groups remain stubs only; domain behavior begins in Phase 2.

### 2026-05-07 - T02 - CI Contract Tests

- Scope: `.github/workflows/ci.yml`, `tests/test_ci_contract.py`, `docs/tasks.md`
- Why this work happened: Phase 1 needed a local test contract for the product CI workflow before domain behavior starts.
- Decisions applied: `D-002`, `D-006`
- Evidence collected: `.venv/bin/python -m pytest tests -q --tb=short` -> 6 passed; `.venv/bin/python -m ruff check trader_risk_audit tests` -> passed; `.venv/bin/python -m ruff format --check trader_risk_audit tests` -> passed.
- Follow-ups: implement T03 baseline smoke tests.
- Notes for next agent: `.github/workflows/ci.yml` is the supported workflow; `ci/ci.yml` still appears to be a generic template and should not be treated as the operational CI definition.

### 2026-05-07 - T01 - Project Skeleton

- Scope: `pyproject.toml`, `requirements*.txt`, `trader_risk_audit/`, `tests/test_project_skeleton.py`, `RUNBOOK.md`
- Why this work happened: Phase 1 needed an executable Python package and supported local validation commands.
- Decisions applied: `D-001`, `D-006`
- Evidence collected: pre-T02 `.venv/bin/python -m pytest tests -q --tb=short` -> 3 passed.
- Follow-ups: complete T02 and T03 before Phase 2.
- Notes for next agent: CLI command groups are stubs; do not interpret them as audit execution behavior.

### 2026-05-07 - Bootstrap - Phase 1 Governance Package

- Scope: `docs/`, `.github/workflows/ci.yml`, `.claude/commands/orchestrate.md`
- Why this work happened: product-local bootstrap-new workflow initialization
- Decisions applied: `D-001`, `D-002`, `D-003`, `D-004`, `D-005`, `D-006`
- Evidence collected: Phase 1 audit pending at `docs/audit/PHASE1_AUDIT.md`
- Follow-ups: run Phase 1 validation before T01
- Notes for next agent: the product is local-first and deterministic; do not add live broker APIs, runtime agent loops, or AI-owned violation truth.
