# Agent Notes - Signal Analytics Sandbox

Date: 2026-05-15

This file keeps only restart-relevant notes. Detailed phase history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Active State

- Phase: 22 Expanded Public Corpus
- Active task: SAS-DR-001 Deep Retrospective Scope Lock
- Baseline: 166 pass / 0 skip
- Primary roadmap: `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`

## Current Decision

Warm demand/pre-order interest exists. Phase 21 produced a real internal
LLM-reviewed media-backed result, but the source/window was too narrow for
external delivery. The next route expands the public corpus, adds image/OCR,
builds a reviewed claim ledger, and compares measurable claims to public market
data.

## Locked Scope

- Source/channel: `https://t.me/bablos79`
- Period: existing public text capture window from 2026-04-27 through 2026-05-06.
- Capture method: public/operator unauthenticated Telegram `/s/` HTML captures.
- Report type: bounded public-source author/source research report.
- Language: Russian-first pilot report.
- Media scope: now required for the next loop because the text-only report has
  0 customer-report-eligible metric rows.

Capture pack: `docs/pilot/bablos79_CAPTURE_PACK.md` and
`docs/pilot/bablos79_CAPTURE_PACK.json`.

Review queue closure: `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.md` and
`docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.json`.

Outcome prep: `docs/pilot/bablos79_OUTCOME_PREP.md` and
`docs/pilot/bablos79_OUTCOME_PREP.json`.

Report draft: `docs/pilot/reports/bablos79_SIGNAL_REPORT_V1.md`.

Multimodal plan: `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md`.

Real media intake: `docs/pilot/bablos79_REAL_MEDIA_INTAKE.md`.

Current result: `SAS-LIVE-002..SAS-AF-008` completed and Phase 21 is archived.
Two public voice files were acquired, but no transcript provider was configured,
zero reviewed usable media refs exist, and the ready gate rejects this
source/window for external delivery.

Next task: run `SAS-DR-001` and create `docs/pilot/bablos79_DEEP_SCOPE.md`.

## Guardrails

- Public/operator-authorized sources only.
- Media evidence remains draft/internal until human-reviewed.
- No marketplace, leaderboard, advice, future-profit claims, private scraping,
  or paid X/Twitter dependency.
- Core is paused.
- Keep weak/counterexamples and non-measurable claims; do not produce a
  promotional channel-ranking report.

## Key Links

- `docs/CODEX_PROMPT.md`
- `docs/tasks.md`
- `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
- `docs/pilot/MEDIA_MODALITY_DECISION.md`
- `docs/archive/PHASE21_REVIEW.md`
