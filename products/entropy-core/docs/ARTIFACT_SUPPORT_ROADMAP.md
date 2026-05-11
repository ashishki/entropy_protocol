# Entropy Core Artifact Support Roadmap

Status: Active
Date: 2026-05-11

This file gives strategic routing only. Detailed acceptance criteria and file
scope live in `docs/tasks.md` Phase 15, T69-T74.

## Goal

Keep Core as internal artifact-validity infrastructure for Trader Risk Audit and
Signal Analytics Sandbox. Core is not the public product in this cycle.

## Active Phase

| Task | Purpose | Output |
|---|---|---|
| T69 | Freeze shared artifact contract. | Minimal report artifact contract. |
| T70 | Define report validity checklist. | Internal/external readiness checklist. |
| T71 | Define reproducibility checklist. | Rerun/hash/nondeterminism guidance. |
| T72 | Document product bridge support. | Trader/Signal bridge notes. |
| T73 | Add review packet templates. | Scope, validation, error, delivery templates. |
| T74 | Review platformization gate. | Stay-internal / SDK / defer decision. |

## Core Should Provide

- artifact contract;
- no-claim boundary;
- reproducibility guidance;
- manual validation checklist;
- narrow product bridge notes;
- small shared templates where useful.

## Core Must Not Do Now

- public SDK;
- hosted service;
- live broker/exchange execution;
- live capital path;
- holdout/OOS expansion;
- generic agent framework;
- Core-driven rewrite of product report logic.

## Read Order

1. `docs/CODEX_PROMPT.md`
2. this file
3. repo-root `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` T69-T74
5. task-specific `Context-Refs`
