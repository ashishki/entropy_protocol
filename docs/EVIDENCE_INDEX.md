# Evidence Index — Entropy Protocol

_Proof lookup across reviews, evals, and heavy tasks. Retrieval convenience only — points to canonical artifacts._
_Required because this project has heavy tasks (T16, T17, T18, T19, T20, T21, T22) and cross-phase evidence expectations._

---

## Heavy Task Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|---------|--------|------|
| T16 (SimBroker Fill Engine) | Determinism + no-lookahead + bar-range constraint | tests/unit/test_simbroker.py::test_fill_engine_determinism; tests/unit/test_simbroker.py::test_fill_engine_no_lookahead; tests/unit/test_simbroker.py::test_fill_constrained_to_bar_high; tests/unit/test_simbroker.py::test_fill_constrained_to_bar_low; tests/unit/test_simbroker.py::test_fill_unconstrained_within_bar; tests/unit/test_simbroker.py::test_fill_log_has_all_required_fields | Passing locally | 2026-05-03 |
| T17 (Calibration Interface) | Abstract interface enforcement + no-op mock | tests/unit/test_simbroker.py::test_bid_ask_provider_is_abstract; tests/unit/test_simbroker.py::test_noop_bid_ask_provider_returns_none; tests/unit/test_simbroker.py::test_noop_is_valid_subclass | Passing locally | 2026-05-03 |
| T18 (IS/OOS Splitter) | Strict IS/OOS boundary + exact N-bar embargo + leakage boundary test | tests/integration/test_walk_forward.py::test_splitter_is_window_ends_before_embargo; tests/integration/test_walk_forward.py::test_embargo_excludes_correct_bars; tests/integration/test_walk_forward.py::test_no_future_leakage | Passing locally | 2026-05-03 |
| T19 (Leakage Detection) | Four-check leakage checklist PASS/FAIL evidence, including missing-detector FAIL | tests/integration/test_leakage.py::test_full_leakage_checklist; tests/integration/test_leakage.py::test_full_leakage_checklist_requires_all_checks; tests/integration/test_leakage.py::test_leakage_normalization_detected; tests/integration/test_leakage.py::test_leakage_regime_lookahead_detected; tests/integration/test_leakage.py::test_leakage_universe_selection_detected; tests/integration/test_leakage.py::test_leakage_within_window_optimization_detected | Passing locally | 2026-05-03 |
| T20 (Walk-Forward Runner) | RunRecord hashes + missing/non-PASS leakage gates + DB persistence | tests/integration/test_walk_forward.py::test_runner_produces_run_record_with_all_hashes; tests/integration/test_walk_forward.py::test_runner_blocks_oos_before_leakage_check; tests/integration/test_walk_forward.py::test_runner_blocks_oos_when_leakage_check_fails; tests/integration/test_walk_forward.py::test_runner_persists_run_record_to_db; tests/integration/test_walk_forward.py::test_runner_rejects_missing_code_hash | Passing locally | 2026-05-03 |
| T21 (P&L Attribution) | Four-stream attribution + stream boundary + drawdown + stub metrics | tests/unit/test_attribution.py::test_four_stream_worked_example; tests/unit/test_attribution.py::test_net_sharpe_excludes_stream_d; tests/unit/test_attribution.py::test_drawdown_record_worked_example; tests/unit/test_attribution.py::test_net_sharpe_numerical_accuracy; tests/unit/test_attribution.py::test_performance_metrics_stub_fields | Passing locally | 2026-05-03 |
| T22 (P1/P3 State Machine) | Synthetic circuit-breaker test suite | tests/unit/test_governance.py::test_p1_circuit_breaker_suite | Not started | — |

## Phase Gate Evidence

| Phase | Gate | Artifact | Status | Date |
|-------|------|---------|--------|------|
| Phase 0 (v1) | All T01-T24 pass; no OOS claims before T19 passes | docs/audit/CYCLE{N}_REVIEW.md | Not started | — |
| Phase 2 | T04-T06 complete; no P0/P1 in scoped boundary review | docs/audit/PHASE2_REVIEW.md | Passing locally | 2026-05-03 |
| Phase 3 | T07-T08 complete; no P0/P1 in scoped boundary review | docs/audit/PHASE3_REVIEW.md | Passing locally | 2026-05-03 |
| Phase 4 | T09-T11 complete; no P0/P1 in scoped boundary review | docs/audit/PHASE4_REVIEW.md | Passing locally | 2026-05-03 |
| Phase 5 | T12-T14 complete; no new P0/P1 in scoped boundary review; T15 blocked by D-010 | docs/audit/PHASE5_REVIEW.md | Passing locally; blocked before T15 | 2026-05-03 |
| Phase 6 | T15-T17 complete; no new open P0/P1/P2 in scoped boundary review | docs/audit/PHASE6_REVIEW.md | Passing locally | 2026-05-03 |
| Phase 7 | T18-T20 complete; WF-P1-01 remediated; T21 stopped pending formula-governance disposition | docs/audit/PHASE7_REVIEW.md | Passing locally; blocked before T21 | 2026-05-03 |

## Domain Model Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T05 (Registry and Run Models) | TrialSpec, RunRecord, FillLog, GovernanceEvent validation | tests/unit/test_models.py::test_trial_spec_requires_all_hash_fields; tests/unit/test_models.py::test_trial_spec_requires_family_tag; tests/unit/test_models.py::test_run_record_requires_simbroker_version; tests/unit/test_models.py::test_fill_log_cost_fields_nonnegative; tests/unit/test_models.py::test_governance_event_validates_event_type | Passing locally | 2026-05-03 |
| T06 (Performance Models) | PnL stream boundary, NetSharpe method, drawdown validation, explicit stub reason code | tests/unit/test_models.py::test_pnl_streams_net_sharpe_excludes_stream_d; tests/unit/test_models.py::test_net_sharpe_requires_canonical_method_id; tests/unit/test_models.py::test_drawdown_record_validates_values; tests/unit/test_models.py::test_performance_metrics_allows_stub_fields | Passing locally | 2026-05-03 |
| P2-03 | get_tracer return type corrected to Tracer | entropy/tracing.py; `.venv/bin/pyright --pythonpath .venv/bin/python entropy/` | Passing locally | 2026-05-03 |

## Database Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T07 (Database Schema + Alembic Migrations) | PostgreSQL 16 migration upgrade/schema/downgrade checks | tests/integration/test_registry_db.py::test_alembic_upgrade_creates_all_tables; tests/integration/test_registry_db.py::test_trial_registry_schema; tests/integration/test_registry_db.py::test_runs_table_schema; tests/integration/test_registry_db.py::test_governance_events_schema; tests/integration/test_registry_db.py::test_alembic_downgrade_reverts_migration | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |
| T-DB-1 / P2-04 | PostgreSQL fixture rollback isolation | tests/integration/test_fixture_isolation.py::test_postgres_fixture_rolls_back_on_teardown | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |
| T09 (Trial Registry Write Path) | Valid insert, missing hash rejection, duplicate rejection, parameterized/no UPDATE/DELETE inspection | tests/integration/test_registry_db.py::test_write_valid_trial_spec_inserts_row; tests/integration/test_registry_db.py::test_write_rejects_missing_dataset_hash; tests/integration/test_registry_db.py::test_write_rejects_duplicate_trial_id; tests/unit/test_registry.py::test_write_path_uses_parameterized_sql; tests/unit/test_registry.py::test_write_path_issues_no_update_or_delete | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |
| T10 (Experiment Readiness Gate) | Ready, missing hash/family, duplicate family, and unknown-trial readiness outcomes | tests/unit/test_registry.py::test_gate_returns_ready_for_complete_trial; tests/unit/test_registry.py::test_gate_lists_missing_dataset_hash; tests/unit/test_registry.py::test_gate_lists_missing_family_tag; tests/unit/test_registry.py::test_gate_detects_duplicate_trial_id; tests/unit/test_registry.py::test_gate_raises_for_unknown_trial_id | Passing locally | 2026-05-03 |
| T11 (Trial Registry Read Path) | Read by trial_id, family, status, family count, and no-write guard | tests/unit/test_registry.py::test_read_by_trial_id_found_and_not_found; tests/unit/test_registry.py::test_read_by_family_returns_correct_list; tests/unit/test_registry.py::test_read_by_status_filters_correctly; tests/unit/test_registry.py::test_count_trials_in_family_includes_all_statuses; tests/unit/test_registry.py::test_read_path_issues_no_writes | Passing locally | 2026-05-03 |

## Hashing Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T08 (Deterministic Hashing) | Row-order independent dataset hash, row/schema change detection, deterministic run/policy hashes | tests/unit/test_hashing.py::test_dataset_hash_is_row_order_independent; tests/unit/test_hashing.py::test_dataset_hash_detects_row_change; tests/unit/test_hashing.py::test_dataset_hash_detects_schema_change; tests/unit/test_hashing.py::test_run_hash_is_deterministic; tests/unit/test_hashing.py::test_policy_hash_is_key_order_independent | Passing locally | 2026-05-03 |

## Observability Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T-OBS-2 / P2-02 | Tracing and metrics helper unit tests | tests/unit/test_observability.py::test_get_tracer_does_not_raise; tests/unit/test_observability.py::test_increment_counter_does_not_raise; tests/unit/test_observability.py::test_record_histogram_does_not_raise; tests/unit/test_observability.py::test_get_tracer_return_annotation_is_tracer_interface | Passing locally | 2026-05-03 |
| T-OBS-1 / P2-01 | `entropy health` ok/degraded JSON and exit-code behavior | tests/unit/test_cli.py::test_health_command_ok; tests/unit/test_cli.py::test_health_command_degraded_no_postgres; tests/unit/test_cli.py::test_health_command_output_is_valid_json; manual `.venv/bin/entropy health` checks | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |

## Documentation Evidence

| Finding | Evidence Type | Artifact | Status | Date |
|---------|--------------|----------|--------|------|
| P2-05 | ADR governance path bootstrap | docs/adr/README.md | Updated | 2026-05-03 |
| P2-06 | Architecture component table coverage | docs/ARCHITECTURE.md §Component Table | Updated | 2026-05-03 |
| P2-07 | ERA0 authority status | docs/core/ERA0_SPEC.md §Authority Status | Updated | 2026-05-03 |
| P2-08 | Documentation map and current phase clarity | docs/README.md §Documentation Map; docs/README.md §Current Phase | Updated | 2026-05-03 |
| T-GOV-2 / D-010 / D-015 / D-016 | Focused T15 blocker evidence: canonical mitigations for F-1/F-2/F-4/F-5; F-30/F-31 future real-evidence gates | docs/audit/D010_CLOSURE_PACKET.md; docs/audit/D010_FOCUSED_AUDIT_F1_F2_F4_F5.md; docs/core/PROTOCOL_SPEC.md v1.8; docs/core/CHARTER.md v5.3; docs/core/GLOSSARY.md v1.4; docs/DECISION_LOG.md D-015/D-016 | Focused audit passed; T15 unblocked for cost-model implementation only; F-30/F-31 not closed and no synthetic closure permitted | 2026-05-03 |
| D-017 / T21 Formula-Governance Disposition | T21 narrow waiver/disposition; F-22 stream wording closure for current canonical implementation scope; T23 statistical helpers remain out of T21 | docs/audit/T21_FORMULA_GOVERNANCE_DISPOSITION.md; docs/DECISION_LOG.md D-017; docs/tasks.md T21 | T21 unblocked under D-017 constraints | 2026-05-03 |

## Data Pipeline Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T12 (Data Ingestion Interface) | DataProvider ABC, concrete/missing method behavior, provider registry, error hierarchy | tests/unit/test_data_quality.py::test_data_provider_is_abstract; tests/unit/test_data_quality.py::test_concrete_provider_instantiates; tests/unit/test_data_quality.py::test_provider_missing_method_raises_type_error; tests/unit/test_data_quality.py::test_provider_registry_get_and_not_found; tests/unit/test_data_quality.py::test_error_hierarchy_inheritance | Passing locally | 2026-05-03 |
| T13 (Local Fixture Adapter + Parquet Store) | CSV fixture parsing, deterministic Parquet write, DB provenance hash match, rollback cleanup, health check | tests/unit/test_data_quality.py::test_fixture_adapter_parses_csv; tests/integration/test_registry_db.py::test_fixture_adapter_writes_parquet; tests/integration/test_registry_db.py::test_fixture_adapter_records_correct_hash; tests/unit/test_data_quality.py::test_fixture_adapter_rolls_back_on_db_failure; tests/unit/test_data_quality.py::test_fixture_adapter_health_check | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |
| T14 (Data Quality Checks) | UTC timestamp enforcement, gap detection, OHLCV sanity, aggregate report | tests/unit/test_data_quality.py::test_validate_timestamps_raises_for_naive_datetime; tests/unit/test_data_quality.py::test_validate_timestamps_raises_for_non_utc_timezone; tests/unit/test_data_quality.py::test_detect_gaps_raises_at_threshold; tests/unit/test_data_quality.py::test_sanity_check_raises_for_zero_close; tests/unit/test_data_quality.py::test_sanity_check_raises_for_high_below_close; tests/unit/test_data_quality.py::test_run_all_checks_returns_report | Passing locally | 2026-05-03 |

## SimBroker Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T15 (SimBroker Cost Model) | Deterministic cost decomposition, zero-cost path, borrow component, config validation | tests/unit/test_simbroker.py::test_cost_model_worked_example; tests/unit/test_simbroker.py::test_cost_model_is_deterministic; tests/unit/test_simbroker.py::test_cost_model_borrow_component; tests/unit/test_simbroker.py::test_cost_model_zero_costs; tests/unit/test_simbroker.py::test_cost_model_config_validates_nonnegative | Passing locally | 2026-05-03 |
| T16 (SimBroker Fill Engine) | Fill price constraint, byte-identical deterministic FillLog, no-lookahead, complete cost fields, persisted `constrained` schema field | tests/unit/test_simbroker.py::test_fill_constrained_to_bar_high; tests/unit/test_simbroker.py::test_fill_constrained_to_bar_low; tests/unit/test_simbroker.py::test_fill_unconstrained_within_bar; tests/unit/test_simbroker.py::test_fill_engine_determinism; tests/unit/test_simbroker.py::test_fill_log_has_all_required_fields; tests/unit/test_simbroker.py::test_fill_engine_no_lookahead; tests/integration/test_registry_db.py::test_fill_logs_schema | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |
| T17 (SimBroker Calibration Interface) | BidAskProvider abstract boundary, no-op provider, quote validation | tests/unit/test_simbroker.py::test_bid_ask_provider_is_abstract; tests/unit/test_simbroker.py::test_noop_bid_ask_provider_returns_none; tests/unit/test_simbroker.py::test_noop_is_valid_subclass; tests/unit/test_simbroker.py::test_bid_ask_quote_validates_spread_and_timestamp | Passing locally | 2026-05-03 |

## Walk-Forward Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T18 (IS/OOS Splitter) | Strict timestamp separation, N consecutive-bar embargo assumption, zero-embargo behavior, empty-IS rejection, injected feature leakage detection | tests/integration/test_walk_forward.py::test_splitter_is_window_ends_before_embargo; tests/integration/test_walk_forward.py::test_splitter_oos_window_starts_at_cutoff; tests/integration/test_walk_forward.py::test_embargo_excludes_correct_bars; tests/integration/test_walk_forward.py::test_no_future_leakage; tests/integration/test_walk_forward.py::test_splitter_zero_embargo; tests/integration/test_walk_forward.py::test_splitter_raises_for_empty_is_window | Passing locally | 2026-05-03 |
| T19 (Leakage Detection Checklist) | Normalization leakage, regime label look-ahead, universe selection bias, within-window optimization, full clean PASS report, missing-detector FAIL report | tests/integration/test_leakage.py::test_leakage_normalization_detected; tests/integration/test_leakage.py::test_leakage_normalization_clean; tests/integration/test_leakage.py::test_leakage_regime_lookahead_detected; tests/integration/test_leakage.py::test_leakage_regime_lookahead_clean; tests/integration/test_leakage.py::test_leakage_universe_selection_detected; tests/integration/test_leakage.py::test_leakage_universe_selection_clean; tests/integration/test_leakage.py::test_leakage_within_window_optimization_detected; tests/integration/test_leakage.py::test_leakage_within_window_optimization_clean; tests/integration/test_leakage.py::test_full_leakage_checklist; tests/integration/test_leakage.py::test_full_leakage_checklist_requires_all_checks | Passing locally | 2026-05-03 |
| T20 (Walk-Forward Runner) | IS-only strategy call, T19 leakage gate before OOS, failed-leakage OOS block, OOS-only evaluation call, complete RunRecord metadata, rollback-safe PostgreSQL persistence | tests/integration/test_walk_forward.py::test_runner_produces_run_record_with_all_hashes; tests/integration/test_walk_forward.py::test_runner_blocks_oos_before_leakage_check; tests/integration/test_walk_forward.py::test_runner_blocks_oos_when_leakage_check_fails; tests/integration/test_walk_forward.py::test_runner_persists_run_record_to_db; tests/integration/test_walk_forward.py::test_runner_rejects_missing_code_hash | Passing locally against Docker PostgreSQL 16 | 2026-05-03 |

## Attribution Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|----------|--------|------|
| T21 (P&L Attribution Engine) | D-017 bounded implementation: PnLStreams series model, stream (d) exclusion, raw Net Sharpe over supplied active returns, deterministic drawdown records, PerformanceMetrics stubs | entropy/attribution/engine.py; tests/unit/test_attribution.py; tests/unit/test_models.py::test_pnl_streams_net_sharpe_excludes_stream_d | Passing locally | 2026-05-03 |

## Statistical Formula Stubs (blockers from PROJECT_BRIEF.md)

| Formula | Status | Blocking task | Resolution path |
|---------|--------|--------------|-----------------|
| Harvey-Liu deflation | Incomplete — needs worked example | T23 | Implement stub; document formula assumption; resolve in Phase 0+ |
| Sharpe CI derivation | Incomplete — needs validation examples | T23 | Implement analytical method with configurable bootstrap fallback |
| K3/N_eff estimator | Must be locked across docs and implementation | T23 | Implement with documented formula; test against known N_eff |
| Purge/embargo formula | Incomplete — T18 documents and implements temporary N consecutive-bar assumption; canonical derivation still required | T18 | Keep assumption visible in `entropy/walkforward/splitter.py`; note in ADR when resolved |
| P4 weekly regime algorithm | Not independently reproducible | Out of scope v1 | Defer to Phase 1+ |
