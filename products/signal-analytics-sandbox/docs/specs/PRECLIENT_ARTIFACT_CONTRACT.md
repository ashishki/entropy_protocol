# Pre-Client Artifact Contract

Date: 2026-05-23
Status: `phase37_contract_v1`

This contract defines the artifacts that must exist before any client outreach,
paid report sale, private-channel analysis, partnership discussion, public
dashboard launch, ranking, or marketplace framing.

Phase 37 is a pre-client artifact hardening phase. Its output is a reliable
internal diligence package, not customer validation and not external approval.

## Product Boundary

The product promise before client outreach is:

> We can produce a source-linked diligence package that explains what a public
> trading channel appears useful for, what is weak or noisy, which claims were
> historically measurable, and which conclusions remain blocked.

The product must not promise:

- investment advice;
- future profit;
- best-channel ranking;
- private Telegram scraping;
- paywalled/login-walled bypass;
- customer-facing use of unaccepted transcript/OCR/chart claims;
- provider gaps counted as author failures.

## Reliability Status Enum

Every artifact and every claim-like row must use one of these reliability
statuses.

| Status | Meaning | Allowed audience |
|---|---|---|
| `draft` | Produced by deterministic extraction or a model, not yet reviewed. | internal only |
| `model_reviewed` | Reviewed by model reviewer/arbiter; useful for triage only. | internal only |
| `operator_reviewed` | Human/operator accepted, rejected, or marked needs-context. | internal or paid-report candidate |
| `market_validated` | Compared to approved public market data/proxy with provenance. | internal or gated report |
| `dashboard_safe` | Approved by safety gate for compact free dashboard display. | buyer demo / public only if gate permits |
| `paid_report_safe` | Approved by safety gate for paid deep report content. | paid report only |
| `blocked` | Must not be used as a product claim. | internal blocker only |

Reliability can move forward only through evidence and gates. A model reviewer
cannot directly promote a media claim to `dashboard_safe` or `paid_report_safe`.

## Required Artifact Inventory

| Artifact | Owner | Input dependencies | Reliability status at creation | Allowed audience | Purpose |
|---|---|---|---|---|---|
| Product artifact contract | codex + operator | Phase 36 scorecard, paid boundary, dashboard schema | `operator_reviewed` after task acceptance | internal | Defines the rules for all pre-client artifacts. |
| Model-reviewed candidate packet | codex | media review results, multimodal RR drafts | `model_reviewed` | internal | Triage queue for human/operator review. |
| Evidence appendix | codex | source rows, media manifest, transcript/OCR drafts, model reviews, V1 metrics | `draft` until reviewed | internal | Trace every claim, example, blocker, and report statement. |
| Free dashboard card dataset | codex + operator | dashboard schema, scorecard, evidence appendix | `draft` until safety gate | internal dashboard prototype | Compact summary for acquisition-layer cards. |
| Per-channel internal deep reports | codex | evidence appendix, V1 metrics, media reviews, dashboard cards | `draft` until safety gate | internal | Full diligence narrative per channel. |
| Paid-style demo report | codex + operator | per-channel reports, paid boundary, evidence appendix | `draft` until safety gate | internal demo only | Show the paid-report shape before buyer conversations. |
| Candidate outcome/RR snapshot | codex | review packet, market APIs, provider/proxy rules | `market_validated` per evaluated row; otherwise `blocked` | internal | Determine which candidates are actually measurable. |
| Static free dashboard prototype | codex | free dashboard cards | `draft` until safety gate | internal demo only | Show how a free dashboard could look without launching it. |
| Artifact safety gate | codex + operator | dashboard cards, reports, demo, appendix | `operator_reviewed` | internal | Decide dashboard-safe, paid-report-only, internal-only, and blocked fields. |
| Phase 37 deep review | codex + operator | all Phase 37 artifacts | `operator_reviewed` | internal | Decide whether to proceed to client discovery. |

## Audience Classes

| Audience | Definition | Allowed content |
|---|---|---|
| `internal_only` | Development, review, and strategy use. | Drafts, model-reviewed rows, blockers, raw counts, failed attempts. |
| `buyer_demo_candidate` | Material that may be shown in a discovery conversation if safety gate allows. | Dashboard-safe summaries and internal-demo excerpts with disclaimers. |
| `public_dashboard_candidate` | Material that may later become public. | Only `dashboard_safe` fields after explicit gate approval. |
| `paid_report_candidate` | Material for a future paid diligence report. | Only `paid_report_safe` content after external-ready gate approval. |
| `blocked` | Not showable outside internal review. | Unaccepted media claims, private-source promises, unsupported rankings, advice. |

## Artifact Gates

### Gate 1 - Source And Legality

An artifact can proceed only if all source rows are public/operator-authorized
and no private, paywalled, login-walled, or access-control bypass source is
required.

### Gate 2 - Evidence Traceability

Every claim, metric, strength, weakness, and example must trace to at least one
of:

- public source URL;
- media ref with checksum or path;
- transcript/OCR artifact path and text hash;
- model-review row;
- operator-review row;
- market provider URL/snapshot metadata;
- explicit blocker row.

### Gate 3 - Review Status

Model-reviewed media is not customer-facing. Transcript/OCR/chart claims remain
internal until human/operator accepted. Human/operator review may still mark a
row `needs_context`, `post_factum_only`, `rejected_noise`, or `blocked`.

### Gate 4 - Market Validation

Outcome and RR claims must use approved public market data/proxies. Provider
gaps, unsupported assets, ambiguous timestamps, missing stop/target/entry, and
post-factum-only screenshots are blockers or exclusions, not author losses.

### Gate 5 - Wording Safety

Artifacts must not contain:

- buy/sell/hold recommendations;
- future-profit language;
- guaranteed accuracy;
- universal best/worst channel ranking;
- marketplace claims;
- private-source access promises;
- claims that unaccepted media evidence is proven truth.

### Gate 6 - Client Readiness

Only the Phase 37 safety gate and deep review can decide whether the team may
proceed to buyer conversations. A positive decision means "ready for discovery",
not "validated business" and not "approved public product".

## Free Dashboard Card Contract

Free cards are a compact decision-support preview. Required fields:

- `source_id`;
- `source_type`;
- `evaluated_window`;
- `what_it_is`;
- `primary_markets`;
- `content_style`;
- `measurable_claim_count`;
- `sample_size_label`;
- `signal_performance_summary`;
- `setup_rr_status`;
- `media_coverage_summary`;
- `strengths`;
- `weaknesses`;
- `evidence_confidence`;
- `gate_status`;
- `allowed_audience`;
- `blocked_claims`.

Free cards must not include the full evidence appendix, full transcript/OCR
text, all source examples, or paid-report-only interpretation.

## Paid Deep Report Contract

Paid deep reports may include:

- full evidence appendix;
- source-by-source examples and counterexamples;
- confirmed and contradicted measurable claims;
- media/OCR/voice findings after review;
- post-factum vs forward-looking distinction;
- setup/RR analysis;
- methodology and risk-discipline analysis;
- source limitations and blocker register.

Paid deep reports still require explicit safety and external-ready gates. They
must not become investment advice or a promise that a channel will perform in
the future.

## Pre-Client Done Criteria

Phase 37 is done only when:

- every report/card statement links to evidence or a blocker;
- every model-reviewed row is clearly labeled non-customer-facing;
- every media-backed product claim is either operator-reviewed or blocked;
- every market outcome row records provider/proxy provenance or exclusion;
- the static dashboard is internal-only and no-advice;
- the paid-style demo report is internal-demo-only;
- the safety gate says exactly what can be shown in first buyer conversations;
- the Phase 37 deep review records one of:
  - `proceed_to_client_discovery`;
  - `continue_internal_hardening`;
  - `pivot_scope`.

## Explicit Non-Goals

Phase 37 does not:

- contact customers;
- test willingness to pay;
- launch a public dashboard;
- process private groups;
- form paid-channel partnerships;
- implement billing;
- rank authors;
- approve external delivery.
