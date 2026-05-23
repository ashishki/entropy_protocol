# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.03
Date: 2026-05-23
Phase: 37
Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 37 (Pre-Client Artifact Hardening)
- Baseline: 345 pass / 0 skip
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `pyright` passes
- Latest completed: `SAS-PRECLIENT-005 Per-Channel Internal Deep Report V0`
- Phase 0 gates acknowledged; Engineering Phase 1 (T01+) may begin.
- | SAS-001: Paid Pilot Demand Validation | acknowledged |
- | SAS-002: Public-Source Legal/Terms Memo | acknowledged |
- External gate: `approve_internal_only`
- External delivery: not approved
- Current priority: build reliable internal artifacts before client outreach.

## Next Task

Active route: Phase 37 pre-client artifact hardening.

- Two-month run `2026-03-22..2026-05-22`: 526 text rows, 37 normalized
  claims, 28 7d evaluable, 19 confirmed, 9 contradicted.
- Two-month multimodal run `2026-03-22..2026-05-22`: 570 posts, 295 media
  refs, 70 voice transcripts, 185 image/OCR drafts, 40 video/manual blockers,
  1 internal RR-ready setup draft.
- Media reviewer pass: `gpt-4.1-mini` reviewed 255 media drafts; `gpt-4.1`
  arbitrated 35 high-signal rows and accepted 9 internal candidates.
- `SAS-PRECLIENT-001..005` completed the artifact contract, 9-row
  model-reviewed packet, 301-row evidence appendix, and 3 internal free-card
  drafts, plus 3 internal deep reports. Media/RR customer-facing use remains
  blocked pending review gates.
- Next task: `SAS-PRECLIENT-006` paid-style demo report.

Read first: `docs/tasks.md` Phase 37, `docs/AI_DEVELOPMENT_PLAN_RU.md`,
`docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md`,
`docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`,
`docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`.

## Canonical Artifacts

- `bablos79` media queue: `docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md`
- `bablos79` Phase 36 gate: `docs/pilot/bablos79_PHASE36_EXTERNAL_READY_GATE.md`
- Phase 36 scorecard: `docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md`
- Phase 36 gate: `docs/pilot/three_channel_PHASE36_EXTERNAL_READY_GATE.md`
- Two-month run: `docs/pilot/three_channel_2M_RUN_SUMMARY.md`
- Two-month multimodal run: `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`, `docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json`
- Media reviewer run: `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`
- V1 metrics: `docs/pilot/three_channel_V1_METRIC_RESULTS.json`
- V1 report: `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
- V1 gate: `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
- Pre-client plan: `docs/tasks.md` Phase 37
- Pre-client contract: `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md`
- Pre-client review packet: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`
- Pre-client evidence appendix: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`
- Pre-client dashboard cards: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.md`
- Pre-client reports: `docs/pilot/reports/preclient/`

## Key Product Facts

- Internal V1 validation is complete.
- V1 evaluable claims: `bablos79` 14, `nemphiscrypts` 49, `pifagortrade` 107.
- Current gate decision is `approve_internal_only`.
- Full queue rows: 1710 total; 172 included claim rows, 1534 source text rows,
  5 pending false negatives, 233 provider-gap tagged rows, 4 media blockers.
- False-negative pass: 5 reviewed, 3 extracted drafts, 2 needs_context,
  0 scoreable now.
- Report language safety: pass, 0 findings.
- Benchmark-relative outcomes: implemented with missing-benchmark exclusion.
- Run metrics record step durations, provider calls, cache hits, estimated
  cost, deterministic totals, and metrics hash.
- Main blockers: missing durable operator decisions, provider/media gaps,
  sparse setup/RR.
- Latest multimodal finding: media extraction works and materially expands
  evidence coverage, but customer-facing use remains blocked by human/operator
  review; strict RR setup coverage is still extremely sparse.
- Phase 37 must produce artifact contract, review packet, evidence appendix,
  dashboard cards, internal reports, paid-style demo, candidate outcomes,
  static dashboard, safety gate, and deep review before client outreach.

## Active Guardrails

- Public/operator-authorized sources only.
- No private Telegram scraping, login bypass, paywalled bypass, advice,
  future-profit claims, unsupported ranking, marketplace framing, or Core work.
- Unsupported providers/proxies are exclusions, not wins/losses.
- Unreviewed transcript/OCR/chart claims stay out of customer-facing metrics.
- Every customer-facing report requires an explicit external-ready gate.
