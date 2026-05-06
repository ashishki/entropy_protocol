# Phase 1A Archive Registration Boundary Packet

Date: 2026-05-05
Task: P1A-003
Status: `COMPLETE`
Boundary ID: `PHASE1A-ARCHIVE-REGISTRATION-BOUNDARY-v1`

## Decision

P1A-003 is approved as the machine-readable archive split registration and
read-gate boundary for Phase 1A archive-only baseline planning.

The boundary is derived from freeze `PHASE1A-ARCHIVE-FREEZE-v1`. It validates
the freeze manifest hash, preserves the 15-dataset archive-only universe, and
defines deterministic access rules for archive formation, archive validation,
and archive holdout. It does not implement strategy logic, portfolio logic,
archive performance evaluation, Growth instrumentation, RDL scaffolding, live
feeds, or OOS/performance claims.

## Boundary Scope

| Field | Value |
|---|---|
| Dataset count | 15 |
| Split count | 3 |
| Archive only | `true` |
| Gate claim allowed | `false` |
| Freeze manifest hash | `54a820dbb07557294e821356168db4dbc6ba70fda4464a519442c4b20faea35e` |
| Boundary manifest hash | `2759fad18037361412f504384f22b411b4283b00e7764150f8c660f4375620df` |

## Split Access Rules

| Split | Window | Access | Required fields |
|---|---|---|---|
| `ARCHIVE_FORMATION` | `2020-01-01` through `2022-12-31` | `ALLOW` | none |
| `ARCHIVE_VALIDATION` | `2023-01-01` through `2024-12-31` | `ALLOW_WITH_REGISTRATION` | `baseline_registration_id`, `baseline_spec_hash`, `validation_registration_hash` |
| `ARCHIVE_HOLDOUT` | `2025-01-01` through `2025-12-31` | `LOCKED` | future unlock required |

Holdout denial reason:
`HOLDOUT_LOCKED_PENDING_BASELINE_REGISTRATION`.

## Artifacts

| Artifact | Path |
|---|---|
| Boundary implementation | `entropy/evidence/phase1a_registration.py` |
| Unit tests | `tests/unit/test_phase1a_registration.py` |
| Package export | `entropy/evidence/__init__.py` |
| Boundary manifest | `artifacts/evidence/phase1a_registration_boundary/boundary_001/PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_MANIFEST.json` |
| Boundary summary | `artifacts/evidence/phase1a_registration_boundary/boundary_001/PHASE1A_ARCHIVE_REGISTRATION_BOUNDARY_SUMMARY.md` |
| Freeze manifest | `artifacts/evidence/phase1a_archive_freeze/freeze_001/PHASE1A_ARCHIVE_FREEZE_MANIFEST.json` |

## Validation

- Freeze manifest hash must match the P1A-002 frozen hash.
- Frozen datasets remain archive-only and no-claim.
- `ARCHIVE_FORMATION` reads are allowed only for formation/instrumentation
  purposes.
- `ARCHIVE_VALIDATION` reads require registration metadata.
- `ARCHIVE_HOLDOUT` reads are denied even if request metadata is supplied,
  until a future explicit unlock artifact changes the boundary state.

## Next Task

Proceed to P1A-004: Archive Baseline Specification Registration.

P1A-004 should register the first baseline specification shape and hash against
this boundary before any strategy, portfolio, archive evaluation, Growth/RDL,
live, OOS, or performance-claim implementation begins.
