# CODEX_PROMPT.md

Version: 1.13
Date: 2026-05-08
Phase: 8

This file is the single source of truth for implementation session state. Every Codex agent reads this file before starting work and updates it at phase boundaries or when the orchestrator records findings.

---

## Current Phase

- Phase: 8
- Name: Demo Productization
- Business goal: make the founder-led demo feel like a coherent mini-product from Telegram entry to approved report without confusing public/internal samples with paid pilot evidence or expanding into advice, broker control, signal analytics, or SaaS scope.
- Phase gate: T33-T36 complete; the team has a Telegram demo happy path, public sample demo mode, polished report readability, and RU/EN two-minute scripts that push toward real export/rules and paid pilot commitment.

## Current State

- Phase: 8
- Baseline: 105 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
- Last updated: 2026-05-08
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

T33 - Telegram Demo Happy Path

Task intent:

- Turn the existing Telegram pilot pieces into a coherent demo happy path: start an audit, upload files or choose a demo sample, receive an audit id/status, and receive an operator-approved report.
- Support `/start`, `/new_audit`, file upload guidance, audit id/status response, and approved report delivery copy without requiring real network access in tests.
- Keep the user-facing path clear without exposing raw trade rows, Telegram handles, broker account ids, or private notes.
- Stay inside ADR-001: no broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior.

Required context before starting:

- `docs/IMPLEMENTATION_CONTRACT.md`
- `docs/tasks.md#t33-telegram-demo-happy-path`
- `docs/adr/ADR-001-telegram-intake-delivery.md`
- `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`
- `docs/IMPLEMENTATION_CONTRACT.md#confidential-data-handling`

Immediate scope:

- `trader_risk_audit/telegram_bot/handlers.py`
- `trader_risk_audit/telegram_bot/delivery.py`
- `tests/integration/test_telegram_demo_happy_path.py`
- `docs/TELEGRAM_DEMO_FLOW_RU.md`

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

ADR-001 is filed. Telegram is an allowed simple demo/intake/delivery surface for Phase 7: a user may upload files, receive an audit id/status, and receive an operator-approved report. Any new Telegram work must stay inside ADR-001 and must not add broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior.

## Future Planned Phases

- Phase 9 - Intake Quality and Operator Speed (T37-T40): policy profile selector, intake file validator, operator runbook CLI, and evidence capture automation.
- Phase 10 - Conversion Assets (T41-T44): before/after report comparison, objection handling, ICP-specific demo variants, and paid pilot offer page.

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
| CODE-1 | P2 | Delivery packet hash is absent from generated audit manifests; core audit hashes remain covered, but Telegram-ready delivery packets cannot be verified through `manifest.json`. | `trader_risk_audit/cli.py`, `demo/public_sample_001/output/manifest.json`, `tests/integration/test_public_sample_pack.py` | Open |

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

## Phase History

- Phase 5 Concierge Pilot Workflow complete: T17-T20 delivered end-to-end local audit CLI, Telegram-ready copy packet, retention/delete controls, and anonymized pilot regression fixtures. Baseline moved from 49 to 61 passing tests. Deep review Cycle 5 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 6 Pilot Validation and Telegram Intake complete: T21-T29 delivered synthetic demo artifacts, pilot intake/workspace conventions, ADR-001, constrained Telegram intake/delivery, operator queue, mocked pilot flow, and business evidence log. Baseline moved from 61 to 88 passing tests. Deep review Cycle 7 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 7 Internal Validation with Public Samples complete: T30-T32 delivered source policy, starter profile boundaries, `demo/public_sample_001/`, public sample evidence docs, and a go decision for manual outreach. Baseline moved from 92 to 105 passing tests. Deep review Cycle 8 found P0:0, P1:0, P2:1; Stop-Ship: No.
- Future phases planned: Phase 9 Intake Quality and Operator Speed (T37-T40) and Phase 10 Conversion Assets (T41-T44). These phases improve demo quality and pilot conversion without changing the no-broker, no-signal, no-advice product boundary.

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
