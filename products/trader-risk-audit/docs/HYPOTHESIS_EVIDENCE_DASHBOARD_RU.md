# Hypothesis Evidence Dashboard RU

## Назначение

Dashboard измеряет не активность ради активности, а движение manual pilot к
платежам, повторным commitments и referrals. Это локальный evidence artifact,
не CRM, не hosted SaaS и не платежная система.

## Funnel Event Schema

Каждый automated funnel event записывается как одна строка без direct
identifiers:

- `event_type` - одно из разрешенных событий ниже;
- `timestamp` - безопасный timestamp события;
- `intake_id` - anonymized local intake label;
- `source_type` - `csv_export`, `bybit_read_only_api`, `binance_read_only_api`,
  `public_sample_demo`, `internal_demo`, or `demo_artifact`;
- `evidence_source` - `market`, `customer`, `paid_pilot`, `public_sample_demo`,
  `internal_demo`, or `demo_artifact`;
- `tags` - короткие non-sensitive tags.

Запрещено записывать raw trade data, credentials, direct identifiers, broker
account ids, payment identifiers, checkout ids, emails, Telegram handles,
private notes или source-row payloads.

## Required Events

- `prospect_qualified` - prospect соответствует ICP и дал past-behavior signal.
- `intake_started` - начат локальный intake.
- `valid_export` - получен валидный export/import artifact без raw leakage.
- `policy_built` - written rules mapped to deterministic policy.
- `audit_run` - локальный audit completed or blocked with safe status.
- `preview_generated` - claim-safe preview готов для prospect.
- `cta_accepted` - prospect accepted/requested the manual paid audit CTA.
- `paid_report` - manual reviewed report was paid and delivered.
- `repeat_commitment` - prospect committed to another audit cycle.
- `referral` - prospect referred another trader, coach, or team lead.

## Gate Evidence

Gate evidence comes only from market/customer/paid pilot sources, not demo
sources. Strongest gate events are:

- `cta_accepted`
- `paid_report`
- `repeat_commitment`
- `referral`

Supporting funnel evidence includes `prospect_qualified`, `intake_started`,
`valid_export`, `policy_built`, `audit_run`, and `preview_generated`. These
support conversion diagnosis but do not replace paid/repeat/referral evidence.

## Vanity/Demo Events

`public_sample_demo`, `internal_demo`, and `demo_artifact` are vanity/demo
events for QA, demo readiness, and artifact quality. They do not count as paid
pilot reports, qualified market prospects, repeat commitments, referrals, PMF,
or willingness-to-pay evidence.

Open-source SEC artifact validation from Phase 16 remains artifact quality
evidence only. It can prove report shape, traceability, limitations, and
reproducibility; it cannot prove customer demand.

## Gate Rules

Proceed only when market/customer/paid pilot evidence reaches all of these
thresholds:

- 10 `prospect_qualified` signals or legacy qualified prospect rows;
- 5 valid exports/rules from `valid_export` or legacy export+rules rows;
- 3 `paid_report` signals or legacy paid delivered reports;
- 2 total repeat/referral signals from `repeat_commitment` and `referral`.

Return `needs_more_evidence` when thresholds are incomplete and blockers do not
dominate. Return `pivot` when blocking objections dominate and no paid reports
exist; this means the offer, ICP, or intake path needs rework before more
engineering work.

Uploads/API connections alone are not PMF. A successful upload, valid export,
read-only API connection, `policy_built`, `audit_run`, or `preview_generated`
is useful funnel diagnosis, but it does not prove willingness-to-pay, does not
replace paid_report, does not replace repeat_commitment, and does not replace
referral.

## Phase 29 Pre-Private Validation

When no operator-approved private/anonymized export exists, use
`docs/HYPOTHESIS_VALIDATION_WITHOUT_PRIVATE_EXPORT_PLAN.md` and the Phase 29
docs to collect weaker but useful evidence:

- problem interviews based on past behavior, not compliments;
- report review sessions using open/demo artifacts with explicit boundaries;
- export willingness asks after pain and workflow fit are visible;
- manual pilot asks after export willingness is credible.

Phase 29 evidence must be classified as:

- `technical_evidence` for reproducible reports and deterministic workflow;
- `product_evidence` for report usefulness, clarity, and trust;
- `market_evidence` for qualified pain, current workaround, and export
  willingness;
- `paid_evidence` for paid report, repeat commitment, or referral;
- `blocked_private_evidence` when T116 is still missing.

Do not count open-source reports, real-open-data rehearsals, report review
compliments, or demo conversations as paid reports, repeat commitments,
referrals, PMF, or private report readiness.

Current Phase 29 review status: `reviewed_no_aggregate_evidence`. The planning
artifacts are complete, but no safe aggregate discovery/report-review rows have
been supplied yet. Decision is `continue_concierge_validation`, not
`return_to_t116`, because no approved anonymized export exists.

Phase 30 execution status: `operator_outreach_required`. The outreach templates,
ICP rubric, aggregate evidence template, and outcome scoring rubric are ready,
but they are execution materials only. They do not count as market evidence,
paid evidence, repeat commitments, referrals, PMF, or private report readiness.

## T93 CSV Friction Decision

2026-05-15 verdict: defer real local read-only exchange network fetching.

Reason: Phase 21 created measurement infrastructure, but no market evidence log
was supplied showing CSV/export friction as the binding blocker. Repo-visible
counts for qualified prospects, valid exports, CSV/export blockers,
API-request objections, paid reports, repeat/referral signals, and paid intent
are all 0.

T94-T97 remain blocked unless a future privacy-safe evidence export reopens the
gate with market evidence.
