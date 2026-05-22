# Private Pilot Feedback Log Template

Status: Phase 25 template
Date: 2026-05-15
Audience: operator only

Use this template after a warm prospect demo, paid ask, reviewed report
delivery, or follow-up. Commit only safe summaries. Keep raw private data,
customer identifiers, payment identifiers, handles, emails, private paths,
screenshots, and report excerpts outside git.

## Entry Template

```markdown
## YYYY-MM-DD - <safe_feedback_label>

| Field | Safe value |
|---|---|
| Feedback label | `<safe_feedback_label>` |
| Source stage | `<demo_only|paid_ask|input_received|report_delivered|follow_up>` |
| Prospect segment | `<prop_funded|crypto_discretionary|team_coach|other_safe_segment>` |
| Private run label | `<safe_run_label|not_applicable>` |
| Report review status | `<not_applicable|blocked_do_not_deliver|needs_fix|approved_for_manual_delivery|delivered_manual>` |
| Usefulness signal | `<strong|medium|weak|unclear>` |
| Trust signal | `<strong|medium|weak|unclear>` |
| Clarity signal | `<clear|some_confusion|unclear>` |
| Main objection tag | `<privacy|price|format|rules_mapping|data_export|trust|timing|not_painful|other_safe_tag>` |
| Paid decision | `<paid|manual_payment_intent|declined|no_ask_made|pending>` |
| Price band discussed | `<none|under_50|49_149|150_299|300_plus>` |
| Repeat signal | `<repeat_requested|repeat_possible|no_repeat_signal>` |
| Referral signal | `<referral_offered|referral_possible|no_referral_signal>` |
| Next action | `<safe next action>` |

### Safe Notes

- Usefulness: `<aggregate wording only>`
- Trust: `<aggregate wording only>`
- Clarity: `<aggregate wording only>`
- Objection: `<safe tag and short paraphrase only>`
- Payment: `<manual evidence status without payment identifiers>`
- Repeat/referral: `<safe signal only>`
```

## Allowed Evidence

Allowed committed feedback:

- safe feedback label;
- safe private run label, if one exists;
- stage and segment;
- aggregate usefulness, trust, and clarity ratings;
- blocker or objection tags;
- whether a paid ask was made;
- manual payment intent or paid status without payment identifiers;
- price band, not exact private invoice or receipt data;
- repeat or referral signal;
- safe next action.

## Forbidden Evidence

Do not commit:

- names, handles, emails, phone numbers, addresses, or social profile links;
- payment ids, invoices, receipts, checkout links, bank details, wallet
  addresses, or transaction hashes;
- raw private trade rows, report tables, screenshots, broker statements,
  support chats, private journals, CRM notes, or customer files;
- account ids, balances, API keys, tokens, signatures, cookies, or passwords;
- private local paths or cloud-sync paths;
- direct quotes that reveal identity, strategy, account details, or private
  trading behavior.

## Evidence Interpretation

Treat feedback as market evidence only when it comes from a real warm prospect
or private pilot interaction. Open-source and synthetic demo reactions can
improve the artifact, but they do not count as paid-pilot evidence, customer
validation, PMF, market demand, or proof that traders will pay.

## Rollup Fields

For weekly review, summarize only:

- number of paid asks made;
- number of paid or manual payment-intent responses;
- top objection tags;
- count of reviewed private reports delivered;
- repeat signals;
- referral signals;
- blockers preventing the next paid ask.
