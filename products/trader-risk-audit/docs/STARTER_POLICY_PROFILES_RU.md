# Starter Risk Policy Profiles

Purpose:

Дать оператору и основателю три стартовых профиля строгости для internal validation и demo-пакетов: `soft`, `medium`, `hard`. Это не инвестиционный совет, не рекомендация по стратегии и не обещание улучшить результат. Профили нужны только как воспроизводимые audit presets, чтобы проверить дисциплину сделок против явных правил.

## Ownership Boundary

Правила могут приходить из трех источников:

- Trader custom rules: личные правила трейдера, записанные до аудита.
- Prop/funded account rules: внешние лимиты счета, например daily loss, max loss, forbidden behavior.
- Starter templates: наши `soft`, `medium`, `hard` профили как начальная точка для внутреннего теста или demo.

Кастомизация приветствуется и ожидается. Если у трейдера есть собственные правила или prop account limits, они имеют приоритет над starter templates. Оператор должен зафиксировать, какие значения изменены, почему изменены, и кто их утвердил.

## Calibration Assumption

YAML-шаблоны используют примерный account equity `100000 USD`, потому что текущий deterministic evaluator принимает абсолютные USD thresholds, а не процентные thresholds. Процентные уровни ниже объясняют логику профилей; перед реальным аудитом значения нужно пересчитать под фактический капитал, стиль, инструмент, таймфрейм и правила счета.

## Profiles

| Profile | Use case | Rationale | Template |
|---|---|---|---|
| Soft | Трейдер хочет увидеть только крупные discipline breaches без агрессивных false positives. | Daily loss около 3%, drawdown около 8%, короткий cooldown, широкий position limit. | `templates/policies/starter_policy_soft.yaml` |
| Medium | Базовый internal validation и demo profile. | Daily loss около 2%, drawdown около 5%, средний cooldown, умеренный position limit. | `templates/policies/starter_policy_medium.yaml` |
| Hard | Prop/funded trader, trader после серии discipline breaches, или internal stress test. | Daily loss около 1%, drawdown около 3%, длинный cooldown, строгий position limit. | `templates/policies/starter_policy_hard.yaml` |

## What These Profiles Do Not Claim

- They do not say which trades should be opened or closed.
- They do not say the profile is optimal for a strategy.
- They do not predict performance or reduce trading risk by themselves.
- They do not replace written trader rules, prop rules, or operator-approved policy mapping.
- They do not turn public sample validation into paid pilot evidence.

## Internal Validation Use

For Phase 7 public-sample validation, run the same normalized sample against `soft`, `medium`, and `hard` where possible. The expected behavior is that stricter profiles produce equal or more discipline flags, but the review should focus on explainability and source-row traceability, not on proving that `hard` is better.

Readiness signal:

- The profile chosen for a report is visible in source metadata.
- The report states that starter profiles are audit presets, not trading advice.
- Violations are explainable from source rows.
- A founder can explain the difference between `soft`, `medium`, and `hard` in under two minutes.
