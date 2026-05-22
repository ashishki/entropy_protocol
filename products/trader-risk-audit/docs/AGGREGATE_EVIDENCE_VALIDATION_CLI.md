# Aggregate Evidence Validation CLI

Status: complete
Date: 2026-05-19
Phase: 31

## Purpose

`evidence aggregate-validate` validates the Phase 30 safe aggregate outreach
CSV before any summary is copied into git-visible docs.

It is safety tooling only. It does not automate outreach, create market
evidence, approve private report delivery, or move the paid-pilot ready gate.

## Command

```bash
.venv/bin/python -m trader_risk_audit.cli evidence aggregate-validate \
  --log-file ../private_inputs/aggregate_outreach.csv
```

The log file should live outside git. The command prints only aggregate counts,
not the input path, contact details, or raw notes.

## Required Columns

```csv
date,batch_id,source_type,icp_label,event_type,count,past_incident_tag,current_workaround_tag,trust_blocker_tag,export_willingness_tag,pilot_ask_tag,next_action_tag
```

The allowed tags are defined in
`docs/SAFE_AGGREGATE_EVIDENCE_LOG_TEMPLATE.md`.

## Output

Example safe output:

```text
Aggregate Evidence Validation
Rows: 3
Total count: 7
Market count: 5
Demo count: 2
Export willing yes: 1
Pilot yes: 0
Return to T116 signals: 1
Status: valid
```

## Failure Cases

The command exits non-zero when:

- columns do not match the required schema exactly;
- count is not a non-negative integer;
- source/event/ICP/tag value is outside the allowed set;
- a value contains an email, handle, phone-like value, account number,
  credential marker, raw trade marker, payment marker, checkout marker, or
  source-row marker.

## Boundary

Allowed:

- validating aggregate outreach logs;
- printing aggregate counts;
- using `return_to_t116` only as a signal that an approved export may exist
  outside git and needs operator review.

Not allowed:

- storing contact lists in git;
- storing names, handles, companies, wallet ownership claims, account ids,
  screenshots, raw rows, private notes, private paths, credentials, or payment
  references;
- treating validation success as customer demand, PMF, paid evidence, or
  private report readiness.

