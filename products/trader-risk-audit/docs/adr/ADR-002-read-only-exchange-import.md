# ADR-002: Read-Only Exchange Import Boundary

Status: Accepted
Date: 2026-05-09

## Context

Trader Risk Audit currently accepts local trade exports and written risk rules.
Some target users trade on exchanges such as Binance and Bybit, where private
APIs can return historical fills/executions. A read-only import path could
reduce user friction while preserving the product's post-trade audit wedge.

This ADR is based on the official exchange API surfaces checked on 2026-05-09:

- Binance Spot REST account trade history exposes `GET /api/v3/myTrades` as a
  signed `USER_DATA` account endpoint. Binance signed endpoints require API key
  authentication and request signing. Reference:
  `https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints`
  and
  `https://developers.binance.com/docs/binance-spot-api-docs/rest-api/request-security`.
- Bybit V5 exposes `GET /v5/execution/list` for execution history with product
  category, time-window, limit, and cursor parameters. Bybit also exposes
  `GET /v5/user/query-api`, whose response includes `readOnly` and permission
  metadata for the API key. Reference:
  `https://bybit-exchange.github.io/docs/v5/order/execution` and
  `https://bybit-exchange.github.io/docs/v5/user/apikey-info`.

## Decision

Trader Risk Audit may add a local, operator-controlled read-only exchange
import workflow for executed trade history. The allowed scope is:

- Binance and Bybit first, with one exchange implemented at a time.
- Historical fills/executions only.
- Local CLI import commands that write raw API snapshots and normalized trade
  files before the existing deterministic audit command runs.
- API credentials supplied through environment variables or an explicit local
  secret prompt, never committed files.
- Manifest hashes for raw snapshots, normalized outputs, reports, and delivery
  packets.
- Human/operator review before a fetched dataset is used in a paid report.

The workflow must stay post-trade. It may not place, amend, cancel, or manage
orders; transfer funds; withdraw assets; change leverage; change margin mode;
scrape signal channels; provide trading advice; or run a persistent trading
bot.

## Permission Rules

Every connector must enforce least privilege:

- Require read-only API keys where the exchange exposes an inspectable
  read-only flag.
- Reject keys that expose trade, order-write, withdrawal, transfer, or account
  mutation permissions when those permissions can be detected.
- Prefer IP allowlisting in operator/user setup guidance.
- Treat inability to verify permissions as `needs_operator_review`, not as a
  silent pass.
- Never print API keys, secrets, signatures, account ids, balances, or raw rows
  in logs or CLI status output.

## Data Flow

1. User creates an exchange API key with read-only permissions.
2. User provides the key to a local import command through environment variables
   or an explicit local prompt.
3. Connector verifies key metadata where possible.
4. Connector fetches bounded historical fills/executions by exchange-specific
   market, symbol/category, and time window.
5. Connector writes a raw immutable snapshot file and an import manifest.
6. Normalizer maps the raw exchange records into the existing canonical trade
   format.
7. Existing `audit` command consumes the normalized file and written risk
   policy.
8. Existing report, delivery packet, and audit manifest generation remains the
   source of final audit truth.

## Storage and Secret Handling

- Secrets must come from environment variables, process stdin, OS keychain, or a
  later explicitly approved local secret store.
- Secrets must not be written to `manifest.json`, queue metadata, workspace
  metadata, test fixtures, screenshots, logs, or docs.
- Raw exchange snapshots may contain sensitive trade history and must be treated
  like user-provided trade exports.
- Test fixtures must use synthetic or explicitly sanitized exchange-like JSON.

## Exchange-Specific Constraints

Binance:

- Start with Spot account trade history.
- Require explicit symbols and time ranges; do not assume one endpoint can fetch
  every account trade without symbol/window planning.
- Signed request implementation must be covered by deterministic tests that use
  fixture credentials only.

Bybit:

- Start with V5 execution history for `spot` and `linear` categories.
- Handle cursor pagination and seven-day request windows.
- Use API key information to verify read-only status where available.

## Consequences

This ADR allows later roadmap phases to build local read-only importers. It
does not permit live broker/exchange control, trading automation, hosted
credential storage, SaaS account onboarding, checkout, Telegram credential
collection, signal analytics, or investment advice.

Implementation must be phased. Before any real exchange network path is added,
the roadmap must define the credential permission contract, synthetic fixture
policy, and redaction tests. The first network-capable connector task may only
proceed after those safety gates pass.
