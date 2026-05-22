# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.02
Date: 2026-05-22
Phase: 36
Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 36 (Channel Impact Framework And Cross-Channel Completion)
- Baseline: 326 passing tests, 0 skipped
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `pyright` passes
- Latest completed: `Two-Month Multimodal Research Run`
- Phase 0 gates acknowledged; Engineering Phase 1 (T01+) may begin.
- | SAS-001: Paid Pilot Demand Validation | acknowledged |
- | SAS-002: Public-Source Legal/Terms Memo | acknowledged |
- External gate: `approve_internal_only`
- External delivery: not approved
- Current priority: apply the same impact/evidence loop to all three channels
  before dashboard/deep-report comparison

## Next Task

Active route: Phase 36 complete; next operator decision is internal dashboard
prototype vs another evidence-completion loop.

- `SAS-BABLOS-003` adds the media linkage queue: 8 candidates, 2
  source-linked audio rows ready for transcript acceptance, 0 OCR-ready rows,
  0 customer-facing media claims allowed.
- `SAS-BABLOS-004..008` close the `bablos79` Phase 36 pass as internal-only:
  0 human/operator accepted transcripts, 0 OCR drafts, 0 accepted media claims,
  0 computed outcomes, external delivery rejected.
- `SAS-IMPACT-003..004` add equivalent completion scopes for `nemphiscrypts`
  and `pifagortrade`.
- `SAS-IMPACT-005..008` add taxonomy, dashboard schema, paid boundary,
  three-channel scorecard, gate, and deep review.
- Two-month run `2026-03-22..2026-05-22`: 526 text rows, 37 normalized
  claims, 28 7d evaluable, 19 confirmed, 9 contradicted.
- Two-month multimodal run `2026-03-22..2026-05-22`: 570 posts, 295 media
  refs, 70 voice transcripts, 185 image/OCR drafts, 40 video/manual blockers,
  1 internal RR-ready setup draft.
- Media reviewer pass: `gpt-4.1-mini` reviewed 255 media drafts; `gpt-4.1`
  arbitrated 35 high-signal rows and accepted 9 internal candidates.

Read first: `docs/AI_DEVELOPMENT_PLAN_RU.md`, `docs/tasks.md` Phase 36,
`docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md`,
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
- `bablos79` Phase 36 blocker: current corpus is not a full 90-day multimodal
  capture; image/OCR is blocked until media is source-linked; audio remains
  internal-only until human/operator accepted.
- Impact dimensions now include signal performance, trend sense, insight depth,
  methodology, risk discipline, practical usefulness, creativity, and evidence
  confidence.

## Active Guardrails

- Public/operator-authorized sources only.
- No private Telegram scraping, login bypass, paywalled bypass, advice,
  future-profit claims, unsupported ranking, marketplace framing, or Core work.
- Unsupported providers/proxies are exclusions, not wins/losses.
- Unreviewed transcript/OCR/chart claims stay out of customer-facing metrics.
- Every customer-facing report requires an explicit external-ready gate.
