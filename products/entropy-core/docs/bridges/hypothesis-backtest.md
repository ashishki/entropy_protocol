# Hypothesis Backtest Bridge Design

Version: 1.0
Date: 2026-05-07
Status: Design only

This bridge defines the allowed path from research-assist hypothesis drafts to
registered, hash-bound, leakage-safe evaluation objects. It does not activate
autonomous strategy execution, registry writes, holdout reads, phase-gate
decisions, metric computation, evidence generation, live trading, or
OOS/performance claims.

## Bridge State Model

| State | Meaning | Evaluation allowed? |
|-------|---------|---------------------|
| `draft_hypothesis` | Human or AI-assisted research draft, not admissible evidence | No |
| `human_reviewed_candidate` | Human sponsor reviewed scope, family, and risk | No |
| `registered_trial_candidate` | Human explicitly requests Trial Registry admission | No |
| `registered_hash_bound_trial` | Trial Registry entry exists with dataset, code, policy, and parameter hashes | Only after readiness and leakage gates |
| `leakage_checked_evaluation_object` | Registered object has required leakage and holdout boundary evidence | Only under explicit evaluation approval |

## Human Registration Requirement

No draft hypothesis can become an evaluation object until all of the following
are true:

- `human_registration_required` is recorded.
- A human sponsor reviewed the draft hypothesis.
- The hypothesis family is assigned before evaluation-window data is examined.
- Trial Registry admission is explicit and append-only.
- Dataset hash, code hash, policy hash, and parameter-lock hash are bound before evaluation.
- Experiment Readiness Gate status is recorded.
- Evaluation execution approval is recorded before any governed backtest.

AI-generated drafts remain research-only until this registration path is
complete. Drafts cannot enter the walk-forward harness, contribute to
phase-gate evidence, influence portfolio routing, or be cited as OOS evidence.

## AI-Owned Truth Rejections

The bridge rejects AI-authored ownership of:

- `registry_truth`
- `gate_decision`
- `metric_computation`
- `evidence_truth`
- `leakage_status`
- `holdout_status`
- `report_claim_status`
- `oos_performance_label`
- `production_label`
- `capital_ready_label`

AI output may draft candidate wording only. It may not write registry records,
approve gates, compute metrics, determine evidence truth, mark leakage or
holdout status, or create report claim labels.

## Required Boundaries

Holdout boundary:

- Holdout remains locked by default.
- No holdout read occurs without explicit human holdout approval.
- Holdout unlock cannot be inferred from draft quality, AI confidence, or
  backtest interest.

Leakage boundary:

- Leakage checks are mandatory before any OOS/evaluation label.
- Failed leakage checks block label creation and must preserve failing check ids.
- Registration must occur before evaluation-window data is examined.

No-claim boundary:

- Draft and candidate outputs carry `not_oos_performance`,
  `not_phase_gate_approval`, `not_production`, and `not_capital_ready` labels.
- No report may imply validated performance, production readiness, or capital
  readiness without matching gate evidence.

Runtime escalation boundary:

- Python 3.12 remains the active runtime.
- No second runtime, native extension, service worker, broker API, exchange API,
  live feed, or autonomous execution loop is introduced by this bridge.
- Any runtime/language escalation requires benchmark evidence, ADR, CI/toolchain
  plan, rollback plan, and human approval before code is added.

## Forbidden Activations

- autonomous_strategy_execution
- ai_registry_write
- ai_gate_decision
- ai_metric_computation
- ai_evidence_generation
- holdout_read_without_approval
- leakage_bypass
- oos_performance_claim
- production_label
- capital_ready_label
- live_broker_or_exchange_integration
- runtime_escalation_without_adr
