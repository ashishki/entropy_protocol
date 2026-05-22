# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.02
Date: 2026-05-22
Phase: 36

Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 36 (Channel Impact Framework And Cross-Channel Completion)
- Baseline: 316 passing tests, 0 skipped
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `pyright` passes
- Latest completed: `SAS-IMPACT-008 Cross-Channel Impact Recompute And Gate`
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

- `SAS-IMPACT-001..002` define broad impact criteria, source-of-truth layers,
  dashboard vs paid-report boundary, and the same loop for `bablos79`,
  `nemphiscrypts`, and `pifagortrade`.
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

1. `docs/AI_DEVELOPMENT_PLAN_RU.md`
2. `docs/tasks.md` Phase 36
3. `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md`
4. `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
5. `docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md`
6. `docs/pilot/three_channel_PHASE36_EXTERNAL_READY_GATE.md`

## Canonical Artifacts

- Phase 36 loop: `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
- `bablos79` media queue: `docs/pilot/bablos79_PHASE36_MEDIA_LINKAGE_QUEUE.md`
- `bablos79` Phase 36 gate: `docs/pilot/bablos79_PHASE36_EXTERNAL_READY_GATE.md`
- Phase 36 scorecard: `docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md`
- Phase 36 gate: `docs/pilot/three_channel_PHASE36_EXTERNAL_READY_GATE.md`
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

## Validation Commands

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src/ tests/ scripts/
.venv/bin/ruff format --check src/ tests/ scripts/
.venv/bin/pyright
```
