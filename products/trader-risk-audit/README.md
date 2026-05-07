# Trader Risk Audit Workspace

Purpose:

Primary commercial MVP. A trader uploads executed trades and written risk rules.
The system reports deterministic rule violations and their P&L impact.

## Core Promise

Upload trades plus rules. Receive an audit report showing what rules were
violated, when they were violated, and how much damage violations created.

## Current Status

- Current phase: Phase 5 - Concierge Pilot Workflow.
- Completed: Phase 1 foundation, Phase 2 input contracts, Phase 3 rule evaluation, Phase 4 reporting/artifacts, and Phase 5 concierge pilot workflow.
- Local baseline: 61 passing tests, 0 skipped.
- Quality checks: `ruff check trader_risk_audit tests` and `ruff format --check trader_risk_audit tests` are clean.
- Review status: Phase 5 deep review archived at `docs/archive/PHASE5_REVIEW.md`; Stop-Ship: No.

## Features

| Area | Status | Notes |
|------|--------|-------|
| Package skeleton | Complete | `python -m trader_risk_audit --version` is available. |
| CLI command surface | Partial | `audit` runs the local deterministic workflow and `retention` manages manifest-referenced files; `manifest` remains a stub. |
| Config guardrails | Complete | Live broker API and order-blocking flags are rejected for v1. |
| CI contract | Complete | GitHub Actions installs editable package, runs ruff lint, ruff format check, and pytest. |
| Canonical trade schema | Complete | `TradeRecord` validates canonical fields, normalizes sides, and exposes stable row ids. |
| Trade importer | Complete | Supported local CSV exports normalize into sorted canonical records with deterministic JSON serialization. |
| Risk policy schema | Complete | Pydantic/PyYAML policy loading validates version, account scope, session, and supported rule types. |
| Policy review packet | Complete | Ambiguous policy mappings produce review packets and unresolved packets block evaluation. |
| Session aggregates | Complete | Configured session dates, daily realized P&L, exposure totals, and equity curve inputs are implemented. |
| Position/asset evaluators | Complete | Forbidden asset and max position size violations are source-traceable; missing leverage emits unsupported-data warnings. |
| Loss/drawdown/cooldown evaluators | Complete | Daily loss, drawdown, and cooldown rules use explicit strict breach semantics and source-row violations. |
| Violation determinism | Complete | Violation ids are stable hashes and violation/warning serialization is deterministic. |
| Violation P&L attribution | Complete | Top-level row buckets are exclusive, overlapping rule summaries reconcile, and golden evidence is checked. |
| Report model | Complete | Deterministic report sections, violation rows, attribution summary, limitations, and next-review checklist are modeled. |
| Markdown report generator | Complete | Report models render to deterministic Markdown with traceable violation tables and golden fixture coverage. |
| Claim guard | Complete | Reports include the required disclaimer and deterministic validation blocks unsupported advice, performance, live-control, and causal claim phrases. |
| Artifact manifest | Complete | Required inputs and outputs are hashed; content hashes exclude generated timestamps and local paths. |
| End-to-end audit CLI | Complete | Local `audit` writes normalized trades, violations, attribution, report Markdown, and manifest artifacts. |
| Telegram-ready delivery packet | Complete | Copyable local text includes summary, violation counts, P&L, limitations, disclaimer, and report path without sending messages. |
| Retention/delete workflow | Complete | Manifest artifact groups can be listed, dry-run deleted, or deleted with explicit confirmation. |
| Pilot regression fixture pack | Complete | Anonymized end-to-end fixtures pin deterministic violations, attribution, report, and manifest hashes. |

## Tests

| Command | Current Result |
|---------|----------------|
| `.venv/bin/python -m pytest tests -q --tb=short` | 61 passed |
| `.venv/bin/python -m ruff check trader_risk_audit tests` | passed |
| `.venv/bin/python -m ruff format --check trader_risk_audit tests` | passed |

## Scope In

- Manual pilot reports.
- Trade export normalization.
- Risk policy input.
- Deterministic violation evaluation.
- Violation attribution.
- Markdown/PDF/Telegram-ready report packets.

## Scope Out

- Live broker/exchange APIs.
- Order blocking.
- Full SaaS dashboard.
- Strategy backtesting platform.
- AI-generated trading strategies.
- Public marketplace.

## Read First

1. `docs/CODEX_PROMPT.md`
2. `docs/tasks.md`
3. `../../docs/PRODUCT_PORTFOLIO.md`
4. `../../docs/AI_DEVELOPMENT_OPERATING_MODEL.md`

## Local AI Workflow

This workspace has its own `PLAYBOOK.md`, `prompts/`, `templates/`, `hooks/`,
`ci/`, prompts, hooks, and Codex tmux operating materials. Do not rely on root-level workflow files or legacy nested-agent assumptions
for Trader Risk Audit development.

## Repository Layout

```text
trader_risk_audit/
  __init__.py
  __main__.py
  cli.py
  config.py
  artifacts/
    __init__.py
    manifest.py
  evaluation/
    __init__.py
    aggregates.py
    attribution.py
    calendar.py
    rules.py
    violations.py
  observability.py
  policy/
    __init__.py
    review.py
    schema.py
    validation.py
  reporting/
    __init__.py
    claim_guard.py
    delivery.py
    markdown.py
    model.py
  storage/
    __init__.py
    retention.py
  trades/
    __init__.py
    importers.py
    schema.py
tests/
  fixtures/trades/missing_columns_export.csv
  fixtures/trades/supported_export.csv
  fixtures/trades/valid_trades.csv
  fixtures/policies/valid_policy.yaml
  fixtures/policies/unsupported_rule_policy.yaml
  fixtures/policies/ambiguous_policy.yaml
  fixtures/trades/aggregate_scenarios.csv
  fixtures/trades/position_asset_trades.csv
  fixtures/trades/loss_rule_scenarios.csv
  fixtures/trades/attribution_overlap.csv
  fixtures/pilot/trades.csv
  fixtures/pilot/policy.yaml
  fixtures/expected/attribution_overlap_expected.json
  fixtures/expected/report_expected.md
  fixtures/expected/pilot_violations.json
  fixtures/expected/pilot_attribution.json
  fixtures/expected/pilot_report.md
  fixtures/expected/pilot_manifest_hashes.json
  fixtures/policies/position_asset_policy.yaml
  fixtures/policies/loss_rules_policy.yaml
  test_baseline_smoke.py
  test_ci_contract.py
  test_project_skeleton.py
  unit/trades/test_trade_schema.py
  unit/trades/test_importers.py
  unit/policy/test_policy_schema.py
  unit/policy/test_policy_review.py
  unit/evaluation/test_aggregates.py
  unit/evaluation/test_position_asset_rules.py
  unit/evaluation/test_loss_rules.py
  unit/evaluation/test_violation_records.py
  unit/evaluation/test_attribution.py
  unit/reporting/test_report_model.py
  unit/reporting/test_markdown_report.py
  unit/reporting/test_claim_guard.py
  unit/reporting/test_delivery_packet.py
  unit/artifacts/test_manifest.py
  unit/storage/test_retention.py
  integration/test_attribution_golden.py
  integration/test_audit_cli.py
  integration/test_pilot_fixture_pack.py
docs/
  ARCHITECTURE.md
  CODEX_PROMPT.md
  IMPLEMENTATION_CONTRACT.md
  audit/
  archive/
.github/workflows/ci.yml
pyproject.toml
requirements.txt
requirements-dev.txt
```
