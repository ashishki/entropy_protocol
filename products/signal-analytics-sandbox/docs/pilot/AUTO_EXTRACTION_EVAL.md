# Auto Extraction Evaluation - bablos79 Draft Helper

Date: 2026-05-08
Eval Source: manual artifact evaluation of `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`,
`docs/pilot/bablos79_REVIEW_QUEUE.md`, and `docs/pilot/EXTRACTION_LOG.md`
after running local validation (`93 passed, 0 skipped`, `ruff check src/ tests/`,
`.venv/bin/pyright`).
Status: Phase 10 decision input

## Boundary

This evaluation measures draft extraction usefulness only. It does not approve
signals, create ledger rows, produce outcome metrics, or authorize customer-
facing performance claims. Human review is still required before any row can
become final extraction truth.

## Row Counts

| Metric | Count |
|--------|------:|
| Captured public posts | 60 |
| Draft export rows | 60 |
| Final approved rows | 0 |
| Final pending_manual_extraction rows | 60 |
| Review queue rows | 23 |
| Rows outside review queue | 37 |

The draft helper reduces first-pass human review from 60 rows to a 23-row
exception queue, a 61.7% reduction before quality-control sampling is reviewed.

## Suggested-Status Distribution

| Suggested status | Count | Interpretation |
|------------------|------:|----------------|
| `review_candidate` | 0 | No row has complete asset/direction/entry/stop/target evidence. |
| `needs_review` | 1 | One cancellation/deferral row needs human judgment. |
| `insufficient_fields` | 16 | Asset or trade-management hints exist, but required approved-signal fields are missing. |
| `not_a_signal` | 43 | Parser found no positive draft signal fields. |
| `rejected_draft` | 0 | No validator-rejected draft rows in this phase. |

## False-Positive Notes

- Hashtag asset detection is useful for triage but over-inclusive for signal
  detection: asset-only posts such as commentary, jokes, news, and third-party
  references become `insufficient_fields` instead of final `not_a_signal`.
- Close/reduce phrases (`закрыл`, `часть закрыл`, `зафиксировал`) are useful
  review triggers but cannot be evaluated without linked original setup rows.
- The parser correctly keeps all complete-signal claims at zero; no row is
  promoted to `approved`, and no performance metric can be produced.
- Human review has not yet confirmed true false-positive / false-negative rates,
  so this evaluation cannot claim extraction quality beyond workload triage.

## Useful Suggestions

- The 23-row review queue collects all low-confidence, asset-bearing, and
  trade-management rows where a human reviewer is most likely to make a useful
  decision.
- The 37 rows outside the queue form a candidate skip set for faster manual
  pass-through, subject to sampled quality control.
- Draft reason codes make the next reviewer action explicit: missing required
  fields, close/reduce context, uncertainty, or no trade terms.

## Operator-Review Implications

The draft helper is useful as an internal triage assistant, not as extraction
truth. The next operator step should be human exception review of
`docs/pilot/bablos79_REVIEW_QUEUE.md`, followed by sampled verification of
non-queued rows. If human review confirms the queue quality, the product can
continue using the draft helper for this source. If many queued rows are false
positives or non-queued rows contain missed signals, improve parser rules before
using the helper on another source.

## Decision Input

Recommended verdict: `keep draft helper` for internal exception review only.

No next engineering scope is approved by this evaluation. The exact remaining
bottleneck is human review of 23 queued rows plus sampled verification of the
37 non-queued rows. Bot ingestion, private scraping, marketplace, copy trading,
broker integration, public leaderboard, SaaS expansion, and LLM truth remain
out of scope.
