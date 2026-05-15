# Entropy Core Artifact Support Roadmap

Status: Complete
Date: 2026-05-12

This file gives strategic routing only. Detailed acceptance criteria and file
scope live in `docs/tasks.md` Phase 15, T69-T74.

## Goal

Keep Core as internal artifact-validity infrastructure for Trader Risk Audit and
Signal Analytics Sandbox. Core is not the public product in this cycle.

## Phase 15 Outputs

| Task | Purpose | Output |
|---|---|---|
| T69 | Freeze shared artifact contract. | Minimal report artifact contract: `docs/core/ARTIFACT_CONTRACT.md`. |
| T70 | Define report validity checklist. | Internal/external readiness checklist: `docs/core/REPORT_VALIDITY_CHECKLIST.md`. |
| T71 | Define reproducibility checklist. | Rerun/hash/nondeterminism guidance: `docs/core/REPRODUCIBILITY_CHECKLIST.md`. |
| T72 | Document product bridge support. | Trader/Signal bridge notes: `docs/core/PRODUCT_ARTIFACT_BRIDGES.md`. |
| T73 | Add review packet templates. | Scope, validation, error, delivery templates in `docs/templates/`. |
| T74 | Review platformization gate. | Stay internal: `docs/audit/ARTIFACT_SUPPORT_REVIEW.md`. |

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
