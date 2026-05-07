# Trader Risk Audit Spec

## MVP Inputs

- Executed trade export.
- Written risk rules.
- Timezone/session definition.
- Optional account/equity baseline for drawdown and daily-loss rules.

## MVP Rules

| Rule | Description | MVP |
|---|---|---|
| Max daily loss | Flag trading after daily loss threshold | Yes |
| Max drawdown | Flag equity drawdown breach | Yes |
| Cooldown after loss | Flag trades during cooldown window | Yes |
| Max position size | Flag position size above policy | Yes |
| Forbidden assets | Flag trades in disallowed instruments | Yes |
| Max leverage | Flag leverage above policy when data exists | Later |
| Strategy adherence | Compare trades to named playbook rules | Later, manual first |

## MVP Outputs

- Violation list.
- Violating vs compliant P&L.
- Worst violation days.
- Repeated behavior patterns.
- Rule-by-rule summary.
- Audit packet ID.

## Explicit Cuts

- No SaaS dashboard.
- No live broker connection.
- No automated order blocking.
- No AI-generated strategy code.
- No marketplace.

