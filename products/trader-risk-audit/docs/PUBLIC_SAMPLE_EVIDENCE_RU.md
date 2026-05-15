# Public Sample Evidence RU

## Назначение

Этот документ описывает `demo/public_sample_001/`, первый Phase 7 evidence pack
для internal validation. Он показывает, что Trader Risk Audit может взять
audit-safe public-like rows, применить starter policy profile, сгенерировать
детерминированные artifacts, пройти claim guard и подготовить понятный demo.

Это internal validation и demo artifact, но не market validation. Этот pack
нельзя считать qualified prospect call, paid pilot report, repeat commitment,
referral, PMF evidence, customer proof, proof that traders will pay или
доказательством готовности платить.

## Pack Contents

- `demo/public_sample_001/source.md` - source metadata, license/terms check,
  privacy removals, internal/demo labels, starter profile context.
- `demo/public_sample_001/trades.csv` - compact public-like transformed rows.
- `demo/public_sample_001/policy.yaml` - hard starter profile adaptation for
  `acct_public_sample_001`.
- `demo/public_sample_001/output/normalized_trades.json`
- `demo/public_sample_001/output/violations.json`
- `demo/public_sample_001/output/attribution_summary.json`
- `demo/public_sample_001/output/report.md`
- `demo/public_sample_001/output/telegram_packet.txt`
- `demo/public_sample_001/output/manifest.json`

## Source and Privacy Summary

Primary source candidate: SEC EDGAR Insider Transactions Data Sets / Form 4
non-derivative transactions. The committed fixture is public-like and derived
for internal validation; before replacing it with a live downloaded sample, the
operator must recheck the exact source URL, access date, license/terms, and
allowed redistribution of derived fixtures.

The pack removes or avoids reporting owner names, signatures, remarks,
footnotes, relationship titles, owner addresses, owner identifiers, issuer
contact fields, broker account ids, Telegram handles, emails, payment
identifiers, account balances, raw private exports, private notes, and
credentials.

## Starter Profile Context

The generated audit uses the `hard` starter profile because the goal is compact
internal stress testing. `soft`, `medium`, and `hard` remain customizable audit
presets only. They are not investment advice, not strategy recommendations, not
optimal risk settings, and not replacements for trader custom rules or
prop/funded account rules.

For comparison:

- `soft` has wider thresholds and should generally produce fewer flags.
- `medium` is the baseline internal validation profile.
- `hard` is stricter and useful for stress testing explainability.

This comparison does not claim that one profile is objectively best.

## Risk Scenarios Demonstrated

The generated report demonstrates at least five explainable deterministic
scenario types:

- max daily loss post-breach trade;
- max drawdown post-breach trade;
- cooldown trade inside window;
- max position size exceeded;
- forbidden asset.

Each violation is traceable to source row ids in the generated report and
violation artifact.

## Reproducibility

Generation command:

```bash
.venv/bin/python -m trader_risk_audit audit \
  --trades demo/public_sample_001/trades.csv \
  --policy demo/public_sample_001/policy.yaml \
  --output-dir demo/public_sample_001/output
```

Validation commands:

```bash
.venv/bin/python -m pytest tests/integration/test_public_sample_pack.py -q --tb=short
.venv/bin/python -m pytest tests -q --tb=short
.venv/bin/python -m ruff check trader_risk_audit tests
.venv/bin/python -m ruff format --check trader_risk_audit tests
```

The committed manifest records deterministic artifact hashes, including the
Telegram-ready delivery packet. Generated timestamps are manifest metadata and
are not part of deterministic content-hash inputs.

## Telegram Demo Boundary

`telegram_packet.txt` is copyable demo text only. Telegram may be used later as
upload, audit id/status, local operator run, and operator-approved report
delivery under ADR-001. This pack does not add broker APIs, signal parsing,
order blocking, auto-advice, live trading behavior, credentials, or unapproved
report delivery.

## Demo Mode

Local command:

```bash
.venv/bin/python -m trader_risk_audit demo public-sample
```

The command returns the existing public sample summary, report path, source
label, selected starter profile, and delivery packet path. It reuses
`demo/public_sample_001/output/report.md` and
`demo/public_sample_001/output/telegram_packet.txt`; it does not create a new
report format and does not convert the public sample into prospect, paid pilot,
PMF, or market validation evidence.

## Outreach Readiness

This pack supports the Phase 7 readiness review because it provides
reproducible reports, explainable violations, at least three risk scenarios, and
a two-minute readable demo path. It still does not satisfy the market validation
gate. The market validation gate remains 3 paid audit reports from 10 qualified
prospects within 14 days, then at least 2 repeat audit commitments within
30 days.
