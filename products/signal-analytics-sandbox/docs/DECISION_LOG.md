# Decision Log — Signal Analytics Sandbox

Version: 1.0
Last updated: 2026-05-08

This file is a lightweight retrieval surface. It is not the source of truth. If an entry conflicts with a canonical document (`docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/spec.md`, `docs/tasks.md`, ADRs), the canonical document wins and this file must be corrected.

---

## Rules

- Keep entries short and link to the authoritative document or section.
- Record why a decision was made and what it replaced.
- Update this file when architecture, runtime, governance, or major implementation direction changes.
- Mark superseded decisions explicitly instead of deleting them.

---

## Decision Index

| ID    | Date       | Status | Decision | Why it matters | Canonical source | Supersedes |
|-------|------------|--------|----------|----------------|------------------|------------|
| D-001 | 2026-05-07 | Active | Solution shape: Hybrid (deterministic core + bounded workflow + gated LLM-assist adapter) | Audit/explainability is "very high" per brief; deterministic core is the basis of the reproducibility contract; LLM is gated escalation only. | `docs/ARCHITECTURE.md#solution-shape` | none |
| D-002 | 2026-05-07 | Active | Governance: Lean | Local single-operator sandbox; audit-heaviness is encoded as project-specific contract rules (PSR-1..PSR-11) rather than Standard-grade ceremony. | `docs/ARCHITECTURE.md#solution-shape` | none |
| D-003 | 2026-05-07 | Active | Runtime tier: T0 | Local CLI; no shell mutation, no isolation, no privilege, no persistent worker. Lower runtime tiers do not exist; higher tiers are not justified. | `docs/ARCHITECTURE.md#runtime-and-isolation-model` | none |
| D-004 | 2026-05-07 | Active | All capability profiles OFF (RAG / Tool-Use / Agentic / Planning / Compliance) | No managed corpus, no LLM-directed tool calls, no decision loop, no plan-as-deliverable, no named regulatory framework. Profile activation requires an ADR. | `docs/ARCHITECTURE.md#capability-profiles` | none |
| D-005 | 2026-05-07 | Active | Distribution: Python package `signal_sandbox` + console-script `signal-sandbox` | Library is needed for tests / scripts / future agents; CLI is needed for repeatable pilot operator workflows. | `docs/ARCHITECTURE.md#tech-stack` | none |
| D-006 | 2026-05-07 | Active | Python 3.12 | Consistency with Entropy Core and existing workspace per operator decision; brief mandates 3.12. | `docs/ARCHITECTURE.md#tech-stack` | none |
| D-007 | 2026-05-07 | Active | Price-data adapter pattern with multiple providers (operator-file, exchange-public, paid, yfinance-dev) | Brief priorities: data quality > reproducibility > legal > snapshot/cache > provenance > cost. Adapter pattern lets us pick the best provider per pilot without changing the deterministic core. | `docs/ARCHITECTURE.md#external-integrations`, `docs/tasks.md#T09` | none |
| D-008 | 2026-05-07 | Active | Snapshot persistence uses deterministic Parquet bytes (rows sorted by asset/timestamp, fixed columns, zstd compression, statistics disabled) plus deterministic JSON metadata; SHA-256 verifies the Parquet payload. | Reproducibility contract (PSR-2) requires byte-identical re-runs; snapshot immutability is the foundation. ADR-001 fixes the writer contract for T09/T11. | `docs/adr/ADR-001-snapshot-serialization.md`, `docs/IMPLEMENTATION_CONTRACT.md#PSR-5`, `docs/tasks.md#T11` | none |
| D-009 | 2026-05-07 | Active | LLM extraction is gated escalation: parser-first by default; LLM adapter requires `SIGNAL_SANDBOX_ENABLE_LLM=1` AND per-run `--llm-approved` flag | Brief: high cost sensitivity, "treating LLM output as truth" forbidden, manual extraction may not scale. Double gate ensures intentional activation. | `docs/IMPLEMENTATION_CONTRACT.md#PSR-3`, `docs/tasks.md#T20` | none |
| D-010 | 2026-05-07 | Active | Phase 0 tasks SAS-001 (paid pilot demand) and SAS-002 (legal/risk memo) are visible in `docs/tasks.md` (option (a)), human-owned, gating engineering Phase 1 | Demand validation and legal/source-risk boundaries must be visible to the orchestrator, not hidden in prose. | `docs/tasks.md#phase-0`, `docs/IMPLEMENTATION_CONTRACT.md#PSR-10` | none |
| D-011 | 2026-05-07 | Active | Three heavy tasks marked: T12 (outcome matcher), T14 (report renderer), T20 (LLM extraction adapter) | These three carry the load-bearing correctness, evidence-integrity, and non-truth-from-LLM contracts. Other tasks are routine. | `docs/tasks.md` (Execution-Mode: heavy fields) | none |
| D-012 | 2026-05-07 | Active | OBS-3 (HTTP `GET /health`) is replaced by CLI subcommand `signal-sandbox status` for this CLI/library project | The playbook's HTTP health invariant does not apply to a local CLI; the substitute preserves intent (config sanity, no PII, no auth, no network). | `docs/ARCHITECTURE.md#observability`, `docs/IMPLEMENTATION_CONTRACT.md#OBS-3` | none |
| D-013 | 2026-05-07 | Active | Phase 9 is a customer-backed Telegram pilot loop over the three operator/customer-provided public Telegram sources, before any further automation | After T20 the implementation graph is complete, but the next risk is customer/payment validation and report usefulness. The orchestrator must continue through `SAS-PILOT-001..007` in `docs/tasks.md`, not through ad hoc prose. | `docs/tasks.md#phase-9--customer-backed-telegram-pilot-loop`, `docs/PILOT_DEVELOPMENT_LOOP_RU.md` | none |
| D-014 | 2026-05-07 | Active | Phase 9 decision: continue manual extraction for the captured first-source batch; defer automation | `bablos79` now has 60 public text captures from unauthenticated Telegram `/s/` pages, but no manual extraction, approved records, customer decision impact, or payment signal. Engineering expansion remains premature. | `docs/pilot/PILOT_DECISION.md`, `docs/pilot/CAPTURE_LOG.md`, `workspace/captures/bablos79/` | none |
| D-015 | 2026-05-07 | Superseded | Phase 10 approved as a narrow deterministic draft-extraction assistant, initially starting with seed labels | The 60 captured posts create a concrete extraction bottleneck. Automation is limited to reviewable parser suggestions; no auto-approved ledger writes, bot ingestion, private scraping, or LLM truth. | `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`, `docs/tasks.md#phase-10--draft-extraction-assistant-for-captured-telegram-posts` | none |
| D-016 | 2026-05-07 | Active | Frontier model may be used offline for author-specific lexicon/profile discovery before parser implementation | A short hard-coded Russian trading lexicon is likely to miss each author's idioms. Model output is allowed only as evidence-cited candidate vocabulary/profile data; runtime parser, exports, tests, and ledger writes remain deterministic and non-LLM. | `docs/tasks.md#sas-auto-001b-author-lexicon-and-draft-profile-discovery`, `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md` | none |
| D-017 | 2026-05-08 | Active | Phase 10 starts with machine-first pseudo-label bootstrap instead of manual seed labeling | The desired workflow is automation-first: frontier model drafts labels for all captured posts, deterministic validators reject unsupported fields, and humans review only exceptions or customer-facing claims. This preserves auditability while avoiding full manual seed labeling. | `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`, `docs/tasks.md#sas-auto-001-machine-first-pseudo-label-bootstrap`, `docs/pilot/AUTO_EXTRACTION_DEVELOPMENT_PLAN.md` | D-015 |

---

## Retrieval Notes

- Read this file before revisiting architecture, changing runtime tier, modifying the reproducibility contract, swapping price-data adapters, or activating the LLM extraction adapter.
- If a task has `Context-Refs`, prefer those entries over scanning this file top-to-bottom.
