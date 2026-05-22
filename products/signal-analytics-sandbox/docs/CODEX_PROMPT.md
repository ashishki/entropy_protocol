# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.01
Date: 2026-05-19
Phase: 35

Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 35 (Reliability And Scaling)
- Baseline: 295 passing tests, 0 skipped
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `pyright` passes
- Latest completed: `SAS-NEXT-032 Cost And Time Instrumentation`
- External gate: `approve_internal_only`
- External delivery: not approved
- Current priority: await operator review or next roadmap expansion

## Phase 0 Gate Status

- SAS-001/SAS-002 are complete and acknowledged.
- Engineering Phase 1 (T01+) may begin.

| Gate | Status |
| --- | --- |
| SAS-001: Paid Pilot Demand Validation | acknowledged |
| SAS-002: Public-Source Legal/Terms Memo | acknowledged |

## Next Task

No active `SAS-NEXT` task remains in the current roadmap.

- `SAS-NEXT-001..032` are complete.
- Next work requires operator/product decision on external gate, pilots, or new
  roadmap scope.

1. `docs/AI_DEVELOPMENT_PLAN_RU.md`
2. `docs/tasks.md` Phase 35
3. `docs/pilot/three_channel_V1_METRIC_RESULTS.json`
4. `docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.json`
5. `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
6. `docs/archive/PHASE27_REVIEW.md`

## Canonical V1 Artifacts

- V1 approval matrix: `docs/pilot/three_channel_V1_APPROVAL_MATRIX.md`
- V1 extraction review: `docs/pilot/three_channel_V1_EXTRACTION_REVIEW.md`
- V1 extractor calibration: `docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md`
- V1 metrics:
  `docs/pilot/three_channel_V1_METRIC_RESULTS.json`
- V1 scorecard:
  `docs/pilot/three_channel_V1_SCORECARD.md`
- V1 report:
  `docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md`
- V1 external gate:
  `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md`
- Full review queue:
  `docs/pilot/three_channel_FULL_REVIEW_QUEUE.json`
- False-negative pass:
  `docs/pilot/three_channel_FALSE_NEGATIVE_PASS.json`
- Report language safety:
  `docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.json`
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
