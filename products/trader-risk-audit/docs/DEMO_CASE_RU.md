# Demo Case RU - Risk Audit Case 001

## Назначение

Этот материал является демонстрационным примером для первых разговоров с трейдерами и командами. Все сделки, правила, даты, символы, account id и результаты в `demo/risk_audit_case_001/` являются синтетическими.

Демо показывает формат результата: какие детерминированные проверки выполняются, как отчет ссылается на source rows, как считается violation-attributed P&L и какой короткий текст можно подготовить для ручной доставки.

## Что входит

- `trades.csv` - синтетический trade export.
- `policy.yaml` - синтетическая risk policy с лимитом дневного убытка, cooldown, forbidden asset и max position size.
- `output/report.md` - сгенерированный Markdown report.
- `output/telegram_packet.txt` - Telegram-ready текст для ручного копирования, без отправки ботом.
- `output/manifest.json` - manifest с content hashes для артефактов локального audit workflow, включая `telegram_packet.txt`.

## Как использовать на demo call

Основной message: Trader Risk Audit превращает trade export и written risk rules в reproducible audit report. В отчете видны timestamps, source row ids, deterministic violations, repeated patterns, limitations и P&L attribution.

Показывать этот кейс можно только как пример artifact quality и workflow shape. Он не является market validation, доказательством готовности платить, доказательством прибыльности стратегии или обещанием результата для реального трейдера.

## Claim Boundaries

- Данные полностью синтетические и не являются customer export.
- Отчет не является инвестиционной рекомендацией.
- Отчет не доказывает качество торговой стратегии.
- Отчет не обещает profit, не моделирует counterfactual returns и не объясняет причину убытков без детерминированных evidence fields.
- Продукт не подключается к broker/exchange API, не управляет live orders и не блокирует сделки.
- Telegram-ready packet является copyable delivery text only; бот, credentials и автоматическая отправка не входят в этот demo case.

## Pilot framing

Demo case можно показать до запроса реальных exports/rules, чтобы prospect понимал формат результата. После demo нужно переходить к behavioral questions, payment test и сбору настоящего trade export только через утвержденный pilot intake process.
