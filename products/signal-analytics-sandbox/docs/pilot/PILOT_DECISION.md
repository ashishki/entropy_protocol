# Pilot Decision - Repeat Or Automate Gate

Дата: 2026-05-08
Статус: updated after Phase 10 draft extraction evaluation

## Verdict

**keep draft helper for exception review; no scope expansion**

Do not build bot ingestion, private scraping, public SaaS, leaderboard,
marketplace, copy trading, broker integration, public leaderboard, LLM truth,
or Entropy Core feed.

The Phase 10 draft helper is useful as an internal triage surface: it reduced
the first-pass review set from 60 captured posts to 23 exception-review rows.
It is not approved extraction truth. Manual review, approved records, customer
decision impact, and payment signal are still absent.

## Evidence References

| Artifact | Evidence | Decision impact |
|----------|----------|-----------------|
| `docs/pilot/PILOT_SCOPE.md` | First source is `https://t.me/bablos79`; default target is 30-50 defensible signal records. | Scope is clear, but no captures exist yet. |
| `docs/pilot/METHODOLOGY_V0.md` | Capture/extraction/outcome/report guardrails are defined before source work. | Methodology is ready; no method change needed. |
| `docs/pilot/CAPTURE_LOG.md` | 60 public text posts captured from unauthenticated Telegram `/s/` HTML pages. | Capture blocker is cleared for the first batch. |
| `docs/pilot/EXTRACTION_LOG.md` | Final status remains `pending_manual_extraction=60`; draft suggested statuses are 43 `not_a_signal`, 16 `insufficient_fields`, 1 `needs_review`. | Draft suggestions are available, but final extraction is still pending human review. |
| `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md` | 60 parser-generated draft rows with reviewer_id=`pending`. | Draft helper covers the full captured batch without ledger writes. |
| `docs/pilot/bablos79_REVIEW_QUEUE.md` | 23 exception-review rows selected by low confidence, asset candidates, trade-management ambiguity, and sampled non-signals. | Human review can focus on 23 rows before sampled verification of the remaining 37. |
| `docs/pilot/AUTO_EXTRACTION_EVAL.md` | Eval source/date, row counts, queue size, false-positive notes, and operator-review implications are recorded. | Decision input supports keeping the helper only as internal review aid. |
| `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md` | Blocked-report memo only; no approved ledger, price snapshot, outcomes, or customer report metrics. | No customer-readable historical audit exists yet because extraction is pending. |
| `docs/pilot/CUSTOMER_FEEDBACK.md` | Feedback row is `pending-customer-review`. | No decision impact evidence. |
| `docs/pilot/PAYMENT_SIGNAL_LOG.md` | Payment row is `pending-operator-input`; no paid/deposit/repeat/referral status. | No payment signal. |

## Automation Decision

Keep the draft helper for internal exception review only.

Reason:

- real public captures exist for the first batch;
- draft suggestions now cover all 60 captured posts;
- the review queue narrows first-pass human attention to 23 rows;
- no final extraction review has happened yet;
- no operator minutes per approved signal were measured after queue review;
- no customer report was delivered;
- no payment, repeat request, or referral was recorded.

The smallest next action is not more engineering. It is human exception review:

1. review the 23 rows in `docs/pilot/bablos79_REVIEW_QUEUE.md`;
2. sample-check non-queued `not_a_signal` rows from
   `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`;
3. classify final rows as approved, ambiguous, not_a_signal,
   insufficient_fields, duplicate, or needs_rule_template;
3. create approved ledger records only for complete, human-reviewed signals.

## Remaining Source Plan

Do not move to `https://t.me/nemphiscrypts` or
`https://t.me/pifagortrade` yet unless the operator explicitly decides that
`bablos79` is blocked and records the blocker.

Proceeding to the second or third source requires one of:

- `bablos79` completes manual extraction and either produces approved records or
  a concrete extraction blocker;
- `bablos79` is formally marked blocked with a concrete reason such as
  `non_public`, `paywalled`, `login_walled`, `screenshot_only`, or
  `insufficient_text`;
- operator instructs a source-order change and updates the capture log with why
  the deterministic first-source order was overridden.

## Continue / Stop Conditions

Continue the manual pilot only if:

- manual extraction classifies the captured batch;
- extraction can produce approved, ambiguous, excluded, or blocker rows from
  real evidence;
- a customer can review either a real report or a specific blocker memo.

Stop or defer the pilot if:

- manual extraction finds no defensible signal records;
- requested sources require private/paywalled/login-walled access;
- the customer wants prediction, advice, or profitable-channel recommendation;
- there is no payment/deposit/repeat/referral behavior after a real delivery;
- the main blocker remains sales/operator input rather than tooling.

## Product Boundary

This decision does not create a new engineering phase or authorize product
expansion.

Any future engineering task must cite a measured bottleneck from human review of
`docs/pilot/bablos79_REVIEW_QUEUE.md`, sampled non-signal verification, report
feedback, or payment logs. Current evidence supports keeping the draft helper as
an internal review aid only.

## Subsequent Roadmap Update — 2026-05-09

The operator later clarified that the first group is broader than strict signal
calls: it includes market regime commentary, event/news analysis, voice-message
analysis behavior, watchlists, and occasional visible trade entries. Based on
that product direction, `docs/pilot/AUTHOR_MARKET_INTELLIGENCE_ROADMAP.md` now
plans Phases 11-19.

This does not retroactively approve any Phase 10 draft row. The first new task
is `SAS-MI-001: Author Market Intelligence Architecture ADR`, which must decide
capability profiles and runtime/storage boundaries before RAG/vector/agent code
is implemented.
