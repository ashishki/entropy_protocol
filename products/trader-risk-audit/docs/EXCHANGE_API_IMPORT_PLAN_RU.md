# План: безопасный read-only import с Binance и Bybit

Дата: 2026-05-09
Статус: accepted safety roadmap; Phase 13/14 fixture-backed Bybit and Binance
MVP paths are implemented; real network code remains blocked until explicit
operator-controlled connector scope is approved.
ADR: `docs/adr/ADR-002-read-only-exchange-import.md`

## T93 Decision - 2026-05-15

Verdict: defer real local read-only exchange network fetching.

Phase 21 delivered the evidence dashboard and privacy-safe export, but no
market customer evidence log was supplied showing that CSV/export friction is
the binding blocker. Current measured counts for qualified prospects, valid
exports, CSV/export blockers, API-request objections, paid reports,
repeat/referral signals, and paid intent are all 0 in repo-visible evidence.

T94-T97 remain blocked. Do not update ADR-002 for real fetching and do not
implement real exchange network calls until a future privacy-safe evidence
export justifies reopening the gate.

## Цель

Снизить friction для трейдера: вместо ручного CSV export пользователь создает
read-only API key на бирже, локальный importer забирает историю исполненных
сделок, нормализует ее в текущий формат Trader Risk Audit, а существующий audit
engine строит report, delivery packet и manifest.

Это не trading integration. Продукт остается post-trade audit: он не ставит,
не отменяет и не изменяет ордера, не выводит средства, не меняет плечо, не
дает торговые сигналы и не принимает инвестиционные решения.

## Источники API

- Binance Spot: signed account endpoint `GET /api/v3/myTrades` для trade
  history по symbol:
  `https://developers.binance.com/docs/binance-spot-api-docs/rest-api/account-endpoints`
- Binance security model: signed account endpoints требуют API key, signature,
  timestamp/recvWindow:
  `https://developers.binance.com/docs/binance-spot-api-docs/rest-api/request-security`
- Bybit V5: `GET /v5/execution/list` для execution history, category
  `linear`, `inverse`, `spot`, `option`, cursor pagination, seven-day request
  windows:
  `https://bybit-exchange.github.io/docs/v5/order/execution`
- Bybit V5: `GET /v5/user/query-api` возвращает metadata ключа, включая
  `readOnly` и permission groups:
  `https://bybit-exchange.github.io/docs/v5/user/apikey-info`

## Product Boundary

Allowed:

- read-only import of historical fills/executions;
- local CLI commands only;
- raw immutable snapshots and normalized trade files;
- manifest hashes over raw snapshots and generated outputs;
- operator review before paid report delivery;
- docs that teach users to create read-only, preferably IP-allowlisted keys.
- CSV upload fallback for users who do not want API keys.

Forbidden:

- trade/order placement, amend, cancel, or close-position calls;
- withdrawals, transfers, account mutation, leverage/margin changes;
- hosted secret storage before a separate ADR;
- Telegram collection of API keys;
- live alerts, signal parsing, auto-advice, or order blocking;
- use of AI as violation truth.

## Phase 11 - Import Safety Contract

Goal: approve and test the safety boundary before any real exchange network
path exists.

Tasks:

- T45: Accept ADR-002 and update architecture/scope docs.
- T46: Define exchange credential and permission contract.
- T47: Add synthetic raw exchange fixture policy and secret-redaction tests.

Exit gate:

- Docs clearly distinguish read-only import from broker/exchange control.
- Tests fail if connector code logs or persists API secrets.
- No real network calls are introduced in this phase.

T45 decision: ADR-002 is accepted as the canonical product boundary. T46 and
T47 must complete before Phase 12 can introduce fixture-backed import plumbing,
and no Binance or Bybit network request may be implemented during Phase 11.

## Phase 12 - Exchange Import Core

Goal: build shared local import plumbing that can work with fixtures before
Binance/Bybit-specific clients are added.

Tasks:

- T48: Add exchange raw snapshot schema and import manifest format.
- T49: Add exchange normalizer interface that maps raw fills into canonical
  trade records.
- T50: Add `exchange-import` CLI skeleton with fixture-backed import mode.

Exit gate:

- Fixture-backed import writes raw snapshot, normalized trades, and import
  manifest.
- Existing `audit` can consume normalized exchange trades without evaluator
  changes.
- Import content hashes are deterministic across output directories.

## Phase 13 - Bybit Read-Only MVP

Goal: import Bybit execution history safely for one real pilot path.

Tasks:

- T51: Implement Bybit API key metadata check using `GET /v5/user/query-api`.
- T52: Implement Bybit execution fetch planner for `spot` and `linear`,
  including seven-day window slicing and cursor pagination.
- T53: Implement Bybit raw-to-canonical normalizer and fixture golden tests.
- T54: Add Bybit import-to-audit integration test using sanitized fixtures.

Exit gate:

- Import rejects non-read-only keys when metadata says `readOnly != 1`.
- Fetch planning is deterministic and test-covered without real credentials.
- No order/write/withdraw/transfer endpoint exists in the codebase.

## Phase 14 - Binance Read-Only MVP

Goal: import Binance Spot account trade history safely after Bybit path proves
the shared import core.

Tasks:

- T55: Implement Binance signed request helper for account-data endpoints.
- T56: Implement Binance Spot `myTrades` fetch planner by symbol and time
  window.
- T57: Implement Binance raw-to-canonical normalizer and fixture golden tests.
- T58: Add Binance import-to-audit integration test using sanitized fixtures.

Exit gate:

- User must provide explicit symbols and time range.
- Signed request tests use fixture credentials only.
- No Binance order/write/withdraw/transfer endpoint exists in the codebase.

## Phase 15 - Operator UX and Pilot Validation

Goal: make read-only import discussable and operable in founder-led paid pilots
without expanding to SaaS or live trading.

Status: complete for the Phase 15 gate. Cycle 20 deep review found P0:0, P1:0,
P2:0, Stop-Ship: No. Real exchange network fetching is still not implemented
and must not be represented as available until future approved work adds it.

Tasks:

- T59: Complete - update operator runbook and paid pilot intake docs for read-only API
  import.
- T60: Complete - add safe CLI guidance for key permissions, IP allowlisting, and local
  secret handling.
- T61: Complete - add pilot evidence fields for import method and API-connection
  objections.
- T62: Complete - run deep review focused on secret handling, permission enforcement,
  reproducibility, and product boundary.

Exit gate: passed.

- Pilot docs explain CSV upload and read-only API import as two intake methods.
- Read-only API setup docs require read-only keys, disabled trading/order,
  withdrawal, transfer, leverage/margin, and account mutation permissions, and
  preferred IP allowlisting.
- API keys and secrets remain local-only and must not be stored in files,
  metadata, queue records, reports, manifests, Telegram, email, screenshots, or
  committed fixtures.
- Docs repeat no-advice, no-live-control, no-order-blocking, no hosted-secret,
  and no SaaS onboarding boundaries.
- Evidence log can distinguish CSV pilots from exchange-import pilots.
- Review confirms no broker control, no trading, no hosted secrets, and no
  advice scope.

## Operator Intake Decision

Use CSV upload when:

- trader already has a clean CSV export;
- trader does not want to create API keys;
- permission status is unclear;
- operator wants the lowest-risk intake path.

Use read-only API import only when:

- trader explicitly opts in;
- the key is read-only or requires operator review when unverifiable;
- trade/order, withdrawal, transfer, leverage/margin, and account mutation
  permissions are disabled;
- symbols/category and time range are explicit;
- credentials are entered through the approved local secret path.

## Suggested CLI Shape

```bash
export TRA_BYBIT_API_KEY=...
export TRA_BYBIT_API_SECRET=...

python -m trader_risk_audit exchange-import bybit \
  --category linear \
  --symbol BTCUSDT \
  --from 2026-04-01 \
  --to 2026-05-01 \
  --output-dir ./audit_inputs/bybit_may

python -m trader_risk_audit audit \
  --trades ./audit_inputs/bybit_may/normalized_trades.csv \
  --policy ./my_policy.yaml \
  --output-dir ./audit_outputs/bybit_may
```

```bash
export TRA_BINANCE_API_KEY=...
export TRA_BINANCE_API_SECRET=...

python -m trader_risk_audit exchange-import binance \
  --market spot \
  --symbols BTCUSDT,ETHUSDT,SOLUSDT \
  --from 2026-04-01 \
  --to 2026-05-01 \
  --output-dir ./audit_inputs/binance_may
```

## Key Product Rule

The import connector is a convenience path into the existing audit engine. It
must not become portfolio tracking, live risk control, signal analytics,
automated trading, or exchange account management.
