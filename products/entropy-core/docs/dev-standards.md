# Development Standards - Entropy Core

Version: 1.0
Last updated: 2026-05-07

## Code Style

- Use Python 3.12.
- Keep registry, leakage, attribution, governance, and report claim logic deterministic.
- Use Pydantic v2 for external schemas and typed domain models.
- Use `src/entropy/tracing.py` for spans.
- Do not introduce a second runtime or native extension without the language escalation gate.

## Tests

- Every task acceptance criterion must map to one pytest function.
- Use isolated temporary filesystem and database state.
- Heavy tasks must update `docs/EVIDENCE_INDEX.md`.
- Keep reset tests under `tests/reset/` when they verify workflow/tooling contracts rather than product behavior.

## Data and Claims

- No live broker/exchange credentials in fixtures or CI.
- No holdout read unless explicitly approved.
- No OOS/performance, production, or capital-ready labels without gate evidence.
- Reports and evidence packets must distinguish scaffold, archive-only, and admissible evaluation states.
