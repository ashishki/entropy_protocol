# Risk Rules Template RU

Заполните правила своими словами. Можно писать так, как вы обычно объясняете
правила себе, coach или team lead. Не добавляйте API keys, пароли, реальные
broker account ids, Telegram handles, email или другие личные данные.

## Current Rules

Для каждого правила укажите:

- название правила;
- threshold и unit;
- период действия: session/day/week/account/instrument;
- что считается нарушением;
- с какой даты правило действует;
- пример сделки или ситуации, где правило должно сработать.

## Past Rules

Если в audit period правила менялись, укажите старую версию:

- какое правило действовало раньше;
- когда оно было изменено;
- почему оно было изменено;
- какие сделки относятся к старой версии.

## Ambiguity Review

Если правило звучит неоднозначно, оператор должен явно утвердить deterministic
mapping до evaluation. Ambiguous rules, unsupported rule types и новые rule
semantics не интерпретируются автоматически и не используются для violation
truth без operator approval.

Примеры неоднозначности:

- "не переторговать" без числового лимита;
- "остановиться после плохой сделки" без loss threshold и cooldown minutes;
- "не брать большой размер" без max position size и unit;
- "не торговать новости" без списка symbols, time window или source rule.
