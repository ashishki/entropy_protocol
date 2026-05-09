# Audit-Grade Automation Roadmap

Date: 2026-05-08
Status: directional development roadmap
Scope: public signal-source due diligence pipeline

## Product Direction

The target product is not a fully autonomous trading-signal bot. The target is
an audit-grade pipeline for public signal-source due diligence:

```text
public source
  -> evidence capture
  -> machine-first draft extraction
  -> deterministic validators
  -> author-specific parser profile
  -> exception review
  -> approved ledger
  -> deterministic price matching
  -> customer-facing audit report
```

The intended end state automates most repetitive work while preserving an audit
trail for every customer-facing claim. LLM output may generate drafts,
pseudo-labels, lexicon candidates, summaries, and review queues. It must not be
the final source of truth for approved records or reported performance metrics.

## Non-Negotiable Boundaries

Allowed:

- public-source capture with evidence URL, source timestamp, capture timestamp,
  raw text, and text hash;
- frontier-model draft extraction over local public captures;
- deterministic validation of every extracted field;
- author-specific parser profiles derived from evidence-backed drafts;
- human exception review for high-value, ambiguous, low-confidence, or sampled
  rows;
- private audit reports with methodology, exclusions, and disclaimers.

Forbidden until a separate decision explicitly changes scope:

- private/authenticated scraping;
- login-walled or paywalled source capture;
- OCR as a default ingestion path;
- public leaderboard;
- marketplace;
- copy trading;
- broker/exchange execution;
- investment advice;
- auto-approved LLM extraction;
- Entropy Core signal feed contamination.

## Phase A - Data Foundation

Goal: make public-source evidence capture reproducible and legally bounded.

Current status: mostly implemented for the first Telegram source.

Inputs:

- source manifest;
- public source URL;
- legal/source eligibility memo;
- operator capture request.

Build:

- source manifest validation;
- public/private URL rejection;
- captured post schema;
- raw-text hash validation;
- deterministic capture ordering;
- capture manifest.

Artifacts:

- `workspace/captures/<source_id>/*.json`
- `docs/pilot/<source_id>_CAPTURE_MANIFEST.json`
- `docs/pilot/CAPTURE_LOG.md`

Exit criteria:

- every capture has source URL, evidence URL, source timestamp when available,
  capture timestamp, raw text, and text hash;
- capture loader returns a deterministic batch;
- no private or login-walled evidence enters the workspace.

Stop conditions:

- source is private, paywalled, login-walled, or ToS-disallowed;
- useful signals are only available through screenshots/OCR and no separate OCR
  decision exists.

## Phase B - Machine-First Pseudo-Label Bootstrap

Goal: avoid manual seed labeling by letting a frontier model produce structured
draft labels for every captured post.

Inputs:

- local public captures;
- methodology document;
- source boundary rules;
- extraction schema.

Build:

- offline prompt/runbook for pseudo-label generation;
- structured pseudo-label artifact;
- evidence-span requirements;
- confidence and uncertainty fields;
- per-row status suggestions.

Expected output per post:

- `capture_id`;
- `suggested_status`;
- `asset_candidates`;
- `direction_candidate`;
- `entry_candidate`;
- `stop_candidate`;
- `target_candidate`;
- `missing_fields`;
- `evidence_spans`;
- `confidence`;
- `uncertainty_reason`;
- `lexicon_terms_found`;
- `draft_only=true`.

Artifacts:

- `docs/pilot/bablos79_PSEUDO_LABELS.md`
- `workspace/extraction/bablos79_pseudo_labels.jsonl`

Exit criteria:

- every captured post has one pseudo-label row;
- every extracted field cites an evidence span;
- low-confidence and contradictory rows are marked for review;
- no pseudo-label is written to the approved ledger.

Stop conditions:

- model routinely invents fields not present in text;
- evidence spans cannot be verified against raw captures;
- most rows are low confidence, making the automation non-useful.

## Phase C - Deterministic Validation Layer

Goal: turn model output into a constrained, checkable draft artifact.

Inputs:

- pseudo-label JSONL;
- raw captures;
- signal record schema;
- source methodology.

Build:

- evidence-span verifier;
- numeric field verifier;
- ticker/asset format verifier;
- direction/intent consistency checks;
- missing-field detector;
- contradiction detector;
- confidence-gate rules.

Artifacts:

- `src/signal_sandbox/extraction/draft_validation.py`
- `tests/unit/test_draft_validation.py`
- `docs/pilot/bablos79_VALIDATION_SUMMARY.md`

Exit criteria:

- every pseudo-label is classified as `validated_draft`, `needs_review`,
  `rejected_draft`, or `not_a_signal`;
- validators reject hallucinated spans and numbers;
- validators are deterministic and have no network or LLM dependency.

Stop conditions:

- validation rejects most model outputs;
- valid trade signals cannot be distinguished from commentary without
  unacceptable false positives.

## Phase D - Author-Specific Parser Profile

Goal: capture the author's recurring language patterns so future drafts can be
classified reproducibly without LLM runtime calls.

Inputs:

- validated pseudo-labels;
- raw captures;
- lexicon terms found by the model;
- validator decisions.

Build:

- author-specific lexicon draft;
- parser profile schema;
- accepted-for-draft / excluded / needs-review term states;
- static parser profile loader;
- versioned parser-profile hash.

Artifacts:

- `workspace/lexicons/bablos79_lexicon_draft.json`
- `docs/pilot/bablos79_AUTHOR_PROFILE.md`
- `src/signal_sandbox/extraction/parser_profile.py`
- `tests/unit/test_parser_profile.py`

Exit criteria:

- repeated terms have evidence capture IDs;
- high-risk terms are excluded or marked `needs_review`;
- parser profile is deterministic and hashable;
- runtime parser does not call an LLM.

Stop conditions:

- author language is too inconsistent for a reusable profile;
- the profile cannot improve triage beyond raw pseudo-labels.

## Phase E - Human Exception Review

Goal: replace full manual labeling with targeted review of only the rows that
matter for audit quality.

Inputs:

- validated drafts;
- parser profile output;
- confidence scores;
- report-value heuristics.

Build:

- review queue artifact;
- sampling policy for `not_a_signal`;
- high-value candidate selection;
- ambiguous and low-confidence routing;
- reviewer decision fields.

Artifacts:

- `docs/pilot/bablos79_REVIEW_QUEUE.md`
- `docs/pilot/EXTRACTION_LOG.md`

Rows requiring review:

- `review_candidate`;
- `needs_review`;
- low-confidence rows;
- rows with conflicting model/validator/parser outputs;
- random sample from `not_a_signal`;
- any row used in customer-facing claims.

Exit criteria:

- important rows have reviewer status;
- sampled non-signal rows are checked for false negatives;
- no customer-facing metric uses unreviewed extracted signals.

Stop conditions:

- review queue remains almost as large as the full capture set;
- reviewers cannot resolve ambiguity from public evidence alone.

## Phase F - Approved Ledger

Goal: create audit-grade signal records only after the draft and review gates
have enough evidence.

Inputs:

- reviewed extraction log;
- validated drafts;
- raw capture evidence;
- methodology rules.

Build:

- draft-to-signal-record conversion;
- reviewer/provenance enforcement;
- approved/excluded/deferred status semantics;
- ledger write integration;
- audit checks for unreviewed records.

Artifacts:

- `workspace/ledger/<source_id>.parquet`
- `docs/pilot/<source_id>_APPROVED_LEDGER_SUMMARY.md`

Exit criteria:

- every approved record has evidence URL, source timestamp, text hash, reviewer
  ID, and extraction provenance;
- excluded/deferred rows have reasons;
- no LLM-sourced row is approved without review provenance.

Stop conditions:

- too few approved/evaluable rows exist for a meaningful report;
- required entry/stop/target fields are absent from public evidence.

## Phase G - Price Matching And Outcomes

Goal: evaluate approved records against deterministic market data snapshots.

Inputs:

- approved ledger;
- price provider selection;
- outcome rule registry;
- report window.

Build:

- snapshot acquisition or operator-file import;
- immutable snapshot persistence;
- target/stop/timeout matching;
- excluded-row accounting;
- deterministic aggregation.

Artifacts:

- `workspace/snapshots/<snapshot_id>/`
- `workspace/outcomes/<source_id>.parquet`
- `docs/pilot/<source_id>_OUTCOME_SUMMARY.md`

Exit criteria:

- every evaluated record cites snapshot provenance;
- outcomes are reproducible from ledger and snapshots;
- excluded rows are visible and counted separately.

Stop conditions:

- price data cannot cover the source's assets/timeframe;
- signals are not evaluable under the published methodology.

## Phase H - Customer Report V1

Goal: ship a private audit report that a potential customer can judge and pay
for.

Inputs:

- approved ledger;
- outcomes;
- aggregation summary;
- methodology;
- exclusions and limitations.

Build:

- source-level audit report;
- evidence table;
- evaluated signal table;
- excluded/ambiguous section;
- methodology and disclaimer block;
- customer feedback log.

Artifacts:

- `docs/pilot/reports/<source_id>_REPORT_V1.md`
- `docs/pilot/CUSTOMER_FEEDBACK.md`
- `docs/pilot/PAYMENT_SIGNAL_LOG.md`

Exit criteria:

- report is useful enough for a customer conversation;
- customer objections are recorded;
- payment or refusal signal is captured.

Stop conditions:

- customers do not care about the report;
- customers only want capabilities outside the legal/product boundary.

## Phase I - Multi-Source Pilot

Goal: prove the workflow generalizes beyond one author.

Inputs:

- three to five customer-provided public sources;
- Phase B-H workflow;
- source-specific parser profiles.

Build:

- repeatable source onboarding checklist;
- per-source capture, draft extraction, review, ledger, and report artifacts;
- cross-source bottleneck comparison;
- source parseability scoring.

Artifacts:

- `docs/pilot/<source_id>/` or equivalent source-specific artifacts;
- `docs/pilot/MULTI_SOURCE_PILOT_SUMMARY.md`

Exit criteria:

- at least two sources produce useful reviewed reports;
- parseability and review workload are measured per source;
- customer/payment evidence justifies productization.

Stop conditions:

- only one source is parseable;
- review cost is too high relative to willingness to pay.

## Phase J - Operator Productization

Goal: turn the pilot workflow into a repeatable internal tool.

Inputs:

- validated multi-source workflow;
- known bottlenecks;
- repeated report templates.

Build:

- source queue;
- CLI commands for draft generation, validation, review export, ledger build,
  outcome matching, and report rendering;
- standardized artifact layout;
- runbook;
- regression fixtures from reviewed sources.

Artifacts:

- CLI workflow commands;
- `docs/operator/RUNBOOK.md`;
- source queue artifacts.

Exit criteria:

- operator can run a source end-to-end with documented commands;
- repeated work is automated;
- failures produce actionable artifacts, not silent partial outputs.

Stop conditions:

- customer validation remains weak;
- workflow still depends on ad hoc manual file edits for core steps.

## Phase K - Telegram Delivery

Goal: deliver reports where customers already are without making Telegram the
core extraction engine.

Inputs:

- private report workflow;
- customer Telegram delivery preference;
- operator productized pipeline.

Build:

- manual or semi-automated Telegram report delivery;
- request intake format;
- status messages;
- payment/feedback capture.

Artifacts:

- delivery checklist;
- Telegram message templates;
- feedback/payment logs.

Exit criteria:

- Telegram improves distribution or response rate;
- delivery does not require private scraping or bot-first architecture.

Stop conditions:

- users primarily request private/paywalled channels;
- support and abuse risks exceed paid demand.

## Phase L - Semi-Self-Serve Audit Product

Goal: let users submit public sources while preserving review and evidence
gates.

Inputs:

- productized operator workflow;
- validated delivery channel;
- payment signal.

Build:

- public-source intake;
- job status tracking;
- automated capture/draft/validation/report draft;
- review UI or internal frontend;
- payment-gated report delivery.

Artifacts:

- source submission flow;
- internal review surface;
- generated draft reports;
- billing/payment records.

Exit criteria:

- most jobs reach draft report without operator intervention;
- final review remains fast and focused;
- customers pay for completed reports.

Stop conditions:

- self-serve requests are mostly ineligible sources;
- review burden remains too large for unit economics.

## Phase M - Confidence-Gated Automation

Goal: approach the ideal system: high-confidence sources become mostly
automated, while risky cases stay review-gated.

Inputs:

- reviewed historical decisions;
- parser profiles;
- validation metrics;
- customer report outcomes.

Build:

- source parseability score;
- confidence-gated report generation;
- drift detection for author language changes;
- regression suite from reviewed cases;
- review sampling policy;
- trust score for evidence quality.

Artifacts:

- confidence policy;
- parser profile registry;
- source parseability dashboard;
- automation evaluation reports.

Exit criteria:

- high-confidence sources need only exception review;
- false-positive/false-negative rates are measured;
- customer-facing claims remain backed by evidence and deterministic outcomes.

Stop conditions:

- automation causes unbounded false positives;
- source language drifts faster than profiles can adapt;
- customers value speed more than audit reliability, forcing a product
  positioning decision.

## Current Next Loop

The next development loop should start with Phase B, not manual seed labeling:

1. Generate pseudo-labels for all 60 `bablos79` captures.
2. Verify evidence spans and hallucination risk.
3. Extract author lexicon candidates from pseudo-labels.
4. Build deterministic validators.
5. Produce a review queue instead of asking a human to label every row.

The first manual gate moves from "label 10-15 seed rows before coding" to
"review only the exception queue and any row that will support a customer-facing
claim."
