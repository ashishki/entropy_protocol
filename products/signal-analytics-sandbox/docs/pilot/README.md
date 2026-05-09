# Pilot Docs

Эта папка хранит рабочие артефакты пилота по трем публичным Telegram-группам:

- `https://t.me/bablos79`
- `https://t.me/nemphiscrypts`
- `https://t.me/pifagortrade`

Главный план пилота: `../PILOT_DEVELOPMENT_LOOP_RU.md`.
Roadmap автоматизации: `AUDIT_GRADE_AUTOMATION_ROADMAP.md`.
Текущий Phase 10 план: `AUTO_EXTRACTION_DEVELOPMENT_PLAN.md`.

## Следующие документы

Создать в первую очередь:

1. `PILOT_SCOPE.md` - какие источники, какой период, сколько сигналов, что входит и не входит.
2. `METHODOLOGY_V0.md` - как извлекаем сигналы, что считаем ambiguous, как считаем outcomes.
3. `CAPTURE_LOG.md` - какие посты захвачены и откуда.
4. `EXTRACTION_LOG.md` - какие сигналы утверждены, исключены или спорные.
5. `CUSTOMER_FEEDBACK.md` - что сказал заказчик после отчета.

Правило: автоматизация может делать draft/pseudo-labels, validators и review
queue, но approved ledger и customer-facing claims требуют exception review.
