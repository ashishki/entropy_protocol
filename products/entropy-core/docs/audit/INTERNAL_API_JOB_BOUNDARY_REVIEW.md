# Internal API And Job Boundary Review

Date: 2026-05-14
Phase: 24
Scope: T107-T110
Status: PASS

## Summary

Phase 24 established an internal-only integration boundary:

- ADR `docs/adr/ADR-CORE-INTERNAL-API-JOB-BOUNDARY.md` accepted an internal
  Python facade and in-process job model;
- FastAPI service, hosted Core service, public SDK, external auth, tenant model,
  external SLA, and worker runtime dependencies were deferred/rejected;
- `src/entropy/artifacts/api.py` exposes typed internal functions for validate,
  register, compare, build evidence, and transition state;
- `src/entropy/artifacts/jobs.py` defines idempotent in-process artifact jobs.

## Blocked Service Surfaces

No public SDK, hosted service, HTTP API, multi-tenant auth, external SLA,
background worker dependency, Celery, Redis, Temporal, Kafka, service container,
holdout/OOS expansion, live execution, broker/exchange execution, production
deployment, capital-ready path, or investment-advice path was introduced.

## Validation

- `.venv/bin/python -m pytest -q tests/unit/test_internal_api_facade.py`: `3 passed`.
- `.venv/bin/python -m pytest -q tests/unit/test_internal_api_facade.py tests/unit/test_internal_job_model.py`: `6 passed`.
- `.venv/bin/python -m pytest -q tests/`: `600 passed, 20 skipped`.
- `.venv/bin/python -m ruff check .`: pass.
- `.venv/bin/python -m pyright src/entropy/artifacts src/entropy/cli.py src/entropy/db/models.py`: `0 errors`.
- `git diff --check`: pass.

## Limitations

- The facade is internal library code, not a public SDK.
- Jobs are in-process records only, not a worker runtime.
- Future service/API or worker runtime work requires a new ADR and human
  approval before implementation.

## Findings

| Severity | Finding | Status |
|---|---|---|
| P2 | Full pyright still has pre-existing test import-resolution errors outside the artifact source files. | Open |

## Decision

Phase 24 is complete. No P0/P1 finding blocks continuation, and no human gate is
triggered. Open Phase 25 with T111 CAF Artifact Vocabulary.
