# Pre-Private Evidence Capture Runbook

Status: draft
Date: 2026-05-19

## Purpose

Capture pre-private validation evidence without storing private identifiers,
raw trade rows, screenshots, private paths, payment identifiers, or customer
notes in git.

This runbook covers discovery conversations and report review sessions only. It
does not authorize private data storage or delivery.

## Allowed Evidence Rows

Use aggregate rows like this in an operator-controlled evidence log outside git
or in a future sanitized export:

```csv
date,source_type,icp_label,event_type,past_incident_tag,current_workaround_tag,report_usefulness_score,export_willingness_tag,pilot_ask_tag,next_action_tag
2026-05-19,market,solo_crypto,problem_interview,max_daily_loss,spreadsheet,4,export_willing_later,pilot_later,send_redaction_checklist
```

Allowed `source_type`:

- `market`
- `customer`
- `paid_pilot`
- `internal_demo`
- `demo_artifact`

Allowed `event_type`:

- `problem_interview`
- `report_review`
- `export_willingness_ask`
- `manual_pilot_ask`

## Forbidden Fields

Never record:

- name;
- email;
- Telegram handle;
- company;
- exchange account id;
- broker account id;
- wallet ownership claim;
- exact wallet-to-person mapping;
- exact P&L;
- raw trade rows;
- screenshots;
- private strategy notes;
- credentials;
- payment identifiers;
- private file paths.

## Promotion Rules

Evidence may be summarized in git only if it is aggregate and non-identifying.

Examples allowed in git:

- `12 problem interviews completed; 7 had weekly manual review; 4 cited export
  friction; 2 agreed to prepare anonymized export.`
- `3 report reviews scored usefulness 4/5 or higher; missing fees and realized
  P&L were the top trust blockers.`

Examples forbidden in git:

- exact quotes that identify a person or account;
- account/wallet ownership claims;
- private file names;
- screenshots;
- payment references;
- raw rows or row excerpts.

## Gate Mapping

| Evidence | Updates |
|---|---|
| Problem interview aggregate | `docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md` summary only |
| Report review aggregate | `docs/PRE_PRIVATE_HYPOTHESIS_EVIDENCE_MATRIX.md` |
| Export willingness yes | T116 blocker note and operator next action |
| Approved anonymized export exists outside git | Start T116 |
| Paid manual report delivered | Hypothesis evidence dashboard and paid-pilot gate review |

