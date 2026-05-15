# CAF Decision Primitives Review

Date: 2026-05-14
Phase: 25
Scope: T111-T114
Status: PASS

## Summary

Phase 25 added the first Capital Allocation Framework artifact primitives inside
Core:

- `src/entropy/artifacts/caf.py` defines the CAF artifact vocabulary,
  no-claim labels, forbidden execution fields, and unsafe claim labels.
- `AllocationDecisionArtifact` binds a decision id, portfolio context ref,
  constraint refs, evidence refs, rationale refs, four-stream attribution refs,
  limitations, and no-claim boundaries.
- `FourStreamAttributionRefs` keeps stream d separately referenced while net
  Sharpe streams are limited to streams a, b, and c.
- `AllocationDecisionArtifact.to_artifact_contract()` renders CAF decisions into
  the base `entropy-core-artifact/v1` contract for standard validation.
- Synthetic CAF fixtures cover the valid allocation decision shape and unsafe
  live-allocation, investment-advice, and capital-ready variants.

## Validation

- Scoped CAF tests: `.venv/bin/python -m pytest -q tests/unit/test_caf_artifact_vocabulary.py tests/unit/test_allocation_decision_artifact.py tests/unit/test_caf_artifact_fixtures.py` -> `12 passed`.
- Full suite: `.venv/bin/python -m pytest -q tests/` -> `612 passed, 20 skipped`.
- Ruff: `.venv/bin/ruff check .` clean.
- Pyright: `src/entropy/artifacts`, `src/entropy/cli.py`, and
  `src/entropy/db/models.py` clean with `0 errors`.
- Whitespace: `git diff --check` clean.

## No-Capital-Execution Boundary

This phase did not approve or add:

- capital movement;
- investment advice;
- live allocation;
- broker or exchange execution;
- order placement or order blocking;
- live capital;
- production or capital-ready labels;
- public SDK, hosted service, or external compliance claims.

CAF artifacts are evidence contracts only. They describe governed decision
evidence and boundaries; they do not execute allocations.

## Findings

| Severity | Finding | Status |
|----------|---------|--------|
| P0 | None | Closed |
| P1 | None | Closed |
| P2 | Full pyright over test files still has the pre-existing test import-resolution limitation recorded in state docs. Source scoped pyright is clean. | Open / non-blocking |

## Roadmap Decision

No P0/P1 blocker remains. Phase 26 Enterprise Audit Readiness can open with
T115 Audit Bundle Schema.
