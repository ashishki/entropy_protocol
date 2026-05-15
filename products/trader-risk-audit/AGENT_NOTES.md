# Agent Notes - Trader Risk Audit

Date: 2026-05-11

This file keeps only restart-relevant notes. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/archive/`,
and `docs/tasks.md`.

## Active State

- Phase: 16 Artifact-First Real Audit Validation
- Active task: T63 Real Audit Scope Lock
- Baseline: 176 pass / 0 skip
- Primary roadmap: `docs/ARTIFACT_VALIDATION_ROADMAP.md`

## Current Decision

The next blocker is validating a real audit report artifact, not continuing
generic import feature expansion.

## Operator Input Needed

- first real trade source/export;
- audit period and timezone;
- policy/rules or selected starter profile;
- privacy/redaction boundary;
- report language and delivery format.

If this input is missing, record the blocker and stop.

## Guardrails

- Raw private/customer trade data must not be committed.
- T56-T62 are deferred unless required by the selected real audit artifact.
- ADR-002 remains read-only, local, and historical only.
- No live exchange control, order blocking, SaaS expansion, or trading advice.

## Key Links

- `docs/CODEX_PROMPT.md`
- `docs/tasks.md`
- `docs/ARTIFACT_VALIDATION_ROADMAP.md`
- `docs/STARTER_POLICY_PROFILES_RU.md`
