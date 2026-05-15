# Product Bridge Profile Review

Date: 2026-05-14
Phase: 20
Scope: T91-T94
Status: PASS

## Summary

Phase 20 added Core-only product bridge profile validation:

- profile model and known profile registry in `src/entropy/artifacts/profiles.py`;
- `generic`, `trader-risk-audit`, and `signal-analytics-sandbox` profile ids;
- profile overlays for required and forbidden no-claim labels;
- `--profile` support for `entropy artifact validate` and
  `entropy artifact register`;
- synthetic product-shaped fixtures under `tests/fixtures/artifacts/profiles/`;
- tests proving product-specific optional fields remain outside the Core base
  artifact schema.

## Ownership Boundary

Core may validate product-shaped artifact boundaries. Core does not own product
runtime behavior, product report generation, source ingestion, domain truth,
delivery approval, customer data handling, or product-local error registers.

The profile ids are validation overlays only. They do not edit or depend on the
Trader Risk Audit or Signal Analytics Sandbox workspaces.

## Validation

- `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_profiles.py`: `3 passed`.
- `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_profile_cli.py tests/unit/test_product_bridge_profiles.py tests/unit/test_artifact_cli.py tests/unit/test_artifact_registry_cli.py`: `15 passed`.
- `.venv/bin/python -m pytest -q tests/unit/test_product_bridge_profile_fixtures.py tests/unit/test_product_bridge_profile_cli.py tests/unit/test_product_bridge_profiles.py`: `9 passed`.
- `.venv/bin/python -m pytest -q tests/`: `566 passed, 20 skipped`.
- `.venv/bin/python -m ruff check .`: pass.
- `.venv/bin/python -m pyright src/entropy/artifacts src/entropy/cli.py`: `0 errors`.
- `git diff --check`: pass.

## Limitations

- Profiles validate boundary vocabulary only.
- Product-specific schemas and report fields remain product-local.
- Synthetic fixtures are not pilot-ready product artifacts.
- Profile validation does not approve external delivery, production,
  capital-ready status, holdout/OOS claims, live execution, broker/exchange
  execution, hosted service scope, public SDK scope, or investment advice.

## Findings

| Severity | Finding | Status |
|---|---|---|
| P2 | Full pyright still has pre-existing test import-resolution errors outside the artifact source files. | Open |

## Decision

Phase 20 is complete. No P0/P1 finding blocks continuation, and no human gate is
triggered. Open Phase 21 with T95 Artifact Governance State Model.
