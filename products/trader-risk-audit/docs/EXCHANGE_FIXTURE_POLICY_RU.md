# Exchange Fixture and Redaction Policy RU

## Назначение

Этот документ задает правила для raw exchange fixtures, которые понадобятся
для будущих Binance/Bybit import tests. Fixtures нужны только для deterministic
regression tests: проверить parsing, pagination planning, normalization,
manifest hashing и redaction boundaries до использования реальных API.

Exchange fixtures не являются customer account history, paid pilot evidence,
market validation, PMF evidence или доказательством торговой дисциплины
реального пользователя.

## Allowed Fixture Sources

Разрешены только:

- fully synthetic Binance/Bybit-like JSON created by the developer;
- explicitly sanitized examples where the operator documented source terms,
  fields removed, privacy review date, and intended test use;
- tiny hand-written records that mimic official endpoint field names without
  containing real account history.

Запрещены:

- real API responses copied from a user account;
- paid pilot exports, screenshots, Telegram messages, private notes, CRM data,
  payment records, or broker statements;
- any fixture whose license, source, or sanitization path is unknown.

## Sensitive Fields That Must Be Rejected

Committed exchange fixtures must be rejected or regenerated if they contain:

- real API keys, API secrets, passphrases, access tokens, bearer tokens,
  session cookies, seed phrases, private keys, request signatures, or signed
  query strings;
- exchange account ids, user ids, UID values, subaccount ids, wallet ids,
  account balances, available balance, equity, margin balance, or private
  position size unrelated to the executed fill under test;
- real customer identifiers, trader names, emails, phone numbers, Telegram
  handles, payment ids, private notes, remarks, or support messages;
- raw source rows from prospects or paid pilots;
- enough combined fields to re-identify a person or account.

Fixture tests must scan both field names and representative string values for
these categories. A synthetic value is allowed only when it is clearly labeled
with a `synthetic_` prefix or appears inside fixture metadata that states the
record is synthetic.

## Required Metadata

Every committed exchange fixture file must include:

- `fixture_label`: `synthetic_exchange_fixture` or `sanitized_exchange_fixture`;
- `exchange`: `bybit` or `binance`;
- `endpoint_family`: for example `execution_history` or `account_trade_history`;
- `source_type`: `synthetic` or `sanitized`;
- `privacy_reviewed_by`;
- `privacy_review_date`;
- `fields_removed`;
- `intended_use`: `regression_test_only`;
- `records`: the raw-like execution or trade records.

`intended_use` must not say paid pilot, prospect evidence, PMF evidence,
customer validation, market proof, or production data.

## Allowed Raw Execution Fields

Allowed committed raw-like execution fields are limited to values needed for
deterministic normalization and pagination tests:

| Concept | Allowed example fields |
|---|---|
| Exchange and market scope | `exchange`, `category`, `market`, `symbol` |
| Execution identity | synthetic `exec_id`, synthetic `trade_id`, synthetic `order_id` |
| Execution timing | `exec_time`, `time`, `timestamp` |
| Side and liquidity | `side`, `is_buyer`, `is_maker`, `liquidity` |
| Quantity and price | `exec_qty`, `qty`, `quantity`, `exec_price`, `price` |
| Fees | `exec_fee`, `commission`, `fee_currency`, `commission_asset` |
| Pagination metadata | `cursor`, `next_page_cursor`, `window_start`, `window_end` |
| Source traceability | `source_row_id`, `fixture_record_id` |

Allowed identifiers must be synthetic and must not be copied from a real
account. Synthetic order/trade/execution ids should use readable prefixes such
as `synthetic_exec_001`, `synthetic_trade_001`, or `synthetic_order_001`.

## Redaction Rules

Before committing any sanitized exchange-like fixture, remove or replace:

- credentials, request headers, signatures, and signed query strings;
- account/user/subaccount identifiers;
- balances, equity, margin balance, wallet state, and account settings;
- names, emails, phone numbers, Telegram handles, and private notes;
- IP addresses and device/session identifiers;
- any exchange field that is not required for deterministic import tests.

Replacement values must be synthetic, stable, and visibly non-real. Do not use
real-looking long hexadecimal secrets, production-like API key prefixes, or
values copied from documentation examples if those examples look like secrets.

## Boundary

This policy does not approve exchange network calls. It only allows committed
synthetic or explicitly sanitized fixtures for future local import tests. Real
Binance/Bybit API access remains blocked until ADR-002 safety gates are complete
and a later task implements a bounded connector with credential permission
checks and redaction tests.
