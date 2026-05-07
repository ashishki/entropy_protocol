# Trader Risk Audit Architecture

## Shape

Initial shape: concierge workflow plus deterministic local tooling.

Future shape after validation: deterministic import, rule evaluation, and
report generation components. No live execution.

## Data Flow

1. User provides trade export.
2. User provides written risk policy.
3. Import step normalizes trades into a canonical schema.
4. Rule engine evaluates violations deterministically.
5. Report generator summarizes violations and P&L impact.
6. Audit packet is stored append-only.

## Components

| Component | Purpose | MVP status |
|---|---|---|
| Trade import contract | Normalize CSV/export data | Proposed |
| Risk policy spec | Encode human-written rules | Proposed |
| Rule engine | Evaluate deterministic violations | Proposed |
| Report generator | Produce audit packet | Proposed |
| Telegram delivery | Send reports where users work | Deferred until validation |

## Boundaries

- No broker API.
- No order blocking.
- No live trade monitoring.
- No investment advice claims.
- No strategy performance claims.

