# CODEX_PROMPT.md

Version: 1.31
Date: 2026-05-09
Phase: Phase 13

This file is the single source of truth for implementation session state. Every Codex agent reads this file before starting work and updates it at phase boundaries or when the orchestrator records findings.

---

## Current Phase

- Phase: Phase 14
- Name: Phase 14 - Binance Read-Only MVP
- Business goal: add Binance-specific read-only import planning and fixture-backed normalization while preserving credential redaction and no-control boundaries.
- Phase gate: Phase 14 must prove Binance signed request construction, explicit symbol/window planning, normalizer behavior, and import-to-audit integration against sanitized fixtures before any paid pilot use.

## Current State

- Phase: Phase 14
- Baseline: 176 passing tests
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
- Starter profile reference: `docs/STARTER_POLICY_PROFILES_RU.md` defines internal/demo `soft`, `medium`, and `hard` audit presets; they are customizable validation defaults, not advice.

## Next Task

T56 - Binance Spot Trade Fetch Planner

Task intent:

- Plan deterministic Binance Spot `myTrades` imports by explicit symbols and time ranges.
- Require explicit symbols and date range for Binance spot imports.
- Build deterministic symbol/window requests and record source endpoint metadata.
- Preserve deterministic ordering across symbols and windows.

Required context before starting:

- `docs/adr/ADR-002-read-only-exchange-import.md`
- T55 Binance signed request helper.

Immediate scope:

- `trader_risk_audit/exchange/binance.py`
- `tests/unit/exchange/test_binance_fetch_plan.py`
- `tests/integration/test_binance_import_cli.py`
- Binance all-account history is not assumed; symbols are explicit.

ADR-001 is filed. Telegram is an allowed simple demo/intake/delivery surface for Phase 7: a user may upload files, receive an audit id/status, and receive an operator-approved report. Any new Telegram work must stay inside ADR-001 and must not add broker APIs, signal parsing, order blocking, auto-advice, or live trading behavior.

ADR-002 is accepted. Read-only exchange import is a planned local ingestion path for historical Binance/Bybit fills/executions only. It must not add exchange control, trading, withdrawals, transfers, leverage/margin mutation, hosted secret storage, Telegram credential collection, signal analytics, auto-advice, or live trading behavior. T46 and T47 are complete; Phase 11 boundary review passed with no stop-ship findings before Phase 12 fixture-backed import plumbing starts.

## Future Planned Phases

| Phase | Name | Tasks | Gate |
|-------|------|-------|------|
| 11 | Read-Only Exchange Import Safety | T45-T47 | ADR-002 accepted, credential permission contract defined, exchange fixture/redaction policy in place, no real network calls. |
| 12 | Exchange Import Core | T48-T50 | Fixture-backed import writes raw snapshot, normalized trades, and import manifest; existing `audit` consumes normalized exchange trades. |
| 13 | Bybit Read-Only MVP | T51-T54 | Bybit permission checks, execution fetch planning, normalizer, and import-to-audit integration pass with sanitized fixtures. |
| 14 | Binance Read-Only MVP | T55-T58 | Binance signed account request helper, symbol/window fetch planning, normalizer, and import-to-audit integration pass with sanitized fixtures. |
| 15 | Operator UX and Pilot Validation | T59-T62 | Runbooks, safety guidance, evidence fields, and deep review confirm pilot-ready boundaries. |

Future phase rule:

- Do not skip Phase 7. T30-T32 must produce internal validation evidence before Phase 8 begins.
- After every phase boundary, run mandatory deep review, archive it, apply required fixes, update state docs, then continue automatically to the next planned phase when no stop-ship finding remains. Do not stop only because a phase completed.
- If deep review findings, pilot evidence, or implementation discoveries show that the roadmap should change, update `docs/tasks.md`, this file, README, and relevant audit notes before continuing.
- Demo productization may improve the upload-status-report experience, especially through Telegram, but must stay within ADR-001 and preserve deterministic audit truth.
- Do not build SaaS accounts, checkout, exchange write APIs, broker control, signal analytics, order blocking, or trading advice. Read-only exchange import must stay inside ADR-002 and remain a local post-trade ingestion path.

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
| ARCH-1 | P2 | Product spec now includes bounded local read-only exchange import feature area aligned with ADR-002. | `docs/spec.md` | Closed |
| CODE-1 | P2 | Default audit manifests now include `delivery_packet`; demo/public sample manifests and pilot fixture hashes were regenerated. | `trader_risk_audit/cli.py`, demo fixtures | Closed |
| CODE-2 | P2 | Imported CSV `row_id` values now reject duplicates to prevent attribution bucket collisions. | `trader_risk_audit/trades/importers.py` | Closed |

## Completed Tasks

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
- T45: Read-Only Exchange Import ADR
- T46: Exchange Credential Permission Contract
- T47: Exchange Fixture and Redaction Policy
- T48: Exchange Raw Snapshot Schema and Import Manifest
- T49: Exchange Normalizer Interface
- T50: Fixture-Backed Exchange Import CLI
- T51: Bybit API Key Metadata Check
- T52: Bybit Execution Fetch Planner
- T53: Bybit Raw-to-Canonical Normalizer
- T54: Bybit Import-to-Audit Integration
- T55: Binance Signed Account Request Helper

## Phase History

- Phase 8 Demo Productization complete: T33-T36 delivered Telegram demo happy path, public sample demo mode, report readability polish, and RU/EN two-minute demo scripts. Baseline moved from 105 to 117 passing tests. Deep review Cycle 9 found P0:0, P1:0, P2:0 new; Stop-Ship: No.
- Phase 9 Intake Quality and Operator Speed complete: T37-T40 delivered policy profile selection, intake validation, operator runbook CLI, and evidence capture automation. Baseline moved from 117 to 130 passing tests. Deep review Cycle 10 found P0:0, P1:0, P2:0 new; Stop-Ship: No.
- Phase 10 Conversion Assets complete: T41-T44 delivered before/after comparison, objection handling, ICP demo variants, and paid pilot offer pages. Baseline moved from 130 to 142 passing tests. Deep review Cycle 11 found P0:0, P1:0, P2:0 new; Stop-Ship: No.
- Post-plan CODE-1 cleanup complete: default audit manifests now include `delivery_packet`, committed demo/public sample manifests were regenerated, and pilot fixture hashes were updated. Baseline stayed at 142 passing tests.
- Phase 12 Exchange Import Core complete: T48-T50 delivered raw snapshots, import manifests, exchange normalizer, and fixture-backed `exchange-import fixture` CLI. Baseline moved from 149 to 160 passing tests. Deep review Cycle 15 found P0:0, P1:0, P2:1; Stop-Ship: No.
- Phase 13 Bybit Read-Only MVP complete: T51-T54 delivered Bybit permission checks, execution fetch planning, normalizer, and fixture-backed import-to-audit integration. Baseline moved from 163 to 173 passing tests. Deep review Cycle 17 found P0:0, P1:0, P2:1 fixed; Stop-Ship: No.

## Summary State

- Compacted on 2026-05-09 after T50 because `## Phase History` exceeded 5 summaries.
- Compacted on 2026-05-09 after T48 because `## Completed Tasks` exceeded 20 entries.
- Compacted on 2026-05-09 before T45 because `## Completed Tasks` and `## Phase History` exceeded active-state thresholds.
- Compacted on 2026-05-07 before T22 because `## Completed Tasks` exceeded 20 entries.
- Compacted on 2026-05-07 after Phase 6 because `## Phase History` exceeded 5 entries.
- Archived completed task detail covers T01-T27; active completed task list keeps Phase 6/7 onward pilot workflow context.
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

## Archive - Phase History

- Phase 1 Foundation complete: T01-T03 delivered package skeleton, CI contract, and baseline smoke tests. Baseline moved from 6 to 9 passing tests. Deep review Cycle 1 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 2 Input Contracts complete: T04-T07 delivered canonical trade records, CSV import normalization, risk policy schema, and policy review packets. Baseline moved from 9 to 21 passing tests. Deep review Cycle 2 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 3 Rule Evaluation complete: T08-T12 delivered session aggregation, deterministic evaluators, violation determinism, and reconciled P&L attribution with golden evidence. Baseline moved from 21 to 37 passing tests. Deep review Cycle 3 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 4 Reporting and Artifacts complete: T13-T16 delivered deterministic report data, Markdown output, claim guard validation, and reproducible artifact manifests. Baseline moved from 37 to 49 passing tests. Deep review Cycle 4 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 5 Concierge Pilot Workflow complete: T17-T20 delivered end-to-end local audit CLI, Telegram-ready copy packet, retention/delete controls, and anonymized pilot regression fixtures. Baseline moved from 49 to 61 passing tests. Deep review Cycle 5 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 6 Pilot Validation and Telegram Intake complete: T21-T29 delivered synthetic demo artifacts, pilot intake/workspace conventions, ADR-001, constrained Telegram intake/delivery, operator queue, mocked pilot flow, and business evidence log. Baseline moved from 61 to 88 passing tests. Deep review Cycle 7 found P0:0, P1:0, P2:0; Stop-Ship: No.
- Phase 7 Internal Validation with Public Samples complete: T30-T32 delivered source policy, starter profile boundaries, `demo/public_sample_001/`, public sample evidence docs, and a go decision for manual outreach. Baseline moved from 92 to 105 passing tests. Deep review Cycle 8 found P0:0, P1:0, P2:1; Stop-Ship: No.

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
