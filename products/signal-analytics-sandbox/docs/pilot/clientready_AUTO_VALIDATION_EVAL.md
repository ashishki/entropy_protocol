# Client-Ready Auto-Validation Evaluation

Date: 2026-05-31

This artifact runs the Phase 40-42 auto-validation contract against the 9
Phase 38 media candidates. It remains internal-only and does not approve
customer-facing use.

## Summary

- Candidates evaluated: 9
- auto_accepted: 0
- auto_rejected: 4
- excluded_provider_gap: 0
- needs_human: 5
- blocked_customer_facing: 0 final decisions
- customer-facing policy passed rows: 0
- customer-facing rows: 0
- bulk market history storage used: false

## Decision

No row can be promoted to dashboard or paid-report metrics. The 4 post-factum
rows are auto-rejected for predictive metrics. The 5 remaining rows still need
human/operator context, accepted setup fields, approved recompute provenance,
or provider/proxy clarification.

## Rows

| ledger_id | auto_decision | policy_gate_status | customer_facing_allowed | main blockers |
|---|---|---|---|---|
| clientready-bablos79-10450 | needs_human | blocked_customer_facing | false | operator_acceptance_required; market_outcome_recompute_required; provider_or_proxy_approval_required |
| clientready-nemphiscrypts-3958 | needs_human | blocked_customer_facing | false | operator_context_required; missing_supported_asset; missing_target |
| clientready-pifagortrade-3214 | needs_human | blocked_customer_facing | false | operator_context_required; missing_target |
| clientready-pifagortrade-3218 | needs_human | blocked_customer_facing | false | operator_acceptance_required; ambiguous_fibonacci_levels; missing_supported_asset |
| clientready-pifagortrade-3225 | auto_rejected | blocked_customer_facing | false | post_factum_risk; auto_rejected_for_predictive_metrics |
| clientready-pifagortrade-3234 | needs_human | blocked_customer_facing | false | operator_acceptance_required; target_direction_conflict |
| clientready-pifagortrade-3264 | auto_rejected | blocked_customer_facing | false | post_factum_risk; auto_rejected_for_predictive_metrics |
| clientready-pifagortrade-3274 | auto_rejected | blocked_customer_facing | false | post_factum_risk; auto_rejected_for_predictive_metrics |
| clientready-pifagortrade-3276 | auto_rejected | blocked_customer_facing | false | post_factum_risk; auto_rejected_for_predictive_metrics |

Every row in the JSON artifact cites validator audit refs, policy audit refs,
validator result refs, and blocker reasons. Customer-facing promotion remains
blocked unless the customer-facing policy gate passes.
