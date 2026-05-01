# Entropy Protocol — Project Brief

Use this document before running `prompts/STRATEGIST.md`. It gives the Strategist enough project context to choose the right implementation shape, governance level, runtime tier, and model strategy without guessing.

Current phase: **Phase 0 planning / implementation bootstrap**.
Current repository state: **documentation-only; no implementation code yet**.
Primary authority documents: `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`, `docs/core/GLOSSARY.md`, `docs/tasks.md`.

Open choices are written as bootstrap assumptions. They must be confirmed before they become protocol or implementation commitments.

---

## 1. Project

- **Project name:** Entropy Protocol.
- **One-sentence summary:** A governed systematic capital-allocation research framework that builds evaluation infrastructure before making any trading-edge claim.
- **Why this project exists:** To create a leakage-resistant, auditable research and evaluation system for multi-asset strategy testing, with strict trial registration, walk-forward OOS separation, cost modeling, regime governance, and four-stream P&L attribution.
- **What success looks like in v1:** Phase 0 implementation is operational: data pipeline, Trial Registry, SimBroker, walk-forward harness, leakage audit, P1/P3 governance state machine, and report generation exist with tests and machine-checkable evidence. No live capital and no OOS performance claims are required for v1.

## 2. Users and Workflows

- **Primary users / operators:** Solo founder/developer operating with Codex for implementation and Claude for architecture/spec/audit review.
- **Main workflow 1:** Register a hypothesis or evaluation spec before data examination, lock parameters, assign family, and store hashes in the Trial Registry.
- **Main workflow 2:** Ingest and validate OHLCV/market data, produce versioned Parquet datasets, and monitor gaps/timestamp consistency.
- **Main workflow 3:** Run walk-forward evaluations through SimBroker, generate four-stream P&L reports, raw/deflated Sharpe, CI, leakage evidence, and phase-gate artifacts.

## 3. Scope

- **In scope for v1:**
  - Phase 0 implementation scaffold.
  - Data pipeline for target universe OHLCV at 4H, 1D, and 1W.
  - Trial Registry with preregistration, family tags, parameter locks, dataset hashes, code hashes, and trial-count accounting.
  - SimBroker with fees, slippage, market impact, borrow/funding hooks, and fill logs.
  - Walk-forward harness with strict IS/OOS separation, purge/embargo support, and leakage checks.
  - P&L attribution engine for streams `(a)+(b)+(c)+(d)`, with net Sharpe computed only from `(a)+(b)+(c)`.
  - P1 drawdown circuit breaker and P3 correlation trigger state-machine tests.
  - Reporting artifacts needed for Phase 0 audit evidence.
- **Out of scope / non-goals:**
  - Live trading or capital deployment.
  - Any result labeled OOS before Phase 0 exit criteria are met.
  - Phase 1 long-only skill validation.
  - Phase 2 1W overlay activation.
  - Equity shorts, crypto perpetual shorts, treasury activation.
  - CCA or RDL influence on portfolio routing.
  - AI-generated signals bypassing human registration and the Trial Registry.

## 4. AI Scope

- **Where AI may be needed:**
  - Architecture critique and ambiguity detection.
  - Drafting spec deltas and ADR-style notes.
  - Implementing code, tests, migrations, and reports.
  - Generating audit prompts, checklists, and review summaries.
  - Drafting candidate hypotheses before human review.
- **Where AI is explicitly not wanted:**
  - Authorizing protocol actions.
  - Declaring findings closed without audit rerun.
  - Modifying frozen non-negotiables.
  - Labeling results as OOS outside the governed harness.
  - Sending research objects directly into portfolio routing or risk escalation.
- **Possible retrieval / RAG need:** Yes. Agents need fast retrieval over core docs, tasks, audits, decisions, implementation journal, and evidence index.
- **If retrieval is needed, is text-only likely sufficient or is multimodal evidence truly required:** Text-only is sufficient for v1.
- **If multimodal may be needed, which modalities and why:** None for v1.
- **Possible tool-use need:** High. Agents need filesystem, git, tests, linters, schema migrations, data validation scripts, and report generation.
- **Possible planning / agentic behavior need:** Medium. Long-running implementation should be decomposed into audited tasks with explicit handoff notes, but agents must not autonomously change protocol rules.

## 5. Deterministic Candidates

List the parts that should stay deterministic unless the Strategist proves otherwise.

- **Validation / policy checks:** Trial Registry admission, Experiment Readiness Gate, Research Firewall, phase-gate checks, leakage checklist, P0/P1 audit-finding status checks.
- **Routing / decision rules:** P1-P4 precedence, P1 drawdown breaker, P3 correlation trigger, RDL phase boundaries, RBE lock/default step.
- **Calculations / transformations:** Dataset hashing, bar aggregation, timestamp normalization, four-stream P&L, net Sharpe, CI method, Harvey-Liu deflation, N_eff, CRR, CER, cost drag, SimBroker cost components.
- **Retries / idempotency / audit triggers:** Data ingestion retries, append-only registry writes, immutable run IDs, governance event logs, report generation, evidence artifact creation.

## 6. Human Approval Boundaries

- **What actions must require human approval:**
  - Any Trial Registry admission.
  - Any spec change to `docs/core/PROTOCOL_SPEC.md`, `docs/core/CHARTER.md`, or `docs/core/GLOSSARY.md`.
  - Any change touching frozen non-negotiables, kill criteria, phase exit criteria, metric thresholds, or P&L attribution rules.
  - Any RBE activation above Step 0.
  - Any transition from research artifact to admissible evaluation.
  - Any live capital decision.
- **What can be automated safely:**
  - Data quality checks.
  - Hash computation.
  - Schema validation.
  - Unit/integration tests.
  - Report rendering from already-approved run artifacts.
  - Audit evidence collection.
- **Why these boundaries matter:** The system operates near low-Sharpe, high-multiplicity territory. Small governance leaks can create false confidence, hidden trial inflation, or invalid OOS claims.

## 7. Risk and Error Cost

- **What is expensive if the system is wrong:** False edge claims, contaminated OOS records, understated costs, bad phase-gate decisions, future capital losses.
- **What is expensive if the system is slow:** Delayed Phase 0 completion, delayed 90-day data monitoring, reduced solo execution momentum.
- **What is expensive if the system is inconsistent / variable:** Non-reproducible evaluations, audit failures, contradictory phase-gate evidence, AI context drift.
- **Blast radius if it fails badly:** In v1, mostly research/governance damage. In later phases, potential capital loss and invalid strategic decisions.
- **Audit / explainability needs:** High. Every evaluation must be reproducible from registry spec, dataset hash, code hash, cost model version, and policy hash.

## 8. Data

- **Primary data sources:** Provider-neutral market-data interface with two data tiers:
  - Tier 1 bootstrap: OHLCV for a liquid ~20-asset research universe at 4H, 1D, and 1W.
  - Tier 2 calibration: bid/ask, spread, or paper-fill data sufficient to verify SimBroker fills against market reality.
- **Approximate data volume:** Low to medium for OHLCV at 4H/1D/1W. Higher if bid/ask or orderbook snapshots are retained.
- **Does data change frequently:** Yes. Market data updates continuously or daily depending on feed cadence.
- **Sensitive / regulated data present:** No personal regulated data expected. Project docs, strategy specs, run logs, and trading research are confidential.
- **Retention / deletion expectations:** Keep immutable evaluation datasets, registry entries, governance events, and report artifacts permanently unless a later governance policy says otherwise. Raw provider cache can be pruned only after a normalized Parquet dataset hash and source provenance record exist.
- **Bootstrap target universe assumption:** Start with a liquid, non-exotic ~20-asset universe split across major crypto assets and highly liquid equity/ETF proxies. Final symbols must be approved before Trial Registry use and stored as a versioned universe artifact.
- **Provider selection assumption:** Do not hard-code a provider into core logic. Implement adapter boundaries first, then select providers by data coverage, timestamp quality, historical depth, bid/ask availability, terms of use, and cost.

## 8b. Continuity and Evidence

- **Which decisions are likely to be revisited later:**
  - Data provider choice.
  - Target universe.
  - P4 weekly regime algorithm.
  - Purge/embargo formula.
  - Harvey-Liu reproducibility package.
  - CI derivation.
  - K3/N_eff estimator.
  - SimBroker calibration method.
  - Phase 0 leakage checklist.
- **What prior evidence or proof will future agents need to find quickly:**
  - Open audit findings and acceptance criteria.
  - ADR/Evolution entries for spec changes.
  - Dataset and code hashes for runs.
  - Trial Registry entries.
  - SimBroker calibration evidence.
  - Phase-gate reports and audit rerun results.
- **Will work span multiple sessions / agents / weeks:** Yes. This is a multi-month project with Codex/Claude handoffs.
- **Any existing docs, ADRs, audits, or notes that should become retrieval anchors:**
  - `docs/README.md`
  - `docs/core/PROTOCOL_SPEC.md`
  - `docs/core/CHARTER.md`
  - `docs/core/GLOSSARY.md`
  - `docs/core/EVOLUTION.md`
  - `docs/tasks.md`
  - `docs/audit/REVIEW_REPORT.md`
  - `docs/audit/AUDIT_v1.md`
  - `docs/architecture/AI_ENGINEERING_FRAMEWORK.md`
  - `docs/architecture/workflow_ai_development.md`
  - `docs/governance/research_firewall.md`
  - `docs/governance/experiment_readiness_gate.md`
  - `docs/governance/hypothesis_families.md`

## 9. Integrations

- **External APIs / services:** Provider adapters for exchange OHLCV, broker paper trading/fill logs, and optional professional market-data feeds. The first implementation should support local fixture data plus one real OHLCV adapter; SimBroker calibration can add a bid/ask or paper-fill adapter as a separate step.
- **Databases / storage:** Recommended: PostgreSQL for registry/events/runs, Parquet for market data/features, DuckDB for local analytics.
- **Auth / identity provider:** Not needed for local v1. If a future dashboard is added, use local single-user auth first and defer multi-user identity until there is a real operator need.
- **Webhooks / messaging / queues:** Not needed for v1. Cron/systemd or simple scheduled jobs are likely sufficient at first.

## 10. Constraints

- **Preferred stack:** Python 3.12, `uv`, `pydantic`, `polars`, `pyarrow`, Parquet, DuckDB, PostgreSQL, SQLAlchemy/Alembic, pytest, ruff, pyright or mypy, typer/rich.
- **Deployment target:** Local workstation first. Optional small Linux VPS later for continuous data ingestion, feed monitoring, and paper-fill logging.
- **Budget constraints:** Medium sensitivity. LLM/API/infrastructure costs must be tracked because K2 depends on them in later phases.
- **Latency / throughput expectations:** Low latency is not required for v1. Determinism, reproducibility, and auditability matter more.
- **Compliance requirements:** Internal governance only for v1. No investment-advice or external client workflow.
- **Network / security restrictions:** No credentials in git. Store provider keys in local environment variables or a local secrets file excluded from version control. Treat provider keys, strategy specs, registry records, and run reports as confidential.

## 11. Runtime and Operations

- **Should runtime stay simple (managed service / container) if possible:** Yes. Prefer CLI + local services before introducing orchestration platforms.
- **Any need for shell, package, or toolchain mutation at runtime:** Development environment only. Production-like jobs should not mutate dependencies at runtime.
- **Any need for privileged actions or long-lived isolated workers:** No privileged actions expected. Long-lived ingestion/monitoring worker may be needed later.
- **Recovery / rollback expectations:** Registry writes and governance logs should be append-only. Data ingestion should be idempotent. Evaluation runs should be reproducible and rerunnable from hashes.

## 12. Model and Cost Expectations

Only fill what is known. The Strategist should still make the final recommendation.

- **Cost sensitivity:** medium.
- **Latency sensitivity:** low.
- **Expected request / task volume:** Medium during implementation bursts; low to medium during routine operation.
- **If AI is used, should the system prefer smaller / cheaper models by default:** Yes for routine summarization, extraction, and formatting. Use stronger models for architecture, audit, statistical reasoning, and nontrivial implementation.
- **Any required capabilities:** reasoning, long context, structured output, function/tool calling, code generation, code review.
- **Preview-model tolerance:** low for implementation and governance artifacts; medium for exploratory research drafts that remain non-authoritative.

## 13. Success Metrics

- **Business success metric:** Phase 0 can be completed and audited without invalid OOS claims or governance bypasses.
- **Quality metric:** A third party can reproduce each evaluation report from registry spec, dataset hash, code hash, and policy hash.
- **Latency metric:** Not phase-critical. Batch evaluations should be practical on a local workstation.
- **Cost metric:** Infrastructure + LLM costs are tracked monthly and remain explainable relative to simulated gross return assumptions.
- **Operational metric:** Data pipeline produces zero unexplained gaps over the required 90-day monitoring window; all Phase 0 tests and leakage checks pass.

## 14. Current Phase 0 Blockers

These items should be treated as explicit strategy/bootstrap inputs, not implementation details to guess around:

- Harvey-Liu method package needs formula-level reproducibility and worked examples.
- Sharpe CI method needs derivation and validation examples.
- P4 weekly regime algorithm is not independently reproducible yet.
- IC_long suspect threshold and correlation-aware FLAM control remain unresolved.
- Purge/embargo formula is incomplete.
- Leakage audit must cover normalization leakage, regime label look-ahead, universe selection bias, and within-window optimization.
- Timestamp convention checks must become a gate item.
- K3/N_eff estimator must be locked across docs and implementation.
- P1 circuit-breaker synthetic test suite must be enumerated.

## 15. Recommended First Implementation Slice

- Create project scaffold and test harness.
- Implement typed domain models for datasets, registry entries, runs, fills, P&L streams, and governance events.
- Implement Trial Registry as the first real subsystem.
- Implement deterministic dataset hashing and run hashing.
- Implement data ingestion interface with one provider adapter stub and local Parquet store.
- Implement SimBroker cost model skeleton with fill/cost logs.
- Implement P1/P3 state-machine tests before any strategy skill code.

---

## Usage

1. Review and confirm bootstrap assumptions, especially provider strategy, target universe, and deployment target.
2. Send this completed brief to the Strategist via `prompts/STRATEGIST.md`.
3. Let the Strategist ask one batch of clarifying questions.
4. Use the resulting architecture package as the implementation input for Codex and Claude.
