# Development Standards - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-07

---

## Code Style

- Use Python 3.12.
- Keep functions small and deterministic where they touch trade normalization, rule evaluation, attribution, reports, or manifests.
- Prefer Pydantic models for external input schemas and dataclasses or typed models for internal deterministic records.
- Do not import heavy data libraries at package import time; import them inside importer modules as needed.
- Use `trader_risk_audit/observability.py` for tracing boundaries.

## Tests

- Every task acceptance criterion must have a named pytest test.
- Unit tests cover pure schema, validation, evaluator, attribution, report, and manifest logic.
- Integration tests cover CLI paths and golden fixtures.
- Tests use temporary directories for generated artifacts.
- Fixtures must be anonymized and scanned for customer identifiers before commit.

## Data Handling

- Real customer exports stay outside source control.
- Logs and test output may include counts, hashes, rule ids, and message codes only.
- Do not print raw trade rows, account balances, broker account ids, or free-text notes.

## Reports

- Customer-facing reports are generated from deterministic report models.
- Claim guard validation is required before delivery packet generation.
- Disclaimers are mandatory in any customer-facing report.

## Commits

- One logical change per commit.
- Use `type(scope): description`.
- No AI co-author lines.
- No TODO without a task reference.
