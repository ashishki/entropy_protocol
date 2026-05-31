# Entropy Protocol Portfolio Tasks

Status: active portfolio task graph
Last updated: 2026-05-31

This file coordinates cross-product work only. Implementation tasks still live
inside each product workspace.

## Active Decision

Entropy Protocol now has two durable lines:

1. Entropy Core as a reusable verification and responsibility kernel.
2. Telegram Trader Intelligence as an applied product line built primarily from
   Signal Analytics Sandbox work.

Trader Risk Audit remains a narrow product option, but it is no longer the only
commercial expression of the repository.

## Portfolio Tasks

### EP-001: Portfolio Reframe Sync

Status: complete
Owner: codex
Type: docs

Objective: |
  Align root README, product portfolio docs, and workspace READMEs around the
  current split: Core verification kernel, Telegram Trader Intelligence, Trader
  Risk Audit, and paused/deferred surfaces.

Acceptance-Criteria:
  - `README.md`, `docs/README.md`, and `docs/PRODUCT_PORTFOLIO.md` name the
    current product lines and active/deferred statuses.
  - Root docs link to workspace task graphs instead of implying one monolithic
    product.
  - Boundaries remain explicit: no live capital, no trading advice, no private
    scraping, no autonomous execution.

### EP-002: Telegram Trader Intelligence Productization Plan

Status: in_progress
Owner: codex
Type: product

Objective: |
  Turn Signal Analytics Sandbox from a retrospective research sandbox into a
  buyer-readable Telegram trader intelligence product while preserving evidence
  boundaries and no-advice language.

Acceptance-Criteria:
  - Signal workspace has a productization phase in its task graph.
  - Reports are framed as claim hygiene, narrative tracking, source behavior,
    and risk-signal analysis.
  - The product promise avoids prediction, leaderboard, investment advice, and
    "best trader" claims.

### EP-003: Core Verification Kernel V2 Candidate

Status: in_progress
Owner: codex
Type: architecture

Objective: |
  Define the next Core V2 candidate around portable evidence receipts,
  validator verdicts, and responsibility records that can support current and
  future AI-agent workflows.

Acceptance-Criteria:
  - Core workspace has a V2 candidate task block.
  - Candidate scope is schema/protocol first, not SaaS/runtime-first.
  - `entropy.artifacts.product_receipt` validates portable product proof
    receipts.
  - Product workspaces can consume receipts without Core owning their business
    logic.

### EP-004: Gensyn-Inspired Diversity And Referee Pattern

Status: in_progress
Owner: codex
Type: research

Objective: |
  Adapt the useful engineering lesson from Gensyn-style evolutionary inference:
  run diverse analytical candidates, preserve their evidence, and use a
  deterministic or human-reviewed referee to decide what survives.

Acceptance-Criteria:
  - The pattern is documented as optional validation structure, not as a
    distributed training dependency.
  - Signal analysis can emit candidate lenses and a referee verdict.
  - Workflow Playbook and Entropy Core can reuse the same receipt vocabulary.

### EP-005: Cross-Project Verification Integration

Status: in_progress
Owner: codex
Type: integration

Objective: |
  Define how Entropy Core receipts can be used by AI Workflow Playbook,
  Workflow-To-Agent Studio, Telegram Research Agent, and future products.

Acceptance-Criteria:
  - Integration notes identify artifact types, source-of-truth files, and
    minimum fields.
  - Active products have local proof receipt helpers and tests where the proof
    layer is immediately useful.
  - No project is forced to adopt Entropy Core as a runtime dependency.
  - The integration remains artifact-first: docs, receipts, CI checks, and
    review gates before runtime adapters.
