# Product AI Development Operating Model

Status: Active
Date: 2026-05-07

This document defines the repo-local AI development model for the product
portfolio. The repository root no longer stores a shared playbook, shared prompt
pool, or shared templates; each product workspace owns its own development
pool.

Reference workflow:

- target workspace `PLAYBOOK.md`
- target workspace `prompts/`
- target workspace `templates/`
- target workspace `hooks/`
- target workspace `ci/ci.yml`
- target workspace `.claude/`
- `products/entropy-core/docs/CODEX_PROMPT.md`
- `products/entropy-core/docs/tasks.md`
- `products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md`
- External reference only, not copied into root:
  `https://github.com/ashishki/AI_workflow_playbook/blob/master/docs/usage_guide.md`

## Workspace Model

There is one repository and three product workspaces:

| Workspace | Path | Purpose |
|---|---|---|
| Entropy Core | `products/entropy-core/` | Governed core primitives and protocol-safe bridges |
| Trader Risk Audit | `products/trader-risk-audit/` | Primary commercial MVP |
| Signal Analytics Sandbox | `products/signal-analytics-sandbox/` | Separate public-source signal analytics validation |

Each workspace has local:

- `README.md`
- `.env.example`
- `PLAYBOOK.md`
- `prompts/`
- `templates/`
- `hooks/`
- `ci/ci.yml`
- `.claude/settings.json`
- `.claude/commands/bootstrap-new.md`
- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/tasks.md`
- `docs/CODEX_PROMPT.md`

These local docs are development contracts for segmented work. They do not
override Entropy Core canonical protocol documents.

The repository root intentionally has no shared playbook, prompt pool, template
pool, hooks, or workflow CI template. Product teams update their own workspace
copy when their development process diverges.

## Environment Separation

Real `.env` files are never committed. Each product workspace may have its own
local `.env` derived from `.env.example`. Product-specific virtual environments
also live inside the owning workspace and are not committed.

Rules:

- Keep product-specific env vars prefixed by product:
  - `ENTROPY_CORE_`
  - `TRA_`
  - `SAS_`
- Do not reuse live credentials across products.
- Do not add broker/exchange API keys to any workspace until an explicit gate
  permits it.
- Do not add private Telegram credentials to the sandbox.
- Keep Python virtual environments product-local, e.g.
  `products/entropy-core/.venv/`.

## Stack And Language Policy

The portfolio is Python-first for MVP development, but not Python-only forever.
The goal is to avoid premature multi-language complexity while keeping escape
hatches for real load.

Rules:

- Use Python for v1 product logic unless measured evidence proves it cannot meet
  a stated runtime or memory target.
- Design stable module boundaries around imports, rule evaluation, report
  generation, simulation/evaluation, and data adapters so a hot path can be
  replaced without rewriting the product.
- Prefer vectorized/data-native tools first: Polars, DuckDB, PyArrow/Parquet,
  SQL indexes, batching, caching, and streaming reads before changing language.
- Rust is the preferred escalation for CPU-bound numerical kernels, parsers,
  fill matching, rolling windows, or simulation hot loops.
- Go is the preferred escalation for long-running services, collectors,
  workers, or operational control planes if Python CLI/batch jobs are
  insufficient.
- C/C++ is allowed only for unavoidable external native integration or a proven
  low-level numerical requirement with no Rust/Python alternative.
- No product may add Rust, Go, C/C++, FFI, native extensions, or a second runtime
  service without a benchmark, an ADR, CI/toolchain plan, rollback plan, and
  human approval.

This policy exists to prevent two failure modes: overbuilding the MVP in a
complex stack before demand is proven, and writing Python code with no modular
boundary for future performance replacement.

## Parallel Development Rules

Parallel work is allowed only when write scopes are separated.

| Stream | Path ownership | Parallel-safe? |
|---|---|---|
| Core governance bridge | `products/entropy-core/src/entropy/`, `products/entropy-core/docs/` | Yes, if not touching product MVP files |
| Trader import/rules/reporting | `products/trader-risk-audit/` and future `products/trader-risk-audit/src/` | Yes |
| Signal sandbox | `products/signal-analytics-sandbox/` and future `products/signal-analytics-sandbox/src/` | Yes, separate |
| Core protocol docs | `products/entropy-core/docs/core/`, `products/entropy-core/docs/ARCHITECTURE.md`, `products/entropy-core/docs/spec.md` | No, gated |
| Live risk guard | Any broker/API paths | No, deferred |

## AI Task Startup Protocol

Before an AI development session for a product workspace:

1. Read root `docs/README.md`.
2. Read root `docs/PRODUCT_PORTFOLIO.md`.
3. Read root `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md` when the task touches
   real-data reports, pilot artifacts, or product prioritization.
4. Read the target workspace `README.md`.
5. Read the target workspace `docs/CODEX_PROMPT.md`.
6. Read the target workspace artifact roadmap when present:
   - `products/trader-risk-audit/docs/ARTIFACT_VALIDATION_ROADMAP.md`
   - `products/signal-analytics-sandbox/docs/ARTIFACT_VALIDATION_ROADMAP.md`
   - `products/entropy-core/docs/ARTIFACT_SUPPORT_ROADMAP.md`
7. Read the target workspace `docs/tasks.md`.
8. Confirm the task does not violate product boundaries.

## Context Budget Rule

Product `docs/CODEX_PROMPT.md`, `PHASE_HANDOFF.md`, `AGENT_NOTES.md`, and
`README.md` are active-context files. Keep them compact:

- current state;
- next task;
- active guardrails;
- links to canonical detail.

Do not append long task-by-task logs, deep-review transcripts, or historical
implementation detail to active-context files. Put detailed history in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/EVIDENCE_INDEX.md`, `docs/archive/`,
or `docs/tasks.md` depending on the artifact type.

For implementation work touching `products/entropy-core/src/entropy/` or
Entropy Core docs, also read
`products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md`,
`products/entropy-core/docs/CODEX_PROMPT.md`, and
`products/entropy-core/docs/tasks.md`.

## Task Format

Product workspace tasks should remain forward-looking and YAML-compatible enough
for an orchestrator to parse:

```yaml
Task: TRA-001
Owner: trader-risk-audit
Phase: A
Type: validation
Depends-On: []
Objective: ...
Acceptance-Criteria:
  - id: AC1
    description: ...
    test: manual-evidence
Files:
  - products/trader-risk-audit/docs/...
Notes: ...
```

Do not reconstruct historical backlog inside product workspaces. Start from the
next real incomplete task.

## Review Policy

- Documentation-only product workspace changes require a lightweight review by
  the human sponsor or orchestrator.
- Entropy Core protocol changes require the existing core governance process.
- Code changes that add deterministic import, rule, report, registry, evidence,
  or data handling must include tests.
- Any task introducing live execution, broker APIs, private-source scraping,
  autonomous AI strategy generation, or new runtime services is blocked unless
  a new approved gate exists.

## First AI-Development Sequence

Recommended order:

1. `TRA-001` - paid validation evidence.
2. `TRA-002` - manual audit report template.
3. `TRA-003` - trade import contract from real exports.
4. `TRA-004` - risk policy spec.
5. `TRA-005` - deterministic violation record contract.
6. `TRA-006` - minimal report generator design.
7. `EC-001` - core bridge design only after Trader Risk Audit validation.
8. `SAS-001` - public-source signal sandbox feasibility only if separately
   staffed.
