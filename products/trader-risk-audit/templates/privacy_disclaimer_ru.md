# Privacy and Disclaimer RU

## Local-First Handling

Pilot inputs and generated reports are local-only by default. Operator stores
trade exports, written rules, normalized artifacts, reports and manifests in an
operator-controlled local workspace. Real customer exports, broker account ids,
trader names, emails, Telegram handles, account balances and notes must not be
committed as fixtures or written to logs.

## No Investment Advice

Trader Risk Audit is not investment advice. The report may describe deterministic
violations, timestamps, thresholds, source-row evidence and violation-attributed
P&L, but it does not recommend trades, strategies, position sizing or expected
returns.

## No Live Trading Control

Trader Risk Audit does not control live trading. It does not block orders, manage
positions, place trades, modify stops or send execution instructions.

## No Broker or Exchange API Connection

Trader Risk Audit does not connect to broker or exchange API in v1. Do not send
API keys, broker tokens, passwords, seed phrases or credentials. Any future live
integration requires a separate ADR and explicit approval before implementation.
