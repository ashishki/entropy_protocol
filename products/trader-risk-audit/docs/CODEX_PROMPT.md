# CODEX_PROMPT.md

Version: 1.73
Date: 2026-05-15
Phase: Phase 22

This file is the compact session state for AI development. Do not paste long
history here; use links below.

## Current Phase

- Phase: Phase 22
- Name: Conditional Real Read-Only Import
- Business goal: completed decision gate for whether CSV/export friction
  justifies real local read-only exchange fetching.
- Phase gate: T93 deferred real fetching; T94-T97 are blocked until future
  market evidence reopens the gate.

## Current State

- Baseline: 253 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
- Last updated: 2026-05-15
- Open findings: none
- Current priority: automated pilot validation loop, not SaaS expansion
- Last completed: T93 CSV Friction Decision Gate

## Read First

1. `docs/AUTOMATED_PILOT_ROADMAP.md`
2. `docs/tasks.md` Phase 22, T93-T97
3. `docs/IMPLEMENTATION_CONTRACT.md`
4. `docs/PILOT_INTAKE_CONTRACT_RU.md`
5. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/ARTIFACT_VALIDATION_ROADMAP.md` and Phase 16 artifacts for the
  completed SEC open-source validation baseline
- `docs/STARTER_POLICY_PROFILES_RU.md` for `soft`, `medium`, and `hard`
  starter audit presets

## Next Task

No active roadmap task

T94-T97 are blocked by the T93 defer decision. Use
`docs/CSV_FRICTION_DECISION_REPORT.md`,
`docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md`, and
`docs/adr/ADR-002-read-only-exchange-import.md` as source context if future
market evidence reopens the gate.

Immediate intent:

- do not implement real exchange network fetching;
- collect privacy-safe market evidence outside git;
- reopen T94 only if a future evidence export changes the T93 decision.

## Active Guardrails

- Phase 14/15 exchange-import work is complete but should run only when it
  directly supports the selected real audit artifact or the T93/T94 friction
  gate.
- Public/open-source artifact validation is allowed when private data is not
  supplied, but it is not paid pilot, PMF, or customer validation evidence.
- ADR-001 keeps Telegram as constrained demo/intake/delivery only.
- ADR-002 allows local read-only historical fill ingestion only.
- Phases 20-21 must stay local-first and deterministic: no SaaS accounts,
  hosted uploads, checkout, hosted storage, or background network import.
- No SaaS accounts, checkout, exchange write APIs, broker control, order
  blocking, signal analytics, AI advice, or live trading behavior.

## Historical Pointers

- Completed through T93; details are in `docs/IMPLEMENTATION_JOURNAL.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/archive/`, and `docs/tasks.md`.
- Planned through T97; Phase 19 continues the automated pilot loop.
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

## Maintenance Rule

At every phase boundary update only:

- current phase;
- baseline and validation status;
- next task;
- open findings;
- links if canonical docs move.

Do not append long task logs here.
