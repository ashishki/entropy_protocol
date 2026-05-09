# ADR-002: Author Market Intelligence Architecture

Date: 2026-05-09
Status: accepted

## Context

Signal Analytics Sandbox is expanding from strict signal-source auditing to
Author Market Intelligence. The new product direction is documented in
`docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`: evaluate public market
authors across explicit trade setups, softer directional theses, market-regime
commentary, watchlists, risk warnings, and news/catalyst reactions.

Phase 10 is preserved as the first channel/profile seed, not replaced. The
initial corpus and profile inputs are:

- `workspace/captures/bablos79/`
- `docs/pilot/bablos79_AUTHOR_PROFILE.md`
- `workspace/lexicons/bablos79_lexicon_draft.json`
- `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`
- `docs/pilot/bablos79_REVIEW_QUEUE.md`
- `docs/pilot/AUTO_EXTRACTION_EVAL.md`

## Decision

Author Market Intelligence is approved as a local-first extension of the
existing sandbox. The product remains a deterministic audit system with optional
LLM-assisted draft/context layers. RAG and bounded agentic batch analysis are
now in scope, but only within the boundaries below.

## Scope

In scope:

- Normalize captured public posts into stable source-corpus documents.
- Store author/channel profiles as evidence-cited, reviewable artifacts.
- Add local retrieval over source documents, author profiles, asset aliases,
  and prior extracted ideas.
- Extract `MarketIdea` drafts covering trade setups, directional theses,
  market-regime commentary, watchlists, catalyst reactions, risk warnings, and
  non-market content.
- Evaluate approved ideas against deterministic market data and fixed horizon
  metrics.
- Run bounded internal batch analysis that retrieves cited context, reads
  deterministic metrics, drafts an analyst memo, and stops with an audit log.

## Non-Goals

Out of scope:

- Private Telegram scraping, login-walled sources, paywalled sources, or source
  collection outside `docs/legal_risk_memo.md`.
- Trading bot, copy trading, broker integration, autonomous execution, or
  investment-advice workflow.
- Public leaderboard, SaaS expansion, or autonomous publication before a later
  product/customer gate.
- LLM-derived prices, returns, approved records, outcome metrics, or final
  performance claims.
- Vector storage, embeddings, market-data expansion, or batch-agent code inside
  this ADR task.

## Runtime Tier

Runtime remains **T0**.

The first implementation stays a local Python library and CLI using local files
plus embedded local database files where needed. No long-lived worker, shell
mutation, privileged action, hosted service, container requirement, or runtime
package installation is introduced by this decision.

Future hosted service, autonomous collector, persistent worker, or privileged
tool execution requires a new ADR and runtime-tier review.

## Capability-Profile Changes

| Profile | Status | Declared in Phase | Boundary |
|---------|--------|-------------------|----------|
| RAG | ON | 11 | Local, cited, context-only retrieval. Implementation starts no earlier than Phase 14. |
| Tool-Use | OFF | 1 | No LLM-directed external tool calls are approved. Deterministic retrieval/evaluation functions may exist as application code. |
| Agentic | ON | 11 | Bounded internal batch analyst only. Implementation starts no earlier than Phase 17 and must have fixed iteration/tool/stop limits. |
| Planning | OFF | 1 | No plan-as-deliverable or plan graph is approved. Batch job contracts are workflow configuration, not a planning subsystem. |
| Compliance | OFF | 1 | No named compliance framework is activated. Public-source, ToS, retention, and non-advice rules remain project-specific controls. |

## RAG Storage Choice

The first retrieval substrate will be **local DuckDB plus local vector/index
sidecar files** under the operator workspace.

Rationale:

- Keeps T0 local-first operation.
- Avoids a PostgreSQL/pgvector service dependency before customer evidence
  justifies operational overhead.
- Supports deterministic metadata tables, source-document joins, and future
  index rebuild checksums.
- Leaves room to swap the vector sidecar implementation after the Phase 14
  prototype without changing the source-corpus or citation contract.

Storage rules:

- Every indexed document keeps source document ID, capture ID, evidence URL,
  timestamp, content hash, profile version, embedding model/provider/version,
  index schema version, and index build checksum.
- Retrieval results must cite source document IDs and evidence hashes.
- Retrieval output is context-only and must never mutate approved ledgers,
  price snapshots, deterministic market data, approved `MarketIdea` records, or
  outcome metrics.

## Deterministic-Truth Boundary

RAG and LLM outputs may provide context, draft fields, evidence candidates, and
analyst-summary language only. They cannot produce final prices, returns,
approved records, outcome metrics, scorecards, or customer-facing performance
claims.

The deterministic sources of truth remain:

- source/capture hashes for evidence identity;
- human approval state for final records;
- local market-data snapshots for prices;
- deterministic horizon metric code for returns and outcome labels;
- deterministic report templates for final metric rendering.

## Batch-Agent Boundaries

The Phase 17 batch analyst is approved only as a bounded internal workflow:

- Max iterations must be explicit per batch job.
- Allowed operations must be a fixed set: retrieve cited context, read
  deterministic market/metric artifacts, draft an internal memo, and stop.
- Shell commands, package installation, source collection, ledger approval,
  price mutation, report publication, broker actions, and external posting are
  forbidden.
- Every run must emit an audit log with inputs, retrieval citations, metric
  artifact IDs, prompt/version identifiers, iteration count, stop reason, and
  output path.
- The output is an internal analyst memo until a human approves any
  customer-facing report.

## Rollback Plan

Rollback is document and data compatible:

- Set RAG and Agentic profiles back to OFF in `docs/ARCHITECTURE.md`.
- Do not run Phase 14 or Phase 17 implementation tasks.
- Preserve Phase 10 artifacts and any already-created source corpus documents
  as normal local evidence files.
- Delete or ignore local retrieval index sidecars; approved ledgers, snapshots,
  outcomes, and reports remain valid because retrieval never owns deterministic
  truth.
- If the batch analyst proves too costly or hard to audit, keep deterministic
  corpus/metric/report tasks and revert analyst summaries to manual notes.

## Consequences

Positive:

- Future RAG and batch-analysis work has explicit governance before code lands.
- Phase 10 artifacts continue to compound as the first author profile/corpus
  seed.
- Deterministic market data and outcome metrics stay protected from LLM/RAG
  drift.

Tradeoffs:

- RAG activation adds evaluation and citation-discipline requirements at Phase
  14.
- Agentic activation raises review burden at Phase 17 because termination,
  audit logs, and tool boundaries must be tested.
- DuckDB plus vector sidecars may later be replaced if multi-operator or hosted
  usage becomes real.

## Acceptance Notes

This ADR satisfies `SAS-MI-001` by deciding scope, non-goals, runtime tier,
capability-profile changes, first RAG storage choice, batch-agent boundaries,
deterministic-truth boundaries, and rollback.
