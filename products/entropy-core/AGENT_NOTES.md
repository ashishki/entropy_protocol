# Agent Notes - Entropy Core

Date: 2026-05-11

This file keeps only restart-relevant notes. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/audit/`, and
`docs/tasks.md`.

## Active State

- Phase: 15 Artifact Support Mode
- Active task: T69 Shared Artifact Contract Freeze
- Baseline: 501 pass / 20 skip
- Primary roadmap: `docs/ARTIFACT_SUPPORT_ROADMAP.md`

## Current Decision

Core is internal artifact-support infrastructure for Trader Risk Audit and
Signal Analytics Sandbox. It should not become a public SDK, hosted service, or
platform surface in this cycle.

## Deferred

- T66-T68 local replay continuation;
- live/broker/exchange execution;
- holdout/OOS expansion;
- public Core productization.

## Guardrails

- Holdout remains locked.
- Live capital and broker/exchange execution are not approved.
- Production credentials are not approved.
- OOS/performance claims are not approved.

## Key Links

- `docs/CODEX_PROMPT.md`
- `docs/tasks.md`
- `docs/ARTIFACT_SUPPORT_ROADMAP.md`
- `../../docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
