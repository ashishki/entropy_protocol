# Exchange Import Guide EN

## Purpose

This guide explains how an operator can prepare a local read-only exchange
import for a founder-led pilot. It is not exchange endorsement, SaaS
onboarding, hosted secret storage, or live trading integration.

CSV upload remains the fallback path. If the trader does not want to create an
API key or the permission status is unclear, use `csv_export`.
If the trader does not want to create an API key, do not pressure them; use the
CSV upload path.

## Secret Input Rules

Allowed:

- environment variables for one local shell session;
- an explicit local prompt that does not echo input;
- an OS/local secret path only after separate approval.

Forbidden:

- committing API keys or secrets to files;
- putting keys in `metadata.json`, queue records, reports, manifests,
  screenshots, Telegram, email, docs, tests, or fixtures;
- sharing keys with the operator through chat history.

Environment-variable example:

```bash
export TRA_BYBIT_API_KEY="paste_read_only_key_here"
read -r -s -p "Bybit API secret: " TRA_BYBIT_API_SECRET
export TRA_BYBIT_API_SECRET
printf "\n"
```

Prompt-based example:

```bash
read -r -s -p "Binance API key: " TRA_BINANCE_API_KEY
printf "\n"
read -r -s -p "Binance API secret: " TRA_BINANCE_API_SECRET
printf "\n"
export TRA_BINANCE_API_KEY TRA_BINANCE_API_SECRET
```

Do not write these values into shell history, `.env` files, fixtures, docs, or
committed scripts.

## Setup Checklist

- Key is read-only.
- Trading/order permissions are disabled.
- Withdrawals are disabled.
- Transfers are disabled.
- Leverage/margin changes are disabled.
- Account mutation permissions are disabled.
- IP allowlisting is enabled when available.
- Symbols/category and time range are explicit.
- Written risk rules are available before audit.

## Local Command Shape

Fixture-backed commands are already implemented for tests and local artifact
checks:

```bash
.venv/bin/python -m trader_risk_audit exchange-import fixture \
  --snapshot tests/fixtures/exchange/binance/my_trades.json \
  --output-dir ./audit_inputs/binance_fixture

.venv/bin/python -m trader_risk_audit audit \
  --trades ./audit_inputs/binance_fixture/normalized_trades.csv \
  --policy ./my_policy.yaml \
  --output-dir ./audit_outputs/binance_fixture
```

Planning-only Binance command:

```bash
.venv/bin/python -m trader_risk_audit exchange-import binance-spot-plan \
  --symbol BTCUSDT \
  --symbol ETHUSDT \
  --start-time 2026-04-01T00:00:00Z \
  --end-time 2026-04-07T00:00:00Z
```

Real exchange network fetch remains blocked until explicit future task scope.

## Troubleshooting

| Failure state | Operator response |
|---|---|
| non-read-only key | Stop. Ask the user to create a read-only key with trade/order, withdrawal, transfer, leverage/margin, and account mutation permissions disabled. |
| missing symbol/category | Stop. Ask for an explicit symbol list and Bybit category or Binance Spot market. |
| time range too wide | Split into approved windows; do not guess missing history. |
| rate limit | Pause and retry later; do not bypass with extra keys or uncontrolled loops. |
| permission unverifiable | Mark `needs_operator_review`; use CSV upload if review cannot clear the risk. |

## Boundaries

Read-only API import is only a convenience path into the existing deterministic
audit engine. It must not become portfolio tracking, live alerts, signal
analytics, automated trading, order blocking, investment advice, or exchange
account management.
