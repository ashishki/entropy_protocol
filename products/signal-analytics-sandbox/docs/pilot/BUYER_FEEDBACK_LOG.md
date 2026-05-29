# Buyer Feedback Log

Date: 2026-05-19
Status: active_feedback_template_no_real_demos_recorded
Gate: `approve_internal_only`

## Purpose

Track buyer feedback from demo calls and pilot-offer conversations. This log is
for internal learning only and must not be used as proof of demand until real
buyer records are added by the operator.

## Required Fields

Each demo record must include:

- `demo_id`
- `demo_date`
- `buyer_role`
- `buyer_segment`
- `source_of_intro`
- `problem_confirmed`
- `main_objection`
- `requested_output`
- `willingness_to_pay`
- `price_reaction`
- `next_action`
- `owner`
- `follow_up_due`
- `notes`

## Feedback Log

No real buyer demos are recorded yet.

| demo_id | demo_date | buyer_role | buyer_segment | source_of_intro | problem_confirmed | main_objection | requested_output | willingness_to_pay | price_reaction | next_action | owner | follow_up_due | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `template` | `YYYY-MM-DD` | `<role>` | `<segment>` | `<intro source>` | `yes/no/unclear` | `<objection>` | `<requested output>` | `yes/no/unclear` | `<reaction>` | `<next action>` | `<owner>` | `YYYY-MM-DD` | `<notes>` |

## Objection Categories

- `too_expensive`
- `not_urgent`
- `wrong_output_format`
- `needs_live_monitoring`
- `needs_private_sources`
- `compliance_concern`
- `methodology_unclear`
- `insufficient_media_support`
- `provider_coverage_gap`
- `no_budget_owner`

## Requested Output Categories

- `internal_memo`
- `csv_export`
- `api_export`
- `evidence_appendix`
- `compliance_audit`
- `source_watchlist_review`
- `media_review_pack`
- `robustness_appendix`
- `dashboard_later`

## Willingness-To-Pay Scale

- `yes_paid_pilot`: buyer agrees the bounded paid pilot is worth procurement.
- `yes_if_scope_adjusted`: buyer may pay after scope/output change.
- `unclear`: buyer wants more proof or internal review.
- `no`: buyer will not pay for this workflow.

## Next Action Rules

- Every `yes_paid_pilot` or `yes_if_scope_adjusted` record needs an owner and
  follow-up date.
- Every `unclear` record needs a concrete missing proof item.
- Every `no` record needs the reason preserved for offer iteration.
- Do not count compliments as validation.
- Do not count hypothetical interest as willingness to pay.

## Current Summary

- Real demos recorded: 0
- Paid-pilot positive signals: 0
- Main objections recorded: 0
- Next actions open: 0
