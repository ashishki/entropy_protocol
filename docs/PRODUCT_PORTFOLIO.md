# Entropy Protocol Product Portfolio Strategy

Status: Active commercial direction
Date: 2026-05-15
Authority: Product strategy layer, subordinate to
`products/entropy-core/docs/core/CHARTER.md`,
`products/entropy-core/docs/core/PROTOCOL_SPEC.md`,
`products/entropy-core/docs/ARCHITECTURE.md`, and
`products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md`.

This document records the commercial development course after the startup
pressure test. It does not modify frozen protocol non-negotiables, phase exit
criteria, kill criteria, OOS rules, live-capital boundaries, or research
firewall rules.

## Strategic Decision

Entropy Protocol remains a governed research and audit framework. The next
commercial direction is not a full quant backtesting SaaS, not a trading bot,
and not live broker/exchange control.

The original near-term commercial wedge was:

> Trade upload plus deterministic risk-rule violation audit for active traders.

After the 2026-05-29 portfolio review, the product portfolio is better read as
four separated tracks:

1. `products/entropy-core/` - governed protocol engine and reusable audit
   primitives. Its current role is the portfolio proof layer for product
   receipts, evidence refs, schema compatibility, blocked surfaces, and referee
   verdicts.
2. `products/trader-risk-audit/` - primary commercial MVP.
3. `products/signal-analytics-sandbox/` - validation sandbox that can become
   Telegram Trader Intelligence: public trader-channel claim, narrative,
   source-behavior, and risk-signal analysis.
4. Cross-project verification receipts - portable schema/protocol work that can
   inform AI Workflow Playbook and other projects without making Entropy Core a
   mandatory runtime.

The proof-layer strategy is defined in
`docs/ENTROPY_CORE_PROOF_LAYER_STRATEGY.md`. Products remain the application
points for the protocol; Core validates proof contracts and must not own product
runtime behavior, report authorship, customer delivery, or product-specific
business logic.

Gensyn-style research is inspiration for one narrow pattern only: diverse
candidate analyses plus a referee verdict with preserved evidence. Do not copy
distributed training, token economics, or autonomous agent swarms into this
portfolio.

Detailed reference policy: `docs/ENTROPY_CORE_AND_GENSYN_REFERENCES.md`.

## Artifact-First Validation Overlay

Date: 2026-05-11

The operator clarified that warm demand/pre-order interest already exists for
research/report artifacts. Therefore the immediate blocker is no longer generic
market-demand discovery. The immediate blocker is proving, on real
operator-approved data or public sources, that generated artifacts are correct,
readable, traceable, and safe to show.

Active overlay:

- `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`

Near-term priority:

1. Produce multiple open-source/public audit artifacts for Trader Risk Audit,
   then prepare private/operator-approved paid-pilot reports.
2. Produce a deep public-channel retrospective for Signal Analytics Sandbox,
   including expanded corpus, image/OCR, media review, claim ledger, market
   outcomes, and author capability report.
3. Pause Entropy Core unless Trader/Signal creates a concrete dependency or a
   human approves Core V2.
4. Manually validate reports before external delivery.
5. Package internal demo/report packs for warm pilot conversations.

This overlay does not approve public SaaS, live trading, exchange control,
private scraping, marketplace scope, or unsupported performance/advice claims.
The payment and retention gates below remain useful, but the next operational
gate is artifact validity.

## Product Segments

| Segment | Role | Status | Primary user | Relationship to core |
|---|---|---|---|---|
| Entropy Core | Governed evaluation and audit engine; proof layer for receipts, evidence refs, schema compatibility, and blocked surfaces | Core V2 internal kernel complete through Phase 31; human gate for next slice | Researcher/operator and future engineering team | Source of protocol discipline and portable proof checks |
| Trader Risk Audit | Trade upload, rule evaluation, violation reports | Primary MVP wedge; active open-source validation route | Active prop-style and small-team traders | Uses deterministic rule registry, audit logs, report generation |
| Signal Analytics Sandbox / Telegram Trader Intelligence | Public Telegram/X author/source retrospective reports; trader-channel intelligence product candidate | Active deep-channel retrospective route; productization planned | Signal subscribers, market researchers, and trading teams buying source hygiene | Must not contaminate core evidence or claims; may emit receipts Core can validate |

Current active route:

- Trader: `products/trader-risk-audit/docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
- Signal: `products/signal-analytics-sandbox/docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
- Portfolio task graph: `docs/tasks.md`
- Core: Core V1 checkpoint complete; V2 verification-kernel candidate requires
  explicit task selection before implementation.

## Non-Negotiable Product Boundaries

- No live broker or exchange integration by default.
- No order blocking or live risk guard until explicit evidence and liability
  gates are passed.
- No live capital.
- No OOS or performance claims without controlled evaluation.
- No AI in runtime trading path.
- No AI-generated strategy enters evaluation without human registration in the
  Trial Registry.
- No private Telegram group scraping.
- No paid X/Twitter API dependency before demand is proven.
- No public marketplace, mobile app, or institutional sales motion before the
  primary wedge is validated.

## Stack Strategy

The portfolio is Python-first for validation and MVP work, but architecture must
not assume Python is the permanent language for every future hot path.

Use Python, Polars, DuckDB, Parquet, SQL, and deterministic batch workflows until
real profiling shows a bottleneck. If load or latency later proves Python is the
wrong layer for a specific component, replace that component behind a stable
contract rather than rewriting the whole product.

Escalation options:

- Rust for CPU-bound kernels, parsers, rolling windows, simulations, and other
  hot numerical paths.
- Go for long-running services, collectors, workers, or operational APIs.
- C/C++ only for unavoidable native integration.

Any non-Python language or second runtime requires a benchmark, ADR, CI/toolchain
plan, rollback plan, and human approval.

## Primary Commercial Wedge

Trader Risk Audit is the first product to validate.

Core promise:

> Upload trades and written rules. The system shows which trades violated the
> rules, how much P&L came from violations, and which rule failures repeated.

The first version is upload/import based. It should work from broker/export CSVs
and manually collected policy rules. It must not require live APIs.

## ICP Decision

Primary ICP:

Active prop-style or small-team traders who already have explicit risk rules and
can export trade history.

Secondary ICPs:

- systematic retail traders who want disciplined hypothesis review;
- small trading teams with repeatable rule review workflows;
- Russian trading teams only after warm-intro validation proves data sharing and
  payment behavior.

Deferred ICPs:

- analysts at institutional funds;
- broad discretionary retail traders with vague rules;
- signal sellers and influencers;
- users asking primarily for AI-generated profitable strategies.

## Validation Gates

The original validation gates remain the commercial conversion gates. After the
2026-05-11 operator update, real artifact validation may proceed before these
gates are fully satisfied because warm demand/pre-order interest already exists.
Do not interpret this as approval for broad product expansion: only work needed
to produce, validate, and package real reports is in scope before payment and
retention evidence.

| Gate | Threshold | Decision if false |
|---|---|---|
| Prospect access | 20 qualified conversations in 14 days | Stop market assumption; rebuild ICP |
| Data access | 5 real trade exports plus written rules | Do not build upload product |
| Payment | 3 paid audit reports from 10 qualified prospects | Do not productize |
| Retention | 3 repeat audits within 30 days | Keep concierge or pivot |
| Referral | 2 unpaid referrals from pilot users | Recheck urgency and trust |

## Development Phases

| Phase | Name | Objective | Build posture |
|---|---|---|---|
| A | No-build validation | Prove paid pain through interviews and manual reports | No code |
| B | Trader workflow definition | Lock import, rule, and report workflow | Docs, mock reports |
| C | Manual risk audit pilot | Deliver paid concierge audits | Manual and scripts only |
| D | Minimal import and rule engine | Automate repeated audit work | Narrow engineering |
| E | Hypothesis/backtest bridge | Connect validated user demand to Trial Registry and evaluation | Only if requested by paid users |
| F | Telegram-first delivery | Deliver audit reports where users already work | Delivery only, not signal scraping |
| G | Live risk guard | Explore read-only monitoring and later blocking | Explicit evidence and legal gate |
| H | Expansion or split decision | Choose whether to merge, expand, or split products | Portfolio decision |
| I | Telegram Trader Intelligence | Productize public-channel analysis as source hygiene, narrative, claim, and risk-signal reports | Evidence-first reports, no prediction/advice |
| J | Verification Kernel V2 | Define portable receipts, validator verdicts, and responsibility records | Schema/protocol first, optional adapters later |

## Parallel Team Segmentation

| Team | Owns | Must not own |
|---|---|---|
| Validation/GTM | Interviews, paid pilots, first 10 customers | Product architecture decisions |
| Product/UX | Report format, upload flow, Telegram delivery UX | Core protocol changes |
| Entropy Core | Registry, append-only audit, deterministic report primitives | Live trading or signal scraping |
| Data Import | CSV schemas, broker/export normalization, anonymization | Live broker OAuth or order routing |
| Rule Engine | Deterministic policy evaluation and violation records | Strategy generation |
| Reporting | Audit packets, compliant vs violating P&L summaries | Performance claims outside controlled evidence |
| Hypothesis Bridge | Human-gated hypothesis and backtest workflow | Autonomous AI evaluation |
| Signal Sandbox | Public-source signal ledger and reports | Core protocol evidence |
| Legal/Risk | Liability memo, acceptable use, data retention | Product growth decisions |

## Source Of Truth Rules

Entropy Core canonical protocol docs remain authoritative for core behavior.
Other product workspace docs are working contracts for segmented development and
do not override:

- `products/entropy-core/docs/core/CHARTER.md`
- `products/entropy-core/docs/core/PROTOCOL_SPEC.md`
- `products/entropy-core/docs/ARCHITECTURE.md`
- `products/entropy-core/docs/spec.md`
- `products/entropy-core/docs/IMPLEMENTATION_CONTRACT.md`
- `products/entropy-core/docs/governance/research_firewall.md`

If a product workspace conflicts with an Entropy Core canonical document, the
core document wins and the product workspace must be corrected.
