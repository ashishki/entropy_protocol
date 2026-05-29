# Internal Demo Pack - SEC Form 4 Open Source

Status: T68 complete
Date: 2026-05-12
Audience: operator-only warm conversation prep

## Demo Pack Contents

| Item | Path | Use |
|---|---|---|
| Reviewed report | `demo/open_source_sec_form4_001/output/report_reviewed.md` | Show first-screen artifact quality, findings, and limitations |
| Reviewed delivery packet | `demo/open_source_sec_form4_001/output/telegram_packet_reviewed.txt` | Copy-ready short demo message |
| Generated manifest | `demo/open_source_sec_form4_001/output/manifest.json` | Show reproducible artifact hashes |
| Run notes | `docs/FIRST_AUDIT_RUN_SEC_FORM4_EN.md` | Explain command, artifacts, and deterministic rerun hash |
| Intake summary | `docs/REAL_DATA_INTAKE_SEC_FORM4_EN.md` | Explain source mapping and unsupported fields |
| Manual validation | `docs/MANUAL_VALIDATION_SEC_FORM4_EN.md` | Show arithmetic/source-row checks and error register |
| Claim-safety review | `docs/REPORT_POLISH_SEC_FORM4_EN.md` | Show reviewed hashes and claim guard result |

## Privacy Review

This pack contains no private customer export, broker statement, exchange API
key, account secret, Telegram handle, payment data, email, phone number,
reporting owner name, signature, remark, footnote, address, or private note.

The committed fixture contains only:

- timestamp;
- public symbol;
- side;
- quantity;
- price;
- zero fee assumption;
- anonymized account label;
- sanitized source trace id.

Raw SEC bulk files stay outside git under `/tmp/trader-risk-audit-sec/`.

## One-Minute Talk Track

1. "This is an open-source artifact validation run, not customer proof. The
   point is to show the audit pack format, traceability, reproducibility, and
   limits before asking for private data."
2. "The report takes transaction rows and a written policy, then returns
   deterministic findings with source row ids and a manifest."
3. "Here the strongest finding is a transaction-notional proxy breach. The
   report also flags a validation-only watchlist symbol."
4. "Important limit: this source is not an account ledger, so we do not claim
   P&L, drawdown, leverage, strategy quality, or trading intent."
5. "For a paid pilot, the next step is to run the same artifact workflow on the
   trader's approved export or read-only historical import and their actual
   rules."

## Paid Pilot Ask

Use this wording in warm conversations:

> I can run the same deterministic post-trade audit on your approved export and
> written rules. The output is a source-traceable report, delivery packet, and
> reproducibility manifest. It is not trading advice and it does not connect to
> live order control. The paid pilot is for one completed audit report and one
> follow-up review.

## Scope Boundaries

- No SaaS account.
- No checkout.
- No live broker/exchange control.
- No order placement or order blocking.
- No signal scraping.
- No investment advice.
- No future-performance claims.
- No claim that open-source validation proves willingness to pay.

## Operator Checklist

- Open `report_reviewed.md` first, not the generated raw `report.md`.
- Use `telegram_packet_reviewed.txt` for short-form demo copy.
- If asked for proof, show the manifest content hash from
  `docs/FIRST_AUDIT_RUN_SEC_FORM4_EN.md`.
- If asked about source limits, show `docs/MANUAL_VALIDATION_SEC_FORM4_EN.md`.
- Do not send raw SEC bulk files or private data.
- Ask for a paid pilot only after explaining that a real customer audit needs
  approved private export/read-only import data and written rules.
