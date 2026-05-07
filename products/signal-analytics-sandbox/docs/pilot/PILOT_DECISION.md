# Pilot Decision - Repeat Or Automate Gate

Дата: 2026-05-07
Статус: updated after public capture parsing

## Verdict

**continue manual extraction; defer automation**

Do not build bot ingestion, private scraping, parser automation, public SaaS,
leaderboard, marketplace, copy trading, broker integration, or Entropy Core feed.

The pilot still has not produced the minimum evidence needed to repeat reports
or automate a bottleneck. Public captures now exist, but manual extraction,
approved records, customer decision impact, and payment signal are still absent.

## Evidence References

| Artifact | Evidence | Decision impact |
|----------|----------|-----------------|
| `docs/pilot/PILOT_SCOPE.md` | First source is `https://t.me/bablos79`; default target is 30-50 defensible signal records. | Scope is clear, but no captures exist yet. |
| `docs/pilot/METHODOLOGY_V0.md` | Capture/extraction/outcome/report guardrails are defined before source work. | Methodology is ready; no method change needed. |
| `docs/pilot/CAPTURE_LOG.md` | 60 public text posts captured from unauthenticated Telegram `/s/` HTML pages. | Capture blocker is cleared for the first batch. |
| `docs/pilot/EXTRACTION_LOG.md` | `pending_manual_extraction=60`; approved/ambiguous/not_a_signal/insufficient_fields/duplicate/needs_rule_template all 0. | Manual extraction is the next step; no extraction bottleneck measured yet. |
| `docs/pilot/reports/bablos79_BLOCKED_REPORT_V0.md` | Blocked-report memo only; no approved ledger, price snapshot, outcomes, or customer report metrics. | No customer-readable historical audit exists yet because extraction is pending. |
| `docs/pilot/CUSTOMER_FEEDBACK.md` | Feedback row is `pending-customer-review`. | No decision impact evidence. |
| `docs/pilot/PAYMENT_SIGNAL_LOG.md` | Payment row is `pending-operator-input`; no paid/deposit/repeat/referral status. | No payment signal. |

## Automation Decision

No automation is approved.

Reason:

- real public captures exist for the first batch;
- no manual extraction has happened yet;
- no operator minutes per approved signal were measured;
- no repeated source format was observed;
- no customer report was delivered;
- no payment, repeat request, or referral was recorded.

The smallest next action is not engineering. It is manual extraction:

1. review the 60 captured rows in `docs/pilot/EXTRACTION_LOG.md`;
2. classify each row as approved, ambiguous, not_a_signal, insufficient_fields,
   duplicate, or needs_rule_template;
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

This decision does not create a new engineering phase.

Any future engineering task must cite a measured bottleneck from real capture,
extraction, report, feedback, or payment logs. Current evidence supports only a
manual extraction step, not product expansion.
