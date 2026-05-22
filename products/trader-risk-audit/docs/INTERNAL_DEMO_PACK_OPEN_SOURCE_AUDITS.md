# Internal Demo Pack - Open-Source Audits

Status: active Phase 24 demo pack
Date: 2026-05-15
Audience: operator-only warm conversation prep

This pack uses validated open-source and synthetic audit artifacts to explain
what the report workflow produces. It proves artifact quality: deterministic
rules, source-row traceability, reproducibility, limitation handling, and safe
rejection behavior. It does not prove paid-pilot demand, customer PMF, market
demand, willingness to pay, trader outcomes, or trading performance.

## Demo Pack Contents

| Demo role | Pack | Path | Why it is included |
|---|---|---|---|
| Strong positive case | `risk_audit_case_001` | `demo/risk_audit_case_001/output/report_reviewed.md` | Shows 13 deterministic findings, repeated cooldown/daily-loss/position/forbidden-asset patterns, non-zero violating P&L, and source-row traceability. |
| Limitation case | `synthetic_limit_leverage_001` | `demo/synthetic_limit_leverage_001/output/report_reviewed.md` | Shows the workflow refusing to infer leverage when the CSV has no leverage field. |
| Edge-case explanation | `synthetic_schema_reject_missing_price_001` | `demo/synthetic_schema_reject_missing_price_001/output/run_status.json` | Shows a malformed pack rejected before report generation because `price` is missing. |
| Reference backdrop | `open_source_sec_form4_001` | `demo/open_source_sec_form4_001/output/report_reviewed.md` | Optional traceability reference only; do not position it as a customer ledger. |
| Dashboard | Phase 24 dashboard | `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md` | Shows scorecard status, finding counts, limitations, error-register status, and reproducibility status for every pack. |

## Demo Order

1. Open `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`.
2. State the boundary: these are artifact-quality examples, not customer or
   market evidence.
3. Show `risk_audit_case_001` as the strong positive example.
4. Show `synthetic_limit_leverage_001` as the limitation example.
5. Show `synthetic_schema_reject_missing_price_001/output/run_status.json` as
   the safe rejection example.
6. Close with the buyer promise and one paid-pilot ask.

## Safe Excerpts

Use these excerpts or screenshots. Do not show raw trade rows, private paths,
credentials, or any generated copy without the reviewed caveat above it.

| Moment | Safe excerpt | Source |
|---|---|---|
| Positive report summary | "Rules reviewed: 4", "Violations recorded: 13", "Affected P&L: 121" | `demo/risk_audit_case_001/output/report_reviewed.md` |
| Positive repeated pattern | `demo_cooldown_after_loss: 5`, `demo_max_daily_loss: 4`, `demo_max_position_size: 2` | `demo/risk_audit_case_001/output/report_reviewed.md` |
| Traceable violation table | Show the table headers and one or two rows with source row ids; keep synthetic provenance visible. | `demo/risk_audit_case_001/output/report_reviewed.md` |
| Limitation behavior | "max leverage is unsupported because the CSV has no leverage field" | `demo/synthetic_limit_leverage_001/output/report_reviewed.md` |
| Unsupported-data register | `synthetic_limit_max_leverage: unsupported_leverage_data (leverage)` | `demo/synthetic_limit_leverage_001/output/report_reviewed.md` |
| Rejection behavior | `missing canonical fields: price` | `demo/synthetic_schema_reject_missing_price_001/output/run_status.json` |
| Dashboard proof | "Unresolved P0/P1 findings: 0", "Accepted P2 caveats: 3" | `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md` |

## One-Minute Talk Track

1. "This is an internal artifact-quality demo. It uses open-source and
   synthetic packs to show the report workflow before asking anyone for private
   exports."
2. "The positive example shows how a completed report connects written rules to
   deterministic findings, source row ids, and P&L attribution."
3. "The limitation example matters just as much: if the source lacks leverage,
   the report says unsupported instead of guessing."
4. "The rejection example shows the intake boundary. If a required field like
   price is missing, no partial report or delivery packet is produced."
5. "These examples do not prove demand or PMF. The paid pilot is the test of
   whether this artifact is valuable on a real approved export and written
   rules."

## Buyer Promise

For one approved private export or approved local read-only historical import,
and one set of written risk rules, the operator can produce:

- one deterministic post-trade audit report;
- a short delivery packet;
- source-row traceability for findings;
- explicit unsupported-data limitations;
- a reproducibility manifest;
- one follow-up review of what the report did and did not prove.

The promise is a reviewed audit artifact, not advice, not broker control, not
order blocking, not automated trading, and not guaranteed improvement.

## Paid-Pilot Ask

Use this wording after showing the boundary and examples:

> If this report shape is useful, the next step is one paid manual audit on an
> approved export and your written rules. I will return a reviewed report,
> delivery packet, reproducibility manifest, and limitation notes. It will not
> connect to live trading, place or block orders, or provide investment advice.

## Do Not Say

- "These examples prove PMF."
- "This validates customer demand."
- "This is paid-pilot evidence."
- "The report prevents losses."
- "The report will make trading profitable."
- "The system blocks bad trades."
- "The SEC Form 4 pack is a customer ledger."

## Operator Checklist

- Open reviewed reports, not raw generated reports, during the demo.
- Keep synthetic/open-source provenance visible at all times.
- Include one positive example and one limitation/reject example.
- If asked for proof, show artifact hashes and reproducibility status, not
  market-demand claims.
- If asked about private pilot readiness, point to the dashboard gap:
  `future_session_timezone_boundary_001`.
- Do not add checkout, SaaS account flow, hosted uploads, live exchange
  control, or public landing-page copy from this pack.
