# Trader Risk Audit Artifact Validation Roadmap

Status: Complete
Date: 2026-05-14

This file gives strategic routing for the completed Phase 16 artifact
validation work. Detailed acceptance criteria and file scope live in
`docs/tasks.md` Phase 16, T63-T69.

## Goal

Produce one real-data or verified open-source trader audit report pack that the
operator personally trusts before showing it to warm prospects.

## Completed Phase

| Task | Purpose | Output |
|---|---|---|
| T63 | Lock real audit scope. | Source/rules/privacy/delivery scope note; current scope is `docs/REAL_AUDIT_SCOPE_OPEN_SOURCE_EN.md`. |
| T64 | Intake real data and map policy. | Normalized preview, unsupported-field register, policy review. |
| T65 | Generate first real audit artifacts. | Trades, violations, attribution, report, packet, manifest. |
| T66 | Manually validate calculations. | Validation notes and error register. |
| T67 | Polish report and claim safety. | Operator-trusted report and delivery packet. |
| T68 | Package internal demo. | Safe demo pack and talk track. |
| T69 | Decide external pilot readiness. | Ready/needs-fix/reject decision and paid pilot scope. |

## Required Artifacts

- real audit scope note or verified open-source validation scope note;
- intake/schema summary;
- policy mapping review;
- generated report pack;
- manual validation notes;
- error register;
- redacted demo pack when needed;
- external pilot ready-gate review.

Raw private/customer trade exports must stay outside git. Commit only sanitized
summaries, fixtures, or redacted derivatives.

If private operator data is unavailable, do not block Phase 16. Use a valid
public/open-source transaction dataset with source metadata, privacy review,
and clear limitation wording. Public/open-source validation proves artifact
quality only; it is not market validation or paid-pilot evidence.

## Completion And Next Routing

Phase 16 completed on 2026-05-12 with the SEC EDGAR Form 4 open-source
validation pack and Cycle 21 deep review. The ready gate allows controlled
warm-prospect conversations using the demo pack, but does not count as
customer, paid-pilot, or PMF evidence.

The current development loop has moved to `docs/AUTOMATED_PILOT_ROADMAP.md`.
Start with T70 Automated Intake Session Contract and keep the automation
local-first until evidence justifies hosted product work.

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
2. `docs/AUTOMATED_PILOT_ROADMAP.md`
3. this file for Phase 16 historical context
4. repo-root `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
5. `docs/tasks.md` T63-T69 and T70-T97
6. task-specific `Context-Refs`
