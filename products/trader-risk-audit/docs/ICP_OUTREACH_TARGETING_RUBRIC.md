# ICP Outreach Targeting Rubric

Status: complete_for_operator_use
Date: 2026-05-19
Phase: 30

## Purpose

Use this rubric to choose outreach targets without storing names, handles,
wallet ownership claims, account ids, or private notes in git.

The operator can keep the real contact list outside git. In git, record only
aggregate counts and safe tags.

## Scoring

Score each potential contact from 0 to 2 per category.

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Written rules | No rules | Some informal rules | Explicit risk rules or external limits |
| Review cadence | No review | Ad hoc review | Weekly/session/incident review |
| Export habit | No export habit | Has exported before but rarely | Uses CSV/API/journal/Dune/Excel today |
| Pain recency | No recent issue | Vague issue | Specific recent rule/risk incident |
| Buyer/user access | Not decision maker | Influencer only | Can approve a manual audit or export |
| Privacy fit | Wants unsafe sharing | Unsure | Accepts anonymized/local-only boundary |

Priority score:

- `10-12`: high priority
- `7-9`: medium priority
- `0-6`: low priority

## Safe ICP Labels

Use only these labels in aggregate docs:

- `solo_crypto`
- `prop_funded`
- `coach`
- `dao_treasury`
- `fund_operator`
- `other_safe_label`

## Disqualifiers

Do not spend discovery time if the person:

- wants trading advice, entries, exits, signals, or performance improvement;
- has no executed trade history or transaction history;
- has no rules and no interest in writing rules;
- cannot discuss past workflow at a non-identifying level;
- will only continue if there is SaaS, live monitoring, or exchange control;
- wants to share credentials or raw private data in git-visible channels.

## Aggregate Reporting

Allowed aggregate summary:

```text
20 targets scored: 6 high, 8 medium, 6 low.
Top ICP by score: prop_funded.
Top disqualifier: no written rules.
```

Forbidden in git:

- names;
- emails;
- handles;
- company names;
- wallet/person mapping;
- account ids;
- private notes;
- exact P&L;
- screenshots;
- raw rows.

