# Two-Minute Demo Script RU

Назначение: founder-led sales call script для Trader Risk Audit. Цель - показать
понятный mini-product path и перейти к реальному evidence: real trade export,
written risk rules и paid manual pilot.

## 0:00-0:20 - Problem

Сказать:

"У большинства трейдеров есть правила, которые они хотели соблюдать, но после
торгового дня сложно быстро увидеть, где именно дисциплина сломалась и какой
P&L impact дали эти нарушения. Этот audit берет executed trades и written risk
rules, а затем строит deterministic report."

Не говорить: что результат торговли улучшится, что убытки были вызваны одним
правилом, или что продукт должен решать будущие сделки.

## 0:20-0:40 - Upload

Показать Telegram или local CLI intake:

- upload trade export;
- upload или select written policy;
- получить audit id и status;
- operator reviews ambiguous mapping before delivery.

Сказать:

"В demo используется public sample. Для вашего audit мне нужны real trade
export и written risk rules. Public sample is not market validation and is not
PMF evidence."

## 0:40-0:55 - Selected Profile

Показать selected profile: `hard`.

Сказать:

"Soft, medium и hard - это customizable audit presets. Это not investment
advice, не strategy recommendations и not optimal risk settings. Trader custom
rules и prop/funded account rules имеют приоритет. Если у вас уже есть custom
rules, мы аудируем их, а не заставляем starter profile."

Объяснение profiles:

- soft: более широкие thresholds, обычно меньше discipline flags;
- medium: baseline internal validation profile;
- hard: более строгий stress-test profile;
- custom rules: preferred path для real pilots, когда у trader есть written
  rules.

## 0:55-1:25 - Report Summary

Показать верх `demo/public_sample_001/output/report.md`.

Сказать:

"Report начинается с executive summary: rules reviewed, violations recorded,
affected P&L и selected profile. Затем идут detailed violation table, P&L
attribution, limitations и next review checklist."

Показать:

- report summary;
- rules reviewed;
- violations recorded;
- affected P&L;
- selected profile.

## 1:25-1:45 - Evidence

Показать violation table.

Сказать:

"Каждый violation сохраняет source row ids, timestamp, evaluated value,
threshold, severity и P&L impact. Поэтому каждый flag можно проследить до
input row, а не обсуждать расплывчатый coaching feedback."

Показать:

- source row ids;
- timestamp;
- evaluated value и threshold;
- P&L impact;
- limitations для unsupported или missing data.

## 1:45-2:00 - Next Pilot Ask

Сказать:

"Next pilot ask простой: отправьте real trade export и written risk rules,
утвердите mapping questions и купите один manual audit. Я проверяю, достаточно
ли полезен report, чтобы за него платить, а не собираю список новых features."

Закрыть:

"This audit is not investment advice and does not control live trading. Здесь
no broker APIs, no signal parsing, no order blocking, no auto-advice и no
performance promise."

## Claim Boundary

- Public sample is internal/demo evidence only.
- Public sample is not market validation, not PMF evidence, not qualified
  prospect call, not paid pilot report, not repeat commitment и not referral.
- Audit описывает rule violations в executed trades. Он does not control live
  trading, не выпускает signals, не places orders, не block orders и не обещает
  trading outcomes.
