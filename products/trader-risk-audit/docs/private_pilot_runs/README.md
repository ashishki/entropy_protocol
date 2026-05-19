# Private Pilot Run Notes

Status: active safe-summary register
Date: 2026-05-15
Audience: operator only

This directory stores only safe metadata about private or anonymized pilot audit
runs. Private inputs, generated private artifacts, raw rows, account ids,
customer identifiers, credentials, private paths, screenshots, and payment
details must stay outside git.

## Current Register

| Run note | Label | Run status | Review status | Delivery decision |
|---|---|---|---|---|
| `pilot_waiting_for_input_001.md` | `pilot_waiting_for_input_001` | `blocked_no_operator_approved_input` | `not_started` | `blocked_do_not_deliver` |

## Safe Run Note Fields

Every committed run note must include:

- safe run label;
- note date;
- operator approval status;
- data shape, using aggregate descriptors only;
- rule shape, using aggregate descriptors only;
- local artifact status, without private paths;
- report status;
- review status from `docs/PRIVATE_PILOT_REPORT_REVIEW_CHECKLIST.md`;
- delivery decision;
- blocker tags or safe reviewer notes;
- deletion trigger status.

## Forbidden Content

Do not commit:

- raw private trade rows or row excerpts;
- account ids, exchange ids, balances, names, handles, emails, phone numbers, or
  payment identifiers;
- API keys, signatures, tokens, cookies, passwords, or seed phrases;
- absolute/private local paths or cloud-sync paths;
- screenshots unless redacted and explicitly approved;
- report tables copied from a private run before manual privacy review.

## Template

```markdown
# Private Pilot Run Note - <safe_run_label>

Status: <blocked_no_operator_approved_input|run_complete_pending_review|reviewed_needs_fix|reviewed_approved|delivered_manual>
Date: YYYY-MM-DD
Audience: operator only

## Safe Metadata

| Field | Value |
|---|---|
| Safe run label | `<safe_run_label>` |
| Operator approval status | `<approved|pending|blocked>` |
| Intake method | `<csv_export|bybit_read_only_api|binance_read_only_api|not_supplied>` |
| Audit period shape | `<date_range_days=N|not_supplied>` |
| Data shape | `<row_count_bucket, instrument_count_bucket, field_coverage_only>` |
| Rule shape | `<starter_profile/custom_structured/written_rules_review_required>` |
| Local artifact status | `<not_created|created_outside_git|deleted_after_review>` |
| Report status | `<not_started|generated_pending_review|reviewed_report_ready|blocked>` |
| Review status | `<not_started|blocked_do_not_deliver|needs_fix|approved_for_manual_delivery|delivered_manual>` |
| Delivery decision | `<blocked_do_not_deliver|hold|manual_delivery_allowed|delivered_manual>` |
| Deletion trigger confirmed | `<yes|no|not_applicable>` |

## Blockers Or Review Notes

- `<safe blocker tag or aggregate note only>`

## Privacy Confirmation

This note contains no raw private rows, account ids, credentials, private paths,
customer identifiers, payment details, or unapproved screenshots.
```
