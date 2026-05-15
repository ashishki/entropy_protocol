# Core V1 Productization Review

Date: 2026-05-14
Phase: 27
Scope: T119-T122
Status: PASS

## Summary

Core V1 is now an internal product kernel for artifact trust workflows. It can:

- validate `entropy-core-artifact/v1` JSON/YAML contracts;
- apply product bridge profile overlays for synthetic Trader and Signal shaped
  artifacts without owning product runtime logic;
- register artifacts and append registry/governance events locally;
- classify reproducibility by comparing expected and actual hashes;
- build and inspect evidence packets;
- enforce artifact governance state transitions and approval-event bindings;
- represent archive-only research outputs as governed artifacts;
- represent CAF allocation decision evidence without executing capital;
- store artifact content locally and expose metadata repository primitives;
- expose an internal Python facade and in-process job model without service
  scope;
- build audit bundle, lineage, data classification, and reviewer-role metadata;
- document the internal V1 surface, runbook, and examples.

## Stable Surfaces

- CLI: documented in `docs/core/CORE_V1_SURFACE_FREEZE.md` and `RUNBOOK.md`.
- Schemas: artifact contract, registry, reproducibility manifest, evidence
  packet, research artifact, CAF artifact, governance event, and audit bundle
  versions are listed in the surface freeze.
- Storage: local JSONL registry/governance history, local content-addressed
  filesystem store, explicit PostgreSQL metadata migration, and object-store
  protocol boundary without runtime dependency.
- Docs/examples: synthetic examples live in `docs/core/CORE_V1_EXAMPLES.md`.

## Verification Evidence

- Phase 25 CAF primitives: `docs/audit/CAF_DECISION_PRIMITIVES_REVIEW.md`.
- Phase 26 enterprise audit readiness:
  `docs/audit/ENTERPRISE_AUDIT_READINESS_REVIEW.md`.
- Surface freeze: `docs/core/CORE_V1_SURFACE_FREEZE.md`.
- Operator runbook: `RUNBOOK.md`.
- Examples: `docs/core/CORE_V1_EXAMPLES.md`.
- Evidence index rows: `docs/EVIDENCE_INDEX.md`.

Final validation:

- `.venv/bin/python -m pytest -q tests/` -> `625 passed, 20 skipped`.
- `.venv/bin/ruff check .` -> clean.
- `.venv/bin/pyright src/entropy/artifacts src/entropy/cli.py src/entropy/db/models.py` -> `0 errors`.
- `git diff --check` -> clean.

## Unapproved Surfaces

Core V1 does not approve:

- commercial product runtime ownership;
- Trader Risk Audit or Signal Analytics Sandbox workspace edits from Core;
- public SDK;
- hosted service or SaaS;
- external enterprise/compliance certification;
- SOC 2, regulatory certification, investment-advice compliance, enterprise
  readiness, or enterprise SLA claims;
- auth, SSO, RBAC, or tenant isolation;
- holdout read or unlock;
- OOS/performance conclusions without a future explicit gate;
- live feeds by default;
- live broker/exchange execution;
- order placement or order blocking;
- live capital;
- production credentials;
- production or capital-ready labels;
- investment advice;
- Rust, Go, Java, C/C++, native extensions, FFI, or second runtime service.

## Open Findings

| Severity | Finding | Status |
|----------|---------|--------|
| P0 | None | Closed |
| P1 | None | Closed |
| P2 | Full pyright over test files still has the pre-existing test import-resolution limitation recorded in state docs. Source scoped pyright is clean. | Open / non-blocking |

## V2 Recommendations

- Decide whether Core V2 should remain a local internal kernel or introduce a
  separately approved service boundary.
- If any service boundary is proposed, write ADRs for auth, authorization,
  tenant isolation, deployment, audit logging, and rollback before routes.
- Keep public SDK, hosted service, live execution, holdout/OOS expansion, and
  compliance claims behind explicit human gates.
- Add schema migration policy only when a concrete breaking schema change is
  required.

## Roadmap Decision

Core V1 productization is complete. Automatic roadmap expansion stops here
until a human approves a Core V2 roadmap.
