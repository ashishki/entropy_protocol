# Entropy Protocol — Краткий бриф для архитектора
**Классификация:** Confidential — Onboarding Document
**Файл:** `products/entropy-core/docs/audience/ARCHITECT_BRIEF.md`
**Аудитория:** CTO / Staff+ Architect / Lead Engineer
**Версия:** 2.0
**Дата:** 2026-03-16

## Что это за проект

Entropy Protocol — не торговый бот и не набор сигналов.

Это каркас для исследования, проверки и поэтапного допуска систематических торговых гипотез.

Главная идея:
- сначала строится инфраструктура оценки
- потом гипотезы проходят preregistration
- потом идут walk-forward и paper evaluation
- и только потом возможен переход к капиталу

Проект намеренно построен так, чтобы мешать:
- переобучению
- ручной подгонке
- хаотическому перебору идей

## Зачем он нужен

Если система торгует без жесткой оценки, то команда не знает, где реальный edge, а где шум.

Entropy Protocol нужен, чтобы:
- отделить research от admissible evidence
- держать trial count под контролем
- не смешивать торговый P&L с treasury yield
- принимать решения о развитии системы по правилам, а не по впечатлению

## Структура проекта

### `products/entropy-core/docs/core/`
- `PROTOCOL_SPEC.md` — главная инженерная спецификация
- `CHARTER.md` — стратегические ограничения и non-negotiables
- `EVOLUTION.md` — почему система устроена именно так
- `GLOSSARY.md` — термины

### `products/entropy-core/docs/architecture/`
- AI framework
- workflow
- system architecture
- Research Discovery Layer
- Research Knowledge Graph

### `products/entropy-core/docs/governance/`
- Research Firewall
- Hypothesis Families
- Experiment Readiness Gate

### `products/entropy-core/docs/research/`
- актуальные research reports

### `products/entropy-core/docs/audit/`
- audit pipeline и текущие findings

### `products/entropy-core/docs/audience/`
- короткие документы для конкретных ролей

### `products/entropy-core/docs/archive/`
- исторические reasoning artifacts

## Что система делает

На практическом уровне система должна уметь:
- собирать и нормализовать market data
- прогонять гипотезы через walk-forward evaluation
- симулировать исполнение через SimBroker
- считать P&L по 4 потокам
- держать Trial Registry и multiplicity control
- управлять риском через режимные и структурные правила

## Чего она не делает

Сейчас это не:
- live execution stack
- discretionary trading terminal
- ML-платформа для auto-discovery alpha
- AI-агент, который сам принимает портфельные решения

AI в этой системе помогает исследовать, но не авторизует протокольные действия.

## Архитектурные слои

1. Data Layer
   Хранение и подготовка OHLCV и связанных данных.

2. Evaluation Layer
   Walk-forward harness, Trial Registry, leakage control, SimBroker.

3. Strategy / Portfolio Layer
   Сигналы, sizing, correlation control, regime routing.

4. Research Discovery Layer
   AI-assisted observation, hypothesis generation, critique, experiment proposal.

5. Governance Layer
   Firewall, readiness gate, family tracking, hypothesis budget.

## Ключевые ограничения

- Gross leverage не выше 1.0
- Net Sharpe считается только по trading book: `(a)+(b)+(c)`
- Treasury P&L всегда отдельно
- Ни одна гипотеза не считается valid OOS без evaluation engine
- Фазы идут строго последовательно
- Frozen rules нельзя менять “по месту”

## Что будет мочь система по фазам

### Phase 0
- построить evaluation engine
- настроить SimBroker
- поднять Trial Registry
- зафиксировать research governance

### Phase 1
- получить long-only baseline
- проверить, есть ли вообще рабочая торговая база

### Phase 2
- добавить weekly regime overlay
- проверить, улучшает ли он baseline

### Phase 3
- добавить equity shorts в paper-first режиме

### Phase 4
- опционально рассмотреть crypto perp shorts
- базовый план: скорее bypass, если funding economics плохая

### Phase 5
- включить treasury layer после подтверждения trading viability

## Почему это архитектурно разумно

Для CTO здесь главное не “еще одна стратегия”, а controlled research system.

Ценность проекта в том, что он:
- делает результаты воспроизводимыми
- уменьшает governance drift
- отделяет discovery от evaluation
- позволяет маленькой команде накапливать research memory без потери дисциплины

## Что важно архитектору в первую очередь

Смотреть сначала сюда:
1. `products/entropy-core/docs/core/PROTOCOL_SPEC.md`
2. `products/entropy-core/docs/core/CHARTER.md`
3. `products/entropy-core/docs/architecture/system_architecture.md`
4. `products/entropy-core/docs/architecture/workflow_ai_development.md`
5. `products/entropy-core/docs/audit/REVIEW_REPORT.md`

Главный вопрос для архитектурной оценки:
может ли система оставаться строго проверяемой по мере роста research surface.
