# Implementation Journal — Signal Analytics Sandbox

Version: 1.0
Last updated: 2026-05-15
Status: append-only

This file is durable handoff context across agents and sessions. It records what changed, why, what evidence was collected, and what remains open. It is a retrieval surface, not authority.

---

## Journal Entry Template

```markdown
### YYYY-MM-DD — SESSION_OR_TASK_ID — SHORT_TITLE

- Scope: files / directories / task IDs
- Why this work happened: reason or trigger
- Decisions applied: Decision Log / ADR refs or "none"
- Evidence collected: tests / evals / review reports / manual checks
- Follow-ups: next task, open risk, or "none"
- Notes for next agent: only the context worth carrying forward
```

---

## Entries

### 2026-05-19 — SAS-NEXT-032 — Cost And Time Instrumentation

- Scope: `src/signal_sandbox/runs/metrics.py`,
  `src/signal_sandbox/runs/__init__.py`,
  `tests/unit/test_run_cost_time_instrumentation.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 35 needs run-level operational instrumentation
  for durations, provider calls, cache hits, and estimated costs.
- Decisions applied: added strict step/run metric models, deterministic step
  ordering, aggregate totals, unknown-cost handling, and metrics hash.
- Evidence collected: targeted run metric tests pass. Full validation after
  state update: 295 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: all current `SAS-NEXT-001..032` tasks are complete; await
  operator review, external gate decision, pilot execution, or new roadmap
  scope.

### 2026-05-19 — SAS-NEXT-031 — Regression Suite For Known Channels

- Scope: `tests/unit/test_known_channel_regressions.py`, active state files,
  and `docs/tasks.md`.
- Why this work happened: Phase 35 needs golden checks to catch unexpected
  drift in known pilot-channel metrics and examples.
- Decisions applied: locked current V2 aggregate metrics and selected V1 kept
  claim IDs for `bablos79`, `nemphiscrypts`, and `pifagortrade`.
- Evidence collected: targeted regression tests pass. Full validation after
  state update: 293 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-032 Cost And Time Instrumentation`.

### 2026-05-19 — SAS-NEXT-030 — Retry And Provider Failure Handling

- Scope: `src/signal_sandbox/claims/provider_config.py`,
  `src/signal_sandbox/claims/__init__.py`,
  `tests/unit/test_provider_failure_handling.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 35 needs provider failures to avoid corrupting
  outcome metrics.
- Decisions applied: added retryable and terminal provider-failure fetch plan
  statuses with provider error metadata and no win/loss outcome semantics.
- Evidence collected: targeted provider failure/planning tests pass. Full
  validation after state update: 291 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-031 Regression Suite For Known Channels`.

### 2026-05-19 — SAS-NEXT-029 — Run Manifest And Caching

- Scope: `src/signal_sandbox/runs/`,
  `tests/unit/test_run_manifest_and_caching.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 35 needs deterministic report run manifests and
  compact cache references for reproducible report generation.
- Decisions applied: added strict manifest/ref models, stable sorting,
  canonical JSON hashing, and compact cache refs based on artifact SHA.
- Evidence collected: targeted run manifest tests pass. Full validation after
  state update: 289 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-030 Retry And Provider Failure Handling`.

### 2026-05-19 — SAS-NEXT-028 — Feedback Loop

- Scope: `docs/pilot/BUYER_FEEDBACK_LOG.md`,
  `tests/unit/test_buyer_feedback_log.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 34 needs a repeatable way to capture buyer
  feedback, objections, willingness to pay, and next actions.
- Decisions applied: added required feedback fields, objection/output
  categories, willingness-to-pay scale, next-action rules, and zero-real-demo
  current summary.
- Evidence collected: targeted feedback-log tests pass. Full validation after
  state update: 287 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-029 Run Manifest And Caching`.

### 2026-05-19 — SAS-NEXT-027 — Paid Pilot Offer

- Scope: `docs/pilot/PAID_PILOT_OFFER.md`,
  `tests/unit/test_paid_pilot_offer.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 34 needs a bounded paid-pilot hypothesis after
  buyer profiles and demo script.
- Decisions applied: offer defines scope, deliverables, price hypothesis,
  turnaround, buyer commitments, exclusions, success gate, kill criteria, and
  external boundary.
- Evidence collected: targeted paid-pilot tests pass. Full validation after
  state update: 285 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-028 Feedback Loop`.

### 2026-05-19 — SAS-NEXT-026 — Demo Script

- Scope: `docs/pilot/DEMO_SCRIPT.md`, `tests/unit/test_demo_script.py`, active
  state files, and `docs/tasks.md`.
- Why this work happened: Phase 34 needs a bounded discovery-call script before
  defining the paid pilot offer.
- Decisions applied: script keeps current artifacts internal-only, explains
  method/value/limitations, and avoids advice, future-profit, and external
  readiness claims.
- Evidence collected: targeted demo-script tests pass. Full validation after
  state update: 283 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-027 Paid Pilot Offer`.

### 2026-05-19 — SAS-NEXT-025 — Pilot Buyer List

- Scope: `docs/pilot/BUYER_DISCOVERY.md`,
  `tests/unit/test_buyer_discovery.py`, active state files, and `docs/tasks.md`.
- Why this work happened: Phase 34 needs concrete buyer profiles and pilot use
  cases before demo scripting and paid-pilot offer design.
- Decisions applied: defined 15 ICP/use-case hypotheses, disqualifiers,
  discovery questions, and pilot success criteria under the internal-only gate.
- Evidence collected: targeted buyer-discovery tests pass. Full validation
  after state update: 281 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-026 Demo Script`.

### 2026-05-19 — SAS-NEXT-024 — Customer-Safe Wording Library

- Scope: `src/signal_sandbox/reports/wording.py`,
  `src/signal_sandbox/reports/__init__.py`,
  `tests/unit/test_customer_safe_wording.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 33 needs centralized wording rules for safe
  report/customer surfaces.
- Decisions applied: added allowed context phrases and forbidden wording rules
  for advice, future-profit, leaderboard, marketplace, and overclaims.
- Evidence collected: targeted wording tests pass. Full validation after state
  update: 279 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-025 Pilot Buyer List`.

### 2026-05-19 — SAS-NEXT-023 — Buyer Demo Pack

- Scope: `docs/pilot/three_channel_BUYER_DEMO_PACK.md`,
  `tests/unit/test_buyer_demo_pack.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 33 needs an internal buyer-discovery pack that
  explains the product method without implying external approval.
- Decisions applied: pack is internal-only, includes artifacts/methodology/
  limitations/talk track/gate status, and blocks customer-facing use until gate
  approval.
- Evidence collected: targeted demo-pack tests pass. Full validation after
  state update: 277 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-024 Customer-Safe Wording Library`.

### 2026-05-19 — SAS-NEXT-022 — Evidence Appendix Generator

- Scope: `src/signal_sandbox/reports/evidence_appendix.py`,
  `src/signal_sandbox/reports/__init__.py`,
  `tests/unit/test_evidence_appendix_generator.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 33 needs report metrics to carry source,
  provider, snapshot, and review decision evidence.
- Decisions applied: added strict appendix models and Markdown renderer; rows
  without review decision IDs are rejected.
- Evidence collected: targeted appendix tests pass. Full validation after state
  update: 275 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-023 Buyer Demo Pack`.

### 2026-05-19 — SAS-NEXT-021 — Report Template System

- Scope: `src/signal_sandbox/reports/template.py`,
  `src/signal_sandbox/reports/__init__.py`,
  `tests/unit/test_report_template_system.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 33 needs one report data model that can render
  Markdown and HTML-ready output.
- Decisions applied: added strict `ReportTemplateData`/metric models, Markdown
  renderer, HTML-ready renderer, canonical disclaimer, and HTML escaping.
- Evidence collected: targeted template tests pass. Full validation after
  state update: 273 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-022 Evidence Appendix Generator`.

### 2026-05-19 — SAS-NEXT-020 — Multimodal Claim Recompute

- Scope: `docs/pilot/three_channel_V2_METRIC_RESULTS.json`,
  `tests/unit/test_multimodal_claim_recompute_v2.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 32 needs V2 metrics to include reviewed media
  claims when available and exclude unreviewed media.
- Decisions applied: no current media claim is human/operator accepted, so V2
  text metrics match V1; eight media rows are excluded with explicit reasons
  and a provenance schema defines future inclusion.
- Evidence collected: targeted recompute tests pass. Full validation after
  state update: 271 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-021 Report Template System`.

### 2026-05-19 — SAS-NEXT-019 — OCR And Chart Source-Link Policy

- Scope: `docs/specs/OCR_CHART_SOURCE_LINK_POLICY.md`,
  `tests/unit/test_ocr_chart_source_link_policy.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 32 needs OCR/chart evidence rules before
  multimodal recompute can include any media-derived claim.
- Decisions applied: OCR can produce draft visible text only; chart meaning and
  market claims require source linkage, checksums, human/operator review, and
  accepted claim boundaries.
- Evidence collected: targeted policy tests pass. Full validation after state
  update: 269 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-020 Multimodal Claim Recompute`.

### 2026-05-19 — SAS-NEXT-018 — Transcript Human Review Workflow

- Scope: `docs/pilot/three_channel_TRANSCRIPT_REVIEW.md`,
  `tests/unit/test_transcript_human_review_workflow.py`, active state files,
  and `docs/tasks.md`.
- Why this work happened: Phase 32 needs transcript refs to be accepted or
  rejected by human/operator review before media-backed customer claims.
- Decisions applied: current transcript refs remain pending; workflow requires
  reviewer, reason, checksums, accepted scope, and separate external gate.
- Evidence collected: targeted transcript workflow tests pass. Full validation
  after state update: 267 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-019 OCR And Chart Source-Link Policy`.

### 2026-05-19 — SAS-NEXT-017 — Media Acquisition Inventory Per Channel

- Scope: `docs/pilot/three_channel_V2_MEDIA_INVENTORY.md`,
  `tests/unit/test_media_acquisition_inventory_v2.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 32 needs concrete multimodal inventory before
  transcript/OCR review workflows can be applied.
- Decisions applied: recorded acquired `bablos79` voice refs with SHA-256,
  blocked unlinked media refs, and explicit `not_acquired` posture for the two
  other pilot channels.
- Evidence collected: targeted inventory tests pass. Full validation after
  state update: 265 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-018 Transcript Human Review Workflow`.

### 2026-05-19 — SAS-NEXT-016 — Robustness Checks

- Scope: `docs/pilot/three_channel_V2_ROBUSTNESS_APPENDIX.md`,
  `tests/unit/test_metric_robustness_appendix.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 31 needs explicit sensitivity checks before
  channel utility conclusions can be strengthened.
- Decisions applied: horizon, provider, and sample-size robustness checks are
  documented; current V2 artifacts remain not robust for external delivery.
- Evidence collected: targeted robustness tests pass. Full validation after
  state update: 263 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-017 Media Acquisition Inventory Per Channel`.

### 2026-05-19 — SAS-NEXT-015 — Channel Utility Score V2

- Scope: `docs/pilot/three_channel_V2_SCORECARD.md`,
  `tests/unit/test_channel_utility_score_v2.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 31 needs a diagnostic scorecard that separates
  utility dimensions before robustness checks.
- Decisions applied: scorecard separates coverage, clarity, extraction quality,
  outcome quality, risk quality, limitations, and confidence/sample-size
  warnings, while avoiding composite score claims.
- Evidence collected: targeted scorecard tests pass. Full validation after
  state update: 261 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-016 Robustness Checks`.

### 2026-05-19 — SAS-NEXT-014 — Setup Outcome Expansion

- Scope: `src/signal_sandbox/claims/outcomes.py`,
  `tests/unit/test_setup_outcome_expansion.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 31 needs setup outcomes to support strict
  entry/stop/target/timeout evaluation and R multiple.
- Decisions applied: setup outcomes now store `r_multiple`, compute it from
  initial risk for target, stopped, and timeout exits, and keep missing or
  invalid levels as explicit blockers.
- Evidence collected: targeted setup/outcome tests pass. Full validation after
  state update: 259 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-015 Channel Utility Score V2`.

### 2026-05-19 — SAS-NEXT-013 — Quant Metric Schema V2

- Scope: `docs/specs/CHANNEL_QUANT_METRICS_V2.md`,
  `tests/unit/test_quant_metrics_v2_spec.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 31 needs a stable quant metric contract before
  expanding setup outcomes and scorecards.
- Decisions applied: defined extraction precision/recall, hit rate by type,
  return percent, MFE/MAE, RR, R multiple, benchmark-relative return, drawdown,
  coverage metrics, and mandatory confidence/sample-size warnings.
- Evidence collected: targeted spec tests pass. Full validation after state
  update: 256 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-014 Setup Outcome Expansion`.

### 2026-05-19 — SAS-NEXT-012 — Benchmark-Relative Outcomes

- Scope: `src/signal_sandbox/claims/outcomes.py`,
  `tests/unit/test_benchmark_relative_outcomes.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 30 needs deterministic benchmark-relative
  returns for approved benchmark mappings.
- Decisions applied: outcome engine can compute claim return minus benchmark
  return when both snapshots exist and emits `missing_benchmark_data` when
  benchmark snapshot/horizon data is absent.
- Evidence collected: targeted benchmark tests pass. Full validation after
  state update: 254 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-013 Quant Metric Schema V2`.

### 2026-05-19 — SAS-NEXT-011 — Futures And Commodity Proxy Policy

- Scope: `docs/specs/FUTURES_COMMODITY_PROXY_POLICY.md`,
  `tests/unit/test_futures_commodity_proxy_policy.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 30 requires futures/commodity/index shorthand
  policy before those rows can be scored.
- Decisions applied: `BR`, `NG`, `GOLD`, `SI`, `MIX`, and `IMOEX` remain
  unscoreable without explicit instrument, direction semantics, rollover rule,
  provider, and horizon approval.
- Evidence collected: targeted policy tests pass. Full validation after state
  update: 252 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-012 Benchmark-Relative Outcomes`.

### 2026-05-19 — SAS-NEXT-010 — FX Proxy Policy

- Scope: `docs/specs/FX_PROXY_POLICY.md`,
  `tests/unit/test_fx_proxy_policy.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 30 requires explicit FX pair/direction/provider
  semantics before currency shorthand can enter scoring.
- Decisions applied: no FX shorthand is scoreable by default. `CNY`, `CN`, and
  similar shorthand stay unmapped until operator approves exact pair, direction
  semantics, provider, and horizon.
- Evidence collected: targeted FX policy tests pass. Full validation after
  state update: 250 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-011 Futures And Commodity Proxy Policy`.

### 2026-05-19 — SAS-NEXT-009 — US Equity And Fund Provider Path

- Scope: `src/signal_sandbox/claims/provider_config.py`,
  `docs/pilot/three_channel_V1_APPROVAL_MATRIX.md`,
  `tests/unit/test_us_provider_proxy_path.py`,
  `tests/unit/test_provider_proxy_config_v1.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 30 expands provider/proxy coverage while
  keeping market-data fetches on-demand and scoped.
- Decisions applied: `SPY`, `QQQ`, `AAPL`, `MSFT`, `NVDA`, `TSLA`, and `AMD`
  route to gated `yfinance_dev`. Ambiguous or unsupported symbols such as
  `SPYF` and `OPENAI` remain provider-gap exclusions.
- Evidence collected: targeted provider tests pass. Full validation after
  state update: 248 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-010 FX Proxy Policy`.

### 2026-05-19 — SAS-NEXT-008 — Review Audit Trail

- Scope: `src/signal_sandbox/review/audit.py`,
  `src/signal_sandbox/review/__init__.py`,
  `docs/pilot/three_channel_REVIEW_AUDIT.md`,
  `tests/unit/test_review_audit_trail.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 29 must block external delivery when review
  decisions are incomplete or accepted claims lack required evidence.
- Decisions applied: audit reports 1710 missing operator decisions, zero
  accepted decisions missing required evidence, and `external_gate_blocked`.
- Evidence collected: targeted audit tests pass. Full validation after state
  update: 245 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-009 US Equity And Fund Provider Path`.

### 2026-05-19 — SAS-NEXT-007 — Minimal Review UI

- Scope: `src/signal_sandbox/review/ui.py`,
  `docs/pilot/review_ui/three_channel_review_ui.html`,
  `tests/unit/test_review_ui_static.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 29 needs an ergonomic local/static review
  surface before operator closure can scale across 1710 queue rows.
- Decisions applied: added static HTML surface with channel, claim type, asset,
  provider-status, and review-status filters; row selection shows source text
  next to normalized fields and generates local deterministic JSON/Markdown
  decision artifacts.
- Evidence collected: targeted static UI tests pass. Full validation after
  state update: 242 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-008 Review Audit Trail`.

### 2026-05-19 — SAS-NEXT-006 — Review Queue API And Export

- Scope: `src/signal_sandbox/review/queue.py`,
  `src/signal_sandbox/review/__init__.py`,
  `tests/unit/test_review_queue_export.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 29 needs deterministic import/export before a
  review UI can operate on queue rows and operator decisions.
- Decisions applied: added `ReviewQueueArtifact`/`ReviewQueueRow` loader with
  required-field validation and stable JSON/Markdown decision exporters that
  preserve source links and evidence spans.
- Evidence collected: targeted queue/export tests pass. Full validation after
  state update: 239 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-007 Minimal Review UI`.

### 2026-05-19 — SAS-NEXT-005 — Review Decision Data Model

- Scope: `src/signal_sandbox/review/__init__.py`,
  `src/signal_sandbox/review/decisions.py`,
  `tests/unit/test_review_decision_model.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 29 needs durable operator closure decisions
  before review queue workflow can be operated.
- Decisions applied: added strict `ReviewDecision`, `ReviewEvidenceSpan`, and
  `ReviewDecisionStatus` models with accepted, false_positive, false_negative,
  needs_context, unsupported_provider, and media_blocked statuses.
- Evidence collected: targeted model tests pass. Full validation after state
  update: 236 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-006 Review Queue API And Export`.

### 2026-05-19 — SAS-NEXT-004 — External Gate Rerun

- Scope: `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`,
  `tests/unit/test_external_gate_rerun_v2.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 28 requires an external-ready gate rerun after
  full queue creation, false-negative pass, and report language safety.
- Decisions applied: gate remains `approve_internal_only`. Phase 28 evidence
  improved, but review closure, provider/media coverage, and RR/setup quality
  remain incomplete.
- Evidence collected: gate cites review coverage, false-negative handling,
  provider coverage, multimodal posture, RR/setup coverage, and report wording
  safety. Validation after update: 232 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-005 Review Decision Data Model`.

### 2026-05-19 — SAS-NEXT-003 — Report Language Safety Pass

- Scope: `src/signal_sandbox/reports/safety.py`,
  `src/signal_sandbox/reports/__init__.py`,
  `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`,
  `docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.md`,
  `docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.json`,
  `tests/unit/test_report_language_safety_v2.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 28 requires deterministic report wording checks
  before external gate rerun.
- Decisions applied: V1 report now states `Decision: approve_internal_only`,
  says external/customer-facing delivery is not approved, updates
  false-negative wording after `SAS-NEXT-002`, and keeps media/OCR/chart rows
  excluded from customer-facing metrics.
- Evidence collected: safety scanner passed with zero findings and all required
  context present. Validation after update: 230 passed, 0 skipped; ruff and
  pyright pass.
- Follow-ups: run `SAS-NEXT-004 External Gate Rerun`.

### 2026-05-19 — SAS-NEXT-002 — False-Negative Extraction Pass

- Scope: `docs/pilot/three_channel_FALSE_NEGATIVE_PASS.md`,
  `docs/pilot/three_channel_FALSE_NEGATIVE_PASS.json`,
  `docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md`,
  `src/signal_sandbox/claims/extractor.py`,
  `tests/unit/test_false_negative_extraction_pass.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: operator asked the model to review the evidence file
  and return decisions for the pending false negatives.
- Decisions applied: five pending false negatives were reviewed. Three became
  structured drafts (`fn-001`, `fn-004`, `fn-005`), two remain `needs_context`
  (`fn-002`, `fn-003`), and zero are scoreable customer-facing win/loss rows
  now.
- Evidence collected: `227 passed, 0 skipped`; ruff and pyright pass. Extractor
  now handles plain BTC/ETH/TON token-boundary aliases, BTC Russian alias
  evidence, trap/safety-line setup cues, future close/management wording, and
  keeps `SIGN-UP` blocked.
- Follow-ups: run `SAS-NEXT-003 Report Language Safety Pass`.

### 2026-05-19 — SAS-NEXT-001 — Full-Corpus Human Review Queue

- Scope: `docs/pilot/three_channel_FULL_REVIEW_QUEUE.md`,
  `docs/pilot/three_channel_FULL_REVIEW_QUEUE.json`,
  `tests/unit/test_full_review_queue_artifact.py`, active state files, and
  `docs/tasks.md`.
- Why this work happened: Phase 28 requires full-corpus review coverage before
  any external-ready gate retry.
- Decisions applied: the queue is internal-only and external delivery remains
  blocked until review closure and gate rerun. It covers 1710 rows: 172 V1
  included claim rows, 1534 source text rows, 5 pending false negatives, 233
  provider-gap tagged rows, and 4 media-blocked rows.
- Evidence collected: targeted queue test passes. Full validation after state
  update: 223 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-002 False-Negative Extraction Pass`.

### 2026-05-19 — STRATEGY — AI Development Plan

- Scope: `docs/AI_DEVELOPMENT_PLAN_RU.md`, `README.md`,
  `docs/CODEX_PROMPT.md`, `tests/unit/test_ai_development_plan_doc.py`.
- Why this work happened: operator asked to write a detailed follow-on
  development plan for AI-assisted implementation after Phase 27 V1 closure.
- Decisions applied: next recommended path is Phase 28 external-ready review
  sprint, starting with `SAS-NEXT-001 Full-corpus human review queue`, before
  dashboard/marketplace work.
- Evidence collected: tests assert the plan includes execution tracks, phases,
  guardrails, next action, and validation commands. Validation after doc update:
  218 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: choose whether to execute Phase 28, provider/media expansion, or
  internal buyer-demo packaging.
- Notes for next agent: this is planning documentation only; it does not
  approve external delivery.

### 2026-05-19 — STATE — Post-V1 Task Graph And Prompt Compaction

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`,
  `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`,
  `docs/archive/POST_V1_STATE_COMPACTION_2026-05-19.md`.
- Why this work happened: operator asked whether tasks were updated, excess
  state moved to archive, and bloated prompts reduced.
- Decisions applied: `SAS-NEXT-001..032` were added to `docs/tasks.md` across
  Phases 28-35. Active state now points to `SAS-NEXT-001`. Prompt/handoff files
  were compacted to current state and canonical links; long history remains in
  journal and archive files.
- Evidence collected: state compaction archive records current baseline,
  external gate, and next task. Validation after compaction: 220 passed,
  0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-NEXT-001 Full-Corpus Human Review Queue`.
- Notes for next agent: do not expand active prompt files with phase history;
  append durable history to `docs/IMPLEMENTATION_JOURNAL.md` instead.

### 2026-05-19 — SAS-V1-009 — Phase 27 Deep Review

- Scope: `docs/archive/PHASE27_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/audit/PHASE_REPORT_LATEST.md`,
  `tests/unit/test_phase27_review_artifact.py`, `docs/tasks.md`, state docs.
- Why this work happened: Phase 27 was complete and the orchestrator requires
  a deep review/archive at phase boundary.
- Decisions applied: Phase 27 passed with no P0/P1/P2 implementation findings.
  Internal V1 validation is approved; external delivery remains not approved
  under gate decision `approve_internal_only`.
- Evidence collected: archive records source legality, extraction calibration,
  provider/proxy, multimodal posture, metric reproducibility, report overclaim,
  and external gate checks. Validation after task: 215 passed, 0 skipped; ruff
  and pyright pass.
- Follow-ups: operator strategy decision: full human review, provider/media
  expansion, or internal buyer-demo packaging.
- Notes for next agent: planned phases 0-27 are complete.

### 2026-05-19 — SAS-V1-008 — Customer-Facing V1 Report And External Gate

- Scope: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`,
  `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`,
  `tests/unit/test_three_channel_v1_external_report.py`, `docs/tasks.md`.
- Why this work happened: V1 needed a customer-readable candidate report and a
  clear external-readiness decision.
- Decisions applied: report is internal-only and limitations-first; gate
  decision is `approve_internal_only`, not paid external delivery.
- Evidence collected: tests assert report metrics/examples/limitations and gate
  blockers/no-advice posture. Validation after task: 213 passed, 0 skipped;
  ruff and pyright pass.
- Follow-ups: run `SAS-V1-009` Phase 27 Deep Review.
- Notes for next agent: do not present the report externally without resolving
  gate blockers.

### 2026-05-19 — SAS-V1-007 — Three-Channel Metrics V1 Recompute

- Scope: `scripts/three_channel_v1_metric_report.py`,
  `docs/pilot/three_channel_V1_METRIC_RESULTS.json`,
  `docs/pilot/three_channel_V1_SCORECARD.md`,
  `tests/unit/test_three_channel_metric_results_v1.py`, `docs/tasks.md`,
  state docs.
- Why this work happened: Phase 27 needed internal V1 metrics after approval,
  extraction review, structured extraction, outcome, media, and provider work.
- Decisions applied: V1 applies `SAS-V1-002` review exclusions to V0 evaluated
  claims; false negatives are pending extraction, not wins/losses; unreviewed
  media remains excluded.
- Evidence collected: V1 evaluable claims are `bablos79` 14,
  `nemphiscrypts` 49, `pifagortrade` 107. Scorecard separates coverage,
  extraction quality, outcome quality, risk quality, and evidence limitations.
  Validation after task: 211 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-V1-008` Customer-Facing V1 Report And External Gate.
- Notes for next agent: V1 metrics remain internal until the gate decision.

### 2026-05-19 — SAS-V1-006 — Provider And Proxy Expansion V1

- Scope: `src/signal_sandbox/claims/provider_config.py`,
  `tests/unit/test_provider_proxy_config_v1.py`,
  `docs/pilot/three_channel_V1_APPROVAL_MATRIX.md`, `docs/tasks.md`, state
  docs.
- Why this work happened: V1 needs approved provider/proxy routing and
  on-demand fetch planning before metric recompute.
- Decisions applied: approved Binance crypto and MOEX ISS share routes are
  mappable; futures, FX, US ETF/fund, commodity, and benchmark proxies remain
  `needs_operator_input` unless explicitly approved; provider gaps are
  exclusions, not wins/losses.
- Evidence collected: tests cover approved/unsupported class mapping,
  approved-only fetch planning, and provider-gap exclusions. Validation after
  task: 209 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-V1-007` Three-Channel Metrics V1 Recompute.
- Notes for next agent: fetch planning emits windows only; it does not fetch
  or store bulk market history.

### 2026-05-19 — SAS-V1-005 — Multimodal Claim Extraction V1

- Scope: `docs/pilot/three_channel_V1_MEDIA_INVENTORY.md`,
  `src/signal_sandbox/claims/multimodal.py`,
  `tests/unit/test_multimodal_claim_extraction_v1.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: V1 needs a single claim surface for reviewed text,
  transcript, and OCR evidence while preserving media review boundaries.
- Decisions applied: reviewed transcript/OCR refs may produce structured claim
  drafts with media provenance and source-document links; unreviewed
  transcript/OCR/chart refs remain excluded from customer-facing metrics.
- Evidence collected: tests cover three-channel media inventory status,
  reviewed transcript claim extraction, and unreviewed transcript/OCR
  exclusion. Validation after task: 206 passed, 0 skipped; `ruff check src/
  tests/`, `ruff format --check src/ tests/`, and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-V1-006` Provider And Proxy Expansion V1.
- Notes for next agent: current three-channel media posture remains text-only
  for customer-facing metrics because no media refs are human/operator external
  accepted yet.

### 2026-05-19 — SAS-V1-004 — Level-Aware Outcome Engine V1

- Scope: `src/signal_sandbox/claims/outcomes.py`,
  `tests/unit/test_claim_outcomes_v1.py`,
  `docs/specs/CHANNEL_UTILITY_EVALUATION.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: V1 needs deterministic setup and directional thesis
  outcomes before recomputing three-channel metrics.
- Decisions applied: strict `trade_setup` outcomes require entry, stop, target,
  and direction; `directional_thesis` rows retain fixed-horizon returns without
  levels; `trade_management` rows are excluded unless linked to an approved
  original setup.
- Evidence collected: tests cover target/stop setup outcomes with provenance,
  directional-thesis fixed horizon without levels, and trade-management
  exclusion. Validation after task: 203 passed, 0 skipped; `ruff check src/
  tests/`, `ruff format --check src/ tests/`, and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-V1-005` Multimodal Claim Extraction V1.
- Notes for next agent: the outcome engine consumes immutable snapshots; it
  does not fetch market data or infer missing levels.

### 2026-05-19 — SAS-V1-003 — Structured Claim Extractor V1

- Scope: `src/signal_sandbox/claims/`,
  `tests/unit/test_structured_claim_extractor_v1.py`,
  `docs/specs/CHANNEL_UTILITY_EVALUATION.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: V1 needs reusable structured claim rows before
  level-aware outcomes and metric recompute.
- Decisions applied: added a deterministic, rule-only text extractor for
  `SourceDocument` inputs. It emits claim type, asset/proxy mentions,
  direction, entry/stop/target/RR, horizon hints, evidence spans, ambiguity
  flags, and blockers. Missing structured fields remain null with blockers.
- Evidence collected: tests cover row emission, six claim types, evidence-only
  level fields, missing-field blockers, ambiguity flags, and blocked asset
  tokens. Validation after task: 200 passed, 0 skipped; `ruff check src/
  tests/`, `ruff format --check src/ tests/`, and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-V1-004` Level-Aware Outcome Engine V1.
- Notes for next agent: the extractor normalizes claims only; it does not call
  market APIs or compute outcomes.

### 2026-05-19 — SAS-V1-002 — False-Positive Review And Extractor Calibration Pack

- Scope: `docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md`,
  `docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md`,
  `tests/unit/test_three_channel_v1_extraction_review.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: V1 needed extraction quality review before
  recomputing metrics or producing customer-facing wording.
- Decisions applied: reviewed 20 included V0 claims and 21 excluded public
  probe rows. Calibration now requires negation-aware direction parsing,
  trade-management linkage, conditional setup handling, BTC/ETH alias
  expansion, non-asset token blocking, provider/proxy boundaries, and media
  review boundaries.
- Evidence collected: tests assert sample sizes, allowed review statuses, all
  three channels, and required calibration rules. Validation after task: 196
  passed, 0 skipped; `ruff check src/ tests/`, `ruff format --check src/
  tests/`, and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-V1-003` Structured Claim Extractor V1.
- Notes for next agent: V0 extraction issues are now explicit; the code
  extractor should implement these deterministic constraints before V1 metrics.

### 2026-05-19 — SAS-V1-001 — Three-Channel Approval Matrix

- Scope: `docs/pilot/three_channel_V1_APPROVAL_MATRIX.md`,
  `tests/unit/test_three_channel_v1_approval_matrix.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: Phase 27 needed explicit evaluator, claim-type,
  horizon, provider/proxy, and exclusion decisions before V1 recomputation or
  customer-facing wording.
- Decisions applied: V0 Binance crypto and MOEX ISS share provider classes are
  approved for internal V1 calibration; futures, FX, US ETF/fund, commodity,
  and ambiguous aliases are `needs_operator_input` or `rejected_until_mapped`;
  V0 numbers remain internal until false-positive review and V1 gate.
- Evidence collected: tests assert all three channels are covered, all V0
  provider/proxy classes are decisioned, and external V0 use remains blocked.
  Validation after task: 193 passed, 0 skipped; `ruff check src/ tests/`,
  `ruff format --check src/ tests/`, and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-V1-002` False-Positive Review And Extractor Calibration
  Pack.
- Notes for next agent: the approval matrix is not a customer-facing approval;
  it only authorizes internal V1 calibration work.

### 2026-05-19 — SAS-ER-006 — Phase 26 Deep Review

- Scope: `docs/archive/PHASE26_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/audit/PHASE_REPORT_LATEST.md`,
  `tests/unit/test_phase26_review_artifact.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: Phase 26 was complete and the orchestrator requires
  a deep review/archive before Phase 27 starts.
- Decisions applied: Phase 26 passed with no P0/P1/P2 implementation findings.
  V0 metrics and `bablos79` proxy approvals remain internal research; external
  delivery remains blocked until V1 review and gate.
- Evidence collected: `docs/archive/PHASE26_REVIEW.md` records public-source,
  approval matrix, market-data, metric reproducibility, customer-facing, media,
  and no-advice checks. Validation after task: 190 passed, 0 skipped; `ruff
  check src/ tests/`, `ruff format --check src/ tests/`, and `.venv/bin/pyright`
  pass.
- Follow-ups: run `SAS-V1-001` Three-Channel Approval Matrix.
- Notes for next agent: Phase 27 is active. Do not recompute V1 metrics or
  produce customer-facing wording before the V1 approval matrix exists.

### 2026-05-19 — SAS-ER-001 — Candidate Review And Proxy/Horizon Approval

- Scope: `docs/pilot/bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md`,
  `docs/pilot/bablos79_EVIDENCE_REPAIR_OPERATOR_ACTIONS.md`,
  `tests/unit/test_evidence_repair_proxy_approvals.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: operator asked to proceed after the V0 metric report
  and V1 roadmap; Phase 26 still needed explicit approval/rejection of
  `bablos79` candidate rows, proxies, horizons, providers, and outcome method.
- Decisions applied: approvals are internal V1 research only. Nine position
  disclosure rows have partial asset-level MOEX ISS proxy approvals, one row is
  rejected as context, unsupported assets remain `do_not_fetch`, timestamp
  basis is public Telegram post time, primary horizon is 7d with 1d/3d
  diagnostics, and external/customer-facing use remains blocked.
- Evidence collected: approval tests cover all ten position candidates,
  required provider/horizon/method fields, and blocked unapproved fetches.
  Validation after task: 188 passed, 0 skipped; `ruff check src/ tests/`,
  `ruff format --check src/ tests/`, and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-ER-006` Phase 26 Deep Review before starting
  `SAS-V1-001`.
- Notes for next agent: Phase 27 is planned but should not start until the
  Phase 26 review/archive is complete.

### 2026-05-19 — SAS-ER-005 — Three-Channel V1 Roadmap Task Graph

- Scope: `docs/tasks.md`, `docs/pilot/THREE_CHANNEL_V1_ROADMAP.md`,
  `tests/unit/test_three_channel_v1_roadmap.py`, `docs/CODEX_PROMPT.md`,
  `README.md`, `MEMORY.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`,
  `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: operator asked to make the post-V0 next steps
  concrete in the roadmap after the first V0 metric report.
- Decisions applied: Phase 27 is planned as `SAS-V1-001..009`, covering
  approval matrix, false-positive review, structured claim extraction,
  level-aware outcomes, multimodal claims, provider/proxy expansion, V1
  metric recompute, customer-facing gate, and mandatory deep review.
- Evidence collected: added `docs/pilot/THREE_CHANNEL_V1_ROADMAP.md`; tests
  assert the Phase 27 task graph lists all V1 tasks, covers required
  improvements, and preserves no-private-scraping/no-bulk-market-history/
  no-overclaim boundaries.
- Follow-ups: run `SAS-ER-001` operator approval, then start `SAS-V1-001`
  once Phase 26 approval prerequisites are satisfied.
- Notes for next agent: Phase 27 is planned but not started. V0 metrics remain
  internal research until review and the V1 external-ready gate.

### 2026-05-17 — SAS-ER-004 — Three-Channel Metric Results V0

- Scope: `scripts/three_channel_metric_report.py`,
  `docs/pilot/three_channel_METRIC_RESULTS.json`,
  `docs/pilot/three_channel_METRIC_REPORT.md`,
  `tests/unit/test_three_channel_metric_results.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: operator requested an end-to-end first result that
  compares channels by metrics and produces a report with confirmations and
  numbers.
- Decisions applied: V0 uses public Telegram `/s/` source text, conservative
  rule extraction, asset-level claims, 7d primary horizon, Binance public
  klines for crypto, MOEX ISS daily candles for supported MOEX shares, compact
  per-claim provider confirmation, no bulk market-history database, and no
  investment-advice/future-profit claim.
- Evidence collected: 1,534 public text rows; 187 normalized asset-level
  claims; 184 7d-evaluable claims; 102 confirmed hits; 82 contradicted misses.
  Primary 7d hit rates: `bablos79` 57.894737%, `nemphiscrypts` 58.490566%,
  `pifagortrade` 53.571429%. Report includes confirmed and contradicted
  examples with Telegram evidence links and provider metadata in JSON.
- Follow-ups: human/operator review should inspect extraction false positives,
  approve customer-facing language, and decide whether to add intraday,
  level-aware setup metrics, audio/OCR claim extraction, and broader provider
  coverage.
- Notes for next agent: this is internal V0 research. Do not present it as a
  final channel ranking or paid-ready report without review of the extracted
  claims and wording.

### 2026-05-17 — SAS-ER-003 — Channel Utility Evaluation Contract

- Scope: `docs/specs/CHANNEL_UTILITY_EVALUATION.md`,
  `tests/unit/test_channel_utility_evaluation_spec.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: operator clarified that all market assertions and
  trades confirmed by future market behavior should be validated through open
  APIs without storing huge market databases, and that text, audio, and images
  must normalize into a shared evaluation surface.
- Decisions applied: multimodal evidence converges into `SourceDocument` and
  `MarketIdea`/claim rows; open/public API or operator-public-export windows
  are fetched only after approval; compact immutable snapshots are cached only
  when needed for reproducibility; ambiguous and machine-extracted fields remain
  operator-gated.
- Evidence collected: added a spec covering storage posture, multimodal
  extraction, claim types, evaluation methods, utility metrics, and no-overclaim
  report boundaries. Tests assert multimodal normalization, open/on-demand
  validation, deterministic metrics, operator gating, counterexamples, and no
  future-profit claims.
- Follow-ups: build the three-channel approval matrix for evaluator type,
  claim types, proxy/provider mapping, horizons, strict trade rules, and
  exclusion statuses.
- Notes for next agent: do not compute channel usefulness from raw candidate
  counts. Counts only decide whether there is enough material to approve
  evaluation rules.

### 2026-05-17 — SAS-ER-002 — Three-Channel Public Corpus Probe

- Scope: `scripts/three_channel_public_probe.py`,
  `docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json`,
  `docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.md`,
  `tests/unit/test_three_channel_probe_artifacts.py`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `MEMORY.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `ORCHESTRATOR_CHECKPOINT.md`.
- Why this work happened: operator asked whether the same evidence/readiness
  approach can be applied to the three initial pilot channels, then instructed
  codex to do it.
- Decisions applied: same public Telegram `/s/` method for all three channels;
  no private scraping, login-walled source use, market-data fetch, outcome
  computation, proxy approval, or external claim creation.
- Evidence collected: public probe covered 1,534 text rows across `bablos79`,
  `nemphiscrypts`, and `pifagortrade`; it queued 963 market-adjacent
  candidates, including 64 explicit setup candidates and 114 position/trade
  language candidates. `pifagortrade` is the strongest first-pass candidate
  for setup/directional evaluation; `nemphiscrypts` is suitable for crypto
  directional evaluation after proxy approval; `bablos79` remains mixed and
  needs stricter mapping.
- Follow-ups: run `SAS-ER-001: Candidate Review And Proxy/Horizon Approval`
  for evaluator type, proxy mapping, timestamp basis, horizons, and outcome
  method approval.
- Notes for next agent: the probe is a readiness surface, not a ranking or
  performance report. Every review sample still has
  `market_data_fetch_allowed_now=false` and `external_eligible_now=false`.

### 2026-05-17 — SAS-ER-000 — Public Corpus Repair Capture

- Scope: `docs/pilot/bablos79_EVIDENCE_REPAIR_CAPTURE_MANIFEST.json`,
  `docs/pilot/bablos79_EVIDENCE_REPAIR_CAPTURE_PACK.md`,
  `docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.json`,
  `docs/pilot/bablos79_EVIDENCE_REPAIR_REVIEW_QUEUE.md`,
  `docs/pilot/bablos79_EVIDENCE_REPAIR_OPERATOR_ACTIONS.md`,
  `tests/unit/test_evidence_repair_artifacts.py`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: operator asked to do the evidence repair needed for
  `bablos79` after Phase 25 rejected external delivery.
- Decisions applied: public `/s/` Telegram route only; no private scraping; no
  outcomes, proxy approvals, market-data fetches, media acceptance, or external
  claims without operator approval.
- Evidence collected: 30 public `/s/` pages fetched; 585 public message rows in
  window; 522 text rows; 462 fresh workspace capture JSON files written; 156
  market-adjacent candidates queued; 10 position disclosure candidates queued.
- Follow-ups: run `SAS-ER-001: Candidate Review And Proxy/Horizon Approval`.
- Notes for next agent: position disclosure rows are the most promising path to
  measurable outcomes, but they still need explicit horizon/outcome and proxy
  approval before any market data fetch.

### 2026-05-15 — SAS-DR-022 — Author Capability Report Deep Review

- Scope: `docs/archive/PHASE25_RETROSPECTIVE_REVIEW.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/META_ANALYSIS.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`,
  `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 25 needed the mandatory boundary review and
  archive to close the deep channel retrospective loop.
- Decisions applied: `SAS-DR-018..021`; external delivery remains rejected and
  next work must repair evidence rather than move to marketplace scope.
- Evidence collected: Cycle 25 review found no P0/P1/P2 implementation
  findings; scorecard/report/demo/gate preserve insufficient-evidence posture;
  planned phases 0-25 are complete.
- Follow-ups: none in current task graph. Operator may start a new
  evidence-repair/corpus-expansion loop.
- Notes for next agent: internal archive/demo scope is allowed; external paid
  report, positive author-strength claims, ranking, advice, and
  future-performance claims remain blocked.

### 2026-05-15 — SAS-DR-021 — Deep External Ready Gate

- Scope: `docs/pilot/bablos79_DEEP_EXTERNAL_READY_GATE.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 25 needed an external ready/reject decision
  before final deep review.
- Decisions applied: `SAS-DR-020` demo pack; no external delivery without
  sufficient evidence, market outcomes, accepted media, legal boundary, and
  claim-safe posture.
- Evidence collected: gate decision is `reject_external_delivery`; internal
  demo scope is allowed; external paid report scope is rejected; buyer promise,
  exclusions, feedback questions, and reconsideration conditions are recorded.
- Follow-ups: run `SAS-DR-022: Author Capability Deep Review` next.
- Notes for next agent: Phase 25 final review should close the retrospective as
  internal-only/rejected for external delivery unless a new operator decision
  changes the evidence state.

### 2026-05-15 — SAS-DR-020 — Deep Retrospective Demo Pack

- Scope: `docs/pilot/bablos79_DEEP_RETROSPECTIVE_DEMO_PACK.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 25 needed an internal demo pack for warm
  conversations before external-ready gate review.
- Decisions applied: `SAS-DR-019` report posture; demo pack must remain
  internal-only/not-external-ready and must not expose raw media or overstate
  transcript/OCR certainty.
- Evidence collected: demo pack includes report summary, strongest available
  topic examples, counterexamples/blockers, media evidence summary, market
  outcome summary, limitations, buyer use case, talk track, demo boundaries,
  and canonical links.
- Follow-ups: run `SAS-DR-021: Deep External Ready Gate` next.
- Notes for next agent: expected gate decision is reject/not-external-ready
  unless a new operator decision overrides the current evidence state.

### 2026-05-15 — SAS-DR-019 — Author Capability Report V1

- Scope: `docs/pilot/reports/bablos79_AUTHOR_CAPABILITY_REPORT_V1.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 25 needed a buyer-readable report generated
  from the scorecard, ledger, outcomes, media evidence, and limitations.
- Decisions applied: `SAS-DR-018` scorecard and Phase 24 deep review; report
  must be insufficient-evidence first and must not force a positive narrative.
- Evidence collected: report V1 includes source/period, evidence coverage,
  scorecard summary, topic observations, weak/non-measurable examples, public
  market outcome state, media evidence summary, limitations, external-delivery
  posture, evidence appendix, and no-advice boundary.
- Follow-ups: run `SAS-DR-020: Deep Retrospective Demo Pack` next.
- Notes for next agent: demo pack must state internal-only/not-external-ready
  and must not expose raw media or overstate transcript/OCR certainty.

### 2026-05-15 — SAS-DR-018 — Author Capability Scorecard

- Scope: `docs/pilot/bablos79_AUTHOR_CAPABILITY_SCORECARD.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 25 needed a scorecard structure before the
  buyer-readable author capability report.
- Decisions applied: Phase 24 deep review; positive author-strength claims are
  blocked unless later corpus/proxy/outcome evidence supports them.
- Evidence collected: scorecard labels categories as
  `insufficient_evidence`, `context_only`, `blocked`, `not_measured`, or
  `not_applicable`; it makes no positive strength claims and enumerates the
  required report limitations.
- Follow-ups: run `SAS-DR-019: Author Capability Report V1` next.
- Notes for next agent: report V1 must explain evidence and limitations rather
  than imply author skill, reliability, ranking, advice, or future performance.

### 2026-05-15 — SAS-DR-017 — Claim Ledger Deep Review

- Scope: `docs/archive/PHASE24_REVIEW.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/META_ANALYSIS.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`,
  `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 24 needed the mandatory boundary review before
  author capability report artifacts could begin.
- Decisions applied: `SAS-DR-012..016`; no positive author capability claim
  without sufficient reviewable corpus, approved proxies, market snapshots,
  computed outcomes, and balanced counterexample review.
- Evidence collected: Cycle 24 review found no P0/P1/P2 implementation
  findings, but blocked positive author-strength claims because there are only
  14 reviewable non-blocker claim rows, 0 approved proxies, 0 market snapshots,
  0 computed outcomes, and 0 confirmed or contradicted examples.
- Follow-ups: run `SAS-DR-018: Author Capability Scorecard` next.
- Notes for next agent: Phase 25 must use an insufficient-evidence /
  limitations-first posture unless the operator later expands corpus and
  approves proxy/media evidence.

### 2026-05-15 — SAS-DR-016 — Counterexample And Weak Evidence Register

- Scope: `docs/pilot/bablos79_COUNTEREXAMPLES.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 24 needed weak, blocked, unresolved,
  non-measurable, and unsupported examples preserved before any author
  capability report could make a positive claim.
- Decisions applied: `SAS-DR-015` outcome artifact; no positive
  author-strength conclusion without counterexample review and deterministic
  outcome support.
- Evidence collected: register lists unresolved examples, ambiguous/weak
  examples, non-measurable examples, unsupported-media examples, and explicitly
  records that contradicted computed examples are unavailable because no
  metrics were computed.
- Follow-ups: run `SAS-DR-017: Claim Ledger Deep Review` next.
- Notes for next agent: current evidence supports an insufficient-evidence
  report posture, not a positive capability report.

### 2026-05-15 — SAS-DR-015 — Retrospective Outcome Evaluation

- Scope: `docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.json`,
  `docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md`,
  `tests/unit/test_retrospective_outcomes_artifact.py`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`,
  `README.md`.
- Why this work happened: Phase 24 needed outcome-state artifacts after proxy
  mapping, while preventing unsupported market metrics.
- Decisions applied: `SAS-DR-014` proxy map; no outcome metric without approved
  proxy, source timestamp, horizon, and market-data snapshot.
- Evidence collected: 67 outcome rows were recorded; 0 metrics were computed;
  0 market-data snapshots were used; 0 rows were confirmed or contradicted.
  Unresolved, non-measurable, not-applicable, and unsupported-media rows remain
  visible. Targeted outcome artifact tests pass.
- Follow-ups: run `SAS-DR-016: Counterexample And Weak Evidence Register`
  next.
- Notes for next agent: counterexample register should draw from unresolved,
  ambiguous, non-measurable, and unsupported rows because there are no computed
  contradicted outcomes yet.

### 2026-05-15 — SAS-DR-014 — Market Proxy Map

- Scope: `docs/pilot/bablos79_MARKET_PROXY_MAP.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 24 needed explicit proxy decisions before any
  market data fetch or outcome computation could be considered.
- Decisions applied: `SAS-DR-013` draft ledger; no hidden proxy guessing for
  broad market/exchange claims; deterministic outcomes require approved proxy,
  timestamp, horizon, and method.
- Evidence collected: 14 reviewable non-blocker rows were reviewed; 0 proxies
  were approved; 0 market-data fetch rows were allowed. Broad "Russian
  exchange" transcript claims require explicit operator-approved proxy logic and
  transcript acceptance before deterministic or external use.
- Follow-ups: run `SAS-DR-015: Retrospective Outcome Evaluation` next.
- Notes for next agent: expected outcome state is zero computed metrics unless
  a later task adds approved proxy rows.

### 2026-05-15 — SAS-DR-013 — Expanded Claim Ledger Draft

- Scope: `docs/pilot/bablos79_CLAIM_LEDGER.json`,
  `docs/pilot/bablos79_CLAIM_LEDGER.md`,
  `tests/unit/test_claim_ledger_artifact.py`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 24 needed a draft claim ledger that keeps weak,
  ambiguous, non-market, unsupported, and media-blocked rows visible before
  proxy mapping and outcome work.
- Decisions applied: `SAS-DR-012` taxonomy; Phase 23 media evidence boundary;
  draft extraction cannot create final truth.
- Evidence collected: ledger contains 67 rows: 60 text capture rows, 3
  LLM-reviewed internal transcript claim rows, and 4 unsupported media blocker
  rows. It records 14 reviewable non-blocker claim rows, 0 deterministic
  outcome-ready rows, 0 customer-report-eligible rows, and an
  insufficient-corpus decision for the 30-50 reviewable-claim target. Targeted
  ledger artifact tests pass.
- Follow-ups: run `SAS-DR-014: Market Proxy Map` next.
- Notes for next agent: proxy mapping must not invent hidden tickers for broad
  "market" claims; most rows should remain unresolved or non-measurable.

### 2026-05-15 — SAS-DR-012 — Author Claim Taxonomy

- Scope: `docs/pilot/bablos79_CLAIM_TAXONOMY.md`,
  `docs/specs/MARKET_IDEA_SCHEMA.md`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 24 needed a taxonomy before extracting a claim
  ledger, so broad commentary would not be forced into strict trade-signal
  rows.
- Decisions applied: Phase 23 media evidence boundary; existing MarketIdea
  schema and deterministic metric contract; no-advice and no-ranking boundary.
- Evidence collected: taxonomy defines `macro_context`, `event_risk`,
  `directional_bias`, `explicit_trade_setup`, `level_timing_call`,
  `watchlist`, `non_market_commentary`, and `unsupported_media_claim`.
  Deterministic-outcome-ready fields are explicit, and broad claims are allowed
  as author insights without becoming performance evidence.
- Follow-ups: run `SAS-DR-013: Expanded Claim Ledger Draft` next.
- Notes for next agent: include weak, ambiguous, non-market, and unsupported
  media rows in the ledger instead of filtering them out.

### 2026-05-15 — SAS-DR-011 — Multimodal Evidence Deep Review

- Scope: `docs/archive/PHASE23_REVIEW.md`, `docs/audit/REVIEW_REPORT.md`,
  `docs/audit/ARCH_REPORT.md`, `docs/audit/META_ANALYSIS.md`,
  `docs/audit/PHASE_REPORT_LATEST.md`, `docs/audit/AUDIT_INDEX.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`,
  `README.md`.
- Why this work happened: Phase 23 needed a mandatory boundary review before
  claim-ledger and market-outcome work could begin.
- Decisions applied: Phase 23 media evidence gate; `SAS-DR-009` transcript
  acceptance policy; ADR-004 media evidence pipeline; source-truth preservation
  contract.
- Evidence collected: deep review found no P0/P1/P2 implementation findings.
  It confirmed public media authorization boundaries, skipped OCR state,
  image/chart blockers, zero reviewed image/OCR refs, two internal-only
  transcript joins, zero external-eligible media-backed refs, and source-join
  preservation. Validation: 167 passing tests, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-DR-012: Author Claim Taxonomy` next.
- Notes for next agent: Phase 24 may proceed for internal claim-ledger work, but
  external media-backed delivery remains blocked.

### 2026-05-15 — SAS-DR-010 — Multimodal Source Join V2

- Scope: `docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW_V2.md`,
  `tests/unit/test_multimodal_source_join.py`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 23 needed a second source-document preview that
  joins text, voice/transcript, and image/OCR evidence while preserving draft,
  internal, reviewed, and external-eligible boundaries.
- Decisions applied: `SAS-DR-009` transcript acceptance policy; Phase 23 media
  evidence gate; source-document truth preservation contract.
- Evidence collected: preview records 60 text rows, 58 text-only rows, 2
  internal-only LLM-reviewed transcript joins, 0 human/operator accepted
  transcript refs, 0 reviewed image/OCR refs, 4 blocked image/chart/OCR rows,
  and 0 external-eligible media-backed refs. The source-join regression test now
  checks preservation of existing refs plus dedupe of additive media/transcript
  refs. Validation: 167 passing tests, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-DR-011: Multimodal Evidence Deep Review` next.
- Notes for next agent: Phase 23 currently supports internal transcript source
  joins only; it has no external-ready media-backed evidence.

### 2026-05-15 — SAS-DR-009 — Voice/Transcript Review Policy Update

- Scope: `docs/pilot/bablos79_TRANSCRIPT_ACCEPTANCE_POLICY.md`,
  `docs/pilot/bablos79_TRANSCRIPT_LLM_REVIEW.md`,
  `docs/audit/PHASE21_ERROR_REGISTER.md`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 23 needed a policy gate defining how managed
  Whisper drafts and LLM-reviewed transcript refs can support internal joins
  without becoming external report truth.
- Decisions applied: ADR-004 draft-evidence boundary; Phase 21 external-ready
  blockers; Phase 23 media review gate.
- Evidence collected: policy defines `draft_pending_review`,
  `llm_reviewed_internal`, `human_operator_accepted`, `external_claim_ready`,
  and `rejected_unusable`. Both Phase 21 transcript refs are reclassified as
  `llm_reviewed_internal`; internal source joins are allowed with labels;
  external delivery remains blocked without human/operator acceptance or
  explicit claim-level waiver. Transcript evidence content was not changed.
- Follow-ups: run `SAS-DR-010: Multimodal Source Join V2` next.
- Notes for next agent: include transcript refs only in internal-only preview
  sections unless a later human/operator acceptance artifact exists.

### 2026-05-15 — SAS-DR-008 — Image And Chart Review Queue

- Scope: `docs/pilot/bablos79_IMAGE_REVIEW_QUEUE.md`,
  `docs/pilot/bablos79_REVIEWED_MEDIA_EVIDENCE.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 23 needed image/OCR/chart review state and a
  reviewed-media export before any multimodal source join could consume media
  evidence.
- Decisions applied: ADR-004 draft-evidence boundary; `SAS-DR-007` skipped OCR
  run state.
- Evidence collected: review queue lists 4 blocker rows and no draft OCR text,
  visible ticker/level/date evidence, or reviewed chart interpretation.
  Reviewed media evidence export has 0 usable image/chart/OCR refs and carries
  4 blockers forward. Validation remains 166 passing tests, 0 skipped; ruff and
  pyright pass.
- Follow-ups: run `SAS-DR-009: Voice/Transcript Review Policy Update` next.
- Notes for next agent: image/OCR contributes no source-join-ready evidence in
  the current state.

### 2026-05-15 — SAS-DR-007 — OCR Draft Run

- Scope: `docs/pilot/bablos79_OCR_RUN_EXPANDED.md`,
  `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 23 needed the OCR run state recorded before any
  image/chart review queue could decide what evidence exists.
- Decisions applied: ADR-004 draft-evidence boundary; `SAS-DR-006` image
  manifest blockers.
- Evidence collected: OCR provider was not configured or invoked because there
  were 0 acquired image artifacts. The run records 0 inputs, 0 outputs, 4
  skipped items, exact blockers, and the draft-only/no-claim boundary.
  Validation remains 166 passing tests, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-DR-008: Image And Chart Review Queue` next and export
  reviewed media evidence as empty/blocked unless exact source-linked image
  artifacts appear.
- Notes for next agent: no OCR artifact exists; do not invent draft text,
  visible ticker/level/date evidence, or chart interpretation.

### 2026-05-15 — SAS-DR-006 — Public Image Acquisition And Manifest

- Scope: `docs/pilot/bablos79_IMAGE_MANIFEST.json`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 23 needed an explicit image acquisition
  manifest before OCR could run over public screenshots/images/charts.
- Decisions applied: ADR-004 media evidence pipeline; Phase 22 gap register and
  media inventory; public-source-only boundary.
- Evidence collected: no exact public/operator-authorized image, screenshot, or
  chart artifact with source-document linkage exists in the current workspace.
  The manifest records 0 acquired image artifacts, 4 blocked candidate rows, OCR
  not allowed now, no private media committed, and raw-media
  retention/deletion policy. Validation remains 166 passing tests, 0 skipped;
  ruff and pyright pass.
- Follow-ups: run `SAS-DR-007: OCR Draft Run` next. It should record skipped or
  blocked OCR status unless exact source-linked public image artifacts are
  supplied.
- Notes for next agent: do not create OCR output or chart interpretation from
  unlinked channel-level media or locked-window gap assumptions.

### 2026-05-15 — SAS-DR-005 — Expanded Corpus Deep Review

- Scope: `docs/audit/META_ANALYSIS.md`, `docs/audit/ARCH_REPORT.md`,
  `docs/audit/REVIEW_REPORT.md`, `docs/archive/PHASE22_REVIEW.md`,
  `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `AGENT_NOTES.md`,
  `PHASE_HANDOFF.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`,
  `docs/tasks.md`.
- Why this work happened: Phase 22 reached its boundary and needed a deep
  review before Phase 23 image/OCR and multimodal evidence work.
- Decisions applied: `D-026`; ADR-004 media evidence pipeline;
  public-source-only, anti-cherry-pick, draft-media, and no-advice boundaries.
- Evidence collected: Phase 22 review found no P0/P1/P2 implementation
  findings. It verified fixed pre-outcome scope, public-source legality,
  capture integrity, media inventory boundaries, corpus gap disclosure, and no
  private scraping. Validation remains 166 passing tests, 0 skipped; ruff and
  pyright pass. Review archived at `docs/archive/PHASE22_REVIEW.md`.
- Follow-ups: run `SAS-DR-006: Public Image Acquisition And Manifest` next.
  Phase 22 found zero acquisition-ready image/chart rows; keep image acquisition
  blocked unless exact public/operator-authorized source-linked artifacts are
  available.
- Notes for next agent: external delivery remains blocked. Phase 23 must not
  create OCR/image claims from unlinked channel-level media or gap-window
  assumptions.

### 2026-05-15 — SAS-DR-004 — Corpus Gap Register

- Scope: `docs/pilot/bablos79_CORPUS_GAP_REGISTER.md`,
  `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 22 needed known corpus gaps classified before
  extraction, OCR, claim-ledger, market proxy, or outcome work can interpret the
  expanded source window.
- Decisions applied: `D-026`; public-source-only and media evidence boundaries.
- Evidence collected: created 9 gap rows covering missing locked-window
  periods, non-contiguous seed message IDs, missing linked voice/video media,
  unlinked image/chart candidates, forbidden private/access-controlled sources,
  and unresolved timestamps. The register explicitly says gaps are not evidence
  of author quality. Manual docs validation passed; full validation remains 166
  passing tests, 0 skipped; ruff passed.
- Follow-ups: run `SAS-DR-005: Expanded Corpus Deep Review` next before Phase
  23 multimodal evidence work.
- Notes for next agent: the deep review must block Phase 23 if it finds P0/P1
  source-legality, private-scraping, or manifest-integrity issues.

### 2026-05-15 — SAS-DR-003 — Expanded Media Inventory

- Scope: `docs/pilot/bablos79_MEDIA_INVENTORY_EXPANDED.md`,
  `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 22 needed media references separated by source
  document and authorization/acquisition status before OCR, transcription
  review, claim extraction, or outcome work.
- Decisions applied: `D-026`; ADR-004 media evidence pipeline; public-source
  media rules from `docs/legal_risk_memo.md`.
- Evidence collected: inventoried 2 acquired public voice/audio refs, 2 missing
  linked media refs (`bablos79-10486` voice context and `bablos79-10465`
  promised follow-up video), 2 unlinked channel-level image/chart candidates,
  and media blockers for locked-window coverage gaps. Manual docs validation
  passed; full validation remains 166 passing tests, 0 skipped; ruff passed.
- Follow-ups: run `SAS-DR-004: Corpus Gap Register` next to classify all gaps
  before extraction or outcomes.
- Notes for next agent: no image/screenshot/chart item is acquisition-ready for
  OCR yet. Do not claim image analysis, chart interpretation, or transcript/OCR
  usability from this inventory.

### 2026-05-15 — SAS-DR-002 — Expanded Public Capture Manifest

- Scope: `docs/pilot/bablos79_EXPANDED_CAPTURE_MANIFEST.json`,
  `docs/pilot/bablos79_EXPANDED_CAPTURE_PACK.md`,
  `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`, `docs/CODEX_PROMPT.md`,
  `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`,
  `ORCHESTRATOR_CHECKPOINT.md`, `README.md`.
- Why this work happened: Phase 22 needed stable expanded-corpus source
  coverage before media inventory, OCR/transcription, claim extraction, market
  proxy mapping, or retrospective outcomes.
- Decisions applied: `D-026`; `SAS-DR-001` locked public-source and
  anti-cherry-pick scope.
- Evidence collected: registered 60 existing public text seed captures inside
  the locked 90-day window, preserved source/document IDs, source timestamps,
  source URLs, text SHA-256 values, source language, and 2 linked voice media
  refs. The manifest records 3 explicit gap entries: pre-seed locked-window
  coverage, post-seed locked-window coverage, and non-contiguous seed message
  IDs. Manual JSON validation passed; full validation remains 166 passing tests,
  0 skipped; ruff passed.
- Follow-ups: run `SAS-DR-003: Expanded Media Inventory` next. It should use
  the expanded manifest and must not claim OCR, image analysis, or transcript
  usability.
- Notes for next agent: no fresh public network capture was run in this task.
  Treat the manifest as a seed registration plus gap surface, not as full
  coverage of the locked 90-day window.

### 2026-05-15 — SAS-DR-001 — Deep Retrospective Scope Lock

- Scope: `docs/pilot/bablos79_DEEP_SCOPE.md`,
  `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`,
  `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`,
  `tests/test_workspace_validation.py`.
- Why this work happened: Phase 22 needed to lock the expanded public source
  window and anti-cherry-pick protocol before any expanded capture, media
  review, claim ledger, market proxy mapping, or retrospective outcome analysis.
- Decisions applied: `D-025`, `D-026`, ADR-004 media evidence pipeline, Phase
  21 ready-gate rejection for the narrow source/window.
- Evidence collected: locked `bablos79` to the public Telegram window
  `2026-02-15T00:00:00+00:00` through `2026-05-15T23:59:59+00:00`; recorded
  inclusion/exclusion rules, public `/s/` capture method, draft-only media
  posture, Russian-first report language, claim boundary, and mandatory
  capture-before-outcome order. A stale phase-boundary guard test fixture was
  converted to derive the current phase from `docs/CODEX_PROMPT.md`, so future
  phase rollovers do not require hard-coded test updates. Baseline was restored
  and validated at 166 passing tests, 0 skipped; ruff passed.
- Follow-ups: run `SAS-DR-002: Expanded Public Capture Manifest` next for the
  locked 90-day window.
- Notes for next agent: do not narrow the corpus around known good examples.
  Preserve weak, ambiguous, contradicted, unresolved, and non-measurable rows
  as part of the product evidence.

### 2026-05-15 — SAS-DR-001..022 Planning — Deep Channel Retrospective Route

- Scope: `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`, `docs/tasks.md`,
  `docs/CODEX_PROMPT.md`, `README.md`, `PHASE_HANDOFF.md`,
  `AGENT_NOTES.md`, `MEMORY.md`, `ORCHESTRATOR_CHECKPOINT.md`,
  `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator paused Core, kept Trader and Signal active,
  and clarified that the current `bablos79` window is too narrow. The product
  must expand the public corpus, add image/OCR analysis, build a reviewed claim
  ledger, and compare measurable author claims to open market data.
- Decisions applied: `D-025`, ADR-004 media evidence pipeline, Phase 21 reject
  decision for the narrow source/window.
- Evidence collected: documentation-only roadmap/task update. No product code
  changed in this planning step.
- Follow-ups: start `SAS-DR-001: Deep Retrospective Scope Lock`.
- Notes for next agent: do not over-polish the current Phase 21 report. Fix the
  evidence problem by expanding the corpus and preserving weak/counterexamples
  alongside strong examples.

### 2026-05-14 — SAS-LIVE-001 — Real Media Scope And Evidence Intake

- Scope: `docs/pilot/bablos79_REAL_MEDIA_INTAKE.md`, `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`.
- Why this work happened: Phase 21 needed a concrete public/operator-authorized media intake plan before media acquisition, transcription, OCR, or media-backed report claims.
- Decisions applied: `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md` Phase 0; `docs/legal_risk_memo.md#media-evidence`; ADR-004 media evidence pipeline; current text-only report result showing 0 customer-report-eligible metric rows.
- Evidence collected: the workspace still has 60 public text captures but 0 local raw media files, 0 Telegram media file IDs, 0 transcript artifacts, 0 OCR artifacts, and 0 reviewed media refs. The plan records source-linked candidate blockers for `bablos79-10486` (voice context mentioned, no voice media link/file) and `bablos79-10465` (future video mentioned, no actual media item), excludes unlinked channel-level image/screenshot/chart/voice media, and blocks acquisition until the operator supplies exact public/operator-authorized media rows.
- Follow-ups: `SAS-LIVE-002` is blocked until the operator supplies at least one media row with source URL/ref, capture ID, source document ID, modality, authorization state, original media URL/file ID or local file path, expected report value, report gap, and retention preference.
- Notes for next agent: do not run acquisition, transcription, OCR, source joins, report generation, or media-backed customer claims from channel-level hearsay. Resume only when concrete linked media inputs exist.

### 2026-05-14 — SAS-LIVE-002/SAS-AF-008 — Media Route Completion And Ready Gate

- Scope: `workspace/media/bablos79/`, `docs/pilot/bablos79_REAL_MEDIA_ACQUISITION.md`, `docs/pilot/bablos79_MEDIA_MANIFEST.json`, `docs/pilot/bablos79_TRANSCRIPT_RUN.md`, `docs/pilot/bablos79_OCR_RUN.md`, `docs/pilot/bablos79_MEDIA_REVIEW.md`, `docs/pilot/bablos79_MULTIMODAL_SOURCE_PREVIEW.md`, `docs/retrieval_eval.md`, `docs/pilot/bablos79_MULTIMODAL_REVIEW_QUEUE.md`, `docs/pilot/bablos79_MULTIMODAL_OUTCOME_PREP.md`, `docs/pilot/reports/bablos79_MEDIA_BACKED_REPORT_V1.md`, `docs/audit/PHASE21_VALIDITY_REVIEW.md`, `docs/audit/PHASE21_ERROR_REGISTER.md`, `docs/pilot/bablos79_INTERNAL_DEMO_PACK.md`, `docs/pilot/bablos79_EXTERNAL_PILOT_READY_GATE.md`, `docs/tasks.md`, `docs/audit/MEDIA_EVAL.md`.
- Why this work happened: operator instructed the loop to continue without stopping; the public Telegram `/s/` route was used only for the approved public source to resolve the previous media-input blocker as far as possible.
- Decisions applied: ADR-004 media evidence pipeline; public-source-only legal memo; Phase 21 claim-safety and no-advice boundaries; RAG/source-join preservation contract.
- Evidence collected: acquired two public OGG voice files from `https://t.me/bablos79/10476` and `https://t.me/bablos79/10478`, registered two `MediaArtifact` rows, recorded transcript attempts as `skipped_provider_not_configured`, recorded OCR as `skipped_non_image_media`, reviewed zero usable transcript/OCR refs, joined zero media-derived refs, produced a multimodal review queue with 0 media-backed eligible rows, produced outcome prep with 0 market-data fetches and 0 metrics, and rendered a media-backed reject/limitation report. Validation: 163 passed, 0 skipped; ruff passes; pyright passes.
- Follow-ups: Phase 21 deep review/archive. Product decision is reject current `bablos79` source/window for external delivery; continue only with a stronger media/evidence input set or a different approved source.
- Notes for next agent: do not sell or present this as an external-ready sample. It is an internal reject-case demo proving the system refuses unsupported media-backed claims.

### 2026-05-12 — SAS-LIVE-PLAN — Real Media-Backed Report Loop

- Scope: `docs/MULTIMODAL_REPORT_DEVELOPMENT_PLAN.md`, `docs/tasks.md`, `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`, `README.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `MEMORY.md`.
- Why this work happened: operator clarified that the next loop must acquire and analyze real public audio/images, not merely document a text-only result.
- Decisions applied: ADR-004 media evidence pipeline; public-source-only legal memo; text-only Phase 21 report result showing 0 customer-report-eligible metric rows.
- Evidence collected: added a concrete `SAS-LIVE-001..009` task sequence from real media intake through acquisition, transcription, OCR, human media review, multimodal source join, multimodal extraction/review, outcome prep, media-backed report V1, and final manual validity/demo/ready gates.
- Follow-ups: run `SAS-LIVE-001: Real Media Scope And Evidence Intake` next.
- Notes for next agent: do not claim audio/image analysis until concrete public/operator-authorized media items are linked, acquired/registered, processed, and human-reviewed.

### 2026-05-12 — SAS-AF-004/SAS-AF-005 — Outcome Prep And First Report

- Scope: `src/signal_sandbox/artifact_pipeline.py`, `src/signal_sandbox/cli.py`, `tests/unit/test_artifact_pipeline.py`, `tests/integration/test_cli_smoke.py`, `docs/pilot/bablos79_OUTCOME_PREP.md`, `docs/pilot/bablos79_OUTCOME_PREP.json`, `docs/pilot/reports/bablos79_SIGNAL_REPORT_V1.md`, `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 21 needed outcome readiness and a first real report artifact after the review queue showed no complete metric-eligible rows.
- Decisions applied: artifact-first validation overlay; current operator direction to keep moving with the source and LLM/pseudo-label result; no-advice/no-future-claims boundary.
- Evidence collected: added `signal-sandbox snapshot` to write outcome prep registers from closed review queues and `signal-sandbox report` to render a V1 Markdown report from capture/review/outcome artifacts. Generated `bablos79` outcome prep has 60 assessed rows, 0 market-data fetches, 0 outcome metrics, 50 not-applicable rows, 7 unresolved insufficient-evidence rows, and 3 operator-review-required rows. Generated report is `docs/pilot/reports/bablos79_SIGNAL_REPORT_V1.md`; it is a text-only negative/limitation report with evidence appendix and canonical disclaimer. Validation after implementation: 163 passed, 0 skipped; `ruff check src/ tests/` passes; `pyright` passes.
- Follow-ups: run `SAS-AF-006: Manual Validity Review` next. Operator should evaluate whether the 3 ambiguous rows or any insufficient rows should be upgraded, rejected, or kept as limitations.
- Notes for next agent: the report is useful precisely because it says this capture window does not support defensible performance metrics. Do not add market-data snapshots until rows become metric-eligible.

### 2026-05-12 — SAS-AF-003 — Human Review Queue Closure

- Scope: `src/signal_sandbox/artifact_pipeline.py`, `src/signal_sandbox/cli.py`, `tests/unit/test_artifact_pipeline.py`, `tests/integration/test_cli_smoke.py`, `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.md`, `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.json`, `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 21 needed the validated capture/pseudo-label rows separated into report-input categories before outcome prep.
- Decisions applied: current operator direction to treat LLM/pseudo-label output as valid draft input for end evaluation; public-source-only and non-advice boundaries.
- Evidence collected: added `signal-sandbox review` to load the capture pack JSON and write Markdown/JSON queue closure artifacts. Generated `bablos79` closure has 60 rows: 50 `rejected_not_market_related`, 7 `insufficient_evidence`, 3 `ambiguous_needs_operator_review`, and 0 customer-report-eligible rows. No ledgers, outcomes, reports, or customer-facing claims were created. Validation: `tests/unit/test_artifact_pipeline.py` and `tests/integration/test_cli_smoke.py` pass; scoped ruff passes.
- Follow-ups: run `SAS-AF-004: Market Data Snapshot And Outcome Prep` next. It should produce an unresolved outcome register and avoid market-data fetches unless the operator upgrades rows to complete measurable candidates.
- Notes for next agent: do not force metrics from incomplete rows. A "no measurable rows in this window" artifact is acceptable and more useful than fabricated outcome stats.

### 2026-05-12 — SAS-AF-002 — Public Capture Pack

- Scope: `src/signal_sandbox/artifact_pipeline.py`, `src/signal_sandbox/cli.py`, `tests/unit/test_artifact_pipeline.py`, `tests/integration/test_cli_smoke.py`, `docs/pilot/bablos79_CAPTURE_PACK.md`, `docs/pilot/bablos79_CAPTURE_PACK.json`, `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 21 needed a real operator-inspectable capture pack before review closure, outcome prep, or report generation.
- Decisions applied: `SAS-AF-001` locked `bablos79`; public-source-only boundary; current operator direction to treat LLM/pseudo-label output as valid draft input for end evaluation.
- Evidence collected: added `signal-sandbox extract` to load public captures, validate optional pseudo-label spans against raw capture text, and write Markdown/JSON capture packs without creating ledgers, reports, outcomes, or customer-facing claims. Generated `bablos79` pack has 60 rows, source range `2026-04-27T07:12:22+00:00` through `2026-05-06T06:57:32+00:00`, status counts 50 `not_a_signal`, 7 `insufficient_fields`, and 3 `needs_review`. Validation: `tests/unit/test_artifact_pipeline.py` and `tests/integration/test_cli_smoke.py` pass; scoped ruff passes.
- Follow-ups: run `SAS-AF-003: Human Review Queue Closure` next using `docs/pilot/bablos79_CAPTURE_PACK.json` and the existing pseudo-label JSONL.
- Notes for next agent: use pseudo-label rows as valid draft input, but keep approved ledger/report claims separated until operator final evaluation. Media remains unavailable for this artifact.

### 2026-05-12 — SAS-AF-001 — Channel And Report Scope Lock

- Scope: `docs/ARTIFACT_VALIDATION_ROADMAP.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`.
- Why this work happened: Phase 21 needed a concrete source/report/legal/claim scope before capture-pack registration, review closure, outcome prep, or report generation.
- Decisions applied: artifact-first validation overlay; `docs/pilot/PILOT_SCOPE.md` deterministic first-source choice; public-source legal memo; Phase 20 media decision.
- Evidence collected: locked source to `https://t.me/bablos79`, source ID `bablos79`, existing 60 public text captures under `workspace/captures/bablos79/`, bounded capture period `2026-04-27T07:12:22+00:00` through `2026-05-06T06:57:32+00:00`, Russian-first text-only report scope, and explicit claim boundaries. Existing captures are sufficient to start `SAS-AF-002`, but not sufficient for customer-facing claims until human review and limitations are recorded.
- Follow-ups: run `SAS-AF-002: Public Capture Pack` next.
- Notes for next agent: do not add fresh scraping or media-backed customer claims. Treat media as out of scope unless the operator supplies reviewed public media evidence and updates the scope.

### 2026-05-09 — SAS-MEDIA-008 — Multimodal Coverage Pack And Decision Gate

- Scope: `docs/pilot/bablos79_MULTIMODAL_COVERAGE_PACK.md`, `docs/pilot/MEDIA_MODALITY_DECISION.md`, `docs/audit/STRATEGY_NOTE.md`, `docs/archive/PHASE20_REVIEW.md`, `docs/audit/AUDIT_INDEX.md`, `docs/audit/PHASE_REPORT_LATEST.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 20 needed a final coverage/decision gate and deep review/archive before any Phase 21 work.
- Decisions applied: ADR-004 media evidence pipeline; Phase 20 draft evidence boundaries; D-018 continuous phase loop.
- Evidence collected: multimodal coverage records 60 public text captures and 0 local media artifacts, transcript artifacts, OCR artifacts, multimodal joins, or ready-for-customer-sample rows. Decision is iterate internally and do not use media evidence in customer samples yet. Phase 20 deep review archived at `docs/archive/PHASE20_REVIEW.md`; Stop-Ship No; P0/P1/P2 all 0. Validation after phase: 157 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes.
- Follow-ups: pause implementation until operator supplies/authorizes public media or a new Phase 21 task graph is explicitly added.
- Notes for next agent: do not invent Phase 21. Run the Phase 20 media pipeline only on real public/operator-authorized media and keep all transcript/OCR evidence human-reviewed before customer-facing use.

### 2026-05-09 — SAS-MEDIA-007 — Multimodal SourceDocument Join

- Scope: `src/signal_sandbox/media/source_join.py`, `tests/unit/test_multimodal_source_join.py`, `docs/specs/SOURCE_CORPUS.md`, `docs/specs/MEDIA_ARTIFACTS.md`, `src/signal_sandbox/media/__init__.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 20 needed transcript/OCR refs joined into source-corpus records without changing canonical text captures.
- Decisions applied: ADR-004 draft evidence boundary; `SAS-MEDIA-006` OCR boundary; `SourceDocument` evidence-preservation contract.
- Evidence collected: added `join_multimodal_source_document()` to return enriched `SourceDocument` copies with additive media/transcript/OCR refs while preserving original text, evidence URL, and text hash. The helper validates source ID, capture ID, source-document ID, media ID, and source media checksum before adding refs. Validation after task: 157 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-MEDIA-008: Multimodal Coverage Pack And Decision Gate`, then Phase 20 deep review/archive/doc update before any Phase 21 work.
- Notes for next agent: final coverage/decision must show that current local transcript/OCR coverage is still zero unless real media artifacts are supplied/reviewed; customer-facing report use remains blocked without human-approved evidence coverage.

### 2026-05-09 — SAS-MEDIA-006 — OCR Draft Adapter

- Scope: `src/signal_sandbox/media/ocr.py`, `tests/unit/test_ocr_draft_adapter.py`, `docs/specs/MEDIA_ARTIFACTS.md`, `docs/audit/MEDIA_EVAL.md`, `src/signal_sandbox/media/__init__.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 20 inventory approved OCR draft extraction for image/screenshot text only.
- Decisions applied: `SAS-MEDIA-005` inventory decision; ADR-004 media evidence pipeline; PSR-3 draft-output boundary; PSR-11 no forward-looking claims.
- Evidence collected: added `run_ocr_draft()` with an injected OCR client, image/screenshot modality guard, draft OCR JSON output, provider/model/provenance/checksums, bounding metadata, `draft_pending_review` status, pending reviewer ID, and review-required notes. Approved chart claims are refused; chart labels, price levels, or trade interpretations can only be stored as review-required notes. Validation after task: 154 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS. Media eval updated in `docs/audit/MEDIA_EVAL.md`.
- Follow-ups: run `SAS-MEDIA-007: Multimodal SourceDocument Join`.
- Notes for next agent: source joins must preserve original `SourceDocument.text`, `evidence_url`, and `text_sha256` exactly. Transcript/OCR refs are additive draft evidence, not truth-artifact mutations.

### 2026-05-09 — SAS-MEDIA-005 — Image Evidence Inventory And OCR Scope

- Scope: `docs/pilot/bablos79_MEDIA_INVENTORY.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 20 needed an inventory/scope gate before implementing OCR or image annotation.
- Decisions applied: ADR-004 media evidence pipeline; `SAS-MEDIA-005` gate; PSR-3 draft-output boundary; PSR-11 no forward-looking claims.
- Evidence collected: current local evidence has 60 public text captures and no local raw media files, Telegram media IDs, transcript artifacts, or OCR artifacts. The inventory records channel-level image/screenshot and voice/audio gaps plus text references in `bablos79-10486` and `bablos79-10465`. It approves draft OCR extraction for image/screenshot text only, keeps chart/image interpretation manual-review-only, and forbids chart-derived trading claims. Review skipped as doc-only.
- Follow-ups: run `SAS-MEDIA-006: OCR Draft Adapter`.
- Notes for next agent: OCR output must be draft-pending-review only. Chart labels, price levels, and trade claims can be captured only as review-required notes, not approved truth or customer-facing claims.

### 2026-05-09 — SAS-MEDIA-004 — Whisper Transcript Draft Adapter

- Scope: `src/signal_sandbox/media/transcription.py`, `tests/unit/test_whisper_transcript_adapter.py`, `docs/specs/MEDIA_ARTIFACTS.md`, `docs/audit/MEDIA_EVAL.md`, `src/signal_sandbox/media/__init__.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 20 needed a gated managed Whisper-style draft transcription path over local voice artifacts after Telegram voice acquisition.
- Decisions applied: ADR-004 media evidence pipeline; PSR-3 LLM output is never truth; PSR-4 cost/approval posture; T0 runtime guardrails.
- Evidence collected: added `run_whisper_transcription()` with `SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION=1` plus per-run approval before invoking an injected fakeable client. Successful runs write draft transcript JSON with media ID, transcript ID, provider/model, transcript SHA-256, source media checksum, status `draft_pending_review`, reviewer ID `pending`, review-required state, and raw-media retention action. Provider failures return typed failure status and create no transcript. Validation after task: 151 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS. Media eval recorded in `docs/audit/MEDIA_EVAL.md`.
- Follow-ups: run `SAS-MEDIA-005: Image Evidence Inventory And OCR Scope`.
- Notes for next agent: transcription output is draft evidence only. Do not route transcripts or OCR/image outputs to approved MarketIdea rows, ledgers, reports, metrics, or customer-facing claims without human review.

### 2026-05-09 — SAS-MEDIA-003 — Telegram Voice Acquisition Adapter

- Scope: `src/signal_sandbox/media/telegram_voice.py`, `tests/unit/test_telegram_voice_acquisition.py`, `docs/specs/MEDIA_ARTIFACTS.md`, `src/signal_sandbox/media/__init__.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 20 needed Telegram voice acquisition before managed Whisper transcription, while preserving ADR-004 public/operator-authorized and draft-evidence boundaries.
- Decisions applied: ADR-004 media evidence pipeline; PSR-1 public-source-only; T0 runtime guardrails; Dream_Motif_Interpreter voice download pattern adapted with injected clients and no domain-model reuse.
- Evidence collected: added `acquire_telegram_voice_artifact()` with an injected async Telegram client, deterministic media ID, `.ogg.part` download then checksum/rename, `MediaArtifact` return, legal media authorization checks, allowed public/operator-forwarded states, typed unauthorized/download errors, and partial-file cleanup on download failure. Validation after task: 147 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-MEDIA-004: Whisper Transcript Draft Adapter`.
- Notes for next agent: no transcription exists yet. `SAS-MEDIA-004` must keep double gates, fake clients in CI, draft transcript status, raw-media retention/cleanup policy, and no approved ledger/report/customer-claim path.

### 2026-05-09 — SAS-MEDIA-002 — MediaArtifact Schema And Manifest

- Scope: `src/signal_sandbox/media/artifact.py`, `src/signal_sandbox/media/__init__.py`, `tests/unit/test_media_artifact.py`, `docs/specs/MEDIA_ARTIFACTS.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 20 needed deterministic local media metadata before Telegram voice acquisition, Whisper transcription, OCR, or multimodal source-document joins.
- Decisions applied: ADR-004 media evidence pipeline; PSR-1 public-source-only; PSR-3 LLM output is never truth; T0 runtime guardrails.
- Evidence collected: added strict Pydantic `MediaArtifact` metadata with source/capture/source-document linkage, source timestamp, modality, original URL/file ID, local path, SHA-256, MIME type, optional duration/image dimensions, retention state, creation timestamp, and draft transcript/OCR refs. `build_media_manifest()` sorts by source timestamp, source-document ID, and media ID and writes deterministic Markdown/JSON. Extra provider-output fields are forbidden. Validation after task: 144 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes.
- Follow-ups: run `SAS-MEDIA-003: Telegram Voice Acquisition Adapter`.
- Notes for next agent: `SAS-MEDIA-003` may download Telegram voice with an injected fakeable client and record `MediaArtifact` metadata only. Do not add transcription, OCR, provider-side transcript storage, approved-ledger writes, metrics, reports, or customer claims.

### 2026-05-09 — SAS-MEDIA-001 — Media Scope ADR And Legal Addendum

- Scope: `docs/adr/ADR-004-media-evidence-pipeline.md`, `docs/legal_risk_memo.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `docs/pilot/MEDIA_MODALITY_DEVELOPMENT_PLAN.md`.
- Why this work happened: Phase 20 needed a legal/architecture gate before adding media artifact schemas, Telegram voice acquisition, Whisper transcription, image/OCR inventory, or OCR draft adapters.
- Decisions applied: D-023, D-024; PSR-1 public-source-only; PSR-3 LLM output is never truth; ADR-002 deterministic-truth boundary; T0 runtime guardrails.
- Evidence collected: ADR-004 references the Dream_Motif_Interpreter mechanics files for Telegram `voice.file_id` download, media-event sequencing, acknowledgement/enqueue flow, managed Whisper boundary, provider failure handling, and raw-media cleanup. The legal memo now has explicit voice/audio/image/OCR posture, allowed public/operator-forwarded capture, forbidden private/authenticated sources, raw-media retention, and deletion triggers. Validation after task: 141 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes.
- Follow-ups: run `SAS-MEDIA-002: MediaArtifact Schema And Manifest` next. Keep it metadata-only with no Telegram, Whisper, OCR, network, provider, approved-ledger, or customer-claim behavior.
- Notes for next agent: transcript/OCR output is draft evidence only and review-required. Raw media is temporary local operational data unless the operator explicitly retains a local evidence snapshot under the accepted retention policy.

### 2026-05-09 — SAS-MI-019 — Reviewer Coverage Export Pack

- Scope: `src/signal_sandbox/market_ideas/review_coverage.py`, `tests/unit/test_review_coverage_export.py`, `docs/pilot/bablos79_REVIEW_COVERAGE_PACK.md`, `src/signal_sandbox/market_ideas/__init__.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: ADR-003 selected deterministic reviewer/export improvements as the next tool because the current bottleneck is reviewed evidence coverage across the 60 public `bablos79` captures.
- Decisions applied: ADR-003; ADR-002 deterministic-truth boundary; PSR-1 public-source-only; PSR-11 no forward-looking claims.
- Evidence collected: added a deterministic coverage exporter that produces one row per `SourceDocument`, sorted by timestamp/document/capture ID, with MarketIdea review status, evidence refs, deterministic outcome status, missing fields, reviewer action, and reviewer ID. Status buckets separate `needs_evidence_review`, `needs_metric_snapshot`, `needs_interpretation_review`, and `ready_for_customer_sample`. The artifact records 60 public captures as internal review support with no customer-facing claims. Validation after task: 141 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes.
- Follow-ups: no further task is defined in `docs/tasks.md`; operator/product decision is required before adding another phase.
- Notes for next agent: do not treat coverage rows as approved ledger truth or customer-report claims. Any new modality/provider/tool work requires a new scoped task and, if it changes runtime/capability boundaries, an ADR.

### 2026-05-09 — SAS-MI-018 — Modality And Tooling Scope ADR

- Scope: `docs/adr/ADR-003-channel-specific-tools.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/IMPLEMENTATION_JOURNAL.md`.
- Why this work happened: Phase 19 needed to decide which channel-specific tool is justified by current evidence before adding any modality/provider work.
- Decisions applied: ADR-002 deterministic-truth boundary; Phase 18 decision gate; PSR-1 public-source-only; PSR-11 no forward-looking claims.
- Evidence collected: ADR-003 compares voice transcription, OCR/image annotation, news/catalyst linking, fund/equity data, reviewer UI/export improvements, and new channel lexicons against the measured bottleneck. It chooses reviewer/export improvements and adds `SAS-MI-019: Reviewer Coverage Export Pack` as the narrow acceptance-tested follow-up. No provider dependency or external service was added. Validation after task: 138 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes.
- Follow-ups: run `SAS-MI-019: Reviewer Coverage Export Pack` next.
- Notes for next agent: the selected next work is deterministic local export only. Do not implement voice/OCR/news/fund data providers, private scraping, broker integration, public leaderboard, marketplace, or forward-looking claims.

### 2026-05-09 — SAS-MI-017 — Sellability And Scope Decision Gate

- Scope: `docs/pilot/AUTHOR_MARKET_REPORT_DECISION.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `docs/audit/AUDIT_INDEX.md`, `docs/archive/PHASE18_REVIEW.md`.
- Why this work happened: Phase 18 needed an explicit decision on whether Author Market Report V0 is ready to sell, should iterate internally, should narrow, or should pause before Phase 19 tool/modality scoping.
- Decisions applied: ADR-002 deterministic-truth boundary; PSR-1 public-source-only; PSR-6 canonical disclaimer; PSR-11 no forward-looking claims; D-018 continuous phase loop.
- Evidence collected: decision gate records verdict, evidence coverage, customer-feedback status, payment-signal status, implementation risk, exact next bottleneck, and forbidden scope. Verdict is iterate internally, do not sell yet. Validation after task: 138 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Phase 18 deep review archived at `docs/archive/PHASE18_REVIEW.md` with P0/P1/P2 all 0.
- Follow-ups: run `SAS-MI-018: Modality And Tooling Scope ADR` next.
- Notes for next agent: Phase 19 is approved only as a scoping ADR. The measured bottleneck is thin evidence coverage across the 60 public `bablos79` captures, not report formatting. Keep private scraping, live trading, broker integration, public leaderboard expansion, marketplace expansion, and forward-looking claims forbidden.

### 2026-05-09 — SAS-MI-016 — Author Market Report Template

- Scope: `src/signal_sandbox/reports/author_market.py`, `tests/unit/test_author_market_report.py`, `docs/pilot/reports/bablos79_AUTHOR_MARKET_REPORT_V0.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 18 needed a customer-facing Author Market Report V0 template after the bounded internal analyst memo foundation.
- Decisions applied: ADR-002 deterministic-truth boundary; PSR-6 canonical disclaimer; PSR-11 no forward-looking claims.
- Evidence collected: renderer includes channel overview, data coverage, idea taxonomy, deterministic outcomes, evidence examples, limitations, and the canonical non-advice disclaimer. It raises `MissingReportProvenance` when source-document or market-snapshot provenance is absent, and separates trade setup metrics from broader commentary metrics. Validation after task: 138 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-MI-017: Sellability And Scope Decision Gate` next.
- Notes for next agent: the decision gate should cite the V0 report artifact, evidence coverage limits, customer/payment status, and implementation risk before approving any next scope.

### 2026-05-09 — SAS-MI-015 — Internal Analyst Memo Export

- Scope: `src/signal_sandbox/batch_analyst/memo.py`, `tests/unit/test_analyst_memo_export.py`, `docs/pilot/BABLOS79_INTERNAL_MARKET_MEMO.md`, `docs/audit/AGENTIC_EVAL.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 17 needed an internal analyst memo export after the bounded batch analyst contract.
- Decisions applied: ADR-002 bounded Agentic profile; deterministic-truth boundary; internal-only analyst output until human review.
- Evidence collected: memo model validates internal-only usage and interpretive-claim citations against retrieved document IDs or deterministic metric IDs. Validation after task: 135 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Agentic evaluation recorded in `docs/audit/AGENTIC_EVAL.md`. Phase 17 deep review archived at `docs/archive/PHASE17_REVIEW.md` with P0/P1/P2 all 0.
- Follow-ups: run `SAS-MI-016: Author Market Report Template` next.
- Notes for next agent: customer-facing report code must keep source-document and market-snapshot provenance mandatory, include the canonical non-advice guardrails, and keep explicit trade setup performance separate from broader commentary behavior.

### 2026-05-07 — Bootstrap — Phase 1 Governance Package

- Scope: `docs/ARCHITECTURE.md`, `docs/spec.md`, `docs/tasks.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, `docs/prompts/`, `docs/audit/`, `.github/workflows/ci.yml`, `.claude/commands/orchestrate.md`.
- Why this work happened: project bootstrap via the AI Workflow Playbook `/bootstrap-new` flow.
- Decisions applied: D-001..D-012 (initial decision log; see `docs/DECISION_LOG.md`).
- Evidence collected: brief is `templates/PROJECT_BRIEF.md`; operator answers locked the five bootstrap clarifying questions on 2026-05-07.
- Follow-ups: SAS-001 (paid pilot demand), SAS-002 (legal/risk memo) must complete and be acknowledged in `docs/CODEX_PROMPT.md §Phase 0 Gate Status` before T01 begins.
- Notes for next agent: Heavy tasks are T12 (outcome matcher), T14 (report renderer), T20 (LLM extraction adapter). The reproducibility contract (PSR-2) and the LLM-non-truth rule (PSR-3) are load-bearing — preserve at every adapter boundary.

### 2026-05-07 — Phase 9 Planning — Customer-Backed Telegram Pilot Loop

- Scope: `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `docs/PILOT_DEVELOPMENT_LOOP_RU.md`, `docs/pilot/README.md`.
- Why this work happened: the operator clarified that the three Telegram groups in `docs/PILOT_LOG.md` were provided by potential customers and the next loop will be run through `prompts/ORCHESTRATOR.md`, so the pilot must be represented in the orchestrator-readable task graph, not only in a strategy report.
- Decisions applied: D-013.
- Evidence collected: `STARTUP_PRESSURE_TEST_RU.md` pressure test; operator clarification in chat; existing pilot sources in `docs/PILOT_LOG.md`.
- Follow-ups: run `SAS-PILOT-001: Pilot Scope` next. Start with `docs/pilot/PILOT_SCOPE.md`, then `SAS-PILOT-002: Methodology V0`.
- Notes for next agent: Phase 9 is validation-first. Do not modify product code until the pilot decision gate identifies a measured bottleneck. Do not widen into Telegram bot, private scraping, public SaaS, leaderboard, marketplace, copy trading, broker integration, or Entropy Core feed.

### 2026-05-07 — SAS-PILOT-001 — Pilot Scope

- Scope: `docs/pilot/PILOT_SCOPE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `tests/test_workspace_validation.py`.
- Why this work happened: Phase 9 needed a concrete pilot scope before capture, extraction, or report work could start.
- Decisions applied: D-013; public-source-only and validation-first boundaries from `docs/IMPLEMENTATION_CONTRACT.md` and `docs/PILOT_DEVELOPMENT_LOOP_RU.md`.
- Evidence collected: pre-task baseline restored to 84 passed, 0 skipped after updating the phase-boundary guard test to match current Phase 9 state; `ruff check src/ tests/` passes.
- Follow-ups: run `SAS-PILOT-002: Methodology V0` next, using `docs/pilot/PILOT_SCOPE.md` as the first context reference.
- Notes for next agent: first source is `https://t.me/bablos79` by deterministic PILOT_LOG ordering, not expected performance. Default target is 30-50 defensible signal records where available. If public captures are missing or insufficient, write blocker/limitation rows instead of inventing posts or signals.

### 2026-05-07 — SAS-PILOT-002 — Methodology V0

- Scope: `docs/pilot/METHODOLOGY_V0.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the first source audit needed fixed capture, extraction, outcome, provenance, and report guardrails before any public posts are recorded.
- Decisions applied: D-013; PSR-1 public-source-only, PSR-2 reproducibility, PSR-3 LLM output is never truth, PSR-6 disclaimer integrity, and PSR-11 no forward-looking claims.
- Evidence collected: `docs/pilot/METHODOLOGY_V0.md` covers required capture fields, signal qualification, statuses, deterministic outcome/exclusion semantics, price provenance, and non-advice / historical-only guardrails. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-003: First Source Capture Plan And Log` next for `https://t.me/bablos79`.
- Notes for next agent: do not fabricate public posts. If the workspace has no real captures, create the capture log with `pending-operator-input` rows and explicit blocker/status definitions.

### 2026-05-07 — SAS-PILOT-003 — First Source Capture Plan And Log

- Scope: `docs/pilot/CAPTURE_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the first source audit needed a public/operator-supplied capture structure before manual extraction could begin.
- Decisions applied: D-013; PSR-1 public-source-only boundary and `docs/pilot/METHODOLOGY_V0.md` capture field requirements.
- Evidence collected: no real `bablos79` captures are present in the workspace; `docs/pilot/CAPTURE_LOG.md` initializes the queue with `pending-operator-input`, status definitions, required evidence fields, and skip/block reason codes. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-004: First Source Manual Extraction Log` next. It should state extraction is blocked until the operator supplies real public captures.
- Notes for next agent: do not invent `public_url`, raw text, hashes, or signal candidates. Keep any rows without real evidence as `pending-operator-input`.

### 2026-05-07 — SAS-PILOT-004 — First Source Manual Extraction Log

- Scope: `docs/pilot/EXTRACTION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the pilot needed a manual extraction log and blocker state before any report artifact could be produced.
- Decisions applied: D-013; `docs/pilot/METHODOLOGY_V0.md` extraction statuses and human-review boundaries.
- Evidence collected: `docs/pilot/CAPTURE_LOG.md` has no `captured` rows, so `docs/pilot/EXTRACTION_LOG.md` records `pending_capture=1`, all approved/ambiguous/excluded counts as 0, and an explicit blocker on operator-supplied public captures. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-005: First Source Report V0` next. Because no captures/extraction exist, write a blocked-report memo instead of report metrics.
- Notes for next agent: do not create outcomes, win/loss statistics, or signal examples without real captured public posts and human-reviewed extraction rows.

### 2026-05-07 — SAS-PILOT-005 — First Source Report V0

- Scope: `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 9 needed a customer-readable report artifact or honest blocker memo for the first source.
- Decisions applied: D-013; non-advice/historical-only and no-forward-looking boundaries from `docs/IMPLEMENTATION_CONTRACT.md`.
- Evidence collected: no captures, extraction rows, approved ledger, price snapshot, or outcomes exist. The blocked-report memo records zero counts, blocker, limitations, and next required operator inputs. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-006: Customer Feedback And Payment Signal Log` next. Since no customer-ready report was delivered, feedback/payment rows should be pending.
- Notes for next agent: do not record payment success, customer decision impact, or report acceptance without real customer behavior.

### 2026-05-07 — SAS-PILOT-006 — Customer Feedback And Payment Signal Log

- Scope: `docs/pilot/CUSTOMER_FEEDBACK.md`, `docs/pilot/PAYMENT_SIGNAL_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 9 needed customer feedback and payment-signal structures before the repeat/automation decision gate.
- Decisions applied: D-013; validation-first rule that customer/payment behavior, not engineering completion, decides next scope.
- Evidence collected: no customer review or payment signal exists because the first report is blocked on captures. Feedback/payment logs contain pending rows, past-behavior questions, payment status definitions, refusal reasons, and Telegram-delivery guardrails. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run `SAS-PILOT-007: Repeat Or Automate Decision` next. Current evidence should lead to "stop/defer until public captures are supplied"; no automation is justified.
- Notes for next agent: do not mark pilot success without paid/deposit/repeat/referral behavior or a real customer decision impact.

### 2026-05-07 — SAS-PILOT-007 — Repeat Or Automate Decision

- Scope: `docs/pilot/PILOT_DECISION.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 9 needed an explicit decision gate after pilot logs showed whether to repeat, automate, pivot, or stop.
- Decisions applied: D-014.
- Evidence collected: the decision cites scope, methodology, capture log, extraction log, blocked-report memo, customer feedback log, and payment signal log. Current evidence shows no real captures, no extraction, no customer decision impact, and no payment signal. Validation remains 84 passed, 0 skipped; ruff and pyright pass.
- Follow-ups: run Phase 9 deep review/archive. After that, wait for operator-supplied public captures before reopening the pilot loop.
- Notes for next agent: no new engineering phase is approved. Do not continue to remaining sources or automation until `bablos79` is unblocked or formally blocked with a concrete reason.

### 2026-05-07 — Public Capture Parse — bablos79

- Scope: `workspace/captures/bablos79/`, `docs/pilot/bablos79_CAPTURE_MANIFEST.json`, `docs/pilot/CAPTURE_LOG.md`, `docs/pilot/EXTRACTION_LOG.md`, `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md`, `docs/pilot/PILOT_DECISION.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator instructed Codex to parse the public first source instead of waiting for manually supplied capture files.
- Decisions applied: D-014 updated — continue manual extraction for the captured first-source batch; defer automation.
- Evidence collected: fetched public unauthenticated Telegram `/s/` HTML pages for `bablos79`, captured 60 text posts into `workspace/captures/bablos79/`, and validated them with `load_captures(Path("workspace"), "bablos79")` returning 60 posts with matching hashes.
- Follow-ups: manually classify the 60 captures in `docs/pilot/EXTRACTION_LOG.md`; do not generate approved records, outcomes, or report metrics until extraction and human review are complete.
- Notes for next agent: capture blocker is cleared for the first batch, but there is still no approved ledger and no customer/payment signal. Automation remains deferred.

### 2026-05-07 — Phase 10 Planning — Draft Extraction Assistant

- Scope: `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator approved building a clear parser/automatic extraction path after the first public capture batch existed.
- Decisions applied: D-015, D-016.
- Evidence collected: initial Phase 10 task graph required seed labels, offline frontier-model author lexicon discovery with human approval, deterministic parser implementation, draft export, extraction-log merge, and evaluation before any next automation decision.
- Follow-ups: superseded on 2026-05-08 by the machine-first pseudo-label bootstrap plan.
- Notes for next agent: this seed-label-first plan is historical context only; use the 2026-05-08 roadmap entry below.

### 2026-05-08 — Audit-Grade Automation Roadmap

- Scope: `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`, `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`.
- Why this work happened: operator clarified that the next loop should avoid manual seed labeling and automate the first pass, while keeping audit-grade boundaries through validators and exception review.
- Decisions applied: D-017; D-015 superseded.
- Evidence collected: roadmap now defines phases A-M from data foundation through confidence-gated automation; Phase 10 now starts with `SAS-AUTO-001: Machine-First Pseudo-Label Bootstrap`.
- Follow-ups: run `SAS-AUTO-001` to create `docs/pilot/bablos79_PSEUDO_LABELS.md` and `workspace/extraction/bablos79_pseudo_labels.jsonl` for all 60 captures.
- Notes for next agent: do not start with `BABLOS79_LABEL_SEED.md`; manual work is now exception review, not seed labeling. Parser code starts after pseudo-labels and `docs/pilot/bablos79_AUTHOR_PROFILE.md` exist.

### 2026-05-08 — Continuous Phase Loop Contract

- Scope: `docs/prompts/ORCHESTRATOR.md`, `docs/CODEX_PROMPT.md`, `docs/DECISION_LOG.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`.
- Why this work happened: operator clarified that the AI development loop must not stop between phases after deep review; it should continue after review/archive/doc update.
- Decisions applied: D-018.
- Evidence collected: `docs/prompts/ORCHESTRATOR.md` now has a Phase Continuation Contract and `Step 6.7` requiring next-task advancement after phase review unless a concrete stop condition exists.
- Follow-ups: when Phase 10 finishes, run deep review, archive, update docs, then immediately advance to the next task/phase and continue the loop.
- Notes for next agent: do not leave the project in a "review complete, waiting" state unless a named blocker or explicit user pause exists.

### 2026-05-08 — SAS-AUTO-001 — Machine-First Pseudo-Label Bootstrap

- Scope: `docs/pilot/bablos79_PSEUDO_LABELS.md`, `workspace/extraction/bablos79_pseudo_labels.jsonl`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`, `tests/test_workspace_validation.py`.
- Why this work happened: Phase 10 starts with machine-first pseudo-labels over all 60 local public captures so manual review can focus on exceptions rather than seed-labeling every row.
- Decisions applied: D-017; draft-only / no-LLM-truth boundary from `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md` and `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`.
- Evidence collected: generated 60 JSONL pseudo-label rows matching `workspace/captures/bablos79/`; distribution is 50 `not_a_signal`, 7 `insufficient_fields`, and 3 `needs_review`. Validation confirmed required JSONL fields, `draft_only=true`, `approval_state="unapproved"`, matching capture IDs, and evidence-span text present in raw captures. Updated the phase-boundary guard test from Phase 9->10 to Phase 10->11 after advancing project state. Baseline remains 84 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-AUTO-001B: Author Lexicon And Draft Profile Discovery` next, using `docs/pilot/bablos79_PSEUDO_LABELS.md`, `workspace/extraction/bablos79_pseudo_labels.jsonl`, and `workspace/captures/bablos79/`.
- Notes for next agent: do not treat pseudo-labels as approved extraction truth. Parser implementation remains blocked until the author profile and lexicon draft exist.

### 2026-05-08 — SAS-AUTO-001B — Author Lexicon And Draft Profile Discovery

- Scope: `docs/pilot/bablos79_AUTHOR_PROFILE.md`, `workspace/lexicons/bablos79_lexicon_draft.json`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needs an author-specific draft lexicon/profile before deterministic parser implementation can use pseudo-label evidence safely.
- Decisions applied: D-017; `SAS-AUTO-001B` contract that frontier-model/profile output is offline analysis only and cannot decide approved signal truth.
- Evidence collected: generated 32 evidence-cited candidates grouped by category. Profile-state distribution is 17 `accepted_for_draft`, 9 `needs_review`, and 6 `excluded`. Validation confirmed every candidate has term, category, evidence_capture_ids, evidence_excerpts, false_positive_risk, confidence, and profile_state with no invalid state values. Baseline remains 84 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-AUTO-002: Deterministic Validators And Draft Parser Library` next. Use only static `accepted_for_draft` entries for parser draft behavior; `needs_review` and `excluded` entries must not become automatic parser truth.
- Notes for next agent: the next task is the first Phase 10 product-code task. Keep it pure/local with no CLI wiring, network calls, runtime LLM calls, or ledger writes.

### 2026-05-08 — SAS-AUTO-002 — Deterministic Validators And Draft Parser Library

- Scope: `src/signal_sandbox/extraction/draft_validation.py`, `src/signal_sandbox/extraction/draft_parser.py`, `tests/unit/test_draft_validation.py`, `tests/unit/test_draft_parser.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed pure/local code to verify pseudo-label evidence and turn static accepted profile terms into review-only draft suggestions before any export artifact is generated.
- Decisions applied: D-017; PSR-3 LLM output is never truth; PSR-8 evidence field preservation; T0 runtime boundary.
- Evidence collected: added `validate_pseudo_label()` with rejection tests for unsupported evidence/candidate fields and `parse_draft()` with tests for structured output, evidence preservation, deterministic repeated classification, and review-required complete candidates. Full validation: 90 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-AUTO-003: Draft Export Artifact` next to export parser suggestions for all captured `bablos79` posts into `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`.
- Notes for next agent: `draft_parser.py` intentionally does not approve records or write ledgers. Keep export rows reviewer_id=`pending` and deterministic.

### 2026-05-08 — SAS-AUTO-003 — Draft Export Artifact

- Scope: `src/signal_sandbox/extraction/draft_export.py`, `tests/unit/test_draft_export.py`, `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed a reviewable export of parser suggestions for every captured post before exception review can replace full manual labeling.
- Decisions applied: D-017; draft-only boundary; no approved ledger writes before human review.
- Evidence collected: exported 60 rows sorted by source timestamp and capture_id. Suggested status distribution is 43 `not_a_signal`, 16 `insufficient_fields`, and 1 `needs_review`; every row has reviewer_id=`pending`. No ledger directory/files were created. Full validation: 93 passed, 0 skipped; `ruff check src/ tests/` passes; `.venv/bin/pyright` passes. Light review PASS.
- Follow-ups: run `SAS-AUTO-004: Exception Review Queue And Extraction Log Merge` next to update `docs/pilot/EXTRACTION_LOG.md` and create `docs/pilot/bablos79_REVIEW_QUEUE.md`.
- Notes for next agent: keep draft suggested statuses separate from final extraction statuses. Do not convert any row to `approved`.

### 2026-05-08 — SAS-AUTO-004 — Exception Review Queue And Extraction Log Merge

- Scope: `docs/pilot/bablos79_REVIEW_QUEUE.md`, `docs/pilot/EXTRACTION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed to turn draft parser output into a targeted human review surface while preserving final extraction status as pending.
- Decisions applied: D-017; draft-only boundary; no approved ledger writes before human review.
- Evidence collected: `docs/pilot/EXTRACTION_LOG.md` now has separate draft suggested status counts and one draft suggestion row per capture. `docs/pilot/bablos79_REVIEW_QUEUE.md` has 23 rows selected by exception status, confidence `<0.50`, customer-facing asset candidates, trade-management ambiguity, and deterministic non-signal sampling. All reviewer IDs remain `pending`; final status counts remain 0 approved / 60 pending manual extraction. Baseline remains 93 passed, 0 skipped.
- Follow-ups: run `SAS-AUTO-005: Draft Extraction Evaluation And Next Decision` next.
- Notes for next agent: evaluation must cite row counts, review queue size, false-positive risks, and the automation boundary. Do not approve bot/private scraping/marketplace/copy-trading/LLM-truth expansion.

### 2026-05-08 — SAS-AUTO-005 — Draft Extraction Evaluation And Next Decision

- Scope: `docs/pilot/AUTO_EXTRACTION_EVAL.md`, `docs/pilot/PILOT_DECISION.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 10 needed a decision gate to decide whether the machine-first draft helper should be kept, improved, discarded, or replaced by manual-only extraction.
- Decisions applied: D-017; no scope expansion without measured customer/payment evidence.
- Evidence collected: `docs/pilot/AUTO_EXTRACTION_EVAL.md` records Date, Eval Source, row counts, suggested-status distribution, 23-row review queue size, false-positive notes, useful suggestions, and operator-review implications. `docs/pilot/PILOT_DECISION.md` now says keep the draft helper for internal exception review only. Baseline remains 93 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 10 deep review/archive/doc update. There is no next engineering task in `docs/tasks.md`; the next product action after review is human exception review of 23 queued rows plus sampled verification of 37 non-queued rows.
- Notes for next agent: do not start a new engineering phase unless human review, report feedback, or payment evidence identifies a measured bottleneck.

### 2026-05-09 — Phase 11+ Planning — Author Market Intelligence Roadmap

- Why this work happened: operator review of the first `bablos79` group showed that the channel is not only explicit trade signals; it also contains broad market regime commentary, event/news analysis, voice-message analysis behavior, watchlists, and occasional visible trade entries. The product should evaluate how those ideas behaved against market data rather than force every post into the old signal-only model.
- Decisions applied: D-019 and D-020. Phase 10 artifacts remain useful and become the first channel profile/corpus seed. RAG, Planning, and Agentic work is planned but still gated by `SAS-MI-001` before implementation.
- Evidence collected: created `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md`; appended Phases 11-19 and tasks `SAS-MI-001..018` to `docs/tasks.md`; updated `README.md`, `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `MEMORY.md`, and `AGENT_NOTES.md` for the new stage. Validation after planning docs: 94 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-001: Author Market Intelligence Architecture ADR` next. Do not implement vector storage, embeddings, market-data expansion, or batch-agent code before the ADR updates capability profiles and runtime/storage boundaries.

### 2026-05-09 — SAS-MI-001 — Author Market Intelligence Architecture ADR

- Scope: `docs/adr/ADR-002-author-market-intelligence.md`, `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 11 needed an explicit architecture gate before RAG, vector storage, market-data expansion, or batch-agent work could begin.
- Decisions applied: D-021. ADR-002 activates RAG for local cited context only, activates Agentic only for a bounded internal batch analyst, keeps Tool-Use and Planning OFF, keeps runtime T0, and selects local DuckDB plus local vector/index sidecar files as the first retrieval substrate.
- Evidence collected: ADR-002 cites the Author Market Intelligence roadmap and Phase 10 `bablos79` artifacts as the initial corpus/profile seed. Architecture capability profiles now match the ADR. No product code, embeddings, vector storage, market-data expansion, approved ledger writes, or batch-agent code were added. Validation after doc gate: 94 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-002: MarketIdea Schema And Metrics Contract` next. Keep deterministic market data as the only source of prices, returns, approved records, and outcome metrics.

### 2026-05-09 — SAS-MI-002 — MarketIdea Schema And Metrics Contract

- Scope: `docs/specs/MARKET_IDEA_SCHEMA.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 11 needed a schema and deterministic metric contract before Phase 12 adds asset resolution code.
- Decisions applied: ADR-002 deterministic-truth boundary; RAG context-only boundary; existing `SignalRecord` and outcome matcher semantics remain the strict trade/evaluation baseline.
- Evidence collected: created `docs/specs/MARKET_IDEA_SCHEMA.md` with required and optional fields, enum values, evidence-span rules, approval states, draft-only labels, deterministic horizons, metric outputs, review queue policy, examples, and SignalRecord compatibility rules. No product code, market-data fetch, embeddings, vector storage, approved ledger writes, or batch-agent code were added. Validation after spec: 94 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 11 strategy/deep review/archive before implementing `SAS-MI-003: Asset Universe And Alias Registry`.

### 2026-05-09 — SAS-MI-003 — Asset Universe And Alias Registry

- Scope: `src/signal_sandbox/assets/`, `tests/unit/test_asset_registry.py`, `docs/specs/ASSET_UNIVERSE.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 12 needed deterministic asset identity and alias resolution before market-data store and horizon metrics work.
- Decisions applied: ADR-002 T0/local-first boundary; `MARKET_IDEA_SCHEMA.md` resolution states; no guessing and no market-data fetches in this task.
- Evidence collected: added `Asset`, `AssetAlias`, `AliasResolution`, and `AssetRegistry`; resolution normalizes aliases and returns `exact`, `ambiguous`, or `unresolved` with evidence. Seed registry covers BTC, ETH, SOL, SPY, QQQ, Phase 10 observed tickers (AMD, CHMF, GAZP, MAGN, SBER, SFIN, VKCO, VTBR, X5), and an unresolved fallback. Validation after task: 97 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. No market data was fetched.
- Follow-ups: run `SAS-MI-004: Market Data Store Contract` next.

### 2026-05-09 — SAS-MI-004 — Market Data Store Contract

- Scope: `src/signal_sandbox/market_data/`, `tests/unit/test_market_data_store.py`, `docs/specs/MARKET_DATA_STORE.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 12 needed immutable local OHLCV snapshot storage before horizon metric evaluation.
- Decisions applied: ADR-002 T0/local-first boundary; no paid/network provider expansion; snapshot immutability and checksum discipline from the existing price snapshot contract.
- Evidence collected: added `MarketDataSnapshotMetadata`, `MarketDataSnapshot`, `MarketDataStoreProtocol`, `LocalMarketDataStore`, and `make_operator_file_snapshot()`. Snapshots persist under `workspace/market_data/snapshots/<snapshot_id>/` with deterministic metadata and OHLCV bytes, load verifies checksum, list returns sorted metadata, and different-byte overwrite raises `SnapshotAlreadyExists`. Validation after task: 102 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. No paid or network market-data provider was added.
- Follow-ups: run `SAS-MI-005: Deterministic Horizon Metrics` next.

### 2026-05-09 — SAS-MI-005 — Deterministic Horizon Metrics

- Scope: `src/signal_sandbox/market_data/metrics.py`, `tests/unit/test_horizon_metrics.py`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 12 needed deterministic horizon metrics over local snapshots before source corpus/retrieval work begins.
- Decisions applied: ADR-002 deterministic-truth boundary; `MARKET_IDEA_SCHEMA.md` metric contract; no LLM/RAG/retrieval/analyst dependency.
- Evidence collected: added `evaluate_horizon_metrics()` with 1d, 3d, 7d, and 30d returns, MFE, MAE, and explicit `unresolved_asset`, `non_directional`, and `insufficient_data` statuses. Decimal rounding is deterministic. Validation after task: 105 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 12 deep review/archive and continue to `SAS-MI-006: SourceDocument Corpus Schema`.

### 2026-05-09 — SAS-MI-006 — SourceDocument Corpus Schema

- Scope: `src/signal_sandbox/corpus/`, `tests/unit/test_source_document.py`, `docs/specs/SOURCE_CORPUS.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 13 needed a normalized source-corpus document shape before channel profiles and retrieval implementation.
- Decisions applied: ADR-002 RAG context-only boundary; public-source evidence preservation; no embeddings/vector/retrieval implementation in this task.
- Evidence collected: added `SourceDocument` and `from_captured_post()`. The schema preserves capture ID, source ID, author, timestamp, text, evidence URL, text SHA-256, optional media/transcript/OCR references, and metadata. Conversion from `CapturedPost` preserves evidence URL and text hash. Validation after task: 108 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. No transcription/OCR provider, embedding, vector store, or retrieval API was added.
- Follow-ups: run `SAS-MI-007: Channel Profile Registry` next.

### 2026-05-09 — SAS-MI-007 — Channel Profile Registry

- Scope: `src/signal_sandbox/profiles/`, `tests/unit/test_channel_profile.py`, `docs/specs/CHANNEL_PROFILES.md`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 13 needed versioned channel-specific profile state before local retrieval can use author/channel context.
- Decisions applied: ADR-002 RAG context-only boundary; Phase 10 `bablos79` lexicon remains draft/profile evidence and cannot approve signal truth.
- Evidence collected: added `ProfileTerm`, `ChannelProfile`, `ChannelProfileRegistry`, and `import_bablos79_profile()`. The importer preserves `accepted_for_draft`, `needs_review`, and `excluded` states from `workspace/lexicons/bablos79_lexicon_draft.json`, records modality flags and review rules, and returns no default profile for unknown channels. Validation after task: 111 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 13 deep review/archive, then continue to `SAS-MI-008: Local Retrieval Store Prototype`.

### 2026-05-09 — SAS-MI-008 — Local Retrieval Store Prototype

- Scope: `src/signal_sandbox/retrieval/`, `tests/unit/test_retrieval_store.py`, `pyproject.toml`, `requirements.txt`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 14 needed the ADR-approved local retrieval ingestion substrate before query APIs can return cited context.
- Decisions applied: ADR-002 RAG context-only boundary; local DuckDB plus vector/index sidecar substrate; retrieval cannot mutate approved ledgers, market data, deterministic metrics, or report truth artifacts.
- Evidence collected: added `LocalRetrievalStore`, `EmbeddingMetadata`, `IndexedSourceDocument`, deterministic test embeddings, local DuckDB metadata catalog, and deterministic vector sidecar files. Ingestion preserves stable document IDs and citation metadata, records embedding/index metadata including fixture ID, and repeated ingestion is idempotent. Validation after task: 114 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-009: Cited Retrieval API` next.

### 2026-05-09 — SAS-MI-009 — Cited Retrieval API

- Scope: `src/signal_sandbox/retrieval/query.py`, `tests/unit/test_retrieval_query.py`, `src/signal_sandbox/retrieval/store.py`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 14 needed a cited retrieval API for batch analysis before market-idea extraction and later analysis tasks can use local context.
- Decisions applied: ADR-002 RAG context-only boundary; retrieval results must cite source document IDs and evidence hashes and cannot mutate deterministic truth artifacts.
- Evidence collected: added `CitedRetrievalResult`, `RetrievalQueryFilters`, and `query_retrieval_store()`. Results include document_id, snippet, score, source timestamp, evidence URL, and text_sha256; filters for channel and timestamp are deterministic; uncited result models are rejected. Validation after task: 117 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 14 deep review/archive, then continue to `SAS-MI-010: MarketIdea Draft Extractor`.

### 2026-05-09 — SAS-MI-010 — MarketIdea Draft Extractor

- Scope: `src/signal_sandbox/market_ideas/`, `tests/unit/test_market_idea_extractor.py`, `docs/ARCHITECTURE.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 15 needed deterministic source-document to MarketIdea draft extraction before batch export.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; ADR-002 deterministic-truth boundary; Phase 10/13 channel profile states remain draft hints only.
- Evidence collected: added `MarketIdeaDraft`, `EvidenceSpan`, and `MarketIdeaDraftExtractor`. The extractor classifies fixtures into all required MarketIdea categories, uses channel profiles for asset aliases before fallback token matching, preserves direct evidence spans for asset/direction/horizon-risk-catalyst fields when present, and always emits `queued_for_review` unapproved drafts. Validation after task: 120 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-011: MarketIdea Batch Draft Export` next.

### 2026-05-09 — SAS-MI-011 — MarketIdea Batch Draft Export

- Scope: `src/signal_sandbox/market_ideas/export.py`, `tests/unit/test_market_idea_export.py`, `docs/pilot/MARKET_IDEA_DRAFTS_BABLOS79.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 15 needed a reviewable batch export surface before deterministic thesis evaluation.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; draft-only and human-review boundaries; no approved ledger or outcome/report side effects.
- Evidence collected: added `MarketIdeaExportRow`, `MarketIdeaBatchExport`, `export_market_idea_drafts()`, and Markdown rendering. The export creates one row per source document, separates `draft_approval_state` from `final_review_status`, records parser status, review queue reasons, evidence refs, candidate assets, and suggested horizons, and writes only a draft Markdown artifact. Validation after task: 123 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 15 deep review/archive, then continue to `SAS-MI-012: MarketIdea Outcome Evaluator`.

### 2026-05-09 — SAS-MI-012 — MarketIdea Outcome Evaluator

- Scope: `src/signal_sandbox/market_ideas/outcomes.py`, `tests/unit/test_market_idea_outcomes.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 16 needed deterministic thesis evaluation over MarketIdea drafts/reviewed rows.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; deterministic-truth boundary; `SAS-MI-005` horizon metric contract.
- Evidence collected: added `MarketIdeaOutcome`, `IdeaOutcomeStatus`, and `evaluate_market_idea_outcome()`. The evaluator resolves assets through the asset registry, returns unresolved/ambiguous/no-snapshot statuses without guessing, computes horizon metrics through `evaluate_horizon_metrics()` when a matching local snapshot exists, and records source document ID, market idea ID, asset ID, snapshot ID, and metric version. Validation after task: 126 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run `SAS-MI-013: Author Metrics Aggregator` next.

### 2026-05-09 — SAS-MI-013 — Author Metrics Aggregator

- Scope: `src/signal_sandbox/market_ideas/author_metrics.py`, `tests/unit/test_author_metrics.py`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 16 needed author/channel aggregates over deterministic MarketIdea outcomes.
- Decisions applied: `MARKET_IDEA_SCHEMA.md`; deterministic aggregation boundary; non-market/null content must be separate from failed directional ideas.
- Evidence collected: added `AuthorMetrics` and `aggregate_author_metrics()`. The aggregator computes counts by idea type, asset type, horizon status, and review status; directional hit rate only over evaluable long/short outcomes; and null/non-market count/rate separately. Validation after task: 129 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass.
- Follow-ups: run Phase 16 deep review/archive, then continue to `SAS-MI-014: Batch Analyst Contract`.

### 2026-05-09 — SAS-MI-014 — Batch Analyst Contract

- Scope: `src/signal_sandbox/batch_analyst/`, `tests/unit/test_batch_analyst_contract.py`, `docs/specs/BATCH_ANALYST.md`, `docs/CODEX_PROMPT.md`, `docs/tasks.md`.
- Why this work happened: Phase 17 needed a bounded agentic contract before any internal memo export.
- Decisions applied: ADR-002 bounded Agentic profile; fixed operations, max iterations, cost cap, audit log, explicit stop reason, and no mutation/publication authority.
- Evidence collected: added `BatchAnalystJob`, `BatchAnalystRunner`, stop reasons, allowed operation enum, and audit log models. Tests cover schema fields, stop reasons, and checksums for retrieval, metric reads, prompt input, and generated memo. Validation after task: 132 passed, 0 skipped; `ruff check src/ tests/` and `.venv/bin/pyright` pass. Strict agent-trigger review found no shell, network collector, broker, report publisher, ledger mutation, or package/runtime mutation surface.
- Follow-ups: run `SAS-MI-015: Internal Analyst Memo Export` next.

### 2026-05-22 — Two-Month Multimodal Research Run

- Scope: `scripts/three_channel_multimodal_research.py`, `docs/pilot/three_channel_MULTIMODAL_*`, `tests/unit/test_three_channel_multimodal_research.py`, `docs/ANALYST_HANDOFF_RU.md`, `docs/CODEX_PROMPT.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: the operator clarified that the two-month text-only run was insufficient; the research must extract from public Telegram images, voice/audio, and text, then account for entry, stop, target, RR, and position-size evidence where present.
- Decisions applied: public `/s/` Telegram only; raw media stays in ignored `workspace/`; per-media transcript/OCR cache stays ignored; compact manifest/queue/RR/report artifacts are committed; draft transcript/OCR rows remain internal until human/operator accepted.
- Evidence collected: 570 public posts in `2026-03-22..2026-05-22`, 295 media refs, 255 draft transcript/OCR rows (70 voice, 185 image), 40 video/manual blockers, 549 RR draft rows, and 1 internal RR-ready setup draft (`bablos79` post `10450`, `MAGN` short, entry `28400`, stop `28600`, target `26364`, computed RR `10.18`, customer-facing blocked by media review).
- Follow-ups: review/accept or reject draft transcript/OCR rows before customer-facing use; add video processing only if product/legal gate accepts it; improve asset aliasing for Russian names and exchange-specific symbols; run outcome simulation for accepted RR setups.

### 2026-05-22 — Media Reviewer Model Pass

- Scope: `scripts/three_channel_media_reviewer.py`, `docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json`, `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`, `tests/unit/test_three_channel_media_reviewer.py`, active-state handoff docs.
- Why this work happened: the operator asked to add proportionate models that can act as media reviewers and show what they find in image/audio-derived evidence.
- Decisions applied: `gpt-4.1-mini` performs mass review over all 255 transcript/OCR draft rows; `gpt-4.1` performs arbiter review over 35 high-signal rows; model review remains internal-only and does not replace human/operator acceptance.
- Evidence collected: mass reviewer accepted 1 internal candidate, marked 177 rows needs-human-review, 66 reject-noise, 4 context-only, and 7 unable-to-review. Arbiter accepted 9 internal candidates: `pifagortrade` posts `3214`, `3218`, `3225`, `3234`, `3264`, `3274`, `3276`; `bablos79` post `10450`; and `nemphiscrypts` post `3958`.
- Follow-ups: route the 9 arbiter-accepted rows to human/operator review, then recompute setup/RR/outcomes only for accepted rows.

### 2026-05-23 — Phase 37 Pre-Client Artifact Task Graph

- Scope: `docs/tasks.md`, `docs/AI_DEVELOPMENT_PLAN_RU.md`, `docs/CODEX_PROMPT.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `tests/unit/test_preclient_task_graph.py`, active-state task-graph tests.
- Why this work happened: the operator asked to convert the dashboard/paid-report strategy into AI-loop tasks covering everything that can be done internally before client outreach, with reliable artifacts as the priority.
- Decisions applied: no client outreach, private-channel analysis, partnership discussions, public dashboard launch, or paid report promise before Phase 37 produces traceable artifacts and passes the safety/deep-review gate.
- Evidence planned: Phase 37 now defines 10 tasks covering artifact contract, model-reviewed candidate packet, evidence appendix, free dashboard cards, per-channel reports, paid-style demo report, candidate outcome/RR recompute, static dashboard prototype, artifact safety gate, and Phase 37 deep review.
- Follow-ups: start `SAS-PRECLIENT-001` by writing `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md` and its tests.

### 2026-05-23 — SAS-PRECLIENT-001 — Product Artifact Contract

- Scope: `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`, `tests/unit/test_preclient_task_graph.py`.
- Why this work happened: Phase 37 needed a reliability contract before generating any dashboard cards, paid-style reports, evidence appendices, or client-facing demo material.
- Decisions applied: pre-client only; no outreach, no public dashboard, no paid promise, no private-channel analysis, no ranking, no advice; model-reviewed media cannot become dashboard-safe or paid-report-safe without human/operator gates.
- Evidence collected: the contract defines required artifacts, reliability statuses (`draft`, `model_reviewed`, `operator_reviewed`, `market_validated`, `dashboard_safe`, `paid_report_safe`, `blocked`), audience classes, six artifact gates, free dashboard card fields, paid report boundaries, done criteria, and explicit non-goals.
- Follow-ups: run `SAS-PRECLIENT-002` to build the model-reviewed candidate review packet from `three_channel_MEDIA_REVIEW_RESULTS.json` and `three_channel_MULTIMODAL_RR_DRAFTS.json`.

### 2026-05-23 — SAS-PRECLIENT-002 — Model-Reviewed Candidate Review Packet

- Scope: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`, `docs/pilot/preclient_MODEL_REVIEW_PACKET.json`, `tests/unit/test_preclient_model_review_packet.py`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, `AGENT_NOTES.md`, `PHASE_HANDOFF.md`.
- Why this work happened: Phase 37 needed a compact operator packet that joins model reviewer decisions with media/RR evidence before any dashboard card, report, or paid-style claim can use those rows.
- Decisions applied: model review is triage only; every packet row remains `model_reviewed`, `blocked_pending_human_operator_review`, and excluded from customer-facing metrics until a human/operator accepts or rejects it.
- Evidence collected: the packet contains 9 unique arbiter-accepted internal candidates: `bablos79` 1, `nemphiscrypts` 1, and `pifagortrade` 7. It preserves source links, `media_ref_id`, modality, mass/arbiter decisions, evidence types, extracted text excerpts, setup/RR fields where present, and required operator action. The packet also records 1 overlapping mass-review accepted row and 0 customer-facing rows.
- Follow-ups: run `SAS-PRECLIENT-003` to build the evidence appendix over this packet, keeping all rows internal until operator review and market recompute are complete.

### 2026-05-23 — SAS-PRECLIENT-003 — Evidence Appendix Builder

- Scope: `src/signal_sandbox/reports/evidence_appendix.py`, `src/signal_sandbox/reports/__init__.py`, `docs/pilot/preclient_EVIDENCE_APPENDIX.md`, `docs/pilot/preclient_EVIDENCE_APPENDIX.json`, `tests/unit/test_preclient_evidence_appendix.py`, active-state docs.
- Why this work happened: reliable dashboard cards and paid-style reports need one deterministic place where source posts, media refs, transcript/OCR artifacts, review decisions, market-provider state, and blockers can be traced.
- Decisions applied: the appendix is internal-only, includes no raw media bytes or `workspace/media` paths, treats provider gaps as exclusions rather than author losses, and keeps model-reviewed media out of customer-facing metrics.
- Evidence collected: the generated appendix has 301 rows: 255 media-review rows, 40 video/manual blockers, 3 text-only V1 metric summaries, and 3 provider-gap summaries. It distinguishes text-only claims, media-backed candidates, post-factum rows, context-only rows, rejected noise, provider gaps, and media-processing blockers.
- Follow-ups: run `SAS-PRECLIENT-004` to derive compact free-dashboard card data from the appendix without promoting blocked media rows.
