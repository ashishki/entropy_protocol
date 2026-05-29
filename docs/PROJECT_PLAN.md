# Entropy Protocol - Project Plan

Status: active infrastructure + active trader intelligence product line
Role: verification kernel and Telegram trader intelligence workspace
Priority: P0/P1

## Strategic Role

Entropy Protocol should split into two related lines:

1. **Entropy Core** - reusable verification and responsibility layer for AI
   decisions/actions.
2. **Telegram Trader Intelligence** - applied product for analyzing Telegram
   trader channels, narratives, claims, source behavior, and risk signals.

Core gives the evidence model. Trader Intelligence gives a concrete market-facing
use case.

## Product Lines

### Entropy Core

Purpose:
- action receipts
- decision receipts
- source/evidence chains
- referee verdicts
- risk acceptance records
- responsibility trace

Gensyn influence to adapt:
- REE-style receipts: model/config/input/output/evidence linkage.
- Verde-style referee verification: independent check of claimed inference.
- DEI-style diversity: multiple analytical lenses, not many identical agents.
- AXL-style specialist routing as a future reference, not current dependency.

### Telegram Trader Intelligence

Purpose:
- ingest Telegram trader channels
- extract trade claims and narratives
- track source behavior and reputation signals
- generate weekly risk/intelligence memos
- preserve citations and evidence receipts

This product should not promise market prediction. It should sell signal hygiene:
who is specific, who is noisy, which narratives repeat, where evidence is weak,
and what changed this week.

## Near-Term Roadmap

### P0 - Reframe Repository

- Update root README to show both lines clearly.
- Mark old grand-protocol ambition as paused.
- Make `products/trader-risk-audit/` or a new product workspace the home for
  Telegram Trader Intelligence.
- Add an `entropy-core` schema/reference section.

### P0 - Trader Intelligence MVP

- Define channel registry.
- Store raw posts with immutable evidence IDs.
- Extract claims:
  - asset
  - direction
  - timeframe
  - confidence
  - invalidation
  - rationale
  - quote
- Produce weekly memo with source citations.
- Track deleted/edited/reframed claims when data allows.

### P1 - Verification Receipts

- Add `signal_analysis_receipt`.
- Add `source_reputation_record`.
- Add `referee_verdict`.
- Add deterministic citation checks.
- Link each weekly memo to its evidence window.

### P1 - Diverse Analytical Lenses

- Add separate lenses:
  - momentum
  - risk
  - manipulation/scam
  - macro narrative
  - contrarian
  - evidence quality
- Compare agreement/disagreement across lenses in the memo.

### P2 - Cross-Project Integration

- Feed useful patterns into AI Workflow Playbook.
- Reuse Telegram Research Agent ingestion if practical.
- Reuse Demand Radar report quality/evidence patterns.

## AI-Development Tasks

- Use AI for extraction prompt drafts, schema proposals, report templates, and
  reviewer/referee prompts.
- Keep evidence extraction deterministic where possible.
- Require receipts for model-generated memos.
- Do not let AI generate trading advice without risk framing and evidence links.

## Stop Conditions

- Stop any feature that turns this into a trading bot.
- Stop broad protocol work unless it improves the trader intelligence product or
  reusable verification kernel.
