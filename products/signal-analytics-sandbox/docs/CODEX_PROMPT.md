# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.02
Date: 2026-05-22
Phase: 36

Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 36 (Channel Impact Framework And Cross-Channel Completion)
- Baseline: 295 passing tests, 0 skipped
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `pyright` passes
- Latest completed: `SAS-IMPACT-002 Cross-Channel Development Loop`
- Phase 0 gates acknowledged; Engineering Phase 1 (T01+) may begin.
- | SAS-001: Paid Pilot Demand Validation | acknowledged |
- | SAS-002: Public-Source Legal/Terms Memo | acknowledged |
- External gate: `approve_internal_only`
- External delivery: not approved
- Current priority: apply the same impact/evidence loop to all three channels
  before dashboard/deep-report comparison

## Next Task

Active route: `SAS-BABLOS-003 Media Linkage Queue`, then equivalent completion
scopes for `nemphiscrypts` and `pifagortrade`.

- `SAS-NEXT-001..032` are complete.
- `SAS-IMPACT-001..002` define broad impact criteria, source-of-truth layers,
  dashboard vs paid-report boundary, and the same loop for `bablos79`,
  `nemphiscrypts`, and `pifagortrade`.
- `SAS-BABLOS-001..002` document that current `bablos79` evidence is partial:
  60 text captures over about 9 days, 2 internal-only audio refs, 0
  source-linked image/OCR artifacts, 14 reviewable non-blocker rows, 0
  deterministic deep-ledger outcome-ready rows.

1. `docs/AI_DEVELOPMENT_PLAN_RU.md`
2. `docs/tasks.md` Phase 36
3. `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md`
4. `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
5. `docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md`
6. `docs/pilot/bablos79_PHASE36_TEXT_RECAPTURE_PLAN.md`

## Canonical Artifacts

- Impact framework: `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md`
- Phase 36 loop: `docs/pilot/three_channel_PHASE36_IMPACT_DEVELOPMENT_LOOP.md`
- `bablos79` scope: `docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md`
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
