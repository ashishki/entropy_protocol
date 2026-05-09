# ADR-003: Channel-Specific Tools Scope

Date: 2026-05-09
Status: accepted

## Context

Phase 18 produced an Author Market Report V0 template and a decision gate. The
decision was not to sell V0 yet. The report shape is useful, but evidence
coverage is too thin for a customer sale: the 60 public `bablos79` captures need
reviewed source-document coverage, cited MarketIdea rows, deterministic outcome
metrics, and customer feedback/payment evidence.

Phase 19 decides which channel-specific tool is justified by that bottleneck.
This ADR does not implement a provider, service, scraper, broker path, report
publisher, or hosted workflow.

## Decision

Choose **reviewer UI/export improvements** as the next tool category.

The first follow-up task is `SAS-MI-019: Reviewer Coverage Export Pack`. It
will create a deterministic local review/export artifact that maps each public
source document to MarketIdea draft/review status, evidence coverage,
deterministic metric/outcome status, missing fields, and the next reviewer
action.

## Candidate Tools

| Candidate | Measured channel/profile bottleneck | Expected user value | Cost/risk | Decision |
|-----------|-------------------------------------|---------------------|-----------|----------|
| Voice transcription | `bablos79` has voice-analysis behavior in profile notes, but the current local corpus is text captures; no audio files or customer request proves this is the blocker. | Could unlock voice-heavy channels later. | Adds provider/model cost, accuracy review burden, retention risk, and modality evidence complexity. | Defer. |
| OCR/image annotation | Current reviewed bottleneck is text evidence coverage, not image/screenshot extraction. | Could help screenshot-heavy sources later. | Adds OCR provider/model dependency and screenshot/retention legal review. | Defer. |
| News/catalyst linker | Market commentary may reference events, but no evaluated report failed because catalyst linking was missing. | Could improve explanation once evidence/outcomes exist. | Risk of uncited external claims and network/provider drift. | Defer. |
| Fund/equity data | Current asset universe already covers initial crypto/equity symbols enough for the first evidence pass. | Could widen multi-asset coverage later. | Adds market-data provider/licensing scope before demand evidence. | Defer. |
| Reviewer UI/export improvements | The exact Phase 18 bottleneck is reviewed coverage across 60 public text captures, cited MarketIdea rows, deterministic outcomes, and customer-ready sample evidence. | Helps the operator see which rows are ready, missing evidence, missing metrics, or unsafe for customer report reuse. | Low. Local deterministic export only; no provider, no service, no publication path. | Choose. |
| New channel lexicons | Current profile exists for `bablos79`; unknown-channel work is not the blocker for the first report sample. | Useful when a second channel enters review. | Risk of generic feature expansion before first report evidence coverage. | Defer. |

## Chosen Next Task

`SAS-MI-019: Reviewer Coverage Export Pack`

The task must be narrow and acceptance-tested:

- deterministic local export, sorted by source timestamp and document/capture
  ID;
- one row per source document;
- explicit status buckets for missing evidence, missing deterministic metrics,
  review-required interpretation, and ready-for-customer-sample rows;
- no approved ledger writes;
- no report publication;
- no provider dependency;
- no external service;
- no private scraping, broker integration, public leaderboard, marketplace, or
  forward-looking claims.

## Runtime And Capability Impact

Runtime remains **T0**.

Capability profile changes:

| Profile | Status after ADR | Reason |
|---------|------------------|--------|
| RAG | ON | Unchanged; context-only retrieval remains allowed but is not expanded by this ADR. |
| Tool-Use | OFF | No LLM-directed tool calls or provider tools are approved. |
| Agentic | ON | Unchanged; bounded internal analyst remains allowed, but the chosen next task is deterministic export work. |
| Planning | OFF | No plan-as-deliverable subsystem is introduced. |
| Compliance | OFF | No named compliance framework is activated. |

## Non-Goals

Out of scope:

- private Telegram scraping;
- authenticated scraping or scraping behind access controls;
- voice transcription provider implementation;
- OCR/image provider implementation;
- external news/catalyst API integration;
- paid market-data provider expansion;
- live trading or broker integration;
- copy trading;
- autonomous report publication;
- public leaderboard or marketplace expansion;
- investment advice or forward-looking claims.

## Rollback Plan

If the reviewer coverage export does not reduce review friction, delete or
ignore the generated artifact and continue manual review from existing
MarketIdea and capture files. No persistent provider state or external service
will exist to unwind.

## Acceptance Notes

This ADR satisfies `SAS-MI-018`: it lists candidate tools, ties each candidate
to the measured bottleneck, evaluates expected value and cost/risk, chooses one
next task, and adds no provider dependency or external service.
