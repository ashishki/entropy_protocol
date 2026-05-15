# Signal Analytics Sandbox Artifact Validation Roadmap

Status: Active Phase 21 routing
Date: 2026-05-11

This file gives strategic routing only. Detailed acceptance criteria and file
scope live in `docs/tasks.md` Phase 21, SAS-AF-001..008.

## Goal

Produce one real public-source research/report artifact, manually validate the
evidence, and decide whether it is ready for controlled external pilot use.

## Active Phase

| Task | Purpose | Output |
|---|---|---|
| SAS-AF-001 | Lock channel/source and report scope. | Source/report/legal/claim scope note. |
| SAS-AF-002 | Build public capture pack. | Source manifest, capture log, corpus preview. |
| SAS-AF-003 | Close human review queue. | Reviewed rows and ambiguity register. |
| SAS-AF-004 | Prepare market data/outcomes. | Asset mapping, snapshot refs, unresolved outcomes. |
| SAS-AF-005 | Generate first real source report. | Report, evidence appendix, limitations. |
| SAS-AF-006 | Manually validate evidence. | Validation notes and error register. |
| SAS-AF-007 | Polish report/demo pack. | Internal demo pack and talk track. |
| SAS-AF-008 | Decide external pilot readiness. | Ready/needs-fix/reject decision and paid pilot scope. |

## Required Artifacts

- source/report scope note;
- public source manifest;
- capture pack;
- reviewed extraction export;
- outcome-prep summary where supported;
- report artifact;
- manual validation notes;
- error register;
- external-safe demo excerpts;
- ready-gate review.

## Guardrails

- public/operator-authorized sources only;
- no private Telegram groups;
- no access-control bypass;
- no paid X/Twitter dependency before public-source artifact validation;
- no customer-facing media claims until transcript/OCR evidence is human-reviewed;
- no marketplace, leaderboard, or future-profit claim.

## Read Order

1. `docs/CODEX_PROMPT.md`
2. this file
3. repo-root `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` SAS-AF-001..008
5. task-specific `Context-Refs`
