# Artifact Registry Review

Date: 2026-05-14
Phase: 17
Scope: T79-T82
Status: PASS

## Summary

Phase 17 added a local, internal, append-only artifact registry layer on top of
Phase 16 validation:

- governed registry models in `src/entropy/artifacts/registry.py`;
- immutable `ArtifactRegistryRecord`, `ArtifactHashSet`, and
  `ArtifactRegistryEvent` Pydantic schemas;
- append-only local JSONL writes for records and events;
- `entropy artifact register <path>`;
- `entropy artifact show <artifact_id>`;
- `entropy artifact list`;
- `entropy artifact history <artifact_id>`.

The registry rejects invalid or unvalidated artifacts, rejects unresolved unsafe
claim surfaces, and rejects duplicate registration with a stable machine-readable
error.

## Append-Only Behavior

Corrections are represented as new records and/or events. Existing records are
frozen Pydantic models, and JSONL persistence appends registration events rather
than rewriting prior event history.

## Storage Decision

The local file-backed registry remains sufficient until Phase 23. Database
persistence, migrations, and durable storage abstractions are intentionally not
introduced in Phase 17.

## Validation

- `.venv/bin/python -m pytest -q tests/unit/test_artifact_registry.py tests/unit/test_artifact_registry_cli.py tests/unit/test_artifact_cli.py tests/unit/test_cli.py`: `15 passed`.
- `.venv/bin/python -m pytest -q tests/`: `534 passed, 20 skipped`.
- `.venv/bin/python -m ruff check .`: pass.
- `.venv/bin/python -m pyright src/entropy/artifacts src/entropy/cli.py`: `0 errors`.
- `git diff --check`: pass.

## Limitations

- Registry storage is local JSONL only.
- No database persistence is introduced before Phase 23.
- No public SDK, hosted service, product runtime, holdout/OOS, live execution,
  broker/exchange, capital, production, or capital-ready scope is opened.

## Findings

| Severity | Finding | Status |
|---|---|---|
| P2 | Full pyright still has pre-existing test import-resolution errors outside the new artifact source files. | Open |

## Decision

Phase 17 is complete. No P0/P1 finding blocks continuation, and no human gate is
triggered. Open Phase 18 with T83 Reproducibility Manifest Schema.
