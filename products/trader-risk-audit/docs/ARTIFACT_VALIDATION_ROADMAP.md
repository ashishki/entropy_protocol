# Trader Risk Audit Artifact Validation Roadmap

Status: Active
Date: 2026-05-11

This file gives strategic routing only. Detailed acceptance criteria and file
scope live in `docs/tasks.md` Phase 16, T63-T69.

## Goal

Produce one real-data trader audit report pack that the operator personally
trusts before showing it to warm prospects.

## Active Phase

| Task | Purpose | Output |
|---|---|---|
| T63 | Lock real audit scope. | Source/rules/privacy/delivery scope note. |
| T64 | Intake real data and map policy. | Normalized preview, unsupported-field register, policy review. |
| T65 | Generate first real audit artifacts. | Trades, violations, attribution, report, packet, manifest. |
| T66 | Manually validate calculations. | Validation notes and error register. |
| T67 | Polish report and claim safety. | Operator-trusted report and delivery packet. |
| T68 | Package internal demo. | Safe demo pack and talk track. |
| T69 | Decide external pilot readiness. | Ready/needs-fix/reject decision and paid pilot scope. |

## Required Artifacts

- real audit scope note;
- intake/schema summary;
- policy mapping review;
- generated report pack;
- manual validation notes;
- error register;
- redacted demo pack when needed;
- external pilot ready-gate review.

Raw private/customer trade exports must stay outside git. Commit only sanitized
summaries, fixtures, or redacted derivatives.

## Allowed Engineering

- parser fixes proven by the real export;
- validation/error-message improvements;
- report readability improvements;
- manifest/reproducibility hardening;
- redaction/demo-pack helpers;
- minimum read-only exchange import work only if needed for this real artifact.

## Out Of Scope

- SaaS accounts/dashboard;
- checkout;
- live exchange control;
- order blocking;
- AI trading advice;
- strategy backtesting platform;
- broad connector expansion not needed by the active real audit.

## Read Order

1. `docs/CODEX_PROMPT.md`
2. this file
3. repo-root `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
4. `docs/tasks.md` T63-T69
5. task-specific `Context-Refs`
