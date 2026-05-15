# CODEX_PROMPT.md

Version: 1.74
Date: 2026-05-15
Phase: Phase 23

This file is the compact session state for AI development. Do not paste long
history here; use links below.

## Current Phase

- Phase: Phase 23
- Name: Open-Source Audit Case Bank
- Business goal: build a larger bank of valid open-source/public/synthetic
  audit artifacts before warm prospect delivery.
- Phase gate: at least 5 candidate case packs exist with source notes,
  policies, reports, manifests, reviewed reports, validation notes, and
  preserved limitation/reject cases.

## Current State

- Baseline: 253 passing tests
- Ruff: clean (`ruff check` and `ruff format --check`)
- Last CI: workflow configured; remote run not observed from this clone
- Last updated: 2026-05-15
- Open findings: none
- Current priority: open-source case-bank validation, not SaaS expansion
- Last completed: T93 CSV Friction Decision Gate

## Read First

1. `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
2. `docs/tasks.md` Phase 23, T98-T103
3. `docs/AUTOMATED_PILOT_ROADMAP.md`
4. `docs/IMPLEMENTATION_CONTRACT.md`
5. `docs/PILOT_INTAKE_CONTRACT_RU.md`
6. task-specific `Context-Refs` in `docs/tasks.md`

Other useful links:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
- `docs/ARTIFACT_VALIDATION_ROADMAP.md` and Phase 16 artifacts for the
  completed SEC open-source validation baseline
- `docs/STARTER_POLICY_PROFILES_RU.md` for `soft`, `medium`, and `hard`
  starter audit presets

## Next Task

T98 Open-Source Source Selection Protocol

Immediate intent:

- do not implement real exchange network fetching;
- create `docs/OPEN_SOURCE_CASE_BANK.md`;
- define anti-cherry-pick source selection and case-pack criteria;
- keep open-source packs separate from paid/customer/PMF evidence.

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
- Core is paused; do not open Core tasks from this workspace.
- Open-source validation batches must include positive, limitation/reject, and
  edge-case examples where available.

## Historical Pointers

- Completed through T93; details are in `docs/IMPLEMENTATION_JOURNAL.md`,
  `docs/EVIDENCE_INDEX.md`, `docs/archive/`, and `docs/tasks.md`.
- T94-T97 remain blocked by T93 defer.
- Active planned work is T98-T115: open-source case bank, multi-case report
  quality loop, and private-pilot readiness.
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

## Maintenance Rule

At every phase boundary update only:

- current phase;
- baseline and validation status;
- next task;
- open findings;
- links if canonical docs move.

Do not append long task logs here.
