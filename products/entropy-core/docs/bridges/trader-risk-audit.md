# Trader Risk Audit Bridge Contract

Version: 1.0
Date: 2026-05-07
Schema version: `trader-risk-audit-bridge/v1`
Status: Contract only

This contract defines the deterministic Entropy Core surfaces that Trader Risk
Audit may reuse. It does not approve direct product integration, live trading,
broker access, order blocking, production readiness, capital readiness, or
OOS/performance claims.

## Allowed Core Primitives

- `entropy.models.performance.PnLStreams`
- `entropy.attribution.archive_only_attribution_payload`
- `entropy.evidence.build_phase_gate_evidence_packet`

Allowed use is limited to deterministic schema, attribution, evidence, and
no-claim packet primitives. Product runtime code must not write Core registry
records or make Core phase-gate decisions through this bridge.

## Forbidden Core Calls

- `live_broker_api`
- `exchange_api_client`
- `order_blocking`
- `holdout_read`
- `oos_performance_label`
- `production_label`
- `capital_ready_label`
- `registry_write`
- `phase_gate_approval`

Any requested bridge surface matching these names is rejected by
`validate_trader_risk_bridge_request`.

## Human Approval Boundaries

- `product_bridge_activation`
- `risk_policy_interpretation`
- `ambiguous_export_mapping`
- `new_rule_type`
- `paid_report_delivery`

These approvals are product governance requirements. They are not replaced by
Core evidence packets or deterministic schema validation.

## Schemas

Risk policy primitive:

- `schema_version`
- `policy_id`
- `approval_id`
- `approved_by`
- `rules`
- `deterministic_owner`

Violation record primitive:

- `schema_version`
- `violation_id`
- `policy_id`
- `rule_id`
- `source_row_ids`
- `observed_value`
- `threshold`
- `unit`
- `severity`
- `occurred_at`
- `attributed_pnl`
- `deterministic_owner`

Attribution primitive:

- `schema_version`
- `attribution_id`
- `violation_id`
- `source_row_ids`
- `compliant_pnl`
- `violating_pnl`
- `attribution_method_id`

Report primitive:

- `schema_version`
- `report_id`
- `policy_id`
- `violation_ids`
- `report_hash`
- `no_claim_labels`
- `delivery_approval_required`

## Runtime Truth Boundary

Bridge schemas are deterministic Pydantic models. They forbid extra fields and
reject LLM-owned fields such as prompt, completion, model-output, LLM, or
AI-generated truth fields. LLM output may not own policy truth, violation truth,
P&L arithmetic, attribution, evidence truth, report claim status, or delivery
approval.

## No-Claim Labels

- `not_live_trading`
- `not_order_blocking`
- `not_oos_performance`
- `not_production`
- `not_capital_ready`
