# CODEX_PROMPT.md

Version: 1.19
Date: 2026-05-09
Phase: Complete

This file is the single source of truth for implementation session state. Every Codex agent reads this file before starting work and updates it at phase boundaries or when the orchestrator records findings.

---

## Current Phase

- Phase: Complete
- Name: Planned Roadmap Complete Through Phase 10
- Business goal: all planned phases are implemented through conversion assets while preserving local-first, deterministic, no-broker, no-signal, no-advice boundaries.
- Phase gate: T41-T44 complete; before/after report comparison, objection handling, ICP demo variants, and paid pilot offer page are done, Phase 10 boundary review is archived, and post-plan CODE-1 manifest cleanup is complete.

## Current State

- Phase: Complete
- Baseline: 142 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
- Last updated: 2026-05-09
- Open findings: none
- Session tokens (approx): not yet tracked
- Cumulative phase tokens (approx): not yet tracked

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Task graph: `docs/tasks.md`
- Implementation contract: `docs/IMPLEMENTATION_CONTRACT.md`
- Task-scoped context: read `Context-Refs` in `docs/tasks.md` before broad searching.

## Next Task

None - all currently planned tasks through T44 are complete.

Task intent:

- Continue only if validation evidence, review findings, or a user request justifies a roadmap update.
- Do not add SaaS accounts, checkout, broker APIs, signal analytics, order blocking, or trading advice without a new ADR and paid pilot evidence.

Required context before starting:

- `docs/archive/PHASE10_REVIEW.md`
- `docs/audit/PHASE_REPORT_LATEST.md`
- `docs/PILOT_EVIDENCE_LOG_RU.md`
- `STARTUP_PRESSURE_TEST_RU.md#14-final-recommendation`

Immediate scope:

- no immediate implementation scope

Candidate source decision:

- Primary: SEC EDGAR Insider Transactions Data Sets / Form 4 non-derivative transactions.
- Use only source rows allowed by `docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md`.
- Filter: P/S transaction rows with required date, ticker, shares, and price where available.
- Mapping: `TRANS_DATE` -> timestamp, `ISSUERTRADINGSYMBOL` -> symbol, `TRANS_ACQUIRED_DISP_CD` A/D -> buy/sell, `TRANS_SHARES` -> quantity, `TRANS_PRICEPERSHARE` -> price, `ACCESSION_NUMBER` plus row key -> source traceability.
- Privacy rule: remove reporting owner names, signatures, remarks, footnotes, relationship titles, owner addresses/identifiers, and unnecessary personal fields before committing a public sample pack.
- Backup: public exchange trade-print samples only if SEC Form 4 cannot support at least three explainable risk scenarios; label backup samples as market prints, not account history.

Starter policy decision:

- Provide three starter audit presets: `soft`, `medium`, and `hard`.
- Treat them as internal validation/demo defaults, not investment advice, strategy recommendations, or optimal risk settings.
- Prefer trader custom rules and prop/funded account rules when available.
- For Phase 7 internal validation, run public samples through these profiles where useful to test explainability across strictness levels.
- T30 completed source policy and starter profile tests. Baseline after T30: 97 passing tests.
- T31 completed `demo/public_sample_001/`, `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`, and public sample pack integration tests. Baseline after T31: 102 passing tests.
- Starter profile reference remains `docs/STARTER_POLICY_PROFILES_RU.md`; Phase 7 treats `soft`, `medium`, and `hard` as customizable audit presets only.
- T32 completed `docs/INTERNAL_VALIDATION_REVIEW_RU.md` and readiness review tests. Baseline after T32: 105 passing tests.
- Phase 7 deep review Cycle 8 archived at `docs/archive/PHASE7_REVIEW.md`: Stop-Ship No, P0:0, P1:0, P2:1 (`CODE-1` delivery packet hash absent from generated manifests).
- T33 completed Telegram demo happy path with mocked-client tests and `docs/TELEGRAM_DEMO_FLOW_RU.md`. Baseline after T33: 108 passing tests.
- T34 completed local `demo public-sample` mode and Telegram sample labeling tests. Baseline after T34: 111 passing tests.
- T35 completed report readability polish: generated reports now start with an executive summary containing rule count, violation count, affected P&L, and selected policy profile while preserving deterministic violation tables, source-row traceability, limitations, next-review checklist, and claim guard boundaries. Baseline after T35: 114 passing tests.
- T36 completed RU/EN two-minute demo scripts covering problem, upload, selected profile, report summary, source-row traceability, P&L impact, next pilot ask, profile explanation, and claim boundaries. Baseline after T36: 117 passing tests.
- Phase 8 deep review Cycle 9 archived at `docs/archive/PHASE8_REVIEW.md`: Stop-Ship No, P0:0, P1:0, P2:0 new; historical carry-forward `CODE-1` was later resolved after Phase 10.
- T37 completed policy profile selector with starter template resolution, custom-policy requirement, non-sensitive workspace metadata, and Telegram `/profiles` copy. Baseline after T37: 120 passing tests.
- T38 completed intake file validation for CSV structure, extension, size, missing profile/custom policy, Telegram safe feedback, and non-runnable invalid upload status. Baseline after T38: 124 passing tests.
- T39 completed operator runbook CLI for local workspace prepare/run and queue output references without raw row output or hosted services. Baseline after T39: 127 passing tests.
- T40 completed evidence capture automation for local customer log append, demo-vs-market evidence separation, and validation gate summaries. Baseline after T40: 130 passing tests.
- Phase 9 deep review Cycle 10 archived at `docs/archive/PHASE9_REVIEW.md`: Stop-Ship No, P0:0, P1:0, P2:0 new; historical carry-forward `CODE-1` was later resolved after Phase 10.
- T41 completed RU/EN before/after report comparison docs showing raw export gaps versus deterministic audit outputs with source rows, violation-attributed P&L, and paid pilot CTA. Baseline after T41: 133 passing tests.
- T42 completed RU/EN objection handling pack for privacy, broker/API, advice, journal comparison, pricing, and repeat audit objections while preserving factual claim boundaries and pilot gate references. Baseline after T42: 136 passing tests.
- T43 completed RU/EN ICP demo variants for prop/funded traders, active crypto discretionary traders, and small teams/coaches, all mapped to the same validation evidence gate and product boundary. Baseline after T43: 139 passing tests.
- T44 completed RU/EN paid pilot offer pages with deliverables, inputs, timeline, privacy/no-advice boundaries, price placeholder, CTA, and references to demo/comparison/objection/intake assets. Baseline after T44: 142 passing tests.
- Phase 10 deep review Cycle 11 archived at `docs/archive/PHASE10_REVIEW.md`: Stop-Ship No, P0:0, P1:0, P2:0 new; historical carry-forward `CODE-1` was later resolved after Phase 10.
- Post-plan CODE-1 cleanup complete: default `audit` now writes `telegram_packet.txt`, hashes it as `delivery_packet` in `manifest.json`, and preserves deterministic manifest content hashes across output directories. Baseline remains 142 passing tests.

ADR-001 is filed. Telegram is an allowed simple demo/intake/delivery surface for Phase 7: a user may upload files, receive an audit id/status, and receive an operator-approved report. Any new Telegram work must stay inside ADR-001 and must not add broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior.

## Future Planned Phases

No future phase beyond Phase 10 is currently planned in this file.

Future phase rule:

- Do not skip Phase 7. T30-T32 must produce internal validation evidence before Phase 8 begins.
- After every phase boundary, run mandatory deep review, archive it, apply required fixes, update state docs, then continue automatically to the next planned phase when no stop-ship finding remains. Do not stop only because a phase completed.
- If deep review findings, pilot evidence, or implementation discoveries show that the roadmap should change, update `docs/tasks.md`, this file, README, and relevant audit notes before continuing.
- Demo productization may improve the upload-status-report experience, especially through Telegram, but must stay within ADR-001 and preserve deterministic audit truth.
- Do not build SaaS accounts, checkout, broker APIs, signal analytics, order blocking, or trading advice unless a later ADR and paid pilot evidence explicitly justify that scope.

Before implementation, the orchestrator should hand Codex a narrow task digest inline:

- assignment and acceptance criteria
- file scope
- applicable contract rules only
- dependency facts from prior tasks
- immediate pipeline or flow if one matters

Only send Codex to full documents when the task is architecture-shaping, security-sensitive, ambiguous, or too risky to compress safely.

## Fix Queue

empty

## Open Findings

| ID | Sev | Description | Files | Status |
|----|-----|-------------|-------|--------|
| none | - | No open findings. CODE-1 was resolved after Phase 10 by adding default delivery packet generation and manifest hashing. | - | Closed |

## Completed Tasks

- T17: End-to-End Audit CLI
- T18: Telegram-Ready Delivery Packet
- T19: Local Retention and Deletion Workflow
- T20: Pilot Regression Fixture Pack
- T21: Demo Audit Pack
- T22: Pilot Intake Contract
- T23: Local Audit Workspace Convention
- T24: Telegram Intake ADR
- T25: Minimal Telegram Bot Skeleton
- T26: Operator Review Queue
- T27: Telegram Delivery Packet Send
- T28: End-to-End Telegram Pilot Test
- T29: Pilot Payment and Evidence Log
- T30: Public Sample Source Policy
- T31: Public Sample Evidence Pack
- T32: Internal Outreach Readiness Review
- T33: Telegram Demo Happy Path
- T34: Public Sample Demo Mode
- T35: Report Polish for Demo Readability
- T36: Two-Minute Demo Script
- T37: Policy Profile Selector
- T38: Intake File Validator
- T39: Operator Runbook CLI
- T40: Evidence Capture Automation
- T41: Before/After Report Comparison
- T42: Objection Handling Pack
- T43: ICP-Specific Demo Variants
- T44: Paid Pilot Offer Page

## Phase History

- Phase 5 Concierge Pilot Workflow complete: T17-T20 delivered end-to-end local audit CLI, Telegram-ready copy packet, retention/delete controls, and anonymized pilot regression fixtures. Baseline moved from 49 to 61 passing tests. Deep review Cycle 5 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 6 Pilot Validation and Telegram Intake complete: T21-T29 delivered synthetic demo artifacts, pilot intake/workspace conventions, ADR-001, constrained Telegram intake/delivery, operator queue, mocked pilot flow, and business evidence log. Baseline moved from 61 to 88 passing tests. Deep review Cycle 7 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 7 Internal Validation with Public Samples complete: T30-T32 delivered source policy, starter profile boundaries, `demo/public_sample_001/`, public sample evidence docs, and a go decision for manual outreach. Baseline moved from 92 to 105 passing tests. Deep review Cycle 8 found P0:0, P1:0, P2:1; Stop-Ship: No.
- Phase 8 Demo Productization complete: T33-T36 delivered Telegram demo happy path, public sample demo mode, report readability polish, and RU/EN two-minute demo scripts. Baseline moved from 105 to 117 passing tests. Deep review Cycle 9 found P0:0, P1:0, P2:0 new; Stop-Ship: No.
- Phase 9 Intake Quality and Operator Speed complete: T37-T40 delivered policy profile selection, intake validation, operator runbook CLI, and evidence capture automation. Baseline moved from 117 to 130 passing tests. Deep review Cycle 10 found P0:0, P1:0, P2:0 new; Stop-Ship: No.
- Phase 10 Conversion Assets complete: T41-T44 delivered before/after comparison, objection handling, ICP demo variants, and paid pilot offer pages. Baseline moved from 130 to 142 passing tests. Deep review Cycle 11 found P0:0, P1:0, P2:0 new; Stop-Ship: No.
- Post-plan CODE-1 cleanup complete: default audit manifests now include `delivery_packet`, committed demo/public sample manifests were regenerated, and pilot fixture hashes were updated. Baseline stayed at 142 passing tests.

## Summary State

- Compacted on 2026-05-07 before T22 because `## Completed Tasks` exceeded 20 entries.
- Compacted on 2026-05-07 after Phase 6 because `## Phase History` exceeded 5 entries.
- Archived completed task detail covers T01-T16; active completed task list keeps Phase 5/6 pilot workflow context.
- Current phase, baseline, next task, open findings, active decisions, and evidence pointers remain in their canonical sections above.

## Archive - Completed Tasks

- T01: Project Skeleton
- T02: CI Setup
- T03: Baseline Smoke Tests
- T04: Canonical Trade Schema
- T05: Trade Export Importer
- T06: Risk Policy Schema
- T07: Policy Review Packet
- T08: Session Calendar and Aggregates
- T09: Position and Asset Rule Evaluators
- T10: Loss, Drawdown, and Cooldown Evaluators
- T11: Violation Record Determinism
- T12: Violation P&L Attribution
- T13: Report Model and Summaries
- T14: Markdown Report Generator
- T15: Claim Guard and Disclaimers
- T16: Artifact Manifest and Reproducible Hashes

## Archive - Phase History

- Phase 1 Foundation complete: T01-T03 delivered package skeleton, CI contract, and baseline smoke tests. Baseline moved from 6 to 9 passing tests. Deep review Cycle 1 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 2 Input Contracts complete: T04-T07 delivered canonical trade records, CSV import normalization, risk policy schema, and policy review packets. Baseline moved from 9 to 21 passing tests. Deep review Cycle 2 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 3 Rule Evaluation complete: T08-T12 delivered session aggregation, deterministic evaluators, violation determinism, and reconciled P&L attribution with golden evidence. Baseline moved from 21 to 37 passing tests. Deep review Cycle 3 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 4 Reporting and Artifacts complete: T13-T16 delivered deterministic report data, Markdown output, claim guard validation, and reproducible artifact manifests. Baseline moved from 37 to 49 passing tests. Deep review Cycle 4 found P0:0, P1:0, P2:0; Stop-Ship: No.

## Compaction Protocol

- Trigger when `## Completed Tasks` exceeds 20 entries or `## Phase History` exceeds 5 phase summaries.
- Preserve current phase, baseline, next task, open findings, active decisions, and evidence pointers.
- Move older detail into an archive section rather than deleting it.

---

## Profile State: RAG

- RAG Status: OFF
- Active corpora: n/a
- Retrieval baseline: n/a
- Open retrieval findings: none
- Index schema version: n/a
- Pending reindex actions: none
- Retrieval-related next tasks: none
- Retrieval-driven tasks: none

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Plan validation method: n/a
- Open plan findings: none

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

## NFR Baseline

- API p99 latency: n/a (no API in v1)
- Batch audit duration: not yet measured
- Error rate: not yet measured
- Throughput: not yet measured
- Last measured: n/a
- NFR regression open: No

## Evaluation State

### Last Evaluation

- Profile: n/a
- Task: n/a
- Date: n/a
- Eval Source: n/a
- Metric(s): n/a
- Score: n/a
- Baseline: n/a
- Delta: n/a
- Regression: n/a

### Open Evaluation Issues

none

### Evaluation History

none

---

## Instructions for Codex

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the full task definition in `docs/tasks.md` before writing code.
3. Read all Depends-On tasks to understand interface contracts.
4. Read task `Context-Refs` and relevant continuity artifacts when the task depends on prior decisions, proof, findings, rule semantics, attribution, retention, or report claims.
5. Run `pytest -q` to capture the current baseline before making changes. If the baseline is broken, stop and report the blocker.
6. Run `ruff check`. It must exit 0 before implementation starts. Fix ruff issues first in a separate commit.
7. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
8. Update this file at every phase boundary with the new baseline, next task, and open findings.
9. Commit with format `type(scope): description` - one logical change per commit.
10. When done, return `IMPLEMENTATION_RESULT: DONE` with the new baseline, tests run, and files changed.
11. When blocked, return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker, command output summary, and affected files.

## Phase 1 Validation

Phase 1 validation was not run before T01 in this workspace, and `docs/audit/PHASE1_AUDIT.md` is absent. Cycle 1 review recorded this as a non-blocking governance warning because the workspace had already advanced to T03 when the orchestrator resumed.
