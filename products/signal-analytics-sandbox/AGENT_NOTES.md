# Agent Notes — Signal Analytics Sandbox

Date: 2026-05-07
Agent: Codex

## Investigation Summary

- Product path inspected: `products/signal-analytics-sandbox/`.
- Current product state is planning/governance first, implementation not started.
- `docs/ARCHITECTURE.md` specifies a local-first Python 3.12 library + CLI named `signal-sandbox`.
- `docs/tasks.md` defines Phase 0 as human-owned gates and Phase 1 as the first engineering skeleton.
- `docs/CODEX_PROMPT.md §Phase 0 Gate Status` still marks both gates as `pending`:
  - SAS-001 paid pilot demand validation.
  - SAS-002 public-source legal / terms memo.
- `RUNBOOK.md` reports no package manager, build command, dev server, or CLI; the only supported validation command is the product-local unittest command.

## Setup Verification

Supported validation command after this session:

```bash
cd products/signal-analytics-sandbox && .venv/bin/python -m unittest discover -s tests -v
```

Result on 2026-05-07:

- 7 tests passed.
- No external package manager or network access required.

## Decisions

- Did not start T01 or any product implementation because `IMPLEMENTATION_CONTRACT.md §PSR-10` forbids engineering tasks until SAS-001 and SAS-002 are acknowledged by the operator.
- Added a product-local standard-library validation suite instead of adding runtime implementation.
- Fixed the safest validated issue found: `hooks/guard_phase_boundary.sh` did not recognize the product's current phase-line format with parenthetical text.
- Extended validation coverage for `hooks/guard_phase_boundary.sh` so it blocks cross-phase advancement through the `Next Task` pointer, not only direct phase-line edits.

## 2026-05-07 Update

- Operator acknowledged SAS-001 and SAS-002 for initial Telegram pilot sources:
  `https://t.me/bablos79`, `https://t.me/nemphiscrypts`, `https://t.me/pifagortrade`.
- Created `docs/PILOT_LOG.md` and `docs/legal_risk_memo.md`.
- Updated `docs/CODEX_PROMPT.md` gate state to `acknowledged`.
- Wrote `docs/audit/PHASE1_AUDIT.md` with PASS.
- Completed T01 Project Skeleton:
  - `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`
  - `src/signal_sandbox/` package and subpackages
  - click-based `signal-sandbox` console script
  - shared `src/signal_sandbox/observability.py:get_tracer()`
  - T01 unit/integration tests
- Validation after T01: 11 pytest passed; ruff check passed; ruff format check passed; pyright passed.
- Completed T02 CI Setup:
  - added `tests/unit/test_ci_workflow.py`
  - verified workflow trigger branches, Python 3.12, pip cache, CI command order, install command, and dev dependencies
  - added repository-root `.github/workflows/signal-analytics-sandbox-ci.yml` so GitHub can actually run this product's CI in the monorepo
  - validation after CI bridge: 18 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T03 Phase 1 Smoke Tests:
  - added `tests/unit/test_observability.py`
  - added structured JSON logger helpers in `src/signal_sandbox/observability.py`
  - extended `tests/integration/test_cli_smoke.py` with temp-workspace `status`
  - validation after T03/root CI bridge: 18 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 1 deep review completed and archived at `docs/archive/PHASE1_REVIEW.md`.
- `docs/audit/AUDIT_INDEX.md` has Cycle 1 / Phase 1 archive row.
- Completed T04 SourceManifest Pydantic Schema:
  - added `src/signal_sandbox/sources/manifest.py`
  - added `tests/unit/test_source_manifest.py`
  - validation after T04: 22 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T05 Capture Loader:
  - added `src/signal_sandbox/capture/loader.py`
  - added `src/signal_sandbox/sources/private_patterns.py`
  - added `tests/unit/test_capture_loader.py`
  - validation after T05: 26 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T06 SignalRecord Schema:
  - added `src/signal_sandbox/ledger/record.py`
  - added `tests/unit/test_signal_record.py`
  - validation after T06: 31 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 2 deep review completed and archived at `docs/archive/PHASE2_REVIEW.md`.
- `docs/audit/AUDIT_INDEX.md` has Cycle 2 / Phase 2 archive row.
- Completed T07 Ledger I/O (Parquet):
  - added `src/signal_sandbox/ledger/io.py`
  - added `tests/unit/test_ledger_io.py`
  - validation after T07: 35 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T08 Dedup + Ambiguity Flagging:
  - added `src/signal_sandbox/ledger/dedup.py`
  - added `tests/unit/test_dedup.py`
  - validation after T08: 38 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 3 deep review completed and archived at `docs/archive/PHASE3_REVIEW.md`.
- Accepted ADR-001: deterministic Parquet snapshot bytes with rows sorted by asset/timestamp, fixed columns, zstd compression, and statistics disabled.
- Completed T09 PriceDataProvider Abstract Interface:
  - added `src/signal_sandbox/prices/base.py`
  - added `tests/unit/test_price_provider_base.py`
  - validation after T09: 41 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T10 OperatorFilePriceProvider:
  - added `src/signal_sandbox/prices/operator_file.py`
  - added `tests/integration/test_operator_file_provider.py`
  - validation after T10: 44 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T11 PriceSnapshot Persistence + Provenance:
  - added `src/signal_sandbox/prices/snapshot.py`
  - added `tests/unit/test_snapshot_persistence.py`
  - validation after T11: 47 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 4 deep review completed and archived at `docs/archive/PHASE4_REVIEW.md`.
- Completed T12 Outcome Matching Engine:
  - added `src/signal_sandbox/outcomes/matcher.py`
  - added `src/signal_sandbox/outcomes/rule_registry.py`
  - added `tests/integration/test_outcome_matcher.py`
  - wrote `docs/audit/HEAVY_T12_EVIDENCE.md`
  - validation after T12: 55 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T13 Aggregator:
  - added `src/signal_sandbox/outcomes/aggregate.py`
  - added `tests/unit/test_aggregator.py`
  - validation after T13: 59 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Completed T14 Markdown Report Generator:
  - added `src/signal_sandbox/reports/disclaimers.py`
  - added `src/signal_sandbox/reports/markdown.py`
  - added `tests/integration/test_report_generator.py`
  - wrote `docs/audit/HEAVY_T14_EVIDENCE.md`
  - validation after T14: 65 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Phase 5 deep review completed and archived at `docs/archive/PHASE5_REVIEW.md`.
- Completed T15 ExtractionAdapter ABC:
  - added `src/signal_sandbox/extraction/base.py`
  - added `tests/unit/test_extraction_base.py`
  - validation after T15: 68 pytest passed; ruff check passed; ruff format check passed; pyright passed
- Next task: T16 ManualExtractionAdapter.

## Technical Risks

1. Phase 0 gates are still pending, so core implementation is intentionally blocked.
2. There is no Python package skeleton yet (`pyproject.toml`, `src/`, `tests/unit`, and `tests/integration` are absent), so the architecture and Phase 1 CI expectations are not executable.
3. Product-local CI files exist, but the currently planned CI commands depend on files that do not exist until T01/T02. Treat CI as a Phase 1 deliverable, not a verified setup.
4. The product-local `.github/workflows/ci.yml` lives under the product directory; in a monorepo it will not be picked up by GitHub unless copied or bridged from the repository root.
5. Hook behavior is now lightly covered, but only the highest-risk governance checks have tests. More hook cases should be added before relying on the workflow heavily.

## Minimal Improvement Plan

1. Keep the new workspace validation suite as the pre-engineering setup check.
2. Operator completes SAS-001 and SAS-002, then acknowledges both rows in `docs/CODEX_PROMPT.md`.
3. Start T01 exactly as written in `docs/tasks.md`: package skeleton, CLI stubs, shared observability module, and smoke tests.
4. During T02, reconcile the CI workflow location and commands with the monorepo layout.
5. Update `RUNBOOK.md` again once real pytest/ruff/pyright commands exist.

## Unresolved Follow-Up

- Decide whether this product should have a root-level workflow entry that delegates into `products/signal-analytics-sandbox/`, or whether product-local workflows are only templates.
