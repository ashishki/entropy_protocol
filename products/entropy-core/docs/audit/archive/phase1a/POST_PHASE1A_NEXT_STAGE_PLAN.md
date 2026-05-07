# Post-Phase-1A Next Stage Plan

Date: 2026-05-05
Stage: `Post-Phase-1A Audit Readiness And Deep Review`
Status: `SELECTED`

## Objective

Prepare and run the required post-Phase-1A deep protocol review before opening a
new implementation phase.

This stage exists because Phase 1A closed a meaningful scaffold/probe phase, and
the operating rule requires a deep review after a large phase. The current audit
prompt chain must be refreshed first because F-C3-007 shows stale Cycle 1
pre-development metadata.

## Task List

### P1A-011 Audit Prompt Metadata Refresh

Refresh current-cycle metadata in:

- `products/entropy-core/docs/audit/PROMPT_0_META.md`
- `products/entropy-core/docs/audit/PROMPT_1_ARCH_REVIEW.md`
- `products/entropy-core/docs/audit/PROMPT_2_INVARIANTS.md`
- `products/entropy-core/docs/audit/PROMPT_3_DRIFT_GUARD.md`
- `products/entropy-core/docs/audit/PROMPT_4_ADVERSARIAL.md`
- `products/entropy-core/docs/audit/PROMPT_5_CONSOLIDATED.md`

Acceptance:

- prompts identify the current post-Phase-1A context;
- stale Cycle 1 pre-development assumptions are removed or overridden;
- the prompt sequence still points to current root audit outputs;
- no archive bulk-load requirement is introduced;
- no protocol semantics are changed.

### P1A-012 Post-Phase-1A Deep Protocol Review

Run the audit sequence:

1. `PROMPT_0_META.md`
2. `PROMPT_1_ARCH_REVIEW.md`
3. `PROMPT_2_INVARIANTS.md`
4. `PROMPT_3_DRIFT_GUARD.md`
5. `PROMPT_4_ADVERSARIAL.md`
6. `PROMPT_5_CONSOLIDATED.md`

Acceptance:

- root audit outputs are refreshed;
- findings are classified P0/P1/P2/P3;
- no Phase 1 evaluation/trading approval is inferred from the review itself.

### P1A-013 Consolidated Post-Phase-1A Decision

Use the consolidated review to select the next task graph.

Possible outcomes:

- archive-only hardening block;
- benchmark-contract extension;
- Phase 1 planning path requiring explicit human approval;
- no-go until audit findings are closed.

## Blockers And Dispositions

| ID | Status | Disposition |
|---|---|---|
| F-C3-007 | Open | Fix in P1A-011 before full audit run |
| Phase 1 evaluation gate | Not approved | Requires separate human/gate decision after review |
| Holdout | Locked | No unlock in this stage |
| Runtime escalation | Not approved | Requires benchmark miss, ADR, architecture/task/CI updates, and human approval |

## Evidence Requirements

- `git diff --check` after documentation changes;
- prompt refresh diff demonstrating current-cycle metadata;
- refreshed audit output files from P1A-012;
- consolidated review finding inventory before any new implementation task.

## Review Gates

- P1A-011 review: confirm prompt metadata is current and does not rewrite
  canonical protocol rules.
- P1A-012 review: confirm deep audit ran in order and did not approve forbidden
  claims.
- P1A-013 review: human/strategic decision before opening any implementation
  block.

## Non-Goals

- Phase 1 evaluation/trading;
- alpha logic;
- portfolio allocation or backtest/evaluation;
- holdout read/unlock;
- live feed, streaming provider, broker integration, or live capital;
- Growth/RDL/RBE activation;
- Rust, Go, C/C++, FFI, native extensions, or second runtime service;
- OOS/performance, production, or capital-ready labels.
