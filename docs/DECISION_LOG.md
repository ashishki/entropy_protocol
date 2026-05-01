# Decision Log — Entropy Protocol

_Retrieval convenience only. Not an authority. Each entry points to the canonical source._

| ID | Decision | Canonical source | Date |
|----|----------|-----------------|------|
| D-001 | All Capability Profiles OFF — application is deterministic; no LLM in runtime path | docs/ARCHITECTURE.md §Capability Profiles | 2026-05-01 |
| D-002 | Runtime tier T1 — CI requires PostgreSQL service; local workstation uses local services | docs/ARCHITECTURE.md §Solution Shape | 2026-05-01 |
| D-003 | Governance level Standard — research-governance damage is recoverable in v1; no compliance framework | docs/ARCHITECTURE.md §Solution Shape | 2026-05-01 |
| D-004 | Net Sharpe computed ONLY from streams (a)+(b)+(c) — stream (d) carry excluded per protocol spec | docs/IMPLEMENTATION_CONTRACT.md §Net Sharpe Stream Boundary | 2026-05-01 |
| D-005 | Trial Registry writes are append-only; no UPDATE/DELETE on registry or governance_events | docs/IMPLEMENTATION_CONTRACT.md §Registry Append-Only | 2026-05-01 |
| D-006 | Provider-neutral data interface — no hard-coded provider; adapter boundary required before any real OHLCV fetch | docs/ARCHITECTURE.md §External Integrations | 2026-05-01 |
| D-007 | DuckDB for local analytics — embedded, no service needed; Parquet as immutable dataset store | docs/ARCHITECTURE.md §Tech Stack | 2026-05-01 |
| D-008 | Dataset hash = SHA-256(sorted rows + schema fingerprint) — row-order independent reproducibility | docs/tasks.md T08 | 2026-05-01 |
| D-009 | Python is the default Phase 0/1 language; Rust/Go/C/C++ require measured bottleneck, benchmark, ADR, CI/task updates, and human approval before implementation | docs/ARCHITECTURE.md §Language Escalation Policy; docs/IMPLEMENTATION_CONTRACT.md §Language Escalation Control | 2026-05-01 |
