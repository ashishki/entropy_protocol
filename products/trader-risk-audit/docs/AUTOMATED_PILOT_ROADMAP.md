# Automated Pilot Roadmap

Status: planned
Date: 2026-05-14

## Goal

Move from founder-run manual audits to an automated validation loop:

```text
upload/export -> schema profile -> structured rules -> one-click audit ->
claim-safe preview -> paid pilot CTA -> evidence dashboard
```

The goal is not public SaaS scale yet. The goal is to test the hypothesis with
less operator labor while preserving deterministic audit truth, privacy,
claim-safety, and no live trading control.

## Operating Conventions

- Default external artifact language: English.
- Default operator/reporting display timezone for pilot evidence: MSK
  (`Europe/Moscow`) unless the source export or prospect explicitly requires a
  different timezone.
- Source timestamps must preserve their declared timezone/offset; display
  timezone conversion is a reporting concern, not a data rewrite.
- Every phase must keep raw private/customer trade rows outside git and outside
  logs.

## Phase Map

| Phase | Name | Purpose | Gate |
|---|---|---|---|
| 17 | Automated Intake Profiler | Turn raw user exports into a safe, actionable intake profile before operator work starts. | A user can upload/point to a CSV and get mapped fields, blockers, unsupported fields, and next action without exposing raw rows in logs. |
| 18 | Structured Rule Builder | Replace manual YAML authoring with supported rule catalog + profiles + threshold form. | A user can build a valid policy from supported rule types; unsupported free text becomes a limitation/review item. |
| 19 | One-Click Audit Runner | Run the deterministic audit from an intake session and policy without developer intervention. | One command/session produces normalized trades, report, packet, manifest, and run status. |
| 20 | Report Preview And Paid CTA | Create a claim-safe preview that can ask for a paid pilot without exposing full raw data. | Prospect sees value, limitations, and a narrow paid audit ask without advice/SaaS/live-control claims. |
| 21 | Hypothesis Evidence Dashboard | Track conversion and repeat-intent evidence from the automated flow. | Operator can see upload->valid export->report preview->paid ask->paid/repeat/referral counts. |
| 22 | Conditional Real Read-Only Import | Add real local read-only exchange fetch only if CSV/export friction blocks conversion. | Decision gate proves CSV friction; any real fetch stays local, read-only, no hosted secrets, no write/control endpoints. |

## Phase 17 - Automated Intake Profiler

Input:

- local CSV/export path supplied by operator or prospect;
- optional profile hint such as `soft`, `medium`, `hard`, or custom rules
  expected later;
- non-sensitive prospect/session label;
- explicit source timezone plus display timezone, defaulting display output to
  MSK when the operator does not override it.

Build:

- intake session contract with stable session id, timestamps, status, input
  references, safe metadata, blockers, warnings, and next action;
- schema profiler that reads headers and limited type/shape information without
  logging raw private rows;
- mapping suggestions from export columns to canonical trade fields;
- actionable Markdown/JSON intake report for the operator and prospect.

Outputs:

- `intake_session.json`;
- `schema_profile.json`;
- `intake_report.md`;
- blocker and unsupported-field register.

### Intake Session Contract

`intake_session.json` is the safe metadata boundary before any row parsing.
It records:

- deterministic `session_id`;
- prospect-safe label;
- source type and safe file references;
- source timezone and display timezone, defaulting display output to
  `Europe/Moscow`;
- trading session start/end and account currency;
- privacy flags confirming no credentials and local-only raw rows;
- current intake status.

It must not record raw trade rows, private notes, Telegram handles, credentials,
API keys, absolute private customer directories, or live-control flags.

### CSV Schema Profile Contract

`schema_profile.json` is the sanitized pre-normalization shape summary for an
intake session. It records:

- intake session id and safe source file name;
- inspected column names and canonical mapping candidates;
- missing required canonical fields;
- row count;
- duplicate explicit row-id risk;
- timestamp timezone coverage;
- source/display timezone assumptions;
- fee, leverage, and P&L field availability;
- unsupported columns by name only.

It must not record cell values, raw rows, account balances, customer notes,
absolute private customer directories, or secrets.

### Intake Report Contract

`intake_report.md` is the prospect-readable summary produced from
`intake_session.json` and `schema_profile.json`. It records:

- current intake status: `runnable`, `needs-user-fix`,
  `needs-operator-review`, or `rejected`;
- concrete reasons for the status;
- accepted canonical fields and source column names;
- blockers and unsupported checks;
- unsupported columns by name only;
- the next action for the prospect or operator.

It must not record raw row values, private identifiers, account balances,
customer notes, absolute private customer directories, credentials, or advice.

Gate:

- valid exports produce mappings and next action;
- invalid exports explain exactly what is missing;
- raw private/customer rows are not committed or written into logs/reports;
- deep review confirms privacy, determinism, and scope boundaries.

Out of scope:

- hosted upload service;
- account creation;
- checkout;
- real exchange network fetch.

## Phase 18 - Structured Rule Builder

Input:

- Phase 17 intake profile;
- chosen starter profile or explicit threshold answers;
- free-text unsupported rule notes when the requested rule cannot be evaluated.

Build:

- supported rule catalog with required fields, examples, and evaluation
  coverage;
- profile-to-policy builder that emits existing deterministic policy YAML;
- prompt/form contract for thresholds such as max daily loss, max drawdown,
  forbidden assets, cooldown windows, and max position size;
- unsupported-rule register that preserves user intent without pretending it is
  evaluated.

Outputs:

- generated `policy.yaml`;
- `policy_builder_summary.json`;
- `unsupported_rules.md`;
- policy review packet when approval is required.

Gate:

- supported choices generate a valid policy accepted by the existing audit
  engine;
- unsupported requests become explicit limitations/review items;
- no trading advice, strategy recommendation, or LLM-owned rule truth is added.

Out of scope:

- free-form legal/compliance interpretation;
- strategy generation;
- automatic threshold recommendation.

## Phase 19 - One-Click Audit Runner

Input:

- valid intake session from Phase 17;
- valid generated or approved policy from Phase 18.

Build:

- local session runner that performs normalization, policy validation,
  evaluation, attribution, report generation, delivery packet generation, and
  manifest creation;
- status model for pending, blocked, running, complete, and failed states;
- artifact bundle index that points to report, packet, violations,
  attribution, manifest, and limitations;
- reproducibility gate that can rerun and compare manifest content hashes.

Outputs:

- complete report pack under a session output directory;
- `audit_session_status.json`;
- `artifact_bundle.json`;
- reproducibility check result.

Gate:

- one command/session produces the full deterministic artifact pack;
- rerun stability is proven by matching content hash;
- failures are actionable and do not leak raw rows or secrets.

Out of scope:

- background worker queue;
- hosted storage;
- multi-tenant SaaS dashboard.

## Phase 20 - Report Preview And Paid CTA

Input:

- completed Phase 19 audit bundle;
- claim guard results;
- paid pilot offer boundaries.

Build:

- claim-safe preview model that summarizes value without exposing full raw
  private data;
- redacted preview Markdown/text suitable for prospect follow-up;
- paid pilot CTA that asks for reviewed full report, written rules, and
  approved data scope;
- conversion event capture for preview shown, CTA shown, CTA accepted,
  declined, and objection reason;
- paid unlock boundary that prevents accidental full-report delivery before
  approval/payment decision.

Outputs:

- `report_preview.md`;
- `preview_summary.json`;
- `paid_pilot_cta.md`;
- conversion event rows in the local evidence log.

Gate:

- preview passes claim guard;
- user can see enough value to decide on a paid pilot;
- full report remains gated until operator-approved delivery;
- no checkout, performance promise, advice, or SaaS claim appears.

Out of scope:

- payment processor integration;
- automated customer billing;
- public landing page rewrite.

## Phase 21 - Hypothesis Evidence Dashboard

Input:

- local evidence events from intake, rule builder, runner, preview, paid CTA,
  paid report, repeat commitment, and referral outcomes.

Build:

- privacy-safe event schema with no raw trade rows, secrets, or customer
  identifiers;
- dashboard CLI/report that summarizes funnel counts, blockers, objections,
  conversion rates, and repeat/referral signals;
- hypothesis gate rules that distinguish product quality evidence from market
  validation evidence;
- export format for sharing aggregate evidence without private data.

Outputs:

- `hypothesis_events.csv` or equivalent local log;
- `hypothesis_dashboard.md`;
- `hypothesis_gate.json`;
- privacy-safe aggregate export.

Gate:

- operator can answer whether the automated loop produced enough valid exports,
  previews, paid asks, paid commitments, repeat commitments, and referrals;
- public/open-source demos are excluded from PMF and paid-pilot counts;
- dashboard results can drive the next roadmap decision.

Out of scope:

- analytics SaaS;
- tracking pixels;
- third-party customer data enrichment.

## Phase 22 - Conditional Real Read-Only Import

Input:

- Phase 21 evidence showing CSV/export friction is the binding blocker;
- updated ADR decision approving or rejecting real read-only fetch;
- existing Phase 14/15 fixture-backed Binance/Bybit import foundation.

Build only if the gate passes:

- CSV friction decision report;
- ADR update for minimal local real fetch;
- local read-only network fetch path with explicit endpoint allowlist,
  no hosted secrets, no write/control endpoints, and no live order behavior;
- integration from real fetched historical fills into the Phase 19 runner.

Outputs:

- friction decision report;
- updated ADR;
- local-only real fetch run notes if approved;
- import-to-runner artifact pack and deep review.

Gate:

- evidence proves CSV friction blocks conversion strongly enough to justify the
  added safety surface;
- any real fetch remains local, read-only, historical, and inspectable;
- no exchange secret is committed, logged, hosted, or reused outside the local
  run.

Out of scope:

- live trading;
- order placement/cancellation;
- withdrawals/transfers;
- hosted secret storage;
- always-on sync.

## Non-Negotiable Boundaries

- No public SaaS accounts before paid/repeat evidence.
- No checkout implementation before the preview/CTA gate proves demand.
- No live broker/exchange control, order placement, withdrawals, transfers,
  leverage mutation, order blocking, or trading advice.
- No LLM-owned violation truth.
- No hosted exchange secrets.
- Public/open-source demos do not count as PMF or paid-pilot evidence.

## Success Metrics

Minimum useful automated hypothesis evidence:

- 10 qualified prospects enter the automated intake.
- 5 valid exports/rules or read-only historical import candidates are accepted.
- 3 prospects request or pay for full reviewed report.
- 2 prospects commit to a repeat audit or refer another trader/team.

## Implementation Order

1. Build local/CLI-first automation.
2. Keep generated artifacts inspectable on disk.
3. Add web/SaaS surface only after paid/repeat evidence justifies it.
4. Add real read-only exchange network fetching only if CSV/export upload
   friction is the binding conversion blocker.
