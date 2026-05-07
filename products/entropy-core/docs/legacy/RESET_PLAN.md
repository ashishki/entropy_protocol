# Governance Reset Plan - Entropy Core

Version: 1.0
Date: 2026-05-07
Status: executed by bootstrap-new governance reset

## Intent

Rebuild the AI Workflow Playbook loop for Entropy Core over the existing codebase. This is not a source-code reset. It replaces active workflow state and prompts while preserving code, tests, migrations, canonical protocol docs, governance docs, and historical evidence.

## Preserved As Active Inputs

- `src/entropy/`
- `tests/`
- `migrations/`
- `pyproject.toml`
- `docs/core/`
- `docs/governance/`
- `templates/PROJECT_BRIEF.md`
- `docs/PROJECT_BRIEF.md`
- `docs/archive/`
- `docs/audit/archive/`

## Archived From Active Context

- previous `docs/CODEX_PROMPT.md`
- previous `docs/tasks.md`
- previous top-level audit outputs and old prompt variants
- previous compact decision/evidence/journal files
- previous `docs/prompts/*`

Archived files live under `docs/legacy/old-workflow/2026-05-07/`.

## New Active Authority

- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/tasks.md`
- `docs/CODEX_PROMPT.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/audit/`
- `docs/prompts/`

## Reset Rules

- Do not delete old evidence.
- Do not treat old workflow state as authority.
- Read legacy files only through task `Context-Refs`.
- First implementation task after reset establishes the true local baseline from the existing codebase.
