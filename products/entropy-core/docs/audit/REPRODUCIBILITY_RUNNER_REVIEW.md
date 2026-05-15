# Reproducibility Runner Review

Date: 2026-05-14
Phase: 18
Scope: T83-T86
Status: PASS

## Summary

Phase 18 added reproducibility manifests, deterministic hash comparison, and
compare-only CLI behavior:

- `ReproducibilityManifest`, `HashComparisonPolicy`, and declared
  nondeterminism schemas in `src/entropy/artifacts/reproducibility.py`;
- `ArtifactHashCompareRunner` status classification for exact, materially
  equivalent, partial, declared non-reproducible, and failed reproduction;
- safe diff metadata without raw payload dumps;
- `entropy artifact compare <artifact_id> --against <path>`;
- `entropy artifact reproduce <artifact_id>` fail-closed behavior.

## Rerun Execution Decision

Direct rerun command execution is not approved in Phase 18. The implemented CLI
is compare-only, and `artifact reproduce` refuses execution unless a future
explicit gate approves sandboxed local command execution.

## Validation

- `.venv/bin/python -m pytest -q tests/unit/test_reproducibility_manifest.py tests/unit/test_reproducibility_runner.py`: `11 passed`.
- `.venv/bin/python -m pytest -q tests/unit/test_reproducibility_manifest.py tests/unit/test_reproducibility_runner.py tests/unit/test_reproducibility_cli.py tests/unit/test_artifact_cli.py`: `17 passed`.
- `.venv/bin/python -m pytest -q tests/`: `548 passed, 20 skipped`.
- `.venv/bin/python -m ruff check .`: pass.
- `.venv/bin/python -m pyright src/entropy/artifacts src/entropy/cli.py`: `0 errors`.
- `git diff --check`: pass.

## Limitations

- No arbitrary shell command execution is implemented.
- Comparison currently targets JSON-like payloads.
- Status classification is local/internal evidence support only.
- Reproducibility status does not imply performance, external pilot, delivery,
  production, capital-ready, holdout, OOS, live, broker/exchange, or investment
  advice approval.

## Findings

| Severity | Finding | Status |
|---|---|---|
| P2 | Full pyright still has pre-existing test import-resolution errors outside the artifact source files. | Open |

## Decision

Phase 18 is complete. No P0/P1 finding blocks continuation, and no human gate is
triggered. Open Phase 19 with T87 Evidence Packet Schema.
