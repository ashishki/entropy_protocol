# Agent Notes - Trader Risk Audit

Date: 2026-05-15

This file keeps only restart-relevant notes. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/archive/`,
and `docs/tasks.md`.

## Active State

- Phase: 23 Open-Source Audit Case Bank
- Last completed: T93 CSV Friction Decision Gate
- Active task: T98 Open-Source Source Selection Protocol
- Baseline: 253 pass / 0 skip
- Primary roadmap: `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`

## Current Decision

The next priority is building a larger open-source/public/synthetic audit case
bank before approaching warm prospects. Validation success means truthful,
reproducible reports with preserved limitations, not only positive findings.

## Operator Input Needed

- complete T98-T103 before adding private pilot work;
- collect future privacy-safe market evidence outside git before reopening T94;
- preserve the distinction between demo artifact quality and paid/customer
  validation evidence;
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
- `docs/AUTOMATED_PILOT_ROADMAP.md`
- `docs/ARTIFACT_VALIDATION_ROADMAP.md`
- `docs/STARTER_POLICY_PROFILES_RU.md`
