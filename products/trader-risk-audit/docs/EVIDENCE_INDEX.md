# Evidence Index - Trader Risk Audit

Version: 1.0
Last updated: 2026-05-08

This file indexes durable proof so agents can retrieve evidence quickly. It is not authoritative by itself; every row must point to the real artifact.

---

## When To Use

Maintain this file because Trader Risk Audit has a heavy P&L attribution task and will accumulate pilot evidence, golden fixtures, and phase review reports.

## Evidence Table

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|
| T01 Project Skeleton | Test suite | `tests/test_project_skeleton.py` | package version, module version command, live-trading config guardrails | 2026-05-07 | Yes |
| T02 CI Setup | Test suite | `tests/test_ci_contract.py` | Python 3.12 CI contract, editable install, lint/format/test steps, no runtime credential names | 2026-05-07 | Yes |
| T03 Baseline Smoke Tests | Test suite | `tests/test_baseline_smoke.py` | import-time dependency boundary, CLI command surface, shared tracer interface | 2026-05-07 | Yes |
| T04 Canonical Trade Schema | Test suite and fixture | `tests/unit/trades/test_trade_schema.py`, `tests/fixtures/trades/valid_trades.csv` | stable trade row ids, canonical missing-field errors, side alias normalization/rejection | 2026-05-07 | Yes |
| T05 Trade Export Importer | Test suite and fixtures | `tests/unit/trades/test_importers.py`, `tests/fixtures/trades/supported_export.csv`, `tests/fixtures/trades/missing_columns_export.csv` | supported CSV normalization, missing source column errors, byte-identical JSON serialization | 2026-05-07 | Yes |
| T06 Risk Policy Schema | Test suite and fixtures | `tests/unit/policy/test_policy_schema.py`, `tests/fixtures/policies/valid_policy.yaml`, `tests/fixtures/policies/unsupported_rule_policy.yaml` | required policy fields, unsupported rule type errors, stable rule ids in serialization | 2026-05-07 | Yes |
| T07 Policy Review Packet | Test suite and fixture | `tests/unit/policy/test_policy_review.py`, `tests/fixtures/policies/ambiguous_policy.yaml` | ambiguous rule review packets, unresolved evaluation gate, approved deterministic field application with source text preserved | 2026-05-07 | Yes |
| T08 Session Calendar and Aggregates | Test suite and fixture | `tests/unit/evaluation/test_aggregates.py`, `tests/fixtures/trades/aggregate_scenarios.csv` | configured session-date assignment, daily realized P&L net of fees, equity curve peak/current/drawdown after closed trades | 2026-05-07 | Yes |
| T09 Position and Asset Rule Evaluators | Test suite and fixtures | `tests/unit/evaluation/test_position_asset_rules.py`, `tests/fixtures/policies/position_asset_policy.yaml`, `tests/fixtures/trades/position_asset_trades.csv` | forbidden asset source-row violations, max position size exposure/threshold records, unsupported leverage warning without guessed violation | 2026-05-07 | Yes |
| T10 Loss, Drawdown, and Cooldown Evaluators | Test suite and fixtures | `tests/unit/evaluation/test_loss_rules.py`, `tests/fixtures/policies/loss_rules_policy.yaml`, `tests/fixtures/trades/loss_rule_scenarios.csv` | post-breach max daily loss, max drawdown evidence fields, cooldown window violations with explicit threshold semantics | 2026-05-07 | Yes |
| T11 Violation Record Determinism | Test suite | `tests/unit/evaluation/test_violation_records.py` | stable violation ids, deterministic violation serialization order, separate unsupported-data warning serialization | 2026-05-07 | Yes |
| T12 Violation P&L Attribution | Heavy proof: unit, integration, golden expected fixture | `tests/unit/evaluation/test_attribution.py`, `tests/integration/test_attribution_golden.py`, `tests/fixtures/expected/attribution_overlap_expected.json` | top-level row buckets are exclusive, overlapping rule membership does not double count total P&L, fees are included once, non-zero reconciliation delta blocks report generation | 2026-05-07 | Yes |
| T13 Report Model and Summaries | Test suite | `tests/unit/reporting/test_report_model.py` | deterministic report sections, source-traceable violation rows with P&L impact, unsupported warnings represented as limitations | 2026-05-07 | Yes |
| T14 Markdown Report Generator | Test suite and golden fixture | `tests/unit/reporting/test_markdown_report.py`, `tests/fixtures/expected/report_expected.md` | required Markdown headings, violation traceability columns, byte-identical report rendering from the same report model | 2026-05-07 | Yes |
| T15 Claim Guard and Disclaimers | Test suite | `tests/unit/reporting/test_claim_guard.py` | required disclaimer validation, forbidden phrase categories and matches, evidence-backed report language pass path | 2026-05-07 | Yes |
| T16 Artifact Manifest and Reproducible Hashes | Test suite | `tests/unit/artifacts/test_manifest.py` | required artifact hashes, package-version content hash with generated timestamp excluded, missing artifact validation failure | 2026-05-07 | Yes |
| T17 End-to-End Audit CLI | Integration test suite | `tests/integration/test_audit_cli.py` | audit command writes deterministic artifacts and manifest, unresolved policy review blocks report output, repeated runs preserve content hashes | 2026-05-07 | Yes |
| T18 Telegram-Ready Delivery Packet | Test suite | `tests/unit/reporting/test_delivery_packet.py` | delivery packet required fields, character-limit truncation with omitted count, claim guard failure blocks packet generation | 2026-05-07 | Yes |
| T19 Local Retention and Deletion Workflow | Test suite | `tests/unit/storage/test_retention.py` | retention list metadata without raw trade rows, dry-run path reporting without deletion, confirmed delete removed/missing path reporting | 2026-05-07 | Yes |
| T20 Pilot Regression Fixture Pack | Integration test suite and golden fixture pack | `tests/integration/test_pilot_fixture_pack.py`, `tests/fixtures/pilot/`, `tests/fixtures/expected/pilot_*` | anonymized pilot input pack, deterministic end-to-end expected violations/attribution/report/hash outputs, committed fixture identifier scan | 2026-05-07 | Yes |
| T30 Public Sample Source Policy | Policy doc and test suite | `docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md`, `tests/test_public_sample_source_policy.py`, `tests/test_starter_policy_profiles.py` | public/anonymized source rules, required metadata, license/terms checks, privacy and secret rejection, internal/demo evidence labels, outreach readiness gate, starter profile boundaries | 2026-05-08 | Yes |
| T31 Public Sample Evidence Pack | Demo evidence pack and integration test | `demo/public_sample_001/`, `docs/PUBLIC_SAMPLE_EVIDENCE_RU.md`, `tests/integration/test_public_sample_pack.py` | source metadata, transformed public-like rows, hard starter profile policy, generated audit outputs, Telegram packet, manifest hash reproducibility, claim-safe report with at least three risk scenarios, internal/demo labeling | 2026-05-08 | Yes |
| T32 Internal Outreach Readiness Review | Readiness review and test suite | `docs/INTERNAL_VALIDATION_REVIEW_RU.md`, `tests/test_internal_readiness_review.py` | reproducibility/explainability/scenario/demo/claim-safety gate results, separation of internal product confidence from market validation, go decision for manual outreach, concrete risks and stop conditions | 2026-05-08 | Yes |

## Retrieval Rules

- Prefer rows that match the current task's `Context-Refs`, open findings, or heavy-task evidence.
- If an evidence row points to a stale or missing artifact, fix the artifact or mark the row pending until the artifact exists.
- Do not treat a journal note as proof when a test, eval, fixture, or review report exists.
