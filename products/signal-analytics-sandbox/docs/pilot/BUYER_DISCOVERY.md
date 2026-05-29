# Buyer Discovery Plan

Date: 2026-05-19
Status: internal_discovery_plan
Gate: `approve_internal_only`

## Boundary

This document is an internal pilot-operations artifact. It is not a sales deck,
customer-facing report, investment recommendation, or claim that the current V2
artifacts are externally approved.

## Working Verdict

The strongest wedge is not "find winning channels." The stronger wedge is
evidence-backed due diligence on public market commentary: what was said, what
was reviewable, what was measurable, what was excluded, and how robust the
result is.

Core assumption: at least one buyer segment already spends time or money
manually checking public trading commentary and will pay for a faster,
evidence-backed audit report.

## Buyer Profiles And Pilot Use Cases

| ID | Buyer profile | Pain | Current behavior | Likely pilot use case | Validation signal |
|---|---|---|---|---|---|
| B01 | Crypto fund research lead | Public Telegram/X calls are noisy and hard to verify before research use. | Analyst manually screenshots posts and checks charts. | Audit 3-5 public crypto channels over a fixed window. | Asks for repeat coverage or adds their own watchlist. |
| B02 | Digital-asset family office analyst | Needs a defensible view on which sources are worth reading. | Relies on referrals and ad hoc analyst notes. | Source utility report with exclusions and evidence appendix. | Shares real source list and asks for method constraints. |
| B03 | Prop trading risk manager | Traders cite outside channels without a paper trail. | Reviews chat logs after losses or disputes. | Evidence pack showing claims, outcomes, and unsupported rows. | Wants internal compliance/risk archive integration. |
| B04 | Retail broker research/content team | Wants to reference public sentiment without advice exposure. | Manual editorial review and legal disclaimers. | Internal-only source quality scan for content planning. | Legal/compliance joins discovery call. |
| B05 | Fintech data vendor product manager | Needs alternative-data features with provenance. | Monitors social data vendors and builds prototypes. | API-shaped sample of normalized claims and outcome fields. | Requests schema, sample data, and refresh cadence. |
| B06 | Crypto exchange research team | Tracks public narratives around listed assets. | Manual narrative monitoring and influencer lists. | Channel/topic audit for asset-specific public commentary. | Provides assets, channels, and evaluation window. |
| B07 | Financial media editor | Needs to vet contributors and source claims. | Manual editorial checks and reputation heuristics. | Contributor/source retrospective with evidence examples. | Wants a report before publishing or renewing a contributor. |
| B08 | Creator platform trust/safety team | Must investigate harmful or misleading market claims. | Reactive review after reports. | Claim ledger with source refs, unsafe wording, and review status. | Asks for moderation workflow and audit log. |
| B09 | Quant research boutique | Wants structured public-signal datasets without building capture/review tooling. | Scrapes small samples and cleans by hand. | Reviewed claim dataset plus deterministic outcome snapshot. | Requests export format and reproducibility checks. |
| B10 | Compliance consultant for finfluencers | Needs evidence-backed reviews of client content. | Samples posts manually and writes qualitative memos. | Pre-publication or retrospective claim-risk audit. | Brings a real client channel and asks about report language. |
| B11 | Newsletter/operator buying ad placements | Needs to avoid promoting low-quality signal sources. | Uses follower count and anecdotal reputation. | Sponsor/source due-diligence report with limitations. | Willing to pay before campaign spend. |
| B12 | Trading education company | Wants to separate educational commentary from signal claims. | Manual curriculum/content review. | Claim taxonomy and unsafe wording audit. | Requests wording library and reviewer workflow. |
| B13 | Fund-of-funds operational due diligence analyst | Needs to assess managers who cite public sources. | Interviews managers and samples source material. | Evidence appendix for cited public commentary sources. | Adds this to an ODD checklist. |
| B14 | Market intelligence agency | Needs analyst-ready source summaries with provenance. | Analysts build decks manually from posts and charts. | Internal research pack with coverage and robustness appendix. | Requests multi-source batch coverage. |
| B15 | Legal team reviewing marketing claims | Needs proof that performance language is bounded. | Checks final copy, not underlying evidence. | Report wording and evidence consistency audit. | Asks for customer-safe wording rules and audit trail. |

## First Discovery Sequence

1. Start with buyers who already have a source list and a reason to audit it:
   fund research, compliance, media/editorial, and data product teams.
2. Offer an internal sample walkthrough using the three-channel demo pack, but
   state that current artifacts are not externally approved.
3. Ask for one real source/window they already care about and one decision they
   would make differently if the report were reliable.

## Disqualifiers

- Buyer wants live trading alerts, copy trading, or advice.
- Buyer wants a public channel ordering without review/gate approval.
- Buyer cannot provide public/operator-authorized sources.
- Buyer only wants a dashboard and does not care about evidence provenance.
- Buyer will not define what decision the report should support.

## Discovery Questions

- What public sources did you manually check in the last 30 days?
- What decision depended on that check?
- How long did the manual review take?
- What made the result hard to trust?
- Which exclusions would make a report unusable for you?
- What format would be easiest to use internally: memo, CSV, API, appendix, or
  dashboard?

## Pilot Success Criteria

- Buyer provides at least one real public source list.
- Buyer agrees on a fixed historical window before analysis.
- Buyer accepts that unsupported rows remain exclusions.
- Buyer names the internal decision the report should support.
- Buyer is willing to pay for a bounded audit after seeing the internal demo.
