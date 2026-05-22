# Safe Aggregate Evidence Log Template

Status: complete_for_operator_use
Date: 2026-05-19
Phase: 30

## Purpose

Use this template to summarize Phase 30 outreach without exposing private
contact data or raw trading data.

The working contact list and detailed notes must stay outside git. Only
aggregate rows like the examples below may be summarized in git after privacy
review.

Before using an aggregate log in any git-visible summary, validate it locally:

```bash
.venv/bin/python -m trader_risk_audit.cli evidence aggregate-validate \
  --log-file ../private_inputs/aggregate_outreach.csv
```

See `docs/AGGREGATE_EVIDENCE_VALIDATION_CLI.md`.

## CSV Columns

```csv
date,batch_id,source_type,icp_label,event_type,count,past_incident_tag,current_workaround_tag,trust_blocker_tag,export_willingness_tag,pilot_ask_tag,next_action_tag
```

Allowed `source_type`:

- `market`
- `customer`
- `paid_pilot`
- `internal_demo`
- `demo_artifact`

Allowed `event_type`:

- `targets_scored`
- `outreach_sent`
- `problem_interview`
- `report_review`
- `export_willingness_ask`
- `manual_pilot_ask`

## Example Aggregate Rows

```csv
date,batch_id,source_type,icp_label,event_type,count,past_incident_tag,current_workaround_tag,trust_blocker_tag,export_willingness_tag,pilot_ask_tag,next_action_tag
2026-05-19,batch_001,market,prop_funded,targets_scored,8,not_applicable,not_applicable,not_applicable,not_asked,not_asked,start_outreach
2026-05-20,batch_001,market,prop_funded,problem_interview,3,max_daily_loss,spreadsheet,missing_fees,not_asked,not_asked,ask_report_review
2026-05-22,batch_001,market,prop_funded,report_review,2,not_applicable,current_manual_review,missing_pnl,not_asked,not_asked,ask_export_willingness
```

## Allowed Tags

Past incident:

- `max_daily_loss`
- `max_drawdown`
- `position_size`
- `forbidden_asset`
- `cooldown`
- `leverage`
- `session_rule`
- `no_recent_incident`
- `not_applicable`

Current workaround:

- `spreadsheet`
- `journal`
- `exchange_dashboard`
- `dune_query`
- `python_notebook`
- `screenshots`
- `coach_review`
- `manual_memory`
- `none`
- `not_applicable`

Trust blocker:

- `missing_fees`
- `missing_pnl`
- `missing_leverage`
- `policy_mapping`
- `privacy`
- `source_shape`
- `report_clarity`
- `none`
- `not_applicable`

Export willingness:

- `export_willing_yes`
- `export_willing_later`
- `export_blocked_privacy`
- `export_blocked_effort`
- `export_blocked_no_rules`
- `export_blocked_no_value`
- `not_asked`

Pilot ask:

- `pilot_yes_paid`
- `pilot_yes_free_first`
- `pilot_later`
- `pilot_no_price`
- `pilot_no_trust`
- `pilot_no_urgency`
- `pilot_needs_team_approval`
- `not_asked`

Next action:

- `start_outreach`
- `ask_report_review`
- `ask_export_willingness`
- `ask_manual_pilot`
- `return_to_t116`
- `continue_validation`
- `narrow_icp`
- `revise_offer`
- `pause_or_pivot`

## Forbidden

Do not record:

- names;
- emails;
- handles;
- companies;
- wallet ownership claims;
- account ids;
- broker/exchange ids;
- raw trade rows;
- private strategy notes;
- exact P&L;
- screenshots;
- credentials;
- payment references;
- private file paths.
