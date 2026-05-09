# Before/After Report Comparison EN

Purpose: show why Trader Risk Audit is more useful than a raw trade export
during a paid pilot conversation. This page uses public sample data from
`demo/public_sample_001`; it contains no real customer data, no Telegram
handles, no broker account ids, no emails, and no private exports.

## Before: Raw Trade Export

A raw trade export can show fields such as:

| Timestamp | Symbol | Side | Quantity | Price |
|---|---|---|---|---|
| public sample row | RISKY | buy | sample quantity | sample price |

What the raw export does not explain:

- which written rule was checked;
- whether the rule breach was deterministic;
- which source rows support the finding;
- whether the trade happened after a daily loss, drawdown, cooldown, position
  size, or forbidden-asset rule;
- the violation-attributed P&L for the flagged row.

## After: Audit Report

The audit report adds deterministic rule checks, source row ids, and
violation-attributed P&L:

| Raw export gap | Audit report output |
|---|---|
| Trade row has no rule context. | Rule ID and rule type identify the checked policy. |
| Row evidence is hard to discuss. | Source row ids trace each flag back to the input. |
| P&L is not tied to discipline. | P&L impact shows violation-attributed P&L for flagged rows. |
| Missing data can be ignored. | Limitations make unsupported or missing fields explicit. |
| Next step is vague. | Next review checklist tells the operator what to verify. |

This is not investment advice and does not control live trading. It has no
performance promise, no broker APIs, no signal parsing, no order blocking, and
no auto-advice.

## Paid Pilot CTA

Send a real trade export and written risk rules for one paid pilot manual audit.
The deliverable is a deterministic report with rule breaches, source rows,
P&L impact, limitations, and next-review checklist. The goal is to decide
whether the audit is worth paying for, not to discuss more features.
