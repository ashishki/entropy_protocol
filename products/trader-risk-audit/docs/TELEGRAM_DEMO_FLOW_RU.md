# Telegram Demo Flow RU

## Назначение

Этот документ описывает Phase 8 demo happy path для Telegram. Цель - показать
founder-led mini-product flow: пользователь видит понятный старт, может начать
audit request, может выбрать public sample demo без отправки private files,
получает audit id/status, а approved report delivery остается под контролем
оператора.

Это demo/intake surface, а не новый Telegram product scope.

## Happy Path

1. `/start` - объясняет, что доступен upload flow через `/new_audit` и public
   sample demo через `/demo_sample`.
2. `/new_audit` - просит trade export, written risk rules и intake metadata.
   Файлы сохраняются локально для operator review.
3. File upload - принимает только разрешенные file types и возвращает audit id
   со status `received`.
4. `/status` - возвращает non-sensitive status по audit id.
5. `/demo_sample` - показывает `demo_public_sample_001`, source label,
   selected starter profile, report path и delivery packet path.
6. Operator review - оператор локально проверяет artifacts и переводит request
   в `ready_for_review`.
7. Approved report delivery - отправляется только operator-approved delivery
   packet и report document. Delivery copy содержит required disclaimer.

## User-Facing Copy Boundaries

Allowed text:

- audit id;
- status labels like `received`, `ready_for_review`, `delivered`;
- local report path;
- local delivery packet path;
- source label: public/internal demo evidence, not paid pilot evidence;
- starter profile name: `soft`, `medium`, or `hard`;
- reminder that operator review is required before delivery.

Forbidden text:

- raw trade rows;
- Telegram handles;
- broker account ids;
- account balances;
- private notes;
- API keys, bearer tokens, passwords, seed phrases, or private keys;
- paid customer identifiers.

## ADR-001 Boundary

The Telegram demo must stay inside ADR-001:

- operator-approved report delivery only;
- no broker APIs;
- no signal parsing;
- no order blocking;
- no auto-advice;
- no live trading behavior;
- no AI-owned violation truth;
- no unapproved report delivery.

Telegram text may summarize approved deterministic report artifacts, but it must
not create new claims, modify evaluated values, infer missing rules, or provide
investment advice.

## Public Sample Boundary

The public sample demo uses `demo/public_sample_001/`. It is internal validation
and demo evidence only. It is not a qualified prospect call, paid pilot report,
repeat commitment, referral, PMF evidence, customer validation, or proof that
traders will pay.
