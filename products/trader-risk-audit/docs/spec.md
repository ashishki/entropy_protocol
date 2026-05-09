# Specification - Trader Risk Audit

Version: 1.1
Last updated: 2026-05-09
Status: Draft

---

## Overview

Trader Risk Audit turns a trader's executed trade export and written risk rules into a deterministic audit packet. The packet identifies rule violations, shows source trade rows and timestamps, summarizes violation-attributed P&L, and produces a Markdown report plus a Telegram-ready delivery summary for concierge pilots.

## User Roles

| Role | Capabilities |
|------|--------------|
| Trader | Provides trade exports, written risk rules, timezone/session definition, and optional notes; receives audit report and follow-up checklist. |
| Operator | Normalizes supported exports, resolves ambiguous inputs with the trader, approves policy interpretation, runs local audit workflow, and reviews reports before delivery. |
| Reviewer | Checks that violation records, P&L attribution, report language, and artifact manifests match the deterministic evidence. |
| Developer | Implements and maintains deterministic import, validation, evaluation, attribution, reporting, and workflow tooling. |

## Feature Area 1 - Project Skeleton and Local CLI

Description: Provide a Python package, local CLI entry point, configuration loader, shared observability module, and initial smoke test structure so future tasks can add domain behavior without changing project boundaries.

Acceptance criteria:

1. `python -m trader_risk_audit --version` exits with code 0 and prints the package version.
2. The CLI exposes an `audit` command with `--trades`, `--policy`, and `--output-dir` options before domain execution is wired.
3. Configuration defaults point to local directories and reject enabled live broker or order-blocking flags.
4. The shared observability module exports a single `get_tracer()` function and logging helpers do not emit raw file contents.

Out of scope for v1:

- Hosted API server.
- User accounts or authentication flows.
- Background workers or scheduled jobs.

## Feature Area 2 - Trade Export Normalization

Description: Parse supported CSV/XLSX trade exports into a canonical trade schema that downstream rule evaluators can process deterministically.

Acceptance criteria:

1. Supported input rows normalize into records with `row_id`, `timestamp`, `symbol`, `side`, `quantity`, `price`, `fees`, `account_id`, and `source_file`.
2. Missing required fields return validation errors listing the missing canonical fields and source column names inspected.
3. Timestamp parsing requires an explicit timezone or timezone-aware source value.
4. Re-running normalization on the same file and config produces byte-identical normalized JSON output.
5. Fixtures contain only anonymized account, symbol, and note values.

Out of scope for v1:

- Live broker import APIs.
- Automatic inference of unsupported broker-specific semantics.
- OCR or screenshot extraction.

## Feature Area 3 - Risk Policy Schema

Description: Represent trader-written rules as a versioned risk policy file that can be reviewed by a human and evaluated by deterministic rule engines.

Acceptance criteria:

1. Policy files declare schema version, account scope, timezone/session definition, and a list of rule objects.
2. Supported rule types include max daily loss, max drawdown, cooldown after loss threshold, max position size, forbidden assets, and max leverage when leverage fields are present.
3. Unsupported rule types fail validation with the unsupported type and rule id.
4. Ambiguous trader-written rules are recorded in a review packet and are not evaluated until the operator supplies an approved deterministic policy mapping.
5. Rule ids are stable and appear unchanged in violations, reports, and manifests.

Out of scope for v1:

- AI-owned final policy interpretation.
- Strategy adherence scoring beyond manually approved rule mappings.
- Auto-generated trading or risk rules.

## Feature Area 4 - Deterministic Rule Evaluation

Description: Evaluate normalized trades against approved policies and emit violation records with complete source evidence.

Acceptance criteria:

1. Each violation record contains `violation_id`, `rule_id`, `rule_type`, `source_row_ids`, `timestamp`, `evaluated_value`, `threshold`, `severity`, and `message_code`.
2. Max daily loss flags trades that occur after the configured realized daily loss threshold is breached.
3. Max drawdown flags trades after the configured equity drawdown threshold is breached.
4. Cooldown flags trades opened inside a configured cooldown window after a qualifying loss event.
5. Max position size flags rows where normalized absolute exposure exceeds the policy limit.
6. Forbidden assets flags rows whose normalized symbol matches the policy's forbidden set.
7. Max leverage flags rows only when leverage input fields are present; missing leverage fields produce an explicit unsupported-data warning, not a guessed violation.
8. The same normalized trades and policy produce identical violation JSON across repeated runs.

Out of scope for v1:

- Intraday live monitoring.
- Order rejection or pre-trade checks.
- Probabilistic or LLM-scored violations.

## Feature Area 5 - Violation P&L Attribution

Description: Summarize compliant versus violating P&L without double counting rows that trigger multiple violations.

Acceptance criteria:

1. Every trade row contributes to at most one primary P&L bucket in the top-level compliant versus violating summary.
2. Rule-level summaries can show overlapping violation membership while the top-level total remains reconciled to total realized P&L.
3. Attribution output includes total P&L, compliant P&L, violating P&L, unclassified P&L, and reconciliation delta.
4. Any non-zero reconciliation delta fails the audit command before report generation.
5. Golden fixtures document expected attribution values for representative overlap scenarios.

Out of scope for v1:

- Tax lot accounting.
- Slippage simulation.
- Counterfactual "what would have happened" claims.

## Feature Area 6 - Report Generation and Claim Guard

Description: Generate a Markdown audit report and Telegram-ready summary packet from deterministic artifacts while blocking unsupported claims.

Acceptance criteria:

1. Markdown reports include input summary, policy summary, violation table, repeated patterns, worst violation days, P&L attribution, limitations, and next-review checklist.
2. Each violation row in the report includes rule id, timestamp, source row ids, evaluated value, threshold, and P&L impact where available.
3. Report text includes the configured disclaimer that the audit is not investment advice and does not control live trading.
4. Claim guard rejects report text containing configured forbidden phrases for profit promises, live order control, or unsupported causal assertions.
5. Telegram-ready output stays below the configured character limit and links to the local report artifact path.

Out of scope for v1:

- Public dashboards.
- Automated paid delivery.
- PDF generation unless Markdown delivery proves insufficient in pilots.

## Feature Area 7 - Artifact Manifest and Reproducibility

Description: Produce a manifest that lets an operator or reviewer confirm which inputs, outputs, and code version generated a report.

Acceptance criteria:

1. Manifest records hashes for source export, policy file, normalized trades, violations, attribution summary, report, and delivery packet.
2. Manifest records package version, command arguments, generated artifact paths, and generation timestamp.
3. Output hash calculation excludes volatile fields such as generation timestamp.
4. Re-running the same immutable inputs produces the same normalized, violation, attribution, and report content hashes.
5. Manifest validation fails if any referenced artifact is missing.

Out of scope for v1:

- Remote evidence storage.
- Blockchain or external notarization.
- Multi-user audit history search.

## Feature Area 8 - Local Retention and Deletion

Description: Keep pilot data local by default and give the operator a deterministic way to delete or archive an audit input/output set on request.

Acceptance criteria:

1. The retention command lists audit artifact groups by manifest id without printing raw trade data.
2. The delete command removes all files referenced by a manifest after an explicit operator confirmation argument.
3. Deletion output lists file paths removed and file paths that were already absent.
4. A dry-run mode reports the same path set without deleting files.
5. No committed test fixture contains real trader identity, broker account id, or customer export data.

Out of scope for v1:

- Hosted retention policy enforcement.
- Legal hold workflow.
- Customer self-service deletion portal.

## Feature Area 9 - Local Read-Only Exchange Import

Description: Provide a bounded local import path for sanitized or approved
read-only exchange execution history so the existing deterministic audit engine
can consume normalized exchange trades.

Acceptance criteria:

1. Raw exchange snapshots record exchange, market/category, symbols, explicit
   time range, fetched pages, endpoint labels, and raw records without
   credentials.
2. Exchange import manifests hash the raw snapshot and normalized output while
   excluding generated timestamps from deterministic content hashes.
3. Exchange normalizers map raw fills/executions into canonical `TradeRecord`
   objects without changing evaluator semantics.
4. Fixture-backed import writes raw snapshot, normalized trade CSV, and import
   manifest artifacts that the existing `audit` command can consume.
5. Read-only permission checks reject detectable order-write, withdrawal,
   transfer, leverage/margin, or account-mutation permissions before real
   connector use.

Out of scope for v1:

- Exchange order placement, amend, cancel, or close-position calls.
- Withdrawals, transfers, leverage/margin changes, hosted secret storage, or
  Telegram credential collection.
- Real exchange network calls before the specific Bybit/Binance connector tasks
  and safety gates approve them.
- Portfolio tracking, live alerts, signal analytics, order blocking, trading
  advice, or AI-owned violation truth.
